#!/usr/bin/env python3
"""Validate required invest-harness structure and generated skill frontmatter."""

from __future__ import annotations

import re
import json
from pathlib import Path

from sync_invest_skills import REPO_ROOT, repo_relative

REQUIRED_PATHS = [
    ("AGENTS.md", "repository guidance"),
    ("README.md", "user README"),
    ("OPENCLAW.md", "OpenClaw entrypoint"),
    ("HERMES.md", "Hermes entrypoint"),
    ("CLAUDE.md", "Claude entrypoint"),
    ("GEMINI.md", "Gemini entrypoint"),
    ("invest_prompt_v2.md", "core invest prompt"),
    ("docs/harness/invest/team-spec.md", "team spec"),
    ("docs/harness/invest/runbook.md", "runbook"),
    ("docs/harness/invest/cross-tool-usage.md", "cross-tool usage"),
    ("docs/harness/invest/data-source-policy.md", "data source policy docs"),
    ("docs/harness/invest/mcp-routing.md", "MCP routing docs"),
    ("docs/harness/invest/research-layer/overview.md", "evidence layer overview"),
    ("docs/harness/invest/research-layer/question-decomposition.md", "question decomposition contract"),
    ("docs/harness/invest/research-layer/source-capability-registry.md", "source capability registry"),
    ("docs/harness/invest/research-layer/signal-primitives.md", "signal primitives contract"),
    ("docs/harness/invest/research-layer/validation-gates.md", "validation gates contract"),
    ("docs/harness/invest/research-layer/claim-boundary-policy.md", "claim boundary policy"),
    ("docs/harness/invest/research-layer/ontology.md", "ontology mapping contract"),
    ("docs/harness/invest/templates/input-intake.md", "input intake template"),
    ("docs/harness/invest/templates/request-summary.md", "request summary template"),
    ("docs/harness/invest/templates/findings-common.md", "findings template"),
    ("docs/harness/invest/templates/conflicts.md", "conflicts template"),
    ("docs/harness/invest/templates/report.md", "report template"),
    ("docs/harness/invest/templates/qa-review.md", "QA template"),
    (
        "docs/harness/invest/templates/quarterly-sentiment-deep-dive.md",
        "quarterly sentiment template",
    ),
    ("docs/harness/invest/templates/market-price-snapshot.md", "market price snapshot template"),
    ("docs/harness/invest/templates/screen-criteria.md", "screen criteria template"),
    ("docs/harness/invest/templates/candidate-universe.md", "candidate universe template"),
    ("docs/harness/invest/templates/idea-scorecard.md", "idea scorecard template"),
    ("docs/harness/invest/templates/shortlist.md", "shortlist template"),
    ("docs/harness/invest/templates/comps.md", "comps template"),
    ("docs/harness/invest/templates/dcf.md", "DCF template"),
    ("docs/harness/invest/templates/earnings-update.md", "earnings update template"),
    ("docs/harness/invest/templates/earnings-preview.md", "earnings preview template"),
    ("docs/harness/invest/templates/sector.md", "sector report template"),
    ("docs/harness/invest/templates/thesis-update.md", "thesis update template"),
    ("docs/harness/invest/templates/catalysts.md", "catalyst calendar template"),
    ("docs/harness/invest/templates/html-report.md", "HTML report template"),
    ("docs/harness/invest/templates/morning-note.md", "morning note template"),
    ("docs/harness/invest/templates/update-plan.md", "report update plan template"),
    ("docs/harness/invest/templates/qa-fix-list.md", "QA fix list template"),
    ("docs/harness/invest/templates/qa-final-check.md", "QA final check template"),
    ("docs/harness/invest/templates/evidence-plan.md", "evidence plan template"),
    ("docs/harness/invest/templates/source-call-plan.md", "source call plan template"),
    ("docs/harness/invest/templates/evidence-ledger.md", "evidence ledger template"),
    ("docs/harness/invest/templates/signal-card.md", "signal card template"),
    ("docs/harness/invest/templates/source-validation.md", "source validation template"),
    ("docs/harness/invest/templates/api-call-log.md", "API call log template"),
    ("docs/harness/invest/templates/unresolved-data-gaps.md", "unresolved data gaps template"),
    ("plugins/vertical-plugins/invest-research", "vertical source plugin"),
    ("plugins/agent-plugins/invest-harness", "agent plugin generated layer"),
    (".agents/skills", "generated agent skills"),
    (".agents/commands", "generated agent commands"),
    (".agents/policies", "generated agent policies"),
    ("scripts/Sync-InvestSkills.ps1", "PowerShell sync script"),
    ("scripts/Set-Credentials.ps1", "PowerShell credential registration script"),
    ("scripts/env/Import-HarnessEnv.ps1", "PowerShell .env loader"),
    ("scripts/mcp/Start-McpServer.ps1", "PowerShell MCP wrapper core"),
    ("scripts/mcp/Start-KoreaStockMcp.ps1", "PowerShell korea-stock MCP wrapper"),
    ("scripts/mcp/Start-YFinanceMcp.ps1", "PowerShell yfinance MCP wrapper"),
    ("scripts/Test-SkillDrift.ps1", "PowerShell drift script"),
    ("scripts/Test-WorkspaceSafety.ps1", "PowerShell workspace safety script"),
    ("scripts/Test-HarnessStructure.ps1", "PowerShell structure script"),
    ("scripts/Test-CommandRuntime.ps1", "PowerShell command runtime smoke script"),
    ("scripts/sync_invest_skills.py", "Python sync script"),
    ("scripts/test_skill_drift.py", "Python drift script"),
    ("scripts/test_workspace_safety.py", "Python workspace safety script"),
    ("scripts/test_harness_structure.py", "Python structure script"),
    ("scripts/invest_command_runtime.py", "Python command runtime parser"),
    ("scripts/test_command_runtime.py", "Python command runtime smoke tests"),
    ("scripts/test_portable_env_mcp.py", "Python portable env and MCP wrapper tests"),
    ("scripts/verify_invest_harness.py", "Python aggregate verifier"),
    (".mcp.institutional.json", "optional institutional MCP catalog"),
]

