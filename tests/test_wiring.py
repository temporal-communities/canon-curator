import pytest
import yaml
from pathlib import Path

from canon_curator.wiring import (
	build_geodata_enricher,
	build_authordata_enricher,
	build_readerstats_enricher,
	build_popularity_enricher,
	make_strategy_registry,
)
from canon_curator.enrich.enrichers import (
	GeodataEnricher,
	AuthordataEnricher,
	PopularityEnricher,
	ReaderstatEnricher,
)
from canon_curator.enrich.chains import FirstSuccessChain, KeepAllChain
from canon_curator.enrich.clients import (
	GNDClient, 
	WikidataClient, 
	QRankClient, 
	GoodreadsClient,
)


@pytest.fixture
def gnd_client(mocker):
	return mocker.Mock()

@pytest.fixture
def wikidata_client(mocker):
	return mocker.Mock()

@pytest.fixture
def qrank_client(mocker):
	return mocker.Mock()

@pytest.fixture
def goodreads_client(mocker):
	return mocker.Mock()

@pytest.fixture
def good_config():
	"""Config with valid strategies and strategy chains for all enrichers."""
	config_path = Path(__file__).parent / "testdata" / "good_config.yml"
	with config_path.open("r", encoding="utf-8") as f:
		return yaml.safe_load(f)


@pytest.fixture
def bad_config():
	"""Config with invalid strategies and strategy chains."""
	config_path = Path(__file__).parent / "testdata" / "bad_config.yml"
	with config_path.open("r", encoding="utf-8") as f:
		return yaml.safe_load(f)


@pytest.fixture
def registry(gnd_client, wikidata_client, qrank_client, goodreads_client):
	return make_strategy_registry(gnd_client, wikidata_client, qrank_client, goodreads_client)


@pytest.mark.parametrize(
	"builder, expected_class",
	[
		(build_geodata_enricher, GeodataEnricher),
		(build_authordata_enricher, AuthordataEnricher),
		(build_readerstats_enricher, ReaderstatEnricher),
	],
)
def test_build_enrichers_with_first_success_chain(
	builder,
	expected_class,
	good_config,
	registry
):
	if builder is build_geodata_enricher:
		enricher = builder(registry, good_config)

	elif builder is build_authordata_enricher:
		enricher = builder(registry, good_config)

	elif builder is build_readerstats_enricher:
		enricher = builder(registry, good_config)

	assert isinstance(enricher, expected_class)
	assert isinstance(enricher.chain, FirstSuccessChain)


@pytest.mark.parametrize(
	"builder, expected_class",
	[
		(build_popularity_enricher, PopularityEnricher),
	],
)
def test_build_enrichers_with_keep_all_chain(
	builder,
	expected_class,
	good_config,
	registry
):
	enricher = builder(registry, good_config)
	assert isinstance(enricher, expected_class)
	assert isinstance(enricher.chain, KeepAllChain)


def test_build_geodata_enricher_invalid(registry, bad_config):
	with pytest.raises(ValueError):
		build_geodata_enricher(registry, bad_config)


def test_build_readerstats_enricher_invalid(registry, bad_config):
	with pytest.raises(ValueError):
		build_readerstats_enricher(registry, bad_config)
