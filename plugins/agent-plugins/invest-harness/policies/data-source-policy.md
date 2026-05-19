<!-- GENERATED-SYNC: source=plugins/vertical-plugins/invest-research/policies/data-source-policy.md; kind=policy; script=scripts/sync_invest_skills.py -->
> [!IMPORTANT]
> Generated execution artifact. Do not edit directly; edit the vertical source and rerun `python scripts/sync_invest_skills.py` (or `scripts/Sync-InvestSkills.ps1` / `scripts/Sync-InvestSkills.sh`).
> Common policies are synced from `plugins/vertical-plugins/invest-research/policies/`.
> Runtime output paths must use `${ACTIVE_WORKSPACE}`.
<!-- END GENERATED-SYNC -->

# Data Source Policy

## Purpose

Use reproducible, personally accessible data sources before optional institutional sources.

## Default Source Order

For Korean listed companies:

1. Company IR plus DART and KRX through the `korea-stock` MCP server when available.
2. Exchange pages and yfinance for market-data cross-checks and global peer comparison.
3. Reputable public filings and fetched official documents.
4. Web search only when structured sources are insufficient.

For US listed companies:

1. Company IR plus SEC EDGAR filings and company facts.
2. Exchange pages and official press releases.
3. yfinance, FMP, and Alpha Vantage for market data, financial snapshots, estimates, and news.
4. Web search only for context or missing public facts.

For global listed companies:

1. Company IR, local exchange filings, and regulator filings.
2. yfinance, FMP, and Alpha Vantage where coverage exists.
3. Web search only for source discovery and context.

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
| Company IR | Official company disclosures | None |
| SEC EDGAR | Official US filings | None for basic access |
| `yfinance` | Global public market data | None |
| FRED | Macro indicators | Optional API key |
| Alpha Vantage | Market/fundamental data | `ALPHA_VANTAGE_API_KEY` |
| Financial Modeling Prep | Financial data and estimates | `FMP_API_KEY` |
| Web Search + Web Fetch | Link discovery plus article/document/PDF body retrieval | None |

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

## Source Recording

Each finding must separate:

- source name
- retrieval date
- filing or market date
- currency
- accounting basis
- whether a number is reported, calculated, or inferred
