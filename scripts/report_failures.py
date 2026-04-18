from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", nargs="+")
    parser.add_argument("--json-output", required=True)
    args = parser.parse_args()

    retryable: list[str] = []
    non_retryable: list[str] = []
    summaries: list[str] = []

    for raw_path in args.inputs:
        path = Path(raw_path)
        if not path.exists():
            continue
        if path.suffix == ".json":
            data = json.loads(path.read_text(encoding="utf-8"))
            for issue in data.get("issues", []) or data.get("blockers", []):
                text = str(issue)
                summaries.append(text)
                if any(token in text.lower() for token in ["timestamp", "ranking", "path", "artifact", "missing"]):
                    retryable.append(text)
                else:
                    non_retryable.append(text)

    payload = {
        "retryable": sorted(set(retryable)),
        "nonRetryable": sorted(set(non_retryable)),
        "summary": sorted(set(summaries)),
    }
    Path(args.json_output).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

