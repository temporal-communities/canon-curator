import json
from pathlib import Path

WIKIPEDIA_DBLIST_PATH = Path(__file__).parent.parent / "testdata" / "wikipedia_dblist.txt"
WIKIPEDIA_DBLIST = WIKIPEDIA_DBLIST_PATH.read_text(encoding="utf-8")

Q17892_PATH = Path(__file__).parent.parent / "testdata" / "Q17892.json"
with open(Q17892_PATH, "r", encoding="utf-8") as f: 
	ENTITY_Q17892 = json.load(f)
Q1018197_PATH = Path(__file__).parent.parent / "testdata" / "Q1018197.json"
with open(Q1018197_PATH, "r", encoding="utf-8") as f: 
	ENTITY_Q1018197 = json.load(f)
Q47008571_PATH = Path(__file__).parent.parent / "testdata" / "Q47008571.json"
with open(Q47008571_PATH, "r", encoding="utf-8") as f:
	ENTITY_Q47008571 = json.load(f)


CLAIM_BIRTH_PLACE_ERESOS = {
		"mainsnak": {
			"snaktype": "value",
			"property": "P19",
			"datatype": "wikibase-item",
			"datavalue": {
				"value": {"entity-type": "item", "numeric-id": 1018197},
				"type": "wikibase-entityid",
			},
		},
		"type": "statement",
		"id": "Q17892$D5A7BA00-90E6-4C39-97DA-DC06800E7F65",
		"rank": "normal",
		"references": [
			{
				"snaks": {
					"P248": [
						{
							"snaktype": "value",
							"property": "P248",
							"datatype": "wikibase-item",
							"datavalue": {
								"value": {"entity-type": "item", "numeric-id": 65921422},
								"type": "wikibase-entityid",
							},
						}
					],
					"P3365": [
						{
							"snaktype": "value",
							"property": "P3365",
							"datatype": "external-id",
							"datavalue": {"value": "saffo", "type": "string"},
						}
					],
					"P1810": [
						{
							"snaktype": "value",
							"property": "P1810",
							"datatype": "string",
							"datavalue": {"value": "Saffo", "type": "string"},
						}
					],
					"P813": [
						{
							"snaktype": "value",
							"property": "P813",
							"datatype": "time",
							"datavalue": {
								"value": {
									"time": "+00000002021-01-25T00:00:00Z",
									"precision": 11,
									"after": 0,
									"before": 0,
									"timezone": 0,
									"calendarmodel": "http://www.wikidata.org/entity/Q1985727",
								},
								"type": "time",
							},
						}
					],
				},
				"snaks-order": ["P248", "P3365", "P1810", "P813"],
				"hash": "424742ebe03951785dc139cf15ae2978ea2bda9f",
			}
		],
	}

