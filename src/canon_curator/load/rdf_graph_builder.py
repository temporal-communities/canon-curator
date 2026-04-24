from __future__ import annotations

from collections.abc import Iterable

from rdflib import BNode, Graph, Literal, URIRef
from rdflib.namespace import Namespace, DCTERMS, PROV, OWL, RDF, RDFS, XSD

from canon_curator.models.enrichment import (
	EnrichmentRecord,
	AuthorRecord,
	GeoRecord,
	ReaderstatsRecord,
	PopularityRecord,
	EvidenceLevel,
	PopularityMetric,
)
from canon_curator.models.records import EnrichedWorkRecord

CANON = Namespace("https://github.com/temporal-communities/canon-curator/ontology/")
GEO_WGS = Namespace("http://www.w3.org/2003/01/geo/wgs84_pos#")
PAV = Namespace("http://purl.org/pav/")


# Dictionaries for vocabulary alignment
# Keys are interpretation_context values, which for Wikidata strategies are Wikidata property
# IRIs (e.g. https://www.wikidata.org/wiki/Property:P19). These double as sourceAccessedAt
# values since the property page is consulted to understand what is being queried.
# GND strategies set interpretation_context to a documentation PDF URL, which does not match
# any key here. GND records therefore fall through to the defaults (assumedGeolocation
# and assumedGender). This is correct as long as GND evidence_level is always None.

_GEO: dict[str | None, dict[EvidenceLevel | None, tuple[str, str]]] = {
	"https://www.wikidata.org/wiki/Property:P19": {
		EvidenceLevel.AUTHORITATIVE: ("authorBirthPlace", "author"),
		EvidenceLevel.REFERENCED: ("authorBirthPlace", "author"),
		EvidenceLevel.INFERRED: ("assumedGeolocation", "author"),
		None: ("assumedGeolocation", "author"),
	},
	"https://www.wikidata.org/wiki/Property:P495": {
		EvidenceLevel.AUTHORITATIVE: ("workOrigin", "work"),
		EvidenceLevel.REFERENCED: ("workOrigin", "work"),
		EvidenceLevel.INFERRED: ("assumedGeolocation", "work"),
		None: ("assumedGeolocation", "work"),
	},
}

_AUTHOR: dict[str | None, dict[EvidenceLevel | None, tuple[str, str]]] = {
	"https://www.wikidata.org/wiki/Property:P21": {
		EvidenceLevel.AUTHORITATIVE: ("selfIdentifiedGender", "author"),
		EvidenceLevel.REFERENCED: ("recordedGender", "author"),
		EvidenceLevel.INFERRED: ("assumedGender", "author"),
		None: ("assumedGender", "author"),
	},
}

_POPULARITY: dict[PopularityMetric | None, str] = {
	PopularityMetric.SITELINKS: "sitelinkCount",
	PopularityMetric.QRANK: "qRank",
	None: "popularityMetric",
}


