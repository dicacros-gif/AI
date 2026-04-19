from __future__ import annotations

import argparse
import json
import os
import sys


def runtime_status() -> dict[str, str | bool]:
    return {
        "github_actions": os.environ.get("GITHUB_ACTIONS", ""),
        "runner_environment": os.environ.get("RUNNER_ENVIRONMENT", ""),
        "runner_name": os.environ.get("RUNNER_NAME", ""),
        "server_only_ok": (
            os.environ.get("GITHUB_ACTIONS", "").lower() == "true"
            and os.environ.get("RUNNER_ENVIRONMENT", "").lower() == "github-hosted"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    status = runtime_status()
    if args.json:
        print(json.dumps(status, ensure_ascii=False, indent=2))
    if not status["server_only_ok"]:
        message = (
            "AI Watch automation is server-only. "
            "Run update/publish phases only on GitHub-hosted runners via GitHub Actions."
        )
        if args.json:
            payload = {"ok": False, "message": message, "status": status}
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            print(message)
            print(json.dumps(status, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
