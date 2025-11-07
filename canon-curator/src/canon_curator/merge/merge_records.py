from collections.abc import Iterable

from canon_curator.models.records import BaseWorkRecord, EnrichedWorkRecord
from canon_curator.models.enrichment import EnrichmentRecord, GeoRecord, AuthorRecord, PopularityRecord, ReaderstatRecord


def _make_index(records: Iterable[EnrichmentRecord]) -> dict:
    return {rec.rec_uuid: rec for rec in records}


def merge_records(
        base_recs: Iterable[BaseWorkRecord],
        geo_recs: Iterable[GeoRecord],
        author_recs: Iterable[AuthorRecord],
        popularity_recs: Iterable[PopularityRecord],
        readerstat_recs: Iterable[ReaderstatRecord],
) -> Iterable[EnrichedWorkRecord]:
    """Merge BaseWorkRecords with enrichment data, using dataclass defaults for missing fields."""

    geo_index = _make_index(geo_recs)
    author_index = _make_index(author_recs)
    popularity_index = _make_index(popularity_recs)
    readerstat_index = _make_index(readerstat_recs)

    enriched_recs = []
    for rec in base_recs:
        uid = rec.uuid
        enriched_recs.append(
            EnrichedWorkRecord(
                base_data=rec,
                geodata=geo_index.get(uid, GeoRecord()),
                authordata=author_index.get(uid, AuthorRecord()),
                wd_metrics=popularity_index.get(uid, PopularityRecord()),
                readerstats=readerstat_index.get(uid, ReaderstatRecord()),
            )
        )

    return enriched_recs
