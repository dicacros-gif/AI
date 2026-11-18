# Codex Execution Notes

- agents: score_evidence_judge, unsupported_number_guard, ranking_consistency_guard, chronology_checker, citation_integrity_checker, manufacturer_strategy_agent, mna_scenario_agent, revenue_model_verifier, traction_metric_checker, market_size_trend_curator, privacy_sandbox_deprecation_guard, deprecation_watch_agent
- gates: deterministic_formula_used, unsupported_claims_zero_weight, ranking_tiebreak_applied, deprecated_adtech_thesis_blocked, ai2_quantified_scorecard_applied, a_b_split_applied, current_measurement_policy_frame_applied
- fail-closed fields: score_input, ranking_claim, policy_drift, measurement_stack_support, privacy_readiness

Work from the claim/evidence contract first. Do not trust uncited page text. Keep changes deterministic and conservative.
- scorecard version: ai2_mobile_adtech_v2026_04_oem_quantified
- scorecard weights: {"A": {"label": "Partnership possibility", "points": 20}, "B": {"label": "M&A possibility", "points": 20}, "C": {"label": "Technology and IP", "points": 12}, "D": {"label": "Revenue and finance", "points": 12}, "E": {"label": "Market and regulation", "points": 12}, "F": {"label": "Team strength", "points": 12}, "G": {"label": "Competitive moat", "points": 12}}
- required tracking fields: last_funding_date, last_round, lead_investor, oem_or_telco_partnership_evidence, supported_oem_surfaces, sdk_maturity, measurement_stack_support, privacy_readiness, public_reach_or_device_footprint, is_public_company, mna_type, monthly_subscription_price, pricing_currency, revenue_share_ratio, revenue_share_basis, monetization_as_of_month

