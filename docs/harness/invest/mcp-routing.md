# MCP Routing

## Default Routing

| Scope | First choice | Backup | Notes |
|---|---|---|---|
| Korean listed companies | `korea-stock` | yfinance | Use DART/KRX identifiers before financial statement or trade-data calls. |
| US listed companies | yfinance plus SEC/IR references | web search for source discovery | Use official filings for reported financials when precision matters. |
| Global listed companies | yfinance | company IR / local exchange / regulator | Label coverage gaps explicitly. |
| Macro indicators | FRED or official central-bank/statistical sources | web search for source discovery | Keep series IDs and dates. |

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

## Capability Status Routing

`connection_status` in the source capability registry is repo-evidence status
only, not live runtime proof.

- `connected`: route to the documented tool contract when the evidence need matches.
- `documented_only`: record the source as known but unavailable to the harness unless a callable tool is later added.
- `planned`: treat as a docs-only contract for future integration.
- `external_manual`: allow manual evidence collection, but record the gap for automated runs.

Source routing must preserve FMP and ECOS as existing capability contracts and
must not require optional institutional servers for default validation.
