from collections.abc import Iterable, Mapping
from uuid import UUID

from canon_curator.models import (
	BaseWorkRecord,
	EnrichedWorkRecord,
	GeoRecord,
	AuthorRecord,
	PopularityRecord,
	ReaderstatsRecord,
)


def merge_records(
	base_recs: Iterable[BaseWorkRecord],
	geodata: Mapping[UUID, GeoRecord],
	authordata: Mapping[UUID, AuthorRecord],
	popularity: Mapping[UUID, PopularityRecord],
	readerstats: Mapping[UUID, ReaderstatsRecord],
) -> list[EnrichedWorkRecord]:
	"""Merge BaseWorkRecords with enrichment data, using dataclass defaults for missing fields."""
	enriched_recs: list[EnrichedWorkRecord] = []
	for rec in base_recs:
		uid = rec.uuid

		if uid is None:
			continue

		enriched_recs.append(
			EnrichedWorkRecord(
				base_data=rec,
				geodata=geodata.get(uid, GeoRecord()),
				authordata=authordata.get(uid, AuthorRecord()),
				wd_metrics=popularity.get(uid, PopularityRecord()),
				readerstats=readerstats.get(uid, ReaderstatsRecord()),
			)
		)

	return enriched_recs
