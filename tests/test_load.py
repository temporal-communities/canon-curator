import pytest
import json
from pathlib import Path

import pyoxigraph as ox
from io import StringIO
from rdflib import Graph

from canon_curator.load import JSONLinesExporter, JSONLDExporter, TurtleExporter
from canon_curator.load.namespaces import RDF, CANON

EXPECTED_JSONL_PATH = Path(__file__).parent / "testdata" / "expected_jsonlines_export.jsonl"
EXPECTED_JSONL = EXPECTED_JSONL_PATH.read_text(encoding="utf-8")
EXPECTED_TURTLE_STAR_PATH = Path(__file__).parent / "testdata" / "expected_turtle_star_export.ttl"
EXPECTED_TURTLE_REIFIED_PATH = Path(__file__).parent / "testdata" / "expected_turtle_reified_export.ttl"
EXPECTED_JSONLD_STAR_PATH = Path(__file__).parent / "testdata" / "expected_jsonld_star_export.jsonld"
EXPECTED_JSONLD_REIFIED_PATH = Path(__file__).parent / "testdata" / "expected_jsonld_reified_export.jsonld"

EXPECTED_JSONLD_STAR = json.loads(EXPECTED_JSONLD_STAR_PATH.read_text(encoding="utf-8"))
EXPECTED_JSONLD_REIFIED = json.loads(EXPECTED_JSONLD_REIFIED_PATH.read_text(encoding="utf-8"))

CANON_LIST_IRI = "https://example.org/test-list"
SOFTWARE_AGENT_IRI = "https://github.com/temporal-communities/canon-curator/"
METADATA_IRI = "https://example.org/test-list-metadata"



def _load_turtle(path: Path) -> ox.Store:
    store = ox.Store()
    store.load(input=path.read_text(encoding="utf-8"), format=ox.RdfFormat.TURTLE, to_graph=ox.DefaultGraph())
    return store


def _annotation_triples(store: ox.Store) -> set[tuple[str, str, str, str]]:
    """Extract triple annotations as (subject, predicate, object, enrichment_iri) tuples.

    Detects RDF 1.2 reifying triples via rdf:reifies and all other triples with the same 
    reifier (blank node id) as subject and canon:hasEnrichment as predicate. Used to 
    test Turtle RDF 1.2 export where rdflib isomorphic() cannot be used. 
    """
    rdf_reifies    = ox.NamedNode(RDF + "reifies")
    has_enrichment = ox.NamedNode(CANON + "hasEnrichment")

    triple_terms: dict[str, ox.Triple] = {
        quad.subject.value: quad.object
        for quad in store
        if quad.predicate == rdf_reifies and isinstance(quad.object, ox.Triple)
    }
    enrichment_iris: dict[str, str] = {
        quad.subject.value: quad.object.value
        for quad in store
        if (
            quad.predicate == has_enrichment
            and isinstance(quad.subject, ox.BlankNode)
            and quad.subject.value in reifies
        )
    }
    return {
        (
            triple_terms[bnode_id].subject.value,
            triple_terms[bid].predicate.value,
            str(triple_terms[bid].object),
            enrichment_iris[bid],
        )
        for bid in triple_terms
        if bid in enrichment_iris
    }

def test_jsonlines_export_success(
    expected_enriched_work_record, expected_empty_enriched_work_record
):
    buffer = StringIO()
    exporter = JSONLinesExporter("test.jsonl")
    exporter.file = buffer
    exporter.export([expected_enriched_work_record, expected_empty_enriched_work_record])
    assert buffer.getvalue() == EXPECTED_JSONL


def test_jsonld_star_export_raises_oserror(
    expected_enriched_work_record,
    expected_empty_enriched_work_record,
    tmp_path,
):

    with pytest.raises(OSError) as excinfo:
        
        exporter = JSONLDExporter(
            "test.jsonld",
            out_dir=tmp_path,
            canon_list_iri=CANON_LIST_IRI,
            canon_list_name="My Test Canon List",
            canon_list_metadata_iri=METADATA_IRI,
            software_agent_iri=SOFTWARE_AGENT_IRI,
            provenance_format="star"
        )

        exporter.open()
        exporter.export([expected_enriched_work_record, expected_empty_enriched_work_record])
        exporter.close()
    assert "JSON-LD does not support RDF 1.2 yet" in str(excinfo.value)


def test_jsonld_reified_export_success(
    expected_enriched_work_record,
    expected_empty_enriched_work_record,
    tmp_path,
):
    exporter = JSONLDExporter(
        "test.jsonld",
        out_dir=tmp_path,
        canon_list_iri=CANON_LIST_IRI,
        canon_list_name="My Test Canon List",
        canon_list_metadata_iri=METADATA_IRI,
        software_agent_iri=SOFTWARE_AGENT_IRI,
        provenance_format="reified",
    )

    exporter.open()
    exporter.export([expected_enriched_work_record, expected_empty_enriched_work_record])
    exporter.close()

    produced = Graph().parse(
        data=(tmp_path / "test.jsonld").read_text(encoding="utf-8"),
        format="json-ld",
    )
    expected = Graph().parse(
        data=json.dumps(EXPECTED_JSONLD_REIFIED["@graph"]),
        format="json-ld",
    )

    assert produced.isomorphic(expected)


def test_turtle_star_export_success(expected_enriched_work_record, tmp_path):
    exporter = TurtleExporter(
        "test.ttl",
        out_dir=tmp_path,
        canon_list_iri=CANON_LIST_IRI,
        canon_list_name="My Test Canon List",
        canon_list_metadata_iri=METADATA_IRI,
        software_agent_iri=SOFTWARE_AGENT_IRI,
        provenance_format="star",
    )

    exporter.open()
    exporter.export([expected_enriched_work_record])
    exporter.close()

    produced = _load_turtle(tmp_path / "test.ttl")
    expected = _load_turtle(EXPECTED_TURTLE_STAR_PATH)


    assert _annotation_triples(produced) == _annotation_triples(expected)


def test_turtle_reified_export_success(expected_enriched_work_record, tmp_path):
    exporter = TurtleExporter(
        "test.ttl",
        out_dir=tmp_path,
        canon_list_iri=CANON_LIST_IRI,
        canon_list_name="My Test Canon List",
        canon_list_metadata_iri=METADATA_IRI,
        software_agent_iri=SOFTWARE_AGENT_IRI,
        provenance_format="reified",
    )

    exporter.open()
    exporter.export([expected_enriched_work_record])
    exporter.close()

    produced = Graph().parse(tmp_path / "test.ttl", format="turtle")
    expected = Graph().parse(EXPECTED_TURTLE_REIFIED_PATH, format="turtle")

    assert produced.isomorphic(expected)
