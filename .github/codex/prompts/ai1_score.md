You are running `ai1_score`.

Read:
1. `AGENTS.md`
2. `phase_context.md`
3. your assigned agent TOML
4. same-run `ai1_scout` outputs

Goal:
- Score only approved new AI/1 candidates.
- Keep existing published companies in place; do not remove them here.

Scoring rules:
- Unsupported claims get zero credit.
- Prefer SW/service/engine/technology leverage over pure hardware-first stories.
- Score only from authoritative English-language evidence; Korean-language sources cannot justify points.
- Tie-breaks: revenue strength, traction recency, primary-source quality, manufacturer/M&A fit, defensibility.
- Final approved new-candidate order must be deterministic 1 -> N.

Do not edit published HTML.
Write the files defined in `phase_context.md`.
