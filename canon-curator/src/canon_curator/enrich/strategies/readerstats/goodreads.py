from canon_curator.models.enrichment import ReaderstatRecord
from canon_curator.models.records import BaseWorkRecord
from canon_curator.enrich.clients.goodreads_client import GoodreadsClient

_client = GoodreadsClient()  # client is never closed! change this later


def _goodreads(goodreads_id: str, client: GoodreadsClient) -> list[ReaderstatRecord]:
    return [ReaderstatRecord.empty()]


def goodreads_readerstats(record: BaseWorkRecord) -> list[ReaderstatRecord]:
    return _goodreads(goodreads_id=record.work_goodreads_id, client=_client)
