# Internet Data Management: Ontology and PageRank

My CS BSc coursework.

## Project Summary

Python scripts for crawling web links, calculating PageRank, building an RDF football ontology, and running SPARQL-style ontology queries.

## Tech Stack

Python 3, requests, lxml, rdflib, RDF/N-Triples, SPARQL-style queries, PageRank.

## Repository Layout

- `assignment/` contains the supplied exercise handout or tests recovered for this coursework.
- The repository root contains the recovered submitted source, data, and text-output artifacts needed to inspect the solution.
- `scripts/check_repository.py` performs static repository validation.

Submission ZIP wrappers, Apple metadata, official solution PDFs, and office-document/PDF answer exports were intentionally omitted from this repository.

## Validate

Run:

```sh
make check
```

Install Python dependencies with:

```sh
python3 -m pip install -r requirements.txt
```

The validator is static and does not access the network. Original scraping scripts may require live web access if run directly.
