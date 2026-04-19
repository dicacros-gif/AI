# Company Factcheck Skill

## Purpose
- Verify company claims at the claim level before scoring or publish

## Inputs
- normalized evidence records
- candidate record
- current claim ledger

## Outputs
- verified candidate record
- rejected or reserve record
- conflict notes

## Checklist
- Resolve company aliases into one canonical company identifier
- Verify headquarters from official legal or registry evidence
- Verify South Korea and China exclusion
- Verify unicorn or probable-unicorn status conservatively
- Verify category fit for AI/1 or AI/2
- Verify every decisive number and date has a source
- Fail closed when a core claim is missing, stale, unsupported, or contradictory

## Guardrails
- English authoritative sources outrank Korean-language secondary media
- Do not pass HQ as verified when it is ambiguous
- Do not score first and verify later
