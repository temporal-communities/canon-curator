from __future__ import annotations
from collections.abc import Callable, Sequence
from abc import ABC, abstractmethod

from canon_curator.models import EnrichmentRecord, BaseWorkRecord

type Strategy[T: EnrichmentRecord] = Callable[[BaseWorkRecord], Sequence[T]]


class StrategyChain[T: EnrichmentRecord](ABC):
	def __init__(self, strategies: Sequence[Strategy[T]]):
		self.strategies: list[Strategy[T]] = list(strategies)

	@abstractmethod
	def run(self, record: BaseWorkRecord) -> Sequence[T]:
		"""Run strategies to process records and return enrichment results."""
		pass


class FirstSuccessChain[T: EnrichmentRecord](StrategyChain[T]):
	"""
	Runs a sequence of enrichment strategies and returns the first successful result.
	Each strategy is applied to the given record in the order provided. As soon as a
	strategy produces at least one non-empty EnrichmentRecord, the chain stops and that
	record (or records) is returned. If all strategies yield empty records, a list with
	an empty EnrichmentRecord is returned.
	"""

	def run(self, record: BaseWorkRecord) -> Sequence[T]:
		"""Assumes strategy returns a list of enrichment records and returns the first non-empty result."""
		enrichment_recs: Sequence[T] = []
		for strategy in self.strategies:
			enrichment_recs = strategy(record)
			if any(not rec.is_empty() for rec in enrichment_recs):
				return enrichment_recs
		return enrichment_recs


class KeepAllChain[T: EnrichmentRecord](StrategyChain[T]):
	"""
	Runs a sequence of enrichment strategies and returns all results. Each strategy
	is applied to the given record in the order provided. The chain stops when all
	strategies have been tried.
	"""

	def run(self, record: BaseWorkRecord) -> Sequence[T]:
		"""Assumes strategy returns a list of enrichment records and returns all results."""
		enrichment_recs: list[T] = []
		for strategy in self.strategies:
			enrichment_recs.extend(strategy(record))

		return enrichment_recs
