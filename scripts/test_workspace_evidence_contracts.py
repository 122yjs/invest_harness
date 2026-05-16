#!/usr/bin/env python3
"""Validate 00_evidence workspace template contracts."""

from __future__ import annotations

from sync_invest_skills import REPO_ROOT

REQUIRED_TOKENS = {
    "evidence-plan.md": [
        "Raw Request",
        "Question Decomposition",
        "Required Evidence Types",
        "Source Capabilities Needed",
        "Signal Primitives Needed",
        "Validation Gates",
        "Unresolved Ambiguities",
    ],
    "source-call-plan.md": [
        "Evidence Type",
        "Candidate Source",
        "Trust Tier",
        "Reason Selected",
        "Required Parameters",
        "Fallback Sources",
        "Expected Output",
        "Validation Checks",
        "Source Limitations",
    ],
    "evidence-ledger.md": [
        "Evidence ID",
        "Source",
        "Source Type",
        "Trust Tier",
        "Retrieved At",
        "Period",
        "Metric",
        "Value",
        "Unit",
        "Transformation",
        "Used By",
        "Claim Boundary",
        "Caveat",
    ],
    "signal-card.md": [
        "signal id",
        "signal primitive",
        "subject",
        "geography",
        "period",
        "inputs",
        "calculations",
        "output signal",
        "confidence",
        "caveats",
        "downstream analyst usage",
    ],
    "source-validation.md": [
        "Validation Status",
        "Missing Data",
        "Unit/Date Checks",
        "Source Conflicts",
        "Relative vs Absolute Checks",
        "Forbidden Claim Checks",
        "Unresolved Data Gaps",
    ],
    "api-call-log.md": [
        "Source",
        "Endpoint/Tool",
        "Parameters",
        "Timestamp",
        "Success/Failure",
        "Response Summary",
        "Cache Path",
        "Error",
    ],
    "unresolved-data-gaps.md": [
        "Missing Evidence",
        "Affected Claim",
        "Attempted Sources",
        "Impact",
        "Next Step",
    ],
}


def main() -> int:
    failures: list[str] = []
    for filename, tokens in REQUIRED_TOKENS.items():
        path = REPO_ROOT / "docs/harness/invest/templates" / filename
        text = path.read_text(encoding="utf-8").lower()
        for token in tokens:
            if token.lower() not in text:
                failures.append(f"{filename} missing token: {token}")

    if failures:
        print("Workspace evidence contract check failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Workspace evidence contract check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
