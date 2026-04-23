# AI Watch Phase Context

- phase: `ai2_candidate_verify`
- kind: `candidate_verify`
- domain: `ai2`
- page: `ai2`
- run date (KST): `2026-04-24`
- phase root: `.state/runs/2026-04-24/ai2/ai2_candidate_verify`
- publish target: `2/index.html`
- prompt file: `script-only phase`
- timeout: `18 minutes`
- purpose: Verify newly scouted AI/2 candidates before scoring, including OEM surface support, SDK maturity, measurement stack support, privacy readiness, reach classification, and deprecation risk.
- source model: raw source -> evidence -> claim -> verify -> score -> render -> publish
- fail-closed: if HQ, unicorn status, category, valuation, timestamps, or ranking claims are unsupported, stale, or contradictory, do not publish
- freshness contract: use explicit TTL / recency logic instead of timestamp-only refreshes
- no-news-day policy: if external updates are absent, refresh trend evidence, stale claims, score rationale, logic issues, or source-quality notes until a validated publish delta exists
- runner model: GitHub-hosted jobs are ephemeral; consume artifacts or committed state only
- decisive evidence: official English / filing / registry / developer-doc sources outrank Korean-language media
