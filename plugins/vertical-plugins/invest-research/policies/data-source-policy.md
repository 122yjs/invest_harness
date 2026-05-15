# Data Source Policy

## Purpose

Use reproducible, personally accessible data sources before optional institutional sources.

## Default Source Order

For Korean listed companies:

1. DART and KRX through the `korea-stock` MCP server when available.
2. yfinance for market-data cross-checks and global peer comparison.
3. Company IR, exchange pages, and reputable public filings.
4. Web search only when structured sources are insufficient.

For US listed companies:

1. SEC EDGAR and company IR for filings.
2. yfinance for market data, financial snapshots, and news.
3. Exchange pages and official press releases.
4. Web search only for context or missing public facts.

For global listed companies:

1. yfinance where coverage exists.
2. Company IR, local exchange filings, and regulator filings.
3. Web search only for source discovery and context.

## Optional Institutional Layer

Institutional MCPs and paid datasets are optional. Their absence must not make the basic workflow fail. When present, they are supporting sources rather than replacements for the run's primary public source trail.

The disabled catalog lives at `.mcp.institutional.json`. Keep `mcpServers` empty by default so local validation and public-source workflows do not depend on paid credentials.

Optional sources currently tracked:

- Daloopa
- Morningstar
- S&P Global
- FactSet
- Moody's
- MT Newswires
- Aiera
- LSEG
- PitchBook
- Chronograph
- Egnyte

## Free And Low-Cost Layer

Use personally accessible sources first:

| Source | Access | Credential |
|---|---|---|
| `korea-stock` | DART/KRX official data | `DART_API_KEY` / `KRX_API_KEY` when required |
| `yfinance` | Global public market data | None |
| SEC EDGAR | Official US filings | None for basic access |
| FRED | Macro indicators | Optional API key |
| Alpha Vantage | Market/fundamental data | `ALPHA_VANTAGE_API_KEY` |
| Financial Modeling Prep | Financial data and estimates | `FMP_API_KEY` |
| Company IR | Official company disclosures | None |
| Web search | Source discovery and context | None |

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

## Source Recording

Each finding must separate:

- source name
- retrieval date
- filing or market date
- currency
- accounting basis
- whether a number is reported, calculated, or inferred
