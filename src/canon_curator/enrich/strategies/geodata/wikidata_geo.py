from datetime import datetime, UTC
from uuid import UUID
import logging

from canon_curator.enrich.clients import WikidataClient
from canon_curator.models import GeoRecord, BaseWorkRecord, EvidenceLevel

logger = logging.getLogger(__name__)


def _wikidata_geo(
	entity_id: str,
	property_id: str,
	work_uuid: UUID | None,
	client: WikidataClient,
) -> list[GeoRecord]:
	"""Map Wikidata claims to GeoRecords."""
	if not entity_id:
		logger.warning("Skipping Wikidata geo enrichment for %s: empty entity_id", property_id)
		return []

	property_dict = client.fetch_property(entity_id, property_id)
	claims = property_dict.get("claims", [])
	if not claims:
		logger.info(
			"No claims for %s on %s; returning empty GeoRecord.",
			property_id,
			entity_id,
		)
		return []

	retrieval_time = datetime.now(UTC)
	geo_records: list[GeoRecord] = []

	for claim in claims:
		logger.debug("Parsing claim %r", claim)

		geo_id = claim.get("entity_id")
		geo_label = claim.get("label")
		geo_uri = f"http://www.wikidata.org/entity/{geo_id}" if geo_id else None

		lat = None
		lon = None
		coord_dict = client.fetch_property(geo_id, "P625")
		for c in coord_dict.get("claims", []):
			lat_val = c.get("latitude")
			lon_val = c.get("longitude")
			lat = float(lat_val) if lat_val is not None else None
			lon = float(lon_val) if lon_val is not None else None

		references = claim.get("sources", [])
		has_references = len(references) > 0
		is_inferred = has_references and all(
			"P887" in ref.get("qualifiers", {}) for ref in references
		)
		evidence_level = (
			None
			if not has_references
			else EvidenceLevel.INFERRED
			if is_inferred
			else EvidenceLevel.REFERENCED
		)
		logger.debug(f"References: {references}")

		if not any([geo_id, geo_uri, geo_label, lat, lon]):
			continue

		geo_records.append(
			GeoRecord(
				work_uuid=work_uuid,
				geo_id=geo_id,
				geo_uri=geo_uri,
				geo_label=geo_label,
				lat=lat,
				lon=lon,
				sources=[ref["source"] for ref in references if ref["source"]],
				num_sources=len(references),
				evidence_level=evidence_level,
				source_db="https://www.wikidata.org/",
				request_uri=f"http://www.wikidata.org/entity/{entity_id}",
				interpretation_context=f"https://www.wikidata.org/wiki/Property:{property_id}",
				retrieved_at=retrieval_time,
			)
		)

	if not geo_records:
		return []
	return geo_records


def wikidata_p19(record: BaseWorkRecord, client: WikidataClient) -> list[GeoRecord]:
	"""Strategy for Wikidata P19 (place of birth) on the author entity."""
	if not record.author_qid:
		logger.warning(
			"Skipping wikidata_p19: no author_qid for %s (%s)",
			record.uuid,
			record.title,
		)
		return [GeoRecord.empty()]

	geo_recs = _wikidata_geo(
		record.author_qid, work_uuid=record.uuid, property_id="P19", client=client
	)
	if not geo_recs:
		return [GeoRecord.empty()]

	return geo_recs


def wikidata_p495(record: BaseWorkRecord, client: WikidataClient) -> list[GeoRecord]:
	"""Strategy for Wikidata P495 (country of origin) on the work entity."""
	if not record.work_qid:
		logger.warning(
			"Skipping wikidata_p495: no work_qid for %s (%s)",
			record.uuid,
			record.title,
		)
		return [GeoRecord.empty()]

	geo_recs = _wikidata_geo(
		record.work_qid, work_uuid=record.uuid, property_id="P495", client=client
	)
	if not geo_recs:
		return [GeoRecord.empty()]

	return geo_recs
