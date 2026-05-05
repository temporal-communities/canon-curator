import pytest

from canon_curator.enrich.clients import WikidataClient
from tests.testdata.wikidata import (
	ENTITY_Q17892,
	ENTITY_Q1018197,
	CLAIM_BIRTH_PLACE_ERESOS,
	CLAIM_BIRTH_PLACE_LESBOS,
	CLAIM_BIRTH_PLACE_MYTILENE,
	CLAIM_COORDINATES,
	BIRTH_PLACE_CLAIMS,
	COORDINATES_CLAIMS,
	SAMPLE_CLAIMS,
	EXPECTED_REFERENCES_ERESOS,
	EXPECTED_REFERENCES_LESBOS,
	EXPECTED_REFERENCES_EMPTY,
	EXPECTED_DATAVALUE_ERESOS,
	EXPECTED_DATAVALUE_LESBOS,
	EXPECTED_DATAVALUE_MYTILENE,
	EXPECTED_DATAVALUE_COORDINATES,
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


@pytest.mark.parametrize(
	"property_id, entity_id, entity, claims_collection",
	[
		("P19", "Q17892", ENTITY_Q17892, BIRTH_PLACE_CLAIMS),
		("P625", "Q1018197", ENTITY_Q1018197, COORDINATES_CLAIMS),
	],
)
def test_fetch_claims_success(client, property_id, entity_id, entity, claims_collection):
	entity_data = entity.get("entities", {}).get(entity_id)
	result = client._fetch_claims(entity_data, property_id)
	assert result == claims_collection


@pytest.mark.parametrize(
	"property_id, entity_id, entity",
	[
		("P200", "Q17892", ENTITY_Q17892),
	],
)
def test_fetch_claims_property_id_not_found(client, property_id, entity_id, entity):
	entity_data = entity.get("entities", {}).get(entity_id)
	result = client._fetch_claims(entity_data, property_id)
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
def test_parse_references_success(client, mocked_return, expected_return):
	return_value = client._parse_references(mocked_return)
	assert return_value == expected_return


@pytest.mark.parametrize(
	"claim, expected",
	[
		(CLAIM_BIRTH_PLACE_ERESOS, EXPECTED_DATAVALUE_ERESOS),
		(CLAIM_BIRTH_PLACE_LESBOS, EXPECTED_DATAVALUE_LESBOS),
		(CLAIM_BIRTH_PLACE_MYTILENE, EXPECTED_DATAVALUE_MYTILENE),
		(CLAIM_COORDINATES, EXPECTED_DATAVALUE_COORDINATES),
	],
)
def test_parse_datavalue_success(client, claim, expected):
	result = client._parse_datavalue(claim["mainsnak"]["datavalue"])
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
		"canon_curator.enrich.clients.WikidataClient._fetch_entity",
		return_value={"test_id": entity_id},
	)

	mocker.patch(
		"canon_curator.enrich.clients.WikidataClient._fetch_claims",
		return_value=claims_collection,
	)

	mocker.patch(
		"canon_curator.enrich.clients.WikidataClient._parse_datavalue",
		side_effect=targets,
	)

	mocker.patch(
		"canon_curator.enrich.clients.WikidataClient._fetch_label",
		side_effect=["Eresos", "Lesbos", "Mytilene"],
	)

	mocker.patch(
		"canon_curator.enrich.clients.WikidataClient._parse_references",
		side_effect=sources,
	)

	result = client.fetch_property(entity_id, property_id)

	assert result == expected_return


def test_fetch_property_returns_empty(mocker, client):
	mocker.patch(
		"canon_curator.enrich.clients.WikidataClient._fetch_entity",
		return_value={"id": "Q17892"},
	)
	mocker.patch("canon_curator.enrich.clients.WikidataClient._fetch_claims", return_value=None)
	result = client.fetch_property("Q17892", "P20")
	assert result == EXPECTED_EMPTY_RESULT


@pytest.mark.parametrize(
	"entity_id, entity, wikipedia_only, expected_result",
	[
		("Q17892", ENTITY_Q17892, False, 147),
		("Q17892", ENTITY_Q17892, True, 112),
	],
)
def test_fetch_sitelinks_success(mocker, client, entity_id, entity, wikipedia_only, expected_result):
	entity_data = entity.get("entities", {}).get(entity_id)
	mocker.patch(
		"canon_curator.enrich.clients.WikidataClient._fetch_entity",
		return_value=entity_data,
	)
	result = client.fetch_sitelinks(entity_id, wikipedia_only)
	assert result == expected_result