class RDFGraphBuilder:
	"""Build an rdflib Graph from EnrichedWorkRecord instances.

	The dictionaries _GEO, _AUTHOR map each enrichment record's
	interpretation_context and evidence_level to the correct canon: property and subject.
	RDF-star annotations link each triple to its enrichment record node.
	Please note: Statement-level provenance for geodata and author data is added with standard reification,
	since RDFlib does not support RDF-star yet. Exporters may convert reified statements to JSON-LD-star or Turtle-star.

	"""

	def __init__(
		self,
		canon_list_iri: str,
		canon_list_name: str | None = None,
		canon_list_metadata_iri: str | None = None,
		software_agent_iri: str | None = "https://github.com/temporal-communities/canon-curator/",
	) -> None:
		self.canon_list_iri = URIRef(canon_list_iri)
		self.canon_list_name = canon_list_name
		self.canon_list_metadata_iri = (
			URIRef(canon_list_metadata_iri) if canon_list_metadata_iri else None
		)
		self.software_agent_iri = URIRef(software_agent_iri) if software_agent_iri else None

	def build(self, records: Iterable[EnrichedWorkRecord]) -> Graph:
		g = Graph()
		g.bind("canon", CANON)
		g.bind("pav", PAV)
		g.bind("prov", PROV)
		g.bind("dct", DCTERMS)
		g.bind("geo", GEO_WGS)

		self._add_canon_list(g)
		if (
			self.canon_list_metadata_iri
		):  # TODO: add warning for missing metadata; merge with graph, add connector
			self._add_list_metadata(g)

		seen_authors: dict[str, URIRef] = {}
		activity_iris: list[URIRef] = []
		for rec in records:
			author_iri = self._add_author(g, rec, seen_authors)
			work_iri = self._add_work(g, rec, author_iri)
			for geo_rec in rec.geodata or []:
				if geo_rec.geo_uri:
					_, activity_iri = self._add_geo_enrichment(g, work_iri, author_iri, geo_rec)
					activity_iris.append(activity_iri)
			for author_rec in rec.authordata or []:
				if author_rec.gender_uri:
					_, activity_iri = self._add_author_enrichment(g, author_iri, author_rec)
					activity_iris.append(activity_iri)
			for pop_rec in rec.wd_metrics:
				if not pop_rec.is_empty():
					_, activity_iri = self._add_popularity_enrichment(g, work_iri, pop_rec)
					activity_iris.append(activity_iri)
			for rs_rec in rec.readerstats:
				if not rs_rec.is_empty():
					_, activity_iri = self._add_readerstats_enrichment(g, work_iri, rs_rec)
					activity_iris.append(activity_iri)

		self._add_workflow_provenance(g, activity_iris)

		return g

	def _add_canon_list(self, g: Graph) -> None:
		g.add((self.canon_list_iri, RDF.type, CANON.CanonList))
		if self.canon_list_name:
			g.add((self.canon_list_iri, RDFS.label, Literal(self.canon_list_name)))

	def _add_list_metadata(self, g: Graph) -> None:
		if self.canon_list_metadata_iri is None:
			raise ValueError("canon_list_metadata_iri must be set")
		g.add((self.canon_list_iri, CANON.hasMetadata, self.canon_list_metadata_iri))

	def _add_workflow_provenance(self, g: Graph, activity_iris: Iterable[URIRef]) -> URIRef:
		run_iri = URIRef("urn:uuid:enrichment-run")
		g.add((run_iri, RDF.type, CANON.EnrichmentActivity))
		for iri in activity_iris:
			g.add((run_iri, DCTERMS.hasPart, iri))
		return run_iri

	def _add_author(self, g: Graph, rec: EnrichedWorkRecord, seen: dict) -> URIRef:
		base = rec.base_data
		if base.author_qid:
			iri = URIRef(f"https://www.wikidata.org/entity/{base.author_qid}")
		elif base.author_gnd_id:
			iri = URIRef(f"https://d-nb.info/gnd/{base.author_gnd_id}")
		else:
			iri = URIRef(f"urn:uuid:{base.uuid}#author")

		if str(iri) in seen:  #  TODO: test with different enrichment chains
			return seen[str(iri)]
		seen[str(iri)] = iri

		g.add((iri, RDF.type, CANON.Author))
		if base.author:
			g.add((iri, RDFS.label, Literal(base.author)))
		if base.author_qid:
			g.add((iri, OWL.sameAs, URIRef(f"https://www.wikidata.org/entity/{base.author_qid}")))
		if base.author_gnd_id:
			g.add((iri, OWL.sameAs, URIRef(f"https://d-nb.info/gnd/{base.author_gnd_id}")))
		return iri

	def _add_work(self, g: Graph, rec: EnrichedWorkRecord, author_iri: URIRef) -> URIRef:
		base = rec.base_data
		if base.work_qid:
			iri = URIRef(f"https://www.wikidata.org/entity/{base.work_qid}")
		elif base.work_gnd_id:
			iri = URIRef(f"https://d-nb.info/gnd/{base.work_gnd_id}")
		else:
			iri = URIRef(f"urn:uuid:{base.uuid}")

		g.add((iri, RDF.type, CANON.Work))
		g.add((iri, DCTERMS.isPartOf, self.canon_list_iri))
		g.add((iri, DCTERMS.creator, author_iri))
		if base.title:
			g.add((iri, RDFS.label, Literal(base.title)))
			g.add((iri, DCTERMS.title, Literal(base.title)))
		if base.publication_date:
			g.add((iri, DCTERMS.issued, Literal(base.publication_date)))
		if base.work_qid:
			g.add((iri, OWL.sameAs, URIRef(f"https://www.wikidata.org/entity/{base.work_qid}")))
		if base.work_gnd_id:
			g.add((iri, OWL.sameAs, URIRef(f"https://d-nb.info/gnd/{base.work_gnd_id}")))
		if base.work_goodreads_id:
			g.add(
				(
					iri,
					OWL.sameAs,
					URIRef(f"https://www.goodreads.com/book/show/{base.work_goodreads_id}"),
				)
			)
		return iri

	def _add_location(self, g: Graph, geo_rec: GeoRecord) -> URIRef:
		if geo_rec.geo_uri is None:
			raise ValueError("geo_uri must be set")
		iri = URIRef(geo_rec.geo_uri)
		g.add((iri, RDF.type, CANON.Location))
		if geo_rec.geo_label:
			g.add((iri, RDFS.label, Literal(geo_rec.geo_label)))
		if geo_rec.lat is not None:
			g.add((iri, GEO_WGS.lat, Literal(geo_rec.lat, datatype=XSD.decimal)))
		if geo_rec.lon is not None:
			g.add((iri, GEO_WGS.long, Literal(geo_rec.lon, datatype=XSD.decimal)))
		return iri

	def _add_enrichment_provenance(
		self,
		g: Graph,
		enr_iri: URIRef,
		enr_rec: GeoRecord | AuthorRecord | PopularityRecord | ReaderstatsRecord,
	) -> URIRef:
		activity_iri = URIRef(f"{enr_iri}#activity")

		g.add((enr_iri, RDF.type, CANON.EnrichmentRecord))
		g.add((enr_iri, PROV.wasDerivedFrom, self.canon_list_iri))
		g.add((enr_iri, PROV.wasGeneratedBy, activity_iri))

		if enr_rec.retrieved_at is not None:
			g.add(
				(
					enr_iri,
					PROV.generatedAtTime,
					Literal(enr_rec.retrieved_at, datatype=XSD.dateTime),
				)
			)
		if getattr(enr_rec, "source_db", None) and enr_rec.source_db is not None:
			g.add((enr_iri, PROV.wasDerivedFrom, URIRef(enr_rec.source_db)))
		if isinstance(enr_rec, (GeoRecord, AuthorRecord)):
			if enr_rec.sources is not None:
				for src in enr_rec.sources:
					g.add((enr_iri, PROV.hadPrimarySource, URIRef(src)))
			if enr_rec.interpretation_context is not None:
				g.add((enr_iri, PAV.sourceAccessedAt, URIRef(enr_rec.interpretation_context)))

		g.add((activity_iri, RDF.type, CANON.MetadataEnrichment))
		g.add((activity_iri, PROV.generated, enr_iri))
		if enr_rec.retrieved_at is not None:
			g.add(
				(
					activity_iri,
					PROV.startedAtTime,
					Literal(enr_rec.retrieved_at, datatype=XSD.dateTime),
				)
			)
		if getattr(enr_rec, "request_uri", None) and enr_rec.request_uri is not None:
			g.add((activity_iri, PROV.used, URIRef(enr_rec.request_uri)))
		if self.software_agent_iri:
			g.add((activity_iri, PROV.wasAssociatedWith, self.software_agent_iri))

		return activity_iri

	def _add_reification(
		self, g: Graph, subj: URIRef, pred: URIRef, obj: URIRef | Literal, enr_iri: URIRef
	) -> BNode:
		stmt = BNode()
		g.add((stmt, RDF.type, RDF.Statement))
		g.add((stmt, RDF.subject, subj))
		g.add((stmt, RDF.predicate, pred))
		g.add((stmt, RDF.object, obj))
		g.add((stmt, CANON.hasEnrichment, enr_iri))

		return stmt

	def _add_geo_enrichment(
		self, g: Graph, work_iri: URIRef, author_iri: URIRef, geo_rec: GeoRecord
	) -> tuple[URIRef, URIRef]:
		enr_iri = URIRef(f"urn:uuid:{geo_rec.uuid}")
		location_iri = self._add_location(g, geo_rec)

		entry = _GEO.get(geo_rec.interpretation_context)
		canon_property, subject_type = (
			entry[geo_rec.evidence_level] if entry else ("assumedGeolocation", "work")
		)
		subject_iri = author_iri if subject_type == "author" else work_iri
		predicate_iri = CANON[canon_property]

		g.add((subject_iri, predicate_iri, location_iri))
		self._add_reification(g, subject_iri, predicate_iri, location_iri, enr_iri)

		activity_iri = self._add_enrichment_provenance(g, enr_iri, geo_rec)
		return enr_iri, activity_iri

	def _add_author_enrichment(
		self, g: Graph, author_iri: URIRef, author_rec: AuthorRecord
	) -> tuple[URIRef, URIRef]:
		enr_iri = URIRef(f"urn:uuid:{author_rec.uuid}")
		if author_rec.gender_uri is None:
			raise ValueError("gender_uri must be set")

		gender_iri = URIRef(author_rec.gender_uri)

		entry = _AUTHOR.get(author_rec.interpretation_context)
		canon_property, _ = (
			entry[author_rec.evidence_level] if entry else ("assumedGender", "author")
		)
		predicate_iri = CANON[canon_property]

		g.add((author_iri, predicate_iri, gender_iri))
		self._add_reification(g, author_iri, predicate_iri, gender_iri, enr_iri)

		activity_iri = self._add_enrichment_provenance(g, enr_iri, author_rec)
		return enr_iri, activity_iri

	def _add_popularity_enrichment(
		self, g: Graph, work_iri: URIRef, pop_rec: PopularityRecord
	) -> tuple[URIRef, URIRef]:
		enr_iri = URIRef(f"urn:uuid:{pop_rec.uuid}")

		if pop_rec.value is not None:
			canon_property = _POPULARITY[pop_rec.metric]
			predicate_iri = CANON[canon_property]
			value_literal = Literal(pop_rec.value, datatype=XSD.integer)

			g.add((work_iri, predicate_iri, value_literal))
			self._add_reification(g, work_iri, predicate_iri, value_literal, enr_iri)

		activity_iri = self._add_enrichment_provenance(g, enr_iri, pop_rec)
		return enr_iri, activity_iri

	def _add_readerstats_enrichment(
		self, g: Graph, work_iri: URIRef, rs_rec: ReaderstatsRecord
	) -> tuple[URIRef, URIRef]:
		enr_iri = URIRef(f"urn:uuid:{rs_rec.uuid}")

		if rs_rec.avg_rating is not None:
			value_literal = Literal(rs_rec.avg_rating, datatype=XSD.decimal)
			g.add((work_iri, CANON.ratingValue, value_literal))
			self._add_reification(g, work_iri, CANON.ratingValue, value_literal, enr_iri)

		if rs_rec.ratings_count is not None:
			count_literal = Literal(rs_rec.ratings_count, datatype=XSD.integer)
			g.add((work_iri, CANON.ratingCount, count_literal))
			self._add_reification(g, work_iri, CANON.ratingCount, count_literal, enr_iri)

		activity_iri = self._add_enrichment_provenance(g, enr_iri, rs_rec)
		return enr_iri, activity_iri
