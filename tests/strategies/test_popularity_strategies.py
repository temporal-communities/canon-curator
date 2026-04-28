from freezegun import freeze_time

from canon_curator.enrich.strategies.popularity import wikidata_qrank, wikidata_sitelinks


@freeze_time("2025-01-01 00:00:00")
def test_wikidata_qrank_success(mocker, base_record, expected_qrank_record):
	mock_client = mocker.Mock()
	mock_client.get_qrank.return_value = 100
	mock_client.download_url = "https://qrank.toolforge.org/download/qrank.csv.gz"
	mocker.patch(
		"canon_curator.enrich.strategies.popularity.wikidata_qrank.get_qrank_client",
		return_value=mock_client,
	)
	result = wikidata_qrank(base_record)
	assert result == [expected_qrank_record]


@freeze_time("2025-01-01 00:00:00")
def test_wikidata_sitelinks_success(mocker, base_record, expected_sitelinks_record):
	mock_client = mocker.Mock()
	mock_client.fetch_sitelinks.return_value = 20
	mocker.patch(
		"canon_curator.enrich.strategies.popularity.wikidata_sitelinks.get_wikidata_client",
		return_value=mock_client,
	)
	result = wikidata_sitelinks(base_record)
	assert result == [expected_sitelinks_record]
