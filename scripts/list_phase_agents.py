from __future__ import annotations

import argparse
import json

from ai_watch.manifest import phase_matrix


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("phase")
    args = parser.parse_args()
    print(json.dumps(phase_matrix(args.phase), ensure_ascii=False))


if __name__ == "__main__":
    main()

