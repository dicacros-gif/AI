# Ops Guide

## Workflow Overview
- `.github/workflows/ai-watch-scheduler.yml` is now a single daily orchestrator workflow.
- The scheduler starts once per day at `04:03 KST` and then uses `needs:` to enforce phase order.
- The workflow runs only on GitHub-hosted runners.
- Runner-local state is treated as ephemeral; every phase writes state to `.state/runs/YYYY-MM-DD/...` and uploads artifacts for cross-job restore.
- Publish happens only after global QA, retry classification, and publish-diff checks pass.
- Scheduled execution is approximate, not hard real-time.
- Scheduled workflows run from the default branch and should always remain active through normal repository activity.

## Why The Schedule Changed
- GitHub scheduled workflows can be delayed or dropped during heavy load, especially at the start of the hour.
- The workflow therefore avoids `04:00`, `05:00`, `06:00`, and `07:00` exact top-of-hour triggers.
- The repo now uses one orchestrator entrypoint instead of many fragmented cron triggers.
- If a scheduled run is missed or delayed, use `workflow_dispatch` to replay the target date rather than adding more fragmented cron entries.

## Daily Target Timeline
- `04:03 KST` `preflight_source_health`
- `04:08 KST` `ai1_source_freshness_probe`
- `04:13 KST` `ai1_update`
- `04:25 KST` `ai1_verify`
- `04:38 KST` `ai1_scout`
- `04:48 KST` `ai1_entity_resolution`
- `04:55 KST` `ai1_evidence_normalize`
- `05:02 KST` `ai1_claim_ledger_build`
- `05:10 KST` `ai1_candidate_verify`
- `05:18 KST` `ai1_staleness_gate`
- `05:28 KST` `ai1_score`
- `05:38 KST` `ai1_render_staging`
- `05:48 KST` `ai2_source_freshness_probe`
- `05:55 KST` `ai2_update`
- `06:07 KST` `ai2_verify`
- `06:20 KST` `ai2_scout`
- `06:30 KST` `ai2_entity_resolution`
- `06:37 KST` `ai2_evidence_normalize`
- `06:44 KST` `ai2_claim_ledger_build`
- `06:52 KST` `ai2_candidate_verify`
- `07:00 KST` `ai2_staleness_gate`
- `07:10 KST` `ai2_score`
- `07:20 KST` `ai2_render_staging`
- `07:30 KST` `global_recency_recheck`
- `07:40 KST` `global_qa`
- `07:48 KST` `repair_retry`
- `07:55 KST` `publish_if_changed`
- `08:00 KST` `post_publish_smoke`

## Phase Contract Model
- `source_freshness_probe`
  - check RSS, sitemap, ETag, Last-Modified, page hash, app-store version, and newsroom changes before heavy fetch work
- `evidence_normalize`
  - turn raw source outputs into one evidence schema with `source_id`, `source_type`, `published_at`, `retrieved_at_utc`, `quote`, `confidence`, and `ttl_days`
- `claim_ledger_build`
  - split facts into claim-level rows for HQ, funding, valuation, dates, numbers, partnerships, and ranking claims
- `candidate_verify`
  - fail closed on HQ ambiguity, South Korea or China HQ, unicorn status, category mismatch, unsupported numbers, or missing citations before scoring
- `staleness_gate`
  - fail closed on TTL-expired core claims
- `global_recency_recheck`
  - re-check fast-moving official sources just before publish
- `publish_if_changed`
  - publish only when validated content changed and the diff stays inside allowed publish surfaces

## AI/1 Score Model
- AI/1 score uses a quantified A-G smartphone-OEM model
- `A 20`
  - 12-month OEM partnership possibility
- `B 20`
  - minority stake / bolt-on / strategic acquisition fit
- `C 20`
  - device-side technical fit
- `D 15`
  - product differentiation contribution
- `E 10`
  - privacy and regulatory trust
- `F 10`
  - business stability
- `G 5`
  - execution ease
- AI/1 score must record and cite:
  - `on_device_proof_level`
  - `sdk_maturity`
  - `privacy_architecture`
  - `oem_or_tier1_partnership_evidence`
  - `last_funding_date`
  - `last_round`
  - `lead_investor`
  - `strategic_fit_surface`
  - `mna_type`
  - `monthly_subscription_price`
  - `pricing_currency`
  - `revenue_share_ratio`
  - `revenue_share_basis`
  - `monetization_as_of_month`

