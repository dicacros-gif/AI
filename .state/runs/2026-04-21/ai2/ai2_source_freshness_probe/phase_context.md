# AI Watch Phase Context

- phase: `ai2_source_freshness_probe`
- kind: `freshness`
- domain: `ai2`
- page: `ai2`
- run date (KST): `2026-04-21`
- phase root: `.state/runs/2026-04-21/ai2/ai2_source_freshness_probe`
- publish target: `2/index.html`
- prompt file: `script-only phase`
- timeout: `12 minutes`
- purpose: Check RSS, sitemap, developer docs, policy pages, and platform freshness before AI/2 fetch and scout work.
- source model: raw source -> evidence -> claim -> verify -> score -> render -> publish
- fail-closed: if HQ, unicorn status, category, valuation, timestamps, or ranking claims are unsupported, stale, or contradictory, do not publish
- freshness contract: use explicit TTL / recency logic instead of timestamp-only refreshes
- no-news-day policy: if external updates are absent, refresh trend evidence, stale claims, score rationale, logic issues, or source-quality notes until a validated publish delta exists
- runner model: GitHub-hosted jobs are ephemeral; consume artifacts or committed state only
- decisive evidence: official English / filing / registry / developer-doc sources outrank Korean-language media
