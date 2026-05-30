from __future__ import annotations
import logging
import time
import threading

from limits import strategies, storage, parse
import requests
from requests.adapters import HTTPAdapter
from types import TracebackType
from typing import Concatenate, Self
from collections.abc import Callable
from urllib3.util import Retry

logger = logging.getLogger(__name__)

_tls = threading.local()


def rate_limited[Self, **P, T](
	func: Callable[Concatenate[Self, P], T],
) -> Callable[Concatenate[Self, P], T]:
	"""
	Decorator to enforce rate limiting on instance methods.

	This decorator ensures that calls to the decorated method comply with
	the rate limit set in the instance. If the limit is exceeded, it pauses
	execution until the rate limit resets before retrying the request. 
	Note that HttpClient currently sets _limiter to a MovingWindowRateLimiter 
	which implements a rate limiting strategy, in which X requests are allowed 
	in a moving window of Y seconds. Each request is logged, and once the oldest 
	entry in the log expires because it is no longer within the rate limit window,
	a new request is allowed. This means that the rate limiter itself does not 
	space requests; if the window is set to, for example, 200 requests a minute, 
	then in a concurrent scenario, the first 200 requests can be made in fast 
	succession, followed by a long wait time. To ensure requests are spaced out 
	evenly, clients should provide the rate limit in requests per second. This 
	is, however, not enforced. 

	The decorated function must be an instance method of a class that has:
	- A `_limiter` attribute (an instance of `MovingWindowRateLimiter`).
	- A `_limit` attribute (a rate limit object, see https://limits.readthedocs.io/en/stable/api.html#limits.RateLimitItem).
	- A `_key` attribute (a string identifying the rate limit scope).
	"""

	def wrapper(self, *args: P.args, **kwargs: P.kwargs) -> T:
		while not self._limiter.hit(self._limit, self._key):
			reset_time = self._limiter.get_window_stats(self._limit, self._key).reset_time
			wait_time = max(0.0, reset_time - time.time())
			logger.info(
				f"[thread={threading.get_ident()}] "
				f"Rate limit exceeded. Waiting for {wait_time:.2f} seconds before retrying..."
			)
			time.sleep(wait_time)

		return func(self, *args, **kwargs)

	return wrapper


class HttpClient:
	"""
	HttpClient handles HTTP requests with thread-safe rate limiting and automatic retries.
	Thread safety is achieved through a shared rate limit store across all instances / threads
	and a thread-local requests.Session. Note that this client is not suitable for multiprocessing.
	Can be used as a context manager.
	"""

	# share storage across all instances / threads to allow rate limiting across threads
	_store = storage.MemoryStorage()
	_limiter = strategies.MovingWindowRateLimiter(_store)

	def __init__(self, rate_limit: str, client_key: str) -> None:
		# Rate limiter settings
		self._limit = parse(rate_limit)  # returns RateLimitItemPerSecond or RateLimitItemPerHour
		self._key = client_key

	@staticmethod
	def _setup_session() -> requests.Session:
		"""Set up a thread local HTTP session with retry logic and default headers."""
		session = requests.Session()
		retries = Retry(
			backoff_factor=0.1,
			total=5,
			connect=2,  # Retries failed connection attempts (ConnectionError)
			read=2,  # Retries on read timeouts (ReadTimeout)
			status_forcelist=[500, 502, 503, 504],  # Retries on HTTP status codes (HTTPError)
		)
		session.mount("https://", HTTPAdapter(max_retries=retries))
		session.mount("http://", HTTPAdapter(max_retries=retries))
		user_agent = f"canon-curator (https://github.com/temporal-communities/canon-curator) requests/{requests.__version__}"
		session.headers.update({"User-Agent": user_agent, "Accept": "*/*"})
		return session

	def _get_session(self) -> requests.Session:
		session = getattr(_tls, "session", None)
		if session is None:
			logger.debug("Setting up session...")
			session = self._setup_session()
			_tls.session = session
		return session

	@rate_limited
	def fetch_page(
		self, url: str, timeout: int = 10, headers: dict[str, str] | None = None
	) -> requests.Response | None:
		"""Make HTTP request for a url."""

		try:
			session = self._get_session()
			request_headers = dict(session.headers)
			if headers:
				request_headers.update(headers)
			response = session.get(url, timeout=timeout, headers=request_headers)
			response.raise_for_status()  # Handle HTTP 4xx and 5xx errors after unsuccessful retries
			logger.info(f"Fetched {url} with status code: {response.status_code}")
			return response
		except requests.exceptions.RetryError:
			logger.warning(f"Max retries exceeded for {url}.")
		except requests.exceptions.RequestException as e:
			logger.warning(f"Request for {url} failed with exception: {e}")
		return None

	def close(self) -> None:
		"""Close the HTTP session of the thread."""
		session = getattr(_tls, "session", None)
		if session is not None:
			session.close()
			delattr(_tls, "session")

	def __enter__(self) -> Self:
		"""Enable the HTTP client to be used as a context manager."""
		return self

	def __exit__(
		self,
		exc_type: type[BaseException] | None,
		exc_value: BaseException | None,
		traceback: TracebackType | None,
	) -> None:
		"""Close the HTTP session when exiting the context manager."""
		self.close()
