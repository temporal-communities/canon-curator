from __future__ import annotations

import logging
from io import BytesIO
from collections.abc import Sequence
from pathlib import Path

import pyoxigraph as ox

from canon_curator.load.base_exporter import BaseExporter
from canon_curator.load.namespaces import PREFIXES
from canon_curator.load.reification import convert_to_reified_store
from canon_curator.load.rdf_graph_builder import RDFGraphBuilder
from canon_curator.models.records import EnrichedWorkRecord

logger = logging.getLogger(__name__)


class TurtleExporter(BaseExporter):
	"""Export EnrichedWorkRecord instances as Turtle.

	- provenance_format="star" (default): represent provenance in RDF 1.2 syntax and serialize with
	  pyoxigraph's Turtle serializer.
	- provenance_format="reified": represent provenance with classic rdf:Statement reification syntax.
	  This option requires converting the pyoxigraph store prior to serialization.
	"""

	def __init__(
		self,
		filename: str,
		canon_list_iri: str,
		canon_list_name: str | None = None,
		canon_list_metadata_iri: str | None = None,
		software_agent_iri: str | None = "https://github.com/temporal-communities/canon-curator/",
		out_dir: Path | str = ".",
		provenance_format: str = "star",
	) -> None:
		super().__init__(filename=filename, out_dir=out_dir)
		self.filename = filename if str(filename).endswith(".ttl") else f"{filename}.ttl"
		self.provenance_format = provenance_format
		self._builder = RDFGraphBuilder(
			canon_list_iri=canon_list_iri,
			canon_list_name=canon_list_name,
			canon_list_metadata_iri=canon_list_metadata_iri,
			software_agent_iri=software_agent_iri,
		)

	def _serialize_star(self, store: ox.Store) -> str:
		output = BytesIO()
		ox.serialize(
			sorted(store.quads_for_pattern(None, None, None, ox.DefaultGraph()), key=str),
			output,
			format=ox.RdfFormat.TURTLE,
			prefixes=PREFIXES,
		)

		if output is None:
			raise RuntimeError("ox.serialize() returned None unexpectedly")

		return output.getvalue().decode()

	def _serialize_reified(self, store: ox.Store) -> str:
		reified_store = convert_to_reified_store(store)
		output = BytesIO()
		ox.serialize(
			sorted(reified_store.quads_for_pattern(None, None, None, ox.DefaultGraph()), key=str),
			output,
			format=ox.RdfFormat.TURTLE,
			prefixes=PREFIXES,
		)

		if output is None:
			raise RuntimeError("ox.serialize() returned None unexpectedly")

		return output.getvalue().decode()

	def export(self, records: Sequence[EnrichedWorkRecord]) -> None:
		if self.file is None or self.file.closed:
			raise RuntimeError("Export failed. Use as context manager or call open() first.")
		store = self._builder.build(records)
		serialized = (
			self._serialize_reified(store)
			if self.provenance_format == "reified"
			else self._serialize_star(store)
		)
		self.file.write(serialized)
		logger.info("Exported RDF (%s) to %s", self.provenance_format, self.output_path)
