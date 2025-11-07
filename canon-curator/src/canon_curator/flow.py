from prefect import flow, task
from collections.abc import Iterable

from canon_curator.models.records import BaseWorkRecord, EnrichedWorkRecord
from canon_curator.models.enrichment import (
	GeoRecord,
	AuthorRecord,
	PopularityRecord,
	ReaderstatRecord,
)


@task
def extract() -> Iterable[BaseWorkRecord]:
	"""Read input files for (batch) processing."""
	pass


@task()
def enrich_geo() -> Iterable[GeoRecord]:
	"""Retrieve geodata for BaseWorkRecords."""
	pass


@task()
def enrich_author() -> Iterable[AuthorRecord]:
	"""Retrieve author related data for BaseWorkRecords."""
	pass


@task()
def enrich_popularity() -> Iterable[PopularityRecord]:
	"""Retrieve popularity metrics for BaseWorkRecords."""
	pass


@task()
def enrich_readerstats() -> Iterable[ReaderstatRecord]:
	"""Retrieve reader statistics for BaseWorkRecords."""
	pass


@task
def merge() -> Iterable[EnrichedWorkRecord]:
	"""Merge each BaseWorkRecord with EnrichmentRecords"""
	pass


@task
def load() -> None:
	"""Parse EnrichmentRecords into the output format, validate and write to output directory on success."""
	pass


@flow(name="enrichment-pipeline")
def enrichment_pipeline() -> None:
	"""
	Read user config, call build functions from wiring.py to build enrichers and call tasks.
	"""
	pass


if __name__ == "__main__":
	enrichment_pipeline()
