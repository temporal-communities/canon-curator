import logging
from datetime import datetime, UTC
from urllib.parse import urlparse

from canon_curator.models import PopularityRecord, BaseWorkRecord, PopularityMetric
from canon_curator.enrich.clients import QRankClient

logger = logging.getLogger(__name__)


def wikidata_qrank(record: BaseWorkRecord, client: QRankClient) -> list[PopularityRecord]:
	if not record.work_qid:
		logger.warning(f"No work_qid for {record.uuid} ({record.title}), skipping qrank.")
		return [PopularityRecord.empty()]
	retrieval_time = datetime.now(UTC)
	qrank = client.get_qrank(record.work_qid)
	if not qrank:
		logger.warning(f"Could not retrieve qrank for {record.work_qid}")
		return [PopularityRecord.empty()]
	logger.debug(f"Retrieved qrank {qrank} for {record.work_qid}")
	download_url = client.download_url
	return [
		PopularityRecord(
			work_uuid=record.uuid,
			value=qrank,
			metric=PopularityMetric.QRANK,
			source_db=f"https://{urlparse(download_url).netloc}/",
			request_uri=download_url,
			retrieved_at=retrieval_time,
		)
	]
