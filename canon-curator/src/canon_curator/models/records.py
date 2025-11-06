from __future__ import annotations
from dataclasses import dataclass
from dataclasses import field
from canon_curator.models.enrichment import AuthorRecord, GeoRecord, PopularityRecord, ReaderstatRecord


@dataclass
class BaseWorkRecord:
    id: int | None = None
    list_num: int | None = None
    series_num: int | None = None
    title: str | None = None
    author: str | None = None
    author_qid: str | None = None
    work_qid: str | None = None
    author_gnd_id: str | None = None
    work_gnd_id: str | None = None
    work_goodreads_id: str | None = None
    publication_date: str | None = None


@dataclass
class EnrichedWorkRecord(BaseWorkRecord):
    base_data: BaseWorkRecord = field(default_factory=BaseWorkRecord)
    authordata: AuthorRecord = field(default_factory=AuthorRecord)
    geodata: GeoRecord = field(default_factory=GeoRecord)
    wd_metrics: PopularityRecord = field(default_factory=PopularityRecord)
    readerstats: ReaderstatRecord = field(default_factory=ReaderstatRecord)
