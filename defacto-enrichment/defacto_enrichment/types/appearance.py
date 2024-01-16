from dataclasses import dataclass
from typing import Dict, List, Optional

from casanova import TabularRecord
from defacto_enrichment.types.utils import (
    parse_creator_interaction_count,
    parse_interaction_count,
)
from defacto_enrichment.utils import build_interaction_format, build_interaction_stats
from ural import is_url


@dataclass
class Appearance(TabularRecord):
    fact_check_rating: str
    exact_url: Optional[str]
    clean_url: Optional[str]
    domain: Optional[str]
    work_type: Optional[str]
    duration: Optional[str]
    identifier: Optional[str]
    date_published: Optional[str]
    date_modified: Optional[str]
    country_of_origin: Optional[str]
    abstract: Optional[str]
    keywords: Optional[List]
    title: Optional[str]
    text: Optional[str]
    hashtags: Optional[List]
    creator_type: Optional[str]
    creator_date_created: Optional[str]
    creator_location_created: Optional[str]
    creator_identifier: Optional[str]
    creator_facebook_follow: Optional[int]
    creator_facebook_subscribe: Optional[int]
    creator_twitter_follow: Optional[int]
    creator_youtube_subscribe: Optional[int]
    creator_create_video: Optional[int]
    creator_name: Optional[str]
    creator_url: Optional[str]
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
    create_video: Optional[int]

    @classmethod
    def from_json(cls, item: Dict, fact_check_rating: str | None = "") -> "Appearance":
        exact_url = item.get("url")
        clean_url = None
        if exact_url:
            clean_url = exact_url.strip()
            if not is_url(clean_url):
                clean_url = None

        def parse_plural(data: str | None | List) -> List:
            if isinstance(data, List):
                return data
            elif isinstance(data, str):
                return data.split(",")
            else:
                return []

        return Appearance(
            fact_check_rating=str(fact_check_rating),
            exact_url=exact_url,
            clean_url=clean_url,
            domain=item.get("isPartOf", {}).get("name"),
            work_type=item.get("@type"),
            duration=item.get("duration"),
            identifier=item.get("identifier"),
            date_modified=item.get("dateModified"),
            date_published=item.get("datePublished"),
            country_of_origin=item.get("countryOfOrigin"),
            abstract=item.get("abstract"),
            keywords=parse_plural(item.get("keywords")),
            title=item.get("headline"),
            text=item.get("text"),
            hashtags=parse_plural(item.get("defacto:Hashtags")),
            creator_type=item.get("creator", {}).get("@type"),
            creator_date_created=item.get("creator", {}).get("defacto:dateCreated"),
            creator_location_created=item.get("creator", {}).get(
                "defacto:locationCreated"
            ),
            creator_identifier=item.get("creator", {}).get("identifier"),
            creator_facebook_follow=parse_creator_interaction_count(
                data=item, service="Facebook", action="Follow"
            ),
            creator_facebook_subscribe=parse_creator_interaction_count(
                data=item, service="Facebook", action="Subscribe"
            ),
            creator_twitter_follow=parse_creator_interaction_count(
                data=item, service="Twitter", action="Follow"
            ),
            creator_youtube_subscribe=parse_creator_interaction_count(
                data=item, service="YouTube", action="Subscribe"
            ),
            creator_create_video=parse_creator_interaction_count(
                data=item, service="YouTube", action="Create"
            ),
            creator_name=item.get("creator", {}).get("name"),
            creator_url=item.get("creator", {}).get("url"),
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
            tiktok_comment=parse_interaction_count(
                data=item, target_action="Comment", target_service="TikTok"
            ),
            tiktok_share=parse_interaction_count(
                data=item, target_action="Share", target_service="TikTok"
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
            create_video=parse_interaction_count(
                data=item, target_action="Create", target_service="YouTube"
            ),
        )

    @classmethod
    def from_csv_dict_row(cls, row: Dict) -> "Appearance":
        def cast_empty_string(v: str) -> str | None:
            if v != "":
                return v

        row = {k: cast_empty_string(v) for k, v in row.items()}

        def cast_to_int(i: str | None) -> None | int:
            if not i or i == "":
                return None
            else:
                return int(i)

        if row["keywords"]:
            keywords = row["keywords"].split("|")
        else:
            keywords = []
        row["keywords"] = keywords

        if row["hashtags"]:
            hashtags = row["hashtags"].split("|")
        else:
            hashtags = []
        row["hashtags"] = hashtags
        return Appearance(
            fact_check_rating=row["fact_check_rating"],
            exact_url=row["exact_url"],
            clean_url=row["clean_url"],
            domain=row["domain"],
            work_type=row["work_type"],
            duration=row["duration"],
            identifier=row["identifier"],
            date_published=row["date_published"],
            date_modified=row["date_modified"],
            country_of_origin=row["country_of_origin"],
            abstract=row["abstract"],
            keywords=row["keywords"],
            title=row["title"],
            text=row["text"],
            hashtags=row["hashtags"],
            creator_type=row["creator_type"],
            creator_date_created=row["creator_date_created"],
            creator_location_created=row["creator_location_created"],
            creator_identifier=row["creator_identifier"],
            creator_facebook_follow=cast_to_int(row["creator_facebook_follow"]),
            creator_facebook_subscribe=cast_to_int(row["creator_facebook_subscribe"]),
            creator_twitter_follow=cast_to_int(row["creator_twitter_follow"]),
            creator_youtube_subscribe=cast_to_int(row["creator_youtube_subscribe"]),
            creator_create_video=cast_to_int(row["creator_create_video"]),
            creator_name=row["creator_name"],
            creator_url=row["creator_url"],
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
            create_video=cast_to_int(row["create_video"]),
        )

    def to_json(self) -> Dict:
        # Build InteractionStatistics for CreativeWork
        stats = build_interaction_stats(data=self.as_csv_dict_row())
        if self.create_video:
            create_action = build_interaction_format(
                service="YouTube",
                interaction_type="CreateAction",
                count=self.create_video,
            )
            create_action.update({"result": {"@type": "VideoObject"}})
            stats.append(create_action)

        # Build basic metadata for CreativeWork
        r = {
            "url": self.exact_url,
            "@type": self.work_type,
            "isPartOf": {"@type": "WebSite", "name": self.domain},
        }
        if self.identifier:
            r.update({"identifier": self.identifier})
        if self.date_published:
            r.update({"datePublished": self.date_published})
        if self.date_modified:
            r.update({"dateModified": self.date_modified})
        if self.title:
            r.update({"headline": self.title})
        if self.hashtags and len(self.hashtags) > 0 and self.hashtags != [""]:
            r.update({"defacto:Hashtasg": self.hashtags})
        if self.keywords and len(self.keywords) > 0 and self.keywords != [""]:
            r.update({"keywords": self.keywords})
        if self.duration:
            r.update({"duration": self.duration})
        if self.country_of_origin:
            r.update({"countryOfOrigin": self.country_of_origin})
        if self.abstract:
            r.update({"abstract": self.abstract})
        if self.text:
            r.update({"text": self.text})

        # Build Creator metadata
        creator = {}
        if self.creator_type:
            creator.update({"@type": self.creator_type})
        if self.creator_date_created:
            creator.update({"defacto:dateCreated": self.creator_date_created})
        if self.creator_location_created:
            creator.update({"defacto:locationCreated": self.creator_location_created})
        if self.creator_identifier:
            creator.update({"identifier": self.identifier})
        if self.creator_name:
            creator.update({"name": self.creator_name})
        if self.creator_url:
            creator.update({"url": self.exact_url})

        # Build InteractionStatistics for Creator
        creator_stats = []
        if self.creator_facebook_follow:
            creator_stats.append(
                build_interaction_format(
                    service="Facebook",
                    interaction_type="FollowAction",
                    count=self.creator_facebook_follow,
                )
            )
        if self.creator_facebook_subscribe:
            creator_stats.append(
                build_interaction_format(
                    service="Facebook",
                    interaction_type="SubscribeAction",
                    count=self.creator_facebook_subscribe,
                )
            )
        if self.creator_twitter_follow:
            creator_stats.append(
                build_interaction_format(
                    service="Twitter",
                    interaction_type="FollowAction",
                    count=self.creator_twitter_follow,
                )
            )
        if self.creator_youtube_subscribe:
            creator_stats.append(
                build_interaction_format(
                    service="YouTube",
                    interaction_type="SubscribeAction",
                    count=self.creator_youtube_subscribe,
                )
            )
        if self.creator_create_video:
            create_action = build_interaction_format(
                service="YouTube",
                interaction_type="CreateAction",
                count=self.creator_create_video,
            )
            create_action.update({"result": {"@type": "VideoObject"}})
            creator_stats.append(create_action)

        if len(creator_stats) > 0:
            creator.update({"interactionStatistic": creator_stats})

        r.update({"creator": creator, "interactionStatistic": stats})

        return r
