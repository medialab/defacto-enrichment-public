import json
import os

from src.constants import CONFIG


def load_environment_variables() -> str:
    config = {
        "buzzsumo": {"token": os.environ["BUZZSUMO_TOKEN"]},
        "crowdtangle": {
            "token": os.environ["CROWDTANGLE_TOKEN"],
            "rate_limit": os.environ["CROWDTANGLE_RATE_LIMIT"],
        },
        "youtube": {"key": os.environ["YOUTUBE_KEY_LIST"]},
    }
    with open(CONFIG, "w") as f:
        json.dump(config, f)
    return os.environ["ENDPOINT"]
