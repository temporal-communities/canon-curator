import pytest

from canon_curator.merge import merge_records


def test_merge_enrichment_records_success(
	expected_sitelinks_record, expected_qrank_record, expected_merged_popularity_record
):
	assert (
		expected_sitelinks_record.merge(expected_qrank_record) == expected_merged_popularity_record
	)


def test_merge_enrichment_records_returns_empty(expected_empty_popularity_record):
	assert (
		expected_empty_popularity_record.merge(expected_empty_popularity_record)
		== expected_empty_popularity_record
	)


def test_merge_enrichment_records_prefers_first_value_on_field_conflict(
	expected_geo_record_wikidata, expected_geo_record_gnd
):
	assert (
		expected_geo_record_wikidata.merge(expected_geo_record_gnd) == expected_geo_record_wikidata
	)


def test_merge_records_function_success(
	base_record,
	geodata_mapping,
	authordata_mapping,
	popularity_mapping,
	readerstats_mapping,
	expected_enriched_work_record,
):
	result = merge_records(
		[base_record], geodata_mapping, authordata_mapping, popularity_mapping, readerstats_mapping
	)
	assert result == [expected_enriched_work_record]


def test_merge_records_function_returns_empty(
	base_record,
	empty_geodata_mapping,
	empty_authordata_mapping,
	empty_popularity_mapping,
	empty_readerstats_mapping,
	expected_empty_enriched_work_record,
):
	result = merge_records(
		[base_record],
		empty_geodata_mapping,
		empty_authordata_mapping,
		empty_popularity_mapping,
		empty_readerstats_mapping,
	)
	assert result == [expected_empty_enriched_work_record]
