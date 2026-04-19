from __future__ import annotations

import argparse
import json
from pathlib import Path

RETRYABLE_TOKENS = (
    "timeout",
    "429",
    "5xx",
    "temporarily unavailable",
    "artifact",
    "network",
    "parser",
    "retryable",
    "source health",
)

NON_RETRYABLE_TOKENS = (
    "korea/china",
    "south korea",
    "china",
    "unicorn",
    "citation",
    "missing citation",
    "category leakage",
    "category mismatch",
    "html structure",
    "html shell",
    "regression",
    "stale",
    "unsupported",
    "policy drift",
    "deprecated",
)


def classify_issue(text: str) -> str:
    lower = text.lower()
    if any(token in lower for token in NON_RETRYABLE_TOKENS):
        return "non_retryable"
    if any(token in lower for token in RETRYABLE_TOKENS):
        return "retryable"
    return "non_retryable"


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
        if not path.exists() or path.suffix != ".json":
            continue

        data = json.loads(path.read_text(encoding="utf-8"))
        issues = data.get("issues", []) or data.get("blockers", []) or data.get("summary", [])
        for issue in issues:
            text = str(issue)
            summaries.append(text)
            bucket = classify_issue(text)
            if bucket == "retryable":
                retryable.append(text)
            else:
                non_retryable.append(text)

    payload = {
        "retryable": sorted(set(retryable)),
        "nonRetryable": sorted(set(non_retryable)),
        "summary": sorted(set(summaries)),
        "retryPlan": {
            "retryableCount": len(set(retryable)),
            "nonRetryableCount": len(set(non_retryable)),
            "policy": "Retry only bounded transient failures; fail closed on quality, policy, and evidence issues.",
        },
    }
    Path(args.json_output).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
