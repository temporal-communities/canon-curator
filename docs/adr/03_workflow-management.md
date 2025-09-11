---
status: "accepted"
date: 2025-08-25
decision-makers: "@lipogg, @v-ji"
consulted: ""
informed: "@lehkost"
---

# [03] Workflow management with Prefect

## Context and Problem Statement

Our workflow is: 

1. Load CSV/TSV files from canon-shelf GitHub repository
3. Enrich with geodata, popularity metrics and reader statistics from different sources (GeoNames, Wikidata, etc.) and log provenance
4. Export to JSON-LD with JSON-LD context mapping
5. Save enriched JSON-LD files and workflow provenance to Zenodo (or Figshare)

At a later stage, the enriched data will be served to a website with a client-side query interface such as Comunica, and a static JSON API. Possible future extensions to this workflow include adding more enrichment sources and steps (Goodreads, Lovelybooks, ...) and changing or adding output formats (Parquet for DuckDB-wasm instead of JSON-LD for Comunica). 

Choosing a workflow management system hinges on the following requirements:

- Free, open source, actively maintained
- Compatible with the chosen data representation format and workflow: has to support ETL-type workflows (Extract - Transform - Load), support batch processing
- Easily replaceable by a different workflow management system if the requirements change
- Seamlessly integrate with Python workflow, uv for package management,  Nix for environment reproducibility and GitHub for running the workflow; workflow must be able to run entirely in GitHub, but ideally allow switching to more sophisticated workflow orchestration via free cloud execution features later on
- Help reduce boilerplate code while avoiding blackboxing logic that is important for transparency and understandability 
- Help handle concurrent HTTP requests, caching, and writing enriched JSON-LD files in a robust, efficient way
- Allow reading data from GitHub as well as various enrichment sources (Goodreads, Wikidata, GeoNames,...) and writing data to Zenodo (or Figshare)
- Allow expressing the workflow in human readable form understandable to non-experts, not in a niche DSL (domain-specific language)
- Allow defining different workflow paths based on conditions and variations in data, or events during workflow execution (f.e. during the extraction or enrichment steps)
- Allow recording workflow provenance information in a way that can be seamlessly mapped to the provenance data model specified in [ADR 04]

"Nice to have" requirements: 

- Built-in workflow and data provenance tracking
- Visual representation of the workflow


## Considered Options

* Apache Airflow: https://airflow.apache.org/
* Dagster: https://dagster.io/
* Data Chain: https://github.com/iterative/datachain
* Data Version Control (DVC): https://dvc.org/
* Data Load Tool (DLT): https://dlthub.com/
* Fluree JSON-LD database: https://flur.ee/json-ld/
* Kedro framework: https://kedro.org/
* LinkedPipes ETL suite for linked data: https://etl.linkedpipes.com/
* Meltano ETL/data integration engine: https://github.com/meltano/meltano
* Prefect Python framework: https://github.com/PrefectHQ/prefect/; https://docs.prefect.io/v3/
* PyAirbyte Python ETL library: https://github.com/airbytehq/PyAirbyte
* RDFPro CLI tool and library for linked data integration: https://rdfpro.fbk.eu/
* Scrapy Python web scraping framework: https://www.scrapy.org/
* Silk linked data integration framework: https://github.com/silk-framework/silk
* Snakemake workflow management tool: https://snakemake.readthedocs.io/en/stable/
* Windmill developer platform and workflow engine: https://www.windmill.dev/

We considered only open source, free systems. 

## Decision Outcome

Chosen option: "Workflow management with Prefect" because Prefect allows defining dynamic workflows natively in Python and meets most of our requirements. It provides structure and built-in features such as caching, concurrency, and retry logic, while keeping workflow logic transparent and avoiding lock-in to a niche ecosystem. 

## Pros and Cons of the Options

### Apache Airflow

"Apache Airflow® is an open-source platform for developing, scheduling, and monitoring batch-oriented workflows. Airflow’s extensible Python framework enables you to build workflows connecting with virtually any technology. A web-based UI helps you visualize, manage, and debug your workflows. You can run Airflow in a variety of configurations — from a single process on your laptop to a distributed system capable of handling massive workloads."

Pros
* Built-in retry logic for HTTP requests
* Built-in support for concurrency handling 
* Basic built-in provenance tracking (run IDs, parameters, timestamps)
* Workflow visualization feature
* Mature and well-documented

