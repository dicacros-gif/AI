# Global AI Startup Watch

## Project Overview
- This repository publishes two GitHub Pages reports on a fixed KST schedule.
- `AI/1` is the canonical personalization / on-device page.
- `AI/2` is the canonical ad AI / mobile AdTech page.
- The system is designed for GitHub-server-side execution through GitHub Actions and `openai/codex-action@v1`.
- Daily runs must complete on GitHub servers without any dependency on a local laptop, terminal session, or manual keep-alive.

## Repo Layout
- `1/index.html`: canonical publish target for AI/1.
- `2/index.html`: canonical publish target for AI/2.
- `.github/workflows/ai-watch-scheduler.yml`: scheduled GitHub Actions entrypoint.
- `.github/codex/prompts/`: phase prompt files used by Codex Action.
- `.codex/config.toml`: repo-scoped Codex configuration for GitHub Action runs.
- `.codex/agents/*.toml`: custom multi-agent role definitions used by the automation.
- `scripts/`: schedule resolution, phase scaffolding, validators, and reporting.
- `.state/runs/YYYY-MM-DD/...`: structured state tree per run.
- `docs/automation-spec.md`: canonical decisions and rule resolution.
- `docs/ops.md`: operations runbook.

## Canonical Page Mapping
- `AI/1` = mobile AI personalization, on-device data analysis, personalized AI, recommendation engine, privacy-aware UX.
- `AI/2` = ad AI, mobile advertising technology/services, AdTech, SDK, DSP, retargeting, performance marketing, video AI advertising.
- Publish targets are normalized to `AI/1/index.html` and `AI/2/index.html`.
- Mixed `.htm` / `.html` targets are not allowed.

## Canonical Schedule
- `04:00 KST` `ai1_update`
- `04:20 KST` `ai1_verify`
- `04:30 KST` `ai1_scout`
- `04:40 KST` `ai1_score`
- `04:50 KST` `ai1_render`
- `05:00 KST` `ai2_update`
- `05:20 KST` `ai2_verify`
- `05:30 KST` `ai2_scout`
- `05:40 KST` `ai2_score`
- `06:00 KST` `ai2_render`
- `06:10 KST` `global_qa`
- `06:30 KST` `retry_failed`
- `07:00 KST` `republish_or_qa`
- `07:30 KST` `final_retry_or_publish_check`

## English-Source-First Hierarchy
- Tier 0: official English company site, newsroom, blog, docs, pricing, app store, regulatory filings, registry, investor portfolio page in English.
- Tier 1: Reuters, Bloomberg, TechCrunch, The Information, Wired, Fortune, Forbes, WSJ, Financial Times.
- Tier 2: Crunchbase, PitchBook, CB Insights, Dealroom, Tracxn, data.ai, Sensor Tower, Similarweb, Gartner, McKinsey, IDC, Forrester, a16z and peer VC content, patents, papers, arXiv.
- Tier 3: Product Hunt, GitHub, Hacker News, Reddit, X, LinkedIn.

## Hard Filters
- Newly discovered startups must exclude South Korea and China headquarters.
- If headquarters is unclear, the new candidate is ineligible until verified.
- Newly discovered startups must not be unicorns.
- Newly discovered startups need revenue evidence.
- Newly discovered startups need technology differentiation.
- Newly discovered startups need clear mobile-first, mobile-native, or deeply mobile-surface relevance.
- Hardware-first vendors are excluded from new-candidate promotion.
- Prefer software, service, engine, and enabling technology companies over pure hardware vendors.
- Newly discovered candidates can come from any global region except South Korea or China headquarters, and daily discovery should select the strongest evidence-backed eligible candidates from the full global pool.
- `AI/1` publish set excludes semiconductor fabless, chip vendors, and hardware-first companies.
- If an `AI/1` company is primarily a semiconductor, chip, fabless, or hardware vendor, replace it with a software, service, engine, or enabling-technology company backed by English-language evidence.
- Existing published companies stay on the page during recurring runs; automation should refresh facts and add newly discovered candidates instead of pruning the legacy set.
- Legacy violations are flagged as removal candidates for later human review and are not auto-deleted by automation.
- Recurring daily updates should preserve already-published companies and focus on refreshing facts plus adding newly discovered candidates.

## Ranking Rule
- Newly discovered startups only are ranked.
- Rank must start at `1` and continue contiguously through `N`.
- The exact same approved order must be reused across startup list, evaluation, manufacturer partnership, investment insight, monitoring/red-flag sections, anchors, and state artifacts.
- No duplicate ranks.
- No missing ranks.
- No reversed downstream order.
- In section `①` startup list tables, clicking a company row must collapse it to a true single-line summary row.
- Collapsed rows must reduce vertical height visibly; do not leave empty multi-line row height behind.
- Collapsed row summary should keep the top-line essentials only, such as rank, company, and compact meta.

## Date + Time Display Rule
- Every visible write or generation timestamp must include date, weekday, time, and `KST`.
- Example: `'26.4.17 (금) 06:10 KST 기준`
- Date-only labels are forbidden.

## Bullet Style Rule
- Sections `②`, `③`, `④`, `⑤` must use concise bullet-fragment writing.
- Do not end those bullets with sentence-final `~다`.
- Do not end those bullets with periods.
- Prefer noun phrases, short action phrases, and `확인 필요` / `점검 필요` style fragments.

## Do-Not Rules
- Do not use Korean-language sources as decisive support or final publish citations.
- Do not hallucinate undisclosed funding, revenue, headcount, valuation, partnership, or investor details.
- Do not auto-delete existing published companies during recurring automation; only flag issues for later human review.
- Exception: if the user explicitly requests removing fabless, chip, or hardware-first companies from `AI/1`, obey the request in the next render.
- Do not edit published HTML in non-render phases.
- Do not regenerate the entire shell if a minimal diff is enough.
- If unsure, downgrade to unverified; do not invent.

## Done Criteria
- GitHub workflow implemented and scheduled.
- Codex prompt files implemented.
- Repo-scoped `.codex` config implemented.
- Custom agent files implemented.
- Validators implemented.
- State persistence implemented.
- Publish is gated behind validators.
- Canonical page mapping, timestamp rule, rank rule, and exclusion rules are enforced.

## Validation Commands
- `python scripts/generate_codex_assets.py`
- `python scripts/run_phase.py --mode smoke --run-date 2026-04-18`
- `python scripts/validate_ranking.py 1/index.html 2/index.html`
- `python scripts/validate_publish.py --page1 1/index.html --page2 2/index.html`
- `python scripts/validate_state.py --run-root .state/runs/2026-04-18`
- `python scripts/validate_sources.py .state/runs/2026-04-18/global/global_qa/global_qa.json`

## HTML Editing Rule
- Preserve CSS shell, JS behavior, palette buttons, dark/light toggle, collapsible sections, rank badges, summary score blocks, competitor boxes, insight panels, timestamp chips, and footer/header/hero structure.
- Render phases must use minimum-diff edits to existing HTML whenever possible.
