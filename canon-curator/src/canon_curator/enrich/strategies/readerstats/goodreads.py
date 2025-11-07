from canon_curator.enrich.strategies.providers import get_goodreads_client
from canon_curator.models.enrichment import ReaderstatRecord
from canon_curator.models.records import BaseWorkRecord


def _goodreads(goodreads_id: str) -> list[ReaderstatRecord]:
	client = get_goodreads_client()
	return [ReaderstatRecord.empty()]


def goodreads_readerstats(record: BaseWorkRecord) -> list[ReaderstatRecord]:
	return _goodreads(goodreads_id=record.work_goodreads_id)
