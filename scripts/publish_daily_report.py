from __future__ import annotations

import os
import re
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

SEOUL = ZoneInfo("Asia/Seoul")
WEEKDAY_KR = ["월", "화", "수", "목", "금", "토", "일"]
SCHEDULE_LABELS = [
    "월 — 모바일 헬스 · 헬스 서비스 · AI 헬스",
    "화 — 모바일 광고 · 광고 AI · 기술/서비스",
    "수 — 멀티모달 AI · 영상 AI 기술/서비스",
    "목 — 모바일 AI Agent · 휴대폰 AI 기술",
    "금 — 모바일 소셜 · Short Form 서비스",
    "토 — 페이 · 금융 기술 (코인 제외)",
    "일 — 기타 모바일/웹 서비스",
]
DATE_TOKEN_RE = re.compile(r"'26\.\d+\.\d+ \([월화수목금토일]\)")
TITLE_DATE_RE = re.compile(r"Global AI Startup Watch \(Non-Unicorn\) — '26\.\d+\.\d+ \([월화수목금토일]\)")
FOOTER_RE = re.compile(r"<footer>.*?</footer>", re.S)


def parse_target_date() -> date:
    raw = os.getenv("TARGET_DATE", "").strip()
    if raw:
        return date.fromisoformat(raw)
    return datetime.now(SEOUL).date()


def parse_folder_date(name: str, year: int, target: date) -> date | None:
    if not name.isdigit() or len(name) < 2 or len(name) > 4:
        return None
    candidates: list[date] = []
    for split in (1, 2):
        if split >= len(name):
            continue
        month = int(name[:split])
        day = int(name[split:])
        try:
            parsed = date(year, month, day)
        except ValueError:
            continue
        if parsed <= target:
            candidates.append(parsed)
    if not candidates:
        return None
    return max(candidates)


def find_source_file(root: Path, target: date) -> Path:
    target_file = root / f"{target.month}{target.day}" / "index.html"
    if target_file.exists():
        return target_file

    previous = root / f"{(target - timedelta(days=1)).month}{(target - timedelta(days=1)).day}" / "index.html"
    if previous.exists():
        return previous

    dated_candidates: list[tuple[date, Path]] = []
    for child in root.iterdir():
        if not child.is_dir():
            continue
        index_file = child / "index.html"
        if not index_file.exists():
            continue
        parsed = parse_folder_date(child.name, target.year, target)
        if parsed is not None:
            dated_candidates.append((parsed, index_file))

    if not dated_candidates:
        raise FileNotFoundError("No prior dated index.html template was found.")

    dated_candidates.sort(key=lambda item: item[0])
    return dated_candidates[-1][1]


def apply_date_updates(html: str, target: date) -> str:
    display = f"'26.{target.month}.{target.day} ({WEEKDAY_KR[target.weekday()]})"
    html = TITLE_DATE_RE.sub(f"Global AI Startup Watch (Non-Unicorn) — {display}", html)
    html = DATE_TOKEN_RE.sub(display, html)

    html = html.replace('class="sector-day today"', 'class="sector-day"')
    today_label = SCHEDULE_LABELS[target.weekday()]
    html = html.replace(
        f'<span class="sector-day">{today_label}</span>',
        f'<span class="sector-day today">{today_label}</span>',
        1,
    )

    timestamp = datetime.now(SEOUL).strftime("%Y-%m-%d %H:%M KST")
    footer = (
        f"<footer>작성 기준: {display} · 문서 상태: 서버 자동 갱신본 · "
        f"업데이트 시간: {timestamp} · PitchBook public 우선 확인, Dealroom/Crunchbase/official fallback</footer>"
    )
    if FOOTER_RE.search(html):
        html = FOOTER_RE.sub(footer, html, count=1)
    else:
        html = html.replace("</main>", f"  {footer}\n  </main>")
    return html


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    target = parse_target_date()
    source = find_source_file(root, target)
    output_dir = root / f"{target.month}{target.day}"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "index.html"

    html = source.read_text(encoding="utf-8")
    html = apply_date_updates(html, target)
    output_file.write_text(html, encoding="utf-8")
    print(f"Wrote {output_file.relative_to(root)} from {source.relative_to(root)}")


if __name__ == "__main__":
    main()
