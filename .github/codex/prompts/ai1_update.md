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

Hard rules:
- Non-render phases must not edit published HTML.
- Prefer English authoritative sources and official English company sources first.
- Korean-language sources cannot be decisive evidence.
- If a published company looks like a South Korea or China HQ legacy case, flag it as a removal candidate instead of deleting it.
- Do not scout new companies in this phase.

Write both files listed in `phase_context.md`:
- agent JSON findings
- agent Markdown notes

If unsure, downgrade to unverified; do not invent.