CLAIM_BIRTH_PLACE_LESBOS = {
		"mainsnak": {
			"snaktype": "value",
			"property": "P19",
			"datatype": "wikibase-item",
			"datavalue": {
				"value": {"entity-type": "item", "numeric-id": 128087},
				"type": "wikibase-entityid",
			},
		},
		"type": "statement",
		"id": "Q17892$51A17535-857F-4CC9-BA07-BC8476BE1BD8",
		"rank": "preferred",
		"qualifiers": {
			"P7452": [
				{
					"snaktype": "value",
					"property": "P7452",
					"datatype": "wikibase-item",
					"datavalue": {
						"value": {"entity-type": "item", "numeric-id": 111606173},
						"type": "wikibase-entityid",
					},
					"hash": "c3c8b44a80e7854d73df5d4e884f3e890bf765d0",
				}
			]
		},
		"qualifiers-order": ["P7452"],
		"references": [
			{
				"snaks": {
					"P957": [
						{
							"snaktype": "value",
							"property": "P957",
							"datatype": "external-id",
							"datavalue": {"value": "0-19-924017-5", "type": "string"},
						}
					],
					"P1476": [
						{
							"snaktype": "value",
							"property": "P1476",
							"datatype": "monolingualtext",
							"datavalue": {
								"value": {
									"text": "Greek Lyric Poetry: A Commentary on Selected Larger Pieces",
									"language": "en",
								},
								"type": "monolingualtext",
							},
						}
					],
				},
				"snaks-order": ["P957", "P1476"],
				"hash": "182e46eec1d5950e13854869fda6a74cf3d33f7c",
			},
			{
				"snaks": {
					"P248": [
						{
							"snaktype": "value",
							"property": "P248",
							"datatype": "wikibase-item",
							"datavalue": {
								"value": {"entity-type": "item", "numeric-id": 731361},
								"type": "wikibase-entityid",
							},
						}
					],
					"P4223": [
						{
							"snaktype": "value",
							"property": "P4223",
							"datatype": "external-id",
							"datavalue": {"value": "saffo", "type": "string"},
						}
					],
					"P1810": [
						{
							"snaktype": "value",
							"property": "P1810",
							"datatype": "string",
							"datavalue": {"value": "SAFFO", "type": "string"},
						}
					],
					"P813": [
						{
							"snaktype": "value",
							"property": "P813",
							"datatype": "time",
							"datavalue": {
								"value": {
									"time": "+00000002021-01-25T00:00:00Z",
									"precision": 11,
									"after": 0,
									"before": 0,
									"timezone": 0,
									"calendarmodel": "http://www.wikidata.org/entity/Q1985727",
								},
								"type": "time",
							},
						}
					],
				},
				"snaks-order": ["P248", "P4223", "P1810", "P813"],
				"hash": "e5b75c984b21a1bc9b133ffb067d735c60469259",
			},
			{
				"snaks": {
					"P248": [
						{
							"snaktype": "value",
							"property": "P248",
							"datatype": "wikibase-item",
							"datavalue": {
								"value": {"entity-type": "item", "numeric-id": 1768199},
								"type": "wikibase-entityid",
							},
						}
					],
					"P2924": [
						{
							"snaktype": "value",
							"property": "P2924",
							"datatype": "external-id",
							"datavalue": {"value": "3534749", "type": "string"},
						}
					],
					"P1810": [
						{
							"snaktype": "value",
							"property": "P1810",
							"datatype": "string",
							"datavalue": {"value": "САПФО́", "type": "string"},
						}
					],
					"P813": [
						{
							"snaktype": "value",
							"property": "P813",
							"datatype": "time",
							"datavalue": {
								"value": {
									"time": "+00000002021-01-25T00:00:00Z",
									"precision": 11,
									"after": 0,
									"before": 0,
									"timezone": 0,
									"calendarmodel": "http://www.wikidata.org/entity/Q1985727",
								},
								"type": "time",
							},
						}
					],
				},
				"snaks-order": ["P248", "P2924", "P1810", "P813"],
				"hash": "ad2c80dc1afd901066aee94f1dd6be02bc7891e1",
			},
			{
				"snaks": {
					"P248": [
						{
							"snaktype": "value",
							"property": "P248",
							"datatype": "wikibase-item",
							"datavalue": {
								"value": {"entity-type": "item", "numeric-id": 5375741},
								"type": "wikibase-entityid",
							},
						}
					],
					"P1417": [
						{
							"snaktype": "value",
							"property": "P1417",
							"datatype": "external-id",
							"datavalue": {
								"value": "biography/Sappho-Greek-poet",
								"type": "string",
							},
						}
					],
					"P1810": [
						{
							"snaktype": "value",
							"property": "P1810",
							"datatype": "string",
							"datavalue": {"value": "Sappho", "type": "string"},
						}
					],
					"P813": [
						{
							"snaktype": "value",
							"property": "P813",
							"datatype": "time",
							"datavalue": {
								"value": {
									"time": "+00000002021-01-25T00:00:00Z",
									"precision": 11,
									"after": 0,
									"before": 0,
									"timezone": 0,
									"calendarmodel": "http://www.wikidata.org/entity/Q1985727",
								},
								"type": "time",
							},
						}
					],
				},
				"snaks-order": ["P248", "P1417", "P1810", "P813"],
				"hash": "fec3181138965b64bed52f00efbe006128d8aa68",
			},
		],
	}

