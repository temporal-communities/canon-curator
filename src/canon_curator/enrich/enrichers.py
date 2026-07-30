from __future__ import annotations
from collections.abc import Iterable, Sequence
from uuid import UUID

from canon_curator.models import (
	BaseWorkRecord,
	EnrichmentRecord,
	GeoRecord,
	AuthorRecord,
	PopularityRecord,
	ReaderstatsRecord,
)
from canon_curator.enrich.chains import StrategyChain
from canon_curator.enrich.clients import QRankClient, WikidataClient


class BaseEnricher[T: EnrichmentRecord]:
	"""
	Runs a given enrichment strategy chain and returns enrichment records for a list of BaseWorkRecords keyed by record id.
	Validates if provided strategies are allowed.
	"""

	name: str = "base"
	ALLOWED_STRATEGIES: frozenset[str] = frozenset()

	def __init__(self, chain: StrategyChain, strategies: Iterable[str]):
		self.chain = chain
		self.strategies = strategies
		self._validate()

	def _validate(self) -> None:
		invalid_strategy = set(self.strategies) - set(self.ALLOWED_STRATEGIES)
		if invalid_strategy:
			raise ValueError(
				f"{invalid_strategy} is not a valid strategy for {self.__class__.__name__}. "
				f"Allowed: {', '.join(self.ALLOWED_STRATEGIES)}"
			)

	def enrich(self, records: Iterable[BaseWorkRecord]) -> dict[UUID, Sequence[T]]:
		"""Applies the strategy chain to each record and collect results."""
		enrichment_recs: dict[UUID, Sequence[T]] = {}
		for rec in records:
			if rec.uuid is None:
				raise ValueError(f"Cannot enrich record without UUID. Record: {rec}")
			enrichment_recs[rec.uuid] = self.chain.run(rec)
		return enrichment_recs


class GeodataEnricher(BaseEnricher[GeoRecord]):
	name = "geodata"
	ALLOWED_STRATEGIES = frozenset({"gnd_geolabel", "wikidata_p19", "wikidata_p495"})


class AuthordataEnricher(BaseEnricher[AuthorRecord]):
	name = "authordata"
	ALLOWED_STRATEGIES = frozenset({"gnd_gender", "wikidata_p21"})


class PopularityEnricher(BaseEnricher[PopularityRecord]):
	name = "popularity"
	ALLOWED_STRATEGIES = frozenset({"wikidata_sitelinks", "wikidata_qrank"})

	def __init__(
		self,
		chain: StrategyChain,
		strategies: Iterable[str],
		qrank_client: QRankClient | None = None,
		wikidata_client: WikidataClient | None = None,
	) -> None:
		super().__init__(chain, strategies)
		self._qrank_client = qrank_client
		self._wikidata_client = wikidata_client

	def enrich(self, records: Iterable[BaseWorkRecord]) -> dict[UUID, Sequence[PopularityRecord]]:
		if self._wikidata_client is not None:
			self._wikidata_client.prefetch()
		if self._qrank_client is not None:
			qids = [rec.work_qid for rec in records if rec.work_qid]
			self._qrank_client.prefetch(qids)
		return super().enrich(records)


class ReaderstatEnricher(BaseEnricher[ReaderstatsRecord]):
	name = "readerstats"
	ALLOWED_STRATEGIES = frozenset({"goodreads"})
