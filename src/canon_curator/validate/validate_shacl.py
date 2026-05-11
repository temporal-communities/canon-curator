from pyshacl import validate
from pathlib import Path


def validate_shacl(
	graph_path: Path,
	shapes_path: Path,
	ontology_path: Path,
	graph_format: str = "turtle",
	use_debug_mode: bool = False,
) -> tuple[bool, bytes, str]:
	conforms, results_graph, results_text = validate(
		str(graph_path),
		shacl_graph=str(shapes_path),
		ont_graph=str(ontology_path),
		data_graph_format=graph_format,
		shacl_graph_format="turtle",
		inference="rdfs",
		debug=use_debug_mode,
		serialize_report_graph=True,
	)

	return conforms, results_graph, results_text  # type: ignore[return-value]
