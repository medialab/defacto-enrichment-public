import csv
from pathlib import Path
from typing import Dict, List

from defacto_enrichment.flatten.context import Writers
from defacto_enrichment.types import Appearance, FactCheck, SharedContent


def flatten(
    appearance_file: Path, fact_check_file: Path, content_file: Path, data: List[Dict]
):
    with Writers(appearance_file, content_file, fact_check_file) as context:
        appearance_writer, content_writer, fact_check_writer, progress = context
        t = progress.add_task(description="[bold blue]Flatten", total=len(data))
        for fact_check in data:
            progress.advance(t)

            claim_review = fact_check.get("claim-review")
            if not claim_review:
                continue

            fact_check_rating = claim_review.get("reviewRating", {}).get("ratingValue")

            if isinstance(claim_review, Dict):
                try:
                    record = FactCheck.from_json(
                        fact_check_rating=fact_check_rating, item=claim_review
                    )
                except Exception as e:
                    from pprint import pprint

                    pprint(claim_review)
                    raise e
                fact_check_writer.writerow(record.as_csv_dict_row())

            appearance = claim_review.get("itemReviewed", {}).get("appearance")

            if isinstance(appearance, Dict):
                parse_appearance(
                    appearance=appearance,
                    appearance_writer=appearance_writer,
                    shared_content_writer=content_writer,
                    fact_check_rating=fact_check_rating,
                )

            elif isinstance(appearance, List):
                for app in appearance:
                    parse_appearance(
                        appearance=app,
                        appearance_writer=appearance_writer,
                        shared_content_writer=content_writer,
                        fact_check_rating=fact_check_rating,
                    )


def parse_appearance(
    appearance: Dict,
    appearance_writer: csv.DictWriter,
    shared_content_writer: csv.DictWriter,
    fact_check_rating: str,
) -> None:
    appearance_record = Appearance.from_json(
        fact_check_rating=fact_check_rating, item=appearance
    )
    if appearance_record.clean_url and appearance_record.exact_url:
        appearance_writer.writerow(appearance_record.as_csv_dict_row())

        shared_content = appearance.get("sharedContent")
        if shared_content:
            for item in shared_content:
                shared_content_record = SharedContent.from_json(
                    item=item, post_url=appearance_record.exact_url
                )
                shared_content_writer.writerow(shared_content_record.as_csv_dict_row())
