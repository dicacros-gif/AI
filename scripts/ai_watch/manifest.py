from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

try:
    SEOUL = ZoneInfo("Asia/Seoul")
except Exception:
    SEOUL = timezone(timedelta(hours=9), "KST")
STATE_ROOT = Path(".state") / "runs"
STATE_BRANCH = "ai-watch-state"
WORKFLOW_NAME = "ai-watch-scheduler"

KST_WEEKDAYS = ["월", "화", "수", "목", "금", "토", "일"]

CANONICAL_PAGE_MAP: dict[str, dict[str, str]] = {
    "ai1": {
        "slug": "1",
        "target_path": "1/index.html",
        "legacy_source_path": "2/index.html",
        "canonical_label": "모바일 AI 개인화 추천, On-device 데이터 분석",
        "domain_summary": "mobile AI personalization, on-device data analysis, personalized AI, recommendation engine, privacy-aware UX",
        "short_title": "Personalization / On-device",
        "discovery_bias": "Exclude hardware-first vendors and favor software, service, engine, and enabling technology companies.",
    },
    "ai2": {
        "slug": "2",
        "target_path": "2/index.html",
        "legacy_source_path": "1/index.html",
        "canonical_label": "광고 AI / 모바일 광고 기술·서비스",
        "domain_summary": "ad AI, mobile advertising technology/services, AdTech, SDK, DSP, retargeting, performance marketing, video AI advertising",
        "short_title": "Ad AI / Mobile AdTech",
        "discovery_bias": "Exclude hardware-first vendors and favor software, service, engine, and enabling technology companies.",
    },
}

CANONICAL_NAV_LABELS = {
    "ai1": "🔗 1 — 모바일 AI 개인화 추천, On-device 데이터 분석",
    "ai2": "🔗 2 — 광고 AI / 모바일 광고 기술·서비스",
}

PHASE_TO_PAGE: dict[str, str] = {
    "ai1_update": "ai1",
    "ai1_verify": "ai1",
    "ai1_scout": "ai1",
    "ai1_score": "ai1",
    "ai1_render": "ai1",
    "ai2_update": "ai2",
    "ai2_verify": "ai2",
    "ai2_scout": "ai2",
    "ai2_score": "ai2",
    "ai2_render": "ai2",
}

PHASE_PROMPTS: dict[str, str] = {
    "ai1_update": ".github/codex/prompts/ai1_update.md",
    "ai1_verify": ".github/codex/prompts/ai1_verify.md",
    "ai1_scout": ".github/codex/prompts/ai1_scout.md",
    "ai1_score": ".github/codex/prompts/ai1_score.md",
    "ai1_render": ".github/codex/prompts/ai1_render.md",
    "ai2_update": ".github/codex/prompts/ai2_update.md",
    "ai2_verify": ".github/codex/prompts/ai2_verify.md",
    "ai2_scout": ".github/codex/prompts/ai2_scout.md",
    "ai2_score": ".github/codex/prompts/ai2_score.md",
    "ai2_render": ".github/codex/prompts/ai2_render.md",
    "global_qa": ".github/codex/prompts/global_qa.md",
    "retry_failed": ".github/codex/prompts/retry_failed.md",
    "republish_or_qa": ".github/codex/prompts/republish_or_qa.md",
    "final_retry_or_publish_check": ".github/codex/prompts/final_retry_or_publish_check.md",
}

PHASE_UTC_CRONS: dict[str, str] = {
    "ai1_update": "0 19 * * *",
    "ai1_verify": "20 19 * * *",
    "ai1_scout": "30 19 * * *",
    "ai1_score": "40 19 * * *",
    "ai1_render": "50 19 * * *",
    "ai2_update": "0 20 * * *",
    "ai2_verify": "20 20 * * *",
    "ai2_scout": "30 20 * * *",
    "ai2_score": "40 20 * * *",
    "ai2_render": "0 21 * * *",
    "global_qa": "10 21 * * *",
    "retry_failed": "30 21 * * *",
    "republish_or_qa": "0 22 * * *",
    "final_retry_or_publish_check": "30 22 * * *",
}

