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
- Newly discovered candidate order must be identical across all downstream sections.
- Do not invent missing fields.

Write the agent JSON/MD files noted in `phase_context.md`.

