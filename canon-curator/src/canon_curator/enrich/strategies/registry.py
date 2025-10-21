from canon_curator.enrich.strategies.authordata.wikidata_author import wikidata_p21
from canon_curator.enrich.strategies.geodata.wikidata_geo import wikidata_p19, wikidata_p495
from canon_curator.enrich.strategies.authordata.gnd_author import gnd_gender
from canon_curator.enrich.strategies.geodata.gnd_geo import gnd_geolabel
from canon_curator.enrich.strategies.popularity.wikidata_sitelinks import wikidata_sitelinks
from canon_curator.enrich.strategies.popularity.wikidata_qrank import wikidata_qrank
from canon_curator.enrich.strategies.readerstats.goodreads import goodreads


class StrategyRegistry:
    """Registry of enrichment strategy functions"""
    WIKIDATA_P21 = wikidata_p21
    GND_GENDER = gnd_gender
    WIKIDATA_P495 = wikidata_p495
    WIKIDATA_P19 = wikidata_p19
    GND_GEOLABEL = gnd_geolabel
    GOODREADS = goodreads
    WIKIDATA_SITELINKS = wikidata_sitelinks
    WIKIDATA_QRANK = wikidata_qrank
