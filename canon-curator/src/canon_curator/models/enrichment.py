from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime


@dataclass
class GeoRecord:
    geo_uri: str | None = None
    geo_label: str | None = None
    lat: float | None = None
    lon: float | None = None
    source: str | None = None
    interpretation_context: str | None = None
    retrieved_at: datetime | None = None


@dataclass
class AuthorRecord:
    gender_marker: str | None = None
    source: str | None = None
    interpretation_context: str | None = None
    retrieved_at: datetime | None = None


@dataclass
class PopularityRecord:
    sitelinks_count: int | None = None
    q_rank: int | None = None
    retrieved_at: datetime | None = None


@dataclass
class ReaderstatRecord:
    avg_rating: float | None = None
    ratings_count: int | None = None
    source: str | None = None
    retrieved_at: datetime | None = None
