from canon_curator.enrich.clients.wikidata_client import WikidataClient
from canon_curator.models.enrichment import AuthorRecord
from canon_curator.models.records import BaseWorkRecord

_client = WikidataClient()


def _wikidata_author(entity_id: str, property_id: str, client: WikidataClient) -> list[AuthorRecord]:
    return [AuthorRecord.empty()]


def wikidata_p21(record: BaseWorkRecord) -> list[AuthorRecord]:
    return _wikidata_author(record.author_qid, property_id="P21", client=_client)
