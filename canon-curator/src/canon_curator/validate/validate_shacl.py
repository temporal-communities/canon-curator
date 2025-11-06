from pyshacl import validate
from pathlib import Path

_SHAPES_FORMAT = "turtle"
_GRAPH_FORMAT = "json-ld"


def _read_shacl_shapes(shapes_path: str | Path) -> str:
    return Path(shapes_path).read_text(encoding="utf-8")


def validate_shacl(graph: str | bytes, shapes_path: str | Path, use_debug_mode: bool = False):
    shapes = _read_shacl_shapes(shapes_path)
    conforms, v_graph, v_text = validate(graph, shacl_graph=shapes,
                                         data_graph_format=_GRAPH_FORMAT,
                                         shacl_graph_format=_SHAPES_FORMAT,
                                         inference='rdfs', debug=use_debug_mode,
                                         serialize_report_graph=True)

    return conforms, v_graph, v_text
