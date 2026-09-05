import rdflib
import sys
ontology_prefix = "http://example.org/"

query1 = "select ?player ?team where {?player <" + ontology_prefix + "playsFor> ?team. \
         ?team <" + ontology_prefix + "league> <" + ontology_prefix + "Premier_League>. \
         ?player <" + ontology_prefix + "birthPlace> ?city. \
         ?city <" + ontology_prefix + "located_in> <" + ontology_prefix + "Brazil>}"

query2 = "select ?player ?team where {?player <" + ontology_prefix + "playsFor> ?team. \
         ?player <" + ontology_prefix + "birthDate> ?date. \
         FILTER(?date >= '1995-01-01'^^xsd:date)}"

query3 = "select ?player where {?player <" + ontology_prefix + "playsFor> ?team. \
         ?team <" + ontology_prefix + "homeCity> ?city. \
         ?player <" + ontology_prefix + "birthPlace> ?city}"

query4 = "select ?team1 ?team2 where {?team1 <" + ontology_prefix + "homeCity> ?city. \
         ?team2 <" + ontology_prefix + "homeCity> ?city. \
         FILTER(?team1 != ?team2)}"

g = rdflib.Graph()
if len(sys.argv) < 2:
    exit(0)
g.parse(sys.argv[1], format="nt")
print("query1:\n")
print(list(g.query(query1)))
print("\n#############################################################\n")
print("query2:\n")
print(list(g.query(query2)))
print("\n#############################################################\n")
print("query3:\n")
print(list(g.query(query3)))
print("\n#############################################################\n")
print("query4:\n")
print(list(g.query(query4)))
