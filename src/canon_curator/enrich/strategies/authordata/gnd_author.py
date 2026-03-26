from datetime import datetime, UTC
from uuid import UUID
import logging

from canon_curator.enrich.strategies.providers import get_gnd_client
from canon_curator.enrich.clients.gnd_client import GNDProperties
from canon_curator.models import AuthorRecord, BaseWorkRecord

logger = logging.getLogger(__name__)


_GND_GENDER_GUIDE = "https://wiki.dnb.de/download/attachments/50759357/375.pdf"


def _gnd_author(resource_id: str, work_uuid: UUID | None, property_name: str) -> list[AuthorRecord]:
	client = get_gnd_client()
	retrieval_time = datetime.now(UTC)
	authordata = client.fetch_property(resource_id, property_name)
	entries = authordata.get("entries")
	if not entries:
		logger.warning(f"Could not retrieve author data for {resource_id}")
		return []
	logger.debug(f"Retrieved author data {authordata} for {resource_id}")
	return [
		AuthorRecord(
			work_uuid=work_uuid,
			gender_uri=entry.get("uri"),
			gender_marker=entry.get("label"),
			sources=[entry.get("request_url")],
			source_db="https://www.dnb.de/",
			interpretation_context=_GND_GENDER_GUIDE,
			request_uri=f"{client.lobid_base}{resource_id}",
			evidence_level=None,
			retrieved_at=retrieval_time,
		)
		for entry in entries
	]


def gnd_gender(record: BaseWorkRecord) -> list[AuthorRecord]:
	if not record.author_gnd_id:
		logger.warning(
			f"Skipping author data enrichment: no author_gnd_id for {record.uuid} ({record.title})"
		)
		return [AuthorRecord.empty()]
	gender_recs = _gnd_author(
		record.author_gnd_id, work_uuid=record.uuid, property_name=GNDProperties.GENDER
	)
	if not gender_recs:
		logger.warning(f"Could not retrieve author data for {record.author_gnd_id}")
		return [AuthorRecord.empty()]
	logger.info(f"Retrieved {len(gender_recs)} author records.")
	return gender_recs
