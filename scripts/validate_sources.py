from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def scan_json(path: Path) -> list[str]:
    issues: list[str] = []
    data = load_json(path)
    stack = [data]
    while stack:
        current = stack.pop()
        if isinstance(current, dict):
            language = str(current.get("language", "")).lower()
            decisive = bool(current.get("decisive", False))
            source_type = str(current.get("sourceType", "")).lower()
            if decisive and language in {"ko", "kr", "korean"}:
                issues.append(f"{path}: decisive fact relies on Korean-language source.")
            if source_type == "press_release" and current.get("isIndependent") is True:
                issues.append(f"{path}: official release incorrectly labeled as independent media.")
            if "number" in current and current.get("number") and not current.get("asOf"):
                issues.append(f"{path}: numeric claim is missing an as-of date.")
            for value in current.values():
                if isinstance(value, (dict, list)):
                    stack.append(value)
        elif isinstance(current, list):
            stack.extend(current)
    return issues


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+")
    parser.add_argument("--json-output", default="")
    args = parser.parse_args()

    issues: list[str] = []
    for raw_path in args.paths:
        path = Path(raw_path)
        if path.exists() and path.suffix == ".json":
            issues.extend(scan_json(path))

    payload = {"ok": not issues, "issues": issues}
    if args.json_output:
        Path(args.json_output).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if issues:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()

