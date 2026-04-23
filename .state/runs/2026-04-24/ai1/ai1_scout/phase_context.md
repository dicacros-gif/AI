# AI Watch Phase Context

- phase: `ai1_scout`
- kind: `scout`
- domain: `ai1`
- page: `ai1`
- run date (KST): `2026-04-24`
- phase root: `.state/runs/2026-04-24/ai1/ai1_scout`
- publish target: `1/index.html`
- prompt file: `.github/codex/prompts/ai1_scout.md`
- timeout: `24 minutes`
- purpose: Discover new AI/1 candidates from the global pool excluding South Korea and China headquarters.
- source model: raw source -> evidence -> claim -> verify -> score -> render -> publish
- fail-closed: if HQ, unicorn status, category, valuation, timestamps, or ranking claims are unsupported, stale, or contradictory, do not publish
- freshness contract: use explicit TTL / recency logic instead of timestamp-only refreshes
- no-news-day policy: if external updates are absent, refresh trend evidence, stale claims, score rationale, logic issues, or source-quality notes until a validated publish delta exists
- runner model: GitHub-hosted jobs are ephemeral; consume artifacts or committed state only
- decisive evidence: official English / filing / registry / developer-doc sources outrank Korean-language media
