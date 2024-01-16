import json
import os
from argparse import ArgumentParser
from pathlib import Path
from typing import Dict, List

import requests
from lxml import etree
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn


def parse_input_data() -> Dict | None:
    parser = ArgumentParser()
    parser.add_argument("--datafile")
    args = parser.parse_args()
    datafile = args.datafile
    if datafile:
        assert Path(datafile).is_file()
        datafile = Path(datafile)

    # If provided with a file, parse it
    if datafile:
        if datafile.suffix == ".json":
            with open(datafile, "r") as f:
                database_export = json.load(f)
                if isinstance(database_export, List):
                    database_export = {"data": database_export}
                    return database_export
                elif isinstance(database_export, Dict) and database_export.get("data"):
                    return database_export
        elif datafile.suffix == ".xml":
            database_export = rss2json(datafile)
            return database_export

    # Otherwise, export the most recent data
    # from the environment variable's endpoint
    else:
        database_export = get_from_endpoint_data()
        return database_export


def rss2json(rss_file):
    # Parse the RSS feed file
    root = etree.parse(source=rss_file, parser=etree.XMLParser())

    data = []
    # Iterate over all items (fact-checks) in RSS feed
    for item in root.iterfind(r"channel/item"):
        # Get the fact-check's ID and format it
        guid = item.find("guid").text
        factcheck_id = "/".join(guid.split("."))
        item_json = {"id": factcheck_id}

        # Search for a 'claim-review' in the fact-check item
        claim_review = item.find("{https://schema.org/}review")
        if claim_review is not None:
            json_load = json.loads(claim_review.text)
            item_json.update({"claim-review": json_load})

        # To the data/item array, append the constructed dictionary
        data.append(item_json)
    return {"data": data}


def get_from_endpoint_data(endpoint: str | None = None) -> Dict:
    if not endpoint:
        endpoint = os.environ["ENDPOINT"]
    try:
        with Progress(
            TextColumn("{task.description}"), SpinnerColumn(), TimeElapsedColumn()
        ) as progress:
            progress.add_task("[bold yellow]Retrieving data")
            response = requests.get(endpoint)
            response.raise_for_status()
            response = response.json()
    except Exception as e:
        raise e
    else:
        if isinstance(response, dict) and response.get("data"):
            return response
        else:
            raise KeyError


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("endpoint")
    parser.add_argument("output")
    args = parser.parse_args()
    data = get_from_endpoint_data(args.endpoint)
    with open(args.output, "w") as f:
        print(data)
        json.dump(data, f, indent=4, ensure_ascii=False)
