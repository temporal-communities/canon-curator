import pytest
import uuid
from datetime import datetime, UTC

from canon_curator.models import (
	BaseWorkRecord,
	EnrichedWorkRecord,
	PopularityRecord,
	ReaderstatsRecord,
	GeoRecord,
	AuthorRecord,
	EvidenceLevel,
	PopularityMetric,
)

_WORK_UUID = uuid.UUID("00000000-0000-0000-0000-000000000001")
_REC_UUID = uuid.UUID("00000000-0000-0000-0000-000000000002")
_GEO_UUID = uuid.UUID("00000000-0000-0000-0000-000000000003")
_AUTHOR_UUID = uuid.UUID("00000000-0000-0000-0000-000000000004")
_SITELINKS_UUID = uuid.UUID("00000000-0000-0000-0000-000000000005")
_QRANK_UUID = uuid.UUID("00000000-0000-0000-0000-000000000007")
_POPULARITY_UUID = uuid.UUID("00000000-0000-0000-0000-000000000008")
_READERSTATS_UUID = uuid.UUID("00000000-0000-0000-0000-000000000006")
_RETRIEVED_AT = datetime(2025, 1, 1, 0, 0, 0, tzinfo=UTC)


def _make_geo_record_gnd(rec_uuid=_REC_UUID):
	return GeoRecord(
		uuid=rec_uuid,
		work_uuid=_WORK_UUID,
		geo_id="4022153-2",
		geo_uri="https://d-nb.info/standards/vocab/gnd/geographic-area-code#XA-GB",
		geo_label="Großbritannien",
		lat=54.75844,
		lon=-2.69531,
		sources=[],
		num_sources=0,
		evidence_level=None,
		source_db="https://isil.staatsbibliothek-berlin.de/isil/DE-588",
		request_url="https://lobid.org/gnd/4316776-7",
		interpretation_context="https://wiki.dnb.de/download/attachments/90411323/laendercodeleitfaden.pdf",
		retrieved_at=_RETRIEVED_AT,
	)


def _make_geo_record_wikidata(rec_uuid=_REC_UUID):
	return GeoRecord(
		uuid=_REC_UUID,
		work_uuid=_WORK_UUID,
		geo_id="Q1018197",
		geo_uri="http://www.wikidata.org/entity/Q1018197",
		geo_label="Eresos",
		lat=39.169897,
		lon=25.933797,
		sources=["https://www.wikidata.org/entity/Q65921422"],
		num_sources=1,
		evidence_level=EvidenceLevel.REFERENCED,
		source_db="http://www.wikidata.org/entity/Q2013",
		request_url="https://www.wikidata.org/wiki/Special:EntityData/Q17892",
		interpretation_context="https://www.wikidata.org/wiki/Property:P19",
		retrieved_at=_RETRIEVED_AT,
	)


def _make_geo_record_wikidata_no_evidence(rec_uuid=_REC_UUID):
	return GeoRecord(
		uuid=_REC_UUID,
		work_uuid=_WORK_UUID,
		geo_id="Q42295059",
		geo_uri="http://www.wikidata.org/entity/Q42295059",
		geo_label="Mytilene",
		lat=39.1114,
		lon=26.5621,
		sources=[],
		num_sources=0,
		evidence_level=None,
		source_db="http://www.wikidata.org/entity/Q2013",
		request_url="https://www.wikidata.org/wiki/Special:EntityData/Q17892",
		interpretation_context="https://www.wikidata.org/wiki/Property:P19",
		retrieved_at=_RETRIEVED_AT,
	)


def _make_empty_geo_record(rec_uuid=_REC_UUID):
	return GeoRecord(
		uuid=rec_uuid,
		work_uuid=None,
		geo_id=None,
		geo_uri=None,
		geo_label=None,
		lat=None,
		lon=None,
		sources=None,
		num_sources=None,
		evidence_level=None,
		source_db=None,
		request_url=None,
		interpretation_context=None,
		retrieved_at=None,
	)


