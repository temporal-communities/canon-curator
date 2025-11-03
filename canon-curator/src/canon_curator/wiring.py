from canon_curator.enrich.chains import StrategyChain, FirstSuccessChain
from canon_curator.enrich.enrichers import GeodataEnricher, AuthordataEnricher, ReaderstatEnricher, PopularityEnricher


def _build_strategy_chain(user_config: dict, section: str, strategies: dict) -> StrategyChain:
    if user_config[section]["chain"] == "first-success":
        return FirstSuccessChain(strategies)
    else:
        raise ValueError(f"{user_config[section]['chain']} is not a valid strategy chain.")


def build_geodata_enricher(user_config: dict) -> GeodataEnricher:
    strategies = user_config["geodata"]["strategies"]
    chain = _build_strategy_chain(user_config=user_config, section="geodata", strategies=strategies)
    return GeodataEnricher(chain=chain)


def build_authordata_enricher(user_config: dict) -> AuthordataEnricher:
    strategies = user_config["authordata"]["strategies"]
    chain = _build_strategy_chain(user_config=user_config, section="authordata", strategies=strategies)
    return AuthordataEnricher(chain=chain)


def build_readerstats_enricher(user_config: dict) -> ReaderstatEnricher:
    strategies = user_config["readerstats"]["strategies"]
    chain = _build_strategy_chain(user_config=user_config, section="readerstats", strategies=strategies)
    return ReaderstatEnricher(chain=chain)


def build_popularity_enricher(user_config: dict) -> PopularityEnricher:
    strategies = user_config["popularity"]["strategies"]
    chain = _build_strategy_chain(user_config=user_config, section="popularity", strategies=strategies)
    return PopularityEnricher(chain=chain)
