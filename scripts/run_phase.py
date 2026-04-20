from __future__ import annotations

import argparse
import json
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from ai_watch.html_tools import VISIBLE_TS_RE, ensure_canonical_page_mapping, extract_order_map
from ai_watch.manifest import (
    CANONICAL_PAGE_MAP,
    DOMAIN_SCORECARDS,
    NON_NEGOTIABLE_RULES,
    ORCHESTRATOR_SCHEDULE,
    PHASE_REQUIRED_OUTPUTS,
    SOURCE_PRIORITY,
    format_visible_kst,
    kst_date_string,
    phase_contract,
    phase_ids,
    phase_suffix,
    state_phase_root,
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def utc_now_iso() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def require_server_runtime() -> None:
    github_actions = os.environ.get("GITHUB_ACTIONS", "").lower() == "true"
    runner_environment = os.environ.get("RUNNER_ENVIRONMENT", "").lower()
    if github_actions and runner_environment == "github-hosted":
        return
    raise SystemExit(
        "run_phase.py is server-only for AI Watch automation. "
        "Execute it on GitHub-hosted runners through GitHub Actions."
    )


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_jsonl(path: Path, records: list[dict[str, Any]] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = records or []
    body = "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows)
    path.write_text(body, encoding="utf-8")


def page_for_phase(phase_id: str, explicit_page: str | None = None) -> str:
    if explicit_page:
        return explicit_page
    return phase_contract(phase_id).page or ""


def common_metadata(phase_id: str, page: str, run_date: str) -> dict[str, Any]:
    contract = phase_contract(phase_id)
    return {
        "phase": phase_id,
        "kind": contract.kind,
        "domain": contract.domain,
        "page": page or "global",
        "generatedAt": utc_now_iso(),
        "runDateKst": run_date,
        "scheduledStartKst": ORCHESTRATOR_SCHEDULE["kst_start"],
        "phaseSlotKst": contract.kst_slot,
        "stateBranch": "ai-watch-state",
    }


def default_json_payload(file_name: str, phase_id: str, page: str, run_date: str) -> dict[str, Any]:
    contract = phase_contract(phase_id)
    base = common_metadata(phase_id, page, run_date)

    if file_name == "preflight_report.json":
        return base | {
            "status": "ok",
            "checks": {
                "githubHostedRuntime": True,
                "defaultBranchSchedule": True,
                "serverOnlyGuard": True,
            },
        }
    if file_name == "source_registry_health.json":
        return base | {"status": "ok", "tier0Reachability": [], "tier1Reachability": []}
    if file_name == "phase_queue.json":
        return base | {"orchestrator": "needs-based", "notes": ["Single scheduled workflow; no time-fragmented cron fanout."]}
    if file_name == "source_freshness.json":
        return base | {
            "status": "ok",
            "changedSources": [],
            "ttlPolicy": {
                "official_release_days": 7,
                "app_store_days": 3,
                "funding_days": 14,
                "hq_days": 90,
                "partnership_days": 7,
                "policy_days": 14,
            },
        }
    if file_name == "feed_health.json":
        return base | {"status": "ok", "feedsChecked": [], "newsroomsChecked": []}
    if file_name == "updates.json":
        return base | {
            "updates": [],
            "notes": ["Scaffold run; merge Codex findings during repository execution."],
            "fallbackModeIfNoExternalNews": "review_existing_content_and_refresh_trends",
            "mustProduceReviewDelta": True,
        }
    if file_name == "contradictions.json":
        return base | {"contradictions": []}
    if file_name == "source_quality_report.json":
        return base | {"decisiveSourceLanguage": "english-first", "tierPriority": SOURCE_PRIORITY}
    if file_name == "verification.json":
        return base | {
            "status": "ok",
            "checks": [],
            "legacyPolicy": "retain existing published companies by default",
            "fallbackReviewRequired": True,
            "noExternalNewsPolicy": "surface publishable logic, structure, score, or source-quality improvements",
        }
    if file_name == "removal_candidates.json":
        return base | {"candidates": []}
    if file_name == "unsupported_claims.json":
        return base | {"claims": []}
    if file_name == "source_integrity.json":
        return base | {"decisiveLanguagePolicy": "english-authoritative-first", "koreanDecisiveFacts": []}
    if file_name == "scout_candidates.json":
        return base | {"candidates": [], "candidatePool": "global-excluding-south-korea-and-china-hq"}
    if file_name == "scout_rejections.json":
        return base | {"rejections": [], "defaultBias": "prefer software/service/engine/enabling-tech over hardware-first vendors"}
    if file_name == "reserve_candidates.json":
        return base | {"reserve": [], "reasons": ["Reject or reserve unclear HQ, South Korea/China HQ, unicorns, stale claims, and hardware-first candidates."]}
    if file_name == "competitor_map.json":
        return base | {"items": []}
    if file_name == "manufacturer_strategy.json":
        return base | {"items": []}
    if file_name == "ranking_proposal.json":
        return base | {"ranking": [], "rule": "Only newly discovered approved candidates can be ranked 1..N."}
    if file_name == "entity_resolution.json":
        return base | {"resolved": [], "duplicateIds": []}
    if file_name == "alias_map.json":
        return base | {"aliases": {}}
    if file_name == "evidence_index.json":
        return base | {"count": 0, "schema": ["source_id", "source_type", "published_at", "retrieved_at_utc", "quote", "confidence", "ttl_days"]}
    if file_name == "source_tiers.json":
        return base | {"tiers": SOURCE_PRIORITY}
    if file_name == "claim_summary.json":
        return base | {"claimCount": 0, "coreFields": list(contract.fail_closed_fields)}
    if file_name == "claim_conflicts.json":
        return base | {"conflicts": []}
    if file_name == "staleness_gate.json":
        return base | {"status": "ok", "staleClaims": 0, "freshClaims": 0}
    if file_name == "scores.json":
        scorecard = DOMAIN_SCORECARDS.get(page or "", {})
        return base | {
            "scores": [],
            "formula": {"model": scorecard.get("version", "deterministic_a_g"), "weights": scorecard.get("weights", {})},
            "requiredTrackingFields": scorecard.get("required_tracking_fields", []),
            "failClosed": list(contract.fail_closed_fields),
        }
    if file_name == "score_evidence_map.json":
        return base | {"evidence": {}}
    if file_name == "ranking_final.json":
        return base | {"ranking": [], "tieBreakOrder": ["revenue strength", "traction recency", "primary-source quality", "strategic fit", "defensibility"]}
    if file_name == "ranking_audit.json":
        return base | {"pages": {}}
    if file_name == "timestamp_audit.json":
        return base | {"pages": {}}
    if file_name == "publish_diff_guard.json":
        return base | {"status": "ok", "allowedPathsOnly": True, "blockedChanges": []}
    if file_name == "recency_recheck.json":
        return base | {"status": "ok", "recheckedSources": [], "breakingChanges": []}
    if file_name == "global_qa.json":
        return base | {
            "status": "ok",
            "warnings": [],
            "blockers": [],
            "reviewDrivenImprovementRequired": True,
            "noNoopDailyRun": True,
        }
    if file_name == "publish_blockers.json":
        return base | {"blockers": []}
    if file_name == "retry_report.json":
        return base | {"retryable": [], "nonRetryable": []}
    if file_name == "publish_decision.json":
        return base | {
            "decision": "blocked_until_delta",
            "reason": "Full daily runs must produce either a fresh-news delta or a validated review-driven improvement.",
        }
    if file_name == "smoke_report.json":
        return base | {"status": "ok", "pages": {}, "checks": ["timestamp", "ranking", "publish_path", "anchors"]}
    return base


def default_markdown_payload(file_name: str, phase_id: str, page: str, run_date: str) -> str:
    contract = phase_contract(phase_id)
    title_map = {
        "updates.md": "Update Notes",
        "logic_issues.md": "Logic Issues",
        "candidate_verify_report.md": "Candidate Verify Report",
        "score_rationale.md": "Score Rationale",
        "render_log.md": "Render Log",
        "recency_recheck.md": "Recency Recheck",
        "global_qa.md": "Global QA",
        "retry_actions.md": "Retry Actions",
        "smoke_report.md": "Post Publish Smoke",
    }
    title = title_map.get(file_name, file_name)
    lines = [
        f"# {title}",
        "",
        f"- phase: `{phase_id}`",
        f"- page: `{page or 'global'}`",
        f"- run date (KST): `{run_date}`",
        f"- purpose: {contract.purpose}",
        "- no-news-day contract: if net-new external updates are absent, you must still deliver a review-driven improvement by refreshing stale claims, trend cards, score rationale, logic fixes, or source-quality notes",
    ]
    if file_name == "render_log.md":
        lines.extend(
            [
                f"- visible timestamp: `{format_visible_kst()}`",
                "- renderer expectation: update canonical data first, then render HTML deterministically",
            ]
        )
    if file_name == "retry_actions.md":
        lines.append("- no retry actions generated yet")
    if file_name == "smoke_report.md":
        lines.append("- smoke checks scaffold completed")
    return "\n".join(lines) + "\n"


def default_jsonl_records(file_name: str, phase_id: str, page: str, run_date: str) -> list[dict[str, Any]]:
    if file_name == "evidence.jsonl":
        return [
            {
                "phase": phase_id,
                "page": page or "global",
                "run_date_kst": run_date,
                "source_id": "schema_example",
                "source_type": "official_company_page",
                "source_url": "https://example.com",
                "published_at": None,
                "retrieved_at_utc": utc_now_iso(),
                "quote": "",
                "confidence": 0.0,
                "ttl_days": 14,
                "verification_status": "schema_only",
            }
        ]
    if file_name == "claims.jsonl":
        return [
            {
                "phase": phase_id,
                "page": page or "global",
                "run_date_kst": run_date,
                "claim_id": "schema_example",
                "company_id": "schema_example",
                "field": "headquarters_country",
                "value": "",
                "source_id": "schema_example",
                "source_type": "official_company_page",
                "published_at": None,
                "retrieved_at_utc": utc_now_iso(),
                "quote": "",
                "confidence": 0.0,
                "ttl_days": 30,
                "verification_status": "schema_only",
            }
        ]
    return []


def codex_prompt_health() -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for known_phase_id in phase_ids():
        contract = phase_contract(known_phase_id)
        if not contract.runs_codex:
            continue
        prompt = repo_root() / (contract.prompt_file or "")
        entries.append(
            {
                "phase": known_phase_id,
                "promptFile": contract.prompt_file,
                "exists": prompt.exists(),
            }
        )
    return entries


def required_skill_health() -> list[dict[str, Any]]:
    skills = [
        ".agents/skills/source-freshness/SKILL.md",
        ".agents/skills/company-factcheck/SKILL.md",
        ".agents/skills/render-regression/SKILL.md",
    ]
    return [{"path": skill, "exists": (repo_root() / skill).exists()} for skill in skills]


def enrich_preflight_outputs(phase_root: Path, run_date: str) -> None:
    prompt_health = codex_prompt_health()
    skill_health = required_skill_health()
    page_health = [
        {
            "page": page_key,
            "targetPath": page_meta["target_path"],
            "exists": (repo_root() / page_meta["target_path"]).exists(),
        }
        for page_key, page_meta in CANONICAL_PAGE_MAP.items()
    ]
    workflow_path = ".github/workflows/ai-watch-scheduler.yml"
    workflow_exists = (repo_root() / workflow_path).exists()
    preflight_payload = default_json_payload("preflight_report.json", "preflight_source_health", "", run_date)
    preflight_payload["checks"] = {
        "githubHostedRuntime": True,
        "workflowPresent": workflow_exists,
        "pageTargetsPresent": all(item["exists"] for item in page_health),
        "codexPromptsPresent": all(item["exists"] for item in prompt_health),
        "skillsPresent": all(item["exists"] for item in skill_health),
    }
    preflight_payload["workflowPath"] = workflow_path
    preflight_payload["pages"] = page_health
    preflight_payload["codexPrompts"] = prompt_health
    preflight_payload["skills"] = skill_health
    preflight_payload["phaseCount"] = len(phase_ids())
    preflight_payload["schedule"] = ORCHESTRATOR_SCHEDULE
    preflight_payload["reliabilityNotes"] = [
        "GitHub scheduled workflows are not hard real-time.",
        "Top-of-hour triggers are intentionally avoided.",
        "Use workflow_dispatch for replay or manual reruns.",
    ]
    write_json(phase_root / "preflight_report.json", preflight_payload)

    source_registry_payload = default_json_payload("source_registry_health.json", "preflight_source_health", "", run_date)
    source_registry_payload["tier0Reachability"] = SOURCE_PRIORITY["tier0"]
    source_registry_payload["tier1Reachability"] = SOURCE_PRIORITY["tier1"]
    source_registry_payload["policy"] = "Source priority is enforced before claim verification."
    write_json(phase_root / "source_registry_health.json", source_registry_payload)

    phase_queue_payload = default_json_payload("phase_queue.json", "preflight_source_health", "", run_date)
    phase_queue_payload["phaseIds"] = phase_ids()
    phase_queue_payload["notes"] = [
        "One orchestrator workflow controls sequencing through needs.",
        "Phase artifacts are restored from uploaded artifacts and the state branch only.",
    ]
    write_json(phase_root / "phase_queue.json", phase_queue_payload)


def ensure_phase_outputs(phase_root: Path, phase_id: str, page: str, run_date: str) -> None:
    for file_name in PHASE_REQUIRED_OUTPUTS[phase_suffix(phase_id)]:
        target = phase_root / file_name
        if file_name.endswith(".json"):
            write_json(target, default_json_payload(file_name, phase_id, page, run_date))
        elif file_name.endswith(".md"):
            write_text(target, default_markdown_payload(file_name, phase_id, page, run_date))
        elif file_name.endswith(".jsonl"):
            write_jsonl(target, default_jsonl_records(file_name, phase_id, page, run_date))
        else:
            write_text(target, "")


def bootstrap_phase(phase_id: str, run_date: str, explicit_page: str | None = None) -> Path:
    contract = phase_contract(phase_id)
    page = page_for_phase(phase_id, explicit_page)
    phase_root = state_phase_root(run_date, page or None, phase_id)
    phase_root.mkdir(parents=True, exist_ok=True)

    page_path = CANONICAL_PAGE_MAP[page]["target_path"] if page else ""
    write_json(
        phase_root / "run_manifest.json",
        {
            "phase": phase_id,
            "kind": contract.kind,
            "domain": contract.domain,
            "page": page or "global",
            "runDate": run_date,
            "phaseRoot": phase_root.as_posix(),
            "pagePath": page_path,
            "promptFile": contract.prompt_file or "",
            "runsCodex": contract.runs_codex,
            "timeoutMinutes": contract.timeout_minutes,
            "gates": list(contract.gates),
            "failClosedFields": list(contract.fail_closed_fields),
        },
    )
    write_json(
        phase_root / "phase_contract.json",
        {
            "id": contract.id,
            "kind": contract.kind,
            "domain": contract.domain,
            "purpose": contract.purpose,
            "inputs": list(contract.inputs),
            "outputs": list(contract.outputs),
            "agents": list(contract.agents),
            "gates": list(contract.gates),
            "timeout_minutes": contract.timeout_minutes,
            "retry_policy": {
                "max_attempts": contract.retry_policy.max_attempts,
                "backoff_seconds": list(contract.retry_policy.backoff_seconds),
            },
            "evidence_contract": {
                "min_sources_per_core_claim": contract.evidence_contract.min_sources_per_core_claim,
                "min_sources_for_mutable_claim": contract.evidence_contract.min_sources_for_mutable_claim,
                "max_staleness_days": contract.evidence_contract.max_staleness_days,
                "freshness_fields": list(contract.evidence_contract.freshness_fields),
            },
            "fail_closed_fields": list(contract.fail_closed_fields),
            "page": page or "global",
            "prompt_file": contract.prompt_file or "",
            "kst_slot": contract.kst_slot,
            "runs_codex": contract.runs_codex,
        },
    )

    context = "\n".join(
        [
            "# AI Watch Phase Context",
            "",
            f"- phase: `{phase_id}`",
            f"- kind: `{contract.kind}`",
            f"- domain: `{contract.domain}`",
            f"- page: `{page or 'global'}`",
            f"- run date (KST): `{run_date}`",
            f"- phase root: `{phase_root.as_posix()}`",
            f"- publish target: `{page_path or 'n/a'}`",
            f"- prompt file: `{contract.prompt_file or 'script-only phase'}`",
            f"- timeout: `{contract.timeout_minutes} minutes`",
            f"- purpose: {contract.purpose}",
            "- source model: raw source -> evidence -> claim -> verify -> score -> render -> publish",
            "- fail-closed: if HQ, unicorn status, category, valuation, timestamps, or ranking claims are unsupported, stale, or contradictory, do not publish",
            "- freshness contract: use explicit TTL / recency logic instead of timestamp-only refreshes",
            "- no-news-day policy: if external updates are absent, refresh trend evidence, stale claims, score rationale, logic issues, or source-quality notes until a validated publish delta exists",
            "- runner model: GitHub-hosted jobs are ephemeral; consume artifacts or committed state only",
            "- decisive evidence: official English / filing / registry / developer-doc sources outrank Korean-language media",
        ]
    )
    write_text(phase_root / "phase_context.md", context + "\n")

    if contract.runs_codex:
        scorecard_note = ""
        if contract.kind == "score" and page in DOMAIN_SCORECARDS:
            scorecard = DOMAIN_SCORECARDS[page]
            scorecard_note = (
                "\n".join(
                    [
                        "",
                        f"- scorecard version: {scorecard['version']}",
                        f"- scorecard weights: {json.dumps(scorecard['weights'], ensure_ascii=False)}",
                        f"- required tracking fields: {', '.join(scorecard.get('required_tracking_fields', []))}",
                    ]
                )
                + "\n"
            )
        write_text(
            phase_root / "codex_prompt_context.md",
            "\n".join(
                [
                    "# Codex Execution Notes",
                    "",
                    f"- agents: {', '.join(contract.agents)}",
                    f"- gates: {', '.join(contract.gates)}",
                    f"- fail-closed fields: {', '.join(contract.fail_closed_fields)}",
                    "",
                    "Work from the claim/evidence contract first. Do not trust uncited page text. Keep changes deterministic and conservative.",
                ]
            )
            + scorecard_note
            + "\n",
        )
    return phase_root


def load_codex_summary(phase_root: Path) -> str:
    codex_output = phase_root / "codex.final.md"
    if not codex_output.exists():
        return ""
    return codex_output.read_text(encoding="utf-8").strip()


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
    if len(matches) < 2:
        issues.append("Expected at least two visible timestamps (hero and footer).")
    for label in matches:
        if "KST" not in label:
            issues.append(f"Missing KST suffix: {label}")
    return {
        "page": html_path.as_posix(),
        "visibleLabels": matches,
        "pass": not issues,
        "issues": issues,
    }


def consolidate_phase(phase_id: str, run_date: str, explicit_page: str | None = None, visible_timestamp: str | None = None) -> Path:
    page = page_for_phase(phase_id, explicit_page)
    phase_root = state_phase_root(run_date, page or None, phase_id)
    phase_root.mkdir(parents=True, exist_ok=True)
    ensure_phase_outputs(phase_root, phase_id, page, run_date)

    codex_summary = load_codex_summary(phase_root)
    if codex_summary:
        write_json(
            phase_root / "codex_summary.json",
            {
                **common_metadata(phase_id, page, run_date),
                "present": True,
                "path": (phase_root / "codex.final.md").as_posix(),
            },
        )

    if phase_suffix(phase_id) == "render":
        visible = visible_timestamp or format_visible_kst()
        normalized = ensure_canonical_page_mapping(repo_root(), visible)
        ranking_payload = default_json_payload("ranking_audit.json", phase_id, page, run_date)
        ranking_payload["pages"] = {
            key: build_ranking_audit(repo_root() / data["target_path"])
            for key, data in CANONICAL_PAGE_MAP.items()
        }
        ranking_payload["normalized"] = normalized
        timestamp_payload = default_json_payload("timestamp_audit.json", phase_id, page, run_date)
        timestamp_payload["pages"] = {
            key: build_timestamp_audit(repo_root() / data["target_path"])
            for key, data in CANONICAL_PAGE_MAP.items()
        }
        write_json(phase_root / "ranking_audit.json", ranking_payload)
        write_json(phase_root / "timestamp_audit.json", timestamp_payload)
        write_json(
            phase_root / "publish_diff_guard.json",
            default_json_payload("publish_diff_guard.json", phase_id, page, run_date)
            | {
                "allowedPathsOnly": True,
                "allowedPaths": ["1/index.html", "2/index.html", f".state/runs/{run_date}"],
            },
        )
        render_log = default_markdown_payload("render_log.md", phase_id, page, run_date)
        if codex_summary:
            render_log += "\n## Codex Summary\n\n" + codex_summary + "\n"
        write_text(phase_root / "render_log.md", render_log)

    if phase_suffix(phase_id) == "recency":
        recency_note = default_markdown_payload("recency_recheck.md", phase_id, page, run_date)
        recency_note += "- publish-time recheck is a required gate before commit\n"
        write_text(phase_root / "recency_recheck.md", recency_note)

    if phase_suffix(phase_id) == "global_qa" and codex_summary:
        qa_md = default_markdown_payload("global_qa.md", phase_id, page, run_date)
        qa_md += "\n## Codex Summary\n\n" + codex_summary + "\n"
        write_text(phase_root / "global_qa.md", qa_md)

    return phase_root


def execute_phase(phase_id: str, run_date: str, explicit_page: str | None = None, visible_timestamp: str | None = None) -> Path:
    phase_root = bootstrap_phase(phase_id, run_date, explicit_page)
    if phase_suffix(phase_id) == "preflight":
        enrich_preflight_outputs(phase_root, run_date)
    return consolidate_phase(phase_id, run_date, explicit_page, visible_timestamp)


def smoke_run(run_date: str, visible_timestamp: str | None = None) -> None:
    visible = visible_timestamp or format_visible_kst()
    for phase_id in ("ai1_render_staging", "ai2_render_staging", "global_recency_recheck", "global_qa", "post_publish_smoke"):
        consolidate_phase(phase_id, run_date, None, visible)

    smoke_root = state_phase_root(run_date, None, "post_publish_smoke")
    smoke_payload = default_json_payload("smoke_report.json", "post_publish_smoke", "", run_date)
    smoke_payload["pages"] = {
        key: {
            "ranking": build_ranking_audit(repo_root() / data["target_path"]),
            "timestamp": build_timestamp_audit(repo_root() / data["target_path"]),
        }
        for key, data in CANONICAL_PAGE_MAP.items()
    }
    write_json(smoke_root / "smoke_report.json", smoke_payload)
    smoke_md = default_markdown_payload("smoke_report.md", "post_publish_smoke", "", run_date)
    smoke_md += f"- visible timestamp checked: `{visible}`\n"
    write_text(smoke_root / "smoke_report.md", smoke_md)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", required=True, choices=["bootstrap", "consolidate", "execute", "smoke"])
    parser.add_argument("--phase", default="")
    parser.add_argument("--page", default="")
    parser.add_argument("--run-date", default="")
    parser.add_argument("--visible-timestamp", default="")
    args = parser.parse_args()

    require_server_runtime()

    run_date = args.run_date or kst_date_string()

    if args.mode == "bootstrap":
        if not args.phase:
            raise SystemExit("--phase is required for bootstrap mode")
        bootstrap_phase(args.phase, run_date, args.page or None)
        return

    if args.mode == "consolidate":
        if not args.phase:
            raise SystemExit("--phase is required for consolidate mode")
        consolidate_phase(args.phase, run_date, args.page or None, args.visible_timestamp or None)
        return

    if args.mode == "execute":
        if not args.phase:
            raise SystemExit("--phase is required for execute mode")
        execute_phase(args.phase, run_date, args.page or None, args.visible_timestamp or None)
        return

    smoke_run(run_date, args.visible_timestamp or None)


if __name__ == "__main__":
    main()
