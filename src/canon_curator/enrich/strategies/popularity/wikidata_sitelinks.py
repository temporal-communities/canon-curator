from datetime import datetime, UTC
import logging

from canon_curator.models import PopularityRecord, BaseWorkRecord
from canon_curator.enrich.strategies.providers import get_wikidata_client

logger = logging.getLogger(__name__)


def wikidata_sitelinks(record: BaseWorkRecord) -> list[PopularityRecord]:
	if not record.work_qid:
		logger.warning(f"No work_qid for {record.uuid} ({record.title}), skipping sitelinks.")
		return [PopularityRecord.empty()]
	retrieval_time = datetime.now(UTC)
	client = get_wikidata_client()
	num_sitelinks = client.fetch_sitelinks(record.work_qid)
	if not num_sitelinks:
		return [PopularityRecord.empty()]

	return [
		PopularityRecord(
			work_uuid=record.uuid,
			sitelinks_count=num_sitelinks,
			retrieved_at=retrieval_time,
		)
	]
