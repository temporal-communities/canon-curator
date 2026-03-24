from __future__ import annotations
from collections.abc import Iterable, Sequence
from uuid import UUID

from canon_curator.enrich.strategies.registry import Strategy, StrategyRegistry
from canon_curator.models import (
	BaseWorkRecord,
	EnrichmentRecord,
	GeoRecord,
	AuthorRecord,
	PopularityRecord,
	ReaderstatsRecord,
)
from canon_curator.enrich.chains import StrategyChain


class BaseEnricher[T: EnrichmentRecord]:
	"""
	Runs a given enrichment strategy chain and returns enrichment records for a list of BaseWorkRecords keyed by record id.
	Validates if provided strategies are allowed.
	"""

	name: str = "base"
	ALLOWED_STRATEGIES: tuple[Strategy[T], ...] = ()

	def __init__(self, chain: StrategyChain):
		self.chain = chain
		self._validate()

	def _validate(self) -> None:
		for strategy in self.chain.strategies:
			if strategy not in self.ALLOWED_STRATEGIES:
				allowed_names = {s.__name__ for s in self.ALLOWED_STRATEGIES}
				raise ValueError(
					f"{strategy.__name__} is not a valid strategy for {self.__class__.__name__}. "
					f"Allowed: {', '.join(allowed_names)}"
				)

	def enrich(
		self, records: Iterable[BaseWorkRecord]
	) -> dict[UUID | None, Sequence[EnrichmentRecord]]:
		"""Applies the strategy chain to each record and collect results."""
		enrichment_recs: dict[UUID | None, Sequence[EnrichmentRecord]] = {}
		for rec in records:
			enrichment_recs[rec.uuid] = self.chain.run(rec)
		return enrichment_recs


class GeodataEnricher(BaseEnricher[GeoRecord]):
	name = "geodata"
	ALLOWED_STRATEGIES: tuple[Strategy[GeoRecord], ...] = (
		StrategyRegistry.GND_GEOLABEL,
		StrategyRegistry.WIKIDATA_P19,
		StrategyRegistry.WIKIDATA_P495,
	)

	def __init__(self, chain: StrategyChain):
		super().__init__(chain)


class AuthordataEnricher(BaseEnricher[AuthorRecord]):
	name = "authordata"
	ALLOWED_STRATEGIES: tuple[Strategy[AuthorRecord], ...] = (
		StrategyRegistry.GND_GENDER,
		StrategyRegistry.WIKIDATA_P21,
	)

	def __init__(self, chain: StrategyChain):
		super().__init__(chain)


class PopularityEnricher(BaseEnricher[PopularityRecord]):
	name = "popularity"
	ALLOWED_STRATEGIES: tuple[Strategy[PopularityRecord], ...] = (
		StrategyRegistry.WIKIDATA_SITELINKS,
		StrategyRegistry.WIKIDATA_QRANK,
	)

	def __init__(self, chain: StrategyChain):
		super().__init__(chain)


class ReaderstatEnricher(BaseEnricher[ReaderstatsRecord]):
	name = "readerstats"
	ALLOWED_STRATEGIES: tuple[Strategy[ReaderstatsRecord], ...] = (StrategyRegistry.GOODREADS,)

	def __init__(self, chain: StrategyChain):
		super().__init__(chain)
