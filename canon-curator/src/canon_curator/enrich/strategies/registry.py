from typing import ClassVar
from collections.abc import Callable, Sequence

from canon_curator.models import (
	BaseWorkRecord,
	EnrichmentRecord,
	GeoRecord,
	AuthorRecord,
	PopularityRecord,
	ReaderstatRecord,
)
from canon_curator.enrich.strategies.authordata import wikidata_p21, gnd_gender
from canon_curator.enrich.strategies.geodata import wikidata_p19, wikidata_p495, gnd_geolabel
from canon_curator.enrich.strategies.popularity import wikidata_sitelinks, wikidata_qrank
from canon_curator.enrich.strategies.readerstats import goodreads_readerstats

type Strategy[T: EnrichmentRecord] = Callable[[BaseWorkRecord], Sequence[T]]


class StrategyRegistry:
	"""Registry of enrichment strategy functions"""

	WIKIDATA_P21: ClassVar[Strategy[AuthorRecord]] = wikidata_p21
	GND_GENDER: ClassVar[Strategy[AuthorRecord]] = gnd_gender
	WIKIDATA_P495: ClassVar[Strategy[GeoRecord]] = wikidata_p495
	WIKIDATA_P19: ClassVar[Strategy[GeoRecord]] = wikidata_p19
	GND_GEOLABEL: ClassVar[Strategy[GeoRecord]] = gnd_geolabel
	GOODREADS: ClassVar[Strategy[ReaderstatRecord]] = goodreads_readerstats
	WIKIDATA_SITELINKS: ClassVar[Strategy[PopularityRecord]] = wikidata_sitelinks
	WIKIDATA_QRANK: ClassVar[Strategy[PopularityRecord]] = wikidata_qrank
