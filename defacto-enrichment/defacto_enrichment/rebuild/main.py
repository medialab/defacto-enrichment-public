import csv
from pathlib import Path
from typing import Dict, List

from defacto_enrichment.types import Appearance, FactCheck, SharedContent


def rebuild_appearance_schemas(
    database_export: Dict, appearances_csv: Path, shared_content_csv: Path
) -> Dict:
    index_by_url = {}
    with open(appearances_csv) as f:
        reader = csv.DictReader(f)
        for row in reader:
            record = Appearance.from_csv_dict_row(row)
            index_by_url[record.exact_url] = record.to_json()

    with open(shared_content_csv) as f:
        reader = csv.DictReader(f)
        for row in reader:
            record = SharedContent.from_csv_dict_row(row)
            index_by_url[record.post_url].update({"sharedContent": record.to_json()})

    for fact_check in database_export["data"]:
        items = fact_check.get("claim-review")
        # {"claim-review": [{"itemReviewed": {...}}, {"itemReviewed": {...}}, ...]}
        for item in items:
            if isinstance(item, Dict):
                item_reviewed = item["itemReviewed"]
                appearance_value = item_reviewed.get("appearance")
                if isinstance(appearance_value, Dict):
                    appearance_url = appearance_value.get("url")
                    if appearance_url and appearance_url in index_by_url:
                        appearance_value.update(index_by_url[appearance_url])
                elif isinstance(appearance_value, List):
                    for appearance in appearance_value:
                        appearance_url = appearance.get("url")
                        if appearance_url and appearance_url in index_by_url:
                            appearance.update(index_by_url[appearance_url])

    return database_export


def rebuild_fact_check_schema(database_export: Dict, fact_check_csv: Path) -> Dict:
    fact_check_url_index = {}
    with open(fact_check_csv) as f:
        reader = csv.DictReader(f)
        for row in reader:
            record = FactCheck.from_csv_dict_row(row)
            fact_check_url_index[record.exact_url] = record.to_json()

    for fact_check in database_export["data"]:
        if fact_check and fact_check.get("original-url"):
            fact_check_url = fact_check["original-url"]
            if fact_check_url_index.get(fact_check_url):
                fact_check.update(
                    {"interactionStatistic": fact_check_url_index[fact_check_url]}
                )

    return database_export


def rebuild(
    database_export: Dict,
    appearances_csv: Path,
    shared_content_csv: Path,
    fact_check_csv: Path,
):
    # Mutate the database export with updated appearances
    rebuild_appearance_schemas(
        database_export=database_export,
        appearances_csv=appearances_csv,
        shared_content_csv=shared_content_csv,
    )

    # Mutate the database export with the fact checks
    rebuild_fact_check_schema(
        database_export=database_export, fact_check_csv=fact_check_csv
    )
    return database_export


if __name__ == "__main__":
    import json
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("--export")
    parser.add_argument("--appearances")
    parser.add_argument("--shared-content")
    parser.add_argument("--fact-checks")
    parser.add_argument("--outfile")
    args = parser.parse_args()

    with open(args.export, "r") as f:
        exported_data = json.load(f)

    data = rebuild(
        database_export=exported_data,
        appearances_csv=args.appearances,
        shared_content_csv=args.shared_content,
        fact_check_csv=args.fact_checks,
    )

    with open(args.outfile, "w") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
