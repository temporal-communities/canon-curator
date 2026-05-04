from typing import Self
from abc import ABC, abstractmethod
from collections.abc import Sequence
from pathlib import Path
from typing import TextIO

from canon_curator.models.records import EnrichedWorkRecord


class BaseExporter(ABC):
	def __init__(self, filename: str = "enriched_data", out_dir: Path | str = ".") -> None:
		self.filename = filename
		self.out_dir = Path(out_dir)
		self.output_path: Path | None = None
		self.file: TextIO | None = None

	def __enter__(self) -> Self:
		self.open()
		return self

	def __exit__(self, exc_type, exc_value, traceback) -> None:
		self.close()

	def open(self) -> None:
		"""Open the output file for writing."""
		if self.file is not None and not self.file.closed:
			raise RuntimeError("Exporter is already open.")
		self.out_dir.mkdir(parents=True, exist_ok=True)
		self.output_path = self.out_dir / self.filename
		self.file = open(self.output_path, "w", encoding="utf-8")

	def close(self) -> None:
		"""Close the output file."""
		if self.file and not self.file.closed:
			self.file.close()

	@abstractmethod
	def export(
		self,
		records: Sequence[EnrichedWorkRecord],
	) -> None:
		pass
