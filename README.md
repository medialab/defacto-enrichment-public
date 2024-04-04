# defacto-enrichment-public

Scripts and documentation for De Facto database enrichment.

![minall tests](https://github.com/medialab/minall/actions/workflows/tests.yml/badge.svg)
![defacto-enrichment tests](https://github.com/medialab/defacto-enrichment-public/actions/workflows/test.yml/badge.svg)

<img src="defacto-enrichment/badge/badge.svg"/>

## [ClaimReview Schema](schemas/schema.adoc)

The De Facto project's database aggregates fact-checks and makes them available via an RSS feed. Therefore, metadata attached to the fact-checks and the claims they investigate must be in JSON-LD format and follow the ClaimReview and MediaReview schemas, which are commonly used by fact-checkers. We depend as much as possible on the schemas' standards. However, enriched metadata from social media platforms requires the invention of some new ClaimReview properties and types, whose schema is documented on the [AFP-Medialab GitHub repository](https://github.com/AFP-Medialab/defacto-rss/blob/main/Defacto_rss.adoc).

## Enrichment procedure

The enrichment relies on the Python library [`minall`](https://github.com/medialab/minall), which leverages the many platform-specific API client wrappers of [`minet`](https://github.com/medialab/minet) to collect data about appearances of claims in the database.

See documentation here: [https://medialab.github.io/minall/](https://medialab.github.io/minall/)
