import json
from pathlib import Path
from typing import Dict, List

from defacto_enrichment.flatten import flatten
from src.constants import TEMP_APPEARANCES, TEMP_FACT_CHECKS, TEMP_SHARED_CONTENT


def flattener(file: Path) -> None:
    # Get data from in-file
    with open(file, "r") as f:
        loaded_json = json.load(f)
        if isinstance(loaded_json, List):
            data = loaded_json
        elif isinstance(loaded_json, Dict) and loaded_json.get("data"):
            data = loaded_json["data"]
        else:
            return

        # Write in-file data to temporary CSV files
        flatten(
            appearance_file=TEMP_APPEARANCES,
            fact_check_file=TEMP_FACT_CHECKS,
            content_file=TEMP_SHARED_CONTENT,
            data=data,
        )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    args = parser.parse_args()
    flattener(args.file)
