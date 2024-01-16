from dataclasses import dataclass
from typing import Dict, List, Optional

from casanova import TabularRecord
from defacto_enrichment.types.utils import parse_interaction_count
from defacto_enrichment.utils import build_interaction_stats
from ural import is_url


@dataclass
class FactCheck(TabularRecord):
    fact_check_rating: str
    exact_url: Optional[str]
    clean_url: Optional[str]
    date_published: Optional[str]
    facebook_comment: Optional[int]
    facebook_like: Optional[int]
    facebook_share: Optional[int]
    pinterest_share: Optional[int]
    twitter_share: Optional[int]
    tiktok_share: Optional[int]
    tiktok_comment: Optional[int]
    reddit_engagement: Optional[int]
    youtube_watch: Optional[int]
    youtube_comment: Optional[int]
    youtube_like: Optional[int]
    youtube_favorite: Optional[int]
    youtube_subscribe: Optional[int]

    @classmethod
    def from_json(
        cls, item: Dict, fact_check_rating: str | float | int | None = ""
    ) -> "FactCheck":
        exact_url = item.get("isBasedOnUrl")
        clean_url = None
        if exact_url:
            clean_url = exact_url.strip()
            if not is_url(clean_url):
                clean_url = None

        return FactCheck(
            fact_check_rating=str(fact_check_rating),
            exact_url=exact_url,
            clean_url=clean_url,
            date_published=item.get("datePublished"),
            facebook_comment=parse_interaction_count(
                data=item, target_action="Comment", target_service="Facebook"
            ),
            facebook_like=parse_interaction_count(
                data=item, target_action="Like", target_service="Facebook"
            ),
            facebook_share=parse_interaction_count(
                data=item, target_action="Share", target_service="Facebook"
            ),
            pinterest_share=parse_interaction_count(
                data=item, target_action="Share", target_service="Pinterest"
            ),
            twitter_share=parse_interaction_count(
                data=item, target_action="Share", target_service="Twitter"
            ),
            tiktok_share=parse_interaction_count(
                data=item, target_action="Share", target_service="TikTok"
            ),
            tiktok_comment=parse_interaction_count(
                data=item, target_action="Comment", target_service="TikTok"
            ),
            reddit_engagement=parse_interaction_count(
                data=item, target_action="Engagement", target_service="Reddit"
            ),
            youtube_watch=parse_interaction_count(
                data=item, target_action="Watch", target_service="YouTube"
            ),
            youtube_comment=parse_interaction_count(
                data=item, target_action="Comment", target_service="YouTube"
            ),
            youtube_like=parse_interaction_count(
                data=item, target_action="Like", target_service="YouTube"
            ),
            youtube_favorite=parse_interaction_count(
                data=item, target_action="Favorite", target_service="YouTube"
            ),
            youtube_subscribe=parse_interaction_count(
                data=item, target_action="Subscribe", target_service="YouTube"
            ),
        )

    @classmethod
    def from_csv_dict_row(cls, row: Dict) -> "FactCheck":
        def cast_empty_string(v: str) -> str | None:
            if v != "":
                return v

        row = {k: cast_empty_string(v) for k, v in row.items()}

        def cast_to_int(i: str | None) -> None | int:
            if not i or i == "":
                return None
            else:
                return int(i)

        return FactCheck(
            fact_check_rating=row["fact_check_rating"],
            exact_url=row["exact_url"],
            clean_url=row["clean_url"],
            date_published=row["date_published"],
            facebook_comment=cast_to_int(row["facebook_comment"]),
            facebook_like=cast_to_int(row["facebook_like"]),
            facebook_share=cast_to_int(row["facebook_share"]),
            pinterest_share=cast_to_int(row["pinterest_share"]),
            twitter_share=cast_to_int(row["twitter_share"]),
            tiktok_share=cast_to_int(row["tiktok_share"]),
            tiktok_comment=cast_to_int(row["tiktok_comment"]),
            reddit_engagement=cast_to_int(row["reddit_engagement"]),
            youtube_watch=cast_to_int(row["youtube_watch"]),
            youtube_comment=cast_to_int(row["youtube_comment"]),
            youtube_like=cast_to_int(row["youtube_like"]),
            youtube_favorite=cast_to_int(row["youtube_favorite"]),
            youtube_subscribe=cast_to_int(row["youtube_subscribe"]),
        )

    def to_json(self) -> List:
        stats = build_interaction_stats(data=self.as_csv_dict_row())
        return stats
