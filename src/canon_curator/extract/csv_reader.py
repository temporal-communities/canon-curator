import csv
import uuid
import logging
from urllib.parse import urlparse
from typing import TextIO
from pathlib import Path
from functools import cached_property
from io import StringIO

from canon_curator.enrich.clients.http_client import HttpClient
from canon_curator.extract import BaseReader
from canon_curator.models import BaseWorkRecord


logger = logging.getLogger(__name__)


COLUMN_NAMES: dict[str, str] = {
	"list_num": "List Number",
	"series_num": "Series Number",
	"title": "Title",
	"author": "Author",
	"author_qid": "Author Wikidata ID",
	"work_qid": "Work Wikidata ID",
	"author_gnd_id": "Author GND ID",
	"work_gnd_id": "Work GND ID",
	"work_goodreads_id": "Work Goodreads ID",
	"publication_date": "Publication Date",
}


REQUIRED_COLS: frozenset[str] = frozenset(COLUMN_NAMES.values())


class CSVReader(BaseReader):
	def __init__(self, input_file: Path | str, delimiter: str) -> None:
		super().__init__(input_file)
		self.delimiter = delimiter
		self.file: TextIO | None = None
		self._reader: csv.DictReader | None = None

	@cached_property
	def _http_client(self) -> HttpClient:
		return HttpClient(rate_limit="1/second", client_key="csv-reader")

	def _validate(self) -> None:
		if self._reader is None:
			raise RuntimeError("File is not opened.")

		input_cols = set(self._reader.fieldnames or [])
		if not input_cols:
			raise RuntimeError("Input file appears to be empty: no header row found.")

		missing_cols = REQUIRED_COLS - input_cols
		extra_cols = input_cols - REQUIRED_COLS

		if missing_cols:
			logger.warning(
				"Input file is missing columns: %s. "
				"Verify your file follows the template at https://github.com/temporal-communities/canon-shelf.",
				", ".join(missing_cols),
			)
		if extra_cols:
			logger.warning(
				"Input file contains unknown columns that will be ignored: %s",
				", ".join(extra_cols),
			)

	def open(self) -> None:
		if self.file is not None:
			raise RuntimeError("File is already open.")
		if isinstance(self.input_file, str) and urlparse(self.input_file).scheme in (
			"http",
			"https",
		):
			response = self._http_client.fetch_page(self.input_file)
			if not response:
				raise RuntimeError(f"Failed to fetch {self.input_file}")
			self.file = StringIO(response.text)
		else:
			self.file = open(self.input_file, encoding="utf-8")
		self._reader = csv.DictReader(self.file, delimiter=self.delimiter)
		self._validate()

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
					list_num=row.get(COLUMN_NAMES["list_num"]),
					series_num=row.get(COLUMN_NAMES["series_num"]),
					title=row.get(COLUMN_NAMES["title"]),
					author=row.get(COLUMN_NAMES["author"]),
					author_qid=row.get(COLUMN_NAMES["author_qid"]),
					work_qid=row.get(COLUMN_NAMES["work_qid"]),
					author_gnd_id=row.get(COLUMN_NAMES["author_gnd_id"]),
					work_gnd_id=row.get(COLUMN_NAMES["work_gnd_id"]),
					work_goodreads_id=row.get(COLUMN_NAMES["work_goodreads_id"]),
					publication_date=row.get(COLUMN_NAMES["publication_date"]),
				)
			)

		return records
