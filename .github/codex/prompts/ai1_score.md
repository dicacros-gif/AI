You are running `ai1_score`.

Read:
1. `AGENTS.md`
2. `phase_context.md`
3. your assigned agent TOML
4. same-run `ai1_scout` outputs

Goal:
- Score only approved new AI/1 candidates
- Keep existing published companies in place

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

Do not edit published HTML.
Write the files defined in `phase_context.md`.
