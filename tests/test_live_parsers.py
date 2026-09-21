import unittest
from unittest.mock import Mock, patch
import rdflib
import football_ontology as football
import question3a

class ParserTests(unittest.TestCase):
    def test_crawler_accepts_absolute_links_and_stays_on_site(self):
        root = 'https://en.wikipedia.org/wiki/Start'
        page = Mock(content=b'<a href="https://en.wikipedia.org/wiki/Next">next</a><a href="/wiki/Next#section">duplicate</a><a href="https://evil.test/wiki/Other">external</a><a href="/wiki/Category:Other">category</a>')
        with patch('public_web.get', return_value=page) as get:
            links = question3a.crawler(root, max_pages=1)
        self.assertEqual(links[root], {'https://en.wikipedia.org/wiki/Next'})
        get.assert_called_once_with(root)

    def test_football_follows_team_player_city_and_writes_relations(self):
        prefix='https://en.wikipedia.org/wiki/'
        pages = {
            prefix+'Season': b'<table><tr><th>Team</th><th>Location</th></tr><tr><td><a href="/wiki/Club">Club</a></td><td><a href="/wiki/City">City</a></td></tr></table>',
            prefix+'City': b'<table class="infobox"><tbody><tr><th>Country</th><td><a>Country</a></td></tr></tbody></table>',
            prefix+'Club': b'<table class="infobox"><tbody><tr><th>League</th><td><a>League</a></td></tr></tbody></table><table><tr class="vcard agent"><td>1</td><td><abbr>GK</abbr></td><td>XX</td><td><span class="fn"><a href="https://en.wikipedia.org/wiki/Player">Player</a></span></td></tr></table>',
            prefix+'Player': b'<table class="infobox"><tbody><tr><th>Date of birth</th><td><span class="bday">1995-01-02</span></td></tr><tr><th>Place of birth</th><td><a href="/wiki/City">City</a></td></tr></tbody></table>',
        }
        with patch('public_web.get', side_effect=lambda url: Mock(content=pages[url])) as get:
            graph=football.process_flow(prefix+'Season',max_teams=1,max_players=1)
        n=rdflib.Namespace(football.ontology_prefix)
        self.assertIn((n.Player,n.playsFor,n.Club),graph)
        self.assertIn((n.Player,n.birthPlace,n.City),graph)
        self.assertIn((n.City,n.located_in,n.Country),graph)
        self.assertIn((n.Club,n.league,n.League),graph)
        self.assertEqual(get.call_count,5)
