# MCP Routing

## Default Routing

| Scope | First choice | Backup | Notes |
|---|---|---|---|
| Korean listed companies | Company IR plus DART/KRX through `korea-stock` | yfinance for market-data and peer cross-checks | Use official company/regulator disclosure before vendor snapshots. |
| US listed companies | Company IR plus SEC EDGAR filings/company facts | FMP / Alpha Vantage / yfinance when callable, then Web Search + Fetch | Use official filings for reported financials and guidance. |
| Global listed companies | Company IR plus local exchange / regulator filings | yfinance / FMP / Alpha Vantage where coverage exists | Label coverage gaps explicitly. |
| Macro indicators | FRED or official central-bank/statistical sources | web search for source discovery | Keep series IDs and dates. |

## Evidence Trust Routing

Select sources by evidence need, then rank by trust tier:

1. T0 company official and regulator disclosure: Company IR, earnings releases,
   SEC EDGAR, DART/KRX, and local exchange/regulator filings.
2. T1 official market/statistical sources: exchange official data, central banks,
   FRED, ECOS, KOSIS, and statistical agencies.
3. T2 vendor/financial snapshots: yfinance, FMP, Alpha Vantage, and optional
   institutional feeds.
4. T3 discovery/context: Web Search + Fetch and secondary narrative sources.

Runtime availability can force a fallback, but it cannot promote T2 or T3 above
T0 for reported company facts. If official evidence is unavailable, record the
gap before using vendor or fetched secondary evidence.

## Web Search + Web Fetch Routing

Web Search is a discovery step. Use it to find candidate URLs, source titles,
publishers, and date hints. Do not treat search result snippets as primary
evidence.

When a search result is relevant, route the candidate URL to Web Fetch, browser
open, or PDF/document reading before using it in the evidence ledger. Fetch must
read the full article, document, or PDF body, not just the snippet. Record body
retrieval status in the source-call plan and source-validation output.

If Web Fetch cannot retrieve the body, record the URL as an unresolved data gap
or use an official fallback source. Do not add separate scraping infrastructure
for ordinary public articles, documents, or PDFs in this pass.

## Optional Institutional Routing

`.mcp.institutional.json` is a disabled optional catalog. Enabling an institutional server is an environment-specific operation and should not be required by this repository's default tests.

Institutional data can supplement:

- consensus and estimates
- transcript and event monitoring
- credit ratings
- private-market or ownership context

It must not remove the requirement to cite public or official source trails in findings and QA.

## Portable Environment Routing

API keys and local MCP executable paths are environment-specific. Keep secret
values out of tracked files and provide them through the repository-local `.env`
file or Windows User environment variables.

Default public MCP server entrypoints should call the stable PowerShell wrappers:

- `scripts\mcp\Start-KoreaStockMcp.ps1`
- `scripts\mcp\Start-YFinanceMcp.ps1`

If a machine uses a different executable name or package manager path, set only
the corresponding command override variable:

- `INVEST_HARNESS_KOREA_STOCK_MCP_COMMAND`
- `INVEST_HARNESS_KOREA_STOCK_MCP_ARGS`
- `INVEST_HARNESS_YFINANCE_MCP_COMMAND`
- `INVEST_HARNESS_YFINANCE_MCP_ARGS`

Do not store per-machine MCP command details in `.mcp.institutional.json`; that
catalog remains disabled for default validation.

## Capability Status Routing

`connection_status` in the source capability registry is repo-evidence status
only, not live runtime proof.

- `connected`: route to the documented tool contract when the evidence need matches and the live runtime probe confirms availability.
- `documented_only`: record the source as known but unavailable to the harness unless a callable tool is later added.
- `planned`: treat as a docs-only contract for future integration.
- `external_manual`: allow manual evidence collection, but record the gap for automated runs.

Before analyst fan-out, write `Runtime Availability` and `Live Tool Probe` in
`${ACTIVE_WORKSPACE}/00_evidence/source-call-plan.md`. If yfinance is absent
from the live tool inventory, do not keep retrying it; mark it unavailable and
route to actually callable FMP/Alpha Vantage or official/manual fallback
sources.

Source routing must preserve FMP and ECOS as existing capability contracts and
must not require optional institutional servers for default validation.