def _make_author_record_wikidata(rec_uuid=_REC_UUID):
	return AuthorRecord(
		uuid=rec_uuid,
		work_uuid=_WORK_UUID,
		gender_uri="http://www.wikidata.org/entity/Q6581072",
		gender_marker="female",
		sources=["https://www.wikidata.org/entity/Q2494649"],
		num_sources=1,
		evidence_level=EvidenceLevel.REFERENCED,
		source_db="http://www.wikidata.org/entity/Q2013",
		request_url="https://www.wikidata.org/wiki/Special:EntityData/Q40909",
		interpretation_context="https://www.wikidata.org/wiki/Property:P21",
		retrieved_at=_RETRIEVED_AT,
	)


def _make_author_record_gnd(rec_uuid=_REC_UUID):
	return AuthorRecord(
		uuid=rec_uuid,
		work_uuid=_WORK_UUID,
		gender_uri="https://d-nb.info/standards/vocab/gnd/gender#female",
		gender_marker="weiblich",
		sources=[],
		num_sources=0,
		evidence_level=None,
		source_db="https://isil.staatsbibliothek-berlin.de/isil/DE-588",
		request_url="https://lobid.org/gnd/118635174",
		interpretation_context="https://wiki.dnb.de/download/attachments/50759357/375.pdf",
		retrieved_at=_RETRIEVED_AT,
	)


def _make_empty_author_record(rec_uuid=_REC_UUID):
	return AuthorRecord(
		uuid=rec_uuid,
		work_uuid=None,
		gender_uri=None,
		gender_marker=None,
		sources=None,
		num_sources=None,
		evidence_level=None,
		source_db=None,
		request_url=None,
		interpretation_context=None,
		retrieved_at=None,
	)


def _make_sitelinks_record(rec_uuid=_REC_UUID):
	return PopularityRecord(
		uuid=rec_uuid,
		work_uuid=_WORK_UUID,
		value=20,
		metric=PopularityMetric.SITELINKS,
		source_db="http://www.wikidata.org/entity/Q2013",
		request_url="https://www.wikidata.org/wiki/Special:EntityData/Q752584",
		retrieved_at=_RETRIEVED_AT,
	)


def _make_qrank_record(rec_uuid=_REC_UUID):
	return PopularityRecord(
		uuid=rec_uuid,
		work_uuid=_WORK_UUID,
		value=100,
		metric=PopularityMetric.QRANK,
		source_db="https://qrank.toolforge.org/",
		request_url="https://qrank.toolforge.org/download/qrank.csv.gz",
		retrieved_at=_RETRIEVED_AT,
	)


def _make_empty_popularity_record(rec_uuid=_REC_UUID):
	return PopularityRecord(
		uuid=rec_uuid,
		work_uuid=None,
		value=None,
		metric=None,
		source_db=None,
		request_url=None,
		retrieved_at=None,
	)


def _make_readerstats_record(rec_uuid=_REC_UUID):
	return ReaderstatsRecord(
		uuid=rec_uuid,
		work_uuid=_WORK_UUID,
		avg_rating=3.77,
		ratings_count=362177,
		source_db="https://www.goodreads.com/",
		request_url="https://www.goodreads.com/book/show/14942.Mrs_Dalloway",
		retrieved_at=_RETRIEVED_AT,
	)


def _make_empty_readerstats_record(rec_uuid=_REC_UUID):
	return ReaderstatsRecord(
		uuid=rec_uuid,
		work_uuid=None,
		avg_rating=None,
		ratings_count=None,
		source_db=None,
		request_url=None,
		retrieved_at=None,
	)


@pytest.fixture(autouse=True)
def fixed_uuid(mocker):
	mocker.patch("canon_curator.models.enrichment.uuid4", return_value=_REC_UUID)


@pytest.fixture
def base_record():
	return BaseWorkRecord(
		uuid=_WORK_UUID,
		list_num="1",
		series_num=None,
		title="Mrs. Dalloway",
		author="Virginia Woolf",
		author_qid="Q40909",
		work_qid="Q752584",
		author_gnd_id="118635174",
		work_gnd_id="4316776-7",
		work_goodreads_id="841320",
		publication_date="1925",
	)


