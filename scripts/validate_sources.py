from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from urllib.parse import urlparse


KOREAN_LANGUAGE_VALUES = {"ko", "kr", "korean"}
AUTHORITATIVE_TIERS = {"tier0", "tier1", "tier2"}
KOREAN_HOST_MARKERS = (
    ".kr",
    "newsis.com",
    "yna.co.kr",
    "hankyung.com",
    "mk.co.kr",
    "sedaily.com",
    "chosun.com",
    "joongang.co.kr",
    "donga.com",
    "etnews.com",
    "zdnet.co.kr",
)


def contains_hangul(text: str) -> bool:
    return any("\uac00" <= char <= "\ud7a3" for char in text)


def is_korean_url(url: str) -> bool:
    parsed = urlparse(url)
    host = (parsed.netloc or "").lower()
    return any(marker in host for marker in KOREAN_HOST_MARKERS)


def english_authoritative(current: dict) -> bool:
    language = str(current.get("language", "")).lower()
    if language and language not in {"en", "eng", "english"}:
        return False
    if current.get("authoritativeEnglish") is True:
        return True
    tier = str(current.get("sourceTier", "")).lower()
    if tier and tier in AUTHORITATIVE_TIERS:
        return True
    source_type = str(current.get("sourceType", "")).lower()
    if source_type in {"official", "official_site", "newsroom", "blog", "regulatory_filing", "registry", "pricing", "app_store", "authoritative_media"}:
        return True
    if current.get("isOfficial") is True or current.get("isAuthoritative") is True:
        return True
    return False


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def scan_json(path: Path) -> list[str]:
    issues: list[str] = []
    data = load_json(path)
    stack = [data]
    while stack:
        current = stack.pop()
        if isinstance(current, dict):
            language = str(current.get("language", "")).lower()
            decisive = bool(current.get("decisive", False))
            source_type = str(current.get("sourceType", "")).lower()
            url = str(current.get("url", "") or current.get("link", "") or current.get("sourceUrl", ""))
            publisher = str(current.get("publisher", "") or current.get("sourceName", "") or current.get("title", ""))
            if decisive and (
                language in KOREAN_LANGUAGE_VALUES
                or is_korean_url(url)
                or contains_hangul(publisher)
            ):
                issues.append(f"{path}: decisive fact relies on Korean-language source.")
            if decisive and not english_authoritative(current):
                issues.append(f"{path}: decisive fact is missing authoritative English-language support.")
            if source_type == "press_release" and current.get("isIndependent") is True:
                issues.append(f"{path}: official release incorrectly labeled as independent media.")
            if "number" in current and current.get("number") and not current.get("asOf"):
                issues.append(f"{path}: numeric claim is missing an as-of date.")
            supporting_sources = current.get("supportingSources")
            if decisive and isinstance(supporting_sources, list):
                if not any(isinstance(item, dict) and english_authoritative(item) for item in supporting_sources):
                    issues.append(f"{path}: decisive claim has no authoritative English-language supporting source.")
            for value in current.values():
                if isinstance(value, (dict, list)):
                    stack.append(value)
        elif isinstance(current, list):
            stack.extend(current)
    return issues


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+")
    parser.add_argument("--json-output", default="")
    args = parser.parse_args()

    issues: list[str] = []
    for raw_path in args.paths:
        path = Path(raw_path)
        if path.exists() and path.suffix == ".json":
            issues.extend(scan_json(path))

    payload = {"ok": not issues, "issues": issues}
    if args.json_output:
        Path(args.json_output).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if issues:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
