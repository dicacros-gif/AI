You are running `ai2_update` for Global AI Startup Watch.

Read:
1. `AGENTS.md`
2. `phase_context.md`
3. your assigned agent TOML
4. `2/index.html`

Goal:
- Find the latest English-language updates for already-published AI/2 companies only.
- AI/2 is the ad AI / mobile AdTech page.
- If there is no material company-news delta today, do not leave the phase empty. Refresh stale claims, monetization details, macro trend evidence, and insight candidates for existing companies so the run still produces a publishable improvement.

Daily intelligence contract:
- You must write `.state/.../ai2_update/daily_intel_findings.json`.
- Populate at least one of `newArticles`, `outdatedDataFixes`, `newQuantitativeData`, `monetizationUpdates`, `marketTrendUpdates`, `startupDiscoveryLeads`, `scoreRecalculationTriggers`, or `reviewActions`.
- Check stale quantitative fields first: valuation, funding amount, employee count, ARR, revenue, GMV/billings, MAU/DAU, device reach, pricing, take rate, revenue-share ratio, market size, CAGR, score.
- Prefer sources published or updated in the last 90 days; if no 90-day source exists, explicitly mark the latest authoritative source and why it remains usable.
- For every updated number, include `source_url`, `source_title`, `source_type`, `published_at` or `retrieved_at_utc`, `as_of_month`, and a short reason why the old page value changed or stayed unchanged.
- If no new article exists, perform a stale-data and score-basis audit, especially for traffic acquisition, pricing, take-rate, billings-vs-revenue, public-company M&A gate, Privacy Sandbox/ATT/SKAN/AdAttributionKit assumptions, and platform-policy drift.

Hard rules:
- Non-render phases must not edit published HTML.
- Prefer English authoritative and official English sources.
- Exclude Korean-language sources from decisive evidence and final publish citations.
- Legacy Korea/China HQ problems become removal candidates, not auto-deletions.
- Do not scout new companies in this phase.
- Refresh monetization details when available from the latest authoritative source.
- Look for monthly subscription fees, SaaS pricing bands, take rates, revenue-share ratios, preload bounty models, OEM split structures, and pricing-page changes.
- If the latest monetization amount or ratio is not verifiable, mark it unverified instead of guessing.

Write the JSON and Markdown files defined in `phase_context.md`.