Cons
* Can be triggered and run via GitHub Actions but requires an Airflow instance: https://dev.to/alexmercedcoder/orchestrating-airflow-dags-with-github-actions-a-lightweight-approach-to-data-curation-across-spark-dremio-and-snowflake-28eg
* No option for free cloud execution (like Prefect and Windmill)
* Steeper learning curve than Prefect and Windmill 
* Many conventions for Python code, not very flexible: if the workflow management system changes, rewrites might be time-consuming 
* Allows defining workflows in Python, but workflows are still defined as DAGs (directed acyclic graphs) and workflow graph is built and validated before runtime

More information
* https://airflow.apache.org/docs/apache-airflow/stable/index.html
* https://airflow.apache.org/docs/apache-airflow/stable/howto/dynamic-dag-generation.html
* https://airflow.apache.org/docs/apache-airflow/stable/index.html#why-not-airflow
* https://airflow.apache.org/docs/apache-airflow-providers/

### Dagster

"Dagster is a cloud-native data pipeline orchestrator for the whole development lifecycle, with integrated lineage and observability, a declarative programming model, and best-in-class testability. It is designed for developing and maintaining data assets, such as tables, data sets, machine learning models, and reports."

Pros
* Centered on data and datasets ("assets"), with many data-centric features, f.e. attaching ownership information to datasets via @dg.asset decorator, as well as workflow provenance
* Clear project organization with assets, resources and components
* Made for ETL pipelines
* Installable "integrations" instead of built-in connectors, including integrations for GitHub, DuckDB, Polars
* Defaults to uv as package manager

Cons
* Project has to be structured in a way specific to Dagster, has to be rewritten if the workflow management system is replaced 
* Components defined declaratively in YAML files
* Data sources have to be defined as assets, have to be rewritten if the workflow management system is replaced
* Detailed documentation with examples tailored to ETL pipelines
* No free tier for cloud execution

More information
* https://github.com/dagster-io/dagster
* https://dagster.io/integrations#integration-list
* https://docs.dagster.io/guides/build/projects/structuring-your-dagster-project
* https://docs.dagster.io/examples/etl-pipeline
* https://docs.dagster.io/guides/build/assets/metadata-and-tags

### Data Chain

"DataChain is a Python-based AI-data warehouse for transforming and analyzing unstructured data like images, audio, videos, text and PDFs. It integrates with external storage (e.g. S3) to process data efficiently without data duplication and manages metadata in an internal database for easy and efficient querying."

Pros
* Allows defining workflows in Python, does not require extra workflow file
* Made for ETL workflows
* Built-in data lineage tracking 
* Built-in data versioning (via metadata references)
* Allows displaying dependency graphs for databases, their data sources and storage locations
* Built-in optimization techniques: caching and parallelization
* Efficient vectorized operations over Python objects 

Cons
* Geared towards machine learning workflows
* More suitable for handling computation-heavy, parallelizable machine learning workflows, not concurrent HTTP requests

### Data Version Control (DVC)

DVC is Makefile-based/command line data pipeline system to "define, execute and track data pipelines". It is described as "git for data" because it allows versioning data as well as machine learning models and storing them in cloud storage. 

Pros
* Ideal for versioning data artifacts and matching data versions with code versions
* Can be combined with other frameworks like DataChain or Prefect

Cons
* Does not allow defining pipelines in Python, requires additional workflow file
* Does not provide support handling HTTP requests, too lightweight for standalone usage
* Supports only a limited number of mostly proprietary remotes for storing versioned data, no support for Zenodo: https://github.com/iterative/dvc/issues/6009
* Possibly expensive in terms of storage, since files are copied when versioned

* Example usage of DVC with DataChain: https://github.com/shcheklein/example-datachain-dvc
* Example usage of DVC with Prefect: https://medium.com/data-science/create-a-maintainable-data-pipeline-with-prefect-and-dvc-1d691ea5bcea

Note: If Zenodo is supported as remote in the future, we could use DVC for data version control. Alternatively, we could write a fsspec-compatible filesystem for Zenodo to address Zenodo as remote ourselves, as proposed in https://github.com/iterative/dvc/issues/6009.

### Data Load Tool (DLT)

