#!/usr/bin/env python3
"""Validate required invest-harness structure and generated skill frontmatter."""

from __future__ import annotations

import re
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
    ("plugins/vertical-plugins/invest-research", "vertical source plugin"),
    ("plugins/agent-plugins/invest-harness", "agent plugin generated layer"),
    (".agents/skills", "generated agent skills"),
    (".agents/commands", "generated agent commands"),
    (".agents/policies", "generated agent policies"),
    ("scripts/Sync-InvestSkills.ps1", "PowerShell sync script"),
    ("scripts/Test-SkillDrift.ps1", "PowerShell drift script"),
    ("scripts/Test-WorkspaceSafety.ps1", "PowerShell workspace safety script"),
    ("scripts/Test-HarnessStructure.ps1", "PowerShell structure script"),
    ("scripts/sync_invest_skills.py", "Python sync script"),
    ("scripts/test_skill_drift.py", "Python drift script"),
    ("scripts/test_workspace_safety.py", "Python workspace safety script"),
    ("scripts/test_harness_structure.py", "Python structure script"),
    ("scripts/verify_invest_harness.py", "Python aggregate verifier"),
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
]

REQUIRED_COMMANDS = ["analyze", "screen", "comps", "dcf", "earnings", "qa"]

REQUIRED_POLICIES = [
    "workspace-safety.md",
    "market-price-anchor.md",
    "data-source-policy.md",
    "qa-recalculation-policy.md",
    "rating-price-target-policy.md",
]

HANDOFF_PATHS = [
    "${ACTIVE_WORKSPACE}/00_input/input-intake.md",
    "${ACTIVE_WORKSPACE}/00_input/request-summary.md",
    "${ACTIVE_WORKSPACE}/01_financial/findings.md",
    "${ACTIVE_WORKSPACE}/02_fundamental/findings.md",
    "${ACTIVE_WORKSPACE}/03_valuation/findings.md",
    "${ACTIVE_WORKSPACE}/04_technical/findings.md",
    "${ACTIVE_WORKSPACE}/05_macro_sentiment/findings.md",
    "${ACTIVE_WORKSPACE}/06_risk_scenario/findings.md",
    "${ACTIVE_WORKSPACE}/06_risk_scenario/conflicts.md",
    "${ACTIVE_WORKSPACE}/07_draft/report.md",
    "${ACTIVE_WORKSPACE}/08_final/report.md",
    "${ACTIVE_WORKSPACE}/08_final/executive-summary.md",
    "${ACTIVE_WORKSPACE}/09_qa/review.md",
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

