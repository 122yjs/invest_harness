# MCP Routing

## Default Routing

| Scope | First choice | Backup | Notes |
|---|---|---|---|
| Korean listed companies | `korea-stock` | yfinance | Use DART/KRX identifiers before financial statement or trade-data calls. |
| US listed companies | yfinance plus SEC/IR references | web search for source discovery | Use official filings for reported financials when precision matters. |
| Global listed companies | yfinance | company IR / local exchange / regulator | Label coverage gaps explicitly. |
| Macro indicators | FRED or official central-bank/statistical sources | web search for source discovery | Keep series IDs and dates. |

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
