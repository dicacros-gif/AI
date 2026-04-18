from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from ai_watch.manifest import PHASE_REQUIRED_OUTPUTS, phase_suffix


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_phase_root(path: Path) -> list[str]:
    phase = path.name
    suffix = phase_suffix(phase)
    issues: list[str] = []
    for required in PHASE_REQUIRED_OUTPUTS[suffix]:
        if not (path / required).exists():
            issues.append(f"{path}: missing required state artifact `{required}`.")

    scout_candidates = path / "scout_candidates.json"
    if scout_candidates.exists():
        data = load_json(scout_candidates)
        for candidate in data.get("candidates", []):
            hq = str(candidate.get("headquarters", "")).lower()
            if "south korea" in hq or "korea" in hq or "china" in hq:
                issues.append(f"{path}: newly discovered candidate `{candidate.get('name', 'unknown')}` violates Korea/China exclusion.")
            if candidate.get("hqVerified") is False:
                issues.append(f"{path}: newly discovered candidate `{candidate.get('name', 'unknown')}` has unverified HQ.")
            if candidate.get("valuationUsd", 0) and float(candidate["valuationUsd"]) >= 1_000_000_000:
                issues.append(f"{path}: newly discovered candidate `{candidate.get('name', 'unknown')}` is a unicorn and must be excluded.")
            if not candidate.get("hasRevenueEvidence", False):
                issues.append(f"{path}: newly discovered candidate `{candidate.get('name', 'unknown')}` lacks revenue evidence.")
            if candidate.get("companyType") == "pure_hardware" and not candidate.get("softwareServiceLayerEvidence", False):
                issues.append(f"{path}: newly discovered candidate `{candidate.get('name', 'unknown')}` is hardware-first without enough software/service leverage.")
    return issues


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-root", required=True)
    parser.add_argument("--json-output", default="")
    args = parser.parse_args()

    run_root = Path(args.run_root)
    issues: list[str] = []
    for phase_root in sorted(run_root.rglob("*")):
        if phase_root.is_dir() and phase_root.name in {
            "ai1_update",
            "ai1_verify",
            "ai1_scout",
            "ai1_score",
            "ai1_render",
            "ai2_update",
            "ai2_verify",
            "ai2_scout",
            "ai2_score",
            "ai2_render",
            "global_qa",
            "retry_failed",
            "republish_or_qa",
            "final_retry_or_publish_check",
        }:
            issues.extend(validate_phase_root(phase_root))

    payload = {"ok": not issues, "issues": issues}
    if args.json_output:
        Path(args.json_output).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if issues:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()

