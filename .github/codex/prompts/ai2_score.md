You are running `ai2_score`.

Read:
1. `AGENTS.md`
2. `phase_context.md`
3. your assigned agent TOML
4. same-run `ai2_scout` outputs

Goal:
- Score only approved new AI/2 candidates.
- Existing published companies remain in place.

Scoring rules:
- Unsupported claims earn no points.
- Software/service/engine leverage outranks pure hardware-first stories.
- Score only from authoritative English-language evidence; Korean-language sources cannot justify points.
- Use the quantified AI/2 smartphone-OEM adtech scorecard below, not a generic ad-growth scorecard.
- `A` `20` = OEM ad-surface partnership possibility
- `A1` `5` OEM channel fit
- `A2` `4` integration burden
- `A3` `4` commercial proof
- `A4` `4` regional and customer coverage
- `A5` `3` brand and regulatory safety
- `B` `20` = minority stake / bolt-on / strategic acquisition fit
- `B1` `5` strategic synergy
- `B2` `4` deal feasibility
- `B3` `4` integration ease
- `B4` `4` asset scarcity
- `B5` `3` financial case
- `C` `15` = on-device, SDK, and deployment integration ease
- `D` `15` = data, privacy, and regulatory readiness
- `E` `15` = ad performance and commercial proof
- `F` `10` = strategic differentiation and defensibility
- `G` `5` = financial stability and execution
- Do not let generic ad-growth, cookie-era retargeting, or retired ironSource-network narratives inflate AI/2 scores.
- Treat ATT, SKAN, AdAttributionKit, Privacy Sandbox drift, fraud, brand safety, and first-party measurement readiness as first-class scoring inputs.
- Score partnership fit and acquisition fit separately; a company can be strong in one and weaker in the other.
- Use the neutral phrase `휴대폰 제조사` in rationale rather than brand or division names.
- Do not score companies already in a public commercial partnership with the evaluated handset manufacturer as new candidates for addition.
- Record these fields in score rationale and evidence mapping when available:
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
- Tie-break by revenue strength, traction recency, primary-source quality, manufacturer/M&A fit, and defensibility.
- Final new-candidate ranking must be deterministic and contiguous 1 -> N.

Do not edit published HTML.
Write the files named in `phase_context.md`.
