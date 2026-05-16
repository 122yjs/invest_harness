# Validation Gates

Validation gates convert evidence limits into explicit pass/fail/review checks.
Every evidence plan should select gates before analyst fan-out.

## relative_index_gate

- Applies to: Google Trends, Naver DataLab, other relative attention indexes.
- Required checks: query/topic, geography, timeframe, comparison set, category/filter, index caveat.
- Must flag: missing query definition, mismatched geography, unreported relative scale.
- Prohibition: Do not infer sales from Google Trends alone.
- Prohibition: Do not infer market size from relative search interest.

## official_statistics_gate

- Applies to: KOSIS, ECOS, FRED, official macro/statistical sources.
- Required checks: table or series id, unit, period, frequency, release/update date, revision risk.
- Must flag: unit mismatch, stale period, definition break, missing geography.
- Prohibition: Do not convert a broad official category into a company claim without exposure evidence.

## trade_data_gate

- Applies to: customs_trade_api and similar trade datasets.
- Required checks: HS/category mapping, import/export direction, country pair, value/weight unit, latest month, base effect.
- Must flag: low-confidence mapping, missing FOB/CIF basis when relevant, quantity/value conflict.
- Prohibition: Do not infer company-specific revenue from customs trade data alone.

## company_disclosure_gate

- Applies to: DART-KRX, EDGAR, company filings, IR reports.
- Required checks: issuer identity, filing date, period of report, form/report type, currency, accounting basis.
- Must flag: stale report, non-comparable accounting basis, qualitative-only disclosure.
- Trust priority: T0. This gate has priority over vendor snapshots for reported company facts, guidance, share count, risk factors, segment data, and issuer identity.
- Prohibition: Do not infer undisclosed segment revenue or current demand beyond the filing boundary.

## procurement_gate

- Applies to: G2B and other public procurement records.
- Required checks: tender vs award, buyer, stage, date, amount, cancellation or amendment status.
- Must flag: duplicate tenders, cancelled awards, buyer-specific concentration.
- Prohibition: Do not treat public procurement as total market demand.

## market_context_gate

- Applies to: KOTRA, news, market reports, narrative context.
- Required checks: publication date, geography, source type, cited primary sources, qualitative vs quantitative boundary.
- Must flag: uncited numbers, commentary presented as fact, stale context.
- Prohibition: Do not treat KOTRA text/news as export volume.

## valuation_gate

- Applies to: yfinance, Alpha Vantage, FMP, filings, peer multiples, DCF artifacts.
- Required checks: valuation date, price source, share count, metric period, peer comparability, recalculation path.
- Must flag: stale price, mismatched metric periods, unsupported target price.
- Prohibition: Do not state valuation conclusions without source, date, and calculation basis.

## source_conflict_gate

- Applies to: any two or more sources used for the same claim.
- Required checks: date, unit, definition, coverage, methodology, primary vs secondary hierarchy.
- Must flag: unexplained differences, averaged values without rationale, conflicting periods.
- Prohibition: Do not average conflicting sources without explaining the conflict.
