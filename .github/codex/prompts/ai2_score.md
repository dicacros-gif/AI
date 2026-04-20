You are running `ai2_score`.

Read:
1. `AGENTS.md`
2. `phase_context.md`
3. your assigned agent TOML
4. same-run `ai2_scout` outputs

Goal:
- Score only approved new AI/2 candidates
- Existing published companies remain in place

Scoring rules:
- Unsupported claims earn no points
- Software, service, engine, SDK, and enabling-tech leverage outranks hardware-first stories
- Score only from authoritative English-language evidence
- Use the quantified AI/2 smartphone-OEM adtech scorecard, not a generic ad-growth scorecard
- `A20` partnership possibility
- `B20` M&A possibility
- `C12` technology and IP
- `D12` revenue and finance
- `E12` market and regulation
- `F12` team strength
- `G12` competitive moat
- Apply famous VC / SI bonus only inside `B`, cap `B` at `20`
- Apply super-angel / repeat-founder bonus only inside `F`, cap `F` at `12`
- If the company is publicly listed, published `B` score must be forced to `0`
- If `A5 = 0`, commercial partnership is on hold
- If `B3 = 0` and `B4 = 0`, acquisition is on hold
- If `C4 = 0`, commercial deployment is blocked
- If `G4 = 0` and `B2 <= 1`, acquisition should fall back to commercial partnership
- Do not let generic ad-growth, cookie-era retargeting, retired ironSource-network narratives, or outdated Privacy Sandbox theses inflate scores
- Treat ATT, SKAN, AdAttributionKit, Privacy Sandbox drift, fraud, brand safety, and first-party measurement readiness as first-class scoring inputs
- Score partnership fit and acquisition fit separately
- Use the neutral phrase `휴대폰 제조사` in rationale rather than brand or division names
- Do not score companies already in a public commercial partnership with the evaluated handset manufacturer as new candidates for addition
- Record these fields when available:
- `last_funding_date`
- `last_round`
- `lead_investor`
- `oem_or_telco_partnership_evidence`
- `supported_oem_surfaces`
- `sdk_maturity`
- `measurement_stack_support`
- `privacy_readiness`
- `public_reach_or_device_footprint`
- `mna_type`
- `monthly_subscription_price`
- `pricing_currency`
- `revenue_share_ratio`
- `revenue_share_basis`
- `monetization_as_of_month`
- Tie-break by revenue strength, traction recency, primary-source quality, manufacturer/M&A fit, and defensibility

Do not edit published HTML.
Write the files defined in `phase_context.md`.
