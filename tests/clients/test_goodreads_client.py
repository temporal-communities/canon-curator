import pytest

from canon_curator.enrich.clients.goodreads_client import GoodreadsClient
from tests.testdata.goodreads import (
    EDITIONS_PATH,
    FEATURED_PATH,
    EXPECTED_READERSTATS,
    EXPECTED_READERSTATS_EMPTY,
)


@pytest.fixture
def client():
    return GoodreadsClient()


def test_get_featured_path_success(mocker, client):
    mock_response = mocker.Mock()
    mock_response.content = EDITIONS_PATH.read_bytes()
    mocker.patch.object(client, "_fetch_editions_page", return_value=mock_response)
    featured_href = client._get_featured_path("841320")
    assert featured_href == "/book/show/14942.Mrs_Dalloway"


def test_fetch_readerstats_returns_empty(mocker, client):
    mocker.patch.object(client, "_get_featured_path", return_value=None)
    readerstats = client.fetch_readerstats("841320")
    assert readerstats == EXPECTED_READERSTATS_EMPTY


def test_fetch_readerstats_success(mocker, client):
    mocker.patch.object(client, "_get_featured_path", return_value="/book/show/14942.Mrs_Dalloway")
    mock_response = mocker.Mock()
    mock_response.content = FEATURED_PATH.read_bytes()
    mocker.patch(
        "canon_curator.enrich.clients.http_client.HttpClient.fetch_page", return_value=mock_response
    )
    readerstats = client.fetch_readerstats("841320")
    assert readerstats == EXPECTED_READERSTATS
