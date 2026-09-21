# Internet Data Management: Ontology and PageRank

- Authors: Kobie Hazon and Adi Eldar.

The supplied exercise files are in `assignment/`. My code is kept separately, along with the data and answers.

## Project Summary

Python scripts for crawling web links, calculating PageRank, building an RDF football ontology, and running SPARQL-style ontology queries.

## Tech Stack

Python 3, requests, lxml, rdflib, RDF/N-Triples, SPARQL-style queries, PageRank.

## Validate

Run:

```sh
make test
```

Install Python dependencies with:

```sh
uv venv
uv pip install -r requirements.txt
```

`make test` checks incoming-link, scraping, and ontology-query semantics. `make test-live` crawls three public Wikipedia pages and builds a small football graph from a league-season page, team roster, player, and cities. It has a request limit and timeouts; it does not use account credentials. Live website content can change.

## Written answers

My submission with Adi Eldar is in [written-answers.pdf](solution/written-answers.pdf).

## Repository layout

- `src/`: Python implementations.
- `assignment/`: Exercise briefs and supplied inputs.
- `data/`: Input data and test fixtures.
- `solution/`: Written answers.
- `results/`: Submitted output files.
- `tests/`: Executable regression tests.
- `scripts/`: Bounded live-web tests.

Run `make test` from the repository root. The tests use local fixtures; they do not scrape live websites.

Saved-data queries: `uv run --no-project --with-requirements requirements.txt python src/ontology_queries.py data/ontology.nt`. The live ontology generator writes `run-results/ontology.nt`; pass that path to query a new run without overwriting the dataset.

For a bounded live ontology run:

```sh
uv run --no-project --with-requirements requirements.txt python src/football_ontology.py 'https://en.wikipedia.org/wiki/2018%E2%80%9319_Premier_League' --max-teams 1 --max-players 1
```

The season page supplies the team list; linked club pages supply their current rosters, not a historical snapshot of that season.
