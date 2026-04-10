import pytest

from canon_curator.enrich.chains import MergeFieldsChain, FirstSuccessChain


def test_run_first_success_chain_success(
	mocker,
	base_record,
	expected_empty_author_record,
	expected_author_record_gnd,
	expected_author_record_wikidata,
):
	s1 = mocker.Mock(return_value=[expected_empty_author_record])
	s2 = mocker.Mock(return_value=[expected_author_record_gnd])
	s3 = mocker.Mock(return_value=[expected_author_record_wikidata])
	chain = FirstSuccessChain(strategies=[s1, s2, s3])
	result = chain.run(record=base_record)
	assert result == [expected_author_record_gnd]
	s3.assert_not_called()


def test_run_first_success_chain_returns_empty(mocker, base_record, expected_empty_author_record):
	s1 = mocker.Mock(return_value=[expected_empty_author_record])
	s2 = mocker.Mock(return_value=[expected_empty_author_record])
	s3 = mocker.Mock(return_value=[expected_empty_author_record])
	chain = FirstSuccessChain(strategies=[s1, s2, s3])
	result = chain.run(record=base_record)
	assert result == [expected_empty_author_record]
	s3.assert_called_once()


def test_run_merge_fields_chain_success(
	mocker,
	base_record,
	expected_empty_popularity_record,
	expected_sitelinks_record,
	expected_qrank_record,
	expected_merged_popularity_record,
):
	s1 = mocker.Mock(return_value=[expected_empty_popularity_record])
	s2 = mocker.Mock(return_value=[expected_sitelinks_record])
	s3 = mocker.Mock(return_value=[expected_qrank_record])
	chain = MergeFieldsChain(strategies=[s1, s2, s3])
	result = chain.run(record=base_record)
	assert result == [expected_merged_popularity_record]


def test_run_merge_fields_chain_no_merge_when_single_non_empty(
	mocker, base_record, expected_empty_popularity_record, expected_sitelinks_record
):
	s1 = mocker.Mock(return_value=[expected_empty_popularity_record])
	s2 = mocker.Mock(return_value=[expected_sitelinks_record])
	s3 = mocker.Mock(return_value=[expected_empty_popularity_record])
	chain = MergeFieldsChain(strategies=[s1, s2, s3])
	result = chain.run(record=base_record)
	assert result == [expected_sitelinks_record]


def test_run_merge_fields_chain_returns_empty(
	mocker, base_record, expected_empty_popularity_record
):
	s1 = mocker.Mock(return_value=[expected_empty_popularity_record])
	s2 = mocker.Mock(return_value=[expected_empty_popularity_record])
	s3 = mocker.Mock(return_value=[expected_empty_popularity_record])
	chain = MergeFieldsChain(strategies=[s1, s2, s3])
	result = chain.run(record=base_record)
	assert result == [expected_empty_popularity_record]
