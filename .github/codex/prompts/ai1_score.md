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
- Use the quantified AI/1 smartphone-OEM scorecard below, not a generic AI SaaS scorecard.
- `A` `20` = 12-month OEM partnership possibility
- `A1` `6` device integration fit
- `A2` `4` privacy and regulatory fit
- `A3` `5` commercialization structure fit
- `A4` `5` strategic differentiation contribution
- `B` `20` = minority stake / bolt-on / strategic acquisition fit
- `B1` `6` proprietary technology and IP value
- `B2` `5` PMI integration ease
- `B3` `5` strategic gap coverage
- `B4` `4` deal feasibility
- `C` `20` = device-side technical fit
- `D` `15` = product differentiation contribution
- `E` `10` = privacy and regulatory trust
- `F` `10` = business stability
- `G` `5` = execution ease
- For AI/1, do not let ad-tech KPI or generic SaaS growth alone inflate the score.
- Distinguish `claimed`, `demo`, and `production` on-device proof levels.
- Penalize cloud-first products that market themselves as on-device without production-grade evidence.
- Score partnership fit and acquisition fit separately; a company can be strong in one and weaker in the other.
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
