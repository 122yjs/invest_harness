#!/usr/bin/env python3
"""Validate source capability registry contracts."""

from __future__ import annotations

import json
import re

from sync_invest_skills import REPO_ROOT

EXPECTED_SOURCES = [
    "DART-KRX / korea-stock",
    "yfinance",
    "FRED",
    "SEC EDGAR",
    "Alpha Vantage",
    "KOSIS",
    "Korea Customs Service / customs_trade_api",
    "Google Trends",
    "Naver DataLab",
    "KOTRA",
    "G2B / public procurement",
    "Financial Modeling Prep",
    "ECOS or macro official statistics",
]

REQUIRED_FIELDS = [
    "source_id",
    "provider",
    "connection_status",
    "configured_in",
    "available_tools_or_endpoints",
    "evidence_types_supported",
    "good_for",
    "not_good_for",
    "required_inputs",
    "outputs",
    "validation_rules",
    "forbidden_claims",
    "fallback_sources",
    "notes",
]

ALLOWED_STATUSES = {"connected", "documented_only", "planned", "external_manual"}

BANNED_DUPLICATE_CONNECTOR_PHRASES = [
    "connect FRED",
    "connect SEC EDGAR",
    "connect Alpha Vantage",
    "connect yfinance",
    "connect DART-KRX",
    "connect korea-stock",
    "reconnect FRED",
    "reconnect SEC EDGAR",
    "reconnect Alpha Vantage",
    "reconnect yfinance",
    "reconnect DART-KRX",
    "reconnect korea-stock",
    "implement a new FRED client",
    "implement a new EDGAR client",
    "implement a new Alpha Vantage client",
    "duplicate existing API/MCP integration",
]

NON_SOURCE_SECTIONS = {"Contract Fields", "Connection Status Semantics"}


def parse_source_sections(text: str) -> dict[str, str]:
    """Return level-2 Markdown sections that represent source contracts."""
    matches = list(re.finditer(r"^## (.+)$", text, flags=re.MULTILINE))
    sections: dict[str, str] = {}

    for index, match in enumerate(matches):
        title = match.group(1).strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        if title not in NON_SOURCE_SECTIONS:
            sections[title] = text[start:end]

    return sections


def find_connection_status(section: str) -> str | None:
    match = re.search(r"^- connection_status:\s*`?([a-z_]+)`?\s*$", section, re.MULTILINE)
    return match.group(1) if match else None


def main() -> int:
    path = REPO_ROOT / "docs/harness/invest/research-layer/source-capability-registry.md"
    text = path.read_text(encoding="utf-8")
    sections = parse_source_sections(text)
    failures: list[str] = []

    for source in EXPECTED_SOURCES:
        if source not in sections:
            failures.append(f"missing source section: {source}")

    for source, section in sections.items():
        for field in REQUIRED_FIELDS:
            if not re.search(rf"^- {re.escape(field)}:", section, re.MULTILINE):
                failures.append(f"{source}: missing contract field: {field}")

        status = find_connection_status(section)
        if status is None:
            failures.append(f"{source}: missing connection_status enum")
        elif status not in ALLOWED_STATUSES:
            failures.append(f"{source}: invalid connection_status: {status}")

    required_status_note = "repo-evidence only, not live runtime proof"
    if required_status_note not in text:
        failures.append(f"missing status semantics note: {required_status_note!r}")

    lowered_text = text.lower()
    for phrase in BANNED_DUPLICATE_CONNECTOR_PHRASES:
        if phrase.lower() in lowered_text:
            failures.append(f"banned duplicate connector wording present: {phrase}")

    institutional_path = REPO_ROOT / ".mcp.institutional.json"
    institutional = json.loads(institutional_path.read_text(encoding="utf-8"))
    if institutional.get("enabled") is not False:
        failures.append(".mcp.institutional.json must remain disabled for this pass")
    if institutional.get("mcpServers") != {}:
        failures.append(".mcp.institutional.json mcpServers must remain empty for this pass")

    if failures:
        print("Source capability registry check failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Source capability registry check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
