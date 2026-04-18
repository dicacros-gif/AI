from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any

from ai_watch.html_tools import VISIBLE_TS_RE, ensure_canonical_page_mapping, extract_order_map
from ai_watch.manifest import (
    CANONICAL_PAGE_MAP,
    NON_NEGOTIABLE_RULES,
    PHASE_REQUIRED_OUTPUTS,
    SOURCE_PRIORITY,
    format_visible_kst,
    kst_date_string,
    phase_suffix,
    state_phase_root,
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def default_phase_payloads(phase: str, page: str) -> dict[str, Any]:
    now = datetime.now().isoformat()
    suffix = phase_suffix(phase)
    if suffix == "update":
        return {
            "updates.json": {"phase": phase, "page": page, "generatedAt": now, "updates": [], "notes": ["No agent merge content yet; scaffold run."]},
            "updates.md": "# Update Notes\n\n- No merged update content yet.\n",
            "contradictions.json": {"phase": phase, "page": page, "generatedAt": now, "contradictions": []},
            "source_quality_report.json": {"phase": phase, "page": page, "generatedAt": now, "decisiveSourceLanguage": "english-first", "legacyWarnings": []},
        }
    if suffix == "verify":
        return {
            "verification.json": {"phase": phase, "page": page, "generatedAt": now, "status": "ok", "legacyPolicy": "existing companies stay published; violations become removal candidates"},
            "logic_issues.md": "# Logic Issues\n\n- No merged logic issues yet.\n",
            "removal_candidates.json": {"phase": phase, "page": page, "generatedAt": now, "candidates": []},
            "unsupported_claims.json": {"phase": phase, "page": page, "generatedAt": now, "claims": []},
            "source_integrity.json": {"phase": phase, "page": page, "generatedAt": now, "decisiveLanguagePolicy": "english-authoritative-first", "koreanDecisiveFacts": []},
        }
    if suffix == "scout":
        return {
            "scout_candidates.json": {"phase": phase, "page": page, "generatedAt": now, "candidates": []},
            "scout_rejections.json": {"phase": phase, "page": page, "generatedAt": now, "rejections": [], "defaultBias": "prefer U.S.-headquartered software/service/engine/technology companies over pure hardware vendors when evidence quality is comparable"},
            "reserve_candidates.json": {"phase": phase, "page": page, "generatedAt": now, "reserve": [], "reasons": ["Reject or reserve South Korea/China HQ, unicorns, unclear HQ, and pure hardware-first vendors without service/engine leverage. Prefer U.S.-headquartered candidates first when evidence quality is comparable."]},
            "competitor_map.json": {"phase": phase, "page": page, "generatedAt": now, "items": []},
            "manufacturer_strategy.json": {"phase": phase, "page": page, "generatedAt": now, "items": []},
            "ranking_proposal.json": {"phase": phase, "page": page, "generatedAt": now, "ranking": [], "rule": "Only newly discovered approved candidates can be ranked 1..N."},
        }
    if suffix == "score":
        return {
            "scores.json": {"phase": phase, "page": page, "generatedAt": now, "scores": []},
            "score_rationale.md": "# Score Rationale\n\n- No approved new candidates to score in this scaffold run.\n",
            "score_evidence_map.json": {"phase": phase, "page": page, "generatedAt": now, "evidence": {}},
            "ranking_final.json": {"phase": phase, "page": page, "generatedAt": now, "ranking": [], "tieBreakOrder": ["revenue strength", "traction recency", "primary-source quality", "strategic fit", "defensibility"]},
        }
    if suffix == "render":
        return {
            "render_log.md": "# Render Log\n\n- Timestamp and canonical path normalization applied.\n",
            "ranking_audit.json": {"phase": phase, "page": page, "generatedAt": now, "pages": {}},
            "timestamp_audit.json": {"phase": phase, "page": page, "generatedAt": now, "pages": {}},
        }
    if suffix == "global_qa":
        return {
            "global_qa.md": "# Global QA\n\n- No merged blockers recorded yet.\n",
            "global_qa.json": {"phase": phase, "page": page, "generatedAt": now, "status": "ok", "warnings": [], "blockers": []},
            "publish_blockers.json": {"phase": phase, "generatedAt": now, "blockers": []},
        }
    if suffix == "retry":
        return {
            "retry_report.json": {"phase": phase, "generatedAt": now, "retryable": [], "nonRetryable": []},
            "retry_actions.md": "# Retry Actions\n\n- No retry actions generated.\n",
        }
    if suffix == "republish":
        return {
            "republish_decision.json": {"phase": phase, "generatedAt": now, "decision": "qa_only", "reason": "No validated render delta found."},
            "republish_log.md": "# Republish Decision\n\n- No republish required.\n",
        }
    return {
        "final_check.json": {"phase": phase, "generatedAt": now, "status": "ok", "blockers": []},
        "final_check.md": "# Final Check\n\n- Final consistency check scaffold completed.\n",
    }


def bootstrap_phase(phase: str, page: str, role: str, run_date: str) -> Path:
    phase_root = state_phase_root(run_date, page or None, phase)
    phase_root.mkdir(parents=True, exist_ok=True)
    agents_dir = phase_root / "agents"
    agents_dir.mkdir(parents=True, exist_ok=True)
    output_json = agents_dir / f"{role}.json"
    output_md = agents_dir / f"{role}.md"
    page_path = CANONICAL_PAGE_MAP[page]["target_path"] if page else ""
    agent_file = f".codex/agents/{role}.toml"

    write_json(
        phase_root / "run_manifest.json",
        {
            "phase": phase,
            "page": page,
            "runDate": run_date,
            "pagePath": page_path,
            "phaseRoot": phase_root.as_posix(),
            "nonNegotiableRules": NON_NEGOTIABLE_RULES,
            "sourcePriority": SOURCE_PRIORITY,
        },
    )
    context = "\n".join(
        [
            "# AI Watch Phase Context",
            "",
            f"- phase: `{phase}`",
            f"- page: `{page or 'global'}`",
            f"- run date (KST): `{run_date}`",
            f"- phase root: `{phase_root.as_posix()}`",
            f"- publish target: `{page_path or 'n/a'}`",
            f"- agent role: `{role}`",
            f"- agent file: `{agent_file}`",
            f"- required JSON output: `{output_json.as_posix()}`",
            f"- required Markdown output: `{output_md.as_posix()}`",
            "- 신규 업체 규칙: South Korea / China HQ 불가, HQ 불명확 시 reserve/reject, unicorn 불가, revenue evidence 필수.",
            "- 우대 규칙: HW 단독 업체보다 SW·서비스·엔진·기술형 회사를 우대하고, 근거 품질이 비슷하면 미국 본사 후보를 먼저 본다.",
            "- 기존 게시 업체는 자동 삭제하지 않는다. 위반 소지가 있으면 removal candidate로만 기록한다.",
            "- Non-render phase에서는 published HTML을 수정하지 않는다.",
        ]
    )
    write_text(phase_root / "phase_context.md", context + "\n")
    if not output_json.exists():
        write_json(output_json, {"role": role, "phase": phase, "page": page, "status": "pending"})
    if not output_md.exists():
        write_text(output_md, f"# {role}\n\n- Pending Codex execution.\n")
    return phase_root


def load_agent_payloads(phase_root: Path) -> list[dict[str, Any]]:
    payloads: list[dict[str, Any]] = []
    agents_dir = phase_root / "agents"
    if not agents_dir.exists():
        return payloads
    for path in sorted(agents_dir.glob("*.json")):
        try:
            payloads.append(json.loads(path.read_text(encoding="utf-8")))
        except json.JSONDecodeError:
            payloads.append({"role": path.stem, "status": "invalid_json"})
    return payloads


def build_ranking_audit(html_path: Path) -> dict[str, Any]:
    html = html_path.read_text(encoding="utf-8")
    order_map = extract_order_map(html)
    expected = order_map["list"]
    expected_names = [name for _, name in expected]
    expected_ranks = [rank for rank, _ in expected]
    contiguous = expected_ranks == list(range(1, len(expected_ranks) + 1))
    issues: list[str] = []
    if not contiguous:
        issues.append("List ranks are not contiguous from 1..N.")
    for section_name, pairs in order_map.items():
        names = [name for _, name in pairs]
        if pairs and names != expected_names:
            issues.append(f"{section_name} order does not match startup list order.")
    return {
        "page": html_path.as_posix(),
        "sections": order_map,
        "pass": not issues,
        "issues": issues,
    }


def build_timestamp_audit(html_path: Path) -> dict[str, Any]:
    html = html_path.read_text(encoding="utf-8")
    matches = VISIBLE_TS_RE.findall(html)
    issues: list[str] = []
    if len(matches) < 3:
        issues.append("Expected at least three visible timestamps (toolbar, hero, footer).")
    for label in matches:
        if "KST 기준" not in label:
            issues.append(f"Missing KST suffix: {label}")
    return {
        "page": html_path.as_posix(),
        "visibleLabels": matches,
        "pass": not issues,
        "issues": issues,
    }


def consolidate_phase(phase: str, page: str, run_date: str, visible_timestamp: str | None = None) -> Path:
    phase_root = state_phase_root(run_date, page or None, phase)
    phase_root.mkdir(parents=True, exist_ok=True)
    payloads = default_phase_payloads(phase, page)
    merged_agents = load_agent_payloads(phase_root)
    for file_name, payload in payloads.items():
        target = phase_root / file_name
        if isinstance(payload, str):
            write_text(target, payload)
        else:
            payload["mergedAgents"] = [item.get("role", "unknown") for item in merged_agents]
            write_json(target, payload)

    if phase_suffix(phase) == "render":
        visible = visible_timestamp or format_visible_kst()
        normalized = ensure_canonical_page_mapping(repo_root(), visible)
        ranking_payload = {
            "phase": phase,
            "page": page,
            "generatedAt": datetime.now().isoformat(),
            "pages": {
                key: build_ranking_audit(repo_root() / data["target_path"])
                for key, data in CANONICAL_PAGE_MAP.items()
            },
            "normalized": normalized,
        }
        timestamp_payload = {
            "phase": phase,
            "page": page,
            "generatedAt": datetime.now().isoformat(),
            "pages": {
                key: build_timestamp_audit(repo_root() / data["target_path"])
                for key, data in CANONICAL_PAGE_MAP.items()
            },
        }
        write_json(phase_root / "ranking_audit.json", ranking_payload)
        write_json(phase_root / "timestamp_audit.json", timestamp_payload)
        write_text(
            phase_root / "render_log.md",
            "\n".join(
                [
                    "# Render Log",
                    "",
                    f"- Canonical page mapping normalized for `{page}`.",
                    f"- Visible KST timestamp applied: `{visible}`.",
                    "- Existing companies were retained; render step is prepared to append or reorder only approved newly discovered candidates.",
                ]
            )
            + "\n",
        )
    return phase_root


def smoke_run(run_date: str, visible_timestamp: str | None = None) -> None:
    visible = visible_timestamp or format_visible_kst()
    for phase, page in [("ai1_render", "ai1"), ("ai2_render", "ai2"), ("global_qa", "")]:
        consolidate_phase(phase, page, run_date, visible)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", required=True, choices=["bootstrap", "consolidate", "smoke"])
    parser.add_argument("--phase", default="")
    parser.add_argument("--page", default="")
    parser.add_argument("--role", default="")
    parser.add_argument("--run-date", default="")
    parser.add_argument("--visible-timestamp", default="")
    args = parser.parse_args()

    run_date = args.run_date or kst_date_string()

    if args.mode == "bootstrap":
        if not args.phase or not args.role:
            raise SystemExit("--phase and --role are required for bootstrap mode")
        bootstrap_phase(args.phase, args.page, args.role, run_date)
        return

    if args.mode == "consolidate":
        if not args.phase:
            raise SystemExit("--phase is required for consolidate mode")
        consolidate_phase(args.phase, args.page, run_date, args.visible_timestamp or None)
        return

    smoke_run(run_date, args.visible_timestamp or None)


if __name__ == "__main__":
    main()
