# Source Freshness Skill

## Purpose
- Check whether a source changed before running a more expensive fetch or verification step

## Inputs
- source URL list
- prior snapshot hash or metadata
- current run date

## Outputs
- freshness decision per source
- changed source list
- unchanged source list
- fetch priority notes

## Checklist
- Check RSS or Atom feed when available
- Check sitemap `lastmod` when available
- Check `ETag` and `Last-Modified` when available
- Check page hash when metadata is missing
- Check app-store version metadata for app surfaces
- Write results into the phase freshness artifact before deeper collection

## Guardrails
- Do not treat freshness as proof of truth
- Do not skip citation checks because a page changed
- If freshness cannot be determined for a fast-moving source, mark it for conservative recheck
