from __future__ import annotations
from collections.abc import Callable, Iterable, Sequence

from canon_curator.enrich.strategies.registry import StrategyRegistry
from canon_curator.models import (
	BaseWorkRecord,
	EnrichmentRecord,
	GeoRecord,
	AuthorRecord,
	PopularityRecord,
	ReaderstatRecord,
)
from canon_curator.enrich.chains import StrategyChain


class BaseEnricher:
	"""
	Runs a given enrichment strategy chain and returns enrichment records for a list of BaseWorkRecords keyed by record id.
	Validates if provided strategies are allowed.
	"""

	name: str = "base"
	ALLOWED_STRATEGIES: tuple[Callable[[BaseWorkRecord], Sequence[EnrichmentRecord]], ...] = ()

	def __init__(self, chain: StrategyChain):
		self.chain = chain
		self._validate()

	def _validate(self):
		for strategy in self.chain.strategies:
			if strategy not in self.ALLOWED_STRATEGIES:
				allowed_names = {s.__name__ for s in self.ALLOWED_STRATEGIES}
				raise ValueError(
					f"{strategy.__name__} is not a valid strategy for {self.__class__.__name__}. "
					f"Allowed: {', '.join(allowed_names)}"
				)

	def enrich(
		self, records: Iterable[BaseWorkRecord]
	) -> dict[int | None, Sequence[EnrichmentRecord]]:
		"""Applies the strategy chain to each record and collect results."""
		enrichment_recs: dict[int | None, Sequence[EnrichmentRecord]] = {}
		for rec in records:
			enrichment_recs[rec.id] = self.chain.run(rec)
		return enrichment_recs


class GeodataEnricher(BaseEnricher):
	name = "geodata"
	ALLOWED_STRATEGIES: tuple[Callable[[BaseWorkRecord], Sequence[GeoRecord]], ...] = (
		StrategyRegistry.GND_GEOLABEL,
		StrategyRegistry.WIKIDATA_P19,
		StrategyRegistry.WIKIDATA_P495,
	)

	def __init__(self, chain: StrategyChain):
		super().__init__(chain)


class AuthordataEnricher(BaseEnricher):
	name = "authordata"
	ALLOWED_STRATEGIES: tuple[Callable[[BaseWorkRecord], Sequence[AuthorRecord]], ...] = (
		StrategyRegistry.GND_GENDER,
		StrategyRegistry.WIKIDATA_P21,
	)

	def __init__(self, chain: StrategyChain):
		super().__init__(chain)


class PopularityEnricher(BaseEnricher):
	name = "popularity"
	ALLOWED_STRATEGIES: tuple[Callable[[BaseWorkRecord], Sequence[PopularityRecord]], ...] = (
		StrategyRegistry.WIKIDATA_SITELINKS,
		StrategyRegistry.WIKIDATA_QRANK,
	)

	def __init__(self, chain: StrategyChain):
		super().__init__(chain)


class ReaderstatEnricher(BaseEnricher):
	name = "readerstats"
	ALLOWED_STRATEGIES: tuple[Callable[[BaseWorkRecord], Sequence[ReaderstatRecord]], ...] = (
		StrategyRegistry.GOODREADS,
	)

	def __init__(self, chain: StrategyChain):
		super().__init__(chain)
