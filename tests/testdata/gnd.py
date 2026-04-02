from pathlib import Path

GENDER_VOCAB_PATH = Path(__file__).parent.parent / "testdata" / "gnd_gender_vocab.rdf"
GENDER_VOCAB = GENDER_VOCAB_PATH.read_text()

GEOLABEL_VOCAB_PATH = Path(__file__).parent.parent / "testdata" / "gnd_geolabel_vocab.rdf"
GEOLABEL_VOCAB = GEOLABEL_VOCAB_PATH.read_text()

SAMPLE_ENTRY_GENDER = {
	"request_url": "https://lobid.org/gnd/118635174.json",
	"id": "https://d-nb.info/standards/vocab/gnd/gender#female",
	"label": "weiblich",
}

SAMPLE_ENTRY_GEOCODE = {
	"request_url": "https://lobid.org/gnd/4316776-7.json",
	"id": "https://d-nb.info/standards/vocab/gnd/geographic-area-code#XA-GB",
	"label": "Großbritannien",
}

SAMPLE_ENTRY_GEOMETRY = {
	"request_url": "https://lobid.org/gnd/4022153-2.json",
	"type": "Point",
	"asWKT": ["Point ( -002.695310 +054.758440 )"],
}

EXPECTED_FETCH_PROPERTY_RETURN_GENDER = {
	"resource": "118635174",
	"property": "gender",
	"entries": [
		{
			"type": "resource",
			"uri": "https://d-nb.info/standards/vocab/gnd/gender#female",
			"label": "weiblich",
			"request_url": "https://lobid.org/gnd/118635174.json",
		}
	],
}

EXPECTED_FETCH_PROPERTY_RETURN_GEOCODE = {
	"resource": "4316776-7",
	"property": "geographicAreaCode",
	"entries": [
		{
			"type": "resource",
			"uri": "https://d-nb.info/standards/vocab/gnd/geographic-area-code#XA-GB",
			"label": "Großbritannien",
			"request_url": "https://lobid.org/gnd/4316776-7.json",
		}
	],
}

EXPECTED_FETCH_PROPERTY_RETURN_GEOMETRY = {
	"resource": "4022153-2",
	"property": "hasGeometry",
	"entries": [
		{
			"type": "coordinates",
			"latitude": 54.75844,
			"longitude": -2.69531,
			"request_url": "https://lobid.org/gnd/4022153-2.json",
		}
	],
}

EXPECTED_VALUES_GENDER = {
	"type": "resource",
	"uri": "https://d-nb.info/standards/vocab/gnd/gender#female",
	"label": "weiblich",
	"request_url": "https://lobid.org/gnd/118635174.json",
}

EXPECTED_VALUES_GEOCODE = {
	"type": "resource",
	"uri": "https://d-nb.info/standards/vocab/gnd/geographic-area-code#XA-GB",
	"label": "Großbritannien",
	"request_url": "https://lobid.org/gnd/4316776-7.json",
}

EXPECTED_VALUES_GEOMETRY = {
	"type": "coordinates",
	"latitude": 54.75844,
	"longitude": -2.69531,
	"request_url": "https://lobid.org/gnd/4022153-2.json",
}

SAMPLE_CONCEPTS_GENDER = [
	"https://d-nb.info/standards/vocab/gnd/gender#male",
	"https://d-nb.info/standards/vocab/gnd/gender#female",
	"https://d-nb.info/standards/vocab/gnd/gender#notKnown",
]

EXPECTED_STATEMENTS_MALE = {
	"uri": "https://d-nb.info/standards/vocab/gnd/gender#male",
	"statements": [
		{
			"http://www.w3.org/1999/02/22-rdf-syntax-ns#type": "http://www.w3.org/2004/02/skos/core#Concept"
		},
		{
			"http://www.w3.org/2004/02/skos/core#exactMatch": "http://purl.org/linked-data/sdmx/2009/code#sex-M"
		},
		{
			"http://www.w3.org/2004/02/skos/core#exactMatch": "http://rdvocab.info/termList/gender/1002"
		},
		{"http://www.w3.org/2004/02/skos/core#prefLabel": "Male"},
		{"http://www.w3.org/2004/02/skos/core#prefLabel": "Männlich"},
		{
			"http://www.w3.org/2004/02/skos/core#inScheme": "https://d-nb.info/standards/vocab/gnd/gender#"
		},
	],
}

