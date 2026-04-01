from pathlib import Path


EDITIONS_PATH = Path(__file__).parent.parent / "fixtures" / "goodreads_841320_editions.html"
FEATURED_PATH = Path(__file__).parent.parent / "fixtures" / "goodreads_841320_featured.html"

EXPECTED_READERSTATS = {
	"averageRating": 3.77,
	"ratingsCount": 362177,
	"ratingsCountDist": [12578, 31495, 88802, 121547, 107755],
	"textReviewsCount": 25924,
	"featuredUrl": "https://www.goodreads.com/book/show/14942.Mrs_Dalloway",
}

EXPECTED_READERSTATS_EMPTY = {
	"averageRating": None,
	"ratingsCount": None,
	"ratingsCountDist": None,
	"textReviewsCount": None,
	"featuredUrl": None,
}

GOODREADS_HYDRATION_DATA = {
	"props": {
		"pageProps": {
			"apolloState": {
				"Work:kca://work/amzn1.gr.work.v1.BWoHuYZ0fpkTyScWKa57Lw": {
					"stats": {
						"averageRating": 3.77,
						"ratingsCount": 362177,
						"ratingsCountDist": [12578, 31495, 88802, 121547, 107755],
						"textReviewsCount": 25924,
					}
				}
			}
		}
	}
}
