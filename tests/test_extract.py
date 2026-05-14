import pytest
from pathlib import Path

from canon_curator.extract import CSVReader


INPUT_TSV_PATH = Path(__file__).parent / "testdata" / "2025-spiegel-canon-international.tsv"
INPUT_TSV_PATH_EMPTY = Path(__file__).parent / "testdata" / "2025-spiegel-canon-international-empty.tsv"


def test_read_from_http_success(mocker, base_record): 
	mock_response = mocker.Mock()
	mock_response.text = INPUT_TSV_PATH.read_text(encoding="utf-8")
	mocker.patch(
		"canon_curator.extract.csv_reader.HttpClient.fetch_page",
		return_value=mock_response,
	)
	reader = CSVReader("https://github.com/temporal-communities/canon-shelf/data.tsv", delimiter="\t")
	with reader:
		work_records = reader.read_file()

	assert len(work_records) > 0
	first_rec = work_records[0]
	assert first_rec.title == base_record.title
	assert first_rec.author == base_record.author
	assert first_rec.work_qid == base_record.work_qid
	assert first_rec.publication_date == base_record.publication_date


def test_read_from_file_success(base_record):
	reader = CSVReader(INPUT_TSV_PATH, delimiter="\t")
	with reader:
		work_records = reader.read_file()

	assert len(work_records) > 0
	first_rec = work_records[0]
	assert first_rec.title == base_record.title
	assert first_rec.author == base_record.author
	assert first_rec.work_qid == base_record.work_qid
	assert first_rec.publication_date == base_record.publication_date


def test_raises_on_empty_file():
	reader = CSVReader(INPUT_TSV_PATH_EMPTY, delimiter="\t")
	with pytest.raises(RuntimeError, match="Input file appears to be empty"):
		reader.open()


def test_raises_on_uninitialised_reader():
	reader = CSVReader(INPUT_TSV_PATH, delimiter="\t")
	with pytest.raises(RuntimeError, match="File is not opened"):
		reader.read_file()