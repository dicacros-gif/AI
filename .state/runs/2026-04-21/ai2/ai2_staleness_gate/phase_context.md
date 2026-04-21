# AI Watch Phase Context

- phase: `ai2_staleness_gate`
- kind: `staleness`
- domain: `ai2`
- page: `ai2`
- run date (KST): `2026-04-21`
- phase root: `.state/runs/2026-04-21/ai2/ai2_staleness_gate`
- publish target: `2/index.html`
- prompt file: `script-only phase`
- timeout: `8 minutes`
- purpose: Block AI/2 publish candidates whose core claims exceeded TTL or whose platform-policy assumptions drifted.
- source model: raw source -> evidence -> claim -> verify -> score -> render -> publish
- fail-closed: if HQ, unicorn status, category, valuation, timestamps, or ranking claims are unsupported, stale, or contradictory, do not publish
- freshness contract: use explicit TTL / recency logic instead of timestamp-only refreshes
- no-news-day policy: if external updates are absent, refresh trend evidence, stale claims, score rationale, logic issues, or source-quality notes until a validated publish delta exists
- runner model: GitHub-hosted jobs are ephemeral; consume artifacts or committed state only
- decisive evidence: official English / filing / registry / developer-doc sources outrank Korean-language media
