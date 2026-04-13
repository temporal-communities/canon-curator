import pytest

from canon_curator.enrich.strategies.registry import StrategyRegistry
from canon_curator.enrich.chains import FirstSuccessChain
from canon_curator.enrich.enrichers import GeodataEnricher


def test_enricher_raises_value_error_on_disallowed_strategy():
	chain = FirstSuccessChain([StrategyRegistry.WIKIDATA_P21, StrategyRegistry.GND_GENDER])
	with pytest.raises(ValueError) as excinfo:
		GeodataEnricher(chain)
	assert "is not a valid strategy for GeodataEnricher" in str(excinfo.value)


def test_enricher_raises_value_error_on_disallowed_strategy(base_work_record):
	chain = irstSuccessChain([StrategyRegistry.WIKIDATA_P21, StrategyRegistry.GND_GENDER])
	geo_enricher = GeodataEnricher(chain)
	geo_enricher._validate()
	geo_enricher.enrich([base_work_record])


def test_enrich_returns_correct_mapping(mocker, base_work_record, expected_geo_record_wikidata):
	mock_chain = mocker.Mock()
	mock_run = mocker.patch.object(chain, "run", return_value=[expected_geo_record_wikidata])
	enricher = GeodataEnricher(mock_chain)
	result = enricher.enrich([base_record])
	assert isinstance(result[base_record.uuid][0], GeoRecord)
