from __future__ import annotations

import re
from pathlib import Path

from .manifest import CANONICAL_NAV_LABELS, CANONICAL_PAGE_MAP, format_visible_kst

VISIBLE_TS_RE = re.compile(r"'\d{2}\.\d{1,2}\.\d{1,2} \([^)]+\)(?: \d{2}:\d{2} KST 기준 · 작성 \d{2}:\d{2} KST(?: · 작성 \d{2}:\d{2} KST)*| \d{2}:\d{2} KST 기준)")
TITLE_RE = re.compile(r"<title>([^<]+)</title>")
HERO_LINK_BLOCK_RE = re.compile(r"<div class='ss'>.*?</div>", re.S)
TABLE_ROW_RE = re.compile(r"<tr class='tr-main'.*?</tr>", re.S)
ROW_NAME_RE = re.compile(r"<td><a class='cl' href='[^']+' target='_blank'>([^<]+)</a>")
ROW_RANK_RE = re.compile(r"<span class='rk'[^>]*>(\d+)</span>")
EVAL_COMPANY_RE = re.compile(r"<div class='eval-company' data-co='([^']+)'.*?<span class='rk'>(\d+)</span>", re.S)
PARTNER_RE = re.compile(r"<div class='pc interactive-card pc-coll'>.*?<span class='rk'[^>]*>(\d+)</span>\s*([^<]+)</h3>", re.S)
INSIGHT_RE = re.compile(r"<div class='pc-box'[^>]*>.*?<span class='pc-box-ico'>(\d+)</span><b>([^<]+)</b>", re.S)
RED_FLAG_RE = re.compile(r"<div class='rf-box [^']+' onclick=\"trf\(this\)\">\s*<div class='rf-hd'><span class='rf-ico'>[^<]+</span><b>([^<]+)</b>", re.S)
TOP_HERO_RE = re.compile(r"<div class='hc'><span class='ch'>.*?</span>", re.S)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, value: str) -> None:
    path.write_text(value, encoding="utf-8")


def page_title(html: str) -> str:
    match = TITLE_RE.search(html)
    return match.group(1) if match else ""


def page_is_personalization(html: str) -> bool:
    title = page_title(html)
    return "개인화" in title or "On-device" in title


def normalize_nav_block(current_page: str) -> str:
    first_now = " now" if current_page == "ai1" else ""
    second_now = " now" if current_page == "ai2" else ""
    return (
        "<div class='ss'>\n"
        f"  <a href='https://dicacros-gif.github.io/AI/1/' target='_blank' style='text-decoration:none;animation:none !important'><span class='sd sd-link{first_now}'>{CANONICAL_NAV_LABELS['ai1']}</span></a>\n"
        f"  <a href='https://dicacros-gif.github.io/AI/2/' target='_blank' style='text-decoration:none;animation:none !important'><span class='sd sd-link{second_now}'>{CANONICAL_NAV_LABELS['ai2']}</span></a>\n"
        "</div>"
    )


def replace_visible_timestamps(html: str, visible_label: str) -> str:
    return VISIBLE_TS_RE.sub(visible_label, html)


def normalize_cross_links(html: str, current_page: str) -> str:
    return HERO_LINK_BLOCK_RE.sub(normalize_nav_block(current_page), html, count=1)


def normalize_page(html: str, current_page: str, visible_label: str) -> str:
    html = replace_visible_timestamps(html, visible_label)
    return normalize_cross_links(html, current_page)


def ensure_canonical_page_mapping(repo_root: Path, visible_label: str | None = None) -> dict[str, str]:
    visible = visible_label or format_visible_kst()
    page1_path = repo_root / CANONICAL_PAGE_MAP["ai1"]["target_path"]
    page2_path = repo_root / CANONICAL_PAGE_MAP["ai2"]["target_path"]
    page1_html = read_text(page1_path)
    page2_html = read_text(page2_path)

    if not page_is_personalization(page1_html) and page_is_personalization(page2_html):
        page1_html, page2_html = page2_html, page1_html

    page1_html = normalize_page(page1_html, "ai1", visible)
    page2_html = normalize_page(page2_html, "ai2", visible)

    write_text(page1_path, page1_html)
    write_text(page2_path, page2_html)
    return {
        "ai1": page1_path.as_posix(),
        "ai2": page2_path.as_posix(),
        "visible_timestamp": visible,
    }


def _ordered_pairs_from_rows(html: str) -> list[tuple[int, str]]:
    pairs: list[tuple[int, str]] = []
    for row in TABLE_ROW_RE.findall(html):
        rank_match = ROW_RANK_RE.search(row)
        name_match = ROW_NAME_RE.search(row)
        if rank_match and name_match:
            pairs.append((int(rank_match.group(1)), name_match.group(1).strip()))
    return pairs


def _ordered_pairs(pattern: re.Pattern[str], html: str, rank_first: bool = False) -> list[tuple[int, str]]:
    pairs: list[tuple[int, str]] = []
    for left, right in pattern.findall(html):
        if rank_first:
            pairs.append((int(left), right.strip()))
        else:
            pairs.append((int(right), left.strip()))
    return pairs


def extract_order_map(html: str) -> dict[str, list[tuple[int, str]]]:
    list_pairs = _ordered_pairs_from_rows(html)
    red_flag_pairs = [(index + 1, name.strip()) for index, name in enumerate(RED_FLAG_RE.findall(html))]
    if list_pairs:
        red_flag_pairs = red_flag_pairs[: len(list_pairs)]
    return {
        "list": list_pairs,
        "eval": _ordered_pairs(EVAL_COMPANY_RE, html),
        "partner": _ordered_pairs(PARTNER_RE, html, rank_first=True),
        "insight": _ordered_pairs(INSIGHT_RE, html, rank_first=True),
        "red_flag": red_flag_pairs,
    }
