from casanova import namedrecord
from src.constants import DATA_DIR

SHARED_CONTENT_DTYPES = {
    "post_url": "VARCHAR",
    "type": "VARCHAR",
    "content_url": "VARCHAR",
    "height": "INTEGER",
    "width": "INTEGER",
}

SHARED_CONTENT_FIELDNAMES = list(SHARED_CONTENT_DTYPES.keys())

FlatSharedContent = namedrecord(
    "FlatSharedContent",
    SHARED_CONTENT_FIELDNAMES,
    plural=[],
)


SHARED_CONTENT_CSV = DATA_DIR.joinpath("shared_content.csv").resolve()
