import pytest
import yaml
from pathlib import Path

from canon_curator.wiring import (
	build_geodata_enricher,
	build_authordata_enricher,
	build_readerstats_enricher,
	build_popularity_enricher,
)
from canon_curator.enrich.enrichers import (
	GeodataEnricher,
	AuthordataEnricher,
	PopularityEnricher,
	ReaderstatEnricher,
)
from canon_curator.enrich.chains import FirstSuccessChain, KeepAllChain


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


@pytest.mark.parametrize(
	"builder, expected_class",
	[
		(build_geodata_enricher, GeodataEnricher),
		(build_authordata_enricher, AuthordataEnricher),
		(build_readerstats_enricher, ReaderstatEnricher),
	],
)
def test_build_enrichers_with_first_success_chain(builder, expected_class, good_config):
	enricher = builder(user_config=good_config)

	assert isinstance(enricher, expected_class)
	assert isinstance(enricher.chain, FirstSuccessChain)

@pytest.mark.parametrize(
	"builder, expected_class",
	[
		(build_popularity_enricher, PopularityEnricher),
	],
)
def test_build_enrichers_with_keep_all_chain(builder, expected_class, good_config):
	enricher = builder(user_config=good_config)

	assert isinstance(enricher, expected_class)
	assert isinstance(enricher.chain, KeepAllChain)


def test_build_geodata_enricher_invalid(bad_config):
	with pytest.raises(
		ValueError, match="goodreads_readerstats is not a valid strategy for GeodataEnricher."
	):
		build_geodata_enricher(user_config=bad_config)


def test_build_readerstats_enricher_invalid(bad_config):
	with pytest.raises(ValueError, match="invalid-chain is not a valid strategy chain"):
		build_readerstats_enricher(user_config=bad_config)
