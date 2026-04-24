from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ACTION_FIELDS = (
    "newArticles",
    "outdatedDataFixes",
    "newQuantitativeData",
    "monetizationUpdates",
    "marketTrendUpdates",
    "startupDiscoveryLeads",
    "scoreRecalculationTriggers",
    "reviewActions",
)

DISCOVERY_FIELDS = (
    "candidateUniverse",
    "reservedBecauseUnverified",
    "rejectedBecauseIneligible",
)

SCORE_FIELDS = (
    "changedInputs",
    "recalculatedCompanies",
    "unchangedButReviewedCompanies",
    "arithmeticChecks",
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def non_empty_items(data: dict[str, Any], fields: tuple[str, ...]) -> list[Any]:
    items: list[Any] = []
    for field in fields:
        value = data.get(field)
        if isinstance(value, list):
            items.extend(item for item in value if item)
        elif value:
            items.append(value)
    return items


def is_placeholder(data: dict[str, Any]) -> bool:
    return str(data.get("status", "")).lower() == "placeholder_requires_agent_update"


def validate_update(path: Path, domain: str) -> list[str]:
    if not path.exists():
        return [f"{domain}: missing daily intelligence findings at {path}."]
    data = load_json(path)
    issues: list[str] = []
    if is_placeholder(data):
        issues.append(f"{domain}: daily_intel_findings.json is still the placeholder template.")
    if not non_empty_items(data, ACTION_FIELDS):
        issues.append(
            f"{domain}: update phase has no new article, outdated-data fix, quantitative-data refresh, "
            "monetization update, trend update, startup lead, score trigger, or review action."
        )
    return issues


def validate_scout(path: Path, domain: str) -> list[str]:
    if not path.exists():
        return [f"{domain}: missing candidate discovery plan at {path}."]
    data = load_json(path)
    issues: list[str] = []
    if is_placeholder(data):
        issues.append(f"{domain}: candidate_discovery_plan.json is still the placeholder template.")
    if not data.get("searchedThemes"):
        issues.append(f"{domain}: scout phase did not record concrete searched themes.")
    if not non_empty_items(data, DISCOVERY_FIELDS):
        issues.append(
            f"{domain}: scout phase recorded no candidate lead, reserve, or rejection; discovery work is not proven."
        )
    return issues


def validate_score(path: Path, domain: str) -> list[str]:
    if not path.exists():
        return [f"{domain}: missing score recalculation requirements at {path}."]
    data = load_json(path)
    issues: list[str] = []
    if is_placeholder(data):
        issues.append(f"{domain}: score_recalc_requirements.json is still the placeholder template.")
    if not non_empty_items(data, SCORE_FIELDS):
        issues.append(f"{domain}: score phase did not record recalculation or explicit score review work.")
    return issues


def validate_recency(path: Path) -> list[str]:
    if not path.exists():
        return [f"global: missing publish-time recency watchlist at {path}."]
    data = load_json(path)
    issues: list[str] = []
    if is_placeholder(data):
        issues.append("global: recency_watchlist.json is still the placeholder template.")
    if not non_empty_items(data, ("recheckedCompanies", "staleOrChangedClaims", "publishTimeRisks")):
        issues.append("global: recency recheck did not record companies, stale/changed claims, or publish-time risks.")
    return issues


def validate_global_audit(path: Path) -> list[str]:
    if not path.exists():
        return [f"global: missing daily intelligence audit at {path}."]
    data = load_json(path)
    issues: list[str] = []
    if is_placeholder(data):
        issues.append("global: daily_intel_audit.json is still the placeholder template.")
    blockers = data.get("blockers") or []
    for blocker in blockers:
        issues.append(f"global: daily intelligence blocker: {blocker}")
    for domain in ("ai1", "ai2"):
        payload = data.get(domain, {})
        if isinstance(payload, dict) and payload.get("hasPublishableIntel") is False:
            issues.append(f"{domain}: global QA did not confirm publishable intelligence work.")
    return issues


def validate_run(run_root: Path) -> list[str]:
    issues: list[str] = []
    for domain in ("ai1", "ai2"):
        issues.extend(validate_update(run_root / domain / f"{domain}_update" / "daily_intel_findings.json", domain))
        issues.extend(validate_scout(run_root / domain / f"{domain}_scout" / "candidate_discovery_plan.json", domain))
        issues.extend(validate_score(run_root / domain / f"{domain}_score" / "score_recalc_requirements.json", domain))
    issues.extend(validate_recency(run_root / "global" / "global_recency_recheck" / "recency_watchlist.json"))
    issues.extend(validate_global_audit(run_root / "global" / "global_qa" / "daily_intel_audit.json"))
    return issues


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-root", required=True)
    parser.add_argument("--json-output", default="")
    args = parser.parse_args()

    issues = validate_run(Path(args.run_root))
    payload = {"ok": not issues, "issues": issues}
    if args.json_output:
        Path(args.json_output).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if issues:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
