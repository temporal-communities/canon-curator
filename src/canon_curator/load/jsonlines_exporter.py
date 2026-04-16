import json
import logging
from typing import TextIO
from collections.abc import Sequence
from pathlib import Path
from dataclasses import asdict

from canon_curator.load.base_exporter import BaseExporter
from canon_curator.models import EnrichedWorkRecord

logger = logging.getLogger(__name__)


class JSONLinesExporter(BaseExporter):
	def __init__(self, filename: str, out_dir: str = ".") -> None:
		super().__init__(filename, out_dir)
		self.filename = filename if str(filename).endswith(".jsonl") else f"{filename}.jsonl"
		self.output_path: Path | None = None
		self.file: TextIO | None = None

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

	def export(self, records: Sequence[EnrichedWorkRecord]):
		"""Write records to the open file as JSON Lines."""
		if self.file is None or self.file.closed:
			raise RuntimeError("Export failed. Use as context manager or call open() first.")
		for record in records:
			self.file.write(json.dumps(asdict(record), default=str, ensure_ascii=False) + "\n")
		logger.info(f"Wrote {len(records)} records to {self.output_path}.")
