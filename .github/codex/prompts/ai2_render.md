You are running `ai2_render`.

Read:
1. `AGENTS.md`
2. `phase_context.md`
3. your assigned agent TOML
4. current `2/index.html`
5. same-run approved AI/2 artifacts

Goal:
- Render AI/2 conservatively with minimal HTML diff
- Preserve shell, palette buttons, dark-mode toggle, collapsible behavior, rank badges, and section structure
- If same-run state contains no net-new company or company-news delta, still render validated review-driven improvements such as refreshed trend cards, stale-claim fixes, score-rationale tightening, or corrected insight copy.

Hard rules:
- Publish only to `2/index.html`
- Keep all visible timestamps in `date + weekday + time + KST` format
- Existing companies remain unless the user explicitly asked for removal
- Only approved companies may be added or re-ranked
- Sort the full published set by approved total score descending
- Do not append new companies to the bottom
- Re-rank the full page from `1` through `N`
- Keep exactly the same order across sections `①` through `⑤`
- Keep the section index nav in the first visible top-left row
- Keep palette buttons and the dark-mode toggle in that same first visible top-right row
- Do not leave the index, palette buttons, or dark-mode toggle in a second sticky row
- In section `①`, collapsed rows must shrink to a real one-line summary row that shows only the company name
- Do not keep badges, meta text, or extra summary chips in the collapsed row
- Keep competitor-box copy slightly smaller than the main body text in section `①`
- Normalize awkward fragment endings before publish, for example `단단하 → 단단`, `다시 핵심으로 올라왔 → 다시 핵심`, `재편됐 → 재편`, `버려야 한 → 버려야 함`, `내재화했 → 내재화`, `보도됐 → 보도`, `확장했 → 확장`, and never leave orphaned sentence-final `'다`
- In section `①`, use a fixed-layout startup table with narrow widths, smaller cell padding, wrapped headers, and viewport-friendly sizing before allowing horizontal overflow
- In section `①`, merge `기업 + 설립/본사/직원`
- In section `①`, merge `창업자/핵심 경력 + 밸류에이션/펀딩·투자자`, and place each founder's key experience under that founder
- In section `①`, merge `매출·트랙션 + 비즈니스 모델 (매출·과금 상세)`
- In section `①`, merge `사업 상세 + 인사이트`
- Every section `①` row must keep a unique `data-row`
- In section `②`, each `eval-company` wrapper must contain its own `eval-company-hd` immediately followed by its own `eval-company-bd`
- In section `③`, manufacturer partnership boxes must render open by default
- Keep AI/2 strictly in a smartphone / handset / mobile-surface frame
- Remove TV, CTV, FAST, broadcast, smart-TV, living-room, smart-display, kiosk, and signage wording
- Section `⑥` title must be `Startup 상세 채점 기준표 (정량화 기준)`
- In section `⑥`, keep KPI labels readable, push `배점` and `채점 산출 기준` further right, avoid a wide right gutter, and keep the highest-score band highlighted in yellow
- In section `⑥`, render the quantified AI/2 smartphone-OEM adtech scorecard with weights `A20 / B20 / C12 / D12 / E12 / F12 / G12`
- In section `⑥`, show the public-company gate so listed companies publish with official `B = 0`
- In section `⑥`, show the gates `A5 = 0`, `B3 = 0 and B4 = 0`, `C4 = 0`, and `G4 = 0 with B2 <= 1`
- In section `⑥`, keep the block in normal UTF-8 Korean copy with no mojibake or broken placeholder markers
- Quantitative date chips must render as compact labels such as `'26.4월`
- Remove suffixes such as `확인`, `기준`, `official`, `pricing`, and `case` from visible date chips
- Quantitative date chips in startup rows should link to the nearest supporting source
- Do not render hero chips such as `한국/중국 본사 제외` or `영문 권위 소스 기준`
- In `비즈니스 모델 (매출·과금 상세)`, render monthly subscription fees, pricing bands, take rates, preload bounty models, or revenue-share ratios only when the latest authoritative source supports them
- Show monetization amounts or ratios with a visible `'26.x월` as-of label when possible
- If monetization detail is unavailable, render `undisclosed` or `unverified`
- Do not render visible `Samsung`, `삼성`, `삼성전자`, `Samsung Electronics`, `MX 사업부`, or `mx 사업부`
- Rewrite those references into neutral wording such as `휴대폰 제조사`, `leading OEM`, `major Android OEM`, or `strategic investor`
- Insight, article-link, and competitor strength/weakness copy must use concise bullet fragments
- Do not end bullet copy with `~다` or periods
- Rewrite awkward endings into natural fragments instead of deleting the last character only

Write the files named in `phase_context.md`.