PHASE_KST_SLOTS: dict[str, str] = {
    "ai1_update": "04:00 KST",
    "ai1_verify": "04:20 KST",
    "ai1_scout": "04:30 KST",
    "ai1_score": "04:40 KST",
    "ai1_render": "04:50 KST",
    "ai2_update": "05:00 KST",
    "ai2_verify": "05:20 KST",
    "ai2_scout": "05:30 KST",
    "ai2_score": "05:40 KST",
    "ai2_render": "06:00 KST",
    "global_qa": "06:10 KST",
    "retry_failed": "06:30 KST",
    "republish_or_qa": "07:00 KST",
    "final_retry_or_publish_check": "07:30 KST",
}

SCHEDULE_TO_PHASE = {cron: phase for phase, cron in PHASE_UTC_CRONS.items()}

PHASE_REQUIRED_OUTPUTS: dict[str, list[str]] = {
    "update": ["updates.json", "updates.md", "contradictions.json", "source_quality_report.json"],
    "verify": ["verification.json", "logic_issues.md", "removal_candidates.json", "unsupported_claims.json", "source_integrity.json"],
    "scout": ["scout_candidates.json", "scout_rejections.json", "reserve_candidates.json", "competitor_map.json", "manufacturer_strategy.json", "ranking_proposal.json"],
    "score": ["scores.json", "score_rationale.md", "score_evidence_map.json", "ranking_final.json"],
    "render": ["render_log.md", "ranking_audit.json", "timestamp_audit.json"],
    "global_qa": ["global_qa.md", "global_qa.json", "publish_blockers.json"],
    "retry": ["retry_report.json", "retry_actions.md"],
    "republish": ["republish_decision.json", "republish_log.md"],
    "final_check": ["final_check.json", "final_check.md"],
}

SOURCE_PRIORITY = {
    "tier0": [
        "official company english site",
        "official company newsroom",
        "official company blog",
        "product docs",
        "official pricing/help center",
        "app store listing",
        "regulatory filing",
        "company registry",
        "investor portfolio page in english",
    ],
    "tier1": ["Reuters", "Bloomberg", "TechCrunch", "The Information", "Wired", "Fortune", "Forbes", "WSJ", "Financial Times"],
    "tier2": ["Crunchbase", "PitchBook", "CB Insights", "Dealroom", "Tracxn", "data.ai", "Sensor Tower", "Similarweb", "Gartner", "McKinsey", "IDC", "Forrester", "a16z", "Sequoia", "Accel", "Lightspeed", "Index", "Benchmark", "Greylock", "YC", "arXiv", "patents", "papers"],
    "tier3": ["Product Hunt", "GitHub", "Hacker News", "Reddit", "X", "LinkedIn"],
}

NON_NEGOTIABLE_RULES = [
    "Newly discovered startups must use deterministic rank order 1 -> N everywhere downstream.",
    "Newly discovered startups must exclude South Korea and China headquarters unless HQ is verified elsewhere and not in those countries.",
    "Existing published companies are not auto-deleted unless an explicit cleanup rule is being applied.",
    "Explicit cleanup rules remove hardware-first companies and South Korea headquartered companies below the active 51-employee threshold.",
    "New discovery and scoring exclude hardware-first vendors and favor software, service, engine, and enabling technology companies.",
    "Every visible generation timestamp must include date, weekday, time, and KST.",
    "English-language authoritative evidence is decisive; Korean-language sources cannot be the sole support for publish decisions.",
]


def kst_now() -> datetime:
    return datetime.now(SEOUL)


def kst_date_string(now: datetime | None = None) -> str:
    current = now or kst_now()
    return current.strftime("%Y-%m-%d")


def format_visible_kst(dt: datetime | None = None) -> str:
    current = dt or kst_now()
    yy = str(current.year % 100).zfill(2)
    weekday = KST_WEEKDAYS[current.weekday()]
    return f"'{yy}.{current.month}.{current.day} ({weekday}) {current:%H:%M} KST 기준"


@dataclass(frozen=True)
class AgentDefinition:
    role: str
    category: str
    description: str
    phase_tags: tuple[str, ...]
    required_outputs: tuple[str, ...]
    bias: str
    decisive_source_rule: str


def _agent(
    role: str,
    category: str,
    description: str,
    phase_tags: tuple[str, ...],
    required_outputs: tuple[str, ...],
    bias: str = "Prefer structured, source-backed findings over narrative prose.",
    decisive_source_rule: str = "English authoritative sources outrank Korean-language sources for decisive facts.",
) -> AgentDefinition:
    return AgentDefinition(
        role=role,
        category=category,
        description=description,
        phase_tags=phase_tags,
        required_outputs=required_outputs,
        bias=bias,
        decisive_source_rule=decisive_source_rule,
    )


