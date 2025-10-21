from __future__ import annotations
from collections.abc import Callable, Sequence
from abc import ABC, abstractmethod

from canon_curator.models.enrichment import EnrichmentRecord
from canon_curator.models.records import BaseWorkRecord

type Strategy = Callable[[BaseWorkRecord], Sequence[EnrichmentRecord]]

class StrategyChain(ABC):
    def __init__(self, strategies: Sequence[Strategy]):
        self.strategies: list[Strategy] = list(strategies)

    @abstractmethod
    def run(self, record: BaseWorkRecord) -> Sequence[EnrichmentRecord]:
        """Run strategies to process records and return enrichment results."""
        pass

class FirstSuccessChain(StrategyChain):
    """
    Runs a sequence of enrichment strategies and returns the first successful result.
    Each strategy is applied to the given record in the order provided. As soon as a
    strategy produces at least one non-empty EnrichmentRecord, the chain stops and that
    record (or records) is returned. If all strategies yield empty records, a list with
    an empty EnrichmentRecord is returned.
    """
    def __init__(self, strategies: Sequence[Strategy]):
        super().__init__(strategies)

    def run(self, record: BaseWorkRecord) -> Sequence[EnrichmentRecord]:
        """Assumes strategy returns a list of enrichment records and returns the first non-empty result."""
        for strategy in self.strategies:
            enrichment_recs = strategy(record)
            if any(not rec.is_empty() for rec in enrichment_recs):
                return enrichment_recs
        return [EnrichmentRecord.empty()]
