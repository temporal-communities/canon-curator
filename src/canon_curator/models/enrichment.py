from __future__ import annotations
from dataclasses import dataclass, field, fields
from datetime import datetime
from enum import StrEnum
from typing import Self
from uuid import UUID, uuid4


class EvidenceLevel(StrEnum):
	"""
	Registry of evidence levels used to qualify enrichment sources recorded in the 'sources' field

	- 'authoritative' should be used when the statement, claim or triple in the source database has a highly authoritative
	and reliable reference. Example: The reference points to a quote by the author about their own gender identity.
	This level usually requires additional parsing logic, like checking the date for recency and evaluating the reference URL.
	- 'referenced' should be used when the statement, claim or triple in the source database has a clear reference.
	References are usually URLs or IRIs. Example: Wikidata references qualified with P248 (stated in), P143 (imported from
	Wikimedia project), or a reference pointing to a record about a persons' gender in an authority file, including
	Wikidata references qualified with P214 (VIAF ID) or similar.
	- 'inferred' should be used when a statement, claim or triple in the source database is based on some sort of heuristic,
	like a name, linguistic marker, etc. Example: Wikidata references qualified with P887 (based on heuristic), or any claims
	about a person's gender based on gendered pronouns, names, or grammatical gender.

	If there are no references, the field 'evidence_level' should be left on the default value of None.
	"""

	AUTHORITATIVE = "authoritative"
	REFERENCED = "referenced"
	INFERRED = "inferred"


@dataclass
class EnrichmentRecord:
	uuid: UUID = field(
		default_factory=lambda: uuid4()
	)  # note: lambda is necessary for patching, do not remove
	work_uuid: UUID | None = None

	@classmethod
	def empty(cls) -> Self:
		"""Create an empty record with all default values."""
		return cls()

	def is_empty(self) -> bool:
		"""Return True if all fields are None."""
		return all(
			getattr(self, f.name) is None
			for f in fields(self)
			if f.name not in {"work_uuid", "uuid", "retrieved_at"}
		)

	def merge(self, other: Self) -> Self:
		"""Combine two records field-wise, filling missing values from other."""
		merged = {}
		for f in fields(self):
			merged[f.name] = getattr(self, f.name) or getattr(other, f.name)
		return type(self)(**merged)


@dataclass
class GeoRecord(EnrichmentRecord):
	geo_id: str | None = None
	geo_uri: str | None = None
	geo_label: str | None = None
	lat: float | None = None
	lon: float | None = None
	sources: list[str] | None = None
	num_sources: int | None = None
	evidence_level: EvidenceLevel | None = None
	source_db: str | None = None
	request_uri: str | None = None
	interpretation_context: str | None = None
	retrieved_at: datetime | None = None


@dataclass
class AuthorRecord(EnrichmentRecord):
	gender_uri: str | None = None
	gender_marker: str | None = None
	sources: list[str] | None = None
	num_sources: int | None = None
	evidence_level: EvidenceLevel | None = None
	source_db: str | None = None
	request_uri: str | None = None
	interpretation_context: str | None = None
	retrieved_at: datetime | None = None


@dataclass
class PopularityRecord(EnrichmentRecord):
	sitelinks_count: int | None = None
	q_rank: int | None = None
	retrieved_at: datetime | None = None


@dataclass
class ReaderstatsRecord(EnrichmentRecord):
	avg_rating: float | None = None
	ratings_count: int | None = None
	source: str | None = None
	retrieved_at: datetime | None = None
