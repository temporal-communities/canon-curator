import csv
import uuid
from typing import TextIO
from collections.abc import Iterable

from canon_curator.extract import BaseReader
from canon_curator.models import BaseWorkRecord


class CSVReader(BaseReader):
	def __init__(self, filename: str, delimiter: str) -> None:
		super().__init__(filename)
		self.filename = filename
		self.delimiter = delimiter
		self.file: TextIO | None = None
		self._reader: csv.DictReader | None = None

	def open(self) -> None:
		self.file = open(self.filename, encoding="utf-8")
		self._reader = csv.DictReader(self.file, delimiter=self.delimiter)

	def close(self) -> None:
		if self.file and not self.file.closed:
			self.file.close()

	def read_file(self) -> Iterable[BaseWorkRecord]:
		records: list[BaseWorkRecord] = []
		if self._reader is None:
			raise RuntimeError("File is not opened.")
		for row in self._reader:
			records.append(
				BaseWorkRecord(
					uuid=uuid.uuid4(),  # convert to str here?
					list_num=row.get("List Number"),
					series_num=row.get("Series Number"),
					title=row.get("Title"),
					author=row.get("Author"),
					author_qid=row.get("Author_Wikidata_ID"),
					work_qid=row.get("Work_Wikidata_ID"),
					author_gnd_id=row.get("Author_GND_ID"),
					work_gnd_id=row.get("Work_GND_ID"),
					work_goodreads_id=row.get("Work_Goodreads_ID"),
					publication_date=row.get("Publication_Date"),
				)
			)

		return records
