from __future__ import annotations

import pyoxigraph as ox

from canon_curator.load.namespaces import RDF
from canon_curator.load.namespaces import CANON


def convert_to_reified_store(store: ox.Store) -> ox.Store:
	"""Helper function to convert a pyoxigraph store with RDF 1.2 reifying triples into
	classic reification with rdf:Statement.

	Each reifier (_:b) with its reifying triple and a triple describing the reifier:

	    _:b rdf:reifies <<( s p o )>> ;
	        canon:hasEnrichment <enr_rec> .

	becomes a single rdf:Statement blank node:

	    _:stmt a rdf:Statement ;
	           rdf:subject   s ;
	           rdf:predicate p ;
	           rdf:object    o ;
	           canon:hasEnrichment <enr_rec> .

	All other quads are copied unchanged.
	"""
	# Dicts mapping blank node ids to triple terms (triple_terms) or enrichmen record iris (enrichment_iris)
	triple_terms: dict[str, ox.Triple] = {}
	enrichment_iris: dict[str, ox.NamedNode | ox.Literal] = {}
	reified_store = ox.Store()

	for quad in store:
		if quad.predicate == ox.NamedNode(RDF + "reifies") and isinstance(quad.object, ox.Triple):
			triple_terms[quad.subject.value] = quad.object
		elif quad.predicate == ox.NamedNode(CANON + "hasEnrichment") and isinstance(
			quad.subject, ox.BlankNode
		):
			enrichment_iris[quad.subject.value] = quad.object
		else:
			reified_store.add(ox.Quad(quad.subject, quad.predicate, quad.object))

	for bnode_id, triple_term in triple_terms.items():
		bnode = ox.BlankNode()
		reified_store.add(
			ox.Quad(bnode, ox.NamedNode(RDF + "type"), ox.NamedNode(RDF + "Statement"))
		)
		reified_store.add(ox.Quad(bnode, ox.NamedNode(RDF + "subject"), triple_term.subject))
		reified_store.add(ox.Quad(bnode, ox.NamedNode(RDF + "predicate"), triple_term.predicate))
		reified_store.add(ox.Quad(bnode, ox.NamedNode(RDF + "object"), triple_term.object))
		if bnode_id in enrichment_iris:
			reified_store.add(
				ox.Quad(bnode, ox.NamedNode(CANON + "hasEnrichment"), enrichment_iris[bnode_id])
			)

	return reified_store
