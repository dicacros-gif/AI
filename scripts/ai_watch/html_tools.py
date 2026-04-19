from __future__ import annotations

import re
from pathlib import Path

from .manifest import CANONICAL_NAV_LABELS, CANONICAL_PAGE_MAP, format_visible_kst

VISIBLE_TS_RE = re.compile(r"'\d{2}\.\d{1,2}\.\d{1,2} \([^)]+\) \d{2}:\d{2} KST (?:기준|湲곗?)(?: · 작성 \d{2}:\d{2} KST| 쨌 ?묒꽦 \d{2}:\d{2} KST)*")
TITLE_RE = re.compile(r"<title>([^<]+)</title>")
HERO_LINK_BLOCK_RE = re.compile(r"<div class='ss'>.*?</div>", re.S)
TABLE_ROW_RE = re.compile(r"<tr class='tr-main'.*?</tr>", re.S)
ROW_NAME_RE = re.compile(r"<td><a class='cl' href='[^']+' target='_blank'>([^<]+)</a>")
ROW_RANK_RE = re.compile(r"<span class='rk'[^>]*>(\d+)</span>")
EVAL_COMPANY_RE = re.compile(r"<div class='eval-company' data-co='([^']+)'.*?<span class='rk'>(\d+)</span>", re.S)
PARTNER_RE = re.compile(r"<div class='pc interactive-card pc-coll'>.*?<span class='rk'[^>]*>(\d+)</span>\s*([^<]+)</h3>", re.S)
INSIGHT_RE = re.compile(r"<div class='pc-box'[^>]*>.*?<span class='pc-box-ico'>(\d+)</span><b>([^<]+)</b>", re.S)
RED_FLAG_RE = re.compile(r"<div class='rf-box [^']+' onclick=\"trf\(this\)\">\s*<div class='rf-hd'><span class='rf-ico'>[^<]+</span><b>([^<]+)</b>", re.S)
LI_RE = re.compile(r"<li>(.*?)</li>", re.S)
LEAF_DIV_RE = re.compile(r"<div>(.*?)</div>", re.S)
TAG_SPLIT_RE = re.compile(r"(<[^>]+>)")
DIV_TAG_RE = re.compile(r"</?div\b[^>]*>")
SEC_LIST_ID = "sec-list"
SECTION_IDS = ("sec-eval", "sec-partner", "sec-insight", "sec-market")
BULLET_STYLE_SECTION_IDS = (SEC_LIST_ID,) + SECTION_IDS
BULLET_STYLE_ISSUE_RE = re.compile(
    r"(?:[.。]\s*|한다|된다|있다|없다|좋다|높다|크다|맞다|필요하다|가능하다|어렵다|쉽다|커진다|늘어난다|이어진다|형성된다|생긴다|보여\s*준다|봐야\s*한다|해야\s*한다|보수적이어야\s*한다|제공한다|판매한다|강화한다|확장한다|연결한다|배포한다|고도화한다|활용한다|자동화한다|통합한다|구축한다|단축한다|가속한다|통제한다|탐색한다|실험한다|작동한다|절제한다|뒷받침한다|설계한다|전환한다|집행한다|처리한다|노린다|포인트다|안전하다|빨라진다|상단\s*티어다|[가-힣A-Za-z0-9]+다)\s*$"
)
BULLET_ENDING_REPLACEMENTS: tuple[tuple[str, str], ...] = (
    ("내재화했다", "내재화"),
    ("내재화 했다", "내재화"),
    ("내재화 했", "내재화"),
    ("증명했다", "증명"),
    ("증명 했다", "증명"),
    ("증명했", "증명"),
    ("공개했다", "공개"),
    ("공개한다", "공개"),
    ("명확하다", "명확"),
    ("선명하다", "선명"),
    ("직접적이다", "직접적"),
    ("현대적이다", "현대적"),
    ("부족하다", "부족"),
    ("봐야 한다", "추가 확인 필요"),
    ("상단 티어다", "상단 티어"),
    ("빨라진다", "빨라짐"),
    ("안전하다", "안전"),
    ("포인트다", "포인트"),
    ("노린다", "노림"),
    ("보인다", "보임"),
    ("계속 확인해야 한다", "지속 확인 필요"),
    ("추가 확인해야 한다", "추가 확인 필요"),
    ("확인해야 한다", "확인 필요"),
    ("계속 점검해야 한다", "지속 점검 필요"),
    ("추가 점검해야 한다", "추가 점검 필요"),
    ("점검해야 한다", "점검 필요"),
    ("따져봐야 한다", "검토 필요"),
    ("봐야 한다", "점검 필요"),
    ("해야 한다", "추진 필요"),
    ("보수적이어야 한다", "보수 반영 필요"),
    ("확보할 수 있다", "확보 가능"),
    ("만들 수 있다", "구축 가능"),
    ("될 수 있다", "가능"),
    ("할 수 있다", "가능"),
    ("보여 준다", "보여줌"),
    ("보여준다", "보여줌"),
    ("좌우할 수 있다", "좌우 가능"),
    ("작동한다", "유효"),
    ("뒷받침한다", "뒷받침"),
    ("절제한다", "보수 반영"),
    ("실험한다", "실험"),
    ("탐색한다", "탐색"),
    ("통제한다", "통제"),
    ("가속한다", "가속"),
    ("단축한다", "단축"),
    ("구축한다", "구축"),
    ("통합한다", "통합"),
    ("처리한다", "처리"),
    ("집행한다", "집행"),
    ("전환한다", "전환"),
    ("설계한다", "설계"),
    ("자동화한다", "자동화"),
    ("활용한다", "활용"),
    ("고도화한다", "고도화"),
    ("배포한다", "배포"),
    ("연결한다", "연결"),
    ("확장한다", "확장"),
    ("강화한다", "강화"),
    ("판매한다", "판매"),
    ("제공한다", "제공"),
    ("이어진다", "연결"),
    ("형성된다", "형성"),
    ("생긴다", "발생"),
    ("개선된다", "개선"),
    ("개선한다", "개선"),
    ("확대된다", "확대"),
    ("확대한다", "확대"),
    ("확보한다", "확보"),
    ("유지한다", "유지"),
    ("줄인다", "축소"),
    ("높인다", "상승"),
    ("끌어올린다", "상승"),
    ("만든다", "구축"),
    ("어울린다", "적합"),
    ("적합하다", "적합"),
    ("선명하다", "선명"),
    ("직접적이다", "직접적"),
    ("유리하다", "유리"),
    ("민첩하다", "민첩"),
    ("자연스럽다", "자연스러움"),
    ("필요하다", "필요"),
    ("가능하다", "가능"),
    ("어렵다", "어려움"),
    ("쉽다", "용이"),
    ("좋다", "우수"),
    ("높다", "높음"),
    ("좁다", "좁음"),
    ("커진다", "확대"),
    ("크다", "큼"),
    ("빠르다", "빠름"),
    ("맞다", "적합"),
    ("강하다", "강함"),
    ("약하다", "약함"),
    ("있다", "있음"),
    ("없다", "없음"),
    ("된다", "됨"),
    ("이다", ""),
)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, value: str) -> None:
    path.write_text(value, encoding="utf-8")


