# AI Watch Phase Context

- phase: `repair_retry`
- kind: `retry`
- domain: `global`
- page: `global`
- run date (KST): `2026-04-22`
- phase root: `.state/runs/2026-04-22/global/repair_retry`
- publish target: `n/a`
- prompt file: `script-only phase`
- timeout: `10 minutes`
- purpose: Classify failures into retryable and non-retryable buckets and propose only bounded safe reruns.
- source model: raw source -> evidence -> claim -> verify -> score -> render -> publish
- fail-closed: if HQ, unicorn status, category, valuation, timestamps, or ranking claims are unsupported, stale, or contradictory, do not publish
- freshness contract: use explicit TTL / recency logic instead of timestamp-only refreshes
- no-news-day policy: if external updates are absent, refresh trend evidence, stale claims, score rationale, logic issues, or source-quality notes until a validated publish delta exists
- runner model: GitHub-hosted jobs are ephemeral; consume artifacts or committed state only
- decisive evidence: official English / filing / registry / developer-doc sources outrank Korean-language media
