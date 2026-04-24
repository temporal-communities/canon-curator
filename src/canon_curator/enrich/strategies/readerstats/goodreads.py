from datetime import datetime, UTC
from uuid import UUID
import logging

from canon_curator.enrich.strategies.providers import get_goodreads_client
from canon_curator.models import ReaderstatsRecord, BaseWorkRecord

logger = logging.getLogger(__name__)


def _goodreads(goodreads_id: str, work_uuid: UUID | None) -> list[ReaderstatsRecord]:
	client = get_goodreads_client()
	retrieval_time = datetime.now(UTC)
	readerstats = client.fetch_readerstats(goodreads_id)
	if all(value is None for value in readerstats.values()):
		logger.warning(f"No readerstats found for {goodreads_id}")
		return []
	logger.info(f"Returning readerstats for {goodreads_id}")
	avg_rating = readerstats.get("averageRating")
	ratings_count = readerstats.get("ratingsCount")
	featured_url = readerstats.get("featuredUrl")
	return [
		ReaderstatsRecord(
			work_uuid=work_uuid,
			avg_rating=float(avg_rating) if avg_rating else None,
			ratings_count=int(ratings_count) if ratings_count else None,
			source_db=client.goodreads_base,
			request_uri=str(featured_url) if featured_url else None,
			retrieved_at=retrieval_time,
		)
	]


def goodreads_readerstats(record: BaseWorkRecord) -> list[ReaderstatsRecord]:
	if not record.work_goodreads_id:
		logger.warning(
			f"Skipping readerstats enrichment: no work_goodreads_id for {record.uuid} ({record.title})"
		)
		return [ReaderstatsRecord.empty()]
	readerstat_recs = _goodreads(goodreads_id=record.work_goodreads_id, work_uuid=record.uuid)
	if not readerstat_recs:
		return [ReaderstatsRecord.empty()]
	return readerstat_recs