REQUIRED_SKILLS = [
    "invest-orchestrator",
    "financial-analyst",
    "fundamental-analyst",
    "valuation-analyst",
    "technical-analyst",
    "macro-sentiment-analyst",
    "risk-scenario-analyst",
    "report-synthesizer",
    "qa-reviewer",
    "idea-screener",
    "earnings-update",
    "earnings-preview",
    "sector-analyst",
    "thesis-tracker",
    "catalyst-tracker",
    "html-report-synthesizer",
    "morning-note",
    "report-updater",
    "evidence-planner",
    "source-router",
    "signal-analyst",
]

REQUIRED_COMMANDS = [
    "analyze",
    "screen",
    "comps",
    "dcf",
    "earnings",
    "qa",
    "preview",
    "sector",
    "thesis",
    "catalysts",
    "report-html",
    "morning-note",
    "update",
    "evidence",
    "market-intel",
    "source-audit",
]

REQUIRED_POLICIES = [
    "workspace-safety.md",
    "market-price-anchor.md",
    "data-source-policy.md",
    "qa-recalculation-policy.md",
    "rating-price-target-policy.md",
    "report-writing-style-policy.md",
]

HANDOFF_PATHS = [
    "${ACTIVE_WORKSPACE}/00_input/input-intake.md",
    "${ACTIVE_WORKSPACE}/00_input/request-summary.md",
    "${ACTIVE_WORKSPACE}/00_input/market-price-snapshot.md",
    "${ACTIVE_WORKSPACE}/00_input/earnings-update.md",
    "${ACTIVE_WORKSPACE}/00_input/earnings-preview.md",
    "${ACTIVE_WORKSPACE}/00_input/update-plan.md",
    "${ACTIVE_WORKSPACE}/00_evidence/question-decomposition.md",
    "${ACTIVE_WORKSPACE}/00_evidence/evidence-plan.md",
    "${ACTIVE_WORKSPACE}/00_evidence/source-call-plan.md",
    "${ACTIVE_WORKSPACE}/00_evidence/evidence-ledger.md",
    "${ACTIVE_WORKSPACE}/00_evidence/signal-cards.md",
    "${ACTIVE_WORKSPACE}/00_evidence/source-validation.md",
    "${ACTIVE_WORKSPACE}/00_evidence/api-call-log.md",
    "${ACTIVE_WORKSPACE}/00_evidence/unresolved-data-gaps.md",
    "${ACTIVE_WORKSPACE}/00_screen/screen-criteria.md",
    "${ACTIVE_WORKSPACE}/00_screen/candidate-universe.md",
    "${ACTIVE_WORKSPACE}/00_screen/idea-scorecard.md",
    "${ACTIVE_WORKSPACE}/00_screen/shortlist.md",
    "${ACTIVE_WORKSPACE}/01_financial/findings.md",
    "${ACTIVE_WORKSPACE}/02_fundamental/findings.md",
    "${ACTIVE_WORKSPACE}/03_valuation/findings.md",
    "${ACTIVE_WORKSPACE}/03_valuation/comps.md",
    "${ACTIVE_WORKSPACE}/03_valuation/dcf.md",
    "${ACTIVE_WORKSPACE}/04_technical/findings.md",
    "${ACTIVE_WORKSPACE}/05_macro_sentiment/findings.md",
    "${ACTIVE_WORKSPACE}/05_macro_sentiment/thesis-update.md",
    "${ACTIVE_WORKSPACE}/05_macro_sentiment/catalysts.md",
    "${ACTIVE_WORKSPACE}/05_macro_sentiment/morning-note.md",
    "${ACTIVE_WORKSPACE}/06_risk_scenario/findings.md",
    "${ACTIVE_WORKSPACE}/06_risk_scenario/conflicts.md",
    "${ACTIVE_WORKSPACE}/07_draft/report.md",
    "${ACTIVE_WORKSPACE}/08_final/report.md",
    "${ACTIVE_WORKSPACE}/08_final/report.html",
    "${ACTIVE_WORKSPACE}/08_final/executive-summary.md",
    "${ACTIVE_WORKSPACE}/09_qa/review.md",
    "${ACTIVE_WORKSPACE}/09_qa/fix-list.md",
    "${ACTIVE_WORKSPACE}/09_qa/final-check.md",
]