CLAIM_BIRTH_PLACE_MYTILENE = {
		"mainsnak": {
			"snaktype": "value",
			"property": "P19",
			"datatype": "wikibase-item",
			"datavalue": {
				"value": {"entity-type": "item", "numeric-id": 42295059},
				"type": "wikibase-entityid",
			},
		},
		"type": "statement",
		"id": "Q17892$AFBBEE43-9929-4647-9E99-315216B32D90",
		"rank": "normal",
	}

CLAIM_COORDINATES = {
		"mainsnak": {
			"snaktype": "value",
			"property": "P625",
			"datatype": "globe-coordinate",
			"datavalue": {
				"value": {
					"latitude": 39.169897,
					"longitude": 25.933797,
					"altitude": None,
					"globe": "http://www.wikidata.org/entity/Q2",
					"precision": 1e-06,
				},
				"type": "globecoordinate",
			},
		},
		"type": "statement",
		"id": "q1018197$0E3D30CD-AF3D-4A68-8B9F-14BD4CE8B91E",
		"rank": "normal",
	}

SAMPLE_CLAIMS = [
	CLAIM_BIRTH_PLACE_ERESOS,
	CLAIM_BIRTH_PLACE_LESBOS,
	CLAIM_BIRTH_PLACE_MYTILENE,
	CLAIM_COORDINATES,
]


COORDINATES_CLAIMS = ENTITY_Q1018197["entities"]["Q1018197"]["claims"]["P625"]

BIRTH_PLACE_CLAIMS = ENTITY_Q17892["entities"]["Q17892"]["claims"]["P19"]


EXPECTED_REFERENCES_ERESOS = [
	{
		"source": "https://www.wikidata.org/entity/Q65921422",
		"qualifiers": {
			"P3365": "saffo",
			"P1810": "Saffo",
			"P813": "+00000002021-01-25T00:00:00Z",
		},
	}
]

EXPECTED_REFERENCES_LESBOS = [
	{
		"source": None, 
		"qualifiers": {
			"P957": "0-19-924017-5",
			"P1476": "Greek Lyric Poetry: A Commentary on Selected Larger Pieces",
		},
	},
	{
		"source": "https://www.wikidata.org/entity/Q731361",
		"qualifiers": {
			"P4223": "saffo",
			"P1810": "SAFFO",
			"P813": "+00000002021-01-25T00:00:00Z",
		},
	},
	{
		"source": "https://www.wikidata.org/entity/Q1768199",
		"qualifiers": {
			"P2924": "3534749",
			"P1810": "САПФО́",
			"P813": "+00000002021-01-25T00:00:00Z",
		},
	},
	{
		"source": "https://www.wikidata.org/entity/Q5375741",
		"qualifiers": {
			"P1417": "biography/Sappho-Greek-poet",
			"P1810": "Sappho",
			"P813": "+00000002021-01-25T00:00:00Z",
		},
	},
]

EXPECTED_REFERENCES_EMPTY = []

EXPECTED_REFERENCES = [
	EXPECTED_REFERENCES_ERESOS,
	EXPECTED_REFERENCES_LESBOS,
	EXPECTED_REFERENCES_EMPTY,
]

EXPECTED_DATAVALUE_ERESOS = {"type": "item", "label": None, "entity_id": "Q1018197"}
EXPECTED_DATAVALUE_LESBOS = {"type": "item", "label": None, "entity_id": "Q128087"}
EXPECTED_DATAVALUE_MYTILENE = {"type": "item", "label": None, "entity_id": "Q42295059"}
EXPECTED_DATAVALUE_COORDINATES = {"type": "coordinates", "latitude": 39.169897, "longitude": 25.933797}


