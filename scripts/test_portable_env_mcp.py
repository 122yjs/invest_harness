#!/usr/bin/env python3
"""Validate portable credential and MCP wrapper scripts."""

from __future__ import annotations

import re
from pathlib import Path

from sync_invest_skills import REPO_ROOT


SCRIPT_PATHS = [
    REPO_ROOT / "scripts" / "Set-Credentials.ps1",
    REPO_ROOT / "scripts" / "env" / "Import-HarnessEnv.ps1",
    REPO_ROOT / "scripts" / "mcp" / "Start-McpServer.ps1",
    REPO_ROOT / "scripts" / "mcp" / "Start-KoreaStockMcp.ps1",
    REPO_ROOT / "scripts" / "mcp" / "Start-YFinanceMcp.ps1",
]

SECRET_LIKE_PATTERN = re.compile(
    r"(?i)(DART_API_KEY|KRX_API_KEY|FRED_API_KEY|ALPHA_VANTAGE_API_KEY|FMP_API_KEY|"
    r"KOSIS_API_KEY|CUSTOMS_TRADE_API_KEY)\"?\s*=\s*\"?[A-Za-z0-9+/=_-]{12,}"
)


def test_portable_env_and_mcp_scripts_exist() -> None:
    missing = [str(path.relative_to(REPO_ROOT)) for path in SCRIPT_PATHS if not path.is_file()]
    assert missing == []


def test_credential_script_does_not_embed_secret_values() -> None:
    for path in SCRIPT_PATHS:
        content = path.read_text(encoding="utf-8")
        assert SECRET_LIKE_PATTERN.search(content) is None, path.relative_to(REPO_ROOT)


def test_mcp_wrappers_use_environment_overrides() -> None:
    korea = (REPO_ROOT / "scripts" / "mcp" / "Start-KoreaStockMcp.ps1").read_text(
        encoding="utf-8"
    )
    yfinance = (REPO_ROOT / "scripts" / "mcp" / "Start-YFinanceMcp.ps1").read_text(
        encoding="utf-8"
    )

    assert "INVEST_HARNESS_KOREA_STOCK_MCP_COMMAND" in korea
    assert "INVEST_HARNESS_YFINANCE_MCP_COMMAND" in yfinance
    assert "DART_API_KEY" in korea
    assert "KRX_API_KEY" in korea
