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

## Source Recording

Each finding must separate:

- source name
- retrieval date
- filing or market date
- currency
- accounting basis
- whether a number is reported, calculated, or inferred

