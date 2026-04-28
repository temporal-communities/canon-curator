"""
Base URIs used across the load module zo build pyoxigraph NamedNodes with:

    ox.NamedNode(RDF + "type")
    ox.NamedNode(CANON + "Work")

The PREFIXES dict maps base URIs to abbreviations commonly used for
Turtle and other serialization formats.
"""

CANON = "https://github.com/temporal-communities/canon-curator/ontology/"
DCTERMS = "http://purl.org/dc/terms/"
GEO_WGS = "http://www.w3.org/2003/01/geo/wgs84_pos#"
OWL = "http://www.w3.org/2002/07/owl#"
PAV = "http://purl.org/pav/"
PROV = "http://www.w3.org/ns/prov#"
RDF = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
RDFS = "http://www.w3.org/2000/01/rdf-schema#"
XSD = "http://www.w3.org/2001/XMLSchema#"

PREFIXES = {
	"canon": CANON,
	"dct": DCTERMS,
	"geo": GEO_WGS,
	"owl": OWL,
	"pav": PAV,
	"prov": PROV,
	"rdf": RDF,
	"rdfs": RDFS,
	"xsd": XSD,
}
