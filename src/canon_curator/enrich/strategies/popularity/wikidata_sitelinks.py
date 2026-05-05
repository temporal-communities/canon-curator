from datetime import datetime, UTC
import logging

from canon_curator.models import PopularityRecord, BaseWorkRecord, PopularityMetric
from canon_curator.enrich.clients import WikidataClient

logger = logging.getLogger(__name__)


def wikidata_sitelinks(record: BaseWorkRecord, client: WikidataClient) -> list[PopularityRecord]:
	if not record.work_qid:
		logger.warning(f"No work_qid for {record.uuid} ({record.title}), skipping sitelinks.")
		return [PopularityRecord.empty()]
	retrieval_time = datetime.now(UTC)
	num_sitelinks = client.fetch_sitelinks(record.work_qid)
	if not num_sitelinks:
		return [PopularityRecord.empty()]

	return [
		PopularityRecord(
			work_uuid=record.uuid,
			value=num_sitelinks,
			metric=PopularityMetric.SITELINKS,
			source_db="https://www.wikidata.org/",
			request_uri=f"https://www.wikidata.org/entity/{record.work_qid}",
			retrieved_at=retrieval_time,
		)
	]
