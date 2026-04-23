# AI Watch Phase Context

- phase: `ai1_verify`
- kind: `verify`
- domain: `ai1`
- page: `ai1`
- run date (KST): `2026-04-24`
- phase root: `.state/runs/2026-04-24/ai1/ai1_verify`
- publish target: `1/index.html`
- prompt file: `.github/codex/prompts/ai1_verify.md`
- timeout: `18 minutes`
- purpose: Cross-check the current AI/1 page against update outputs for factual, logical, and formatting errors, and surface publishable review corrections even on no-news days.
- source model: raw source -> evidence -> claim -> verify -> score -> render -> publish
- fail-closed: if HQ, unicorn status, category, valuation, timestamps, or ranking claims are unsupported, stale, or contradictory, do not publish
- freshness contract: use explicit TTL / recency logic instead of timestamp-only refreshes
- no-news-day policy: if external updates are absent, refresh trend evidence, stale claims, score rationale, logic issues, or source-quality notes until a validated publish delta exists
- runner model: GitHub-hosted jobs are ephemeral; consume artifacts or committed state only
- decisive evidence: official English / filing / registry / developer-doc sources outrank Korean-language media
