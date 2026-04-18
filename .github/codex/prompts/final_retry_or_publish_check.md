You are running `final_retry_or_publish_check`.

Read:
1. `AGENTS.md`
2. `phase_context.md`
3. your assigned agent TOML
4. latest render/QA/retry state and both published HTML files

Goal:
- Perform the last consistency check before the run is considered complete.

Must confirm:
- canonical mapping is still correct
- visible timestamps include date, time, and `KST`
- rank order is contiguous and consistent
- no publish path drift
- no new blockers remain

Write the files named in `phase_context.md`.

