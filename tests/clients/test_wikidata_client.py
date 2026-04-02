import pytest
import pywikibot

from canon_curator.enrich.clients import WikidataClient
from tests.testdata.wikidata import (
	CLAIM_BIRTH_PLACE_ERESOS,
	CLAIM_BIRTH_PLACE_LESBOS,
	CLAIM_BIRTH_PLACE_MYTILENE,
	CLAIM_COORDINATES,
	BIRTH_PLACE_CLAIMS,
	SAMPLE_CLAIMS,
	EXPECTED_REFERENCES_ERESOS,
	EXPECTED_REFERENCES_LESBOS,
	EXPECTED_REFERENCES_EMPTY,
	EXPECTED_TARGET_ERESOS,
	EXPECTED_TARGET_LESBOS,
	EXPECTED_TARGET_MYTILENE,
	EXPECTED_TARGET_COORDINATES,
	EXPECTED_TARGETS_BIRTH_PLACE,
	EXPECTED_FETCH_PROPERTY_RESULT_BIRTH_PLACE,
	EXPECTED_FETCH_PROPERTY_RESULT_COORDINATES,
	EXPECTED_EMPTY_RESULT,
)


@pytest.fixture
def client():
	return WikidataClient()


def test_fetch_item_page_success(mocker, client):
	client._repo = mocker.Mock()
	mock_item = mocker.Mock()
	mock_item.get = mocker.Mock()
	mock_constructor = mocker.patch("pywikibot.ItemPage", return_value=mock_item)
	result = client._fetch_item_page("Q219368")
	mock_constructor.assert_called_once()
	mock_item.get.assert_called_once()
	assert result is mock_item


def test_fetch_item_page_returns_none(mocker, client):
	client._repo = mocker.Mock()
	mock_item = mocker.Mock()
	mocker.patch("pywikibot.ItemPage", return_value=mock_item)
	mock_item.get.side_effect = pywikibot.exceptions.EntityTypeUnknownError("test")
	result = client._fetch_item_page("Q219368")
	mock_item.get.assert_called_once()
	assert result is None


@pytest.mark.parametrize(
	"property_id, entity_id, claims_collection",
	[
		("P19", "Q17892", BIRTH_PLACE_CLAIMS),
		("P625", "Q1018197", CLAIM_COORDINATES),
	],
)
def test_fetch_claims_success(mocker, client, property_id, entity_id, claims_collection):
	mock_claims = mocker.Mock()
	mock_claims.claims = {property_id: claims_collection}
	mocker.patch(
		"canon_curator.enrich.clients.WikidataClient._fetch_item_page", return_value=mock_claims
	)
	result = client._fetch_claims(property_id, entity_id)
	assert result == claims_collection


def test_fetch_claims_property_id_not_found(mocker, client):
	mock_claims = mocker.Mock()
	mock_claims.claims = {"P19": SAMPLE_CLAIMS}
	mocker.patch(
		"canon_curator.enrich.clients.WikidataClient._fetch_item_page", return_value=mock_claims
	)
	result = client._fetch_claims("P20", "Q17892")
	assert result is None


@pytest.mark.parametrize(
	"mocked_return, expected_return",
	[
		(CLAIM_BIRTH_PLACE_ERESOS, EXPECTED_REFERENCES_ERESOS),
		(CLAIM_BIRTH_PLACE_LESBOS, EXPECTED_REFERENCES_LESBOS),
		(CLAIM_BIRTH_PLACE_MYTILENE, EXPECTED_REFERENCES_EMPTY),
		(CLAIM_COORDINATES, EXPECTED_REFERENCES_EMPTY),
	],
)
def test_fetch_sources_success(client, mocked_return, expected_return):
	return_value = client._fetch_sources(mocked_return)
	assert return_value == expected_return


@pytest.mark.parametrize(
	"claim, expected",
	[
		(CLAIM_BIRTH_PLACE_ERESOS, EXPECTED_TARGET_ERESOS),
		(CLAIM_BIRTH_PLACE_LESBOS, EXPECTED_TARGET_LESBOS),
		(CLAIM_BIRTH_PLACE_MYTILENE, EXPECTED_TARGET_MYTILENE),
	],
)
def test_fetch_target_item_success(mocker, client, claim, expected):
	mock_target = mocker.Mock(spec=["labels", "getID"])
	mock_target.labels = {"en": expected["label"]}
	mock_target.getID.return_value = expected["entity_id"]
	mocker.patch.object(claim, "getTarget", return_value=mock_target)
	result = client._fetch_target(claim, "en")
	assert result == expected


@pytest.mark.parametrize(
	"claim, expected",
	[
		(CLAIM_COORDINATES, EXPECTED_TARGET_COORDINATES),
	],
)
def test_fetch_target_coordinates_success(mocker, client, claim, expected):
	mock_target = mocker.Mock(spec=["lat", "lon"])
	mock_target.lat = expected["latitude"]
	mock_target.lon = expected["longitude"]
	mocker.patch.object(claim, "getTarget", return_value=mock_target)
	result = client._fetch_target(claim, "en")
	assert result == expected


@pytest.mark.parametrize(
	"property_id, entity_id, claims_collection, targets, sources, expected_return",
	[
		(
			"P19",
			"Q17892",
			BIRTH_PLACE_CLAIMS,
			EXPECTED_TARGETS_BIRTH_PLACE,
			[EXPECTED_REFERENCES_ERESOS, EXPECTED_REFERENCES_LESBOS, EXPECTED_REFERENCES_EMPTY],
			EXPECTED_FETCH_PROPERTY_RESULT_BIRTH_PLACE,
		),
		(
			"P625",
			"Q1018197",
			[CLAIM_COORDINATES],
			[EXPECTED_TARGET_COORDINATES],
			[EXPECTED_REFERENCES_EMPTY],
			EXPECTED_FETCH_PROPERTY_RESULT_COORDINATES,
		),
	],
)
def test_fetch_property_success(
	mocker,
	client,
	property_id,
	entity_id,
	claims_collection,
	targets,
	sources,
	expected_return,
):
	mocker.patch(
		"canon_curator.enrich.clients.WikidataClient._fetch_claims",
		return_value=claims_collection,
	)

	mocker.patch(
		"canon_curator.enrich.clients.WikidataClient._fetch_target",
		side_effect=targets,
	)

	mocker.patch(
		"canon_curator.enrich.clients.WikidataClient._fetch_sources",
		side_effect=sources,
	)

	result = client.fetch_property(entity_id, property_id)

	assert result == expected_return


def test_fetch_property_returns_empty(mocker, client):
	mocker.patch("canon_curator.enrich.clients.WikidataClient._fetch_claims", return_value=None)
	result = client.fetch_property("Q17892", "P20")
	assert result == EXPECTED_EMPTY_RESULT
