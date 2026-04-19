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
- In section `①`, collapsed startup rows must shrink to a real one-line summary row with reduced height.
- Do not leave hidden text inside full-height table rows after collapse.
- Every section `①` startup row must keep a unique `data-row` key and collapse state must resolve from that key even after new rows are added.
- In section `②`, each `eval-company` wrapper must contain its own `eval-company-hd` immediately followed by its own `eval-company-bd`.
- Never begin the next `eval-company` block before closing the current card body.
- Section `①` insight, article-link, and competitor strength/weakness copy must use concise bullet fragments.
- Do not end section `①` insight/article/competitor copy with `~다` or periods.
- Prefer fragment endings such as `공개`, `명확`, `선명`, `강함`, `보임`, `노림`.
- Sections `②`, `③`, `④`, `⑤` must use concise bullet fragments, not sentence prose.
- Do not end bullets in sections `②`, `③`, `④`, `⑤` with `~다` or periods.
- Prefer fragment endings such as `노림`, `포인트`, `안전`, `빨라짐`, `상단 티어`.
- Keep AI/1 strictly in a smartphone / handset / mobile-surface frame.
- Remove TV, CTV, FAST, broadcast, smart-TV, living-room, smart-display, kiosk, and signage wording from every published section.
- Do not invent missing fields.

Write the agent JSON/MD files noted in `phase_context.md`.
