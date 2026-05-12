# Data Source Policy

This document mirrors the source policy at `plugins/vertical-plugins/invest-research/policies/data-source-policy.md` for human-facing documentation. The source policy remains the generated-layer source of truth.

## Default Source Order

| Market | Primary | Secondary | Fallback |
|---|---|---|---|
| Korea | DART / KRX through `korea-stock` when available | yfinance market-data cross-checks | Company IR, exchange pages, web search for source discovery |
| US | SEC EDGAR and company IR | yfinance market data, financial snapshots, news | Exchange pages, official press releases, web search for missing context |
| Global | yfinance where coverage exists | Company IR, local exchange and regulator filings | Web search for source discovery and context |

## Free And Low-Cost Layer

| Source | Access | Credential |
|---|---|---|
| `korea-stock` | MCP server for DART/KRX official data | `DART_API_KEY` / `KRX_API_KEY` when required |
| `yfinance` | MCP/server or Python package for global public market data | None |
| SEC EDGAR | Official filings and company facts | None for basic access |
| FRED | Macro indicators | Optional API key |
| Alpha Vantage | Market and fundamental data | `ALPHA_VANTAGE_API_KEY` |
| Financial Modeling Prep | Financial data and estimates | `FMP_API_KEY` |
| Company IR | Official investor relations pages | None |
| Web search | Source discovery and context only | None |

## Optional Institutional Layer

Institutional MCPs are cataloged in `.mcp.institutional.json` but disabled by default. Their absence must not block command parsing, workspace creation, skill dispatch, or public-source report generation.

When an institutional source is available, treat it as a supporting source. Do not replace the public source trail; record source name, retrieval date, filing or market date, currency, accounting basis, and whether each number is reported, calculated, or inferred.
