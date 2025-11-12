from canon_curator.enrich.strategies.providers import get_wikidata_client
from canon_curator.models import GeoRecord, BaseWorkRecord


def _wikidata_geo(entity_id: str, property_id: str) -> list[GeoRecord]:
	client = get_wikidata_client()
	return [GeoRecord.empty()]


def wikidata_p19(record: BaseWorkRecord) -> list[GeoRecord]:
	return _wikidata_geo(record.author_qid, property_id="P19")


def wikidata_p495(record: BaseWorkRecord) -> list[GeoRecord]:
	return _wikidata_geo(record.work_qid, property_id="P495")
