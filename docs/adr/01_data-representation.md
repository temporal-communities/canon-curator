---
status: "accepted"
date: 2025-04-02
decision-makers: "@lipogg, @v-ji"
consulted: "@lehkost"
informed: "@fera333"
---

# [01] Unified Data Representation with JSON and JSON-LD

## Context and Problem Statement

Choosing a data representation format hinges on two main requirements:

1. Accessibility for non-technical users, who should be able to view and contribute canon lists in a human-readable, familiar format.
2. Expressiveness for technical users, who may need to query canon lists and rely on detailed metadata and provenance information to interpret and reuse the data.

To meet both needs, the base data format should be a widely used, human-readable data exchange format that allows both straightforward transformation into a richer, semantically structured representation and easy conversion into a tabular format. The data format should provide future compatibility with a lightweight static web service hosted on GitHub pages with a static read-only data endpoint and client-side search/query capabilities.

## Considered Options

Input: 
* JSON 
* CSV/TSV
* YAML

Output: 
* JSON-LD
* RDF/Turtle

## Decision Outcome

Preferred option: JSON as input and JSON-LD as output, because this option strikes the best balance between ease of use, accessibility and expressiveness. JSON is familiar and easy to handle for non-technical users, while JSON-LD enables semantically rich representations suitable for querying and data reuse. This combination also supports multiple data access modalities and integrates well with our planned static web deployment. While other formats (e.g., CSV/TSV, YAML, RDF/Turtle) remain theoretically viable, the final choice depends on the availability and compatibility of data transformation tools and libraries, as outlined in [ADR 02].

## More Information

* JSON-LD specifications: https://json-ld.org/spec/
* W3C best practices for JSON-LD APIs: https://w3c.github.io/json-ld-bp/
* Client-side SPARQL queries: https://comunica.dev/