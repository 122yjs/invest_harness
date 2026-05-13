#!/usr/bin/env python3
"""Validate source capability registry contracts."""

from __future__ import annotations

from sync_invest_skills import REPO_ROOT

SOURCES = [
    "opendart / DART-KRX",
    "yfinance",
    "kosis",
    "customs_trade_api",
    "google_trends",
    "naver_datalab",
    "kotra",
    "g2b_procurement",
    "ecos or macro official statistics",
    "FRED",
    "Alpha Vantage",
    "Financial Modeling Prep",
    "EDGAR",
]

FIELDS = [
    "provides",
    "good_for",
    "not_good_for",
    "required_inputs",
    "outputs",
    "validation_rules",
    "forbidden_claims",
]


def main() -> int:
    path = REPO_ROOT / "docs/harness/invest/research-layer/source-capability-registry.md"
    text = path.read_text(encoding="utf-8")
    lower = text.lower()
    failures: list[str] = []

    for source in SOURCES:
        if f"## {source}".lower() not in lower:
            failures.append(f"missing source section: {source}")

    for field in FIELDS:
        if field not in lower:
            failures.append(f"missing contract field: {field}")

    if failures:
        print("Source capability registry check failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Source capability registry check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
