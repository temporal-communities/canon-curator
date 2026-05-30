from canon_curator.enrich.clients import GNDClient, WikidataClient, QRankClient, GoodreadsClient
from canon_curator.enrich.chains import StrategyChain, FirstSuccessChain, KeepAllChain
from canon_curator.enrich.enrichers import (
	GeodataEnricher,
	AuthordataEnricher,
	ReaderstatEnricher,
	PopularityEnricher,
)
from canon_curator.enrich.strategies.factory import (
	make_wikidata_p19,
	make_wikidata_p495,
	make_gnd_geolabel,
	make_gnd_gender,
	make_wikidata_p21,
	make_wikidata_sitelinks,
	make_wikidata_qrank,
	make_goodreads_readerstats,
	Strategy,
)


CHAIN_CONSTRUCTORS: dict[str, type[StrategyChain]] = {
	"first-success": FirstSuccessChain,
	"keep-all": KeepAllChain,
}


def make_strategy_registry(
	gnd_client: GNDClient,
	wikidata_client: WikidataClient,
	qrank_client: QRankClient,
	goodreads_client: GoodreadsClient,
) -> dict[str, Strategy]:
	return {
		"wikidata_p19": make_wikidata_p19(wikidata_client),
		"wikidata_p495": make_wikidata_p495(wikidata_client),
		"gnd_geolabel": make_gnd_geolabel(gnd_client),
		"gnd_gender": make_gnd_gender(gnd_client),
		"wikidata_p21": make_wikidata_p21(wikidata_client),
		"wikidata_sitelinks": make_wikidata_sitelinks(wikidata_client),
		"wikidata_qrank": make_wikidata_qrank(qrank_client),
		"goodreads": make_goodreads_readerstats(goodreads_client),
	}

def _get_enricher_config(user_config: dict, key: str) -> dict | None:
    cfg = user_config.get(key)
    if cfg is None:
        return None
    if not cfg.get("strategies"):
        raise ValueError(f"'{key}' config is missing required field: 'strategies'")
    if not cfg.get("chain"):
        raise ValueError(f"'{key}' config is missing required field: 'chain'")
    return cfg


def _build_strategy_chain(
	registry: dict[str, Strategy], strategies: list[str], chain_type: str
) -> StrategyChain:
	if chain_type not in CHAIN_CONSTRUCTORS:
		raise ValueError(
			f"Unknown chain type: {chain_type!r}. Allowed: {', '.join(CHAIN_CONSTRUCTORS)}"
		)

	chain_constructor = CHAIN_CONSTRUCTORS[chain_type]
	resolved_strategies = []
	for strategy in strategies:
		if strategy not in registry:
			raise ValueError(f"Unknown strategy type: {strategy!r}. Allowed: {', '.join(registry)}")
		resolved_strategies.append(registry[strategy])

	return chain_constructor(resolved_strategies)


def build_geodata_enricher(
	registry: dict,
	user_config: dict,
) -> GeodataEnricher | None:
	cfg = _get_enricher_config(user_config, "geodata")
	if cfg is None: 
		return None

	return GeodataEnricher(
		chain=_build_strategy_chain(
			registry,
			cfg["strategies"],
			cfg["chain"],
		),
		strategies=cfg["strategies"],
	)


def build_authordata_enricher(
	registry: dict,
	user_config: dict,
) -> AuthordataEnricher | None:
	cfg = _get_enricher_config(user_config, "authordata")
	if cfg is None: 
		return None
	return AuthordataEnricher(
		chain=_build_strategy_chain(
			registry,
			cfg["strategies"],
			cfg["chain"],
		),
		strategies=cfg["strategies"],
	)


def build_popularity_enricher(
	registry: dict,
	user_config: dict,
	qrank_client: QRankClient | None = None,
) -> PopularityEnricher | None:
	cfg = _get_enricher_config(user_config, "popularity")
	if cfg is None: 
		return None

	return PopularityEnricher(
		chain=_build_strategy_chain(
			registry,
			cfg["strategies"],
			cfg["chain"],
		),
		strategies=cfg["strategies"],
		qrank_client=qrank_client if "wikidata_qrank" in cfg["strategies"] else None,
	)


def build_readerstats_enricher(
	registry: dict,
	user_config: dict,
) -> ReaderstatEnricher | None:
	cfg = _get_enricher_config(user_config, "readerstats")
	if cfg is None: 
		return None

	return ReaderstatEnricher(
		chain=_build_strategy_chain(
			registry,
			cfg["strategies"],
			cfg["chain"],
		),
		strategies=cfg["strategies"],
	)
