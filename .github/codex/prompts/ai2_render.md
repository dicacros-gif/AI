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
- Only approved newly discovered companies may be added or re-ranked.
- Newly discovered candidate order must stay identical across every downstream section.
- Keep the section index nav on the first visible line at the upper-left of the page.
- Palette buttons and the dark-mode toggle must sit on that same first visible top row at the upper-right.
- Do not render the section index as a second row below the toolbar.
- Do not leave palette buttons or the dark-mode toggle in a separate second sticky row.
- In section `①`, collapsed startup rows must shrink to a real one-line summary row with reduced height.
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
- Keep AI/2 strictly in a smartphone / handset / mobile-surface frame.
- Remove TV, CTV, FAST, broadcast, smart-TV, living-room, smart-display, kiosk, and signage wording from every published section.
- Do not invent unsupported numbers or missing fields.

Write the files named in `phase_context.md`.