@pytest.fixture
def expected_qrank_record():
	return _make_qrank_record()


@pytest.fixture
def expected_sitelinks_record():
	return _make_sitelinks_record()


@pytest.fixture
def expected_empty_popularity_record():
	return _make_empty_popularity_record()


@pytest.fixture
def expected_readerstats_record():
	return _make_readerstats_record()


@pytest.fixture
def expected_empty_readerstats_record():
	return _make_empty_readerstats_record()


@pytest.fixture
def expected_geo_record_wikidata():
	return _make_geo_record_wikidata()


@pytest.fixture
def expected_geo_record_wikidata_no_evidence():
	return _make_geo_record_wikidata_no_evidence()


@pytest.fixture
def expected_geo_record_gnd():
	return _make_geo_record_gnd()


@pytest.fixture
def expected_empty_geo_record():
	return _make_empty_geo_record()


@pytest.fixture
def expected_author_record_wikidata():
	return _make_author_record_wikidata()


@pytest.fixture
def expected_author_record_gnd():
	return _make_author_record_gnd()


@pytest.fixture
def expected_empty_author_record():
	return _make_empty_author_record()


@pytest.fixture
def geodata_mapping():
	return {_WORK_UUID: [_make_geo_record_gnd(_GEO_UUID)]}


@pytest.fixture
def empty_geodata_mapping():
	return {_WORK_UUID: [_make_empty_geo_record(_GEO_UUID)]}


@pytest.fixture
def authordata_mapping():
	return {_WORK_UUID: [_make_author_record_wikidata(_AUTHOR_UUID)]}


@pytest.fixture
def empty_authordata_mapping():
	return {_WORK_UUID: [_make_empty_author_record(_AUTHOR_UUID)]}


@pytest.fixture
def popularity_mapping():
	return {_WORK_UUID: [_make_sitelinks_record(_SITELINKS_UUID), _make_qrank_record(_QRANK_UUID)]}


@pytest.fixture
def empty_popularity_mapping():
	return {_WORK_UUID: [_make_empty_popularity_record(_POPULARITY_UUID)]}


@pytest.fixture
def readerstats_mapping():
	return {_WORK_UUID: [_make_readerstats_record(_READERSTATS_UUID)]}


@pytest.fixture
def empty_readerstats_mapping():
	return {_WORK_UUID: [_make_empty_readerstats_record(_READERSTATS_UUID)]}


@pytest.fixture
def expected_enriched_work_record(base_record):
	return EnrichedWorkRecord(
		base_data=base_record,
		geodata=[_make_geo_record_gnd(rec_uuid=_GEO_UUID)],
		authordata=[_make_author_record_wikidata(rec_uuid=_AUTHOR_UUID)],
		wd_metrics=[
			_make_sitelinks_record(rec_uuid=_SITELINKS_UUID),
			_make_qrank_record(rec_uuid=_QRANK_UUID),
		],
		readerstats=[_make_readerstats_record(rec_uuid=_READERSTATS_UUID)],
	)


@pytest.fixture
def expected_empty_enriched_work_record(base_record):
	return EnrichedWorkRecord(
		base_data=base_record,
		geodata=[_make_empty_geo_record(rec_uuid=_GEO_UUID)],
		authordata=[_make_empty_author_record(rec_uuid=_AUTHOR_UUID)],
		wd_metrics=[_make_empty_popularity_record(rec_uuid=_POPULARITY_UUID)],
		readerstats=[_make_empty_readerstats_record(rec_uuid=_READERSTATS_UUID)],
	)


@pytest.fixture
def make_wikidata_p19():
	def strategy(record):
		return [GeoRecord.empty()]

	strategy.name = "wikidata_p19"
	return strategy


@pytest.fixture
def make_gnd_gender():
	def strategy(record):
		return [AuthorRecord.empty()]

	strategy.name = "gnd_gender"
	return strategy


@pytest.fixture
def make_wikidata_p21():
	def strategy(record):
		return [AuthorRecord.empty()]

	strategy.name = "wikidata_p21"
	return strategy
