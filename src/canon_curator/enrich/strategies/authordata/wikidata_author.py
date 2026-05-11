from datetime import datetime, UTC
from uuid import UUID
import logging

from canon_curator.enrich.clients import WikidataClient
from canon_curator.models import AuthorRecord, BaseWorkRecord, EvidenceLevel

logger = logging.getLogger(__name__)


def _wikidata_author(
	entity_id: str,
	property_id: str,
	work_uuid: UUID | None,
	client: WikidataClient,
) -> list[AuthorRecord]:
	"""Map Wikidata claims to AuthorRecords."""
	if not entity_id:
		logger.warning("Skipping Wikidata author enrichment for %s: empty entity_id", property_id)
		return []

	property_dict = client.fetch_property(entity_id, property_id)
	claims = property_dict.get("claims", [])
	if not claims:
		logger.info("No claims for %s on %s; returning empty AuthorRecord.", property_id, entity_id)
		return []

	retrieval_time = datetime.now(UTC)
	author_records: list[AuthorRecord] = []
	for claim in claims:
		logger.debug("Parsing claim %r", claim)

		gender_qid = claim.get("entity_id")
		gender_label = claim.get("label")

		if not gender_qid and not gender_label:
			continue

		gender_uri = f"http://www.wikidata.org/entity/{gender_qid}" if gender_qid else None
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
		author_records.append(
			AuthorRecord(
				work_uuid=work_uuid,
				gender_uri=gender_uri,
				gender_marker=gender_label,
				sources=[ref["source"] for ref in references if ref["source"]],
				num_sources=len(references),
				evidence_level=evidence_level,
				source_db="http://www.wikidata.org/entity/Q2013",
				request_url=f"{client.wikidata_base}{entity_id}",
				interpretation_context=f"https://www.wikidata.org/wiki/Property:{property_id}",
				retrieved_at=retrieval_time,
			)
		)

	if not author_records:
		return []
	return author_records


def wikidata_p21(record: BaseWorkRecord, client: WikidataClient) -> list[AuthorRecord]:
	"""Strategy for Wikidata P21 (sex or gender) on the author entity."""
	if not record.author_qid:
		logger.warning(
			"Skipping wikidata_p21: no author_qid for %s (%s)",
			record.uuid,
			record.title,
		)
		return [AuthorRecord.empty()]

	author_recs = _wikidata_author(
		record.author_qid, work_uuid=record.uuid, property_id="P21", client=client
	)
	if not author_recs:
		return [AuthorRecord.empty()]

	return author_recs
