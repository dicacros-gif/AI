# AI Watch Phase Context

- phase: `global_qa`
- kind: `global_qa`
- domain: `global`
- page: `global`
- run date (KST): `2026-04-22`
- phase root: `.state/runs/2026-04-22/global/global_qa`
- publish target: `n/a`
- prompt file: `.github/codex/prompts/global_qa.md`
- timeout: `20 minutes`
- purpose: Check AI/1 and AI/2 together for duplicates, leakage, citation integrity, timestamps, ranking consistency, shell regression, and no-noop daily-run compliance.
- source model: raw source -> evidence -> claim -> verify -> score -> render -> publish
- fail-closed: if HQ, unicorn status, category, valuation, timestamps, or ranking claims are unsupported, stale, or contradictory, do not publish
- freshness contract: use explicit TTL / recency logic instead of timestamp-only refreshes
- no-news-day policy: if external updates are absent, refresh trend evidence, stale claims, score rationale, logic issues, or source-quality notes until a validated publish delta exists
- runner model: GitHub-hosted jobs are ephemeral; consume artifacts or committed state only
- decisive evidence: official English / filing / registry / developer-doc sources outrank Korean-language media
