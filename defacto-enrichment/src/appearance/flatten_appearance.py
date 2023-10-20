# CLASS TO FLATTEN APPEARANCE FROM JSON-LD TO CSV

from src.appearance.constants import APPEARANCE_FIELDNAMES, FlatAppearance
from src.appearance.utils import (
    parse_creator_interaction_count,
    parse_interaction_count,
    parse_old_creator_date_created_format,
)


class AppearanceFlattener:
    def __init__(self, data: dict, link_id: str) -> None:
        # Identifier for the associated fact-check
        self.link_id = link_id

        # --- DIRECT METADATA ---
        self.url = data.get("url")
        # Remove whitespace from input URL
        if self.url:
            self.url = self.url.strip()
        self.domain = data.get("isPartOf", {}).get("name")
        self.type = data.get("@type")
        self.duration = data.get("duration")
        self.identifier = data.get("identifier")
        self.date_published = data.get("datePublished")
        self.date_modified = data.get("dateModified")
        self.country_of_origin = data.get("countryOfOrigin")
        self.abstract = data.get("abstract")
        self.keywords = data.get("keywords")
        # Parse array of keywords
        if isinstance(self.keywords, str):
            self.keywords = self.keywords.split(",")
        self.title = data.get("headline")
        self.text = data.get("text")
        self.hashtags = data.get("defacto:Hashtags")
        # Parse array of hashtags
        if isinstance(self.hashtags, str):
            self.hashtags = self.hashtags.split(",")
        self.creator_type = data.get("creator", {}).get("@type")

        # --- CREATOR DATA ---
        self.creator_date_created = data.get("creator", {}).get(
            "defacto:dateCreated"
        ) or parse_old_creator_date_created_format(data)
        self.creator_location_created = data.get("creator", {}).get(
            "defacto:locationCreated"
        )
        self.creator_identifier = data.get("creator", {}).get("identifier")
        self.creator_name = data.get("creator", {}).get("name")
        self.creator_url = data.get("creator", {}).get("url")
        self.creator_facebook_follow = parse_creator_interaction_count(
            data=data, service="Facebook", action="Follow"
        )
        self.creator_facebook_subscribe = parse_creator_interaction_count(
            data=data, service="Facebook", action="Subscribe"
        )
        self.creator_twitter_follow = parse_creator_interaction_count(
            data=data, service="Twitter", action="Follow"
        )
        self.creator_youtube_subscribe = parse_creator_interaction_count(
            data=data, service="Youtube", action="Subscribe"
        )
        self.creator_create_video = parse_creator_interaction_count(
            data=data, service="Youtube", action="Create"
        )

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
        # Add create action for YT channel (create_video)
        self.create_video = parse_interaction_count(
            data=data, target_action="Create", target_service="YouTube"
        )

        self.shared_content = data.get("sharedContent")

    def __call__(self) -> FlatAppearance:
        appearance_fields = {k: getattr(self, k) for k in APPEARANCE_FIELDNAMES}
        return FlatAppearance(**appearance_fields)
