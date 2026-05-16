#!/usr/bin/env python3
"""Validate BKNG research operational reliability guardrails."""

from __future__ import annotations

from pathlib import Path

from sync_invest_skills import REPO_ROOT


REQUIRED_TOKENS: dict[str, list[str]] = {
    "docs/harness/invest/planning/05_plan_bkng_research_operational_reliability.md": [
        "BKNG",
        "yfinance runtime",
        "Resource deadlock avoided",
        "`financial-analyst`",
        "`risk-scenario-analyst`",
        "`report-synthesizer`",
        "`max_concurrent_children=3`",
        "Template Fallback",
        "evidence-ledger",
    ],
    "docs/harness/invest/runbook.md": [
        "운영 preflight와 fallback",
        "Runtime Availability",
        "Live Tool Probe",
        "inline fallback template",
        "max_concurrent_children",
        "compact handoff summary",
    ],
    "docs/harness/invest/team-spec.md": [
        "runtime source availability",
        "Runtime Availability",
        "template fallback",
        "서브에이전트 타임아웃",
        "compact handoff summary",
    ],
    "docs/harness/invest/mcp-routing.md": [
        "live runtime proof",
        "Runtime Availability",
        "Live Tool Probe",
        "If yfinance is absent",
        "FMP/Alpha Vantage",
    ],
    "docs/harness/invest/data-source-policy.md": [
        "live callable source inventory",
        "Runtime\nAvailability",
        "If yfinance is absent",
        "FMP or Alpha Vantage",
    ],
    "plugins/vertical-plugins/invest-research/policies/data-source-policy.md": [
        "live callable source inventory",
        "Runtime\nAvailability",
        "If yfinance is absent",
        "FMP or Alpha Vantage",
    ],
    "docs/harness/invest/research-layer/source-capability-registry.md": [
        "live runtime check",
        "Runtime Availability",
        "Live Tool Probe",
        "mark the source unavailable",
        "FMP or Alpha Vantage only when live callable",
    ],
    "docs/harness/invest/templates/source-call-plan.md": [
        "Runtime Availability",
        "Live Tool Probe",
        "available / unavailable / not checked",
        "Connection Status` is repo-evidence status, not live runtime proof",
    ],
    "plugins/vertical-plugins/invest-research/templates/source-call-plan.md": [
        "Runtime Availability",
        "Live Tool Probe",
        "available / unavailable / not checked",
        "Connection Status` is repo-evidence status, not live runtime proof",
    ],
    "plugins/vertical-plugins/invest-research/skills/source-router/SKILL.md": [
        "Runtime Availability",
        "Live Tool Probe",
        "yfinance",
        "FMP/Alpha Vantage",
        "live runtime",
    ],
    "plugins/vertical-plugins/invest-research/skills/invest-orchestrator/SKILL.md": [
        "운영 preflight",
        "Resource deadlock avoided",
        "Runtime Availability",
        "Live Tool Probe",
        "max_concurrent_children",
        "compact handoff summary",
    ],
    "plugins/vertical-plugins/invest-research/skills/financial-analyst/SKILL.md": [
        "Runtime Availability",
        "FMP/Alpha Vantage",
        "대형 웹 페이지를 무제한으로 탐색하지 않는다",
        "BKNG처럼",
    ],
    "plugins/vertical-plugins/invest-research/skills/report-synthesizer/SKILL.md": [
        "compact handoff summary",
        "conflicts table",
        "live runtime unavailable",
    ],
    "AGENTS.md": [
        "live runtime proof",
        "callable source inventory",
        "T0 fallback",
        "FMP/Alpha Vantage/Web Search + Fetch",
    ],
    "README.md": [
        "live runtime",
        "Runtime Availability=unavailable",
        "company IR, SEC EDGAR, DART/KRX 또는 local regulator filing",
        "FMP/Alpha Vantage/Web Search + Fetch",
    ],
}


def main() -> int:
    failures: list[str] = []

    for relative_path, tokens in REQUIRED_TOKENS.items():
        path = REPO_ROOT / relative_path
        if not path.is_file():
            failures.append(f"missing file: {relative_path}")
            continue

        text = path.read_text(encoding="utf-8")
        for token in tokens:
            if token not in text:
                failures.append(f"{relative_path}: missing token: {token!r}")

    if failures:
        print("BKNG operational guardrail check failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("BKNG operational guardrail check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
