from prefect import flow, task
from collections.abc import Iterable

from canon_curator.models import (
	BaseWorkRecord,
	EnrichedWorkRecord,
	GeoRecord,
	AuthorRecord,
	PopularityRecord,
	ReaderstatsRecord,
)


@task
def extract() -> Iterable[BaseWorkRecord]:
	"""Read input files for (batch) processing."""
	raise NotImplementedError


@task()
def enrich_geo() -> Iterable[GeoRecord]:
	"""Retrieve geodata for BaseWorkRecords."""
	raise NotImplementedError


@task()
def enrich_author() -> Iterable[AuthorRecord]:
	"""Retrieve author related data for BaseWorkRecords."""
	raise NotImplementedError


@task()
def enrich_popularity() -> Iterable[PopularityRecord]:
	"""Retrieve popularity metrics for BaseWorkRecords."""
	raise NotImplementedError


@task()
def enrich_readerstats() -> Iterable[ReaderstatsRecord]:
	"""Retrieve reader statistics for BaseWorkRecords."""
	raise NotImplementedError


@task
def merge() -> Iterable[EnrichedWorkRecord]:
	"""Merge each BaseWorkRecord with EnrichmentRecords"""
	raise NotImplementedError


@task
def load() -> None:
	"""Parse EnrichmentRecords into the output format, validate and write to output directory on success."""
	raise NotImplementedError


@flow(name="enrichment-pipeline")
def enrichment_pipeline() -> None:
	"""
	Read user config, call build functions from wiring.py to build enrichers and call tasks.
	"""
	raise NotImplementedError


if __name__ == "__main__":
	enrichment_pipeline()
