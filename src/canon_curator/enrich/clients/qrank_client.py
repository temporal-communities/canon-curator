from __future__ import annotations
import logging
from types import TracebackType
from typing import Self
import polars as pl

logger = logging.getLogger(__name__)


class QRankClient:
	"""
	Download QRank once from https://qrank.toolforge.org/ and load only rows containing relevant QIDs into a dictionary
	for efficient lookup.
	"""

	def __init__(
		self,
		name: str = "qrank",
		download_url: str = "https://qrank.toolforge.org/download/qrank.csv.gz",
	) -> None:
		self.name = name
		self.download_url = download_url
		self.scores: dict[str, int] | None = None

	def __enter__(self) -> Self:
		return self

	def __exit__(
		self,
		exc_type: type[BaseException] | None,
		exc_value: BaseException | None,
		traceback: TracebackType | None,
	) -> None:
		"""Ensure scores are reset when exiting the context."""
		self.scores = None

	@staticmethod
	def _normalise_qid(qid: str) -> str:
		return qid if qid.startswith("Q") else f"Q{qid}"

	def prefetch(self, qids: list[str]) -> None:
		if self.scores:
			return
		qids_norm = {self._normalise_qid(q) for q in qids if q}
		qrank_df = (
			pl.scan_csv(self.download_url, low_memory=True)
			.filter(pl.col("Entity").is_in(qids_norm))
			.collect()
		)

		self.scores = dict(qrank_df.iter_rows())

	def get_qrank(self, qid: str) -> int | None:
		if self.scores is None:
			return None
		return self.scores.get(self._normalise_qid(qid))