## AI/2 Score Model
- AI/2 score uses a quantified A-G smartphone-OEM adtech model
- `A 20`
  - OEM ad-surface partnership possibility
- `B 20`
  - minority stake / bolt-on / strategic acquisition fit
- `C 15`
  - on-device, SDK, and deployment integration ease
- `D 15`
  - data, privacy, and regulatory readiness
- `E 15`
  - ad performance and commercial proof
- `F 10`
  - strategic differentiation and defensibility
- `G 5`
  - financial stability and execution
- AI/2 score must record and cite:
  - `oem_or_telco_partnership_evidence`
  - `supported_oem_surfaces`
  - `sdk_maturity`
  - `measurement_stack_support`
  - `privacy_readiness`
  - `public_reach_or_device_footprint`
  - `last_funding_date`
  - `last_round`
  - `lead_investor`
  - `mna_type`
  - `monthly_subscription_price`
  - `pricing_currency`
  - `revenue_share_ratio`
  - `revenue_share_basis`
  - `monetization_as_of_month`

## Skills Layout
- Repeatable workflow guidance lives under `.agents/skills/`
- `source-freshness`
  - source change detection before deep fetch
- `company-factcheck`
  - claim-level HQ, unicorn, category, and citation checks
- `render-regression`
  - render-surface and publish-diff protection

## Source Freshness And TTL
- official release / official newsroom claims: `1-7` days
- app-store metadata and version claims: `1-3` days
- funding / valuation claims: `7-14` days
- partnership / M&A signals: `7` days
- HQ / legal entity claims: `30-90` days
- platform policy / regulatory drift: `7-14` days
- pricing, take-rate, subscription, and revenue-share claims: `7-14` days

## Source Priority
- `Tier 0`
  - official English site, newsroom, blog, product docs, pricing/help center, app store, filings, registry, investor portfolio page in English
- `Tier 1`
  - Reuters, Bloomberg, TechCrunch, The Information, Wired, Fortune, Forbes, WSJ, Financial Times
- `Tier 2`
  - Crunchbase, PitchBook, CB Insights, Dealroom, Tracxn, data.ai, Sensor Tower, Similarweb, Gartner, McKinsey, IDC, Forrester, a16z and similar VC research, patents, papers
- Korean-language media cannot be decisive support for final publish facts

## Artifact And State Flow
- each phase writes:
  - `run_manifest.json`
  - `phase_contract.json`
  - required output files for that phase kind
- `validate_state.py` checks those phase contracts for required gates, fail-closed fields, and evidence contract keys
- each major job uploads phase directories as artifacts
- downstream jobs download prior artifacts and restore `.state` via `scripts/restore_phase_artifacts.py`
- final state is pushed to the `ai-watch-state` branch

## Manual Re-Runs
- use `workflow_dispatch`
- choose `all` for a full orchestrator run
- choose a specific phase for a server-side single-phase run
- use `target_date` when backfilling or replaying a given KST run date
- do not run production update or publish paths from a local terminal

## Retry Logic
- retry only bounded transient failures
  - timeout
  - 429 / 5xx
  - artifact transport issues
  - temporary source unavailability
- do not retry fail-closed quality issues
  - South Korea / China HQ
  - unicorn confirmed
  - missing citation
  - category leakage
  - unresolved source conflict
  - stale core claim
  - HTML shell regression
  - deprecated platform-policy thesis in AI/2

## Publish Gate
- `publish_if_changed` runs only after `global_qa` and `repair_retry`
- validators must pass:
  - `validate_publish.py`
  - `validate_ranking.py`
  - `validate_state.py`
  - `validate_sources.py`
- pages are committed only when validated page diffs exist
- workflow, templates, and automation control files are not part of the normal automated publish diff

## Troubleshooting Order
1. preflight failure
2. freshness probe failure
3. evidence / claim ledger schema failure
4. candidate verify fail-closed issue
5. staleness gate failure
6. global QA blocker
7. publish diff blocker
8. post-publish smoke failure
