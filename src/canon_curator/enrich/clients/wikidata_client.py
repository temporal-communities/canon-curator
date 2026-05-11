import logging
from functools import cached_property
from types import TracebackType
from typing import Self

from canon_curator.enrich.clients.http_client import HttpClient

logger = logging.getLogger(__name__)


class WikidataClient:
	"""
	WikidataClient interacts with the Wikidata Linked Data Interface to fetch properties and labels.
	See https://www.wikidata.org/wiki/Wikidata:Data_access#Linked_Data_Interface_(URI) for more information.
	If more than one claim exists for a given property, it returns all claims except those ranked "deprecated".
	This behaviour may be adjusted by setting the positive_ranks_only parameter in the fetch_property method
	to false.
	"""

	def __init__(
		self,
		name: str = "wikidata",
		rate_limit="200/minute",
		wikidata_base: str = "https://www.wikidata.org/wiki/Special:EntityData/",
	) -> None:
		self.name = name
		self.rate_limit = rate_limit
		self.wikidata_base = wikidata_base

	def __enter__(self) -> Self:
		"""Enable the use of WikidataClient as a context manager."""
		return self

	def __exit__(
		self,
		exc_type: type[BaseException] | None,
		exc_value: BaseException | None,
		traceback: TracebackType | None,
	) -> None:
		"""Ensure HttpClient is closed when exiting the context."""
		if "_http_client" in self.__dict__:
			self._http_client.__exit__(exc_type, exc_value, traceback)

	@cached_property
	def _http_client(self) -> HttpClient:
		"""Create and return a new HttpClient instance with rate limiting on first access."""
		return HttpClient(self.rate_limit, self.name)

	def _fetch_entity(self, entity_id: str) -> dict | None:
		"""
		Fetch the JSON representation of a Wikidata entity for a given Wikidata entity ID via content negotiation
		and parse properties associated with the entity into a Python dict. Example: https://www.wikidata.org/wiki/Special:EntityData/Q42.json
		"""
		request_url = f"{self.wikidata_base}{entity_id}"
		response = self._http_client.fetch_page(request_url, headers={"Accept": "application/json"})

		if not response:
			return None

		data = response.json()
		return data.get("entities", {}).get(entity_id)

	def _fetch_claims(self, entity: dict, property_id: str) -> list | None:
		"""Fetch claims for the specified property of a Wikidata entity."""
		claims = entity.get("claims", {})
		return claims.get(property_id)

	def _fetch_label(self, entity_id: str, lang: str = "en") -> str | None:
		entity = self._fetch_entity(entity_id)
		if not entity:
			return None
		lang_entry = entity.get("labels", {}).get(lang) or entity.get("labels", {}).get("en")
		return lang_entry.get("value") if lang_entry else None

	def _parse_datavalue(self, datavalue: dict) -> dict:
		"""
		Parse a `datavalue` object from a snak and normalize the snak value (`datavalue.type`) into a
		simplified Python representation. Note that this method operates on the JSON datatype encoding ("string",
		"wikibase-entityid"), not on the property's declared datatype. The encoding "wikibase-entityid" may refer
		to different entity types (item, property, etc.). This method does not distinguish entitiy types and assumes
		items. While this is a valid assumption for the way it is currently used, this implementation detail may be
		worth revisiting if the clients capabilities are extended.
		See https://www.wikidata.org/wiki/Wikidata:Data_formats/JSON_datatype_encodings for more information.
		"""
		value = datavalue.get("value", {})
		dtype = datavalue.get("type")

		if dtype == "wikibase-entityid":
			entity_id = value.get("id") or f"Q{value.get('numeric-id')}"
			return {
				"type": "item",
				"entity_id": entity_id,
				"label": None,
			}

		elif dtype == "globecoordinate":
			return {
				"type": "coordinates",
				"latitude": value.get("latitude"),
				"longitude": value.get("longitude"),
			}

		elif dtype == "string":
			return {
				"type": "literal",
				"value": value,
			}

		elif dtype == "monolingualtext":
			return {
				"type": "literal",
				"value": value.get("text"),
			}

		elif dtype == "time":
			return {
				"type": "time",
				"value": value.get("time"),
			}

		else:
			logger.warning(f"Unknown datatype: {dtype}")
			return {"type": "unknown", "value": value}

	def _parse_references(self, claim: dict) -> list[dict]:
		refs = claim.get("references", [])
		result = []

		for ref in refs:
			snaks = ref.get("snaks", {})
			qualifiers = {}
			source = None

			for pid, values in snaks.items():
				datavalue = values[0].get("datavalue")
				if not datavalue:
					continue

				parsed = self._parse_datavalue(datavalue)
				entity_id = parsed.get("entity_id")
				if entity_id:
					if source is None:
						source = f"https://www.wikidata.org/entity/{entity_id}"
					else:
						qualifiers[pid] = f"https://www.wikidata.org/entity/{entity_id}"
				else:
					qualifiers[pid] = parsed.get("value")

			result.append({"source": source, "qualifiers": qualifiers})

		return result

	def fetch_property(
		self,
		entity_id: str,
		property_id: str,
		positive_ranks_only: bool = True,
		with_claim_label: bool = True,
		label_lang: str = "en",
	) -> dict:
		"""
		Fetch claims for specified property of a Wikidata entity together with associated provenance.
		Returns a dictionary containing the entity id, property id, language, and a list of claims with associated provenance (Wikidata rank and sources).
		If the claim is associated with a Wikidata entity, it is classified as type "item", and the label and ID of the entity are returned.
		If the claim is associated with a coordinates object, it is classified as type "coordinates", and the latitude and longitude are returned.
		If the claim is a text literal, it is classified as type "literal", and the value is returned as a string.
		By default, only claims with positive ranks ("normal" or "preferred") are returned.
		"""
		entity = self._fetch_entity(entity_id)
		if not entity:
			return {"entity": entity_id, "property": property_id, "claims": []}

		claims = self._fetch_claims(entity, property_id)
		if not claims:
			return {"entity": entity_id, "property": property_id, "claims": []}

		processed = []

		for claim in claims:
			rank = claim.get("rank")

			if positive_ranks_only and rank == "deprecated":
				continue

			mainsnak = claim.get("mainsnak", {})
			datavalue = mainsnak.get("datavalue")

			if not datavalue:
				continue

			target = self._parse_datavalue(datavalue)
			if with_claim_label and target.get("type") == "item" and target.get("entity_id"):
				target["label"] = self._fetch_label(target["entity_id"], lang=label_lang)
			sources = self._parse_references(claim)

			processed.append(
				{
					**target,
					"rank": rank,
					"sources": sources,
				}
			)

		return {
			"entity": entity_id,
			"property": property_id,
			"claims": processed,
		}

	def fetch_sitelinks(self, entity_id: str, wikipedia_only: bool = True) -> int:
		"""
		Fetch the number of sitelinks associated with an entity.
		Sitelinks are links from a Wikidata entity to corresponding pages on Wikimedia projects
		(e.g. Wikipedia articles in different languages, Wikiquote pages, etc.). By default, 
		sitelinks are limited to Wikipedia pages.
		"""
		entity = self._fetch_entity(entity_id)
		if not entity:
			return 0

		sitelinks = entity.get("sitelinks", {})

		if wikipedia_only:
			wikipedia_sitelinks = {
				site: data for site, data in sitelinks.items() if site.endswith("wiki")
			}
			return len(wikipedia_sitelinks)

		return len(sitelinks)
