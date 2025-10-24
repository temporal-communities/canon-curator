from __future__ import annotations
import logging
import json
from functools import cached_property
from types import TracebackType
from typing import Self
from urllib.parse import urljoin, urlparse
import requests
import jsonpath_ng as jp
from bs4 import BeautifulSoup

from canon_curator.enrich.clients.http_client import HttpClient

logger = logging.getLogger(__name__)


_HYDRATION_DATA = "#__NEXT_DATA__"
_PAYLOAD_KEYS = (
            "averageRating",
            "ratingsCount",
            "ratingsCountDist",
            "textReviewsCount",
        )


class GoodreadsClient:
    """
    GoodreadsClient retrieves aggregated reader statistics for a given Goodreads work ID.

    It first fetches the editions page to locate the featured edition, then extracts reader
    statistics from the featured edition’s Next.js hydration data (__NEXT_DATA__). These
    statistics represent aggregated ratings and reviews across all editions of the work.
    """

    def __init__(self,
                 name: str = "goodreads",
                 rate_limit = "1/second",
                 goodreads_base: str = "https://www.goodreads.com/",
                 ) -> None:
        self.name = name
        self.rate_limit = rate_limit
        self.goodreads_base = goodreads_base

    def __enter__(self) -> Self:
        """Enable the use of GoodreadsClient as a context manager."""
        return self

    def __exit__(self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: TracebackType | None) -> None:
        """Ensure HttpClient is closed when exiting the context."""
        if "_http_client" in self.__dict__:
            self._http_client.__exit__(exc_type, exc_value, traceback)

    @cached_property
    def _http_client(self) -> HttpClient:
        """Create and return a new HttpClient instance with rate limiting on first access."""
        return HttpClient(self.rate_limit, self.name)

    def _get_editions(self, goodreads_id: str) -> requests.Response | None:
        edition_url = urljoin(self.goodreads_base, f"work/editions/{goodreads_id}")
        return self._http_client.fetch_page(edition_url)

    def _get_featured(self, goodreads_id: str) -> str | None:
        editions_page = self._get_editions(goodreads_id)
        editions_soup = BeautifulSoup(editions_page.content, "html.parser") if editions_page else None
        featured_elem = editions_soup.select_one("h1 > a") if editions_soup else None
        featured_href = featured_elem.get("href") if featured_elem else None

        if not featured_href:
            logger.warning(f"No featured edition for {goodreads_id}")
            return None

        return urlparse(str(featured_href)).path

    def fetch_readerstats(self, goodreads_id: str) -> dict:
        """Fetch and parse reader statistics from Goodreads hydration data."""
        featured_href = self._get_featured(goodreads_id)

        if not featured_href:
            logger.warning(
                f"Could not retrieve featured edition {featured_href} for {goodreads_id}."
            )
            return dict.fromkeys(_PAYLOAD_KEYS, None)

        featured_url = urljoin(self.goodreads_base, featured_href)
        featured_page = self._http_client.fetch_page(featured_url)
        featured_soup = BeautifulSoup(featured_page.content, "html.parser") if featured_page else None
        hydration_elem = featured_soup.select_one(_HYDRATION_DATA) if featured_soup else None
        hydration_str = hydration_elem.text if hydration_elem else None
        hydration_dict = json.loads(hydration_str) if hydration_str else None
        stats_dict = jp.parse("$.props..stats").find(hydration_dict)[0].value if hydration_dict else None

        if not stats_dict:
            logger.warning(
                f"Could not retrieve readerstats for featured edition {featured_url} of {goodreads_id}."
            )
            return dict.fromkeys(_PAYLOAD_KEYS, None)

        return {k: stats_dict[k] for k in _PAYLOAD_KEYS if k in stats_dict}  # leaky abstraction?
