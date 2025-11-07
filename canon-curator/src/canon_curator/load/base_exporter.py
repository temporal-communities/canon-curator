from abc import ABC, abstractmethod
from collections.abc import Sequence
from pathlib import Path

from canon_curator.models.records import EnrichedWorkRecord


class BaseExporter(ABC):
	@abstractmethod
	def export(
		self,
		records: Sequence[EnrichedWorkRecord],
		context_path: str | Path,
		shapes_path: str | Path,
		out_dir: str | Path,
		filename: str,
	) -> None:
		pass
