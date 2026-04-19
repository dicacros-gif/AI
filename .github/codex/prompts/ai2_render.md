You are running `ai2_render`.

Read:
1. `AGENTS.md`
2. `phase_context.md`
3. your assigned agent TOML
4. current `2/index.html`
5. same-run approved AI/2 state artifacts

Goal:
- Render AI/2 conservatively with minimal HTML diff.
- Preserve shell, palette toggle, dark mode toggle, collapsible structure, rank badges, and section layout.

Hard rules:
- AI/2 must publish to `2/index.html`.
- Every visible generation timestamp must include date, weekday, time, and `KST`.
- Existing companies remain published.
- Only approved companies may be added or re-ranked.
- Sort the full published company set by approved total score in descending order.
- Do not append newly added companies to the bottom of the page.
- Re-rank the full published set from `1` through `N` after every approved score update.
- Use a deterministic stable tie-break order.
- Full company order must stay identical across every downstream section.
- Keep the section index nav on the first visible line at the upper-left of the page.
- Palette buttons and the dark-mode toggle must sit on that same first visible top row at the upper-right.
- Do not render the section index as a second row below the toolbar.
- Do not leave palette buttons or the dark-mode toggle in a separate second sticky row.
- In section `③`, manufacturer partnership idea boxes must render open by default.
- Do not leave section `③` partnership bodies collapsed on initial page load.
- In section `①`, collapsed startup rows must shrink to a real one-line summary row with reduced height.
- In section `①`, keep the integrated startup table materially narrower than the old 3000px-wide layout.
- Prefer tighter column widths and more natural line wrapping so more content is visible vertically without excessive horizontal scrolling.
- Do not leave hidden text inside full-height table rows after collapse.
- Every section `①` startup row must keep a unique `data-row` key and collapse state must resolve from that key even after new rows are added.
- In section `②`, each `eval-company` wrapper must contain its own `eval-company-hd` immediately followed by its own `eval-company-bd`.
- Never begin the next `eval-company` block before closing the current card body.
- In section `⑥`, render the quantified AI/2 smartphone-OEM adtech scorecard, not the older generic ad rubric.
- In section `⑥`, keep the full block in normal UTF-8 Korean copy with intact arrows and symbols.
- Do not leave mojibake, `??`, or broken question-mark placeholders anywhere in the criteria block.
- Keep the full AI/2 score weights as `A20 / B20 / C15 / D15 / E15 / F10 / G5`.
- Keep `A` as `OEM ad-surface partnership possibility`.
- Keep `B` as `minority stake / bolt-on / strategic acquisition fit`.
- In section `⑥`, show operational tracking fields such as last funding date, OEM or telco evidence, supported OEM surfaces, SDK maturity, measurement stack support, privacy readiness, public reach or device footprint, and M&A type.
- Remove stale or misleading AI/2 wording that treats cookie-era retargeting, retired ironSource-network assumptions, or deprecated Privacy Sandbox theses as current OEM upside.
- Section `①` insight, article-link, and competitor strength/weakness copy must use concise bullet fragments.
- Do not end section `①` insight/article/competitor copy with `~다` or periods.
- Do not satisfy this by deleting only the last `다`; rewrite the ending into a natural fragment.
- Prefer fragment endings such as `공개`, `명확`, `선명`, `강함`, `보임`, `노림`, `내재화`, `증명`, `정리`, `소개`, `보도`, `설명`, `분류`, `중요`, `유연`, `좁음`, `높음`, `약함`, `빠름`, `두꺼움`, `다룸`, `제시`, `확보`, `전달`, `요약`, `기록`, `언급`, `인수와 같음`, `나음`.
- Sections `②`, `③`, `④`, `⑤` must use concise bullet fragments, not sentence prose.
- Do not end bullets in sections `②`, `③`, `④`, `⑤` with `~다` or periods.
- Prefer fragment endings such as `노림`, `포인트`, `안전`, `빨라짐`, `상단 티어`.
- Keep AI/2 strictly in a smartphone / handset / mobile-surface frame.
- Remove TV, CTV, FAST, broadcast, smart-TV, living-room, smart-display, kiosk, and signage wording from every published section.
- Section `⑥` title must render as `Startup 상세 채점 기준표 (정량화 기준)`.
- In section `⑥`, widen the KPI column enough for readable labels and keep `배점` / `채점 산출 기준` aligned further to the right.
- Do not leave a wide right-side empty gutter in section `⑥`; tables should fill the card cleanly.
- In section `⑥`, keep the KPI column visibly wider, push the score and scoring-rule columns further right, and avoid a loose right gutter.
- In section `⑥`, auto-highlight the highest score band with yellow emphasis plus accent color, and keep low-score bands visually distinct.
- Quantitative date chips must render as compact labels such as `'26.4월`.
- Do not leave suffixes such as `확인`, `기준`, `official`, `pricing`, or `case` inside visible quantitative date chips.
- Replace vague labels such as `최근` with the current page month label.
- Quantitative date chips in startup rows should link to the nearest supporting source article.
- Do not render hero chips such as `한국/중국 본사 제외` or `영문 권위 소스 기준`.
- In `비즈니스 모델 (매출·과금 상세)`, render monthly subscription fees, pricing bands, take rates, preload bounty models, or revenue-share ratios only when the latest authoritative source supports them.
- Show monetization amounts or ratios with a visible `'26.x월` as-of label and nearest-source link where possible.
- If monetization detail is unavailable, render `undisclosed` or `unverified` instead of guessing.
- Do not render visible `Samsung` or `삼성` wording.
- Rewrite those references into neutral wording such as `leading OEM`, `major Android OEM`, or `strategic investor`.
- Do not invent unsupported numbers or missing fields.

Write the files named in `phase_context.md`.
