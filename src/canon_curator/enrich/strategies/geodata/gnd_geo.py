from datetime import datetime, UTC
import logging

from canon_curator.enrich.strategies.providers import get_gnd_client
from canon_curator.enrich.clients.gnd_client import GNDProperties
from canon_curator.models import BaseWorkRecord, GeoRecord

_GND_GEOLABEL_GUIDE = "https://wiki.dnb.de/download/attachments/90411323/laendercodeleitfaden.pdf"
_SEE_ALSO = "http://www.w3.org/2000/01/rdf-schema#seeAlso"
_DNB_ID = "d-nb.info/gnd/"

logger = logging.getLogger(__name__)


def _gnd_geo(resource_id: str, property_name: str) -> list[GeoRecord]:
	client = get_gnd_client()
	retrieval_time = datetime.now(UTC)
	geodata = client.fetch_property(resource_id, property_name)
	logger.debug(f"Retrieved geodata {geodata} for {resource_id}")
	entries = geodata.get("entries")
	if not entries:
		return []

	records: list[GeoRecord] = []
	for entry in entries:
		geo_id = None
		geo_uri = entry.get("uri")
		geo_label = entry.get("label")

		if property_name == GNDProperties.GEOCODE and geo_uri:
			concept = client.fetch_concept(entry["uri"])
			logger.debug(f"Retrieved concept data {concept} for {resource_id}")
			geo_url = next(
				(
					s.get(_SEE_ALSO)
					for s in concept["statements"]
					if _DNB_ID in s.get(_SEE_ALSO, "")
				),
				None,
			)
			geo_id = geo_url.rstrip("/").split("/")[-1] if geo_url else None
			logger.debug(f"Retrieved GND id {geo_id} for geocode associated with {resource_id}")

		records.append(
			GeoRecord(
				geo_id=geo_id,
				geo_uri=geo_uri,
				geo_label=geo_label,
				lat=float(entry.get("latitude")) if entry.get("latitude") else None,
				lon=float(entry.get("longitude")) if entry.get("longitude") else None,
				sources=[],
				num_sources=0,
				request_uri=f"{client.lobid_base}{resource_id}",
				interpretation_context=_GND_GEOLABEL_GUIDE,
				evidence_level=None,
				retrieved_at=retrieval_time,
			)
		)

	return records


def gnd_geolabel(record: BaseWorkRecord) -> list[GeoRecord]:
	if not record.work_gnd_id:
		logger.warning(
			f"Skipping geodata enrichment: no work_gnd_id for {record.uuid} ({record.title})"
		)
		return [GeoRecord.empty()]
	geocode_recs = _gnd_geo(record.work_gnd_id, property_name=GNDProperties.GEOCODE)
	if not geocode_recs:
		logger.warning(f"Could not retrieve geodata for {record.work_gnd_id}")
		return [GeoRecord.empty()]
	geo_recs = []
	for geocode_rec in geocode_recs:
		if not geocode_rec.geo_id:
			logger.warning("Skipping coordinate lookup: no geo_id on geocode record")
			continue
		coords_rec = _gnd_geo(geocode_rec.geo_id, property_name=GNDProperties.GEOMETRY)
		if not coords_rec:
			logger.warning("Could not retrieve coordinate info from GND")
			continue
		logger.debug(f"Retrieved {geocode_rec} and {coords_rec}")
		geo_recs.append(
			GeoRecord(
				work_uuid=record.uuid,
				geo_id=geocode_rec.geo_id,
				geo_uri=geocode_rec.geo_uri,
				geo_label=geocode_rec.geo_label,
				lat=coords_rec[0].lat,
				lon=coords_rec[0].lon,
				sources=geocode_rec.sources,
				num_sources=geocode_rec.num_sources,
				source_db="https://www.dnb.de/",
				request_uri=geocode_rec.request_uri,
				interpretation_context=geocode_rec.interpretation_context,
				evidence_level=geocode_rec.evidence_level,
				retrieved_at=geocode_rec.retrieved_at,
			)
		)
	logger.info(f"Retrieved {len(geo_recs)} geo records.")
	return geo_recs
