from canon_curator.enrich.clients.gnd_client import GNDClient
from canon_curator.enrich.clients.gnd_client import GNDProperties
from canon_curator.models.enrichment import GeoRecord
from canon_curator.models.records import BaseWorkRecord

_client = GNDClient()   # client is never closed! change this later


def _gnd_geo(resource_id: str, property_name: str, client: GNDClient) -> list[GeoRecord]:
    return [GeoRecord.empty()]


def gnd_geolabel(record: BaseWorkRecord) -> list[GeoRecord]:
    labels = _gnd_geo(record.author_qid, property_name=GNDProperties.GEOCODE, client=_client)
    if not labels:
        return [GeoRecord.empty()]
    geo_recs = []
    for label_rec in labels:
        coords_rec = _gnd_geo(label_rec.ext_id, property_name=GNDProperties.GEOMETRY, client=_client)
        geo_recs.append(
            GeoRecord(
                ext_id=label_rec.ext_id,
                geo_uri=label_rec.geo_uri,
                geo_label=label_rec.geo_label,
                lat=coords_rec[0].lat,
                lon=coords_rec[0].lon,
                source=label_rec.source,
                interpretation_context=label_rec.interpretation_context,
                retrieved_at=label_rec.retrieved_at
            )
        )
    return geo_recs
