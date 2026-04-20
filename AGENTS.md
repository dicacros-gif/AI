# AGENTS.md

## Operating Contract
- This repository runs a daily GitHub Actions-only automation
- Do not rely on local scheduler state, local terminal sessions, or persisted runner disk
- All phase outputs must be written to the repo state tree, uploaded as artifacts, or committed to the state branch
- Every full daily run must produce either a fresh external-update delta or a validated review-driven improvement; silent no-op runs are forbidden
- Non-render phases must not edit published HTML
- If unsure, downgrade to `unverified`; do not invent

## Canonical Page Mapping
- `AI/1` = mobile AI personalization, on-device analysis, personalized AI, recommendation engine, privacy-aware UX
- `AI/1` publish target = `1/index.html`
- `AI/2` = ad AI, mobile advertising technology and services, AdTech, SDK, DSP, retargeting, performance marketing, video AI advertising
- `AI/2` publish target = `2/index.html`
- Never publish mixed `.htm` and `.html` targets

## Canonical Schedule
- GitHub Actions orchestrator starts once per day at `00:05 KST`
- All later phases run through `needs` sequencing, not separate cron timing assumptions
- Daily target sequence:
- `00:05` `preflight_source_health`
- `00:10` `ai1_source_freshness_probe`
- `00:15` `ai1_update`
- `00:27` `ai1_verify`
- `00:40` `ai1_scout`
- `00:50` `ai1_entity_resolution`
- `00:57` `ai1_evidence_normalize`
- `01:04` `ai1_claim_ledger_build`
- `01:12` `ai1_candidate_verify`
- `01:20` `ai1_staleness_gate`
- `01:30` `ai1_score`
- `01:40` `ai1_render`
- `01:50` `ai2_source_freshness_probe`
- `01:57` `ai2_update`
- `02:09` `ai2_verify`
- `02:22` `ai2_scout`
- `02:32` `ai2_entity_resolution`
- `02:39` `ai2_evidence_normalize`
- `02:46` `ai2_claim_ledger_build`
- `02:54` `ai2_candidate_verify`
- `03:02` `ai2_staleness_gate`
- `03:12` `ai2_score`
- `03:22` `ai2_render`
- `03:32` `global_recency_recheck`
- `03:42` `global_qa`
- `03:50` `repair_retry`
- `03:57` `publish_if_changed`
- `04:02` `post_publish_smoke`

## Source Hierarchy
- Prefer authoritative English-language sources first
- Tier 0 = official English website, newsroom, official blog, product docs, pricing/help center, app store, filings, registry, investor page in English
- Tier 1 = Reuters, Bloomberg, TechCrunch, The Information, Wired, Fortune, Forbes, WSJ, Financial Times
- Tier 2 = Crunchbase, PitchBook, CB Insights, Dealroom, Tracxn, data.ai, Sensor Tower, Similarweb, Gartner, McKinsey, IDC, Forrester, VC research, papers, patents
- Korean-language sources may support context but cannot be decisive support for ranking, scoring, inclusion, exclusion, or numeric claims
- If no fresh external article is found for a given day, update the publish through review-driven improvements: stale-claim cleanup, trend refresh, score corrections, or logic fixes

## Eligibility Rules
- Newly discovered companies must not be headquartered in South Korea or China
- Use HQ / legal operating base, not founder ethnicity or nationality
- If HQ is unclear, fail closed and keep the company unverified
- Exclude unicorns from new discovery
- Prefer software, service, engine, SDK, and enabling-technology companies over hardware-first, chip, fabless, or device vendors
- If the user explicitly asked to remove companies already in a public commercial partnership with the evaluated handset manufacturer, remove them and close every rank gap

## Timestamp Rules
- Every visible generation timestamp must include date, weekday, time, and `KST`
- Never render date-only labels
- Never render relative-only labels such as `today` without a concrete timestamp
- Quantitative date chips should render as compact labels such as `'26.4월`
- Do not leave suffixes such as `확인`, `기준`, `official`, `pricing`, or `case` inside visible quantitative date chips

## Ranking Rules
- Re-rank the full published company set after each approved score update
- Do not append newly added companies to the bottom
- Rank order must be deterministic and contiguous from `1` through `N`
- The same order must appear in section `①`, section `②`, partnership ideas, investment insight, monitoring notes, and ranking artifacts

## Section 1 Layout Rules
- Section `①` title must stay `Startups list`
- Merge `기업` with `설립 / 본사 / 직원` into one column
- Merge `창업자 / 핵심 경력` with `밸류에이션 / 펀딩·투자자` into one column
- Place each founder's key experience directly under that founder
- Merge `매출·트랙션 / 비즈니스 모델 (매출·과금 상세)` into one column
- Merge `사업 상세 / 인사이트` into one column
- Prefer a fixed-layout table, narrow column widths, smaller cell padding, and wrapped headers before allowing horizontal overflow
- The table should fit inside a normal desktop viewport without horizontal scrolling whenever practical
- Collapsed rows must shrink to a real one-line summary row
- Every section `①` row must keep a unique `data-row`

