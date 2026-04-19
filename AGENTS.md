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

## Server-Only Runtime Rule
- Recurring production work must run only on GitHub-hosted runners through GitHub Actions.
- Do not rely on a local laptop, local terminal, local scheduler, or local background session for update, scoring, render, publish, or retry work.
- Manual intervention should use `workflow_dispatch` on GitHub, not local script execution.
- Local validation can be treated as development-only, but production update/publish paths are server-only.

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
- The top navigation index row must stay on the first visible line at the upper-left of the page.
- Palette buttons and the dark-mode toggle must share that same first visible top row at the upper-right of the page.
- Do not leave the section index as a second-row bar under the toolbar.
- Do not leave palette buttons or the dark-mode toggle in a second sticky row under the top navigation.
- In section `①` startup list tables, clicking a company row must collapse it to a true single-line summary row.
- Collapsed rows must reduce vertical height visibly; do not leave empty multi-line row height behind.
- Collapsed row summary should keep the top-line essentials only, such as rank, company, and compact meta.
- Every `tr-main` row in section `①` must have a unique `data-row` key.
- Collapse / expand logic must resolve state from each row's own `data-row`; do not rely on fragile positional assumptions as the list grows.
- In section `②`, every `eval-company` card must keep its own `eval-company-hd` and `eval-company-bd` inside the same wrapper.
- Do not start a new `eval-company` card before the previous card's `eval-company-bd` has been emitted and closed.
- Section `⑥` title must stay `Startup 상세 채점 기준표 (정량화 기준)`.
- In section `⑥`, widen the left KPI column enough for readable labels, while keeping `배점` and `채점 산출 기준` aligned further to the right.
- In section `⑥`, remove avoidable right-side blank space and let the table fill the card cleanly.
- Section `⑥` tables should fill the available card width; do not leave a wide empty gutter on the right.
- In section `⑥`, keep the KPI column visibly wider, push the score and scoring-rule columns further right, and avoid a loose right gutter.
- In section `⑥`, auto-highlight the highest score band with yellow emphasis plus accent color, and keep low-score bands visually distinct.
- Quantitative date chips should show only compact labels such as `'26.4월`.
- Do not leave suffixes such as `확인`, `기준`, `official`, `pricing`, or `case` inside visible quantitative date chips.
- Replace vague labels such as `최근` with the current visible month label on the page.
- Quantitative date chips in startup rows should link to the nearest supporting source.
- Do not render hero chips such as `한국/중국 본사 제외`, `영문 기사 기준`, or `영문 권위 소스 기준`.

## Date + Time Display Rule
- Every visible write or generation timestamp must include date, weekday, time, and `KST`.
- Example: `'26.4.17 (금) 06:10 KST 기준`
- Date-only labels are forbidden.

## Bullet Style Rule
- Section `①` insight, article-link, and competitor strength/weakness copy must use concise bullet-fragment writing.
- Do not end section `①` insight/article/competitor copy with sentence-final `~다`.
- Never satisfy this rule by trimming only the final `다`; rewrite the ending into a natural fragment instead.
- Prefer fragment endings such as `공개`, `명확`, `선명`, `강함`, `보임`, `노림`, `내재화`, `증명`, `정리`, `소개`, `보도`, `설명`, `분류`, `중요`, `유연`, `좁음`, `높음`, `약함`, `빠름`, `두꺼움`, `다룸`, `제시`, `확보`, `전달`, `요약`, `기록`, `언급`, `인수와 같음`, `나음`.
- Sections `②`, `③`, `④`, `⑤` must use concise bullet-fragment writing.
- Do not end those bullets with sentence-final `~다`.
- Do not end those bullets with periods.
- Prefer noun phrases, short action phrases, and `확인 필요` / `점검 필요` style fragments.
- Prefer fragment endings such as `노림`, `포인트`, `안전`, `빨라짐`, `상단 티어`.

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
- `AI/1` and `AI/2` must stay in a smartphone / handset / mobile-surface frame.
- Do not write TV, CTV, smart TV, FAST, broadcast, set-top, or living-room media framing into published HTML.
- Do not write smart display, kiosk, signage, or store-hardware framing as the primary OEM angle.
- Sections `③`, `④`, `⑤`, `⑥` must be described from a smartphone manufacturer point of view only.
