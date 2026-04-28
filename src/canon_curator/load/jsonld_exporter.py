from __future__ import annotations

import logging
import json
from collections.abc import Sequence

import pyoxigraph as ox

from canon_curator.load.base_exporter import BaseExporter
from canon_curator.load.reification import convert_to_reified_store
from canon_curator.load.rdf_graph_builder import RDFGraphBuilder
from canon_curator.models.records import EnrichedWorkRecord

logger = logging.getLogger(__name__)


class JSONLDExporter(BaseExporter):
	"""Export EnrichedWorkRecord instances as JSON-LD.

	- provenance_format="star": represent provenance in RDF 1.2 syntax and attempt
	  serializing with pyoxigraph's JSON-LD serializer. Raises OSError until Oxigraph
	  adds RDF 1.2 support in JSON-LD.
	- provenance_format="reified" (default): represent provenance with classic
	  rdf:Statement reification syntax. This option requires converting the pyoxigraph
	  store prior to serialization. Output is JSON-LD 1.0 compatible.
	"""

	def __init__(
		self,
		filename: str,
		canon_list_iri: str = "",
		canon_list_name: str | None = None,
		canon_list_metadata_iri: str | None = None,
		software_agent_iri: str | None = "https://github.com/temporal-communities/canon-curator/",
		out_dir: str = ".",
		provenance_format: str = "reified",
	) -> None:
		super().__init__(filename=filename, out_dir=out_dir)
		self.filename = filename if str(filename).endswith(".jsonld") else f"{filename}.jsonld"
		self.provenance_format = provenance_format
		self._builder = RDFGraphBuilder(
			canon_list_iri=canon_list_iri,
			canon_list_name=canon_list_name,
			canon_list_metadata_iri=canon_list_metadata_iri,
			software_agent_iri=software_agent_iri,
		)

	def _serialize_star(self, store: ox.Store) -> str:
		store_dump = store.dump(
			format=ox.RdfFormat.JSON_LD,
			from_graph=ox.DefaultGraph(),
		)

		if store_dump is None:
			raise RuntimeError("store.dump() returned None unexpectedly")

		return store_dump.decode()

	def _serialize_reified(self, store: ox.Store) -> str:
		reified_store = convert_to_reified_store(store)
		store_dump = reified_store.dump(
			format=ox.RdfFormat.JSON_LD,
			from_graph=ox.DefaultGraph(),
		)

		if store_dump is None:
			raise RuntimeError("store.dump() returned None unexpectedly")

		return store_dump.decode()

	def export(self, records: Sequence[EnrichedWorkRecord]) -> None:
		if self.file is None or self.file.closed:
			raise RuntimeError("Export failed. Use as context manager or call open() first.")
		store = self._builder.build(records)
		serialized = (
			self._serialize_star(store)
			if self.provenance_format == "star"
			else self._serialize_reified(store)
		)
		self.file.write(json.dumps(json.loads(serialized), ensure_ascii=False, indent=2))
		logger.info("Exported JSON-LD (%s) to %s", self.provenance_format, self.output_path)
