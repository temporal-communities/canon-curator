import json
import logging
from collections.abc import Sequence
from dataclasses import asdict
from pathlib import Path

from canon_curator.load.base_exporter import BaseExporter
from canon_curator.models import EnrichedWorkRecord

logger = logging.getLogger(__name__)


class JSONLinesExporter(BaseExporter):
	def __init__(self, filename: str, out_dir: Path | str = ".") -> None:
		super().__init__(filename, out_dir)
		self.filename = filename if str(filename).endswith(".jsonl") else f"{filename}.jsonl"

	def export(self, records: Sequence[EnrichedWorkRecord]):
		"""Write records to the open file as JSON Lines."""
		if self.file is None or self.file.closed:
			raise RuntimeError("Export failed. Use as context manager or call open() first.")
		for record in records:
			self.file.write(json.dumps(asdict(record), default=str, ensure_ascii=False) + "\n")
		logger.info(f"Wrote {len(records)} records to {self.output_path}.")