Python package for extracting and loading data that "loads data from various and often messy data sources into well-structured, live datasets". DLT "provides a structured framework that streamlines the process of data integrating into various destinations."

Pros: 
* Allows defining workflows in Python, does not require extra workflow file
* Clear separation of steps in the workflow via decorators (@dlt.source, @dlt.resource, @dlt.transformer, @dlt.destination)
* Built-in connectors for various data sources (RestAPIs, databases) and destination databases
* Allows writing custom sources and destinations that can then be called in the pipeline
* Built-in integration with Scrapy for scraping tasks: https://github.com/dlt-hub/dlt_demos/tree/main/scraping-source

Cons: 
* Geared towards industry ELT pipelines, main use case is loading data into data warehouse, with minimal prior transfomation (EtLT), not ETL 
* DLT automatically infers relational schema and flattens nested input data: processing RDF/JSON-LD and customizing data transformation will likely be tricky
* Good for cleaning messy data that can be mapped to relational schema, but not for creating semantically enriched data

More information
* https://dlthub.com/docs/general-usage/resource
* https://dlthub.com/docs/dlt-ecosystem/destinations/destination
* https://dlthub.com/docs/general-usage/schema-contracts
* https://dlthub.com/blog/dlt-etlt

### Fluree

Fluree is a cloud-native JSON-LD database suite. "Whereas in a relational database management system (RDBMS) you'd create a database to hold your data, in Fluree you create a ledger. A ledger is a record of all the transactions (data insertions, updates, and deletes), and all of your transactions and queries will run against a ledger." https://next.developers.flur.ee/docs/learn/tutorial/introduction/#the-fluree-interface

