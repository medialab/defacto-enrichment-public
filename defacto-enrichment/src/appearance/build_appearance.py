import ast

from src.appearance.utils import build_interaction_format
from src.shared_content.build_shared_content import build_shared_content


class AppearanceBuilder:
    def __init__(self, shared_content_index: dict) -> None:
        self.shared_content_index = shared_content_index

    def parse_interaction_stats(self, data: dict) -> list:
        stats = []
        if data.get("facebook_comment"):
            interaction_stat = build_interaction_format(
                service="Facebook",
                interaction_type="CommentAction",
                count=data["facebook_comment"],
            )
            stats.append(interaction_stat)
        if data.get("facebook_like"):
            interaction_stat = build_interaction_format(
                service="Facebook",
                interaction_type="LikeAction",
                count=data["facebook_like"],
            )
            stats.append(interaction_stat)
        if data.get("facebook_share"):
            interaction_stat = build_interaction_format(
                service="Facebook",
                interaction_type="ShareAction",
                count=data["facebook_share"],
            )
            stats.append(interaction_stat)
        if data.get("pinterest_share"):
            interaction_stat = build_interaction_format(
                service="Pinterest",
                interaction_type="ShareAction",
                count=data["pinterest_share"],
            )
            stats.append(interaction_stat)
        if data.get("twitter_share"):
            interaction_stat = build_interaction_format(
                service="Twitter",
                interaction_type="ShareAction",
                count=data["twitter_share"],
            )
            stats.append(interaction_stat)
        if data.get("tiktok_share"):
            interaction_stat = build_interaction_format(
                service="TikTok",
                interaction_type="ShareAction",
                count=data["tiktok_share"],
            )
            stats.append(interaction_stat)
        if data.get("tiktok_comment"):
            interaction_stat = build_interaction_format(
                service="TikTok",
                interaction_type="CommentAction",
                count=data["tiktok_comment"],
            )
            stats.append(interaction_stat)
        if data.get("reddit_engagement"):
            interaction_stat = build_interaction_format(
                service="Reddit",
                interaction_type="defacto:EngagementAction",
                count=data["reddit_engagement"],
            )
            stats.append(interaction_stat)
        if data.get("youtube_watch"):
            interaction_stat = build_interaction_format(
                service="YouTube",
                interaction_type="WatchAction",
                count=data["youtube_watch"],
            )
            stats.append(interaction_stat)
        if data.get("youtube_comment"):
            interaction_stat = build_interaction_format(
                service="YouTube",
                interaction_type="CommentAction",
                count=data["youtube_comment"],
            )
            stats.append(interaction_stat)
        if data.get("youtube_like"):
            interaction_stat = build_interaction_format(
                service="YouTube",
                interaction_type="LikeAction",
                count=data["youtube_like"],
            )
            stats.append(interaction_stat)
        if data.get("youtube_favorite"):
            interaction_stat = build_interaction_format(
                service="YouTube",
                interaction_type="FavoriteAction",
                count=data["youtube_favorite"],
            )
            stats.append(interaction_stat)
        if data.get("youtube_subscribe"):
            interaction_stat = build_interaction_format(
                service="YouTube",
                interaction_type="SubscribeAction",
                count=data["youtube_subscribe"],
            )
            stats.append(interaction_stat)
        if data.get("create_video"):
            interaction_stat = build_interaction_format(
                service="YouTube",
                interaction_type="CreateAction",
                count=data["create_video"],
            )
            interaction_stat.update({"result": {"@type": "VideoObject"}})
            stats.append(interaction_stat)

        return stats

    def __call__(self, data: dict) -> dict:
        # Add directly descendant metadata
        appearance_url = data["url"]
        keep = {
            "url": appearance_url,
            "@type": data["type"],
            "isPartOf": {"@type": "website", "name": data["domain"]},
        }
        if data.get("identifier"):
            keep.update({"identifier": data["identifier"]})
        if data.get("date_published"):
            keep.update({"datePublished": data["date_published"]})
        if data.get("date_modified"):
            keep.update({"dateModified": data["date_modified"]})
        if data.get("hashtags"):
            try:
                hashtags = ast.literal_eval(data["hashtags"])
            except Exception:
                hashtags = data["hashtags"]
            keep.update({"defacto:Hashtags": hashtags})
        if data.get("title"):
            keep.update({"headline": data["title"]})
        if data.get("duration"):
            keep.update({"duration": data["duration"]})
        if data.get("country_of_origin"):
            keep.update({"countryOfOrigin": data["country_of_origin"]})
        if data.get("abstract"):
            keep.update({"abstract": data["abstract"]})
        if data.get("keywords"):
            try:
                keywords = ast.literal_eval(data["keywords"])
            except Exception:
                keywords = data["keywords"]
            keep.update({"keywords": keywords})
        if data.get("text"):
            keep.update({"text": data["text"]})

        # Add Creator
        creator = {}
        if data.get("creator_type"):
            creator.update({"@type": data["creator_type"]})
        if data.get("creator_date_created"):
            creator.update({"defacto:dateCreated": data["creator_date_created"]})
        if data.get("creator_location_created"):
            creator.update(
                {"defacto:locationCreated": data["creator_location_created"]}
            )
        if data.get("creator_identifier"):
            creator.update({"identifier": data["creator_identifier"]})
        if data.get("creator_name"):
            creator.update({"name": data["creator_name"]})
        if data.get("creator_url"):
            creator.update({"url": data["creator_url"]})
        creator_stats = []
        if data.get("creator_facebook_follow"):
            creator_stats.append(
                build_interaction_format(
                    service="Facebook",
                    interaction_type="FollowAction",
                    count=data["creator_facebook_follow"],
                )
            )
        if data.get("creator_facebook_subscribe"):
            creator_stats.append(
                build_interaction_format(
                    service="Facebook",
                    interaction_type="SubscribeAction",
                    count=data["creator_facebook_subscribe"],
                )
            )
        if data.get("creator_twitter_follow"):
            creator_stats.append(
                build_interaction_format(
                    service="Twitter",
                    interaction_type="FollowAction",
                    count=data["creator_twitter_follow"],
                )
            )
        if data.get("creator_youtube_subscribe"):
            creator_stats.append(
                build_interaction_format(
                    service="YouTube",
                    interaction_type="SubscribeAction",
                    count=data["creator_youtube_subscribe"],
                )
            )
        if data.get("creator_create_video"):
            yt_channel_stat = build_interaction_format(
                service="YouTube",
                interaction_type="CreateAction",
                count=data["creator_create_video"],
            )
            yt_channel_stat.update({"result": {"@type": "VideoObject"}})
            creator_stats.append(yt_channel_stat)
        creator.update({"interactionStatistic": creator_stats})

        keep.update({"creator": creator})

        # Add interactionStatistic for CreativeWork
        work_stats = self.parse_interaction_stats(data)
        keep.update({"interactionStatistic": work_stats})

        # Add sharedContent
        shared_content = build_shared_content(
            appearance_url=appearance_url,
            shared_content_index=self.shared_content_index,
        )
        if shared_content:
            keep.update(shared_content)

        return keep
