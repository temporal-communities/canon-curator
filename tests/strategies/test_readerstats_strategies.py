from freezegun import freeze_time

from canon_curator.enrich.strategies.readerstats.goodreads import _goodreads, goodreads_readerstats
from tests.testdata.goodreads import (
	EXPECTED_READERSTATS,
	EXPECTED_READERSTATS_EMPTY,
)


@freeze_time("2025-01-01 00:00:00")
def test_goodreads_success(mocker, base_record, expected_readerstats_record):
	mock_client = mocker.Mock()
	mock_client.fetch_readerstats.return_value = EXPECTED_READERSTATS
	mock_client.goodreads_base = "https://www.goodreads.com/"
	mocker.patch(
		"canon_curator.enrich.strategies.readerstats.goodreads.get_goodreads_client",
		return_value=mock_client,
	)
	result = _goodreads(base_record.work_goodreads_id, base_record.uuid)
	assert result == [expected_readerstats_record]


@freeze_time("2025-01-01 00:00:00")
def test_goodreads_return_empty(mocker, base_record):
	mock_client = mocker.Mock()
	mock_client.fetch_readerstats.return_value = EXPECTED_READERSTATS_EMPTY
	mocker.patch(
		"canon_curator.enrich.strategies.readerstats.goodreads.get_goodreads_client",
		return_value=mock_client,
	)
	result = _goodreads(base_record.work_goodreads_id, base_record.uuid)
	assert result == []


@freeze_time("2025-01-01 00:00:00")
def test_goodreads_readerstats_returns_empty(
	mocker, base_record, expected_empty_readerstats_record
):
	mocker.patch(
		"canon_curator.enrich.strategies.readerstats.goodreads._goodreads", return_value=[]
	)
	result = goodreads_readerstats(base_record)
	assert result == [expected_empty_readerstats_record]
