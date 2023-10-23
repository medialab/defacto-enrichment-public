# defacto-enrichment-public

Scripts and documentation for De Facto database enrichment.

![Minall tests](https://github.com/medialab/minall/actions/workflows/tests.yml/badge.svg)

## [ClaimReview Schema](schemas/schema.adoc)

The De Facto project's database aggregates fact-checks and makes them available via an RSS feed. Therefore, metadata attached to the fact-checks and the claims they investigate must be in JSON-LD format and follow the ClaimReview and MediaReview schemas, which are commonly used by fact-checkers. We depend as much as possible on the schemas' standards. However, enriched metadata from social media platforms requires the invention of some new ClaimReview properties and types, whose schema is documented on the [AFP-Medialab GitHub repository](https://github.com/AFP-Medialab/defacto-rss/blob/main/Defactor_rss.adoc).

## Enrichment procedure

The enrichment relies on the Python library [`minall`](https://github.com/medialab/minall), which leverages the many platform-specific API client wrappers of [`minet`](https://github.com/medialab/minet) to collect data about the various claims in the database.

`minall` uses the following logic, as represented in this decision tree, to process each URL in the data set.

![decision tree](schemas/decision-tree.png)

## New data fields

### Claim-review

The claim-review is given the new field of `interactionStatistic`, which contains metrics about how the fact-check has circulated on social media.

### Appearance

A claim-review has zero or more appearances of the reviewed claim in the field: `claim-review.itemReviewed.appearance`.

The original key-value pairs are: `url`, `@type`.

The new key-value pairs are: `isPartOf`, `identifier`, `datePublished`, `dateModified`, `defacto:Hashtags`, `headline`, `duration`, `countryOfOrigin`, `abstract`, `keywords`, `text`, `creator`, `interactionStatistic`, `sharedContent`.

#### Original appearance

```json
{
  "url": "example.com",
  "@type": "VARCHAR: a Schema.org classification for the URL as a CreativeWork"
}
```

#### Enriched appearance

```json
{
  "url": "example.com",
  "@type": "VARCHAR: a Schema.org classification for the URL as a CreativeWork",
  "isPartOf": {
    "@type": "website",
    "name": "VARCHAR: the URL's domain name"
  },
  "identifier": "VARCHAR: the identifier given to the CreativeWork via a platform (i.e. YouTube ID, Twitter user ID)",
  "datePublished": "DATE: date (YYYY-MM-DD) when the CreativeWork's content was originally published",
  "dateModified": "DATE: date (YYYY-MM-DD) when the CreativeWork's content was last updated",
  "defacto:Hashtags": "VARCHAR: hashtags associated with the CreativeWork",
  "headline": "VARCHAR: title given to the CreativeWork's content",
  "duration": "VARCHAR: if the URL is of a video, the video's duration",
  "countryOfOrigin": "VARCHAR: if the URL is of a YouTube channel, the channel's registered country",
  "abstract": "VARCHAR: abbreviated description of the CreativeWork's content",
  "keywords": "VARCHAR: keywords associated with the CreativeWork",
  "text": "VARCHAR: the CreativeWork's main textual content",
  "creator": {
    "@type": "VARCHAR: a Schema.org or De Facto classification for the creator of the URL's content",
    "defacto:dateCreated": "DATE: if the CreativeWork's content was created by a social media account, the date of the account's creation on the site",
    "defacto:locationCreated": "VARCHAR: if the CreativeWork's content was created by a social media account, the country in which the account is registered",
    "identifier": "VARCHAR: if the CreativeWork's content was created by a social media account, the social media platform's identifier for the account",
    "name": "VARCHAR: the name of the creator of the CreativeWork's content",
    "url": "VARCHAR: if the URL is a social media post, a link to the creator's account page on the platform",
    "interactionStatistic": [
      {
        "@type": "InteractionCounter",
        "interactionType": "FollowAction",
        "interactionService": {
          "@type": "website",
          "name": "Facebook"
        },
        "userInteractionCount": "INTEGER: if the CreativeWork is a Facebook post, the number of Facebook followers the creator's account has"
      },
      {
        "@type": "InteractionCounter",
        "interactionType": "SubscribeAction",
        "interactionService": {
          "@type": "website",
          "name": "Facebook"
        },
        "userInteractionCount": "INTEGER: if the URL is a Facebook post, the number of Facebook subscribers the creator's account has"
      },
      {
        "@type": "InteractionCounter",
        "interactionType": "FollowAction",
        "interactionService": {
          "@type": "website",
          "name": "Twitter"
        },
        "userInteractionCount": "INTEGER: if the URL is a Tweet, the number of Twitter / X followers the creator's account has"
      },
      {
        "@type": "InteractionCounter",
        "interactionType": "SubscribeAction",
        "interactionService": {
          "@type": "website",
          "name": "YouTube"
        },
        "userInteractionCount": "INTEGER: if the URL is a YouTube video, the number of YouTube channel subscribers the channel has"
      },
      {
        "@type": "InteractionCounter",
        "interactionType": "CreateAction",
        "interactionService": {
          "@type": "website",
          "name": "YouTube"
        },
        "userInteractionCount": "INTEGER: if the URL is a YouTube video, the number of videos the YouTube channel has created",
        "result": {
          "@type": "VideoObject"
        }
      }
    ]
  },
  "interactionStatistic": [
    {
      "@type": "InteractionCounter",
      "interactionType": "CommentAction",
      "interactionService": {
        "@type": "website",
        "name": "Facebook"
      },
      "userInteractionCount": "INTEGER: number of comments the URL has received on Facebook"
    },
    {
      "@type": "InteractionCounter",
      "interactionType": "LikeAction",
      "interactionService": {
        "@type": "website",
        "name": "Facebook"
      },
      "userInteractionCount": "INTEGER: number of likes the URL has received on Facebook"
    },
    {
      "@type": "InteractionCounter",
      "interactionType": "ShareAction",
      "interactionService": {
        "@type": "website",
        "name": "Facebook"
      },
      "userInteractionCount": "INTEGER: number of shares the URL has received on Facebook"
    },
    {
      "@type": "InteractionCounter",
      "interactionType": "ShareAction",
      "interactionService": {
        "@type": "website",
        "name": "Pinterest"
      },
      "userInteractionCount": "INTEGER: number of shares the URL has received on Pinterest"
    },
    {
      "@type": "InteractionCounter",
      "interactionType": "ShareAction",
      "interactionService": {
        "@type": "website",
        "name": "Twitter"
      },
      "userInteractionCount": "INTEGER: number of shares the URL has received on Twitter / X"
    },
    {
      "@type": "InteractionCounter",
      "interactionType": "ShareAction",
      "interactionService": {
        "@type": "website",
        "name": "TikTok"
      },
      "userInteractionCount": "INTEGER: number of shares the URL has received on TikTok"
    },
    {
      "@type": "InteractionCounter",
      "interactionType": "CommentAction",
      "interactionService": {
        "@type": "website",
        "name": "TikTok"
      },
      "userInteractionCount": "INTEGER: number of comments the URL has received on TikTok"
    },
    {
      "@type": "InteractionCounter",
      "interactionType": "defacto:EngagementAction",
      "interactionService": {
        "@type": "website",
        "name": "Reddit"
      },
      "userInteractionCount": "INTEGER: metric engagement the URL has received on Reddit"
    },
    {
      "@type": "InteractionCounter",
      "interactionType": "WatchAction",
      "interactionService": {
        "@type": "website",
        "name": "YouTube"
      },
      "userInteractionCount": "INTEGER: number of views the URL has received on YouTube"
    },
    {
      "@type": "InteractionCounter",
      "interactionType": "CommentAction",
      "interactionService": {
        "@type": "website",
        "name": "YouTube"
      },
      "userInteractionCount": "INTEGER: number of comments the URL has received on YouTube"
    },
    {
      "@type": "InteractionCounter",
      "interactionType": "LikeAction",
      "interactionService": {
        "@type": "website",
        "name": "YouTube"
      },
      "userInteractionCount": "INTEGER: number of likes the URL has received on YouTube"
    },
    {
      "@type": "InteractionCounter",
      "interactionType": "FavoriteAction",
      "interactionService": {
        "@type": "website",
        "name": "YouTube"
      },
      "userInteractionCount": "INTEGER: number of favorite reactions the URL has received on YouTube"
    },
    {
      "@type": "InteractionCounter",
      "interactionType": "SubscribeAction",
      "interactionService": {
        "@type": "website",
        "name": "YouTube"
      },
      "userInteractionCount": "INTEGER: if the URL is of a YouTube channel, the channel's number of subscribers"
    },
    {
      "@type": "InteractionCounter",
      "interactionType": "CreateAction",
      "interactionService": {
        "@type": "website",
        "name": "YouTube"
      },
      "userInteractionCount": "INTEGER: if the URL is of a YouTube channel, the number of videos the channel has created",
      "result": {
        "@type": "VideoObject"
      }
    }
  ],
  "sharedContent": [
    {
      "@type": "a Schema.org classification for the shared media",
      "contentURL": "URL of the shared media",
      "height": "if an image, the height",
      "width": "if an image, the width"
    }
  ]
}
```
