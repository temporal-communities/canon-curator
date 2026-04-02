import pathlib
import pytest

from canon_curator.enrich.clients.qrank_client import QRankClient


EXPECTED_SCORES = {"Q752584": 576436, "Q114761904": 4762, "Q56304713": 298}

SAMPLE_QIDS = ["Q752584", "Q114761904", "Q56304713"]

QRANK_CSV = pathlib.Path(__file__).parent.parent / "testdata" / "qrank.csv"


@pytest.fixture
def client():
	return QRankClient()


def test_prefetch_success(client):
	client.download_url = str(QRANK_CSV)
	client.prefetch(SAMPLE_QIDS)
	assert client.scores == EXPECTED_SCORES


def test_get_qrank_success(client):
	client.download_url = str(QRANK_CSV)
	client.prefetch(SAMPLE_QIDS)
	result = client.get_qrank("Q56304713")
	assert result == EXPECTED_SCORES.get("Q56304713")
