<!-- GENERATED-SYNC: source=plugins/vertical-plugins/invest-research/policies/market-price-anchor.md; kind=policy; script=scripts/Sync-InvestSkills.ps1 -->
> [!IMPORTANT]
> Generated execution artifact. Do not edit directly; edit the vertical source and rerun pwsh ./scripts/Sync-InvestSkills.ps1.
> Common policies are synced from plugins/vertical-plugins/invest-research/policies/.
> Runtime output paths must use `${ACTIVE_WORKSPACE}`.
<!-- END GENERATED-SYNC -->

# Market Price Anchor Policy

## Purpose

All valuation, ratio, rating, and price-target work must use one explicit market-price snapshot for the run.

## Required Snapshot

Store the run's market-price anchor at `${ACTIVE_WORKSPACE}/00_input/market-price-snapshot.md`.

The snapshot must record:

- target company and ticker
- exchange, country, and trading currency
- reference price and reference date
- price source and retrieval timestamp
- shares outstanding source
- market capitalization basis
- net debt or net cash basis
- PER, PBR, EV, EV/EBITDA, and FCF yield calculation inputs
- any fallback source used when primary market data is unavailable

## Source Priority

- Korea: KRX close first, DART filings for share count and financial statement inputs, yfinance as a secondary market-data check.
- United States: yfinance and official exchange/IR data first, SEC EDGAR for filings.
- Global: yfinance, official IR, and exchange data first.

## Rule

Historical filing prices must not silently replace the current market-price anchor. If a current market close is unavailable, record the fallback source and reason in the snapshot before using it.

