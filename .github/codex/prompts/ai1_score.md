You are running `ai1_score`.

Read:
1. `AGENTS.md`
2. `phase_context.md`
3. your assigned agent TOML
4. same-run `ai1_scout` outputs

Goal:
- Score approved new AI/1 candidates
- Re-score existing published companies when fresh evidence, stale-claim repair, or review corrections materially change the score basis

Daily score contract:
- You must write `.state/.../ai1_score/score_recalc_requirements.json`.
- Record `changedInputs`, `recalculatedCompanies`, `unchangedButReviewedCompanies`, and `arithmeticChecks`.
- Recalculate scores when any stale quantitative field, pricing/BM detail, funding/valuation/employee count, ARR/revenue, MAU/DAU, market CAGR, partnership evidence, or on-device proof level changes.
- If no score changes, record which companies and fields were reviewed and why the current score remains valid.
- Total score arithmetic must be reproducible from A/B/C/D/E/F/G sub-scores, bonuses, gates, and caps.

Scoring rules:
- Unsupported claims get zero credit
- Prefer SW, service, engine, SDK, and enabling-technology leverage over hardware-first stories
- Score only from authoritative English-language evidence
- Use the quantified AI/1 handset-manufacturer scorecard, not a generic AI SaaS scorecard
- `A20` partnership possibility with a handset manufacturer
- `B20` M&A possibility
- `C12` technology and IP
- `D12` revenue and finance
- `E12` market and regulation
- `F12` team strength
- `G12` moat and lock-in
- If `A5 = 0`, partnership is commercially on hold
- If the company is public, force `B1 = 0`, `B2 = 0`, and `B3 = 0`
- If `B3 = 0` and `B4 = 0`, acquisition is on hold
- If `C4 = 0`, commercial deployment is blocked
- If `G4 = 0` and `B2 <= 1`, acquisition should fall back to commercial partnership
- Respect category caps exactly
- Distinguish `claimed`, `demo`, and `production` on-device proof levels
- Penalize cloud-first products that market themselves as on-device without production-grade evidence
- Score partnership fit and acquisition fit separately
- Use the neutral phrase `휴대폰 제조사` in rationale rather than brand or division names
- Do not score companies already in a public commercial partnership with the evaluated handset manufacturer as new candidates for addition
- Record these fields when available:
- `last_funding_date`
- `last_round`
- `lead_investor`
- `oem_or_tier1_partnership_evidence`
- `on_device_proof_level`
- `sdk_maturity`
- `privacy_architecture`
- `strategic_fit_surface`
- `mna_type`
- `monthly_subscription_price`
- `pricing_currency`
- `revenue_share_ratio`
- `revenue_share_basis`
- `monetization_as_of_month`
- Tie-break by revenue strength, traction recency, primary-source quality, manufacturer/M&A fit, and defensibility
- If no new candidate survives, still review whether published-company scores or rationale need correction so the full run does not become a no-op.

Do not edit published HTML.
Write the files defined in `phase_context.md`.
