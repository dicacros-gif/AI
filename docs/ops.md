# Ops Guide

## Workflow Overview
- `.github/workflows/ai-watch-scheduler.yml` is the single scheduled automation entrypoint.
- Each scheduled run resolves exactly one phase.
- The workflow fans out the relevant Codex agent subset for that phase, consolidates outputs, validates the result, persists state, and only publishes when gates pass.

## Phase Descriptions
- `ai1_update` / `ai2_update`: latest updates for already-published companies only.
- `ai1_verify` / `ai2_verify`: factual, logical, timestamp, category, and legacy-rule cross-checking.
- `ai1_scout` / `ai2_scout`: new-candidate discovery with strict exclusion and source rules.
- `ai1_score` / `ai2_score`: evidence-backed scoring for approved new candidates only.
- `ai1_render` / `ai2_render`: conservative HTML updates with mandatory KST timestamps.
- `global_qa`: cross-page QA before publish acceptance.
- `retry_failed`: retry plan only for retryable issues.
- `republish_or_qa`: republish only if validated artifacts changed and gates pass.
- `final_retry_or_publish_check`: last consistency pass.

## Manual Re-Run Instructions
- Trigger the workflow with `workflow_dispatch`.
- Choose a specific phase or leave phase resolution to the scheduled slot.
- Optional: provide `target_date` in `YYYY-MM-DD`.
- Use manual runs for smoke tests, backfills, or validator-only checks.

## Retry Logic
- Retry decisions are based on validator outputs and `report_failures.py`.
- Timestamp, ranking, path, and missing-artifact issues are treated as retryable.
- Evidence, category, geography, or source-integrity failures are treated as non-retryable until content is fixed.

## State Persistence
- State artifacts are written under `.state/runs/YYYY-MM-DD/<page-or-global>/<phase>/`.
- The workflow uploads artifacts for every agent and consolidated phase output.
- The scheduler also persists the run state to the dedicated `ai-watch-state` branch for server-side history.

## Validator Usage
- `validate_ranking.py`: checks contiguous ranks and section-order consistency.
- `validate_publish.py`: checks publish targets, shell structure, timestamps, duplicate startups, and placeholders.
- `validate_state.py`: checks required state artifacts and hard-filter violations for new candidates.
- `validate_sources.py`: checks language/source-type integrity and missing `as-of` timing for numbers.
- `report_failures.py`: summarizes retryable vs non-retryable issues.

## Publish Gate
- Publish proceeds only from render or republish phases.
- Render must preserve shell structure and emit visible `KST` timestamps.
- Global QA or final check blockers stop publish.
- Existing published companies are retained by default; new-candidate rules are stricter than legacy cleanup.
- Normal recurring runs should update facts on existing companies and add new discoveries instead of pruning the published set.
- Explicit cleanup passes may remove hardware-first companies and South Korea headquartered companies below the active size threshold of `51` employees.

## Troubleshooting Order
1. Resolve missing state artifacts.
2. Fix path or timestamp formatting errors.
3. Fix ranking/order mismatches.
4. Fix source-integrity and English-evidence issues.
5. Re-run global QA.
6. Only then allow republish.

## Ranking Consistency Checks
- New candidate ranking must start at `1`.
- No gaps, no duplicates.
- Same order across list, evaluation, partnership, insight, and monitoring sections.

## Source-Quality Checks
- Prefer official English sources and authoritative English media.
- Korean-language sources are excluded from decisive facts and final publish citations.
- Hardware-first candidates should be excluded from promotion, and explicit cleanup can remove already published hardware-first companies.
