from __future__ import annotations

import argparse
import re
from pathlib import Path


LIST_BLOCK_RE = re.compile(r"<tr class='tr-main'.*?</tr>", re.S)
LIST_NAME_RE = re.compile(r"<td><a class='cl' href='[^']+' target='_blank'>([^<]+)</a>")
LIST_RANK_RE = re.compile(r"(<span class='rk'[^>]*>)(\d+)(</span>)", re.S)
EVAL_NAME_RE = re.compile(r"data-co='([^']+)'")
PARTNER_NAME_RE = re.compile(r"<h3><span class='rk'[^>]*>\d+</span>\s*([^<]+)</h3>", re.S)
INSIGHT_NAME_RE = re.compile(r"<span class='pc-box-ico'>\d+</span><b>([^<]+)</b>", re.S)
RED_FLAG_NAME_RE = re.compile(r"<div class='rf-hd'>.*?<b>([^<]+)</b>", re.S)
PC_BOX_RANK_RE = re.compile(r"(<span class='pc-box-ico'>)(\d+)(</span>)", re.S)
COUNT_RE = re.compile(r"(통합 스타트업 리스트 )(\d+)(선)")


def _find_matching_div(text: str, start: int) -> int:
    depth = 0
    for match in re.finditer(r"<div\b|</div>", text[start:]):
        token = match.group(0)
        if token.startswith("<div"):
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                return start + match.end()
    raise ValueError(f"Unbalanced div block at index {start}")


def _extract_div_blocks(text: str, marker: str) -> list[tuple[int, int, str]]:
    blocks: list[tuple[int, int, str]] = []
    cursor = 0
    while True:
        start = text.find(marker, cursor)
        if start == -1:
            break
        end = _find_matching_div(text, start)
        blocks.append((start, end, text[start:end]))
        cursor = end
    return blocks


def _replace_blocks(
    text: str,
    blocks: list[tuple[int, int, str]],
    name_extractor,
    remove_names: set[str],
    renumber,
) -> str:
    result: list[str] = []
    cursor = 0
    rank = 1
    for start, end, block in blocks:
        result.append(text[cursor:start])
        name = name_extractor(block)
        if name and name in remove_names:
            cursor = end
            continue
        if name and renumber:
            block = renumber(block, rank)
            rank += 1
        result.append(block)
        cursor = end
    result.append(text[cursor:])
    return "".join(result)


def _extract_name(pattern: re.Pattern[str], block: str) -> str:
    match = pattern.search(block)
    return match.group(1).strip() if match else ""


def _renumber_rk(block: str, rank: int) -> str:
    return LIST_RANK_RE.sub(lambda m: f"{m.group(1)}{rank}{m.group(3)}", block, count=1)


def _renumber_pc_box(block: str, rank: int) -> str:
    return PC_BOX_RANK_RE.sub(lambda m: f"{m.group(1)}{rank}{m.group(3)}", block, count=1)


def _remove_zero_gate_buttons(text: str, remove_names: set[str]) -> str:
    for name in remove_names:
        text = re.sub(
            rf"<span class='gb' data-z='{re.escape(name)}' onclick=\"tz\(this\)\"><span style='font-size:9px'>☐</span>[^<]*</span>",
            "",
            text,
        )
    text = re.sub(r"(</span>)(\s*)(<span class='gb')", r"\1\3", text)
    return text


def _update_list_count(text: str, count: int) -> str:
    return COUNT_RE.sub(lambda m: f"{m.group(1)}{count}{m.group(3)}", text, count=1)


def prune_page(path: Path, remove_names: set[str]) -> int:
    html = path.read_text(encoding="utf-8")

    list_blocks = [(m.start(), m.end(), m.group(0)) for m in LIST_BLOCK_RE.finditer(html)]
    html = _replace_blocks(
        html,
        list_blocks,
        lambda block: _extract_name(LIST_NAME_RE, block),
        remove_names,
        _renumber_rk,
    )

    eval_blocks = _extract_div_blocks(html, "<div class='eval-company'")
    html = _replace_blocks(
        html,
        eval_blocks,
        lambda block: _extract_name(EVAL_NAME_RE, block),
        remove_names,
        _renumber_rk,
    )

    partner_blocks = _extract_div_blocks(html, "<div class='pc interactive-card pc-coll'>")
    html = _replace_blocks(
        html,
        partner_blocks,
        lambda block: _extract_name(PARTNER_NAME_RE, block),
        remove_names,
        _renumber_rk,
    )

    insight_blocks = _extract_div_blocks(html, "<div class='pc-box'")
    html = _replace_blocks(
        html,
        insight_blocks,
        lambda block: _extract_name(INSIGHT_NAME_RE, block),
        remove_names,
        _renumber_pc_box,
    )

    red_flag_blocks = _extract_div_blocks(html, "<div class='rf-box ")
    html = _replace_blocks(
        html,
        red_flag_blocks,
        lambda block: _extract_name(RED_FLAG_NAME_RE, block),
        remove_names,
        None,
    )

    html = _remove_zero_gate_buttons(html, remove_names)

    remaining_names = [m.group(1).strip() for m in LIST_NAME_RE.finditer(html)]
    html = _update_list_count(html, len(remaining_names))

    path.write_text(html, encoding="utf-8")
    return len(remaining_names)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--page", required=True)
    parser.add_argument("--remove", nargs="+", required=True)
    args = parser.parse_args()

    page = Path(args.page)
    remaining = prune_page(page, set(args.remove))
    print(f"{page}: {remaining} companies remain after pruning.")


if __name__ == "__main__":
    main()
