from casanova import namedrecord
from src.constants import DATA_DIR

REVIEW_DTYPES = {
    "link_id": "VARCHAR",
    "url": "VARCHAR",
    "date_published": "DATE",
    "facebook_comment": "INTEGER",
    "facebook_like": "INTEGER",
    "facebook_share": "INTEGER",
    "pinterest_share": "INTEGER",
    "twitter_share": "INTEGER",
    "tiktok_share": "INTEGER",
    "tiktok_comment": "INTEGER",
    "reddit_engagement": "INTEGER",
    "youtube_watch": "INTEGER",
    "youtube_comment": "INTEGER",
    "youtube_like": "INTEGER",
    "youtube_favorite": "INTEGER",
    "youtube_subscribe": "INTEGER",
}


REVIEW_FIELDNAMES = list(REVIEW_DTYPES.keys())


FlatReview = namedrecord(
    "FlatReview",
    REVIEW_FIELDNAMES,
    plural=["keywords", "hashtags"],
)


REVIEW_CSV = DATA_DIR.joinpath("reviews.csv").resolve()
