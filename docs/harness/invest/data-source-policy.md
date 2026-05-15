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

## Source Capability Status

Source availability in the registry is repo-evidence status only, not live
runtime proof.

| Status | Meaning |
|---|---|
| `connected` | Repo evidence documents concrete callable tool names or a configured callable surface. |
| `documented_only` | Repo docs mention the source, but no callable repo tool contract is present. |
| `planned` | The source is contract-described for a future integration pass. |
| `external_manual` | The source can support manual research but is not callable by the harness. |

Use existing yfinance and DART/KRX through `korea-stock` tool contracts when
they apply. Represent FRED, SEC EDGAR, Alpha Vantage, FMP, ECOS, and planned
market-intelligence sources as capability contracts unless callable repo
evidence proves otherwise. Missing tool availability must be recorded as an
unresolved data gap, not silently converted into a new runtime dependency.
