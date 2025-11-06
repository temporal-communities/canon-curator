from __future__ import annotations
from dataclasses import dataclass, fields
from datetime import datetime
from uuid import UUID


@dataclass
class EnrichmentRecord:

    @classmethod
    def empty(cls) -> EnrichmentRecord:
        """Create an empty record with all default values."""
        return cls()

    def is_empty(self) -> bool:
        """Return True if all fields are None."""
        return all(getattr(self, f.name) is None for f in fields(self))


@dataclass
class GeoRecord(EnrichmentRecord):
    rec_uuid: UUID | None = None
    ext_id: str | None = None
    geo_uri: str | None = None
    geo_label: str | None = None
    lat: float | None = None
    lon: float | None = None
    source: str | None = None
    interpretation_context: str | None = None
    retrieved_at: datetime | None = None


@dataclass
class AuthorRecord(EnrichmentRecord):
    rec_uuid: UUID | None = None
    gender_marker: str | None = None
    source: str | None = None
    interpretation_context: str | None = None
    retrieved_at: datetime | None = None


@dataclass
class PopularityRecord(EnrichmentRecord):
    rec_uuid: UUID | None = None
    sitelinks_count: int | None = None
    q_rank: int | None = None
    retrieved_at: datetime | None = None


@dataclass
class ReaderstatRecord(EnrichmentRecord):
    rec_uuid: UUID | None = None
    avg_rating: float | None = None
    ratings_count: int | None = None
    source: str | None = None
    retrieved_at: datetime | None = None
