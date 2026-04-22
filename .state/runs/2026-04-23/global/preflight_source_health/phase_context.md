# AI Watch Phase Context

- phase: `preflight_source_health`
- kind: `preflight`
- domain: `global`
- page: `global`
- run date (KST): `2026-04-23`
- phase root: `.state/runs/2026-04-23/global/preflight_source_health`
- publish target: `n/a`
- prompt file: `script-only phase`
- timeout: `10 minutes`
- purpose: Verify GitHub runtime, secrets, source reachability assumptions, and last-run state availability before any research phase starts.
- source model: raw source -> evidence -> claim -> verify -> score -> render -> publish
- fail-closed: if HQ, unicorn status, category, valuation, timestamps, or ranking claims are unsupported, stale, or contradictory, do not publish
- freshness contract: use explicit TTL / recency logic instead of timestamp-only refreshes
- no-news-day policy: if external updates are absent, refresh trend evidence, stale claims, score rationale, logic issues, or source-quality notes until a validated publish delta exists
- runner model: GitHub-hosted jobs are ephemeral; consume artifacts or committed state only
- decisive evidence: official English / filing / registry / developer-doc sources outrank Korean-language media
