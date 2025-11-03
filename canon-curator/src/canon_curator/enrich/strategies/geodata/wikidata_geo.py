from canon_curator.enrich.clients.wikidata_client import WikidataClient
from canon_curator.models.enrichment import GeoRecord
from canon_curator.models.records import BaseWorkRecord

_client = WikidataClient()


def _wikidata_geo(entity_id: str, property_id: str, client: WikidataClient) -> list[GeoRecord]:
    return [GeoRecord.empty()]


def wikidata_p19(record: BaseWorkRecord) -> list[GeoRecord]:
    return _wikidata_geo(record.author_qid, property_id="P19", client=_client)


def wikidata_p495(record: BaseWorkRecord) -> list[GeoRecord]:
    return _wikidata_geo(record.work_qid, property_id="P495", client=_client)


