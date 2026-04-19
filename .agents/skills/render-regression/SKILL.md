# Render Regression Skill

## Purpose
- Protect publish surfaces during render and publish phases

## Inputs
- validated page data
- rendered HTML output
- prior publish baseline

## Outputs
- render regression notes
- publish diff guard result
- smoke checklist

## Checklist
- Confirm publish path matches canonical mapping
- Confirm section order and anchors are preserved
- Confirm ranking order is consistent across sections
- Confirm visible timestamps include date, weekday, time, and `KST`
- Confirm diff stays inside approved publish surfaces
- Run post-publish smoke checks against public URLs

## Guardrails
- Non-render phases must not edit production HTML
- Do not widen automated publish scope to workflow files or core automation control files
- If shell regression is detected, fail closed
