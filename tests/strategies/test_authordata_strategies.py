from freezegun import freeze_time

from canon_curator.enrich.clients import GNDProperties
from canon_curator.enrich.strategies.authordata import wikidata_p21, gnd_gender
from canon_curator.enrich.strategies.authordata.wikidata_author import _wikidata_author
from canon_curator.enrich.strategies.authordata.gnd_author import _gnd_author
from tests.testdata.wikidata import EXPECTED_FETCH_PROPERTY_RESULT_GENDER
from tests.testdata.gnd import EXPECTED_FETCH_PROPERTY_RETURN_GENDER


@freeze_time("2025-01-01 00:00:00")
def test_wikidata_author_success(mocker, base_record, expected_author_record_wikidata):
    mock_client = mocker.Mock()
    mock_client.fetch_property.return_value = EXPECTED_FETCH_PROPERTY_RESULT_GENDER
    result = _wikidata_author("Q40909", "P21", base_record.uuid, client=mock_client)
    assert len(result) == 1
    assert result[0] == expected_author_record_wikidata


@freeze_time("2025-01-01 00:00:00")
def test_wikidata_p21_returns_empty(mocker, base_record, expected_empty_author_record):
    mocker.patch(
        "canon_curator.enrich.strategies.authordata.wikidata_author._wikidata_author",
        return_value=[],
    )
    result = wikidata_p21(base_record, client=mocker.Mock())
    assert result == [expected_empty_author_record]


@freeze_time("2025-01-01 00:00:00")
def test_gnd_author_success(mocker, base_record, expected_author_record_gnd):
    mock_client = mocker.Mock()
    mock_client.lobid_base = "https://lobid.org/gnd/"
    mock_client.fetch_property.return_value = EXPECTED_FETCH_PROPERTY_RETURN_GENDER
    result = _gnd_author("118635174", base_record.uuid, GNDProperties.GENDER, client=mock_client)
    assert len(result) == 1
    assert result[0] == expected_author_record_gnd


@freeze_time("2025-01-01 00:00:00")
def test_gnd_gender_success(mocker, base_record, expected_author_record_gnd):
    mock_client = mocker.Mock()
    mock_client.lobid_base = "https://lobid.org/gnd/"
    mock_client.fetch_property.return_value = EXPECTED_FETCH_PROPERTY_RETURN_GENDER
    result = gnd_gender(base_record, client=mock_client)
    assert len(result) == 1
    assert result[0] == expected_author_record_gnd