AGENT_DEFINITIONS: dict[str, AgentDefinition] = {
    "official_primary_source_researcher": _agent("official_primary_source_researcher", "core_research", "Collect official English company webpages, pricing, newsroom, docs, product pages, and app store references.", ("update", "scout"), ("json", "md")),
    "official_blog_and_release_reader": _agent("official_blog_and_release_reader", "core_research", "Read official blogs, release notes, launch posts, and newsroom updates for product and partnership changes.", ("update", "scout"), ("json", "md")),
    "english_authoritative_media_researcher": _agent("english_authoritative_media_researcher", "core_research", "Gather independent English-language coverage from authoritative media and note dates, claims, and attribution quality.", ("update", "scout"), ("json", "md")),
    "regulatory_and_filings_checker": _agent("regulatory_and_filings_checker", "core_research", "Check regulatory filings, public corporate filings, policy references, and compliance disclosures.", ("verify", "scout"), ("json",)),
    "company_registry_checker": _agent("company_registry_checker", "core_research", "Verify legal entity basics, incorporation location, and headquarters evidence using company registries and official records.", ("verify", "scout"), ("json",)),
    "app_store_signal_checker": _agent("app_store_signal_checker", "core_research", "Inspect app store presence, screenshots, mobile-first signals, ratings, and surface evidence without inventing usage metrics.", ("update", "scout"), ("json",)),
    "product_surface_checker": _agent("product_surface_checker", "core_research", "Verify product surfaces, use cases, SDKs, APIs, browser extensions, and supported channels.", ("update", "scout"), ("json",)),
    "mobile_first_ux_checker": _agent("mobile_first_ux_checker", "core_research", "Judge whether the company is genuinely mobile-first, mobile-native, or deeply mobile-integrated.", ("scout", "score"), ("json",)),
    "on_device_architecture_checker": _agent("on_device_architecture_checker", "core_research", "Verify on-device, edge, privacy-preserving, offline, or NPU claims and distinguish them from pure cloud wrappers.", ("scout", "score"), ("json",)),
    "privacy_security_compliance_checker": _agent("privacy_security_compliance_checker", "core_research", "Verify privacy, security, data residency, SOC2, HIPAA, GDPR, or similar compliance claims.", ("verify", "scout", "score"), ("json",)),
    "founder_identity_checker": _agent("founder_identity_checker", "core_research", "Verify founder names and identities using authoritative English sources or official company materials.", ("scout",), ("json",)),
    "leadership_background_checker": _agent("leadership_background_checker", "core_research", "Verify leadership background and relevant domain experience without relying on weak biographies.", ("scout", "score"), ("json",)),
    "employee_count_checker": _agent("employee_count_checker", "core_research", "Cross-check employee count claims using authoritative references and conservative estimates only.", ("scout", "verify"), ("json",)),
    "funding_database_checker": _agent("funding_database_checker", "core_research", "Check funding rounds and amounts using authoritative English sources and reputable databases.", ("update", "scout", "score"), ("json",)),
    "investor_lineage_checker": _agent("investor_lineage_checker", "core_research", "Verify investor names, strategic investors, and investor tier quality.", ("scout", "score"), ("json",)),
    "valuation_unicorn_guard": _agent("valuation_unicorn_guard", "core_research", "Block newly discovered startups with verified valuation at or above $1B and mark borderline cases unverified.", ("verify", "scout", "global_qa"), ("json",), bias="Err on exclusion when unicorn status is unclear."),
    "geography_exclusion_guard": _agent("geography_guard", "core_research", "Verify headquarters geography from legal or official operating-base evidence and reject unclear HQ.", ("verify", "scout", "global_qa"), ("json",), bias="HQ ambiguity means ineligible for newly discovered candidates."),
    "korea_china_exclusion_guard": _agent("korea_china_exclusion_guard", "core_research", "Ensure newly discovered startups headquartered in South Korea or China are rejected; legacy published violations become removal candidates.", ("verify", "scout", "global_qa"), ("json",), bias="New candidates from South Korea or China are never eligible."),
    "revenue_model_verifier": _agent("revenue_model_verifier", "core_research", "Verify monetization, pricing, payment conversion, contracts, ARR evidence, or credible revenue proxies.", ("scout", "score"), ("json",), bias="No revenue evidence means reserve or reject."),
    "traction_metric_checker": _agent("traction_metric_checker", "core_research", "Verify traction metrics, usage claims, customer counts, GMV, ARR, or growth indicators conservatively.", ("update", "scout", "score"), ("json",)),
    "competitor_mapper": _agent("competitor_mapper", "core_research", "Map three relevant competitors and summarize strength/weakness comparisons using evidence-backed product logic.", ("scout", "score"), ("json", "md")),
    "manufacturer_strategy_agent": _agent("manufacturer_strategy_agent", "core_research", "Develop smartphone manufacturer partnership scenarios, R/S logic, and OEM strategic fit.", ("scout", "score", "render"), ("json", "md"), bias="Exclude hardware-first vendors and prefer software/service/engine assets that can slot into OEM stacks."),
    "partnership_deal_checker": _agent("partnership_deal_checker", "core_research", "Verify partnerships, LOIs, pilots, integrations, and co-selling signals using primary or authoritative sources.", ("update", "scout", "score"), ("json",)),
    "mna_scenario_agent": _agent("mna_scenario_agent", "core_research", "Assess likely acquirers, asset value, and M&A logic grounded in comparable deals and asset defensibility.", ("scout", "score"), ("json", "md")),
    "market_size_trend_curator": _agent("market_size_trend_curator", "core_research", "Collect market-size, trend, research, and industry direction signals from authoritative English research.", ("scout", "score", "global_qa"), ("json", "md")),
    "patent_paper_ip_checker": _agent("patent_paper_ip_checker", "core_research", "Verify patents, papers, benchmarks, proprietary IP signals, and defensive technical assets.", ("scout", "score"), ("json",)),
    "chronology_checker": _agent("chronology_checker", "logic", "Ensure dates, event order, and recency claims are chronologically coherent.", ("update", "verify", "score"), ("json",)),
    "contradiction_checker": _agent("contradiction_checker", "logic", "Detect summary/body contradictions, stale claims, duplicated claims, or internal logic breaks.", ("verify", "global_qa"), ("json", "md")),
    "unsupported_number_guard": _agent("unsupported_number_guard", "logic", "Flag unsupported quantitative claims, highlighted numbers, or metrics missing timing evidence.", ("verify", "score", "global_qa"), ("json",)),
    "citation_integrity_checker": _agent("citation_integrity_checker", "logic", "Check whether claims, quotes, and sources are linked correctly and whether source type is classified correctly.", ("update", "verify", "score", "global_qa"), ("json",)),
    "english_source_priority_guard": _agent("english_source_priority_guard", "logic", "Enforce English-authoritative-source-first rules and downgrade weaker evidence.", ("update", "verify", "scout", "global_qa"), ("json",)),
    "korean_source_avoidance_guard": _agent("korean_source_avoidance_guard", "logic", "Detect Korean-language media dependence in decisive facts and push those claims to unverified or reserve.", ("verify", "scout", "global_qa"), ("json",), decisive_source_rule="Korean-language media cannot be the decisive source for final-candidate inclusion."),
    "ranking_consistency_guard": _agent("ranking_consistency_guard", "logic", "Ensure newly discovered startup ranks are contiguous, deterministic, and reused unchanged across sections.", ("score", "render", "global_qa", "final_check"), ("json",)),
    "timestamp_format_guard": _agent("timestamp_format_guard", "logic", "Ensure every visible page timestamp includes date, weekday, time, and KST.", ("verify", "render", "global_qa", "final_check"), ("json",)),
    "section_order_consistency_guard": _agent("section_order_consistency_guard", "logic", "Check that startup order stays identical across list, eval, partner, insight, monitoring, and anchor structures.", ("verify", "render", "global_qa", "final_check"), ("json",)),
    "html_regression_guard": _agent("html_regression_guard", "logic", "Detect shell regressions, removed controls, broken collapsible structures, or visual structure drift.", ("render", "global_qa", "republish"), ("json", "md")),
    "score_evidence_judge": _agent("score_evidence_judge", "logic", "Assign or audit scores only when evidence exists and explain conservative deductions.", ("score",), ("json", "md"), bias="Unsupported claims must not earn points; software/service/engine companies are preferred over pure hardware for new discovery."),
    "duplicate_startup_guard": _agent("duplicate_startup_guard", "logic", "Detect duplicates within a page or across AI/1 and AI/2.", ("verify", "global_qa"), ("json",)),
    "category_leakage_guard": _agent("category_leakage_guard", "logic", "Block ad-tech leakage into AI/1 and personalization/on-device leakage into AI/2.", ("verify", "scout", "global_qa"), ("json",)),
    "publish_path_guard": _agent("publish_path_guard", "logic", "Verify canonical publish targets remain AI/1/index.html and AI/2/index.html with no .htm drift.", ("verify", "render", "global_qa", "republish", "final_check"), ("json",)),
    "qa_gatekeeper": _agent("qa_gatekeeper", "logic", "Make final pass/fail QA decisions based on blockers, warnings, and publish-gate policy.", ("global_qa", "retry", "republish", "final_check"), ("json", "md")),
    "retry_orchestrator": _agent("retry_orchestrator", "logic", "Classify retryable vs non-retryable failures and propose the minimum safe reruns.", ("retry", "republish", "final_check"), ("json", "md")),
}

