#!/usr/bin/env python3
"""Validate evidence trust priority and QoQ financial comparison contracts."""

from __future__ import annotations

from sync_invest_skills import REPO_ROOT


REQUIRED_TOKENS: dict[str, list[str]] = {
    "docs/harness/invest/data-source-policy.md": [
        "Evidence Trust Order",
        "T0 | Company official and regulator disclosure",
        "Company IR, earnings releases, shareholder letters, SEC EDGAR, DART/KRX",
        "never overrides T0 for reported company facts",
    ],
    "plugins/vertical-plugins/invest-research/policies/data-source-policy.md": [
        "Evidence Trust Order",
        "T0 | Company official and regulator disclosure",
        "Company IR, earnings releases, shareholder letters, SEC EDGAR, DART/KRX",
        "never overrides T0 for reported company facts",
    ],
    "docs/harness/invest/mcp-routing.md": [
        "Evidence Trust Routing",
        "T0 company official and regulator disclosure",
        "cannot promote T2 or T3 above\nT0",
    ],
    "docs/harness/invest/research-layer/source-capability-registry.md": [
        "Evidence Trust Tier Semantics",
        "T0: company official and regulator disclosure",
        "T0 evidence has priority over T2/T3",
        "Trust tier T0 for US issuer filings",
        "Trust tier T2",
    ],
    "docs/harness/invest/templates/source-call-plan.md": [
        "Trust Tier",
        "T0 / T1 / T2 / T3",
        "Use T0 company official and\nregulator disclosure before T2 vendor snapshots",
    ],
    "docs/harness/invest/templates/evidence-ledger.md": [
        "Trust Tier",
        "Use T0 for Company IR, SEC EDGAR, DART/KRX",
        "must not override T0 reported company facts",
    ],
    "docs/harness/invest/templates/quarterly-sentiment-deep-dive.md": [
        "매출 YoY",
        "매출 QoQ",
        "EPS YoY",
        "EPS QoQ",
        "FCF YoY",
        "FCF QoQ",
    ],
    "plugins/vertical-plugins/invest-research/skills/source-router/SKILL.md": [
        "Rank selected sources by evidence trust tier",
        "T0 company official/regulator disclosure",
        "Runtime availability can force a fallback, but it cannot promote T2/T3",
    ],
    "plugins/vertical-plugins/invest-research/skills/invest-orchestrator/SKILL.md": [
        "evidence trust tier",
        "T0 evidence",
        "T2 vendor snapshot",
    ],
    "plugins/vertical-plugins/invest-research/skills/financial-analyst/SKILL.md": [
        "T0 / 1순위",
        "재무제표와 reported financial fact는 T0 evidence가 우선",
        "YoY와 QoQ를 함께 비교",
        "최근 분기 재무 비교",
        "매출 QoQ",
        "EPS QoQ",
        "FCF QoQ",
    ],
    "plugins/vertical-plugins/invest-research/skills/valuation-analyst/SKILL.md": [
        "YoY/QoQ 성장",
        "최근 분기 매출 QoQ",
        "최근 분기 EPS QoQ",
        "T0 evidence",
    ],
    "plugins/vertical-plugins/invest-research/skills/report-synthesizer/SKILL.md": [
        "YoY 및 QoQ 비교",
        "T0 evidence",
        "peer financial comparison",
    ],
    "plugins/vertical-plugins/invest-research/skills/qa-reviewer/SKILL.md": [
        "YoY와 QoQ가 모두 있는지 확인",
        "T0 evidence",
        "T2 vendor snapshot",
    ],
    "docs/harness/invest/runbook.md": [
        "evidence trust tier",
        "T0 evidence",
        "YoY와 QoQ를 함께 제공",
    ],
    "docs/harness/invest/team-spec.md": [
        "Evidence 신뢰도",
        "재무 비교",
        "YoY와 QoQ",
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
        print("Evidence priority and QoQ contract check failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Evidence priority and QoQ contract check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
