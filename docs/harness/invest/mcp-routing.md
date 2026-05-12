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