PHASE_AGENT_ROLES: dict[str, list[str]] = {
    "ai1_update": [
        "official_primary_source_researcher",
        "official_blog_and_release_reader",
        "english_authoritative_media_researcher",
        "app_store_signal_checker",
        "product_surface_checker",
        "partnership_deal_checker",
        "chronology_checker",
        "citation_integrity_checker",
        "english_source_priority_guard",
        "korean_source_avoidance_guard",
    ],
    "ai1_verify": [
        "regulatory_and_filings_checker",
        "company_registry_checker",
        "valuation_unicorn_guard",
        "geography_exclusion_guard",
        "korea_china_exclusion_guard",
        "privacy_security_compliance_checker",
        "contradiction_checker",
        "unsupported_number_guard",
        "timestamp_format_guard",
        "section_order_consistency_guard",
        "duplicate_startup_guard",
        "category_leakage_guard",
        "publish_path_guard",
    ],
    "ai1_scout": [
        "official_primary_source_researcher",
        "english_authoritative_media_researcher",
        "regulatory_and_filings_checker",
        "company_registry_checker",
        "app_store_signal_checker",
        "product_surface_checker",
        "mobile_first_ux_checker",
        "on_device_architecture_checker",
        "privacy_security_compliance_checker",
        "founder_identity_checker",
        "leadership_background_checker",
        "employee_count_checker",
        "funding_database_checker",
        "investor_lineage_checker",
        "valuation_unicorn_guard",
        "geography_exclusion_guard",
        "korea_china_exclusion_guard",
        "revenue_model_verifier",
        "traction_metric_checker",
        "competitor_mapper",
        "manufacturer_strategy_agent",
        "partnership_deal_checker",
        "mna_scenario_agent",
        "market_size_trend_curator",
        "patent_paper_ip_checker",
        "english_source_priority_guard",
        "korean_source_avoidance_guard",
        "category_leakage_guard",
        "duplicate_startup_guard",
    ],
    "ai1_score": [
        "score_evidence_judge",
        "unsupported_number_guard",
        "ranking_consistency_guard",
        "chronology_checker",
        "citation_integrity_checker",
        "manufacturer_strategy_agent",
        "mna_scenario_agent",
        "revenue_model_verifier",
        "traction_metric_checker",
        "market_size_trend_curator",
    ],
    "ai1_render": [
        "html_regression_guard",
        "timestamp_format_guard",
        "section_order_consistency_guard",
        "ranking_consistency_guard",
        "publish_path_guard",
    ],
    "ai2_update": [
        "official_primary_source_researcher",
        "official_blog_and_release_reader",
        "english_authoritative_media_researcher",
        "app_store_signal_checker",
        "product_surface_checker",
        "partnership_deal_checker",
        "chronology_checker",
        "citation_integrity_checker",
        "english_source_priority_guard",
        "korean_source_avoidance_guard",
    ],
    "ai2_verify": [
        "regulatory_and_filings_checker",
        "company_registry_checker",
        "valuation_unicorn_guard",
        "geography_exclusion_guard",
        "korea_china_exclusion_guard",
        "privacy_security_compliance_checker",
        "contradiction_checker",
        "unsupported_number_guard",
        "timestamp_format_guard",
        "section_order_consistency_guard",
        "duplicate_startup_guard",
        "category_leakage_guard",
        "publish_path_guard",
    ],
    "ai2_scout": [
        "official_primary_source_researcher",
        "english_authoritative_media_researcher",
        "regulatory_and_filings_checker",
        "company_registry_checker",
        "app_store_signal_checker",
        "product_surface_checker",
        "mobile_first_ux_checker",
        "on_device_architecture_checker",
        "privacy_security_compliance_checker",
        "founder_identity_checker",
        "leadership_background_checker",
        "employee_count_checker",
        "funding_database_checker",
        "investor_lineage_checker",
        "valuation_unicorn_guard",
        "geography_exclusion_guard",
        "korea_china_exclusion_guard",
        "revenue_model_verifier",
        "traction_metric_checker",
        "competitor_mapper",
        "manufacturer_strategy_agent",
        "partnership_deal_checker",
        "mna_scenario_agent",
        "market_size_trend_curator",
        "patent_paper_ip_checker",
        "english_source_priority_guard",
        "korean_source_avoidance_guard",
        "category_leakage_guard",
        "duplicate_startup_guard",
    ],
    "ai2_score": [
        "score_evidence_judge",
        "unsupported_number_guard",
        "ranking_consistency_guard",
        "chronology_checker",
        "citation_integrity_checker",
        "manufacturer_strategy_agent",
        "mna_scenario_agent",
        "revenue_model_verifier",
        "traction_metric_checker",
        "market_size_trend_curator",
    ],
    "ai2_render": [
        "html_regression_guard",
        "timestamp_format_guard",
        "section_order_consistency_guard",
        "ranking_consistency_guard",
        "publish_path_guard",
    ],
    "global_qa": [
        "qa_gatekeeper",
        "duplicate_startup_guard",
        "category_leakage_guard",
        "citation_integrity_checker",
        "unsupported_number_guard",
        "timestamp_format_guard",
        "ranking_consistency_guard",
        "section_order_consistency_guard",
        "html_regression_guard",
        "publish_path_guard",
        "english_source_priority_guard",
        "korean_source_avoidance_guard",
        "geography_exclusion_guard",
        "korea_china_exclusion_guard",
        "valuation_unicorn_guard",
    ],
    "retry_failed": ["retry_orchestrator", "qa_gatekeeper"],
    "republish_or_qa": ["qa_gatekeeper", "publish_path_guard", "html_regression_guard", "timestamp_format_guard"],
    "final_retry_or_publish_check": ["qa_gatekeeper", "ranking_consistency_guard", "timestamp_format_guard", "publish_path_guard"],
}


