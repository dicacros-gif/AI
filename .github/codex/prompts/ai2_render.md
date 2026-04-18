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
- Do not invent unsupported numbers or missing fields.

Write the files named in `phase_context.md`.

