# AI Watch Phase Context

- phase: `ai1_candidate_verify`
- kind: `candidate_verify`
- domain: `ai1`
- page: `ai1`
- run date (KST): `2026-04-22`
- phase root: `.state/runs/2026-04-22/ai1/ai1_candidate_verify`
- publish target: `1/index.html`
- prompt file: `script-only phase`
- timeout: `18 minutes`
- purpose: Verify newly scouted AI/1 candidates before scoring, including on-device proof level, SDK maturity, privacy architecture, and OEM evidence classification.
- source model: raw source -> evidence -> claim -> verify -> score -> render -> publish
- fail-closed: if HQ, unicorn status, category, valuation, timestamps, or ranking claims are unsupported, stale, or contradictory, do not publish
- freshness contract: use explicit TTL / recency logic instead of timestamp-only refreshes
- no-news-day policy: if external updates are absent, refresh trend evidence, stale claims, score rationale, logic issues, or source-quality notes until a validated publish delta exists
- runner model: GitHub-hosted jobs are ephemeral; consume artifacts or committed state only
- decisive evidence: official English / filing / registry / developer-doc sources outrank Korean-language media
