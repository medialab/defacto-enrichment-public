from pathlib import Path
from pprint import pprint
from statistics import mean
from typing import Dict, Generator, List, Tuple

from defacto_enrichment.flatten.context import Writers
from defacto_enrichment.types import Appearance, FactCheck, SharedContent


def verify_data(data: List[Dict]):
    """
    Verify the schema of the input data matches what's expected.

    ```
    [
        {
            "id": "<FACT CHECK ID>",
            "url": "<FACT CHECK URL>",
            "datePublished": "<FACT CHECK PUBLICATION DATE>",
            "isBasedOnUrl": "<URL OF FACT CHECK'S ORIGINAL PUBLICATION>",
            "claimReviews": [
                {<CLAIM REVIEW 1>},
                {<CLAIM REVIEW 2>}
            ]
        }
    ]
    ```
    """

    required_keys = ["id", "url", "isBasedOnUrl", "datePublished", "claimReviews"]

    for i in data:
        try:
            assert isinstance(i["claimReviews"], List)
            keys = i.keys()
            for req in required_keys:
                assert req in keys
        except AssertionError as e:
            print(set(required_keys).difference(i.keys()))
            raise e
        try:
            if len(i["claimReviews"]) > 0:
                for c in i["claimReviews"]:
                    c["itemReviewed"]["appearance"]
        except AssertionError as e:
            pprint(i)
            raise e


class DataStream:
    """Class to verify data format and stream parts."""

    def __init__(self, data: List[Dict]) -> None:
        """Verify the JSON array's schema.

        Args:
            data (List[Dict]): Array of fact-check articles in ClaimReview schema.
        """
        verify_data(data)
        self.data = data

    def fact_checks(self) -> Generator[Tuple[str | float, Dict], None, None]:
        """Stream fact-check articles.

        Yields:
            Generator[Tuple[str, Dict], None, None]: Averaged of article's ratings, Article's data
        """
        for fact_check in self.data:
            target_url = "isBasedOnUrl"
            if not fact_check[target_url]:
                continue
            fact_check_ratings = []
            for c in fact_check["claimReviews"]:
                if c.get("reviewRating"):
                    rating_value = c["reviewRating"]["ratingValue"]
                    rating = float(rating_value) if rating_value != "" else None
                    if rating:
                        fact_check_ratings.append(rating)
            if len(fact_check_ratings) > 0:
                fact_check_rating_average = mean(fact_check_ratings)
            else:
                fact_check_rating_average = ""
            yield fact_check_rating_average, fact_check

    @classmethod
    def claim_reviews(
        cls, fact_check: Dict
    ) -> Generator[Tuple[str, Dict, List | None], None, None]:
        """Stream fact-check article's reviewed claims.

        Args:
            fact_check (Dict): Fact-check article's data

        Yields:
            Generator[Tuple[str, Dict, List | None], None, None]: Reviewed claim's rating, reviewed claim's appearance data, appearance's shared content
        """
        for review in fact_check["claimReviews"]:
            if review.get("itemReviewed") and review["itemReviewed"]["appearance"]:
                rating = ""
                if review.get("reviewRating"):
                    rating = review["reviewRating"]["ratingValue"]
                for appearance in cls.stream_appearance(review=review):
                    if appearance:
                        shared_content = None
                        if appearance.get("sharedContent"):
                            shared_content = appearance["sharedContent"]
                        yield rating, appearance, shared_content

    @classmethod
    def stream_appearance(cls, review: Dict) -> Generator[Dict | None, None, None]:
        """Parse and stream appearances in reviewed claim.

        Args:
            review (Dict): Reviewed claim from fact-check article.

        Yields:
            Generator[Dict|None, None, None]: Appearance data.
        """
        appearances = review["itemReviewed"]["appearance"]
        if isinstance(appearances, List):
            for appearance in appearances:
                yield appearance
        else:
            yield appearances


def flatten(
    appearance_file: Path, fact_check_file: Path, content_file: Path, data: List[Dict]
):
    # Set up the CSV writers, progress bar, and class to stream parsed data
    with Writers(appearance_file, content_file, fact_check_file) as writers:
        appearance_writer, content_writer, fact_check_writer, progress = writers
        t = progress.add_task(description="[bold blue]Flatten", total=len(data))
        data_stream = DataStream(data)

        # Iterate through all the data items
        for rating_avg, fact_check in data_stream.fact_checks():
            progress.advance(t)

            # Parse and write the fact-check article's information to the CSV
            fact_check_record = FactCheck.from_json(
                fact_check_rating=rating_avg, item=fact_check
            )
            fact_check_writer.writerow(fact_check_record.as_csv_dict_row())

            # Parse and write the ClaimReview's information to the CSV
            for rating, claim_review, shared_content in data_stream.claim_reviews(
                fact_check=fact_check
            ):
                appearance_record = Appearance.from_json(
                    fact_check_rating=rating, item=claim_review
                )
                if appearance_record.clean_url:
                    appearance_writer.writerow(appearance_record.as_csv_dict_row())

                    # Parse and write the ItemReviewed's shared content to the CSV
                    if appearance_record.exact_url and shared_content:
                        for media in shared_content:
                            media_record = SharedContent.from_json(
                                post_url=appearance_record.exact_url, item=media
                            )
                            content_writer.writerow(media_record.as_csv_dict_row())

        progress.update(task_id=t, completed=len(data))
