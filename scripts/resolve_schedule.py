from __future__ import annotations

import argparse
import json
from pathlib import Path

from ai_watch.manifest import (
    ORCHESTRATOR_SCHEDULE,
    kst_date_string,
    phase_contract,
    phase_ids,
    phase_matrix,
    state_phase_root,
)


def emit_output(path: str, key: str, value: str) -> None:
    with Path(path).open("a", encoding="utf-8") as handle:
        handle.write(f"{key}={value}\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manual-phase", default="all")
    parser.add_argument("--manual-date", default="")
    parser.add_argument("--manual-page", default="")
    parser.add_argument("--github-output", default="")
    args = parser.parse_args()

    phase = (args.manual_phase or "all").strip()
    if phase != "all" and phase not in phase_ids():
        raise SystemExit(f"Unknown phase: {phase}")

    run_date = (args.manual_date or "").strip() or kst_date_string()
    if phase == "all":
        payload = {
            "phase": "all",
            "page": "",
            "run_date": run_date,
            "phase_root": "",
            "prompt_file": "",
            "agent_matrix": "[]",
            "kst_slot": ORCHESTRATOR_SCHEDULE["kst_start"],
            "should_run_codex": "false",
        }
    else:
        contract = phase_contract(phase)
        page = (args.manual_page or "").strip() or contract.page or ""
        payload = {
            "phase": phase,
            "page": page,
            "run_date": run_date,
            "phase_root": state_phase_root(run_date, page or None, phase).as_posix(),
            "prompt_file": contract.prompt_file or "",
            "agent_matrix": json.dumps(phase_matrix(phase), ensure_ascii=False),
            "kst_slot": contract.kst_slot,
            "should_run_codex": "true" if contract.runs_codex else "false",
        }

    if args.github_output:
        for key, value in payload.items():
            emit_output(args.github_output, key, value)
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
