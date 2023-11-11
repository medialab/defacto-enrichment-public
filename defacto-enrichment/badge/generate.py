import os
from pathlib import Path

from minet.buzzsumo.client import BuzzSumoAPIClient
from pybadges import badge


def main():
    token = os.environ["BUZZSUMO_TOKEN"]

    client = BuzzSumoAPIClient(token)
    try:
        calls = client.limit()
    except Exception as e:
        raise e

    kwargs = {
        "left_text": "De Facto's remaining Buzzsumo API calls",
        "right_text": str(calls),
        "right_color": "blue",
    }

    s = badge(**kwargs)
    # s is a string that contains the badge data as an svg image.

    with open(Path(__file__).parent.joinpath("badge.svg"), "w") as f:
        f.writelines(s)


if __name__ == "__main__":
    main()
