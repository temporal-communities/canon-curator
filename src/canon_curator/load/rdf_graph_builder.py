from __future__ import annotations

from collections.abc import Iterable

import pyoxigraph as ox

from canon_curator.load.namespaces import (
	CANON,
	DCTERMS,
	GEO_WGS,
	OWL,
	PAV,
	PROV,
	RDF,
	RDFS,
	XSD,
)

from canon_curator.models.enrichment import (
	AuthorRecord,
	GeoRecord,
	ReaderstatsRecord,
	PopularityRecord,
	EvidenceLevel,
	PopularityMetric,
)
from canon_curator.models.records import EnrichedWorkRecord


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
	"""Build a pyoxigraph Store from EnrichedWorkRecord instances.

	Propositions such as "author Y has birth place Z" are linked with their provenance (=enrichment record)
	using the RDF 1.2 triple annotation / triple term pattern:

		_:b rdf:reifies <<( subj pred obj )>> ;
			canon:hasEnrichment <enr_iri> .

	Propositions denoted by the triple term (subj pred obj) are always asserted in the graph, but the source
	(or lack of sources) is used to decide which subproperty of canon:geoloccation and canon:gender is used
	in the triple term.

	See: https://pyoxigraph.readthedocs.io/en/stable/migration.html#from-0-4-to-0-5 and
	https://www.w3.org/TR/rdf12-concepts/#section-triple-terms-reification for more information.
	"""

	def __init__(
		self,
		canon_list_iri: str,
		canon_list_name: str | None = None,
		canon_list_metadata_iri: str | None = None,
		software_agent_iri: str | None = "https://github.com/temporal-communities/canon-curator/",
	) -> None:
		self.canon_list_iri = ox.NamedNode(canon_list_iri)
		self.canon_list_name = canon_list_name
		self.canon_list_metadata_iri = (
			ox.NamedNode(canon_list_metadata_iri) if canon_list_metadata_iri else None
		)
		self.software_agent_iri = ox.NamedNode(software_agent_iri) if software_agent_iri else None

	def build(self, records: Iterable[EnrichedWorkRecord]) -> ox.Store:
		store = ox.Store()

		store.add(
			ox.Quad(
				self.canon_list_iri,
				ox.NamedNode(RDF + "type"),
				ox.NamedNode(CANON + "CanonList"),
			)
		)
		if self.canon_list_name:
			store.add(
				ox.Quad(
					self.canon_list_iri,
					ox.NamedNode(RDFS + "label"),
					ox.Literal(self.canon_list_name),
				)
			)
		if self.canon_list_metadata_iri:
			store.add(
				ox.Quad(
					self.canon_list_iri,
					ox.NamedNode(CANON + "hasMetadata"),
					self.canon_list_metadata_iri,
				)
			)

		seen_source_dbs: set[str] = set()
		activity_iris: list[ox.NamedNode] = []

		for rec in records:
			author_iri = self._add_author(store, rec)
			work_iri = self._add_work(store, rec, author_iri)

			for geo_rec in rec.geodata or []:
				if geo_rec.geo_uri:
					_, act = self._add_geo_enrichment(store, work_iri, author_iri, geo_rec)
					activity_iris.append(act)
				if geo_rec.source_db:
					seen_source_dbs.add(geo_rec.source_db)

			for author_rec in rec.authordata or []:
				if author_rec.gender_uri:
					_, act = self._add_author_enrichment(store, author_iri, author_rec)
					activity_iris.append(act)
				if author_rec.source_db:
					seen_source_dbs.add(author_rec.source_db)

			for pop_rec in rec.wd_metrics:
				if not pop_rec.is_empty():
					_, act = self._add_popularity_enrichment(store, work_iri, pop_rec)
					activity_iris.append(act)
				if pop_rec.source_db:
					seen_source_dbs.add(pop_rec.source_db)

			for rs_rec in rec.readerstats:
				if not rs_rec.is_empty():
					_, act = self._add_readerstats_enrichment(store, work_iri, rs_rec)
					activity_iris.append(act)
				if rs_rec.source_db:
					seen_source_dbs.add(rs_rec.source_db)

		for source_db_uri in seen_source_dbs:
			store.add(
				ox.Quad(
					ox.NamedNode(source_db_uri),
					ox.NamedNode(RDF + "type"),
					ox.NamedNode(PROV + "Entity"),
				)
			)

		run_iri = ox.NamedNode("urn:uuid:enrichment-run")
		store.add(
			ox.Quad(
				run_iri,
				ox.NamedNode(RDF + "type"),
				ox.NamedNode(CANON + "EnrichmentActivity"),
			)
		)
		for act in activity_iris:
			store.add(ox.Quad(run_iri, ox.NamedNode(DCTERMS + "hasPart"), act))

		if self.software_agent_iri:
			store.add(
				ox.Quad(
					self.software_agent_iri,
					ox.NamedNode(RDF + "type"),
					ox.NamedNode(PROV + "SoftwareAgent"),
				)
			)

		return store

	def _annotate(
		self,
		store: ox.Store,
		subj: ox.NamedNode,
		pred: ox.NamedNode,
		obj: ox.NamedNode | ox.Literal,
		enr_iri: ox.NamedNode,
	) -> None:
		"""Assert a triple in the RDF graph and annotate it using the RDF 1.2 pattern:

		_:b rdf:reifies <<( subj pred obj )>> ;
			canon:hasEnrichment enr_iri .

		See: https://www.w3.org/TR/rdf12-concepts/#section-triple-terms-reification
		"""
		store.add(ox.Quad(subj, pred, obj))
		bnode = ox.BlankNode()
		store.add(ox.Quad(bnode, ox.NamedNode(RDF + "reifies"), ox.Triple(subj, pred, obj)))
		store.add(ox.Quad(bnode, ox.NamedNode(CANON + "hasEnrichment"), enr_iri))

	def _add_author(
		self,
		store: ox.Store,
		rec: EnrichedWorkRecord,
	) -> ox.NamedNode:
		base = rec.base_data
		if base.author_qid:
			iri = ox.NamedNode(f"http://www.wikidata.org/entity/{base.author_qid}")
			if base.author_gnd_id:
				store.add(
					ox.Quad(
						iri,
						ox.NamedNode(OWL + "sameAs"),
						ox.NamedNode(f"https://d-nb.info/gnd/{base.author_gnd_id}"),
					)
				)
		elif base.author_gnd_id:
			iri = ox.NamedNode(f"https://d-nb.info/gnd/{base.author_gnd_id}")
		else:
			iri = ox.NamedNode(f"urn:uuid:{base.uuid}#author")

		store.add(ox.Quad(iri, ox.NamedNode(RDF + "type"), ox.NamedNode(CANON + "Author")))
		if base.author:
			store.add(ox.Quad(iri, ox.NamedNode(RDFS + "label"), ox.Literal(base.author)))

		return iri

	def _add_work(
		self,
		store: ox.Store,
		rec: EnrichedWorkRecord,
		author_iri: ox.NamedNode,
	) -> ox.NamedNode:
		base = rec.base_data
		if base.work_qid:
			iri = ox.NamedNode(f"http://www.wikidata.org/entity/{base.work_qid}")
			if base.work_gnd_id:
				store.add(
					ox.Quad(
						iri,
						ox.NamedNode(OWL + "sameAs"),
						ox.NamedNode(f"https://d-nb.info/gnd/{base.work_gnd_id}"),
					)
				)
		elif base.work_gnd_id:
			iri = ox.NamedNode(f"https://d-nb.info/gnd/{base.work_gnd_id}")
		else:
			iri = ox.NamedNode(f"urn:uuid:{base.uuid}")

		store.add(ox.Quad(iri, ox.NamedNode(RDF + "type"), ox.NamedNode(CANON + "Work")))
		store.add(ox.Quad(iri, ox.NamedNode(DCTERMS + "isPartOf"), self.canon_list_iri))
		store.add(ox.Quad(iri, ox.NamedNode(DCTERMS + "creator"), author_iri))
		if base.title:
			store.add(ox.Quad(iri, ox.NamedNode(RDFS + "label"), ox.Literal(base.title)))
			store.add(ox.Quad(iri, ox.NamedNode(DCTERMS + "title"), ox.Literal(base.title)))
		if base.publication_date:
			store.add(
				ox.Quad(iri, ox.NamedNode(DCTERMS + "issued"), ox.Literal(base.publication_date))
			)
		if base.work_goodreads_id:
			store.add(
				ox.Quad(
					iri,
					ox.NamedNode(OWL + "sameAs"),
					ox.NamedNode(f"https://www.goodreads.com/book/show/{base.work_goodreads_id}"),
				)
			)
		return iri

	def _add_location(self, store: ox.Store, geo_rec: GeoRecord) -> ox.NamedNode:
		if geo_rec.geo_uri is None:
			raise ValueError("geo_uri must be set")
		iri = ox.NamedNode(geo_rec.geo_uri)
		store.add(ox.Quad(iri, ox.NamedNode(RDF + "type"), ox.NamedNode(CANON + "Location")))
		if geo_rec.geo_label:
			store.add(ox.Quad(iri, ox.NamedNode(RDFS + "label"), ox.Literal(geo_rec.geo_label)))
		if geo_rec.lat is not None:
			store.add(
				ox.Quad(
					iri,
					ox.NamedNode(GEO_WGS + "lat"),
					ox.Literal(str(float(geo_rec.lat)), datatype=ox.NamedNode(XSD + "decimal")),
				)
			)
		if geo_rec.lon is not None:
			store.add(
				ox.Quad(
					iri,
					ox.NamedNode(GEO_WGS + "long"),
					ox.Literal(str(float(geo_rec.lon)), datatype=ox.NamedNode(XSD + "decimal")),
				)
			)
		return iri

	def _add_enrichment_provenance(
		self,
		store: ox.Store,
		enr_iri: ox.NamedNode,
		enr_rec: GeoRecord | AuthorRecord | PopularityRecord | ReaderstatsRecord,
	) -> ox.NamedNode:
		activity_iri = ox.NamedNode(f"{enr_iri.value}#activity")

		store.add(
			ox.Quad(enr_iri, ox.NamedNode(RDF + "type"), ox.NamedNode(CANON + "EnrichmentRecord"))
		)
		store.add(ox.Quad(enr_iri, ox.NamedNode(PROV + "wasGeneratedBy"), activity_iri))

		if enr_rec.retrieved_at is not None:
			store.add(
				ox.Quad(
					enr_iri,
					ox.NamedNode(PROV + "generatedAtTime"),
					ox.Literal(
						str(enr_rec.retrieved_at.isoformat()),
						datatype=ox.NamedNode(XSD + "dateTime"),
					),
				)
			)
		if enr_rec.source_db is not None:
			store.add(
				ox.Quad(
					enr_iri,
					ox.NamedNode(PROV + "wasDerivedFrom"),
					ox.NamedNode(enr_rec.source_db),
				)
			)
		if enr_rec.request_uri is not None:
			store.add(
				ox.Quad(
					enr_iri,
					ox.NamedNode(PAV + "importedFrom"),
					ox.NamedNode(enr_rec.request_uri),
				)
			)

		if isinstance(enr_rec, (GeoRecord, AuthorRecord)):
			if enr_rec.sources is not None:
				for src in enr_rec.sources:
					store.add(
						ox.Quad(
							enr_iri,
							ox.NamedNode(PROV + "hadPrimarySource"),
							ox.NamedNode(src),
						)
					)
			if enr_rec.interpretation_context is not None:
				store.add(
					ox.Quad(
						enr_iri,
						ox.NamedNode(PAV + "sourceAccessedAt"),
						ox.NamedNode(enr_rec.interpretation_context),
					)
				)

		store.add(
			ox.Quad(
				activity_iri,
				ox.NamedNode(RDF + "type"),
				ox.NamedNode(CANON + "MetadataEnrichment"),
			)
		)
		store.add(ox.Quad(activity_iri, ox.NamedNode(PROV + "generated"), enr_iri))
		if enr_rec.retrieved_at is not None:
			store.add(
				ox.Quad(
					activity_iri,
					ox.NamedNode(PROV + "startedAtTime"),
					ox.Literal(
						str(enr_rec.retrieved_at.isoformat()),
						datatype=ox.NamedNode(XSD + "dateTime"),
					),
				)
			)
		if self.software_agent_iri:
			store.add(
				ox.Quad(
					activity_iri,
					ox.NamedNode(PROV + "wasAssociatedWith"),
					self.software_agent_iri,
				)
			)

		return activity_iri

	def _add_geo_enrichment(
		self,
		store: ox.Store,
		work_iri: ox.NamedNode,
		author_iri: ox.NamedNode,
		geo_rec: GeoRecord,
	) -> tuple[ox.NamedNode, ox.NamedNode]:
		enr_iri = ox.NamedNode(f"urn:uuid:{geo_rec.uuid}")
		location_iri = self._add_location(store, geo_rec)
		entry = _GEO.get(geo_rec.interpretation_context)
		canon_property, subject_type = (
			entry[geo_rec.evidence_level] if entry else ("assumedGeolocation", "work")
		)
		subject_iri = author_iri if subject_type == "author" else work_iri
		self._annotate(
			store, subject_iri, ox.NamedNode(CANON + canon_property), location_iri, enr_iri
		)
		return enr_iri, self._add_enrichment_provenance(store, enr_iri, geo_rec)

	def _add_author_enrichment(
		self,
		store: ox.Store,
		author_iri: ox.NamedNode,
		author_rec: AuthorRecord,
	) -> tuple[ox.NamedNode, ox.NamedNode]:
		if author_rec.gender_uri is None:
			raise ValueError("gender_uri must be set")
		enr_iri = ox.NamedNode(f"urn:uuid:{author_rec.uuid}")
		entry = _AUTHOR.get(author_rec.interpretation_context)
		canon_property, _ = (
			entry[author_rec.evidence_level] if entry else ("assumedGender", "author")
		)
		self._annotate(
			store,
			author_iri,
			ox.NamedNode(CANON + canon_property),
			ox.NamedNode(author_rec.gender_uri),
			enr_iri,
		)
		return enr_iri, self._add_enrichment_provenance(store, enr_iri, author_rec)

	def _add_popularity_enrichment(
		self,
		store: ox.Store,
		work_iri: ox.NamedNode,
		pop_rec: PopularityRecord,
	) -> tuple[ox.NamedNode, ox.NamedNode]:
		enr_iri = ox.NamedNode(f"urn:uuid:{pop_rec.uuid}")
		if pop_rec.value is not None:
			self._annotate(
				store,
				work_iri,
				ox.NamedNode(CANON + _POPULARITY[pop_rec.metric]),
				ox.Literal(str(pop_rec.value), datatype=ox.NamedNode(XSD + "integer")),
				enr_iri,
			)
		return enr_iri, self._add_enrichment_provenance(store, enr_iri, pop_rec)

	def _add_readerstats_enrichment(
		self,
		store: ox.Store,
		work_iri: ox.NamedNode,
		rs_rec: ReaderstatsRecord,
	) -> tuple[ox.NamedNode, ox.NamedNode]:
		enr_iri = ox.NamedNode(f"urn:uuid:{rs_rec.uuid}")
		if rs_rec.avg_rating is not None:
			self._annotate(
				store,
				work_iri,
				ox.NamedNode(CANON + "ratingValue"),
				ox.Literal(str(rs_rec.avg_rating), datatype=ox.NamedNode(XSD + "decimal")),
				enr_iri,
			)
		if rs_rec.ratings_count is not None:
			self._annotate(
				store,
				work_iri,
				ox.NamedNode(CANON + "ratingCount"),
				ox.Literal(str(rs_rec.ratings_count), datatype=ox.NamedNode(XSD + "integer")),
				enr_iri,
			)
		return enr_iri, self._add_enrichment_provenance(store, enr_iri, rs_rec)