def has_frontmatter(content: str) -> bool:
    normalized = content.replace("\r\n", "\n")
    if not normalized.startswith("---\n"):
        return False
    end = normalized.find("\n---\n", 4)
    if end == -1:
        return False
    frontmatter = normalized[:end]
    return bool(re.search(r"(?m)^name:\s*\S+", frontmatter)) and bool(
        re.search(r"(?m)^description:\s*\S+", frontmatter)
    )


def collect_failures() -> list[str]:
    failures: list[str] = []

    for relative_path, description in REQUIRED_PATHS:
        path = REPO_ROOT / relative_path
        if not path.exists():
            failures.append(f"missing: {description} ({relative_path})")

    for skill_name in REQUIRED_SKILLS:
        for layer in [
            REPO_ROOT / "plugins/vertical-plugins/invest-research/skills",
            REPO_ROOT / "plugins/agent-plugins/invest-harness/skills",
            REPO_ROOT / ".agents/skills",
        ]:
            skill_file = layer / skill_name / "SKILL.md"
            if not skill_file.is_file():
                failures.append(f"missing skill: {repo_relative(skill_file)}")
            elif not has_frontmatter(skill_file.read_text(encoding="utf-8")):
                failures.append(f"invalid skill frontmatter: {repo_relative(skill_file)}")

    for command_name in REQUIRED_COMMANDS:
        for layer in [
            REPO_ROOT / "plugins/vertical-plugins/invest-research/commands",
            REPO_ROOT / "plugins/agent-plugins/invest-harness/commands",
            REPO_ROOT / ".agents/commands",
        ]:
            command_file = layer / f"{command_name}.md"
            if not command_file.is_file():
                failures.append(f"missing command stub: {repo_relative(command_file)}")

    for policy_name in REQUIRED_POLICIES:
        for layer in [
            REPO_ROOT / "plugins/vertical-plugins/invest-research/policies",
            REPO_ROOT / "plugins/agent-plugins/invest-harness/policies",
            REPO_ROOT / ".agents/policies",
        ]:
            policy_file = layer / policy_name
            if not policy_file.is_file():
                failures.append(f"missing policy: {repo_relative(policy_file)}")

    team_spec = (REPO_ROOT / "docs/harness/invest/team-spec.md").read_text(encoding="utf-8")
    orchestrator = (REPO_ROOT / ".agents/skills/invest-orchestrator/SKILL.md").read_text(
        encoding="utf-8"
    )
    for handoff_path in HANDOFF_PATHS:
        if handoff_path not in team_spec:
            failures.append(f"team-spec handoff path missing: {handoff_path}")
        if handoff_path not in orchestrator:
            failures.append(f"orchestrator handoff path missing: {handoff_path}")

    institutional_mcp_path = REPO_ROOT / ".mcp.institutional.json"
    if institutional_mcp_path.is_file():
        institutional_config = json.loads(institutional_mcp_path.read_text(encoding="utf-8"))
        if institutional_config.get("enabled") is not False:
            failures.append(".mcp.institutional.json must be disabled by default")
        if institutional_config.get("mcpServers") not in ({}, None):
            failures.append(".mcp.institutional.json must not enable paid MCP servers by default")

    return failures


def main() -> int:
    failures = collect_failures()
    if failures:
        print("Harness structure check failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(
        "Harness structure check passed: required paths, generated layers, "
        "frontmatter, and handoff contracts are valid."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
