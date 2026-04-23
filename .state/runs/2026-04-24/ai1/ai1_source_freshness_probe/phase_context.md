# AI Watch Phase Context

- phase: `ai1_source_freshness_probe`
- kind: `freshness`
- domain: `ai1`
- page: `ai1`
- run date (KST): `2026-04-24`
- phase root: `.state/runs/2026-04-24/ai1/ai1_source_freshness_probe`
- publish target: `1/index.html`
- prompt file: `script-only phase`
- timeout: `12 minutes`
- purpose: Check RSS, sitemap, ETag, app-store, and newsroom freshness before AI/1 fetch and scout work.
- source model: raw source -> evidence -> claim -> verify -> score -> render -> publish
- fail-closed: if HQ, unicorn status, category, valuation, timestamps, or ranking claims are unsupported, stale, or contradictory, do not publish
- freshness contract: use explicit TTL / recency logic instead of timestamp-only refreshes
- no-news-day policy: if external updates are absent, refresh trend evidence, stale claims, score rationale, logic issues, or source-quality notes until a validated publish delta exists
- runner model: GitHub-hosted jobs are ephemeral; consume artifacts or committed state only
- decisive evidence: official English / filing / registry / developer-doc sources outrank Korean-language media
