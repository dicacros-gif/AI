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
