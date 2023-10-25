import csv
import json
from contextlib import contextmanager
from pathlib import Path

import casanova
import click
import duckdb
from minall.links.links_table import LINKS_FIELDNAMES, LinksTable
from minall.shared_content.shared_content_table import (
    SHARED_CONTENT_FIELDNAMES,
    SharedContentTable,
)
from rich.progress import Progress
from src.appearance.build_appearance import AppearanceBuilder
from src.appearance.flatten_appearance import AppearanceFlattener
from src.shared_content.flatten_shared_content import SharedContentFlattener


@click.group()
def cli():
    pass


@cli.command()
@click.option("--infile")
@click.option("--outdir")
def rename(infile, outdir):
    source = Path(infile)
    dest_dir = Path(outdir)
    dest_dir.mkdir(exist_ok=True)
    new_name = int(round(Path.stat(source).st_mtime, 0))
    destination = dest_dir.joinpath(f"{new_name}-no-commit.json")
    destination.write_text(source.read_text())


@cli.command()
@click.argument("commited-files")
@click.argument("temp-dir")
def compile(commited_files, temp_dir):
    db_connection = duckdb.connect(":memory:")
    appearances_table = LinksTable(connection=db_connection)
    shared_content_table = SharedContentTable(connection=db_connection)
    sorted_files = sorted(list(Path(commited_files).iterdir()))
    outdir = Path(temp_dir)
    outdir.mkdir(exist_ok=True)
    scfp = outdir.joinpath("shared_content.csv")
    afp = outdir.joinpath("appearances.csv")

    with Progress() as progress:
        t = progress.add_task(description="Coalesce data", total=len(sorted_files))
        for file in sorted_files:
            # Open this commit's JSON and write new CSV out-files
            with open(file) as f, writers(shared_content=scfp, appearances=afp) as w:
                shared_content_writer, claims_writer = w
                claims = json.load(f)
                for claim in claims:
                    process_claim(
                        claim=claim,
                        claims_writer=claims_writer,
                        shared_content_writer=shared_content_writer,
                    )

            # Coalesce the commit's flattened data in the SQL database
            appearances_table.insert(infile=afp)
            shared_content_table.insert(infile=scfp)
            progress.advance(t)

    duckdb.table(
        table_name=shared_content_table.table_name, connection=db_connection
    ).write_csv(
        str(scfp), header=True
    )  # type: ignore
    duckdb.table(
        table_name=appearances_table.table_name, connection=db_connection
    ).write_csv(
        str(afp), header=True
    )  # type: ignore

    output = build_json(appearances=afp, shared_content=scfp)

    with open(outdir.joinpath("enriched-urls.json"), "w") as f:
        json.dump(output, f, indent=4)


def build_json(appearances: Path, shared_content: Path) -> list:
    enriched_data_index = {}
    with casanova.reader(appearances) as reader:
        for review_id in reader.cells("link_id"):
            enriched_data_index.update(
                {
                    review_id: {
                        "id": review_id,
                        "claim-review": {},
                    }
                }
            )
    shared_content_index = {}
    with open(shared_content) as f:
        reader = csv.DictReader(f)
        for row in reader:
            appearance_url = row["post_url"]
            if not shared_content_index.get(appearance_url):
                shared_content_index.update({appearance_url: []})
            shared_content_index[appearance_url].append(row)

    builder = AppearanceBuilder(shared_content_index=shared_content_index)
    with open(appearances) as f:
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

    sorted_ids = sorted(list(enriched_data_index.keys()))
    sorted_data = [enriched_data_index[k] for k in sorted_ids]
    return sorted_data


@contextmanager
def writers(shared_content: Path, appearances: Path):
    with open(shared_content, "w") as scf, open(appearances, "w") as af:
        shared_content_writer = csv.DictWriter(scf, SHARED_CONTENT_FIELDNAMES)
        shared_content_writer.writeheader()
        appearance_writer = csv.DictWriter(af, LINKS_FIELDNAMES)
        appearance_writer.writeheader()
        yield shared_content_writer, appearance_writer


def process_claim(
    claim: dict, claims_writer: csv.DictWriter, shared_content_writer: csv.DictWriter
):
    # Get the unique identifier for the review
    review_id = claim["id"]
    review_id.strip()
    claim_review = claim.get("claim-review")
    if not claim_review:
        return

    # Get the item(s) reviewed
    appearance = claim_review.get("itemReviewed", {}).get("appearance")

    # If the appearance has a URL, parse it
    if isinstance(appearance, dict):
        parse_appearances(
            appearance=appearance,
            appearance_writer=claims_writer,
            shared_content_writer=shared_content_writer,
            review_id=review_id,
        )


def parse_appearances(
    appearance: dict,
    appearance_writer: csv.DictWriter,
    shared_content_writer: csv.DictWriter,
    review_id: str,
):
    appearance_record = AppearanceFlattener(data=appearance, link_id=review_id)
    shared_content = appearance_record.shared_content
    appearance_url = appearance_record.url

    if appearance_url:
        appearance_writer.writerow(appearance_record().as_csv_dict_row())

        if shared_content:
            for media in shared_content:
                shared_content_record = SharedContentFlattener(
                    data=media, url=appearance_url
                )
                if shared_content_record.content_url:
                    shared_content_writer.writerow(
                        shared_content_record().as_csv_dict_row()
                    )


if __name__ == "__main__":
    cli()
