from __future__ import annotations
from collections.abc import Callable, Sequence

from canon_curator.models import EnrichmentRecord
from canon_curator.enrich.clients import (
	GNDClient,
	WikidataClient,
	GoodreadsClient,
	QRankClient,
)
from canon_curator.enrich.strategies.authordata import wikidata_p21, gnd_gender
from canon_curator.enrich.strategies.geodata import wikidata_p19, wikidata_p495, gnd_geolabel
from canon_curator.enrich.strategies.popularity import wikidata_sitelinks, wikidata_qrank
from canon_curator.enrich.strategies.readerstats import goodreads_readerstats
from canon_curator.models import (
	BaseWorkRecord,
	GeoRecord,
	AuthorRecord,
	PopularityRecord,
	ReaderstatsRecord,
)

type Strategy[T: EnrichmentRecord] = Callable[[BaseWorkRecord], Sequence[T]]


def make_wikidata_p19(client: WikidataClient) -> Strategy[GeoRecord]:
	def strategy(record: BaseWorkRecord) -> list[GeoRecord]:
		return wikidata_p19(record, client=client)

	return strategy


def make_wikidata_p495(client: WikidataClient) -> Strategy[GeoRecord]:
	def strategy(record: BaseWorkRecord) -> list[GeoRecord]:
		return wikidata_p495(record, client=client)

	return strategy


def make_gnd_geolabel(client: GNDClient) -> Strategy[GeoRecord]:
	def strategy(record: BaseWorkRecord) -> list[GeoRecord]:
		return gnd_geolabel(record, client=client)

	return strategy


def make_gnd_gender(client: GNDClient) -> Strategy[AuthorRecord]:
	def strategy(record: BaseWorkRecord) -> list[AuthorRecord]:
		return gnd_gender(record, client=client)

	return strategy


def make_wikidata_p21(client: WikidataClient) -> Strategy[AuthorRecord]:
	def strategy(record: BaseWorkRecord) -> list[AuthorRecord]:
		return wikidata_p21(record, client=client)

	return strategy


def make_wikidata_sitelinks(client: WikidataClient) -> Strategy[PopularityRecord]:
	def strategy(record: BaseWorkRecord) -> list[PopularityRecord]:
		return wikidata_sitelinks(record, client=client)

	return strategy


def make_wikidata_qrank(client: QRankClient) -> Strategy[PopularityRecord]:
	def strategy(record: BaseWorkRecord) -> list[PopularityRecord]:
		return wikidata_qrank(record, client=client)

	return strategy


def make_goodreads_readerstats(client: GoodreadsClient) -> Strategy[ReaderstatsRecord]:
	def strategy(record: BaseWorkRecord) -> list[ReaderstatsRecord]:
		return goodreads_readerstats(record, client=client)

	return strategy
