import logging
import pywikibot  # type:ignore
from functools import cached_property

logger = logging.getLogger(__name__)


class WikidataClient:
    """
    WikidataClient interacts with the Wikidata API using pywikibot to fetch properties and labels.
    If more than one claim exists for a given property, it returns all claims except those ranked "deprecated".
    """

    def __init__(self, name: str = "wikidata") -> None:
        self.name = name

    # cached_property for thread safety, lazy instantiation: instantiate on first call
    @cached_property
    def _site(self) -> pywikibot.site.APISite:
        return pywikibot.Site("wikidata", "wikidata")

    @cached_property
    def _repo(self) -> pywikibot.site.DataSite:
        return self._site.data_repository()

    @staticmethod
    def _filter_accepted_claims(claim_collection: pywikibot.ClaimCollection) -> pywikibot.ClaimCollection:
        return [claim for claim in claim_collection if claim.rank != "deprecated"]

    @staticmethod
    def _fetch_sources(claim: pywikibot.Claim) -> list:
        references = claim.getSources()
        sources = []
        for reference in references:
            ref_dict = {}
            for pid in reference:
                # parse this so that the return value does not depend on pywikibot
                ref_dict[pid] = reference[pid][0].toJSON()["datavalue"]
            sources.append(ref_dict)
        return sources # leaky abstraction?

    @staticmethod
    def _fetch_target(claim: pywikibot.Claim, lang: str) -> dict:
        claim_item = claim.getTarget()

        # isinstance(claim_item, pywikibot.ItemPage)
        if hasattr(claim_item, "labels") and hasattr(claim_item, "getID"):
            claim_label = claim_item.labels.get(lang, None)  # can this ever return a list instead of string?
            claim_id = claim_item.getID()
            return {"type": "item",
                    "label": claim_label,
                    "entity_id": claim_id}

        # isinstance(claim_item, pywikibot.Coordinate)
        elif hasattr(claim_item, "lat") and hasattr(claim_item, "lon"):
            lat, lon = float(claim_item.lat), float(claim_item.lon)
            return {"type": "coordinates",
                    "latitude": lat,
                    "longitude": lon}

        # isinstance(claim_item, pywikibot.WbMonolingualText)
        elif hasattr(claim_item, "text"):
            return {"type": "literal",
                    "value": claim_item.text}

        else:  # specify later, maybe define custom UnknownClaimType exception?
            raise Exception

    def _fetch_item_page(self, entity_id: str) -> pywikibot.ItemPage:
        """Fetch a Wikidata ItemPage for a given Wikidata entity ID. Automatically resolves redirects if necessary."""

        # Retrieve the Wikidata item by entity ID
        item = pywikibot.ItemPage(self._repo, entity_id)
        try:
            item.get()
        except pywikibot.exceptions.IsRedirectPageError:  # test case for redirects: wikidata:Q42191769
            logger.error(f"Page [[wikidata:{entity_id}]] is a redirect page. Trying to resolve the redirect...")
            item = item.getRedirectTarget()
            item.get()

        return item

    def _fetch_claims(self, property_id: str, entity_id: str) -> pywikibot.ClaimCollection: # list of pywikibot.page._wikibase.Claim; return Iterable[pywikibot.Claim] instead? ;  oder: fetch_property; returns pywikibot.page._collections.ClaimCollection
        """Fetch claims for the specified property of a Wikidata entity."""

        logger.info(f"Fetching {property_id} for {entity_id}")
        if not entity_id:
            logger.debug("No entity ID")
            return None

        item = self._fetch_item_page(entity_id)

        if property_id not in item.claims:
            return None

        return item.claims[property_id]

    def fetch_property(self, entity_id: str, property_id: str,  lang: str = "en", positive_ranks_only: bool = True) -> dict:
        """
        Fetches claims for specified property of a Wikidata entity together with associated provenance.
        Returns a dictionary containing the entity id, property id, language, and a list of claims with associated provenance (Wikidata rank and sources).
        If the claim is associated with a Wikidata entity, it is classified as type "item", and the label and ID of the entity are returned.
        If the claim is associated with a coordinates object, it is classified as type "coordinates", and the latitude and longitude are returned.
        If the claim is a text literal, it is classified as type "literal", and the value is returned as a string.
        By default, only claims with positive ranks ("normal" or "preferred") are returned.
        """
        claims = self._fetch_claims(property_id, entity_id)

        if not claims:
            return {"entity": entity_id,
                    "property": property_id,
                    "lang": lang,
                    "claims": []}

        if positive_ranks_only:
            claims = self._filter_accepted_claims(claims)

        processed_claims = []
        for claim in claims:

            claim_target = self._fetch_target(claim, lang)
            claim_data = {**claim_target,
                          "sources": self._fetch_sources(claim),
                          "rank": claim.rank}

            processed_claims.append(claim_data)

        return {"entity": entity_id,
                "property": property_id,
                "lang": lang,
                "claims": processed_claims}
