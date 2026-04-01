import pytest
from rdflib import URIRef, Graph

from canon_curator.enrich.clients import GNDClient, GNDProperties
from tests.testdata.gnd import (
	SAMPLE_ENTRY_GENDER,
	SAMPLE_ENTRY_GEOCODE,
	SAMPLE_ENTRY_GEOMETRY,
	EXPECTED_VALUES_GENDER,
	EXPECTED_VALUES_GEOCODE,
	EXPECTED_VALUES_GEOMETRY,
	GENDER_VOCAB,
	EXPECTED_STATEMENTS_MALE,
	EXPECTED_STATEMENTS_FEMALE,
	EXPECTED_STATEMENTS_NOTKNOWN,
)


@pytest.fixture
def client():
	return GNDClient()


@pytest.mark.parametrize(
	"entry, property_name, expected_values",
	[
		(SAMPLE_ENTRY_GENDER, GNDProperties.GENDER, EXPECTED_VALUES_GENDER),
		(SAMPLE_ENTRY_GEOCODE, GNDProperties.GEOCODE, EXPECTED_VALUES_GEOCODE),
		(SAMPLE_ENTRY_GEOMETRY, GNDProperties.GEOMETRY, EXPECTED_VALUES_GEOMETRY),
	],
)
def test_get_values_success(client, entry, property_name, expected_values):
	return_values = client._get_values(entry, property_name)
	assert return_values == expected_values


def test_get_values_raises_on_unsupported_property(client):
	with pytest.raises(ValueError, match="Unsupported GND property"):
		client._get_values(SAMPLE_ENTRY_GENDER, "firstAuthor")


def test_fetch_property_returns_empty(mocker, client):
	mocker.patch.object(client, "_fetch_entries", return_value=[])
	result = client.fetch_property("118635174", "firstAuthor")
	assert result == {"resource": "118635174", "property": "firstAuthor", "entries": []}


def test_fetch_vocab_caches_result(mocker, client):
	client._vocab_cache = {}
	mock_response = mocker.Mock()
	mock_response.text = GENDER_VOCAB
	mocker.patch(
		"canon_curator.enrich.clients.http_client.HttpClient.fetch_page", return_value=mock_response
	)
	client._fetch_vocab("https://d-nb.info/standards/vocab/gnd/gender.rdf")
	assert client._vocab_cache


@pytest.mark.parametrize(
	"concept_uri",
	[
		"https://d-nb.info/standards/vocab/gnd/gender#male",
		"https://d-nb.info/standards/vocab/gnd/gender#female",
		"https://d-nb.info/standards/vocab/gnd/gender#notKnown",
	],
)
def test_fetch_vocab_success(mocker, client, concept_uri):
	mock_response = mocker.Mock()
	mock_response.text = GENDER_VOCAB
	mocker.patch(
		"canon_curator.enrich.clients.http_client.HttpClient.fetch_page", return_value=mock_response
	)
	vocab_graph = client._fetch_vocab("https://d-nb.info/standards/vocab/gnd/gender.rdf")
	assert len(vocab_graph) > 0
	subject = URIRef(concept_uri)
	triples = list(vocab_graph.predicate_objects(subject))
	assert len(triples) > 0


@pytest.mark.parametrize(
	"concept_uri, expected_statements",
	[
		("https://d-nb.info/standards/vocab/gnd/gender#male", EXPECTED_STATEMENTS_MALE),
		("https://d-nb.info/standards/vocab/gnd/gender#female", EXPECTED_STATEMENTS_FEMALE),
		("https://d-nb.info/standards/vocab/gnd/gender#notKnown", EXPECTED_STATEMENTS_NOTKNOWN),
	],
)
def test_fetch_concept_success(mocker, client, concept_uri, expected_statements):
	vocab_graph = Graph()
	vocab_graph.parse(data=GENDER_VOCAB, format="xml")
	mocker.patch.object(client, "_fetch_vocab", return_value=vocab_graph)
	return_statements = client.fetch_concept(concept_uri)
	assert return_statements == expected_statements


def test_context_manager_closes_http_client_on_exit(mocker, client):
	client._http_client = mocker.MagicMock()
	with client:
		pass
	client._http_client.__exit__.assert_called_once()
