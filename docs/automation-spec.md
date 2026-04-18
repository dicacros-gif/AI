# Automation Spec

## Original Requirement Summary
- Run the entire Global AI Startup Watch workflow on GitHub servers even when the user's computer is off.
- Use `openai/codex-action@v1`, prompt-file based phases, repo-scoped `AGENTS.md`, `.codex/config.toml`, custom agent files, validators, state persistence, publish gating, retry logic, and KST scheduling.
- Enforce deterministic new-startup ranking, English-authoritative-source priority, visible KST timestamps, and South Korea / China exclusion for newly discovered startups.

## Conflicts Found
- The repository had older scheduled workflows that published unrelated or simplified output and would conflict with the new scheduler.
- The current published page mapping was reversed relative to the new canonical mapping.
- Visible write timestamps were using `기준 · 작성 HH:MM` instead of the canonical `HH:MM KST 기준` format.
- Existing published pages contain legacy companies and source patterns that do not fully comply with the new discovery rules.

## Canonical Decisions Taken
- Canonical page mapping is:
  - `AI/1` = personalization / on-device.
  - `AI/2` = ad AI / mobile AdTech.
- Canonical publish targets are:
  - `1/index.html`
  - `2/index.html`
- Legacy `.htm` usage is treated as invalid drift.
- Scheduled times use `Asia/Seoul` as the business timezone and are converted to UTC cron entries in the workflow.
- Existing published companies are retained by default.
- Legacy rule violations are surfaced as removal candidates rather than auto-deletions.
- Newly discovered companies are filtered more strictly:
  - no South Korea / China HQ
  - no unicorns
  - revenue evidence required
  - mobile relevance required
  - prefer software / service / engine / technology companies over pure hardware vendors

## Final Canonical Schedule
- `04:00 KST` `ai1_update` -> `0 19 * * *` UTC
- `04:20 KST` `ai1_verify` -> `20 19 * * *` UTC
- `04:30 KST` `ai1_scout` -> `30 19 * * *` UTC
- `04:40 KST` `ai1_score` -> `40 19 * * *` UTC
- `04:50 KST` `ai1_render` -> `50 19 * * *` UTC
- `05:00 KST` `ai2_update` -> `0 20 * * *` UTC
- `05:20 KST` `ai2_verify` -> `20 20 * * *` UTC
- `05:30 KST` `ai2_scout` -> `30 20 * * *` UTC
- `05:40 KST` `ai2_score` -> `40 20 * * *` UTC
- `06:00 KST` `ai2_render` -> `0 21 * * *` UTC
- `06:10 KST` `global_qa` -> `10 21 * * *` UTC
- `06:30 KST` `retry_failed` -> `30 21 * * *` UTC
- `07:00 KST` `republish_or_qa` -> `0 22 * * *` UTC
- `07:30 KST` `final_retry_or_publish_check` -> `30 22 * * *` UTC

## Ranking Rule
- Ranking applies to newly discovered approved candidates only.
- Rank must be contiguous from `1` through `N`.
- The same order is reused across all downstream sections and state artifacts.

## English Source Policy
- English-language official and authoritative sources are decisive.
- Korean-language sources are discouraged and cannot stand alone as decisive support for publish decisions.
- Official press releases count as company-distributed claims, not independent verification.

## Korea / China Exclusion Policy
- Newly discovered startups headquartered in South Korea or China are not eligible.
- If HQ is unclear, the candidate is held back.
- Existing published violations are flagged in verify/global QA as removal candidates and are not auto-deleted.

## Date + Time Display Policy
- All visible write/generation labels must include date, weekday, time, and `KST`.
- Date-only visible labels are invalid.

## Publish Target Normalization Decision
- Publish targets are normalized to `1/index.html` and `2/index.html`.
- The scheduler and validators fail on `.htm` drift.
- The render phase keeps the existing shell and applies only conservative page mutations.

