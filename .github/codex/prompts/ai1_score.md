You are running `ai1_score`.

Read:
1. `AGENTS.md`
2. `phase_context.md`
3. your assigned agent TOML
4. same-run `ai1_scout` outputs

Goal:
- Score only approved new AI/1 candidates.
- Keep existing published companies in place; do not remove them here.

Scoring rules:
- Unsupported claims get zero credit.
- Prefer SW/service/engine/technology leverage over pure hardware-first stories.
- Score only from authoritative English-language evidence; Korean-language sources cannot justify points.
- Use the quantified AI/1 handset-manufacturer scorecard below, not a generic AI SaaS scorecard.
- `A` `20` = partnership possibility
- `A1` `5` mobile app commercialization and global active-usage proof
- `A2` `3` multi-device sync and web maturity
- `A3` `4` mobile-native / on-device UX architecture
- `A4` `4` OS-bundle business-model scenario fit
- `A5` `4` verified handset-manufacturer or Tier-1 platform partnership stage
- If `A5 = 0`, partnership is commercially on hold.
- `B` `20` = M&A possibility
- `B1` `5` comparable M&A exits in the vertical
- `B2` `5` acquisition-grade intangible assets
- `B3` `4` strategic-investor depth
- `B4` `3` model / serving-stack independence
- `B5` `3` survival time and org scale
- If the company is public, force `B1 = 0`, `B2 = 0`, and `B3 = 0`.
- If `B3 = 0` and `B4 = 0`, acquisition is on hold.
- `C` `12` = technology and IP
- `D` `12` = revenue and finance
- `E` `12` = market and regulation
- `F` `12` = team strength
- `G` `12` = moat and lock-in
- Respect category caps exactly; never let any section exceed its maximum.
- For AI/1, do not let ad-tech KPI or generic SaaS growth alone inflate the score.
- Distinguish `claimed`, `demo`, and `production` on-device proof levels.
- Penalize cloud-first products that market themselves as on-device without production-grade evidence.
- Score partnership fit and acquisition fit separately; a company can be strong in one and weaker in the other.
- Use the neutral phrase `휴대폰 제조사` in rationale rather than brand or division names.
- Do not score companies already in a public commercial partnership with the evaluated handset manufacturer as new candidates for addition.
- Record these fields in score rationale and evidence mapping when available:
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
- Tie-breaks: revenue strength, traction recency, primary-source quality, manufacturer/M&A fit, defensibility.
- Final approved new-candidate order must be deterministic 1 -> N.

Do not edit published HTML.
Write the files defined in `phase_context.md`.
