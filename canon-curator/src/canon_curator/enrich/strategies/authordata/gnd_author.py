from canon_curator.enrich.clients.gnd_client import GNDClient
from canon_curator.enrich.clients.gnd_client import GNDProperties
from canon_curator.models.enrichment import AuthorRecord
from canon_curator.models.records import BaseWorkRecord

_client = GNDClient()   # client is never closed! change this later


def _gnd_author(resource_id: str, property_name: str, client: GNDClient) -> list[AuthorRecord]:
    return [AuthorRecord.empty()]


def gnd_gender(record: BaseWorkRecord) -> list[AuthorRecord]:
    return _gnd_author(record.author_qid, property_name=GNDProperties.GENDER, client=_client)
