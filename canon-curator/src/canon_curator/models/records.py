from __future__ import annotations
from dataclasses import dataclass
from dataclasses import field
from canon_curator.models.enrichment import AuthorRecord
from canon_curator.models.enrichment import GeoRecord
from canon_curator.models.enrichment import PopularityRecord
from canon_curator.models.enrichment import ReaderstatRecord


@dataclass
class BaseWorkRecord:
    list_num: int
    series_num: int
    title: str | None = None
    author: str | None = None
    author_qid: str | None = None
    work_qid: str | None = None
    author_gnd_id: str | None = None
    work_gnd_id: str | None = None
    work_goodreads_id: str | None = None
    first_ed_place: str | None = None
    first_ed_publisher: str | None = None
    publication_date: str | None = None


@dataclass
class EnrichedWorkRecord(BaseWorkRecord):
    base_data: BaseWorkRecord = field(default_factory=BaseWorkRecord)
    authordata: AuthorRecord = field(default_factory=AuthorRecord)
    geodata: GeoRecord = field(default_factory=GeoRecord)
    wd_metrics: PopularityRecord = field(default_factory=PopularityRecord)
    readerstats: ReaderstatRecord = field(default_factory=ReaderstatsRecord)
