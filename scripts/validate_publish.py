from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from ai_watch.html_tools import VISIBLE_TS_RE, extract_order_map, find_bullet_style_issues

REQUIRED_HTML_PATTERNS = {
    "toolbar": re.compile(r"class='tb'"),
    "sticky_nav": re.compile(r"id='stickyNav'"),
    "eval_company": re.compile(r"class='eval-company(?:\s|')"),
    "criteria_group": re.compile(r"class='crit-group(?:\s|')"),
    "insight_box": re.compile(r"class='pc-box(?:\s|')"),
    "red_flag_box": re.compile(r"class='rf-box(?:\s|')"),
    "row_summary_style": re.compile(r"row-summary-cell"),
    "row_summary_js": re.compile(r"buildRowSummaryHtml"),
}
PLACEHOLDER_MARKERS = ["TODO", "TBD", "PLACEHOLDER", "lorem ipsum"]
FORBIDDEN_NON_MOBILE_PATTERNS = {
    "tv_ctv_framing": re.compile(
        r"(?:\bCTV\b|\bFAST\b|smart[\s-]?TV|TV\s*광고|broadcast|living[-\s]?room|set[-\s]?top)",
        re.IGNORECASE,
    ),
    "non_phone_surface_framing": re.compile(
        r"(?:스마트\s*디스플레이|키오스크|smart\s*display|kiosk|signage)",
        re.IGNORECASE,
    ),
}


def company_names(path: Path) -> list[str]:
    html = path.read_text(encoding="utf-8")
    return [name for _, name in extract_order_map(html)["list"]]


def validate_path(path: Path) -> list[str]:
    if not path.exists():
        return [f"Missing publish target: {path}"]

    html = path.read_text(encoding="utf-8")
    visible_text = re.sub(r"<[^>]+>", " ", html)
    issues: list[str] = []

    for label, pattern in REQUIRED_HTML_PATTERNS.items():
        if not pattern.search(html):
            issues.append(f"{path}: missing required HTML structure `{label}`.")
    for marker in PLACEHOLDER_MARKERS:
        if marker in html:
            issues.append(f"{path}: placeholder text `{marker}` remains in published HTML.")
    for label, pattern in FORBIDDEN_NON_MOBILE_PATTERNS.items():
        if pattern.search(visible_text):
            issues.append(f"{path}: forbidden non-mobile framing `{label}` remains in published HTML.")

    visible_labels = VISIBLE_TS_RE.findall(html)
    if len(visible_labels) < 3:
        issues.append(f"{path}: missing visible KST timestamps in toolbar/hero/footer.")
    for label in visible_labels:
        if "KST" not in label:
            issues.append(f"{path}: timestamp missing KST suffix -> {label}")
    if "기준" in html and "KST 기준" not in html and "비공개" not in html:
        issues.append(f"{path}: found visible date text without explicit KST label.")
    if "<h1></h1>" in html or "class='cb'></div>" in html:
        issues.append(f"{path}: empty critical section detected.")

    bullet_style_issues = find_bullet_style_issues(html)
    if bullet_style_issues:
        issues.append(
            f"{path}: sections 2-5 must use bullet fragments without sentence-final `~다` or periods -> {bullet_style_issues[0]}"
        )
    return issues


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--page1", default="1/index.html")
    parser.add_argument("--page2", default="2/index.html")
    parser.add_argument("--json-output", default="")
    args = parser.parse_args()

    page1 = Path(args.page1)
    page2 = Path(args.page2)
    issues: list[str] = []
    issues.extend(validate_path(page1))
    issues.extend(validate_path(page2))

    for forbidden in [Path("1/index.htm"), Path("2/index.htm")]:
        if forbidden.exists():
            issues.append(f"Forbidden mixed publish target detected: {forbidden}")

    names1 = company_names(page1)
    names2 = company_names(page2)
    duplicates = sorted(set(names1).intersection(names2))
    if duplicates:
        issues.append(f"Duplicate startups across AI/1 and AI/2: {', '.join(duplicates)}")

    payload = {"ok": not issues, "issues": issues}
    if args.json_output:
        Path(args.json_output).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if issues:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
