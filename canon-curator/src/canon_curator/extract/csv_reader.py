from canon_curator.extract.base_reader import BaseReader
from canon_curator.models.records import BaseWorkRecord


class CSVReader(BaseReader):

    def open(self) -> None:
        pass

    def close(self) -> None:
        pass

    def read_file(self) -> BaseWorkRecord:
        pass
