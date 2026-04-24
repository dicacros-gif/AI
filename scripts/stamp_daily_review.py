from __future__ import annotations

import argparse
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path


WEEKDAYS_KO = ("월", "화", "수", "목", "금", "토", "일")
STAMP_RE = re.compile(r"'?\d{2}\.\d{1,2}\.\d{1,2} \([월화수목금토일]\) \d{2}:\d{2} KST 기준")


def current_kst_stamp() -> str:
    now = datetime.now(timezone(timedelta(hours=9), name="KST"))
    return f"'{now:%y}.{now.month}.{now.day} ({WEEKDAYS_KO[now.weekday()]}) {now:%H:%M} KST 기준"


def stamp_page(path: Path, stamp: str) -> bool:
    text = path.read_text(encoding="utf-8")
    next_text, count = STAMP_RE.subn(stamp, text)
    if count == 0:
        raise SystemExit(f"{path}: no visible KST timestamp found")
    if next_text == text:
        return False
    path.write_text(next_text, encoding="utf-8", newline="\n")
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Stamp daily review time on AI watch pages.")
    parser.add_argument("--page", action="append", required=True, help="HTML page to stamp")
    args = parser.parse_args()

    stamp = current_kst_stamp()
    changed = [str(Path(raw)) for raw in args.page if stamp_page(Path(raw), stamp)]
    print({"stamp": stamp, "changed": changed})


if __name__ == "__main__":
    main()