EXPECTED_TARGET_ERESOS = {"type": "item", "label": "Eresos", "entity_id": "Q1018197"}
EXPECTED_TARGET_LESBOS = {"type": "item", "label": "Lesbos", "entity_id": "Q128087"}
EXPECTED_TARGET_MYTILENE = {"type": "item", "label": "Mytilene", "entity_id": "Q42295059"}
EXPECTED_TARGET_COORDINATES = {"type": "coordinates", "latitude": 39.169897, "longitude": 25.933797}

EXPECTED_TARGETS_BIRTH_PLACE = [
	EXPECTED_TARGET_ERESOS,
	EXPECTED_TARGET_LESBOS,
	EXPECTED_TARGET_MYTILENE,
]

EXPECTED_TARGETS = [
	EXPECTED_TARGET_ERESOS,
	EXPECTED_TARGET_LESBOS,
	EXPECTED_TARGET_MYTILENE,
	EXPECTED_TARGET_COORDINATES,
]

EXPECTED_EMPTY_RESULT = {"entity": "Q17892", "property": "P20", "claims": []}

EXPECTED_FETCH_PROPERTY_RESULT_BIRTH_PLACE = {
	"entity": "Q17892",
	"property": "P19",
	"claims": [
		{
			"type": "item",
			"label": "Eresos",
			"entity_id": "Q1018197",
			"sources": [
				{
					"source": "https://www.wikidata.org/entity/Q65921422",
					"qualifiers": {
						"P3365": "saffo",
						"P1810": "Saffo",
						"P813": "+00000002021-01-25T00:00:00Z",
					},
				}
			],
			"rank": "normal",
		},
		{
			"type": "item",
			"label": "Lesbos",
			"entity_id": "Q128087",
			"sources": [
				{
					"source": None, 
					"qualifiers": {
						"P957": "0-19-924017-5",
						"P1476": "Greek Lyric Poetry: A Commentary on Selected Larger Pieces",
					},
				},
				{
					"source": "https://www.wikidata.org/entity/Q731361",
					"qualifiers": {
						"P4223": "saffo",
						"P1810": "SAFFO",
						"P813": "+00000002021-01-25T00:00:00Z",
					},
				},
				{
					"source": "https://www.wikidata.org/entity/Q1768199",
					"qualifiers": {
						"P2924": "3534749",
						"P1810": "САПФО́",
						"P813": "+00000002021-01-25T00:00:00Z",
					},
				},
				{
					"source": "https://www.wikidata.org/entity/Q5375741",
					"qualifiers": {
						"P1417": "biography/Sappho-Greek-poet",
						"P1810": "Sappho",
						"P813": "+00000002021-01-25T00:00:00Z",
					},
				},
			],
			"rank": "preferred",
		},
		{
			"type": "item",
			"label": "Mytilene",
			"entity_id": "Q42295059",
			"sources": [],
			"rank": "normal",
		},
	],
}

EXPECTED_FETCH_PROPERTY_RESULT_COORDINATES_ERESOS = {
	"entity": "Q1018197",
	"property": "P625",
	"claims": [
		{
			"type": "coordinates",
			"latitude": 39.169897,
			"longitude": 25.933797,
			"sources": [],
			"rank": "normal",
		}
	],
}

EXPECTED_FETCH_PROPERTY_RESULT_COORDINATES_LESBOS = {
	"entity": "Q128087",
	"property": "P625",
	"claims": [
		{
			"type": "coordinates",
			"latitude": 39.21,
			"longitude": 26.28,
			"sources": [],
			"rank": "preferred",
		}
	],
}

