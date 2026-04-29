import pytest

from canon_curator.models import GeoRecord
from canon_curator.enrich.chains import FirstSuccessChain
from canon_curator.enrich.enrichers import GeodataEnricher
from canon_curator.models import GeoRecord


def test_enricher_raises_value_error_on_disallowed_strategy(make_wikidata_p21, make_gnd_gender):
	chain = FirstSuccessChain([make_wikidata_p21, make_gnd_gender])
	strategies = {"wikidata_p21", "gnd_gender"}
	with pytest.raises(ValueError) as excinfo:
		GeodataEnricher(chain, strategies)
	assert "is not a valid strategy for GeodataEnricher" in str(excinfo.value)


def test_enricher_accepts_valid_strategies(make_wikidata_p19):
	chain = FirstSuccessChain([make_wikidata_p19])
	geo_enricher = GeodataEnricher(chain, strategies={"wikidata_p19"})
	assert geo_enricher.chain.strategies == [make_wikidata_p19]


def test_enrich_returns_correct_mapping(mocker, base_record, expected_geo_record_wikidata):
	mock_chain = mocker.Mock()
	mocker.patch.object(mock_chain, "run", return_value=[expected_geo_record_wikidata])
	enricher = GeodataEnricher(mock_chain, strategies={"wikidata_p19"})
	result = enricher.enrich([base_record])
	assert isinstance(result[base_record.uuid][0], GeoRecord)
