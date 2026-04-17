import pytest
from pathlib import Path
from io import StringIO

from canon_curator.load import JSONLinesExporter


EXPECTED_JSONL_PATH = Path(__file__).parent / "testdata" / "expected_jsonlines_export.jsonl"
EXPECTED_JSONL = EXPECTED_JSONL_PATH.read_text(encoding="utf-8")


def test_jsonlines_export_success(
	expected_enriched_work_record, expected_empty_enriched_work_record
):
	buffer = StringIO()
	exporter = JSONLinesExporter("test.jsonl")
	exporter.file = buffer
	exporter.export([expected_enriched_work_record, expected_empty_enriched_work_record])
	assert buffer.getvalue() == EXPECTED_JSONL