EXPECTED_FETCH_PROPERTY_RESULT_COORDINATES_MYTILENE = {
	"entity": "Q42295059",
	"property": "P625",
	"claims": [
		{
			"type": "coordinates",
			"latitude": 39.1114,
			"longitude": 26.5621,
			"sources": [],
			"rank": "normal",
		}
	],
}

EXPECTED_FETCH_PROPERTY_RESULT_COORDINATES = EXPECTED_FETCH_PROPERTY_RESULT_COORDINATES_ERESOS

EXPECTED_FETCH_PROPERTY_RESULTS = [
	EXPECTED_FETCH_PROPERTY_RESULT_BIRTH_PLACE,
	EXPECTED_FETCH_PROPERTY_RESULT_COORDINATES_ERESOS,
]

EXPECTED_FETCH_PROPERTY_RESULT_GENDER = {
	"entity": "Q40909",
	"property": "P21",
	"claims": [
		{
			"type": "item",
			"label": "female",
			"entity_id": "Q6581072",
			"sources": [
				{
					"source": "https://www.wikidata.org/entity/Q2494649",
					"qualifiers": {"P813": "+00000002017-11-16T00:00:00Z", "P245": "500330927"},
				}
			],
			"rank": "normal",
		}
	],
}


EXPECTED_WIKIPEDIA_SITES = {
    "aawiki", "abwiki", "acewiki", "adywiki", "afwiki", "akwiki",
    "alswiki", "altwiki", "amiwiki", "amwiki", "angwiki", "annwiki",
    "anpwiki", "anwiki", "arcwiki", "arwiki", "arywiki", "arzwiki",
    "astwiki", "aswiki", "atjwiki", "avkwiki", "avwiki", "awawiki",
    "aywiki", "azbwiki", "azwiki", "banwiki", "barwiki", "bat_smgwiki",
    "bawiki", "bbcwiki", "bclwiki", "bdrwiki", "be_x_oldwiki", "bewiki",
    "bewwiki", "bgwiki", "bhwiki", "biwiki", "bjnwiki", "blkwiki",
    "bmwiki", "bnwiki", "bolwiki", "bowiki", "bpywiki", "brwiki",
    "bswiki", "btmwiki", "bugwiki", "bxrwiki", "cawiki", "cbk_zamwiki",
    "cdowiki", "cebwiki", "cewiki", "chowiki", "chrwiki", "chwiki",
    "chywiki", "ckbwiki", "cowiki", "crhwiki", "crwiki", "csbwiki",
    "cswiki", "cuwiki", "cvwiki", "cywiki", "dagwiki", "dawiki",
    "dewiki", "dgawiki", "dinwiki", "diqwiki", "dsbwiki", "dtpwiki",
    "dtywiki", "dvwiki", "dzwiki", "eewiki", "elwiki", "emlwiki",
    "enwiki", "eowiki", "eswiki", "etwiki", "euwiki", "extwiki",
    "fatwiki", "fawiki", "ffwiki", "fiu_vrowiki", "fiwiki", "fjwiki",
    "fonwiki", "fowiki", "frpwiki", "frrwiki", "frwiki", "furwiki",
    "fywiki", "gagwiki", "ganwiki", "gawiki", "gcrwiki", "gdwiki",
    "glkwiki", "glwiki", "gnwiki", "gomwiki", "gorwiki", "gotwiki",
    "gpewiki", "gucwiki", "gurwiki", "guwiki", "guwwiki", "gvwiki",
    "hakwiki", "hawiki", "hawwiki", "hewiki", "hifwiki", "hiwiki",
    "howiki", "hrwiki", "hsbwiki", "htwiki", "huwiki", "hywiki",
    "hywwiki", "hzwiki", "iawiki", "ibawiki", "idwiki", "iewiki",
    "iglwiki", "igwiki", "iiwiki", "ikwiki", "ilowiki", "inhwiki",
    "iowiki", "isvwiki", "iswiki", "itwiki", "iuwiki", "jamwiki",
    "jawiki", "jbowiki", "jvwiki", "kaawiki", "kabwiki", "kaiwiki",
    "kajwiki", "kawiki", "kbdwiki", "kbpwiki", "kcgwiki", "kgewiki",
    "kgwiki", "kiwiki", "kjwiki", "kkwiki", "klwiki", "kmwiki",
    "kncwiki", "knwiki", "koiwiki", "kowiki", "krcwiki", "krwiki",
    "kshwiki", "kswiki", "kuswiki", "kuwiki", "kvwiki", "kwwiki",
    "kywiki", "ladwiki", "lawiki", "lbewiki", "lbwiki", "lezwiki",
    "lfnwiki", "lgwiki", "lijwiki", "liwiki", "lldwiki", "lmowiki",
    "lnwiki", "lowiki", "lrcwiki", "ltgwiki", "ltwiki", "lvwiki",
    "madwiki", "magwiki", "maiwiki", "map_bmswiki", "mdfwiki", "mgwiki",
    "mhrwiki", "mhwiki", "minwiki", "miwiki", "mkwiki", "mlwiki",
    "mniwiki", "mnwiki", "mnwwiki", "moswiki", "mrjwiki", "mrwiki",
    "mswiki", "mtwiki", "muswiki", "mwlwiki", "myvwiki", "mywiki",
    "mznwiki", "nahwiki", "napwiki", "nawiki", "nds_nlwiki", "ndswiki",
    "newiki", "newwiki", "ngwiki", "niawiki", "nlwiki", "nnwiki",
    "novwiki", "nowiki", "nqowiki", "nrmwiki", "nrwiki", "nsowiki",
    "nupwiki", "nvwiki", "nywiki", "ocwiki", "olowiki", "omwiki",
    "orwiki", "oswiki", "pagwiki", "pamwiki", "papwiki", "pawiki",
    "pcdwiki", "pcmwiki", "pdcwiki", "pflwiki", "pihwiki", "piwiki",
    "plwiki", "pmswiki", "pnbwiki", "pntwiki", "pplwiki", "pswiki",
    "ptwiki", "pwnwiki", "quwiki", "rkiwiki", "rmwiki", "rmywiki",
    "rnwiki", "roa_rupwiki", "roa_tarawiki", "rowiki", "rskwiki", "ruewiki",
    "ruwiki", "rwwiki", "sahwiki", "satwiki", "sawiki", "scnwiki",
    "scowiki", "scwiki", "sdwiki", "sewiki", "sgwiki", "shiwiki",
    "shnwiki", "shwiki", "simplewiki", "siwiki", "skrwiki", "skwiki",
    "slwiki", "smnwiki", "smwiki", "snwiki", "sowiki", "sqwiki",
    "srnwiki", "srwiki", "sswiki", "stqwiki", "stwiki", "suwiki",
    "svwiki", "swwiki", "sylwiki", "szlwiki", "szywiki", "tawiki",
    "taywiki", "tcywiki", "tddwiki", "tenwiki", "test2wiki", "testwiki",
    "tetwiki", "tewiki", "tgwiki", "thwiki", "tigwiki", "tiwiki",
    "tkwiki", "tlwiki", "tlywiki", "tnwiki", "tokwiki", "towiki",
    "tpiwiki", "trvwiki", "trwiki", "tswiki", "ttwiki", "tumwiki",
    "twwiki", "tyvwiki", "tywiki", "udmwiki", "ugwiki", "ukwiki",
    "urwiki", "uzwiki", "vecwiki", "vepwiki", "vewiki", "viwiki",
    "vlswiki", "vowiki", "warwiki", "wawiki", "wowiki", "wuuwiki",
    "xalwiki", "xhwiki", "xmfwiki", "yiwiki", "yowiki", "zawiki",
    "zeawiki", "zghwiki", "zh_classicalwiki", "zh_min_nanwiki", "zh_yuewiki", "zhwiki",
    "zuwiki",
}