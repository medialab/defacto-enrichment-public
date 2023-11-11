from typing import Dict, List


def build_interaction_format(service: str, interaction_type: str, count: int):
    return {
        "@type": "InteractionCounter",
        "interactionType": interaction_type,
        "interactionService": {"@type": "WebSite", "name": service},
        "userInteractionCount": count,
    }


def build_interaction_stats(data: Dict) -> List:
    stats = []
    if data["facebook_comment"]:
        stats.append(
            build_interaction_format(
                service="Facebook",
                interaction_type="CommentAction",
                count=data["facebook_comment"],
            )
        )
    if data["facebook_like"]:
        stats.append(
            build_interaction_format(
                service="Facebook",
                interaction_type="LikeAction",
                count=data["facebook_like"],
            )
        )
    if data["facebook_share"]:
        stats.append(
            build_interaction_format(
                service="Facebook",
                interaction_type="ShareAction",
                count=data["facebook_share"],
            )
        )
    if data["pinterest_share"]:
        stats.append(
            build_interaction_format(
                service="Pinterest",
                interaction_type="ShareAction",
                count=data["pinterest_share"],
            )
        )
    if data["twitter_share"]:
        stats.append(
            build_interaction_format(
                service="Twitter",
                interaction_type="ShareAction",
                count=data["twitter_share"],
            )
        )
    if data["tiktok_share"]:
        stats.append(
            build_interaction_format(
                service="TikTok",
                interaction_type="ShareAction",
                count=data["tiktok_share"],
            )
        )
    if data["tiktok_comment"]:
        stats.append(
            build_interaction_format(
                service="TikTok",
                interaction_type="CommentAction",
                count=data["tiktok_comment"],
            )
        )
    if data["reddit_engagement"]:
        stats.append(
            build_interaction_format(
                service="Reddit",
                interaction_type="defacto:EngagementAction",
                count=data["reddit_engagement"],
            )
        )
    if data["youtube_watch"]:
        stats.append(
            build_interaction_format(
                service="YouTube",
                interaction_type="WatchAction",
                count=data["youtube_watch"],
            )
        )
    if data["youtube_comment"]:
        stats.append(
            build_interaction_format(
                service="YouTube",
                interaction_type="CommentAction",
                count=data["youtube_comment"],
            )
        )
    if data["youtube_like"]:
        stats.append(
            build_interaction_format(
                service="YouTube",
                interaction_type="LikeAction",
                count=data["youtube_like"],
            )
        )
    if data["youtube_favorite"]:
        stats.append(
            build_interaction_format(
                service="YouTube",
                interaction_type="FavoriteAction",
                count=data["youtube_favorite"],
            )
        )
    if data["youtube_subscribe"]:
        stats.append(
            build_interaction_format(
                service="YouTube",
                interaction_type="SubscribeAction",
                count=data["youtube_subscribe"],
            )
        )

    return stats
