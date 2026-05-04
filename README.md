# Canon Curator 

Canon Curator is a modular Python-based ETL (Extract, Transform, Load) pipeline designed to enrich literary canons and lists of literary works with geographic and demographic metadata, reader statistics and popularity metrics. 

## Features

### Enrichment sources

Canon Curator currently supports the following enrichment sources: 
- **Reader statistics**: Goodreads
- **Popularity metrics**: Wikidata sitelinks and QRank
- **Geodata** pertaining to the work (e.g. country of origin of the literary work) or author (e.g. birth place of the author): Wikidata and GND
- **Author data** (currently gender data): Wikidata or GND 

For each type of data (reader statistics, popularity metrics, geodata, gender data), users may specify several enrichment sources. 

### Enrichment strategies 

To control how enriched data is handled, Canon Curator defines different strategy chains: 

- **First Success**: try enrichment sources in a specified order and stop as soon as one source returns a result 
- **Keep All**: try enrichment sources in a specified order and keep all results

### Provenance tracking

Throughout an enrichment run, provenance information is collected on several levels: 
- **Workflow-level provenance**: all enrichment steps in an enrichment run are recorded as enrichment activities and linked to their associated enrichment records
- **Statement-level provenance**: 
    - Time of retrieval
    - Software agent involved in retrieval (e.g. Canon Curator)
    - Source database that was accessed to retrieve the data (e.g. Wikidata or GND)
    - URL that was used for making a request to the source database
    - Primary source(s) for the statement if specified in the source database (e.g. Wikidata references associated with a statement)
    - Additional sources that informed the interpretation and handling of retrieved data (e.g. GND area code guidelines, the URI of the Wikidata property consulted)

### Export formats

Available export formats are: 
- JSONLines 
- JSON-LD with classic reification via rdf:Statement syntax
- Turtle with RDF 1.2 rdf:reifies syntax ("RDF star") or classic reification via rdf:Statement syntax

### Data model 

JSON-LD and Turtle output builds on the following ontologies and vocabularies: 
- CANON, a lightweight domain ontology that can be found [here](https://github.com/temporal-communities/canon-curator/blob/refactor/workflow-management/src/canon_curator/resources/ontology.ttl) (for core classes and properties)
- PROV and PAV (for enrichment provenance)
- Basic Geo (WGS84 lat/long) (for latitude and longitude)
- DC Terms

The data model builds on this [ontology design pattern for place entities](http://www.ontologydesignpatterns.org/cp/owl/place.owl#), the [subactivities pattern](https://doi.org/10.1007/978-3-031-79450) and the [Distributed Provenance Model](https://doi.org/10.1038/s41597-022-01537-6). 

## Usage 

Prerequisites: 
- python >= 3.12
- [uv](https://github.com/astral-sh/uv)


:exclamation: Make sure your canon list is in CSV or TSV format and follows the structure described in [Canon Shelf](https://github.com/temporal-communities/canon-shelf)

1. Clone this repo 
2. Run 

```bash
uv sync
```
3. Create a config.yml file (see `config.sample.yml`) and place it in `src/canon_curator` (or specify a different directory with flag `--config-file` in the following step)
4. Run the pipeline: 

```bash
uv run python src/canon_curator/flow.py \
  --input-file "https://raw.githubusercontent.com/temporal-communities/canon-shelf/main/lists/2025-spiegel-canon-international/2025-spiegel-canon-international.tsv" \
  --out-dir "./out" \
  --output-filename "2025-spiegel-canon-international" \
  --canon-list-name "Spiegel Canon International 2025" \
  --canon-list-metadata-iri "https://raw.githubusercontent.com/temporal-communities/canon-shelf/main/lists/2025-spiegel-canon-international/2025-spiegel-canon-international-metadata.json"
```

If your config.yml is not located in the `src/canon_curator`, you may specify the config file path with `--config-file`. 

Supported input formats: 
- CSV or TSV file following the format described in [Canon Shelf](https://github.com/temporal-communities/canon-shelf) (local file path or URL)
- optional: a schema.org dataset description of the CSV or TSV file providing metadata and provenance information about the canon list

## Contribute 

If you would like to contribute a new enrichment source, request a feature or report a bug, please [open an issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-an-issue). 