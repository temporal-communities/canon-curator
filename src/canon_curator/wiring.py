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


def _build_strategy_chain(
	registry: dict[str, Strategy], strategies: list[str], chain_type: str
) -> StrategyChain:
	if chain_type not in CHAIN_CONSTRUCTORS:
		raise ValueError(
			f"{chain_type!r} is not a valid chain type. Allowed: {', '.join(CHAIN_CONSTRUCTORS)}"
		)

	chain_constructor = CHAIN_CONSTRUCTORS[chain_type]
	resolved_strategies = [registry[strategy] for strategy in strategies]

	return chain_constructor(resolved_strategies)


def build_geodata_enricher(
	registry: dict,
	user_config: dict,
) -> GeodataEnricher:
	cfg = user_config["geodata"]

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
) -> AuthordataEnricher:
	cfg = user_config["authordata"]

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
) -> PopularityEnricher:
	cfg = user_config["popularity"]

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
) -> ReaderstatEnricher:
	cfg = user_config["readerstats"]

	return ReaderstatEnricher(
		chain=_build_strategy_chain(
			registry,
			cfg["strategies"],
			cfg["chain"],
		),
		strategies=cfg["strategies"],
	)
