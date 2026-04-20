# Automation Specification

## Original Requirement Summary
- Run the full AI Watch pipeline on GitHub servers with no dependency on a local laptop
- Keep the workflow fully automated, stateful across phases, and publish-gated
- Prioritize English authoritative evidence
- Exclude newly discovered startups headquartered in South Korea or China
- Keep ranking deterministic and timestamps explicit in `KST`

## Problems Identified In The Prior Design
- The old model assumed many separate scheduled checkpoints instead of one orchestrated run
- Exact top-of-hour schedule slots were treated as reliable even though GitHub scheduled workflows can be delayed under load
- Update and scout phases mixed freshness checks, evidence collection, and verification without a clear contract
- Agent lists were richer than the actual claim-level verification model
- Runner behavior was described too much like a persistent server instead of an ephemeral job VM
- Freshness, TTL, and publish-time recheck were not explicit first-class phases
- Candidate verification happened too late, after scout outputs were already close to scoring

## Canonical Decisions
- One scheduled workflow starts the daily run
- The scheduled entrypoint is `04:03 KST`, not the top of the hour
- Sequencing is controlled by `needs`, not by multiple fragmented cron triggers
- Runtime timezone is `Asia/Seoul`
- GitHub-hosted runners are the canonical production runtime
- Runner-local state is not trusted across jobs
- State is passed through artifacts and the `ai-watch-state` branch
- Each phase is defined as a contract with explicit inputs, outputs, gates, retry policy, evidence contract, and fail-closed fields

## Canonical Page Mapping
- `AI/1` -> `1/index.html`
- `AI/2` -> `2/index.html`
- `.htm` drift is invalid and must fail validation

## Canonical Daily Flow
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

## Why The Schedule Changed
- GitHub scheduled workflows are not a hard real-time scheduler
- Top-of-hour load is a known reliability risk
- A single orchestrator plus `needs` is more reliable than many separate scheduled workflows

## Claim And Evidence Model
- Raw source snapshots are not the final truth model
- All decisive facts must pass through normalized evidence and claim artifacts
- Core artifacts
- `evidence.jsonl`
- `claims.jsonl`
- `claim_summary.json`
- `claim_conflicts.json`
- Claim schema requires:
- `claim_id`
- `company_id`
- `field`
- `value`
- `source_id`
- `source_type`
- `published_at`
- `retrieved_at_utc`
- `quote`
- `confidence`
- `ttl_days`
- `verification_status`
- Monetization claims should also track the latest verifiable monthly subscription amount, pricing currency, revenue-share ratio, revenue-share basis, and monetization as-of month when available

## AI/1 Quantified Scorecard Update
- The prior AI/1 scoring logic was too close to a generic AI company or recommendation API checklist
- AI/1 now uses a smartphone-OEM scorecard that separates partnership fit from acquisition fit
- `A` `20`
- `12-month OEM partnership possibility`
- `A1` `6` device integration fit
- `A2` `4` privacy and regulatory fit
- `A3` `5` commercialization structure fit
- `A4` `5` strategic differentiation contribution
- `B` `20`
- `minority stake / bolt-on / strategic acquisition fit`
- `B1` `6` proprietary technology and IP value
- `B2` `5` PMI integration ease
- `B3` `5` strategic gap coverage
- `B4` `4` deal feasibility
- `C` `20`
- `device-side technical fit`
- `D` `15`
- `product differentiation contribution`
- `E` `10`
- `privacy and regulatory trust`
- `F` `10`
- `business stability`
- `G` `5`
- `execution ease`
- AI/1 candidate verification must record:
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

## AI/1 Scoring Principles Added
- Do not let ad-tech KPI or generic SaaS growth logic inflate AI/1 OEM rankings
- Distinguish `claimed`, `demo`, and `production` on-device proof levels
- Penalize cloud-first products that market themselves as on-device without production-grade proof
- Separate `good partner` from `worth buying`
- A company can score well on partnership fit and still score lower on acquisition fit
- A company can score well on acquisition fit and still be too heavy or too risky for short-term OEM partnership

## AI/1 2026 Observation Areas Added
- semantic layer or personal knowledge graph
- hybrid on-device agents
- cross-device personalization
- privacy-preserving analytics infrastructure