Pros
* Allows plain JSON input, JSON-LD or JSON and context file as input: https://next.developers.flur.ee/docs/learn/foundations/json-ld/
* Immutable, uses ledger to maintain state (i.e. record data changes). Historical states of the database which can be queried: https://next.developers.flur.ee/docs/learn/foundations/verifiable-data/ This functionality is meant to create "verifiable data", but it is also a way to embed provenance tracking in the core of the application.  
* Offers different deployment architectures, among them a build for a web-worker to embed in a browser that allows loading the Fluree query engine into a worker thread: https://docsarchive.flur.ee/docs/reference/serviceworker/examples; https://github.com/fluree/db?tab=readme-ov-file#overview
* There is a React wrapper "that allows you to create real-time apps by wrapping your React components with queries (GraphQL or FlureeQL)." (https://github.com/fluree/db); it allows to query and sync data from a Fluree ledger directly in your React components — using FlureeQL or GraphQL — while automatically updating the UI when data changes.
* Also supports regular SPARQL queries: https://developers.flur.ee/docs/learn/overview/#feature-rundown
* Actively maintained

Cons 
* Dependency on Fluree, might become proprietary at some point 
* Unclear how well the static setup would work, could be brittle
* May be unflexible if we want to replace output format and query options in the future (f.e. Parquet and DuckDB-wasm)

More Information
* https://developers.flur.ee/docs/learn/foundations/json-ld/
* https://next.developers.flur.ee/docs/learn/tutorial/introduction/
* https://next.developers.flur.ee/docs/learn/tutorial/fluree-data-model/
* https://github.com/fluree/db?tab=readme-ov-file#overview

### Kedro

"Kedro is a toolbox for production-ready data science." "It borrows concepts from software engineering and applies them to machine-learning projects" and "standardises how data science code is created." "A Kedro project provides scaffolding for complex data and machine-learning pipelines." 

* Automatically set up a standardized Python project scaffolding, defaults to uv as package manager
* But also allows using individual modules of the Kedro library without committing to the Kedro project structure
* Several lightweight connectors for saving and loading data, mostly basic connectors for loading and saving data from/to CSV, JSON, Parquet and extracting from HTTP API 
* Pipeline visualization feature  
* Built-in dataset versioning
* Built-in data lineage tracking 
* Built-in support for concurrent pipeline execution
* Built-in DVC support: https://docs.kedro.org/en/1.0.0/integrations-and-plugins/dvc/

Cons 
* Requires additional YAML config file for connectors and pipeline definition
* Pipelines are defined as static DAGs (directed acyclic graphs)
* Concurrency limited to running pipeline nodes concurrently, without built-in retries, rate limits

More information
* Project structure: https://docs.kedro.org/en/1.0.0/getting-started/architecture_overview/
* Example projects using Kedro: https://github.com/kedro-org/kedro-community
* Connectors: https://docs.kedro.org/en/0.18.14/kedro.extras.datasets.html
* https://docs.kedro.org/en/1.0.0/catalog-data/data_catalog/#dataset-versioning
* https://docs.kedro.org/en/1.0.0/catalog-data/data_catalog/#the-basics-of-catalogyml
* https://docs.kedro.org/en/1.0.0/build/run_a_pipeline/#runners

### LinkedPipes 

"LinkedPipes ETL is an RDF-based, lightweight ETL tool". It is tailored for linked data workflows and includes components for extracting, transforming and loading data from differnt sources to different target databases.

Pros
* Native RDF support, includes JSON to JSON-LD transformation component

Cons 
* Java based, UI heavy, geared towards Wikibase
* Limited number of components/connectors 
* Not very actively maintained: last commit almost a year ago, only four contributors

### Meltano 

"Meltano is a declarative data integration engine".

Pros
* Many connectors for loading and extracting data, including basic connectors to extract data from/save to CSV, JSON, REST API, GitHub
* Built around Singer taps (data extraction scripts) and targets (data loading scripts) standard for ETL workflows

Cons
* Plugin-based system that requires Meltano-specific declarative config file
* Strict format for writing custom extractors, which might cause issues with messy data sources/scrapers: https://docs.meltano.com/tutorials/custom-extractor
* Project has to be structured in a way specific to Meltano, has to be rewritten if the workflow management system is replaced 
* Many connectors are out of date and no longer maintained according to https://docs.google.com/spreadsheets/d/1ymcGsC9mg7fDkcPzVCjPtz4svoiUEC717tybtmwFBD8/edit?gid=446376949#gid=446376949
* Singer standard is officially an ETL specification, but the Transform part is seemingly meant to be minimal
* Requires SQL-based database as backend (but can use SQLite)
* Stream-based architecture

More information
* https://www.singer.io/

### Prefect

Prefect is a Python framework for workflow orchestration and building data pipelines. It is "an open-source orchestration engine that turns your Python functions into production-grade data pipelines with minimal friction. You can build and schedule workflows in pure Python—no DSLs or complex config files—and run them anywhere you can run Python. Prefect handles the heavy lifting for you out of the box: automatic state tracking, failure handling, real-time monitoring, and more." It positions itself as an alternative to Apache Airflow.

Pros
* Allows defining workflows in Python; tasks discovered and workflow graph is built at runtime, and visualized as a DAG after it was run 
* Allows processing outputs flexibly based on conditions and changing output data
* Built-in caching mechanism 
* Built-in support for handling concurrency in tasks with HTTP requests, including retry logic
* Installable "integrations" instead of built-in connectors
* Easy integration with GitHub via https://docs.prefect.io/integrations/prefect-github
* Basic built-in provenance tracking (run IDs, parameters, timestamps)
* Workflow visualization feature
* Optional cloud execution limits with free tier (alternative to GH actions triggered workflow)
* Can be triggered and run via GitHub Actions: https://docs.prefect.io/v3/advanced/deploy-ci-cd
* Detailed documentation
* Actively maintained: nightly releases

Cons
* If workflows are defined in Python, they have to be rewritten if the workflow management system is replaced 

More information
* https://www.prefect.io/blog/beyond-loops-how-prefect-s-task-mapping-scales-to-thousands-of-parallel-tasks
* https://docs.prefect.io/v3/get-started

### PyAirbyte 

PyAirbyte is a Python wrapper around Airbyte that allows using Airbyte connectors in Python. Airbyte is "the leading data integration platform for ETL / ELT data pipelines from APIs, databases & files to data warehouses, data lakes & data lakehouses."

Pros
* Many connectors for loading and extracting data, including basic connectors to extract data from CSV, JSON, GitHub
* Connectors installed with uv, different Python versions can be specified for different connectors

Cons 
* Does not offer much more than using Airbyte connectors, and most connectors are geared towards industry and data warehousing, not relevant for us
* Writing custom connectors seems to be tricky and formalized through ConnectorBuilder UI: https://docs.airbyte.com/integrations/custom-connectors

More information
* https://airbyte.com/; https://github.com/airbytehq/airbyte

### RDFPro

"RDFpro (RDF Processor) is a public domain, Java command line tool and library for RDF processing. RDFpro offers a suite of stream-oriented, highly optimized RDF processors for common tasks that can be assembled in complex pipelines to efficiently process RDF data in one or more passes. RDFpro originated from the need of a tool supporting typical Linked Data integration tasks, involving dataset sizes up to few billions triples."

Pros
* Native RDF support

Cons
* Java based
* No longer maintained 

### Scrapy 

"Scrapy is a fast high-level web crawling and web scraping framework, used to crawl websites and extract structured data from their pages. It can be used for a wide range of purposes, from data mining to monitoring and automated testing."

Pros
* Built-in support for handling concurrent HTTP requests, extensive middleware and retry configurations
* Includes a pipeline system, but focuses on data extraction
* Workflow is not defined in a single file, pipelines are for basic processing of extracted data and loading it in database

Cons 
* Primarily for web scraping, not API requests or more complex data processing and transformation

### Silk 

"Silk is an open source framework for integrating heterogeneous data sources. The primary uses cases of Silk include: Generating links between related data items within different Linked Data sources. Linked Data publishers can use Silk to set RDF links from their data sources to other data sources on the Web. Applying data transformations to structured data sources."

Pros
* Native RDF support

Cons
* Java based, UI heavy
* Requires Docker

### Snakemake

"The Snakemake workflow management system is a tool to create reproducible and scalable data analyses. Workflows are described via a human readable, Python based language. They can be seamlessly scaled to server, cluster, grid and cloud environments, without the need to modify the workflow definition. Snakemake workflows can entail a description of required software, which will be automatically deployed to any execution environment. Finally, workflow runs can be automatically turned into interactive portable browser based reports, which can be shared with collaborators via email or the cloud and combine results with all used parameters, code, and software."

Pros 
* CLI based but made for usage with Python
* Built-in provenance tracking 
* Workflow visualization feature
* Built-in scheduling and parallelization 
* Geared towards research workflows
* Workflows can be exported to Common Workflow Language: https://snakemake.readthedocs.io/en/stable/executing/interoperability.html

Cons
* Requires additional config file for pipeline definition; pipelines are defined as static DAGs (directed acyclic graphs)
* Parallelization with automatic detection of parallelizable tasks is meant to be run locally across CPU cores or on SLURM / HPC cluster
* More suitable for handling computation-heavy, parallelizable file-producing workflows, not concurrent HTTP requests 
* Relies on Conda, not uv

### Windmill

"Windmill is a fast, open-source workflow engine and developer platform. It's an alternative to the likes of Retool, Superblocks, n8n, Airflow, Prefect, Kestra and Temporal, designed to build comprehensive internal tools (endpoints, workflows, UIs). It supports coding in TypeScript, Python, Go, PHP, Bash, C#, SQL and Rust, or any Docker image, alongside intuitive low-code builders, featuring: An execution runtime for scalable, low-latency function execution across a worker fleet. An orchestrator for assembling these functions into efficient, low-latency flows, using either a low-code builder or YAML. An app builder for creating data-centric dashboards, utilizing low-code or JS frameworks like React."

Pros
* Workflow does not have to be Python-based
* Actively maintained: nightly releases
* Generous optional cloud execution limits with free tier (alternative to GH actions triggered workflow)
* Installable "integrations" instead of built-in connectors
* Built-in HTTP request node
* Allows either defining workflows in Python code or in a separate script


Cons
* Can be triggered and run via GitHub Actions, but intended usage requires paid feature: https://www.windmill.dev/docs/advanced/deploy_gh_gl
* Workflow steps can only be defined in different languages if the workflow is defined in a separate YAML file. If workflows are defined in Python, they have to be rewritten if the workflow management system is replaced
* Documentation is short and mostly meant for the Windmill Web IDE
* Seems to be optimized for usage with separate script, Python workflow definitions require more boilerplate code than Prefect

More information
* https://www.windmill.dev/docs/compared_to/prefect
* https://www.windmill.dev/docs/compared_to/peers
* https://www.windmill.dev/docs/integrations/integrations_on_windmill

## More Information

* Big list of existing workflow systems: https://github.com/common-workflow-language/common-workflow-language/wiki/Existing-Workflow-systems
* SSH Open Marketplace Workflows: https://openhumanitiesdata.metajnl.com/articles/10.5334/johd.192