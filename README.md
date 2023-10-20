# defacto-enrichment-public

Scripts and documentation for De Facto database enrichment.

## Data format

The De Facto project's database aggregates fact-checks and makes them available via an RSS feed. Therefore, metadata attached to the fact-checks and the claims they investigate must be in JSON-LD format and follow the ClaimReview and MediaReview schemas, which are commonly used by fact-checkers. We depend as much as possible on the schemas' standards. However, enriched metadata from social media platforms requires the invention of some new ClaimReview properties and types, whose schema is documented on the [AFP-Medialab GitHub repository](https://github.com/AFP-Medialab/defacto-rss/blob/main/Defactor_rss.adoc).

All information about the enrichments achieved with the [`defacto-enrichment`](defacto-enrichment) workflow are documented in this repository in [`schema.adoc`](schemas/schema.adoc)

## Enrichment procedure

![decision tree](schemas/decision-tree.png)
