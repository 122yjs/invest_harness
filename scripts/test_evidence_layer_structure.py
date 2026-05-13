#!/usr/bin/env python3
"""Validate evidence-layer docs, templates, and eval fixture placement."""

from __future__ import annotations

from pathlib import Path

from sync_invest_skills import REPO_ROOT

RESEARCH_DOCS = [
    "overview.md",
    "question-decomposition.md",
    "source-capability-registry.md",
    "signal-primitives.md",
    "validation-gates.md",
    "claim-boundary-policy.md",
    "ontology.md",
]

TEMPLATES = [
    "evidence-plan.md",
    "source-call-plan.md",
    "evidence-ledger.md",
    "signal-card.md",
    "source-validation.md",
    "api-call-log.md",
    "unresolved-data-gaps.md",
]

GOLDEN = [
    "pet-ecommerce-trend.md",
    "cosmetics-sea-export.md",
    "unseen-market-object.md",
    "google-trends-claim-boundary.md",
]


def assert_file(relative: str) -> None:
    path = REPO_ROOT / relative
    if not path.is_file():
        raise AssertionError(f"missing required evidence-layer file: {relative}")


def main() -> int:
    for name in RESEARCH_DOCS:
        assert_file(f"docs/harness/invest/research-layer/{name}")
    for name in TEMPLATES:
        assert_file(f"docs/harness/invest/templates/{name}")
    for name in GOLDEN:
        assert_file(f"docs/harness/invest/evals/golden-scenarios/{name}")

    overview = (REPO_ROOT / "docs/harness/invest/research-layer/overview.md").read_text(
        encoding="utf-8"
    )
    for token in [
        "Question Decomposition",
        "Evidence Planner",
        "Source Capability Router",
        "Evidence Ledger",
        "Signal Primitives",
        "Validation Gate",
        "Existing Analyst Fan-out",
    ]:
        if token not in overview:
            raise AssertionError(f"overview missing pipeline token: {token}")

    print("Evidence layer structure check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
