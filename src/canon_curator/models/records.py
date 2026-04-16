from __future__ import annotations
from dataclasses import dataclass
from dataclasses import field
from uuid import UUID

from canon_curator.models.enrichment import (
	AuthorRecord,
	GeoRecord,
	PopularityRecord,
	ReaderstatsRecord,
)


@dataclass
class BaseWorkRecord:
	uuid: UUID | None = None
	list_num: str | None = None
	series_num: str | None = None
	title: str | None = None
	author: str | None = None
	author_qid: str | None = None
	work_qid: str | None = None
	author_gnd_id: str | None = None
	work_gnd_id: str | None = None
	work_goodreads_id: str | None = None
	publication_date: str | None = None


@dataclass
class EnrichedWorkRecord:
	base_data: BaseWorkRecord = field(default_factory=BaseWorkRecord)
	authordata: list[AuthorRecord] = field(default_factory=list)
	geodata: list[GeoRecord] = field(default_factory=list)
	wd_metrics: PopularityRecord = field(default_factory=PopularityRecord)
	readerstats: ReaderstatsRecord = field(default_factory=ReaderstatsRecord)