## Section 2 Layout Rules
- Each `eval-company` wrapper must contain its own `eval-company-hd` immediately followed by its own `eval-company-bd`
- Never begin the next evaluation card before closing the current card body

## Section 3 Layout Rules
- Manufacturer partnership idea boxes must render open by default
- Keep section `③` strictly in a smartphone and handset frame
- Do not mention TV, CTV, FAST, broadcast, living-room, smart-display, kiosk, or signage use cases

## Copy Style Rules
- Sections `①`, `②`, `③`, `④`, and `⑤` must use concise bullet-style fragments, not sentence prose
- Do not end bullet copy with `~다` or periods
- Rewrite awkward endings into natural fragments rather than deleting the last character only
- Prefer fragment endings such as `공개`, `설명`, `명확`, `강함`, `약함`, `보임`, `빠름`, `높음`, `정리`, `소개`, `보도`, `분류`, `제시`, `전달`, `기록`, `요약`, `인수와 같음`, `나음`
- In competitor boxes, remove visible `강점` and `약점` labels because the box color already carries that meaning
- In competitor boxes, keep body sentences at normal weight and reserve bold emphasis for short high-signal keywords only

## Output Guardrails
- Do not render visible `Samsung`, `삼성`, `삼성전자`, `Samsung Electronics`, `MX 사업부`, or `mx 사업부`
- Rewrite those references into `휴대폰 제조사`, `leading OEM`, `major Android OEM`, or `strategic investor`
- Apply the same rule to list rows, article labels, insight boxes, partnership cards, score tables, and monitoring notes

## Monetization Detail Rules
- In `비즈니스 모델 (매출·과금 상세)`, always look for the latest authoritative monthly subscription fee, usage-based price, take rate, revenue-share ratio, preload bounty, or OEM split structure
- Prefer official pricing, help-center, developer, partner, investor, or contractual disclosure pages before media summaries
- When the latest monetization detail is found, include the amount or ratio plus a visible `'26.x월` as-of label
- If the amount or ratio cannot be verified, mark it `undisclosed` or `unverified`
- Do not guess subscription fees, take rates, or revenue-share percentages

## AI/1 Scorecard
- Weights = `A20 / B20 / C12 / D12 / E12 / F12 / G12`
- `A` = partnership possibility with a handset manufacturer
- `B` = M&A possibility
- `C` = technology and IP
- `D` = revenue and finance
- `E` = market and regulation
- `F` = team strength
- `G` = moat and lock-in
- Public companies force published `B1 = 0`, `B2 = 0`, and `B3 = 0`
- `A5 = 0` means partnership is on hold
- `B3 = 0` and `B4 = 0` means acquisition is on hold
- `C4 = 0` means commercial deployment is blocked
- `G4 = 0` and `B2 <= 1` means acquisition falls back to commercial partnership

## AI/2 Scorecard
- Weights = `A20 / B20 / C12 / D12 / E12 / F12 / G12`
- `A` = partnership possibility
- `B` = M&A possibility
- `C` = technology and IP
- `D` = revenue and finance
- `E` = market and regulation
- `F` = team strength
- `G` = moat and lock-in
- Public companies force official published `B = 0`
- Apply famous VC / SI bonus only inside `B`, cap `B` at `20`
- Apply super-angel / repeat-founder bonus only inside `F`, cap `F` at `12`
- `A5 = 0` means partnership is on hold
- `B3 = 0` and `B4 = 0` means acquisition is on hold
- `C4 = 0` means commercial deployment is blocked
- `G4 = 0` and `B2 <= 1` means acquisition falls back to commercial partnership
- Do not let cookie-era retargeting, retired ironSource-network assumptions, or deprecated Privacy Sandbox theses inflate scores

## Required Tracking Fields
- `last_funding_date`
- `last_round`
- `lead_investor`
- `oem_or_tier1_partnership_evidence`
- `oem_or_telco_partnership_evidence`
- `supported_oem_surfaces`
- `on_device_proof_level`
- `sdk_maturity`
- `measurement_stack_support`
- `privacy_architecture`
- `privacy_readiness`
- `strategic_fit_surface`
- `public_reach_or_device_footprint`
- `mna_type`
- `is_public_company`
- `monthly_subscription_price`
- `pricing_currency`
- `revenue_share_ratio`
- `revenue_share_basis`
- `monetization_as_of_month`

## Validation Commands
- `python scripts/validate_publish.py --page1 1/index.html --page2 2/index.html`
- `python scripts/validate_ranking.py 1/index.html 2/index.html`
- `python scripts/validate_state.py --run-root .state/runs/<date>`
- `python scripts/validate_sources.py --run-root .state/runs/<date>`

## Done Means
- All required phase reports exist
- No fail-closed gate remains open
- New discovery excludes South Korea and China HQ companies
- Published pages preserve shell, anchors, rank flow, and timestamp format
- Published pages use authoritative English-language support for decisive facts
- Published pages show monetization details only when the amount or ratio is supported
