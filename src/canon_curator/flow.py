import argparse
import logging
import yaml
from urllib.parse import urlparse
from datetime import timedelta
from pathlib import Path
from collections.abc import Iterable, Mapping, Sequence
from uuid import UUID

from prefect import flow, task
from prefect.futures import wait
from prefect.tasks import task_input_hash


from canon_curator.models import (
	BaseWorkRecord,
	EnrichedWorkRecord,
	GeoRecord,
	AuthorRecord,
	PopularityRecord,
	ReaderstatsRecord,
)
from canon_curator.extract import CSVReader
from canon_curator.merge import merge_records
from canon_curator.wiring import (
	make_strategy_registry,
	build_geodata_enricher,
	build_authordata_enricher,
	build_popularity_enricher,
	build_readerstats_enricher,
)
from canon_curator.enrich.enrichers import (
	GeodataEnricher,
	AuthordataEnricher,
	PopularityEnricher,
	ReaderstatEnricher,
)
from canon_curator.enrich.clients import (
	GNDClient,
	WikidataClient,
	QRankClient,
	GoodreadsClient,
)
from canon_curator.load import JSONLinesExporter, JSONLDExporter, TurtleExporter
from canon_curator.validate import validate_shacl

logger = logging.getLogger(__name__)


def setup_logging():
	logging.basicConfig(
		level=logging.INFO,
		format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
	)

	logging.getLogger("canon_curator").setLevel(logging.INFO)
	logging.getLogger("prefect").setLevel(logging.INFO)


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(
		description="Enrich a canon list TSV with geodata, author data, popularity, and reader statistics.",
		formatter_class=argparse.ArgumentDefaultsHelpFormatter,
	)
	parser.add_argument("--input-file", required=True, help="Path or IRI to the input TSV file.")
	parser.add_argument(
		"--out-dir",
		type=Path,
		default=Path(__file__).parent,
		help="Directory where output files will be written.",
	)
	parser.add_argument(
		"--output-filename", required=True, help="Base name for output files (without extension)."
	)
	parser.add_argument(
		"--canon-list-iri",
		required=False,
		help="IRI identifying the canon list. Required when --input-file is a local file path.",
	)
	parser.add_argument(
		"--canon-list-name", required=True, help="Human-readable name of the canon list."
	)
	parser.add_argument(
		"--canon-list-metadata-iri", required=True, help="IRI identifying the canon list metadata."
	)
	parser.add_argument(
		"--config-file",
		type=Path,
		default=Path(__file__).parent / "config.yml",
		help="Path to the user config file. Required format: YAML.",
	)
	parser.add_argument(
		"--shapes-file",
		type=Path,
		default=Path(__file__).parent / "resources/shapes.ttl",
		help="Path to the SHACL shapes file. Required format: Turtle.",
	)
	parser.add_argument(
		"--ontology-file",
		type=Path,
		default=Path(__file__).parent / "resources/ontology.ttl",
		help="Path to the ontology file. Required format: Turtle.",
	)
	return parser.parse_args()


@task
def load_config(config_file: Path) -> dict:
	"""Load and parse the YAML enrichment strategy config."""
	with open(config_file, encoding="utf-8") as f:
		return yaml.safe_load(f)


@task
def extract(input_file: Path | str) -> Iterable[BaseWorkRecord]:
	"""Read input files for (batch) processing."""
	with CSVReader(input_file=input_file, delimiter="\t") as reader:
		return reader.read_file()


@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(hours=1))
def enrich_geo(
	records: Iterable[BaseWorkRecord],
	enricher: GeodataEnricher,
) -> Mapping[UUID, Sequence[GeoRecord]]:
	"""Retrieve geodata for BaseWorkRecords."""
	return enricher.enrich(records)


@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(hours=1))
def enrich_author(
	records: Iterable[BaseWorkRecord],
	enricher: AuthordataEnricher,
) -> Mapping[UUID, Sequence[AuthorRecord]]:
	"""Retrieve author related data for BaseWorkRecords."""
	return enricher.enrich(records)


@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(hours=1))
def enrich_popularity(
	records: Iterable[BaseWorkRecord],
	enricher: PopularityEnricher,
) -> Mapping[UUID, Sequence[PopularityRecord]]:
	"""Retrieve popularity metrics for BaseWorkRecords."""
	return enricher.enrich(records)


@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(hours=1))
def enrich_readerstats(
	records: Iterable[BaseWorkRecord],
	enricher: ReaderstatEnricher,
) -> Mapping[UUID, Sequence[ReaderstatsRecord]]:
	"""Retrieve reader statistics for BaseWorkRecords."""
	return enricher.enrich(records)


@task
def merge(
	base_recs: Iterable[BaseWorkRecord],
	geodata: Mapping[UUID, Sequence[GeoRecord]],
	authordata: Mapping[UUID, Sequence[AuthorRecord]],
	popularity: Mapping[UUID, Sequence[PopularityRecord]],
	readerstats: Mapping[UUID, Sequence[ReaderstatsRecord]],
) -> Iterable[EnrichedWorkRecord]:
	"""Merge each BaseWorkRecord with EnrichmentRecords"""
	return merge_records(
		base_recs=base_recs,
		geodata=geodata,
		authordata=authordata,
		popularity=popularity,
		readerstats=readerstats,
	)


