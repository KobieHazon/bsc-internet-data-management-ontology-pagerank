from pathlib import Path
from urllib.parse import urljoin

import rdflib
from rdflib import Literal, XSD
import public_web
import sys
import lxml.html

infobox_prefix = "//table[contains(@class,'infobox')]/tbody"
def process_city(city_entity, city_url):
    city_html = public_web.get(city_url)
    city_page = lxml.html.fromstring(city_html.content)
    countries = city_page.xpath(
        infobox_prefix + "/tr[.//*[contains(translate(text(),'C','c'),'country')]]//td//a/text()")
    if len(countries) > 0:
        country = countries[0].replace(" ", "_")
        country_entity = rdflib.URIRef(ontology_prefix + country)
        located_in_relation = rdflib.URIRef(ontology_prefix + 'located_in')
        g.add((city_entity, located_in_relation, country_entity))


def process_player(team_entity, player_name, player_position, player_url):
    player_html = public_web.get(player_url)
    player_page = lxml.html.fromstring(player_html.content)

    player_entity = rdflib.URIRef(ontology_prefix + player_name)
    birth_dates = player_page.xpath(
        infobox_prefix + "/tr[./th[contains(text(),'Date of birth')]]/td//*[@class='bday']/text()")
    if len(birth_dates) > 0:
        birth_date = birth_dates[0]
        birth_date_entity = Literal(birth_date, datatype=XSD.date)
        birth_date_relation = rdflib.URIRef(ontology_prefix + 'birthDate')
        g.add((player_entity, birth_date_relation, birth_date_entity))
    position_entity = rdflib.URIRef(ontology_prefix + player_position)
    plays_for_relation = rdflib.URIRef(ontology_prefix + 'playsFor')
    position_relation = rdflib.URIRef(ontology_prefix + 'position')
    g.add((player_entity, plays_for_relation, team_entity))
    g.add((player_entity, position_relation, position_entity))
    cities = player_page.xpath(
        infobox_prefix + "/tr[./th[contains(text(),'Place of birth')]]/td/a/text()")
    if len(cities) > 0:
        player_city = cities[0].replace(" ", "_")
        city_entity = rdflib.URIRef(ontology_prefix + player_city)
        birth_place_relation = rdflib.URIRef(ontology_prefix + 'birthPlace')
        g.add((player_entity, birth_place_relation, city_entity))

        city_url = urljoin(player_url, player_page.xpath(
            infobox_prefix + "/tr[./th[contains(text(),'Place of birth')]]/td/a/@href")[0])
        process_city(city_entity, city_url)


def process_team(team_name, team_url, team_city, max_players=None):
    team_html = public_web.get(team_url)
    team_page = lxml.html.fromstring(team_html.content)

    team_entity = rdflib.URIRef(ontology_prefix + team_name)
    leagues = team_page.xpath(
        infobox_prefix + "/tr[./th[contains(text(),'League')]]/td//text()")
    if len(leagues) > 0:
        league_entity = rdflib.URIRef(
            ontology_prefix + leagues[0].replace(" ", "_"))
        league_relation = rdflib.URIRef(ontology_prefix + "league")
        g.add((team_entity, league_relation, league_entity))
    city_entity = rdflib.URIRef(ontology_prefix + team_city)
    home_city_relation = rdflib.URIRef(ontology_prefix + "homeCity")
    g.add((team_entity, home_city_relation, city_entity))

    rows = team_page.xpath("//tr[contains(concat(' ',normalize-space(@class),' '), ' agent ')]")
    if not rows:
        raise ValueError("Team roster not found")
    for row in rows[:max_players]:
        names = row.xpath("./td[last()]//span[contains(@class,'fn')]/a[1]")
        positions = row.xpath("./td[2]//abbr/text()")
        if not names or not positions:
            raise ValueError("Unrecognized roster row")
        player = names[0]
        process_player(team_entity, player.text_content().strip().replace(' ', '_'),
                       positions[0], urljoin(team_url, player.get('href')))

def process_flow(url, max_teams=None, max_players=None, output=None):
    global g
    g = rdflib.Graph()
    page = lxml.html.fromstring(public_web.get(url).content)
    tables = page.xpath("//table[.//th[normalize-space(.)='Team'] and .//th[normalize-space(.)='Location']]")
    if not tables:
        raise ValueError("Use a league season page containing the Team/Location table")
    rows = tables[0].xpath('.//tr[td]')
    if not rows:
        raise ValueError("League team table is empty")
    for row in rows[:max_teams]:
        teams = row.xpath('./td[1]/a[1]')
        cities = row.xpath('./td[2]/a[1]')
        if not teams or not cities:
            raise ValueError("Unrecognized team/location row")
        team, city = teams[0], cities[0]
        city_name = city.text_content().strip().replace(' ', '_')
        process_city(rdflib.URIRef(ontology_prefix + city_name), urljoin(url, city.get('href')))
        process_team(team.text_content().strip().replace(' ', '_'),
                     urljoin(url, team.get('href')), city_name, max_players=max_players)
    if output is not None:
        output = Path(output)
        output.parent.mkdir(parents=True, exist_ok=True)
        g.serialize(output, format='nt')
    return g

ontology_prefix = "http://example.org/"
g = rdflib.Graph()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Build football RDF from a Wikipedia league-season page and its linked current rosters.')
    parser.add_argument('url')
    parser.add_argument('--max-teams', type=int)
    parser.add_argument('--max-players', type=int)
    parser.add_argument('--output', type=Path, default=Path(__file__).resolve().parents[1]/'run-results/ontology.nt')
    args = parser.parse_args()
    if any(value is not None and value < 1 for value in [args.max_teams, args.max_players]):
        parser.error('Limits must be positive')
    process_flow(args.url, args.max_teams, args.max_players, args.output)
