"""Bounded, anonymous integration check against public Wikipedia pages."""
import contextlib
import io
from pathlib import Path
import runpy
import sys
import tempfile
import time
from urllib.parse import urlsplit
from unittest.mock import patch

import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
session = requests.Session()
session.trust_env = False  # Do not use machine credentials, proxies, or .netrc.
session.headers["User-Agent"] = "CourseworkIntegrationCheck/1.0 (bounded anonymous test)"
calls = []

def get(url, **kwargs):
    parsed = urlsplit(url)
    if parsed.scheme != "https" or parsed.hostname != "en.wikipedia.org" or parsed.username:
        raise ValueError("Only anonymous HTTPS Wikipedia requests are allowed")
    if len(calls) >= 12:
        raise RuntimeError("Request budget exhausted")
    if calls:
        time.sleep(0.4)
    calls.append(url)
    session.cookies.clear()
    response = session.get(url, timeout=20, allow_redirects=False)
    response.raise_for_status()
    if response.is_redirect:
        raise RuntimeError("Unexpected redirect; inspect the public URL before retrying")
    return response

with patch("public_web.get", side_effect=get):
    import question3a
    import question3b
    question3a.DEPTH_LIMIT = 1
    links = question3a.crawler("https://en.wikipedia.org/wiki/Computer_science", max_pages=3)
    assert len(links) == 3 and all(links.values())
    incoming = question3b.in_url_generator(links)
    assert incoming
    print("Live bounded crawl and incoming-link graph passed: %d pages" % len(links))
    import football_ontology
    import rdflib
    graph = football_ontology.process_flow("https://en.wikipedia.org/wiki/2018%E2%80%9319_Premier_League", max_teams=1, max_players=1)
    namespace = rdflib.Namespace(football_ontology.ontology_prefix)
    assert list(graph.triples((None, namespace.playsFor, None)))
    assert list(graph.triples((None, namespace.birthDate, None)))
    assert list(graph.triples((None, namespace.homeCity, None)))
    print("Live team/player/city RDF generation passed: %d triples" % len(graph))
print("Anonymous requests: %d" % len(calls))
