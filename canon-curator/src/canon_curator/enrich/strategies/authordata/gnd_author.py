from canon_curator.enrich.strategies.providers import get_gnd_client
from canon_curator.enrich.clients.gnd_client import GNDProperties
from canon_curator.models.enrichment import AuthorRecord
from canon_curator.models.records import BaseWorkRecord


def _gnd_author(resource_id: str, property_name: str) -> list[AuthorRecord]:
    client = get_gnd_client()
    return [AuthorRecord.empty()]


def gnd_gender(record: BaseWorkRecord) -> list[AuthorRecord]:
    return _gnd_author(record.author_qid, property_name=GNDProperties.GENDER)
