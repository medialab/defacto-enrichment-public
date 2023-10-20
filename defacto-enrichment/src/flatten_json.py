import csv
from contextlib import contextmanager

from minall.utils import progress_bar
from src.appearance.constants import APPEARANCE_CSV, APPEARANCE_FIELDNAMES
from src.appearance.flatten_appearance import AppearanceFlattener
from src.review.constants import REVIEW_CSV, REVIEW_FIELDNAMES
from src.review.flatten_review import ReviewFlattener
from src.shared_content.constants import SHARED_CONTENT_CSV, SHARED_CONTENT_FIELDNAMES
from src.shared_content.flatten_shared_content import SharedContentFlattener


@contextmanager
def new_claims():
    with open(APPEARANCE_CSV, "w") as f:
        writer = csv.DictWriter(f, APPEARANCE_FIELDNAMES)
        writer.writeheader()
        yield writer


@contextmanager
def new_defacto_reviews():
    with open(REVIEW_CSV, "w") as f:
        writer = csv.DictWriter(f, REVIEW_FIELDNAMES)
        writer.writeheader()
        yield writer


@contextmanager
def new_shared_content():
    with open(SHARED_CONTENT_CSV, "w") as f:
        writer = csv.DictWriter(f, SHARED_CONTENT_FIELDNAMES)
        writer.writeheader()
        yield writer


def flatten_all_the_exported_data(data: list):
    with new_claims() as claims_writer, new_defacto_reviews() as defacto_writer, new_shared_content() as shared_content_writer, progress_bar() as progress:
        t = progress.add_task(description="[bold blue]Flatten", total=len(data))
        for claim in data:
            progress.advance(t)
            # Get the unique identifier for the review
            review_id = claim.get("id")
            review_id.strip()
            claim_review = claim.get("claim-review")

            if not claim_review:
                continue

            # To the review CSV, write the review's existing enrichment metadata
            if isinstance(claim_review, dict):
                record = ReviewFlattener(data=claim_review, link_id=review_id)
                defacto_writer.writerow(record().as_csv_dict_row())

            # Get the item(s) reviewed
            appearance = claim_review.get("itemReviewed", {}).get("appearance")

            # To the appearance CSV, write the item's existing metadata
            if isinstance(appearance, dict):
                parse_appearances(
                    appearance=appearance,
                    appearance_writer=claims_writer,
                    shared_content_writer=shared_content_writer,
                    review_id=review_id,
                )

            elif isinstance(appearance, list):
                for app in appearance:
                    parse_appearances(
                        appearance=app,
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
