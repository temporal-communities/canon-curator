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
)

_WORK_UUID = uuid.UUID("00000000-0000-0000-0000-000000000001")
_RETRIEVED_AT = datetime(2025, 1, 1, 0, 0, 0, tzinfo=UTC)


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
    return PopularityRecord(
        work_uuid=_WORK_UUID,
        sitelinks_count=None,
        q_rank=100,
        retrieved_at=_RETRIEVED_AT,
    )


@pytest.fixture
def expected_sitelinks_record():
    return PopularityRecord(
        work_uuid=_WORK_UUID,
        sitelinks_count=20,
        q_rank=None,
        retrieved_at=_RETRIEVED_AT,
    )


@pytest.fixture
def expected_empty_popularity_record():
    return PopularityRecord(
        work_uuid=_WORK_UUID,
        sitelinks_count=None,
        q_rank=None,
        retrieved_at=None,
    )


@pytest.fixture
def expected_readerstats_record():
    return ReaderstatsRecord(
        work_uuid=_WORK_UUID,
        avg_rating=3.77,
        ratings_count=362177,
        source="https://www.goodreads.com/book/show/14942.Mrs_Dalloway",
        retrieved_at=_RETRIEVED_AT,
    )


@pytest.fixture
def expected_empty_readerstats_record():
    return ReaderstatsRecord(
        work_uuid=None,
        avg_rating=None,
        ratings_count=None,
        source=None,
        retrieved_at=None,
    )


@pytest.fixture
def expected_geo_record_wikidata():
    return GeoRecord(
        work_uuid=_WORK_UUID,
        geo_id="Q1018197",
        geo_uri="https://www.wikidata.org/entity/Q1018197",
        geo_label="Eresos",
        lat=39.169897,
        lon=25.933797,
        sources=["https://www.wikidata.org/entity/Q65921422"],
        num_sources=1,
        evidence_level=EvidenceLevel.REFERENCED,
        source_db="https://www.wikidata.org/",
        request_uri="https://www.wikidata.org/entity/Q17892",
        interpretation_context="https://www.wikidata.org/wiki/Property:P19",
        retrieved_at=_RETRIEVED_AT,
    )


@pytest.fixture
def expected_geo_record_wikidata_no_evidence():
    return GeoRecord(
        work_uuid=_WORK_UUID,
        geo_id="Q42295059",
        geo_uri="https://www.wikidata.org/entity/Q42295059",
        geo_label="Mytilene",
        lat=39.1114,
        lon=26.5621,
        sources=[],
        num_sources=0,
        evidence_level=None,
        source_db="https://www.wikidata.org/",
        request_uri="https://www.wikidata.org/entity/Q17892",
        interpretation_context="https://www.wikidata.org/wiki/Property:P19",
        retrieved_at=_RETRIEVED_AT,
    )


@pytest.fixture
def expected_geo_record_gnd():
    return GeoRecord(
        work_uuid=_WORK_UUID,
        geo_id="4022153-2",
        geo_uri="https://d-nb.info/standards/vocab/gnd/geographic-area-code#XA-GB",
        geo_label="Großbritannien",
        lat=54.75844,
        lon=-2.69531,
        sources=[],
        num_sources=0,
        evidence_level=None,
        source_db="https://www.dnb.de/",
        request_uri="https://lobid.org/gnd/4316776-7",
        interpretation_context="https://wiki.dnb.de/download/attachments/90411323/laendercodeleitfaden.pdf",
        retrieved_at=_RETRIEVED_AT,
    )


@pytest.fixture
def expected_empty_geo_record():
    return GeoRecord(
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
        request_uri=None,
        interpretation_context=None,
        retrieved_at=None,
    )


@pytest.fixture
def expected_author_record_wikidata():
    return AuthorRecord(
        work_uuid=_WORK_UUID,
        gender_uri="https://www.wikidata.org/entity/Q6581072",
        gender_marker="female",
        sources=["https://www.wikidata.org/entity/Q2494649"],
        num_sources=1,
        evidence_level=EvidenceLevel.REFERENCED,
        source_db="https://www.wikidata.org/",
        request_uri="https://www.wikidata.org/entity/Q40909",
        interpretation_context="https://www.wikidata.org/wiki/Property:P21",
        retrieved_at=_RETRIEVED_AT,
    )


@pytest.fixture
def expected_author_record_gnd():
    return AuthorRecord(
        work_uuid=_WORK_UUID,
        gender_uri="https://d-nb.info/standards/vocab/gnd/gender#female",
        gender_marker="weiblich",
        sources=[],
        num_sources=0,
        evidence_level=None,
        source_db="https://www.dnb.de/",
        request_uri="https://lobid.org/gnd/118635174",
        interpretation_context="https://wiki.dnb.de/download/attachments/50759357/375.pdf",
        retrieved_at=_RETRIEVED_AT,
    )


@pytest.fixture
def expected_empty_author_record():
    return AuthorRecord(
        work_uuid=None,
        gender_uri=None,
        gender_marker=None,
        sources=None,
        num_sources=None,
        evidence_level=None,
        source_db=None,
        request_uri=None,
        interpretation_context=None,
        retrieved_at=None,
    )


@pytest.fixture
def expected_merged_popularity_record(): 
    return PopularityRecord(
        work_uuid=_WORK_UUID,
        sitelinks_count=20,
        q_rank=100,
        retrieved_at=_RETRIEVED_AT,
    )


@pytest.fixture
def geodata_mapping(expected_geo_record_gnd): 
    return {_WORK_UUID: expected_geo_record_gnd}


@pytest.fixture
def empty_geodata_mapping(expected_empty_geo_record): 
    return {_WORK_UUID: expected_empty_geo_record}


@pytest.fixture
def authordata_mapping(expected_author_record_wikidata): 
    return {_WORK_UUID: expected_author_record_wikidata}


@pytest.fixture
def empty_authordata_mapping(expected_empty_author_record): 
    return {_WORK_UUID: expected_empty_author_record}


@pytest.fixture
def popularity_mapping(expected_merged_popularity_record): 
    return {_WORK_UUID: expected_merged_popularity_record}


@pytest.fixture
def empty_popularity_mapping(expected_empty_popularity_record): 
    return {_WORK_UUID: expected_empty_popularity_record}


@pytest.fixture
def readerstats_mapping(expected_readerstats_record): 
    return {_WORK_UUID: expected_readerstats_record}


@pytest.fixture
def empty_readerstats_mapping(expected_empty_readerstats_record): 
    return {_WORK_UUID: expected_empty_readerstats_record}


@pytest.fixture
def expected_enriched_work_record(    
    base_record,
    expected_geo_record_gnd,
    expected_author_record_wikidata,
    expected_merged_popularity_record,
    expected_readerstats_record,
    ):
    return EnrichedWorkRecord(
				base_data=base_record,
				geodata=expected_geo_record_gnd,
				authordata=expected_author_record_wikidata,
				wd_metrics=expected_merged_popularity_record,
				readerstats=expected_readerstats_record,
			)


@pytest.fixture
def expected_empty_enriched_work_record(    
    base_record,
    expected_empty_geo_record,
    expected_empty_author_record,
    expected_empty_popularity_record,
    expected_empty_readerstats_record,
    ):
    return EnrichedWorkRecord(
				base_data=base_record,
				geodata=expected_empty_geo_record,
				authordata=expected_empty_author_record,
				wd_metrics=expected_empty_popularity_record,
				readerstats=expected_empty_readerstats_record,
			)