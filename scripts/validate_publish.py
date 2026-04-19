from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from ai_watch.html_tools import VISIBLE_TS_RE, extract_order_map, find_bullet_style_issues

REQUIRED_HTML_PATTERNS = {
    "topbar": re.compile(r"class='topbar'"),
    "toolbar": re.compile(r"class='tb'"),
    "sticky_nav": re.compile(r"id='stickyNav'"),
    "eval_company": re.compile(r"class='eval-company(?:\s|')"),
    "criteria_group": re.compile(r"class='crit-group(?:\s|')"),
    "insight_box": re.compile(r"class='pc-box(?:\s|')"),
    "red_flag_box": re.compile(r"class='rf-box(?:\s|')"),
    "row_summary_style": re.compile(r"row-summary-cell"),
    "row_summary_js": re.compile(r"buildRowSummaryHtml"),
    "metric_time_link_js": re.compile(r"hydrateMetricTimeLinks"),
    "criteria_highlight_js": re.compile(r"hydrateCriteriaHighlights"),
    "criteria_highlight_style": re.compile(r"\.crt \.score-top"),
}
TOPBAR_STRUCTURE = re.compile(r"<div class='topbar'>\s*<nav class='nav' id='stickyNav'>.*?</nav>\s*<div class='tb'>", re.S)
FORBIDDEN_TOPBAR_PATTERNS = {
    "toolbar_second_row": re.compile(r"\.tb\{position:sticky", re.IGNORECASE),
    "nav_sticky_second_row": re.compile(r"\.nav\{position:sticky", re.IGNORECASE),
}
FORBIDDEN_DEFAULT_COLLAPSE_PATTERNS = {
    "partner_boxes_collapsed_by_default": re.compile(r"class='pc-b pc-b-shut'"),
}
FORBIDDEN_SECTION1_WIDTH_PATTERNS = {
    "legacy_section1_table_width": re.compile(r"<table style='min-width:3000px'>"),
}
ROW_ID_PATTERN = re.compile(r"<tr class='tr-main' data-row='([^']+)' onclick=\"toggleRow\('([^']+)',this\)\"")
EVAL_COMPANY_START = re.compile(r"<div class='eval-company'[^>]*data-co='[^']+'")
EVAL_COMPANY_KEY = re.compile(r"data-co='([^']+)'")
EVAL_COMPANY_HD = re.compile(r"<div class='eval-company-hd'")
EVAL_COMPANY_BD = re.compile(r"<div class='eval-company-bd'")
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
FORBIDDEN_HERO_CHIPS = (
    "한국/중국 본사 제외",
    "영문 기사 기준",
    "영문 권위 소스 기준",
)
FORBIDDEN_VISIBLE_TERMS = (
    "Samsung",
    "삼성",
)


def company_names(path: Path) -> list[str]:
    html = path.read_text(encoding="utf-8")
    return [name for _, name in extract_order_map(html)["list"]]


def validate_eval_company_cards(path: Path, html: str) -> list[str]:
    issues: list[str] = []
    starts = list(EVAL_COMPANY_START.finditer(html))
    for index, match in enumerate(starts):
        next_start = starts[index + 1].start() if index + 1 < len(starts) else len(html)
        chunk = html[match.start():next_start]
        key_match = EVAL_COMPANY_KEY.search(chunk[:200])
        key = key_match.group(1) if key_match else f"index {index + 1}"
        hd_match = EVAL_COMPANY_HD.search(chunk)
        bd_match = EVAL_COMPANY_BD.search(chunk)
        if not hd_match:
            issues.append(f"{path}: eval-company `{key}` is missing `eval-company-hd` before the next card.")
            continue
        if not bd_match:
            issues.append(f"{path}: eval-company `{key}` is missing `eval-company-bd` before the next card.")
            continue
        if hd_match.start() > bd_match.start():
            issues.append(f"{path}: eval-company `{key}` has `eval-company-bd` before `eval-company-hd`.")
    return issues


def validate_path(path: Path) -> list[str]:
    if not path.exists():
        return [f"Missing publish target: {path}"]

    html = path.read_text(encoding="utf-8")
    visible_text = re.sub(r"<[^>]+>", " ", html)
    issues: list[str] = []
    criteria_start = html.find("id='sec-criteria'")
    criteria_end = html.find("<footer", criteria_start) if criteria_start != -1 else -1
    criteria_html = html[criteria_start:criteria_end] if criteria_start != -1 and criteria_end != -1 else ""

    for label, pattern in REQUIRED_HTML_PATTERNS.items():
        if not pattern.search(html):
            issues.append(f"{path}: missing required HTML structure `{label}`.")
    if not TOPBAR_STRUCTURE.search(html):
        issues.append(f"{path}: top navigation and toolbar controls must share the same first-row topbar wrapper.")
    for label, pattern in FORBIDDEN_TOPBAR_PATTERNS.items():
        if pattern.search(html):
            issues.append(f"{path}: forbidden second-row topbar layout `{label}` detected.")
    for label, pattern in FORBIDDEN_DEFAULT_COLLAPSE_PATTERNS.items():
        if pattern.search(html):
            issues.append(f"{path}: forbidden default-collapsed partnership layout `{label}` detected.")
    for label, pattern in FORBIDDEN_SECTION1_WIDTH_PATTERNS.items():
        if pattern.search(html):
            issues.append(f"{path}: forbidden legacy-wide section-1 table layout `{label}` detected.")

    row_pairs = ROW_ID_PATTERN.findall(html)
    row_ids = [left for left, _ in row_pairs]
    if row_ids and len(row_ids) != len(set(row_ids)):
        issues.append(f"{path}: duplicate section-1 row ids detected.")
    mismatched_pairs = [f"{left}!={right}" for left, right in row_pairs if left != right]
    if mismatched_pairs:
        issues.append(f"{path}: section-1 row id / onclick mismatch -> {mismatched_pairs[0]}")

    issues.extend(validate_eval_company_cards(path, html))

    for marker in PLACEHOLDER_MARKERS:
        if marker in html:
            issues.append(f"{path}: placeholder text `{marker}` remains in published HTML.")

    for label, pattern in FORBIDDEN_NON_MOBILE_PATTERNS.items():
        if pattern.search(visible_text):
            issues.append(f"{path}: forbidden non-mobile framing `{label}` remains in published HTML.")

    for label in FORBIDDEN_HERO_CHIPS:
        if label in visible_text:
            issues.append(f"{path}: forbidden hero chip `{label}` remains in published HTML.")
    for label in FORBIDDEN_VISIBLE_TERMS:
        if label in visible_text:
            issues.append(f"{path}: forbidden visible term `{label}` remains in published HTML.")

    visible_labels = VISIBLE_TS_RE.findall(html)
    if len(visible_labels) < 2:
        issues.append(f"{path}: missing visible KST timestamps in hero/footer.")
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
            f"{path}: section-1 insight/article/competitor copy and sections 2-5 must use bullet fragments without sentence-final `~다` or periods -> {bullet_style_issues[0]}"
        )
    if criteria_html and ("??" in criteria_html or "�" in criteria_html):
        issues.append(f"{path}: section-6 criteria block contains mojibake or question-mark corruption.")
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
