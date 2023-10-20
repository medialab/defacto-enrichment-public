from src.appearance.utils import build_interaction_format


class ReviewBuilder:
    def __init__(self) -> None:
        pass

    def __call__(self, data: dict) -> list:
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

        return stats