def phase_suffix(phase: str) -> str:
    if phase.endswith("_update"):
        return "update"
    if phase.endswith("_verify"):
        return "verify"
    if phase.endswith("_scout"):
        return "scout"
    if phase.endswith("_score"):
        return "score"
    if phase.endswith("_render"):
        return "render"
    if phase == "global_qa":
        return "global_qa"
    if phase == "retry_failed":
        return "retry"
    if phase == "republish_or_qa":
        return "republish"
    if phase == "final_retry_or_publish_check":
        return "final_check"
    raise KeyError(f"Unknown phase: {phase}")


def state_phase_root(run_date: str, page: str | None, phase: str) -> Path:
    if page:
        return STATE_ROOT / run_date / page / phase
    return STATE_ROOT / run_date / "global" / phase


def phase_matrix(phase: str) -> list[dict[str, str]]:
    run_role_list = PHASE_AGENT_ROLES.get(phase, [])
    return [
        {
            "role": role,
            "agent_file": f".codex/agents/{role}.toml",
            "role_category": AGENT_DEFINITIONS[role].category,
        }
        for role in run_role_list
    ]


def schedule_table() -> list[dict[str, str]]:
    rows = []
    for phase, cron in PHASE_UTC_CRONS.items():
        rows.append(
            {
                "phase": phase,
                "kst_slot": PHASE_KST_SLOTS[phase],
                "utc_cron": cron,
                "prompt_file": PHASE_PROMPTS[phase],
            }
        )
    return rows


def schedule_table_json() -> str:
    return json.dumps(schedule_table(), ensure_ascii=False, indent=2)
