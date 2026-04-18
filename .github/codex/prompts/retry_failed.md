You are running `retry_failed`.

Read:
1. `AGENTS.md`
2. `phase_context.md`
3. your assigned agent TOML
4. the latest validator outputs and `publish_blockers.json`

Goal:
- Re-run only safe retryable work.
- Protect state integrity before speed.

Hard rules:
- Never force publish through blockers.
- Keep existing published companies unless a human later removes them.
- Do not invent success; report precise retry scope only.

Write the files named in `phase_context.md`.

