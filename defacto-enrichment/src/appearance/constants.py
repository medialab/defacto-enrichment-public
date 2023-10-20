from casanova import namedrecord
from src.constants import DATA_DIR

APPEARANCE_DTYPES = {
    "link_id": "VARCHAR",
    "url": "VARCHAR",
    "domain": "VARCHAR",
    "type": "VARCHAR",
    "duration": "VARCHAR",
    "identifier": "VARCHAR",
    "date_published": "DATE",
    "date_modified": "DATE",
    "country_of_origin": "VARCHAR",
    "abstract": "VARCHAR",
    "keywords": "VARCHAR",
    "title": "VARCHAR",
    "text": "VARCHAR",
    "hashtags": "VARCHAR",
    "creator_type": "VARCHAR",
    "creator_date_created": "DATE",
    "creator_location_created": "VARCHAR",
    "creator_identifier": "VARCHAR",
    "creator_facebook_follow": "INTEGER",
    "creator_facebook_subscribe": "INTEGER",
    "creator_twitter_follow": "INTEGER",
    "creator_youtube_subscribe": "INTEGER",
    "creator_create_video": "INTEGER",
    "creator_name": "VARCHAR",
    "creator_url": "VARCHAR",
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
    "create_video": "INTEGER",
}


APPEARANCE_FIELDNAMES = list(APPEARANCE_DTYPES.keys())


FlatAppearance = namedrecord(
    "FlatAppearance",
    APPEARANCE_FIELDNAMES,
    plural=["keywords", "hashtags"],
)


APPEARANCE_CSV = DATA_DIR.joinpath("appearances.csv").resolve()
