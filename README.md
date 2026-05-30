# Canon Curator 

Canon Curator is a modular Python-based ETL (Extract, Transform, Load) pipeline designed to enrich literary canons and lists of literary works with geographic and demographic metadata, reader statistics and popularity metrics. 

## Features

### Enrichment sources

Canon Curator currently supports the following enrichment sources: 
- **Reader statistics**: Goodreads
- **Popularity metrics**: Wikidata sitelinks and QRank
- **Geodata** pertaining to the work (e.g. country of origin of the literary work) or author (e.g. birth place of the author): Wikidata and GND
- **Author data** (currently gender data): Wikidata or GND 

For each type of data (reader statistics, popularity metrics, geodata, gender data), users may specify several enrichment sources (see Usage). Data from the GND (Integrated Authority File) is retrieved via the [lobid-gnd endpoint](https://lobid.org/gnd), which is updated every three months. 

### Enrichment strategies 

To control how enriched data is handled, Canon Curator defines different strategy chains: 

- **First Success**: Try enrichment sources in a specified order and stop as soon as one source returns a result 
- **Keep All**: Try enrichment sources in a specified order and keep all results

### Provenance tracking

Throughout an enrichment run, provenance information is collected on several levels: 
- **Workflow-level provenance**:
    - Time of retrieval
    - Software agent involved in retrieval (e.g. Canon Curator)
    - Enrichment pipeline run associated with retrieval
- **Statement-level provenance**: 
    - Source database that was accessed to retrieve the data (e.g. Wikidata or GND)
    - URL that was used for making a request to the source database
    - Primary source(s) for the statement if specified in the source database (e.g. Wikidata references associated with a statement)
    - Additional sources that informed the interpretation and handling of retrieved data (e.g. GND area code guidelines, the URI of the Wikidata property consulted)

### Export formats

Available export formats are: 
- **JSON Lines** 
- **JSON-LD** with classic reification via rdf:Statement syntax
- **Turtle** with RDF 1.2 rdf:reifies syntax ("RDF star") or classic reification via rdf:Statement syntax

### Data model 

JSON-LD and Turtle output builds on the following ontologies and vocabularies: 
- CANON, a lightweight domain ontology that can be found [here](https://github.com/temporal-communities/canon-curator/blob/refactor/workflow-management/src/canon_curator/resources/ontology.ttl) (for core classes and properties)
- PROV and PAV (for enrichment provenance)
- Basic Geo (WGS84 lat/long) (for latitude and longitude)
- Dublin Core Terms

The data model builds on this [ontology design pattern for place entities](http://www.ontologydesignpatterns.org/cp/owl/place.owl#), the [subactivities pattern](https://doi.org/10.1007/978-3-031-79450-6) and the [Distributed Provenance Model](https://doi.org/10.1038/s41597-022-01537-6). 

> [!NOTE]  
> Please note that the ontology does not have a stable, dereferenceable URI yet. A GitHub URL is used in the JSON-LD and Turtle output as a placeholder.


## Usage 

### Prerequisites: 
- python >= 3.12
- [uv](https://github.com/astral-sh/uv)
- a canon list


> [!IMPORTANT]  
> Make sure your canon list is in CSV or TSV format and follows the structure described in [Canon Shelf](https://github.com/temporal-communities/canon-shelf).



### Run the pipeline

1. Clone this repo 
2. Run 

```bash
uv sync
```
3. Create a config.yml file (see `config.sample.yml`) and place it in `src/canon_curator` (or specify a different directory with flag `--config-file` in the following step). You can also just remove the .sample part from the filename of the sample YAML file and adapt the file to your needs. If you want to run only part of the pipeline (e.g., only sitelink and QRank enrichment), delete the sections for the other enrichment sources from the config file. 
4. Run the pipeline: 

```bash
uv run python src/canon_curator/flow.py \
  --input-file "<INPUT_FILE_URL>" \
  --out-dir "<OUTPUT_DIRECTORY>" \
  --output-filename "<OUTPUT_FILENAME>" \
  --canon-list-name "<CANON_LIST_NAME>" \
  [--canon-list-iri "<CANON_LIST_IRI>"] \
  --canon-list-metadata-iri "<CANON_LIST_METADATA_IRI>"
```
Note that `--canon-list-iri` is optional when `--input-file` is a URL, as the URL is used as the IRI. 

**Example 1: Input is URL** 

```bash
uv run python src/canon_curator/flow.py \
  --input-file "https://raw.githubusercontent.com/temporal-communities/canon-shelf/main/lists/2025-spiegel-canon-international/2025-spiegel-canon-international.tsv" \
  --out-dir "./out" \
  --output-filename "2025-spiegel-canon-international" \
  --canon-list-name "Spiegel Canon International 2025" \
  --canon-list-metadata-iri "https://raw.githubusercontent.com/temporal-communities/canon-shelf/main/lists/2025-spiegel-canon-international/2025-spiegel-canon-international-metadata.json"
```

**Example 2: Input is local path** 

```bash
uv run python src/canon_curator/flow.py \
  --input-file "/path/to/your/file.tsv" \
  --out-dir "./out" \
  --output-filename "2025-spiegel-canon-international" \
  --canon-list-name "Spiegel Canon International 2025" \
  --canon-list-iri "https://raw.githubusercontent.com/temporal-communities/canon-shelf/main/lists/2025-spiegel-canon-international/2025-spiegel-canon-international.tsv" \
  --canon-list-metadata-iri "https://raw.githubusercontent.com/temporal-communities/canon-shelf/main/lists/2025-spiegel-canon-international/2025-spiegel-canon-international-metadata.json"
```


If your config.yml is not located in the `src/canon_curator`, you may specify the config file path with `--config-file`. 

Supported input formats: 
- CSV or TSV file following the format described in [Canon Shelf](https://github.com/temporal-communities/canon-shelf) (local file path or URL)
- optional: a schema.org dataset description of the CSV or TSV file providing metadata and provenance information about the canon list

### Manage runs 

Pipeline runs are managed using Python [prefect](https://github.com/PrefectHQ/prefect). To cancel a running workflow run, first list all current and previous runs: 

```bash
uv run prefect flow-run ls 
```
Copy the ID of the flow you wish to cancel, then run: 

```bash
uv run prefect flow-run cancel <FLOW-ID>
```

### Query the output

The default Turtle RDF 1.2 output can be queried with pyoxigraph. For instance, to retrieve all geolocation enrichments for all works in the graph, along with associated provenance information, and serialize query results to CSV, run: 

```python

from pyoxigraph import Store, RdfFormat, QueryResultsFormat

store = Store()
store.load(path="ontology.ttl", format=RdfFormat.TURTLE)
store.bulk_load(
    path="2025-spiegel-canon-international.ttl",
    format=RdfFormat.TURTLE
)


solutions = store.query(
    """
    PREFIX canon: <https://github.com/temporal-communities/canon-curator/ontology/>
    PREFIX rdfs:  <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX prov:  <http://www.w3.org/ns/prov#>
    PREFIX pav:   <http://purl.org/pav/>

    SELECT ?work ?p ?location ?sourceDatabase ?primarySource ?sourceContext ?sourceDataset ?agent ?retrievedAt
    WHERE {
    ?work a canon:Work .
    ?p rdfs:subPropertyOf canon:geolocation .
    ?work ?p ?location .

        << ?work ?p ?location >> canon:hasEnrichment ?rec .

        OPTIONAL { ?rec prov:generatedAtTime   ?retrievedAt }
        OPTIONAL { ?rec prov:wasDerivedFrom    ?sourceDatabase }
        OPTIONAL { ?rec prov:hadPrimarySource  ?primarySource }
        OPTIONAL { ?rec pav:sourceAccessedAt   ?sourceContext }
        OPTIONAL { ?rec pav:importedFrom       ?sourceDataset }

        OPTIONAL {
            ?rec prov:wasGeneratedBy ?act .
            ?act prov:wasAssociatedWith ?agent .
        }
    }
    """
)

solutions.serialize("query_results.csv", format=QueryResultsFormat.CSV)

```

Please refer to the [pyoxigraph documentation](https://pyoxigraph.readthedocs.io/en/stable/store.html#pyoxigraph.Store.query) for more serialization options. 

The easiest way to inspect the enriched data in a tabular format is to parse the JSON Lines output into a Pandas dataframe. For instance, to parse only the popularity metrics and reader statistics into a Pandas dataframe and serialize the dataframe to TSV, run: 

```python 
import pandas as pd

df = pd.read_json("2025-spiegel-canon-international.jsonl", lines=True)

base    = pd.json_normalize(df["base_data"]).drop(columns=["uuid"])
stats   = pd.json_normalize(df["readerstats"].explode()).drop(columns=["uuid", "work_uuid"])
metrics   = pd.json_normalize(df["wd_metrics"].explode()).drop(columns=["uuid", "work_uuid"])

pd.concat([base, stats, metrics], axis=1).to_csv("spiegel_canon.tsv", sep="\t", index=False)

```

## Contribute 

If you would like to contribute a new enrichment source, request a feature or report a bug, please [open an issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-an-issue). 