You are running `ai1_render`.

Read:
1. `AGENTS.md`
2. `phase_context.md`
3. your assigned agent TOML
4. the current `1/index.html`
5. same-run approved AI/1 state artifacts

Goal:
- Render AI/1 conservatively with minimal diff.
- Preserve HTML/CSS/JS shell, dark mode, palette buttons, collapsible sections, rank badges, and existing structure.

Hard rules:
- AI/1 must publish to `1/index.html`.
- Every visible generation timestamp must include date, weekday, time, and `KST`.
- Existing companies remain on the page.
- Only approved newly discovered candidates may be added or re-ordered.
- Do not render semiconductor fabless, chip vendors, or hardware-first vendors in AI/1.
- Replace removed fabless, chip, or hardware-first AI/1 companies with approved software, service, engine, or enabling-technology candidates.
- Newly discovered candidate order must be identical across all downstream sections.
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
- Section `①` insight, article-link, and competitor strength/weakness copy must use concise bullet fragments.
- Do not end section `①` insight/article/competitor copy with `~다` or periods.
- Do not satisfy this by deleting only the last `다`; rewrite the ending into a natural fragment.
- Prefer fragment endings such as `공개`, `명확`, `선명`, `강함`, `보임`, `노림`, `내재화`, `증명`, `정리`, `소개`, `보도`, `설명`, `분류`, `중요`, `유연`, `좁음`, `높음`, `약함`, `빠름`, `두꺼움`, `다룸`, `제시`, `확보`, `전달`, `요약`, `기록`, `언급`, `인수와 같음`, `나음`.
- Sections `②`, `③`, `④`, `⑤` must use concise bullet fragments, not sentence prose.
- Do not end bullets in sections `②`, `③`, `④`, `⑤` with `~다` or periods.
- Prefer fragment endings such as `노림`, `포인트`, `안전`, `빨라짐`, `상단 티어`.
- Keep AI/1 strictly in a smartphone / handset / mobile-surface frame.
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
- Do not render hero chips such as `한국/중국 본사 제외` or `영문 기사 기준`.
- Do not invent missing fields.

Write the agent JSON/MD files noted in `phase_context.md`.
