# Internet Data Management: Ontology and PageRank

My CS BSc coursework.

## Project Summary

Python scripts for crawling web links, calculating PageRank, building an RDF football ontology, and running SPARQL-style ontology queries.

## Tech Stack

Python 3, requests, lxml, rdflib, RDF/N-Triples, SPARQL-style queries, PageRank.

## Provenance

The supplied exercise material is preserved under `assignment/`. Recovered authored source, data, and answers are organized separately; earlier commits remain unchanged.

Submission ZIP wrappers, Apple metadata, official solution PDFs, and office-document/PDF answer exports were intentionally omitted from this repository.

## Validate

Run:

```sh
make check
make test
```

Install Python dependencies with:

```sh
uv venv
uv pip install -r requirements.txt
```

The repository check is static. The regression tests exercise incoming-link and ontology-query semantics without network access. Original scraping scripts may require live web access if run directly.

## Repository layout

- `src/`: authored Python scripts, preserving the coursework filenames and sibling imports.
- `data/`: recovered reference data or HTML/CSV fixtures.
- `assignment/`: supplied exercise material, unchanged.
- `tests/` and `scripts/`: offline regression checks and repository validation.
- `results/` or `solution/` (where present): recovered outputs and written/XML answers.
- `run-results/` (where used): ignored output from new runs, separate from recovered evidence.

Run `make check` and `make test` from the repository root. The tests use local fixtures; they do not scrape live websites.

Saved-data queries: `uv run --no-project --with-requirements requirements.txt python src/ontology_queries.py data/ontology.nt`. The live ontology generator writes `run-results/ontology.nt`; pass that path to query a new run without overwriting the recovered dataset.
