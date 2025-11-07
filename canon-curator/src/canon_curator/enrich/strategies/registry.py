from typing import ClassVar
from collections.abc import Callable, Sequence

from canon_curator.models.records import BaseWorkRecord
from canon_curator.models.enrichment import EnrichmentRecord
from canon_curator.enrich.strategies.authordata.wikidata_author import wikidata_p21
from canon_curator.enrich.strategies.geodata.wikidata_geo import wikidata_p19, wikidata_p495
from canon_curator.enrich.strategies.authordata.gnd_author import gnd_gender
from canon_curator.enrich.strategies.geodata.gnd_geo import gnd_geolabel
from canon_curator.enrich.strategies.popularity.wikidata_sitelinks import wikidata_sitelinks
from canon_curator.enrich.strategies.popularity.wikidata_qrank import wikidata_qrank
from canon_curator.enrich.strategies.readerstats.goodreads import goodreads_readerstats

type Strategy = Callable[[BaseWorkRecord], Sequence[EnrichmentRecord]]


class StrategyRegistry:
    """Registry of enrichment strategy functions"""
    WIKIDATA_P21: ClassVar[Strategy] = wikidata_p21
    GND_GENDER: ClassVar[Strategy] = gnd_gender
    WIKIDATA_P495: ClassVar[Strategy] = wikidata_p495
    WIKIDATA_P19: ClassVar[Strategy] = wikidata_p19
    GND_GEOLABEL: ClassVar[Strategy] = gnd_geolabel
    GOODREADS: ClassVar[Strategy] = goodreads_readerstats
    WIKIDATA_SITELINKS: ClassVar[Strategy] = wikidata_sitelinks
    WIKIDATA_QRANK: ClassVar[Strategy] = wikidata_qrank
