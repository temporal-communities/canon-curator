from collections.abc import Callable, Sequence

from canon_curator.enrich.chains import StrategyChain, FirstSuccessChain
from canon_curator.enrich.enrichers import GeodataEnricher, AuthordataEnricher, ReaderstatEnricher, PopularityEnricher
from canon_curator.models.records import BaseWorkRecord
from canon_curator.models.enrichment import EnrichmentRecord
from canon_curator.enrich.strategies.registry import StrategyRegistry

type Strategy = Callable[[BaseWorkRecord], Sequence[EnrichmentRecord]]

STRATEGY_MAP: dict[str, Strategy] = {
    "gnd_geolabel": StrategyRegistry.GND_GEOLABEL,
    "wikidata_p19": StrategyRegistry.WIKIDATA_P19,
    "wikidata_p495": StrategyRegistry.WIKIDATA_P495,
    "gnd_gender": StrategyRegistry.GND_GENDER,
    "wikidata_p21": StrategyRegistry.WIKIDATA_P21,
    "wikidata_sitelinks": StrategyRegistry.WIKIDATA_SITELINKS,
    "wikidata_qrank": StrategyRegistry.WIKIDATA_QRANK,
    "goodreads": StrategyRegistry.GOODREADS,
}

def _resolve_strategies(strategy_names: list[str]) -> list[Strategy]:
    strategies = []
    for strategy in strategy_names:
        if strategy not in STRATEGY_MAP:
            raise ValueError(f"{strategy} is not a valid strategy")
        strategies.append(STRATEGY_MAP[strategy])
    return strategies


def _build_strategy_chain(user_config: dict, section: str) -> StrategyChain:
    strategy_names = user_config[section]["strategies"]
    strategies = _resolve_strategies(strategy_names)
    chain_type = user_config[section]["chain"]
    if chain_type == "first-success":
        return FirstSuccessChain(strategies)
    else:
        raise ValueError(f"{chain_type} is not a valid strategy chain")


def build_geodata_enricher(user_config: dict) -> GeodataEnricher:
    chain = _build_strategy_chain(user_config=user_config, section="geodata")
    return GeodataEnricher(chain=chain)


def build_authordata_enricher(user_config: dict) -> AuthordataEnricher:
    chain = _build_strategy_chain(user_config=user_config, section="authordata")
    return AuthordataEnricher(chain=chain)


def build_readerstats_enricher(user_config: dict) -> ReaderstatEnricher:
    chain = _build_strategy_chain(user_config=user_config, section="readerstats")
    return ReaderstatEnricher(chain=chain)


def build_popularity_enricher(user_config: dict) -> PopularityEnricher:
    chain = _build_strategy_chain(user_config=user_config, section="popularity")
    return PopularityEnricher(chain=chain)
