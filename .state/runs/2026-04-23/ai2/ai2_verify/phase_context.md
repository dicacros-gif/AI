# AI Watch Phase Context

- phase: `ai2_verify`
- kind: `verify`
- domain: `ai2`
- page: `ai2`
- run date (KST): `2026-04-23`
- phase root: `.state/runs/2026-04-23/ai2/ai2_verify`
- publish target: `2/index.html`
- prompt file: `.github/codex/prompts/ai2_verify.md`
- timeout: `18 minutes`
- purpose: Cross-check the current AI/2 page against update outputs and policy drift for factual, logical, and platform-fit errors, and surface publishable review corrections even on no-news days.
- source model: raw source -> evidence -> claim -> verify -> score -> render -> publish
- fail-closed: if HQ, unicorn status, category, valuation, timestamps, or ranking claims are unsupported, stale, or contradictory, do not publish
- freshness contract: use explicit TTL / recency logic instead of timestamp-only refreshes
- no-news-day policy: if external updates are absent, refresh trend evidence, stale claims, score rationale, logic issues, or source-quality notes until a validated publish delta exists
- runner model: GitHub-hosted jobs are ephemeral; consume artifacts or committed state only
- decisive evidence: official English / filing / registry / developer-doc sources outrank Korean-language media
