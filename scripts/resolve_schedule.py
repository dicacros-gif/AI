from __future__ import annotations

import argparse
import json
from pathlib import Path

from ai_watch.manifest import (
    PHASE_KST_SLOTS,
    PHASE_PROMPTS,
    PHASE_TO_PAGE,
    SCHEDULE_TO_PHASE,
    phase_matrix,
    state_phase_root,
    kst_date_string,
)


def emit_output(path: str, key: str, value: str) -> None:
    with Path(path).open("a", encoding="utf-8") as handle:
        handle.write(f"{key}={value}\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scheduled-cron", default="")
    parser.add_argument("--manual-phase", default="")
    parser.add_argument("--manual-date", default="")
    parser.add_argument("--manual-page", default="")
    parser.add_argument("--github-output", default="")
    args = parser.parse_args()

    phase = (args.manual_phase or "").strip()
    if not phase or phase == "scheduled":
        phase = SCHEDULE_TO_PHASE[args.scheduled_cron.strip()]

    page = (args.manual_page or "").strip() or PHASE_TO_PAGE.get(phase, "")
    run_date = (args.manual_date or "").strip() or kst_date_string()
    phase_root = state_phase_root(run_date, page or None, phase)

    payload = {
        "phase": phase,
        "page": page,
        "run_date": run_date,
        "phase_root": phase_root.as_posix(),
        "prompt_file": PHASE_PROMPTS[phase],
        "agent_matrix": json.dumps(phase_matrix(phase), ensure_ascii=False),
        "kst_slot": PHASE_KST_SLOTS[phase],
        "should_run_codex": "true" if phase_matrix(phase) else "false",
        "commit_main": "true" if phase.endswith("_render") or phase == "republish_or_qa" else "false",
        "validate_publish": "true" if phase.endswith("_render") or phase in {"global_qa", "republish_or_qa", "final_retry_or_publish_check"} else "false",
    }

    if args.github_output:
        for key, value in payload.items():
            emit_output(args.github_output, key, value)
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

