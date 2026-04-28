from collections.abc import Iterable, Mapping, Sequence
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
	geodata: Mapping[UUID, Sequence[GeoRecord]],
	authordata: Mapping[UUID, Sequence[AuthorRecord]],
	popularity: Mapping[UUID, Sequence[PopularityRecord]],
	readerstats: Mapping[UUID, Sequence[ReaderstatsRecord]],
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
				geodata=list(geodata.get(uid, [])),
				authordata=list(authordata.get(uid, [])),
				wd_metrics=list(popularity.get(uid, [])),
				readerstats=list(readerstats.get(uid, [])),
			)
		)

	return enriched_recs
