import rdflib
from rdflib import Literal, XSD
import requests
import sys
import lxml.html

infobox_prefix = "//table[contains(@class,'infobox')]/tbody"
def process_city(city_entity, city_url):
    city_html = requests.get(city_url)
    city_page = lxml.html.fromstring(city_html.content)
    countries = city_page.xpath(
        infobox_prefix + "/tr[.//*[contains(translate(text(),'C','c'),'country')]]//td//a/text()")
    if len(countries) > 0:
        country = countries[0].replace(" ", "_")
        country_entity = rdflib.URIRef(ontology_prefix + country)
        located_in_relation = rdflib.URIRef(ontology_prefix + 'located_in')
        g.add((city_entity, located_in_relation, country_entity))


def process_player(team_entity, player_name, player_position, player_url):
    player_html = requests.get(player_url)
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

        city_url = wiki_dom + player_page.xpath(
            infobox_prefix + "/tr[./th[contains(text(),'Place of birth')]]/td/a/@href")[0]
        process_city(city_entity, city_url)


def process_team(team_name, team_url, team_city):
    team_html = requests.get(team_url)
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

    players_table = "//h2[./span/text()='Players']/following-sibling::table[1]//tr[@class='vcard agent']"
    playeres_positions = team_page.xpath(players_table + "/td[3]/a/text()")
    players_names = team_page.xpath(players_table + "/td[4]/span/a/text()")
    players_urls = team_page.xpath(players_table + "/td[4]/span/a/@href")

    for i in range(0, len(players_names)):
        process_player(team_entity, players_names[i].replace(
            " ", "_"), playeres_positions[i],  wiki_dom + players_urls[i])


def process_flow():
    team_table_str = "//h2[./span/text()='Teams']/following-sibling::table[1]"
    city_url = wiki_dom + \
        page.xpath(team_table_str + "/tbody/tr[2]/td[2]/a/@href")[0]
    city_html = requests.get(city_url)
    league_country = lxml.html.fromstring(city_html.content).xpath(
        infobox_prefix + "/tr[.//*[contains(text(),'country')]]/td//text()")[0]
    league_country_entity = rdflib.URIRef(ontology_prefix + league_country)
    league_name = page.xpath(
        "//table[contains(@class,'infobox')]/caption/a/text()")[0].replace(" ", "_")
    print(league_name)
    league_entity = rdflib.URIRef(ontology_prefix + league_name)
    country_relation = rdflib.URIRef(ontology_prefix + 'country')
    g.add((league_entity, country_relation, league_country_entity))

    rows_num = page.xpath("count(" + team_table_str + "/tbody/tr)")
    for i in range(2, int(rows_num) + 1):
        team_name = page.xpath(
            team_table_str + "/tbody/tr[" + str(i) + "]/td[1]/a/text()")[0].replace(" ", "_")
        team_url = wiki_dom + \
            page.xpath(team_table_str +
                       "/tbody/tr[" + str(i) + "]/td[1]/a/@href")[0]
        team_city = page.xpath(
            team_table_str + "/tbody/tr[" + str(i) + "]/td[2]//text()")[0].strip().replace(" ", "_")
        cities = page.xpath(
            team_table_str + "/tbody/tr[" + str(i) + "]/td[2]/a/@href")
        if len(cities) > 0:
            team_city_url = wiki_dom + cities[0]
            city_entity = rdflib.URIRef(ontology_prefix + team_city)
            process_city(city_entity, team_city_url)
        process_team(team_name, team_url, team_city)

    g.serialize("ontology.nt", format="nt")
    sorted(g)


if len(sys.argv) == 2:
    url = sys.argv[1]
else:
    exit(0)

ontology_prefix = "http://example.org/"
wiki_dom = "https://en.wikipedia.org/"
html = requests.get(url)
page = lxml.html.fromstring(html.content)

g = rdflib.Graph()
process_flow()
