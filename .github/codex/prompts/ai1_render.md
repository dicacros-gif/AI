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
- Sections `②`, `③`, `④`, `⑤` must use concise bullet fragments, not sentence prose.
- Do not end bullets in sections `②`, `③`, `④`, `⑤` with `~다` or periods.
- Keep AI/1 strictly in a smartphone / handset / mobile-surface frame.
- Remove TV, CTV, FAST, broadcast, smart-TV, living-room, smart-display, kiosk, and signage wording from every published section.
- Do not invent missing fields.

Write the agent JSON/MD files noted in `phase_context.md`.