@task
def load(
	records,
	filename: str,
	out_dir: Path | str,
	canon_list_iri: str,
	canon_list_name: str,
	canon_list_metadata_iri: str,
	output_format: str = "turtle",
	provenance_format: str = "star",
) -> Path | None:
	if output_format == "jsonlines":
		with JSONLinesExporter(filename=filename, out_dir=out_dir) as exporter:
			exporter.export(records)
		return None
	elif output_format == "jsonld":
		with JSONLDExporter(
			filename=filename,
			out_dir=out_dir,
			canon_list_iri=canon_list_iri,
			canon_list_name=canon_list_name,
			canon_list_metadata_iri=canon_list_metadata_iri,
			provenance_format=provenance_format,
		) as exporter:
			exporter.export(records)
		return Path(out_dir) / filename
	elif output_format == "turtle":
		with TurtleExporter(
			filename=filename,
			out_dir=out_dir,
			canon_list_iri=canon_list_iri,
			canon_list_name=canon_list_name,
			canon_list_metadata_iri=canon_list_metadata_iri,
			provenance_format=provenance_format,
		) as exporter:
			exporter.export(records)
		return Path(out_dir) / filename
	else:
		raise ValueError("Output format not supported at this time.")


@task
def validate(
	graph_path: Path,
	shapes_path: Path,
	ontology_path: Path,
	use_debug_mode: bool = False,
) -> bool:
	graph_format = "json-ld" if graph_path.suffix == ".jsonld" else "turtle"
	conforms, _, results_text = validate_shacl(
		graph_path=graph_path,
		shapes_path=shapes_path,
		ontology_path=ontology_path,
		graph_format=graph_format,
	)
	if not conforms:
		logger.warning("SHACL validation failed:\n%s", results_text)
	return conforms


@flow(name="enrichment-pipeline")
def enrichment_pipeline(
	input_file: Path | str,
	config_file: Path,
	shapes_file: Path,
	ontology_file: Path,
	out_dir: Path,
	output_filename: str,
	canon_list_metadata_iri: str,
	canon_list_iri: str,
	canon_list_name: str,
) -> None:
	"""Read user config, call build functions from wiring.py to build enrichers and call tasks."""
	with open(config_file, encoding="utf-8") as f:
		user_config = yaml.safe_load(f)

	with (
		QRankClient() as qrank_client,
		WikidataClient() as wikidata_client,
		GNDClient() as gnd_client,
		GoodreadsClient() as goodreads_client,
	):
		registry = make_strategy_registry(
			gnd_client, wikidata_client, qrank_client, goodreads_client
		)
		geodata_enricher = build_geodata_enricher(registry, user_config)
		authordata_enricher = build_authordata_enricher(registry, user_config)
		popularity_enricher = build_popularity_enricher(registry, user_config, qrank_client, wikidata_client)
		readerstats_enricher = build_readerstats_enricher(registry, user_config)

		base_records = extract(input_file)

		geodata_future = (
			enrich_geo.submit(base_records, geodata_enricher) if geodata_enricher else None
		)
		authordata_future = (
			enrich_author.submit(base_records, authordata_enricher) if authordata_enricher else None
		)
		popularity_future = (
			enrich_popularity.submit(base_records, popularity_enricher)
			if popularity_enricher
			else None
		)
		readerstats_future = (
			enrich_readerstats.submit(base_records, readerstats_enricher)
			if readerstats_enricher
			else None
		)

		wait(
			[
				f
				for f in [geodata_future, authordata_future, popularity_future, readerstats_future]
				if f
			]
		)  # type: ignore

		enriched = merge(
			base_recs=base_records,
			geodata=geodata_future.result() if geodata_future else {},
			authordata=authordata_future.result() if authordata_future else {},
			popularity=popularity_future.result() if popularity_future else {},
			readerstats=readerstats_future.result() if readerstats_future else {},
		)

		jsonl_future = load.submit(
			enriched,
			f"{output_filename}.jsonl",
			out_dir,
			canon_list_iri,
			canon_list_name,
			canon_list_metadata_iri,
			output_format="jsonlines",
		)
		jsonld_future = load.submit(
			enriched,
			f"{output_filename}.jsonld",
			out_dir,
			canon_list_iri,
			canon_list_name,
			canon_list_metadata_iri,
			output_format="jsonld",
			provenance_format="reified",
		)
		turtle_future = load.submit(
			enriched,
			f"{output_filename}.ttl",
			out_dir,
			canon_list_iri,
			canon_list_name,
			canon_list_metadata_iri,
			output_format="turtle",
		)

		wait([jsonl_future, jsonld_future, turtle_future])

		jsonld_val_future = validate.submit(jsonld_future.result(), shapes_file, ontology_file)
		wait([jsonld_val_future])


if __name__ == "__main__":
	setup_logging()
	args = parse_args()
	if not args.canon_list_iri and not urlparse(str(args.input_file)).scheme:
		raise SystemExit("error: --canon-list-iri is required when --input-file is a local path")

	enrichment_pipeline(
		input_file=args.input_file,
		config_file=args.config_file,
		shapes_file=args.shapes_file,
		ontology_file=args.ontology_file,
		out_dir=args.out_dir,
		output_filename=args.output_filename,
		canon_list_metadata_iri=args.canon_list_metadata_iri,
		canon_list_iri=args.canon_list_iri,
		canon_list_name=args.canon_list_name,
	)
