import contextlib
import io
from pathlib import Path
import runpy
import sys
import tempfile
import unittest

import rdflib

import question3b


class PageRankAndQueryTests(unittest.TestCase):
    def test_incoming_links_to_seed_are_preserved(self):
        seed = "https://example.test/seed"
        other = "https://example.test/other"
        incoming = question3b.in_url_generator(
            {seed: {other}, other: {seed}}
        )
        self.assertEqual(incoming[seed], {other})
        self.assertEqual(incoming[other], {seed})

    def test_date_query_excludes_players_born_before_1995(self):
        namespace = rdflib.Namespace("http://example.org/")
        graph = rdflib.Graph()
        graph.add((namespace.Alice, namespace.playsFor, namespace.Arsenal))
        graph.add(
            (
                namespace.Alice,
                namespace.birthDate,
                rdflib.Literal("1996-02-03", datatype=rdflib.XSD.date),
            )
        )
        graph.add((namespace.Bob, namespace.playsFor, namespace.Chelsea))
        graph.add(
            (
                namespace.Bob,
                namespace.birthDate,
                rdflib.Literal("1990-04-05", datatype=rdflib.XSD.date),
            )
        )

        script = Path(__file__).resolve().parents[1] / "src" / "ontology_queries.py"
        with tempfile.NamedTemporaryFile(suffix=".nt") as ontology:
            graph.serialize(ontology.name, format="nt")
            old_argv = sys.argv[:]
            try:
                sys.argv = ["ontology_queries.py", ontology.name]
                with contextlib.redirect_stdout(io.StringIO()):
                    query_namespace = runpy.run_path(str(script), run_name="query_test")
            finally:
                sys.argv = old_argv

        actual = {
            tuple(str(value) for value in row)
            for row in query_namespace["g"].query(query_namespace["query2"])
        }
        self.assertEqual(
            actual,
            {("http://example.org/Alice", "http://example.org/Arsenal")},
        )


if __name__ == "__main__":
    unittest.main()
