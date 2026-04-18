You are running `republish_or_qa`.

Read:
1. `AGENTS.md`
2. `phase_context.md`
3. your assigned agent TOML
4. the latest render and QA artifacts

Goal:
- Republish only if validated artifacts changed and publish gates pass.
- Otherwise run another QA-only decision and do not force a publish.

Hard rules:
- Keep canonical page mapping and canonical paths.
- Keep visible timestamps in `KST`.
- Existing companies stay unless manually removed later.

Write the files named in `phase_context.md`.

