import pytest
from freezegun import freeze_time

from canon_curator.enrich.clients import GNDProperties
from canon_curator.enrich.strategies.geodata import wikidata_p19, wikidata_p495, gnd_geolabel
from canon_curator.enrich.strategies.geodata.wikidata_geo import _wikidata_geo
from canon_curator.enrich.strategies.geodata.gnd_geo import _gnd_geo
from tests.testdata.wikidata import (
    EXPECTED_FETCH_PROPERTY_RESULT_BIRTH_PLACE,
    EXPECTED_FETCH_PROPERTY_RESULT_COORDINATES_ERESOS,
    EXPECTED_FETCH_PROPERTY_RESULT_COORDINATES_LESBOS,
    EXPECTED_FETCH_PROPERTY_RESULT_COORDINATES_MYTILENE,
)
from tests.testdata.gnd import (
    EXPECTED_FETCH_PROPERTY_RETURN_GEOCODE,
    EXPECTED_FETCH_PROPERTY_RETURN_GEOMETRY,
    EXPECTED_STATEMENTS_GEOLABEL_GB,
)


@freeze_time("2025-01-01 00:00:00")
def test_wikidata_geo_success(
        mocker, base_record, expected_geo_record_wikidata, expected_geo_record_wikidata_no_evidence
):
    mock_client = mocker.Mock()
    mock_client.fetch_property.side_effect = [
        EXPECTED_FETCH_PROPERTY_RESULT_BIRTH_PLACE,
        EXPECTED_FETCH_PROPERTY_RESULT_COORDINATES_ERESOS,
        EXPECTED_FETCH_PROPERTY_RESULT_COORDINATES_LESBOS,
        EXPECTED_FETCH_PROPERTY_RESULT_COORDINATES_MYTILENE,
    ]
    mocker.patch(
        "canon_curator.enrich.strategies.geodata.wikidata_geo.get_wikidata_client",
        return_value=mock_client,
    )
    result = _wikidata_geo("Q17892", "P19", base_record.uuid)
    assert len(result) == 3
    assert result[0] == expected_geo_record_wikidata
    assert result[2] == expected_geo_record_wikidata_no_evidence


@freeze_time("2025-01-01 00:00:00")
def test_wikidata_p19_returns_empty(mocker, base_record, expected_empty_geo_record):
    mocker.patch(
        "canon_curator.enrich.strategies.geodata.wikidata_geo._wikidata_geo", return_value=[]
    )
    result = wikidata_p19(base_record)
    assert result == [expected_empty_geo_record]


@freeze_time("2025-01-01 00:00:00")
def test_wikidata_p495_returns_empty(mocker, base_record, expected_empty_geo_record):
    mocker.patch(
        "canon_curator.enrich.strategies.geodata.wikidata_geo._wikidata_geo", return_value=[]
    )
    result = wikidata_p495(base_record)
    assert result == [expected_empty_geo_record]


# add more examples later
@pytest.mark.parametrize(
    "resource_id, property_name, fetch_property_return, fetch_concept_return",
    [
        (
                "4316776-7",
                GNDProperties.GEOCODE,
                EXPECTED_FETCH_PROPERTY_RETURN_GEOCODE,
                EXPECTED_STATEMENTS_GEOLABEL_GB,
        ),
    ],
)
@freeze_time("2025-01-01 00:00:00")
def test_gnd_geo_geocode_success(
        mocker,
        resource_id,
        property_name,
        fetch_property_return,
        fetch_concept_return,
        expected_geo_record_gnd,
):
    mock_client = mocker.Mock()
    mock_client.lobid_base = "https://lobid.org/gnd/"
    mock_client.fetch_property.return_value = fetch_property_return
    mock_client.fetch_concept.return_value = fetch_concept_return
    mocker.patch(
        "canon_curator.enrich.strategies.geodata.gnd_geo.get_gnd_client",
        return_value=mock_client,
    )
    result = _gnd_geo(resource_id, property_name)
    assert len(result) == 1
    rec = result[0]
    assert rec.geo_id == expected_geo_record_gnd.geo_id
    assert rec.geo_uri == expected_geo_record_gnd.geo_uri
    assert rec.geo_label == expected_geo_record_gnd.geo_label
    assert rec.evidence_level is None


# add more examples later
@pytest.mark.parametrize(
    "resource_id, property_name, fetch_property_return",
    [("4022153-2", GNDProperties.GEOMETRY, EXPECTED_FETCH_PROPERTY_RETURN_GEOMETRY)],
)
@freeze_time("2025-01-01 00:00:00")
def test_gnd_geo_geometry_success(
        mocker, resource_id, property_name, fetch_property_return, expected_geo_record_gnd
):
    mock_client = mocker.Mock()
    mock_client.lobid_base = "https://lobid.org/gnd/"
    mock_client.fetch_property.return_value = fetch_property_return
    mocker.patch(
        "canon_curator.enrich.strategies.geodata.gnd_geo.get_gnd_client",
        return_value=mock_client,
    )
    result = _gnd_geo(resource_id, property_name)
    assert len(result) == 1
    rec = result[0]
    assert rec.lat == expected_geo_record_gnd.lat
    assert rec.lon == expected_geo_record_gnd.lon


@freeze_time("2025-01-01 00:00:00")
def test_gnd_geolabel_success(mocker, base_record, expected_geo_record_gnd):
    mock_client = mocker.Mock()
    mock_client.lobid_base = "https://lobid.org/gnd/"
    mock_client.fetch_property.side_effect = [
        EXPECTED_FETCH_PROPERTY_RETURN_GEOCODE,
        EXPECTED_FETCH_PROPERTY_RETURN_GEOMETRY,
    ]
    mock_client.fetch_concept.return_value = EXPECTED_STATEMENTS_GEOLABEL_GB
    mocker.patch(
        "canon_curator.enrich.strategies.geodata.gnd_geo.get_gnd_client",
        return_value=mock_client,
    )
    result = gnd_geolabel(base_record)
    assert result == [expected_geo_record_gnd]
