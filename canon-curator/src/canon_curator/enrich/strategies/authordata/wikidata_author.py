from canon_curator.enrich.strategies.providers import get_wikidata_client
from canon_curator.models.enrichment import AuthorRecord
from canon_curator.models.records import BaseWorkRecord


def _wikidata_author(entity_id: str, property_id: str) -> list[AuthorRecord]:
	client = get_wikidata_client()
	return [AuthorRecord.empty()]


def wikidata_p21(record: BaseWorkRecord) -> list[AuthorRecord]:
	return _wikidata_author(record.author_qid, property_id="P21")
