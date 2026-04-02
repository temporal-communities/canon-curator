import threading
from canon_curator.enrich.clients import GNDClient, WikidataClient, GoodreadsClient, QRankClient

_tls = threading.local()


def get_gnd_client() -> GNDClient:
	client = getattr(_tls, "gnd_client", None)
	if client is None:
		client = GNDClient(
			name="gnd",
			rate_limit="1/second",
			lobid_base="https://lobid.org/gnd/",
			context_filename="context",
		)
		_tls.gnd_client = client
	return client


def get_wikidata_client() -> WikidataClient:
	client = getattr(_tls, "wikidata_client", None)
	if client is None:
		client = WikidataClient(name="wikidata")
		_tls.wikidata_client = client
	return client


def get_goodreads_client() -> GoodreadsClient:
	client = getattr(_tls, "goodreads_client", None)
	if client is None:
		client = GoodreadsClient(name="goodreads")
		_tls.goodreads_client = client
	return client


def get_qrank_client() -> QRankClient:
	client = getattr(_tls, "qrank_client", None)
	if client is None:
		client = QRankClient(name="qrank")
		_tls.qrank_client = client
	return client
