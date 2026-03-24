from datetime import datetime, UTC
import logging

from canon_curator.models import PopularityRecord, BaseWorkRecord
from canon_curator.enrich.strategies.providers import get_qrank_client

logger = logging.getLogger(__name__)


def wikidata_qrank(record: BaseWorkRecord) -> list[PopularityRecord]:
	if not record.work_qid:
		logger.warning(f"No work_qid for {record.uuid} ({record.title}), skipping sitelinks.")
		return [PopularityRecord.empty()]
	retrieval_time = datetime.now(UTC)
	client = get_qrank_client()
	qrank = client.get_qrank(record.work_qid)
	if not qrank:
		logger.warning(f"Could not retrieve qrank for {record.work_qid}")
		return [PopularityRecord.empty()]
	logger.debug(f"Retrieved qrank {qrank} for {record.work_qid}")
	return [
		PopularityRecord(
			work_uuid=record.uuid,
			q_rank=qrank,
			retrieved_at=retrieval_time,
		)
	]
