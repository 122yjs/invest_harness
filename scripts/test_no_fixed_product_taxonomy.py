#!/usr/bin/env python3
"""Ensure core evidence routing does not define fixed product/use-case enums."""

from __future__ import annotations

from pathlib import Path

from sync_invest_skills import REPO_ROOT

FORBIDDEN_CORE_TERMS = [
    "cosmetics",
    "pet_supplies",
    "semiconductors",
    "power_equipment",
    "defense",
    "k_food",
]

CORE_PATHS = [
    REPO_ROOT / "docs/harness/invest/research-layer",
    REPO_ROOT / "plugins/vertical-plugins/invest-research/skills/evidence-planner",
    REPO_ROOT / "plugins/vertical-plugins/invest-research/skills/source-router",
    REPO_ROOT / "plugins/vertical-plugins/invest-research/skills/signal-analyst",
]


def main() -> int:
    failures: list[str] = []
    for root in CORE_PATHS:
        for path in root.rglob("*.md"):
            text = path.read_text(encoding="utf-8").lower()
            for term in FORBIDDEN_CORE_TERMS:
                if term in text:
                    failures.append(f"{path.relative_to(REPO_ROOT)} contains forbidden core term {term}")

    qd = (REPO_ROOT / "docs/harness/invest/research-layer/question-decomposition.md").read_text(
        encoding="utf-8"
    )
    for token in [
        "no_fixed_product_taxonomy: true",
        "no_use_case_hard_routing: true",
        "allow_unseen_market_objects: true",
        "source_selection_based_on_evidence_need: true",
    ]:
        if token not in qd:
            failures.append(f"question-decomposition missing policy token: {token}")

    if failures:
        print("No fixed product taxonomy check failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("No fixed product taxonomy check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
