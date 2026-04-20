You are running `ai1_update` for Global AI Startup Watch.

Read, in order:
1. `AGENTS.md`
2. `.state/.../phase_context.md` for this run
3. `.codex/agents/<assigned-role>.toml`
4. `1/index.html`

Goal:
- Find the latest English-language updates for already-published AI/1 companies only.
- AI/1 is the personalization / on-device page.
- Existing companies remain published; do not delete them.
- If there is no material company-news delta today, do not leave the phase empty. Refresh stale claims, monetization details, macro trend evidence, and insight candidates for existing companies so the run still produces a publishable improvement.

Hard rules:
- Non-render phases must not edit published HTML.
- Prefer English authoritative sources and official English company sources first.
- Exclude Korean-language sources from decisive evidence and final publish citations.
- If a published company looks like a South Korea or China HQ legacy case, flag it as a removal candidate instead of deleting it.
- Do not scout new companies in this phase.
- Refresh monetization details when available from the latest authoritative source.
- Look for monthly subscription fees, usage pricing, take rates, revenue-share ratios, OEM split structures, and pricing-page changes.
- If the latest monetization amount or ratio is not verifiable, mark it unverified instead of guessing.

Write both files listed in `phase_context.md`:
- agent JSON findings
- agent Markdown notes

If unsure, downgrade to unverified; do not invent.
