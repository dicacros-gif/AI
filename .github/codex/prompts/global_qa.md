You are running `global_qa`.

Read:
1. `AGENTS.md`
2. `phase_context.md`
3. your assigned agent TOML
4. `1/index.html`
5. `2/index.html`
6. same-run render/state artifacts for both pages

Goal:
- Evaluate both pages together before publish acceptance.

Daily intelligence QA contract:
- You must write `.state/.../global_qa/daily_intel_audit.json`.
- For each page, set `hasPublishableIntel` to true only when same-run artifacts prove at least one of: new article, outdated-data correction, new quantitative metric, monetization refresh, market/trend refresh, candidate discovery lead/reserve/rejection, score recalculation, or explicit stale-data review.
- If no current article exists, confirm the review-driven improvement and cite the artifact path that proves it.
- Block publish when update/scout/score artifacts are still placeholders, empty, or timestamp-only.

Must check:
- full daily run must not end as a silent no-op when fresh-news deltas are absent
- canonical page mapping (`AI/1` personalization, `AI/2` ad AI)
- `.html` publish targets only
- duplicate startups across pages
- missing visible time or missing `KST`
- ranking/order drift
- Korean-language decisive-source dependence or Korean-language final publish citations
- Korea/China new-candidate violations
- unicorn violations
- placeholder text
- broken shell structures
- review-driven improvement exists when no net-new external update exists

Write the files named in `phase_context.md`.
