# Data Source Policy

This document mirrors the source policy at `plugins/vertical-plugins/invest-research/policies/data-source-policy.md` for human-facing documentation. The source policy remains the generated-layer source of truth.

## Default Source Order

| Market | Primary | Secondary | Fallback |
|---|---|---|---|
| Korea | Company IR plus DART / KRX through `korea-stock` when available | exchange pages and yfinance market-data cross-checks | Web Search + Fetch for source discovery and missing context |
| US | Company IR plus SEC EDGAR filings and company facts | exchange pages plus yfinance/FMP/Alpha Vantage market or estimate snapshots | Web Search + Fetch for missing context |
| Global | Company IR plus local exchange and regulator filings | yfinance/FMP/Alpha Vantage where coverage exists | Web Search + Fetch for source discovery and context |

## Evidence Trust Order

Runtime availability decides what can be called, but it does not decide source
trust. For material company facts, financial statements, guidance, segment
data, risk factors, and management commentary, use the highest-trust available
evidence first:

| Tier | Evidence | Examples | Use |
|---|---|---|---|
| T0 | Company official and regulator disclosure | Company IR, earnings releases, shareholder letters, SEC EDGAR, DART/KRX, local exchange/regulator filings | Source of truth for reported financials, guidance, filings, risk factors, share count, and issuer identity |
| T1 | Official market/statistical sources | KRX trade data, exchange official pages, FRED, ECOS, KOSIS, central banks, statistical agencies | Source of truth for official market data and macro/statistical context |
| T2 | Vendor or financial data snapshots | yfinance, FMP, Alpha Vantage, institutional feeds when available | Fast cross-checks, estimates, market snapshots, peer screening; never overrides T0 for reported company facts |
| T3 | Web Search + Fetch and secondary narrative sources | News, trade press, market commentary, fetched web pages or PDFs | Discovery and context only unless the fetched body is an official source |

If tiers conflict, T0 wins unless it is stale for the claim being made. Vendor
or web values may be used as provisional context only when the official value is
missing, and the report must label the gap.

## Web Search And Fetch Policy

Use Web Search for link discovery, not as primary evidence. If search results
only provide summary snippets, use Web Fetch, browser open, or PDF/document
reading on the candidate URL before citing, summarizing, or validating the
claim.

Search finds candidate URLs; Fetch reads the full article, document, or PDF
body. Record the URL, title, publisher, publication date, retrieval timestamp,
and whether the body was successfully fetched. If the body cannot be fetched,
record an unresolved data gap and do not rely on the snippet.

This search-plus-fetch pattern is the default public-web retrieval path for
ordinary articles, documents, and PDFs. Do not add a separate scraping
infrastructure unless a later implementation pass explicitly approves it.

## Free And Low-Cost Layer

| Source | Access | Credential | Notes / Manual Routes |
|---|---|---|---|
| `korea-stock` | MCP server for DART/KRX official data | `DART_API_KEY` / `KRX_API_KEY` when required | Primary official path for Korean equities. |
| Company IR | Official investor relations pages | None | Primary source for corporate presentations & earnings releases. |
| SEC EDGAR | Official filings and company facts | None for basic access | JSON APIs: Submissions (`/submissions/CIK##########.json`), Concepts (`/api/xbrl/companyconcept/CIK##########/us-gaap/{ConceptName}.json`), Facts (`/api/xbrl/companyfacts/CIK##########.json`), Frames (`/api/xbrl/frames/us-gaap/{ConceptName}/USD/CY{YYYYQ#I}.json`), Bulk facts ZIP (`/Archives/edgar/daily-index/xbrl/companyfacts.zip`). |
| `yfinance` | MCP/server or Python package for global public market data | None | Fast global market and valuation data snapshot. |
| FRED | Macro indicators | Optional API key | FRED economic indicators. |
| Alpha Vantage | Market and fundamental data | `ALPHA_VANTAGE_API_KEY` | Supplementary global financials & pricing. |
| Financial Modeling Prep | Financial data and estimates | `FMP_API_KEY` | Supplementary global analyst estimates & snapshots. |
| KOTRA | Export market promotion agency data | None (Public data portal) | OpenAPI (`/data/15034830/openapi.do?recommendDataYn=Y#tab_layer_recommend_data`), 파일 데이터 자료실 (`/data/15083202/fileData.do?recommendDataYn=Y`). |
| Web Search + Web Fetch | Link discovery plus article/document/PDF body retrieval | None | Primary web discovery, also serves as the Universal Fallback. |

## Optional Institutional Layer

Institutional MCPs are cataloged in `.mcp.institutional.json` but disabled by default. Their absence must not block command parsing, workspace creation, skill dispatch, or public-source report generation.

When an institutional source is available, treat it as a supporting source. Do not replace the public source trail; record source name, retrieval date, filing or market date, currency, accounting basis, and whether each number is reported, calculated, or inferred.

## Source Capability Status

Source availability in the registry is repo-evidence status only, not live
runtime proof. Before analyst fan-out, record the live callable source inventory
in `${ACTIVE_WORKSPACE}/00_evidence/source-call-plan.md` as `Runtime
Availability` and `Live Tool Probe`.

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
If yfinance is absent from the live runtime, do not keep retrying that path.
Use actually callable FMP or Alpha Vantage when present; otherwise use SEC
EDGAR, company IR, and Web Search + Fetch with explicit claim boundaries.

## Universal Fallback & Web Search Integration

If any primary, secondary, or specialized data source fails to return the required information (due to credential issues, rate limits, network failures, or API coverage gaps), the system **MUST automatically fall back to Web Search + Web Fetch**. 

The universal fallback utilizes `web_search_fetch` (or browser-based retrieval when JavaScript execution is required) to discover, fetch, and validate missing facts, regulatory filings, press releases, or macro-level tables from public webs and official IR domains. This applies globally to all data fields across every single analytical phase.
