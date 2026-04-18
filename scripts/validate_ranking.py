from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from ai_watch.html_tools import extract_order_map


def validate_page(path: Path) -> list[str]:
    html = path.read_text(encoding="utf-8")
    order_map = extract_order_map(html)
    issues: list[str] = []
    list_pairs = order_map["list"]
    list_ranks = [rank for rank, _ in list_pairs]
    list_names = [name for _, name in list_pairs]

    if list_ranks != list(range(1, len(list_ranks) + 1)):
        issues.append(f"{path}: rank sequence must start at 1 and be contiguous through N.")
    if len(list_names) != len(set(list_names)):
        issues.append(f"{path}: duplicate startup names found in main list.")

    for section_name, pairs in order_map.items():
        section_names = [name for _, name in pairs]
        section_ranks = [rank for rank, _ in pairs]
        if pairs and section_names != list_names:
            issues.append(f"{path}: section `{section_name}` order differs from main list.")
        if pairs and section_ranks != list_ranks:
            issues.append(f"{path}: section `{section_name}` rank labels differ from main list.")
    return issues


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+")
    parser.add_argument("--json-output", default="")
    args = parser.parse_args()

    issues: list[str] = []
    for raw_path in args.paths:
        issues.extend(validate_page(Path(raw_path)))

    payload = {"ok": not issues, "issues": issues}
    if args.json_output:
        Path(args.json_output).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if issues:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()