def page_title(html: str) -> str:
    match = TITLE_RE.search(html)
    return match.group(1) if match else ""


def page_is_personalization(html: str) -> bool:
    title = page_title(html)
    return "On-device" in title or "개인화" in title


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


def _section_range(html: str, section_id: str) -> tuple[int, int] | None:
    start = html.find(f"id='{section_id}'")
    if start == -1:
        return None
    end_candidates = [html.find(f"id='{next_id}'", start + 1) for next_id in SECTION_IDS if next_id != section_id]
    end_candidates.append(html.find("<footer", start + 1))
    valid = [idx for idx in end_candidates if idx != -1 and idx > start]
    end = min(valid) if valid else len(html)
    return start, end


def _find_matching_div_end(text: str, start: int) -> int:
    depth = 0
    for match in DIV_TAG_RE.finditer(text, start):
        if match.group(0).startswith("</div"):
            depth -= 1
            if depth == 0:
                return match.end()
        else:
            depth += 1
    return len(text)


def _iter_div_class_blocks(text: str, class_name: str) -> list[tuple[int, int, str]]:
    token = f"<div class='{class_name}'>"
    blocks: list[tuple[int, int, str]] = []
    cursor = 0
    while True:
        start = text.find(token, cursor)
        if start == -1:
            break
        end = _find_matching_div_end(text, start)
        blocks.append((start, end, text[start:end]))
        cursor = end
    return blocks


def _normalize_bullet_sentence(text: str) -> str:
    normalized = re.sub(r"\s+", " ", text.strip())
    normalized = re.sub(r"[.。]\s*$", "", normalized)
    for source, target in BULLET_ENDING_REPLACEMENTS:
        if normalized.endswith(source):
            normalized = normalized[: -len(source)] + target
            break
    normalized = re.sub(r"[.。]\s*$", "", normalized)
    if normalized.endswith("다"):
        normalized = normalized[:-1]
    return normalized


