from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from ai_watch.manifest import PHASE_REQUIRED_OUTPUTS, phase_contract, phase_ids, phase_suffix


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_phase_root(path: Path) -> list[str]:
    phase_id = path.name
    contract = phase_contract(phase_id)
    suffix = phase_suffix(phase_id)
    issues: list[str] = []

    for required in PHASE_REQUIRED_OUTPUTS[suffix]:
        if not (path / required).exists():
            issues.append(f"{path}: missing required state artifact `{required}`.")

    if not (path / "run_manifest.json").exists():
        issues.append(f"{path}: missing `run_manifest.json`.")
    if not (path / "phase_contract.json").exists():
        issues.append(f"{path}: missing `phase_contract.json`.")
    else:
        phase_contract_payload = load_json(path / "phase_contract.json")
        if not phase_contract_payload.get("gates"):
            issues.append(f"{path}: `phase_contract.json` has no gates.")
        if not phase_contract_payload.get("fail_closed_fields"):
            issues.append(f"{path}: `phase_contract.json` has no fail-closed fields.")
        evidence_contract = phase_contract_payload.get("evidence_contract", {})
        expected_keys = {
            "min_sources_per_core_claim",
            "min_sources_for_mutable_claim",
            "max_staleness_days",
            "freshness_fields",
        }
        missing_keys = expected_keys.difference(evidence_contract.keys())
        if missing_keys:
            missing = ", ".join(sorted(missing_keys))
            issues.append(f"{path}: `phase_contract.json` evidence contract is missing keys: {missing}.")

    if (path / "run_manifest.json").exists():
        manifest_payload = load_json(path / "run_manifest.json")
        if manifest_payload.get("phase") != phase_id:
            issues.append(f"{path}: `run_manifest.json` phase mismatch.")
        if manifest_payload.get("kind") != contract.kind:
            issues.append(f"{path}: `run_manifest.json` kind mismatch for `{phase_id}`.")
        if manifest_payload.get("runsCodex") and not manifest_payload.get("promptFile"):
            issues.append(f"{path}: Codex phase manifest is missing `promptFile`.")

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
            company_type = str(candidate.get("companyType", "")).lower()
            if company_type in {"pure_hardware", "hardware", "hardware_vendor"}:
                issues.append(f"{path}: newly discovered candidate `{candidate.get('name', 'unknown')}` is hardware-first and must be excluded.")

    verified_candidates = path / "verified_candidates.jsonl"
    if verified_candidates.exists() and contract.kind == "candidate_verify":
        content = verified_candidates.read_text(encoding="utf-8").strip()
        if not content:
            issues.append(f"{path}: candidate verify phase produced an empty `verified_candidates.jsonl` file.")

    claims = path / "claims.jsonl"
    if claims.exists() and contract.kind == "claim_ledger":
        if '"source_id":' not in claims.read_text(encoding="utf-8"):
            issues.append(f"{path}: claim ledger has no `source_id` entries.")

    return issues


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-root", required=True)
    parser.add_argument("--json-output", default="")
    args = parser.parse_args()

    run_root = Path(args.run_root)
    issues: list[str] = []
    known_phase_ids = set(phase_ids())
    for phase_root in sorted(run_root.rglob("*")):
        if phase_root.is_dir() and phase_root.name in known_phase_ids:
            issues.extend(validate_phase_root(phase_root))

    payload = {"ok": not issues, "issues": issues}
    if args.json_output:
        Path(args.json_output).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if issues:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
