from __future__ import annotations
import logging
from types import TracebackType
from typing import Self
from rdflib import Graph
from functools import cached_property
from shapely import wkt
from shapely.geometry import Point
from urllib.parse import urljoin

from canon_curator.enrich.clients.http_client import HttpClient

logger = logging.getLogger(__name__)


class GNDProperties:
	"""Constants for supported GND property names used in lobid-gnd API responses."""

	GEOMETRY = "hasGeometry"
	GENDER = "gender"
	GEOCODE = "geographicAreaCode"


class GNDClient:
	"""
	GNDClient interacts with the lobid-gnd API to fetch geographic area codes, gender or latitude/longitude for an
	entry for a resource ID in the Gemeinsame Normdatei (GND). If multiple entries for a property exists, returns all entries.
	Can be used as a context manager.
	"""

	def __init__(
		self,
		name: str = "gnd",
		rate_limit="1/second",
		lobid_base: str = "https://lobid.org/gnd/",
		context_filename: str = "context",
	) -> None:
		self.name = name
		self.rate_limit = rate_limit
		self.lobid_base = lobid_base
		self.context_filename = context_filename

	def __enter__(self) -> Self:
		"""Enable the use of GNDClient as a context manager."""
		return self

	def __exit__(
		self,
		exc_type: type[BaseException] | None,
		exc_value: BaseException | None,
		traceback: TracebackType | None,
	) -> None:
		"""Ensure HttpClient is closed when exiting the context."""
		if (
			"_http_client" in self.__dict__
		):  # self._http_client would inadvertently instantiate http client if it does not exist
			self._http_client.__exit__(exc_type, exc_value, traceback)

	@cached_property
	def _http_client(self) -> HttpClient:
		"""Create and return a new HttpClient instance with rate limiting on first access."""
		return HttpClient(self.rate_limit, self.name)

	@staticmethod
	def _parse_coordinates(wkt_coords: str) -> tuple[float, float]:
		geom = wkt.loads(wkt_coords)
		if not isinstance(geom, Point):
			raise ValueError(f"Expected POINT, got {geom.geom_type}")
		return geom.x, geom.y

	def _get_values(self, entry: dict, property_name: str) -> dict:
		if property_name in {GNDProperties.GENDER, GNDProperties.GEOCODE}:
			return {
				"type": "resource",
				"uri": entry.get("id"),
				"gnd_id": entry.get("gndIdentifier"),
				"label": entry.get("label"),
			}
		elif property_name == GNDProperties.GEOMETRY:
			geom = entry.get("asWKT", [])
			coords = self._parse_coordinates(geom[0])
			lon, lat = float(coords[0]), float(coords[1])
			return {"type": "coordinates", "latitude": lat, "longitude": lon}
		else:
			raise ValueError(f"Unsupported GND property: {property_name} for entry {entry['id']}")

	def _fetch_entries(self, resource_id: str, property_name: str) -> list:
		resource = self._fetch_resource(resource_id)
		if resource:
			return resource.get(property_name, [])
		else:
			return []

	def _fetch_resource(self, resource_id: str) -> dict | None:
		"""
		Fetches a resource by ID from the lobid-gnd API in JSON.
		Requests to the JSON-API return JSON-LD: https://lobid.org/gnd/api#jsonld;
		the context file can be found at: /gnd/context.jsonld
		"""
		url = urljoin(self.lobid_base, f"{resource_id}.json")
		logger.info(f"Fetching resource from {url}")
		response = self._http_client.fetch_page(url)
		if not response:
			logger.warning(f"Could not fetch resource {resource_id} from URL {url}.")
			return None
		return response.json()

	def fetch_vocab(self, vocab_url: str) -> Graph | None:
		"""Fetch RDF vocabulary from specified URL."""
		g = Graph()
		logger.info(f"Fetching RDF vocabulary from {vocab_url}")
		response = self._http_client.fetch_page(vocab_url)
		if not response:
			logger.warning(f"Could not fetch vocabulary from URL {vocab_url}.")
			return None
		return g.parse(response.text, format="xml")

	def fetch_property(self, resource_id: str, property_name: str) -> dict:
		"""
		Fetches properties (values) for a specific entry for a resource ID in the Gemeinsame Normdatei (GND).
		A list of GND properties can be found here: https://lobid.org/gnd/context.jsonld
		"""
		entries = self._fetch_entries(resource_id, property_name)

		if not entries:
			return {"resource": resource_id, "property": property_name, "entries": []}

		processed_entries = [self._get_values(entry, property_name) for entry in entries]

		return {"resource": resource_id, "property": property_name, "entries": processed_entries}
