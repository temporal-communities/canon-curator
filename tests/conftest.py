import pytest
import uuid
from datetime import datetime, UTC

from canon_curator.models import (
    BaseWorkRecord,
    PopularityRecord,
    ReaderstatsRecord,
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