EXPECTED_STATEMENTS_FEMALE = {
	"uri": "https://d-nb.info/standards/vocab/gnd/gender#female",
	"statements": [
		{
			"http://www.w3.org/1999/02/22-rdf-syntax-ns#type": "http://www.w3.org/2004/02/skos/core#Concept"
		},
		{
			"http://www.w3.org/2004/02/skos/core#exactMatch": "http://purl.org/linked-data/sdmx/2009/code#sex-F"
		},
		{
			"http://www.w3.org/2004/02/skos/core#exactMatch": "http://rdvocab.info/termList/gender/1001"
		},
		{"http://www.w3.org/2004/02/skos/core#prefLabel": "Female"},
		{"http://www.w3.org/2004/02/skos/core#prefLabel": "Weiblich"},
		{
			"http://www.w3.org/2004/02/skos/core#inScheme": "https://d-nb.info/standards/vocab/gnd/gender#"
		},
	],
}

EXPECTED_STATEMENTS_NOTKNOWN = {
	"uri": "https://d-nb.info/standards/vocab/gnd/gender#notKnown",
	"statements": [
		{
			"http://www.w3.org/1999/02/22-rdf-syntax-ns#type": "http://www.w3.org/2004/02/skos/core#Concept"
		},
		{
			"http://www.w3.org/2004/02/skos/core#exactMatch": "http://purl.org/linked-data/sdmx/2009/code#sex-U"
		},
		{
			"http://www.w3.org/2004/02/skos/core#exactMatch": "http://rdvocab.info/termList/gender/1003"
		},
		{"http://www.w3.org/2004/02/skos/core#prefLabel": "Not known"},
		{"http://www.w3.org/2004/02/skos/core#prefLabel": "Unbekannt"},
		{
			"http://www.w3.org/2004/02/skos/core#inScheme": "https://d-nb.info/standards/vocab/gnd/gender#"
		},
	],
}

EXPECTED_STATEMENTS_GEOLABEL_GB = {
	"uri": "https://d-nb.info/standards/vocab/gnd/geographic-area-code#XA-GB",
	"statements": [
		{
			"http://www.w3.org/1999/02/22-rdf-syntax-ns#type": "http://www.w3.org/2004/02/skos/core#Concept"
		},
		{
			"http://www.w3.org/2004/02/skos/core#inScheme": "https://d-nb.info/standards/vocab/gnd/geographic-area-code#"
		},
		{"http://www.w3.org/2000/01/rdf-schema#seeAlso": "http://www.geonames.org/2635167"},
		{"http://www.w3.org/2000/01/rdf-schema#seeAlso": "https://d-nb.info/gnd/4022153-2"},
		{"http://www.w3.org/2004/02/skos/core#prefLabel": "Großbritannien"},
		{"http://www.w3.org/2004/02/skos/core#prefLabel": "Great Britain"},
		{
			"http://www.w3.org/2004/02/skos/core#broader": "https://d-nb.info/standards/vocab/gnd/geographic-area-code#XA"
		},
		{
			"http://www.w3.org/2004/02/skos/core#exactMatch": "http://id.loc.gov/vocabulary/geographicAreas/e-uk"
		},
		{
			"http://www.w3.org/2004/02/skos/core#exactMatch": "http://id.loc.gov/vocabulary/countries/xxk"
		},
		{
			"http://xmlns.com/foaf/0.1/page": "https://de.wikipedia.org/wiki/Vereinigtes_K%C3%B6nigreich"
		},
		{"http://xmlns.com/foaf/0.1/page": "https://en.wikipedia.org/wiki/United_Kingdom"},
	],
}
