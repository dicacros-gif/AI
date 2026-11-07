# Codex Execution Notes

- agents: qa_gatekeeper, duplicate_startup_guard, category_leakage_guard, citation_integrity_checker, unsupported_number_guard, timestamp_format_guard, ranking_consistency_guard, section_order_consistency_guard, html_regression_guard, publish_path_guard, english_source_priority_guard, korean_source_avoidance_guard, geography_exclusion_guard, korea_china_exclusion_guard, valuation_unicorn_guard, source_conflict_resolver, artifact_integrity_guard, deprecation_watch_agent, privacy_sandbox_deprecation_guard
- gates: no_duplicate_company_id, no_category_leakage, all_publish_blockers_clear, no_noop_daily_run
- fail-closed fields: headquarters_country, unicorn_status, ranking_claim, timestamp_label, publish_path, html_shell

Work from the claim/evidence contract first. Do not trust uncited page text. Keep changes deterministic and conservative.
