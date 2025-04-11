---
status: "accepted"
date: 2025-04-02
decision-makers: "@lipogg, @v-ji"
consulted: "@lehkost"
informed: "@fera333"
---

# [02] JSON to JSON-LD Transformation

## Context and Problem Statement

The goal of this decision is to define a robust and sustainable approach for transforming JSON files representing research data into JSON-LD (or RDF/Turtle). Several key requirements guide this decision:

1.	Flexibility: Input JSON files may vary depending on the use case. Regardless of structural differences, they should be transformable into a consistent JSON-LD (or RDF/Turtle) format.
2.	Maintainability: The transformation logic should be easy to define, understand, and maintain. 
3.	Reusability: The chosen method should require minimal changes when adapted to other use cases, preferably by updating a single mapping file rather than modifying multiple scripts.
4.	Sustainability: The transformation process should rely on free, open-source tools that are stable and well-maintained to ensure sustainability and align with FAIR data practices.

In short, we are looking for a transformation solution that is declarative, lightweight, standards-compliant, and sustainable, without locking us into a complex or brittle toolchain.

## Considered Options

* JSON to JSON-LD transformation using context definition file and JSON-LD processor
* JSON to RDF transformation using YARRRML mapping, [yarrrml-parser](https://github.com/RMLio/yarrrml-parser) and [rmlmapper](https://github.com/RMLio/rmlmapper-java)
* JSON to RDF transformation using Fix mapping and Librecat [Catmandu](https://github.com/LibreCat/Catmandu)

## Decision Outcome

Chosen option: "JSON to JSON-LD transformation using context definition file and JSON-LD processor", because it strikes the best balance between ease of data transformation, long-term tool support and compliance with FAIR data standards and best practices.

## Pros and Cons of the Options

### JSON to JSON-LD transformation using context definition file and JSON-LD processor

This approach involves defining a JSON-LD context file that maps plain JSON property names to IRIs. The JSON data is then processed using a JSON-LD processor library (e.g., rdflib, pyLD) to expand the data into JSON-LD. 

* Good, because expanding contexts using a JSON-LD processor is straightforward; contexts can be defined in a separate file
* Good, because sufficient number of Python JSON-LD processors exist that support JSON-LD expansion: [rdflib](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.plugins.shared.jsonld.html#rdflib.plugins.shared.jsonld.context.Context.expand) is our first choice, because it is actively maintained and widely used, but pyLD is a good fallback option: [pyLD](https://github.com/digitalbazaar/pyld). There is also a [JSON to JSON-LD transformation component](https://etl.linkedpipes.com/components/t-jsontojsonld) in the [LinkedPipes](https://linkedpipes.com/) ETL suite for linked data, however it is written in Java and meant for UI-based usage.
* Neutral, because workflow has to be adapted if a different input format or RDF serialization is required in the future
* Bad, because prior to context mapping, @type properties have to be injected into the input JSON. This could be solved using type alias (as suggested [here](https://github.com/schemaorg/schemaorg/issues/854)), SHACL validation and type inference script as a fallback for missing type properties. 

### JSON to RDF transformation using YARRRML mapping, [yarrrml-parser](https://github.com/RMLio/yarrrml-parser) and [rmlmapper](https://github.com/RMLio/rmlmapper-java)

In this approach, the transformation from JSON to RDF is controlled via a separate mapping file written in YARRRML, a human-readable YAML-based syntax for defining RML mappings. The YARRRML file is parsed into RML using yarrrml-parser, and the actual RDF is generated using an RML engine such as rmlmapper. 

* Good, because YARRRML, yarrrml-parser and rmlmapper are developed at a research institution and will likely be maintained long-term
* Good, because YARRRML mappings are human-readable and easily understandable, rely on RML and YAML, are widely used
* Neutral, because workflow does not have to be adapted if a different input format (CSV) or RDF serialization (Turtle) is required in the future
* Bad, because multiple components are required for transformation pipeline (YARRRML mapping, parser, RML engine)
* Bad, because YARRRML adds an additional level of abstraction
* Bad, because parent-child relationship in nested arrays cannot be retained with standard YARRRML mappings and existing workarounds only apply to strings (see [this GitHub issue](https://github.com/RMLio/rmlmapper-java/issues/230)), are non-standard (^^ JSONPath operator, see [this GitHub issue](https://github.com/semantifyit/RocketRML/issues/17)) or rely on a library that is not actively maintained ([RocketRML](https://github.com/semantifyit/RocketRML)).

### YAML to RDF transformation using Fix mapping and Librecat [Catmandu](https://github.com/LibreCat/Catmandu)

This approach uses Catmandu to read structured YAML data and apply transformation rules written in the Fix language. Catmandu supports various output formats, including RDF, but it relies on a niche ecosystem and a custom mapping language.

* Neutral, because Catmandu supports many input formats 
* Neutral, because workflow does not have to be adapted if a different input format (CSV, YAML) or RDF serialization (Turtle) is required in the future
* Bad, because Catmandu is old and not as actively maintained, depends on collective of developers
* Bad, because Catmandu relies on Fix language for mappings. Fix is not widely used and not as readable

## More Information

* JSON-LD specifications: https://json-ld.org/spec/
* W3C best practices for JSON-LD APIs: https://w3c.github.io/json-ld-bp/
* List of RDF converters: https://www.w3.org/wiki/ConverterToRdf
* Client-side SPARQL queries: https://comunica.dev/
* LinkedPipes JSON to JSON-LD transformation component [source code](https://github.com/linkedpipes/etl/blob/eb266fcdb4868130c97bdc784df75628801f5177/plugins/t-jsonToJsonLd/src/main/java/com/linkedpipes/plugin/transformer/jsontojsonld/JsonToJsonLd.java) and [documentation](https://etl.linkedpipes.com/components/t-jsontojsonld).