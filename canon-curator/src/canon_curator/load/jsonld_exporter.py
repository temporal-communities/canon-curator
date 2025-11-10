import json
from pathlib import Path
from collections.abc import Sequence

from canon_curator.models import EnrichedWorkRecord
from canon_curator.load import BaseExporter
from canon_curator.validate import validate_shacl


class ValidationError(Exception):
	"""Raised when JSON-LD graph fails SHACL validation."""

	pass


class JSONLDExporter(BaseExporter):
	@staticmethod
	def _read_jsonld_context(context_path: str | Path) -> dict:
		context_str = Path(context_path).read_text(encoding="utf-8")
		return json.loads(context_str)

	def _make_graph(self, records: Sequence[EnrichedWorkRecord], context_path: str | Path) -> dict:
		context_dict = self._read_jsonld_context(context_path)

		graph_nodes = []
		for record in records:
			node = {
				"@id": str(record.base_data.id)
				# build the rest of the graph
			}
			graph_nodes.append(node)

		graph = {"@context": context_dict, "@graph": graph_nodes}

		return graph

	def export(
		self,
		records: Sequence[EnrichedWorkRecord],
		context_path: str | Path,
		shapes_path: str | Path,
		out_dir: str | Path,
		filename: str = "graph.jsonld",
	) -> None:
		"""Build JSON-LD, validate against SHACL, and write to out_dir/filename."""

		graph_obj = self._make_graph(records, context_path)
		graph_jsonld = json.dumps(graph_obj, ensure_ascii=False, separators=(",", ":"))

		conforms, result_graph, result_text = validate_shacl(graph_jsonld, shapes_path)

		if not conforms:
			raise ValidationError(f"Could not validate graph. Validation report: \n {result_text}")

		out_path = Path(out_dir) / filename
		out_path.write_text(graph_jsonld, encoding="utf-8")
