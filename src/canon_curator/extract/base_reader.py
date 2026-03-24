from abc import ABC, abstractmethod
from typing import Self
from collections.abc import Iterable

from canon_curator.models import BaseWorkRecord


class BaseReader(ABC):
	def __init__(self, filename: str) -> None:
		self.filename = filename

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
	def read_file(self) -> Iterable[BaseWorkRecord]:
		pass
