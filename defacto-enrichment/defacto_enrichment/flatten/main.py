import copy
import csv
from pathlib import Path
from typing import Dict, List

from defacto_enrichment.flatten.context import Writers
from defacto_enrichment.types import Appearance, FactCheck, SharedContent


def normalized_fact_checks(data: List[Dict]) -> List[Dict]:
    normalized_data = copy.deepcopy(data)

    # Normalize the value of claim-review to be a List
    for fact_check in normalized_data:
        claim_review = fact_check.get("claim-review")
        if isinstance(claim_review, str):
            claim_review = []
        elif isinstance(claim_review, Dict):
            claim_review = [claim_review]
        else:
            claim_review = claim_review
        fact_check["claim-review"] = claim_review

        if isinstance(claim_review, List):
            # Normalize the value of appearance in itemReviewed
            for items in claim_review:
                item_reviewed = items.get("itemReviewed")
                if isinstance(item_reviewed, Dict):
                    appearance = item_reviewed.get("appearance")
                    if isinstance(appearance, str):
                        appearance = {"url": appearance.strip()}
                    else:
                        appearance = appearance
                    item_reviewed["appearance"] = appearance

    return normalized_data


def flatten(
    appearance_file: Path, fact_check_file: Path, content_file: Path, data: List[Dict]
):
    with Writers(appearance_file, content_file, fact_check_file) as context:
        appearance_writer, content_writer, fact_check_writer, progress = context
        t = progress.add_task(description="[bold blue]Flatten", total=len(data))
        for fact_check in data:
            fact_check_rating = ""
            progress.advance(t)

            claim_reviews = fact_check.get("claim-review")
            if not claim_reviews:
                continue

            for item_reviewed in claim_reviews:
                fact_check_rating = item_reviewed.get("reviewRating", {}).get(
                    "ratingValue"
                )

                appearance = item_reviewed.get("itemReviewed", {}).get("appearance")

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

            try:
                record = FactCheck.from_json(
                    fact_check_rating=fact_check_rating, item=fact_check
                )
            except Exception as e:
                from pprint import pprint

                pprint(fact_check)
                raise e

            # If no fact-check URL, do not write record to minall-destined CSV file
            if record.clean_url:
                fact_check_writer.writerow(record.as_csv_dict_row())


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
