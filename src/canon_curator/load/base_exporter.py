from typing import Self
from abc import ABC, abstractmethod
from collections.abc import Sequence
from pathlib import Path

from canon_curator.models.records import EnrichedWorkRecord


class BaseExporter(ABC):
	def __init__(self, filename: str = "enriched_data", out_dir: str = ".") -> None:
		self.filename = filename
		self.out_dir = Path(out_dir)

	def __enter__(self) -> Self:
		self.open()
		return self

	def __exit__(self, exc_type, exc_value, traceback) -> None:
		self.close()

	@abstractmethod
	def open(self) -> None:
		pass

	@abstractmethod
	def close(self) -> None:
		pass

	@abstractmethod
	def export(
		self,
		records: Sequence[EnrichedWorkRecord],
	) -> None:
		pass
