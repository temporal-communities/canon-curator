from canon_curator.enrich.strategies.providers import get_goodreads_client
from canon_curator.models import ReaderstatsRecord, BaseWorkRecord


def _goodreads(goodreads_id: str) -> list[ReaderstatsRecord]:
	client = get_goodreads_client()
	return [ReaderstatsRecord.empty()]


def goodreads_readerstats(record: BaseWorkRecord) -> list[ReaderstatsRecord]:
	return _goodreads(goodreads_id=record.work_goodreads_id)
