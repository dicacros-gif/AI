# Codex Execution Notes

- agents: score_evidence_judge, unsupported_number_guard, ranking_consistency_guard, chronology_checker, citation_integrity_checker, manufacturer_strategy_agent, mna_scenario_agent, revenue_model_verifier, traction_metric_checker, market_size_trend_curator
- gates: deterministic_formula_used, unsupported_claims_zero_weight, ranking_tiebreak_applied, ai1_quantified_scorecard_applied, a_b_split_applied
- fail-closed fields: score_input, ranking_claim, on_device_proof_level, privacy_architecture

Work from the claim/evidence contract first. Do not trust uncited page text. Keep changes deterministic and conservative.
- scorecard version: ai1_mobile_oem_v2026_04
- scorecard weights: {"A": {"label": "12-month OEM partnership possibility", "points": 20}, "B": {"label": "Minority stake / bolt-on / strategic acquisition fit", "points": 20}, "C": {"label": "Device-side technical fit", "points": 20}, "D": {"label": "Product differentiation contribution", "points": 15}, "E": {"label": "Privacy and regulatory trust", "points": 10}, "F": {"label": "Business stability", "points": 10}, "G": {"label": "Execution ease", "points": 5}}
- required tracking fields: last_funding_date, last_round, lead_investor, oem_or_tier1_partnership_evidence, on_device_proof_level, sdk_maturity, privacy_architecture, strategic_fit_surface, mna_type, monthly_subscription_price, pricing_currency, revenue_share_ratio, revenue_share_basis, monetization_as_of_month

