#!/usr/bin/env python3
"""Validate generic signal primitive contracts."""

from __future__ import annotations

from sync_invest_skills import REPO_ROOT

PRIMITIVES = [
    "search_interest_momentum",
    "export_momentum",
    "transaction_market_size",
    "procurement_demand",
    "disclosure_exposure",
    "market_context_signal",
    "regulatory_risk_signal",
    "valuation_anchor",
    "macro_regime_signal",
    "news_event_signal",
]

FIELDS = [
    "purpose",
    "required_inputs",
    "compatible_sources",
    "common_metrics",
    "output fields",
    "caveats",
    "claim boundaries",
]


def main() -> int:
    path = REPO_ROOT / "docs/harness/invest/research-layer/signal-primitives.md"
    text = path.read_text(encoding="utf-8")
    lower = text.lower()

    failures = [primitive for primitive in PRIMITIVES if primitive not in text]
    failures.extend(field for field in FIELDS if field not in lower)

    if failures:
        print("Signal primitive check failed:")
        for failure in failures:
            print(f"- missing: {failure}")
        return 1

    print("Signal primitive check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
