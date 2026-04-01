from pathlib import Path

GENDER_VOCAB_PATH = Path(__file__).parent.parent / "testdata" / "gnd_gender_vocab.rdf"
GENDER_VOCAB = GENDER_VOCAB_PATH.read_text()

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
