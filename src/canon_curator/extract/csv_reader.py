import csv
import uuid
from typing import TextIO
from pathlib import Path
from functools import cached_property
from io import StringIO

from canon_curator.enrich.clients.http_client import HttpClient
from canon_curator.extract import BaseReader
from canon_curator.models import BaseWorkRecord


class CSVReader(BaseReader):
	def __init__(self, input_file: Path | str, delimiter: str) -> None:
		super().__init__(input_file)
		self.delimiter = delimiter
		self.file: TextIO | None = None
		self._reader: csv.DictReader | None = None

	@cached_property
	def _http_client(self) -> HttpClient:
		return HttpClient(rate_limit="1/second", client_key="csv-reader")

	def open(self) -> None:
		if isinstance(self.input_file, str) and self.input_file.startswith("http"):
			response = self._http_client.fetch_page(self.input_file)
			if not response:
				raise RuntimeError(f"Failed to fetch {self.input_file}")
			self.file = StringIO(response.text)
		else:
			self.file = open(self.input_file, encoding="utf-8")
		self._reader = csv.DictReader(self.file, delimiter=self.delimiter)

	def close(self) -> None:
		if self.file and not self.file.closed:
			self.file.close()

		if "_http_client" in self.__dict__:
			self._http_client.__exit__(None, None, None)

	def read_file(self) -> list[BaseWorkRecord]:
		records: list[BaseWorkRecord] = []
		if self._reader is None:
			raise RuntimeError("File is not opened.")
		for row in self._reader:
			records.append(
				BaseWorkRecord(
					uuid=uuid.uuid4(),
					list_num=row.get("List Number"),
					series_num=row.get("Series Number"),
					title=row.get("Title"),
					author=row.get("Author"),
					author_qid=row.get("Author Wikidata ID"),
					work_qid=row.get("Work Wikidata ID"),
					author_gnd_id=row.get("Author GND ID"),
					work_gnd_id=row.get("Work GND ID"),
					work_goodreads_id=row.get("Work Goodreads ID"),
					publication_date=row.get("Publication Date"),
				)
			)

		return records
