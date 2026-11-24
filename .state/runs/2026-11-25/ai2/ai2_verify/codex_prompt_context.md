# Codex Execution Notes

- agents: regulatory_and_filings_checker, company_registry_checker, valuation_unicorn_guard, geography_exclusion_guard, korea_china_exclusion_guard, privacy_security_compliance_checker, contradiction_checker, unsupported_number_guard, timestamp_format_guard, section_order_consistency_guard, duplicate_startup_guard, category_leakage_guard, publish_path_guard, deprecation_watch_agent, privacy_sandbox_deprecation_guard
- gates: all_numbers_cited, all_dates_have_time, no_category_leakage
- fail-closed fields: unsupported_number, broken_timestamp, policy_drift

Work from the claim/evidence contract first. Do not trust uncited page text. Keep changes deterministic and conservative.