def _normalize_last_text_node(inner_html: str) -> str:
    parts = TAG_SPLIT_RE.split(inner_html)
    for idx in range(len(parts) - 1, -1, -1):
        part = parts[idx]
        if not part or part.startswith("<"):
            continue
        stripped = part.strip()
        if not stripped:
            continue
        leading_len = len(part) - len(part.lstrip())
        trailing_len = len(part) - len(part.rstrip())
        leading = part[:leading_len]
        trailing = part[len(part) - trailing_len :] if trailing_len else ""
        parts[idx] = leading + _normalize_bullet_sentence(stripped) + trailing
        break
    return "".join(parts)


def _normalize_li_items(section_html: str) -> str:
    return LI_RE.sub(lambda match: f"<li>{_normalize_last_text_node(match.group(1))}</li>", section_html)


def _normalize_partner_items(section_html: str) -> str:
    pieces: list[str] = []
    cursor = 0
    for start, end, block in _iter_div_class_blocks(section_html, "pc-l"):
        pieces.append(section_html[cursor:start])
        prefix = "<div class='pc-l'>"
        inner = block[len(prefix) : -len("</div>")]
        normalized_inner = LEAF_DIV_RE.sub(
            lambda match: f"<div>{_normalize_last_text_node(match.group(1))}</div>",
            inner,
        )
        pieces.append(prefix + normalized_inner + "</div>")
        cursor = end
    pieces.append(section_html[cursor:])
    return "".join(pieces)


def _normalize_section1_fragments(section_html: str) -> str:
    section_html = _normalize_li_items(section_html)
    section_html = re.sub(
        r"<div class='ins-li'>(.*?)</div>",
        lambda match: f"<div class='ins-li'>{_normalize_last_text_node(match.group(1))}</div>",
        section_html,
        flags=re.S,
    )
    section_html = re.sub(
        r"<span class='c-str'>(.*?)</span>",
        lambda match: f"<span class='c-str'>{_normalize_last_text_node(match.group(1))}</span>",
        section_html,
        flags=re.S,
    )
    section_html = re.sub(
        r"<span class='c-wk'>(.*?)</span>",
        lambda match: f"<span class='c-wk'>{_normalize_last_text_node(match.group(1))}</span>",
        section_html,
        flags=re.S,
    )
    return section_html


def normalize_bullet_sections(html: str) -> str:
    for section_id in BULLET_STYLE_SECTION_IDS:
        bounds = _section_range(html, section_id)
        if not bounds:
            continue
        start, end = bounds
        block = html[start:end]
        if section_id == SEC_LIST_ID:
            block = _normalize_section1_fragments(block)
        elif section_id == "sec-partner":
            block = _normalize_partner_items(block)
        else:
            block = _normalize_li_items(block)
        html = html[:start] + block + html[end:]
    return html


def _visible_text(fragment: str) -> str:
    text = re.sub(r"<[^>]+>", "", fragment)
    return re.sub(r"\s+", " ", text).strip()


def find_bullet_style_issues(html: str) -> list[str]:
    issues: list[str] = []
    for section_id in BULLET_STYLE_SECTION_IDS:
        bounds = _section_range(html, section_id)
        if not bounds:
            continue
        start, end = bounds
        block = html[start:end]
        if section_id == SEC_LIST_ID:
            for item in LI_RE.findall(block):
                text = _visible_text(item)
                if text and BULLET_STYLE_ISSUE_RE.search(text):
                    issues.append(f"{section_id}: {text}")
            for pattern in (
                re.compile(r"<div class='ins-li'>(.*?)</div>", re.S),
                re.compile(r"<span class='c-str'>(.*?)</span>", re.S),
                re.compile(r"<span class='c-wk'>(.*?)</span>", re.S),
            ):
                for item in pattern.findall(block):
                    text = _visible_text(item)
                    if text and BULLET_STYLE_ISSUE_RE.search(text):
                        issues.append(f"{section_id}: {text}")
        elif section_id == "sec-partner":
            for _, _, pc_block in _iter_div_class_blocks(block, "pc-l"):
                inner = pc_block[len("<div class='pc-l'>") : -len("</div>")]
                for item in LEAF_DIV_RE.findall(inner):
                    text = _visible_text(item)
                    if text and BULLET_STYLE_ISSUE_RE.search(text):
                        issues.append(f"{section_id}: {text}")
        else:
            for item in LI_RE.findall(block):
                text = _visible_text(item)
                if text and BULLET_STYLE_ISSUE_RE.search(text):
                    issues.append(f"{section_id}: {text}")
    return issues


def normalize_page(html: str, current_page: str, visible_label: str) -> str:
    html = replace_visible_timestamps(html, visible_label)
    html = normalize_cross_links(html, current_page)
    return normalize_bullet_sections(html)


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
