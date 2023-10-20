# CLASS TO FLATTEN REVIEW FROM JSON-LD TO CSV
from src.appearance.utils import parse_interaction_count
from src.review.constants import FlatReview


class ReviewFlattener:
    def __init__(self, data: dict, link_id: str) -> None:
        # Identifier for the fact-check
        self.link_id = link_id

        # --- DIRECT METADATA ---
        self.url = data.get("url")
        self.date_published = data.get("published")

        # --- INTERACTIONS DATA ---
        self.facebook_comment = parse_interaction_count(
            data=data, target_action="Comment", target_service="Facebook"
        )
        self.facebook_like = parse_interaction_count(
            data=data, target_action="Like", target_service="Facebook"
        )
        self.facebook_share = parse_interaction_count(
            data=data, target_action="Share", target_service="Facebook"
        )
        self.pinterest_share = parse_interaction_count(
            data=data, target_action="Share", target_service="Pinterest"
        )
        self.twitter_share = parse_interaction_count(
            data=data, target_action="Share", target_service="Twitter"
        )
        self.tiktok_share = parse_interaction_count(
            data=data, target_action="Share", target_service="TikTok"
        )
        self.tiktok_comment = parse_interaction_count(
            data=data, target_action="Comment", target_service="TikTok"
        )
        self.reddit_engagement = parse_interaction_count(
            data=data, target_action="Engagement", target_service="Reddit"
        )
        self.youtube_watch = parse_interaction_count(
            data=data, target_action="Watch", target_service="YouTube"
        )
        self.youtube_comment = parse_interaction_count(
            data=data, target_action="Comment", target_service="YouTube"
        )
        self.youtube_like = parse_interaction_count(
            data=data, target_action="Like", target_service="YouTube"
        )
        self.youtube_favorite = parse_interaction_count(
            data=data, target_action="Favorite", target_service="YouTube"
        )
        self.youtube_subscribe = parse_interaction_count(
            data=data, target_action="Subscribe", target_service="YouTube"
        )

    def __call__(self) -> FlatReview:
        return FlatReview(**self.__dict__)
