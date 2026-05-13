#!/usr/bin/env python3
"""Validate claim-boundary prohibitions."""

from __future__ import annotations

from sync_invest_skills import REPO_ROOT

REQUIRED = [
    "Google Trends is not market size",
    "Search interest is not sales",
    "Customs trade is not company revenue",
    "KOTRA text is not export volume",
]


def main() -> int:
    path = REPO_ROOT / "docs/harness/invest/research-layer/claim-boundary-policy.md"
    text = path.read_text(encoding="utf-8")
    failures = [phrase for phrase in REQUIRED if phrase not in text]
    if failures:
        print("Claim boundary policy check failed:")
        for failure in failures:
            print(f"- missing: {failure}")
        return 1

    print("Claim boundary policy check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