## AI/2 Quantified Scorecard Update
- The prior AI/2 scoring logic was too generic for smartphone OEM decision-making
- AI/2 now uses a smartphone-OEM adtech scorecard that separates partnership fit from acquisition fit
- `A` `20`
- `partnership possibility`
- `A1` `5` commercial mobile app launch and active-user proof
- `A2` `3` multi-device sync and web maturity
- `A3` `4` mobile-native and on-device UX architecture
- `A4` `4` OEM OS and bundle business-model fit
- `A5` `4` verified partnership stage with OEM or Tier-1 platform
- `B` `20`
- `M&A possibility`
- `B0` `gate` public companies publish with official `B = 0`
- `B1` `5` recent global M&A exits in the same vertical
- `B2` `5` intangible assets attractive to large acquirers
- `B3` `4` strategic-investor depth
- `B4` `3` backbone and deep-learning-stack independence
- `B5` `3` survival period and organizational scale
- `C` `12`
- `technology and IP`
- `D` `12`
- `revenue and finance`
- `E` `12`
- `market and regulation`
- `F` `12`
- `team strength`
- `G` `12`
- `competitive moat`
- AI/2 candidate verification must record:
- `oem_or_telco_partnership_evidence`
- `supported_oem_surfaces`
- `sdk_maturity`
- `measurement_stack_support`
- `privacy_readiness`
- `public_reach_or_device_footprint`
- `is_public_company`
- `last_funding_date`
- `last_round`
- `lead_investor`
- `mna_type`
- `monthly_subscription_price`
- `pricing_currency`
- `revenue_share_ratio`
- `revenue_share_basis`
- `monetization_as_of_month`

## AI/2 Scoring Principles Added
- Do not let generic ad-growth stories outrank OEM execution factors
- Distinguish OEM-surface channel fit from pure DSP or creative-tool value
- Penalize outdated cookie-era retargeting theses and retired ironSource-network assumptions
- Treat ATT, SKAN, AdAttributionKit, Privacy Sandbox drift, fraud, and brand safety as first-class risk inputs
- Separate `good OEM partner` from `worth buying`

## AI/2 2026 Observation Areas Added
- OEM advertising reach and device footprint
- preload, app discovery, store, browser, and recommendation surfaces
- ATT, SKAN, AdAttributionKit, Privacy Sandbox drift, first-party measurement, and clean-room readiness
- alternative distribution and OEM inventory control

## New First-Class Phases
- `preflight_source_health`
- check runtime, branch state, basic prerequisites, and source health before expensive work
- `source_freshness_probe`
- detect changes from RSS, sitemap, ETag, Last-Modified, page hash, and app-store metadata before deeper fetches
- `entity_resolution`
- map legal name, brand name, app name, parent, domain, and aliases to one canonical company identifier
- `evidence_normalize`
- turn raw source findings into a standard evidence schema
- `claim_ledger_build`
- split facts into claim-level rows
- `candidate_verify`
- fail closed on HQ ambiguity, Korea or China HQ, unicorn status, category mismatch, stale core evidence, or missing citations before scoring
- `staleness_gate`
- remove TTL-expired core claims from publish eligibility
- `global_recency_recheck`
- refresh fast-moving official sources just before publish
- `publish_diff_guard`
- allow publish only when validated changes stay inside approved surfaces
- `post_publish_smoke`
- confirm public URLs, timestamps, anchors, and publish paths after publish

## Evidence And Freshness Policy
- Official release and newsroom claims: `1-7` days
- App-store metadata and version claims: `1-3` days
- Funding and valuation claims: `7-14` days
- Partnership and M&A signals: `7` days
- HQ and legal-entity claims: `30-90` days
- Platform-policy and regulatory drift claims: `7-14` days
- If a core claim is stale and not refreshed, fail closed

## Source Priority
- `regulatory filing / registry`
- `official company or investor source`
- `app store / developer docs`
- `authoritative English media`
- `secondary databases and analyst platforms`
- `community or social signals`
- Korean-language media can support context but cannot be decisive support for final publish facts

## Fail-Closed Fields
- `headquarters_country`
- `unicorn_status`
- `category`
- `funding_amount`
- `valuation`
- `ranking`
- `timestamp`
- `publish_path`

## Retry Policy
- Retry only transient failures
- network timeout
- 429
- 5xx
- temporary source unavailability
- artifact transport failure
- Do not retry fail-closed quality failures
- Korea or China HQ
- unicorn status confirmed
- stale core claim
- unsupported number
- missing citation
- unresolved source conflict
- category mismatch
- HTML shell regression
- AI/2 deprecation or policy drift blocker

## AI/2 Specific Policy Drift Guard
- AI/2 must explicitly track privacy and platform-policy deprecations
- Deprecated or retired Privacy Sandbox assumptions cannot be scored as current strategic upside
- The automation includes dedicated deprecation-watch and Privacy Sandbox guards in the contract model

## Rendering And Publish Decision
- Non-render phases do not edit production HTML
- Render phases are guarded by publish diff checks and validation
- Publish occurs only when validated content changed
- Workflow files, core templates, and automation control files are outside the normal automated publish surface

## Current Implementation Boundary
- The repository now enforces phase contracts, freshness probes, claim-ledger artifacts, candidate verification, recency recheck, and publish diff guarding
- Render remains constrained to dedicated render phases with HTML regression and publish-surface guards
- A future migration can move fully to data-first deterministic rendering, but the current implementation already narrows and validates the render surface
- AI/1 score scaffolding, prompts, and rendered criteria are aligned to the quantified mobile OEM model above
