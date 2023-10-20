import csv
import json
import os
import sys

import casanova
from minall import process_new_set
from rich import print
from rich.panel import Panel
from src.appearance.build_appearance import AppearanceBuilder
from src.appearance.constants import APPEARANCE_CSV
from src.constants import CONFIG, DATA_DIR, MINALL_OUTPUT
from src.review.build_review import ReviewBuilder
from src.review.constants import REVIEW_CSV
from src.shared_content.constants import SHARED_CONTENT_CSV


def blockPrinting(func):
    def func_wrapper(stage: str, total: int, *args, **kwargs):
        panel = Panel(
            f"[blue]Phase: {stage}\n[white]Total: {total}",
            title="[bold yellow]Minall enrichment",
        )
        print(panel)
        # block all printing to the console
        sys.stdout = open(os.devnull, "w")
        # call the method in question
        value = func(stage, total, *args, **kwargs)
        # enable all printing to the console
        sys.stdout = sys.__stdout__
        # pass the return value of the method back
        return value

    return func_wrapper


@blockPrinting
def run_minall(stage: str, total: int, **kwargs):
    process_new_set(**kwargs)


def update_metadata(
    review_csv=REVIEW_CSV,
    minall_output_dir=MINALL_OUTPUT,
    config_file=CONFIG,
    appearance_csv=APPEARANCE_CSV,
    shared_content_csv=SHARED_CONTENT_CSV,
):
    enriched_data_index = {}
    # Index the reviews
    with casanova.reader(review_csv) as reader:
        for review_id in reader.cells("link_id"):
            enriched_data_index.update(
                {
                    review_id: {
                        "id": review_id,
                        "claim-review": {"interactionStatistic": []},
                    }
                }
            )

    # Update the reviews' metadata
    total = casanova.count(input_file=review_csv)
    run_minall(
        stage="Fact-checks",
        total=total,
        **{
            "links_file": str(review_csv),
            "output_dir": str(minall_output_dir),
            "config_file": str(config_file),
            "buzzsumo_only": True,
        },
    )
    minall_output_dir.joinpath("links.csv").rename(review_csv)

    # Format the review metadata as JSON-LD
    builder = ReviewBuilder()
    with open(review_csv, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            review_id = row["link_id"]
            review_stats = builder(row)
            enriched_data_index[review_id]["claim-review"][
                "interactionStatistic"
            ] = review_stats

    # Update appearances and their associated shared media content
    total = casanova.count(input_file=appearance_csv)
    run_minall(
        stage="Fact-checked claims",
        total=total,
        **{
            "links_file": str(appearance_csv),
            "shared_content_file": str(shared_content_csv),
            "output_dir": str(minall_output_dir),
            "config_file": str(config_file),
        },
    )
    minall_output_dir.joinpath("links.csv").rename(appearance_csv)
    minall_output_dir.joinpath("shared_content.csv").rename(shared_content_csv)

    # Index the shared content
    shared_content_index = {}
    with open(shared_content_csv, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            appearance_url = row["post_url"]
            if not shared_content_index.get(appearance_url):
                shared_content_index.update({appearance_url: []})
            shared_content_index[appearance_url].append(row)

    # Format the appearance metadata as JSON-LD
    builder = AppearanceBuilder(shared_content_index=shared_content_index)
    with open(appearance_csv, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            review_id = row["link_id"]
            appearance_json = builder(row)
            # If the new index already has an array of appearances, append to it
            if (
                enriched_data_index[review_id]["claim-review"]
                .get("itemReviewed", {})
                .get("appearance")
            ):
                enriched_data_index[review_id]["claim-review"]["itemReviewed"][
                    "appearance"
                ].append(appearance_json)
            # Otherwise, update the claim-review and create an appearance array
            else:
                enriched_data_index[review_id]["claim-review"].update(
                    {"itemReviewed": {"appearance": [appearance_json]}}
                )

    # Export data
    final_file = DATA_DIR.joinpath("enriched-urls.json")
    sorted_ids = sorted(list(enriched_data_index.keys()))
    sorted_data = [enriched_data_index[k] for k in sorted_ids]
    with open(final_file, "w") as of:
        json.dump(sorted_data, of, indent=4, ensure_ascii=False)
