# Source Capability Registry

Sources are selected by capability. A source contract says what evidence it can
provide, which claims it can support, and which claims it cannot support alone.
The router should select sources from `required_evidence_types`, not from fixed
use-case labels.

## Contract Fields

Each source contract must include:

- `provides`
- `good_for`
- `not_good_for`
- `required_inputs`
- `outputs`
- `validation_rules`
- `forbidden_claims`

## opendart / DART-KRX

- provides: `company_disclosure`, `financial_statement`, `corporate_action`, `krx_trade_info`
- good_for: listed Korean company identification, official filings, audited statements, share count and exchange data
- not_good_for: global peer data, non-Korean company filings, real-time demand signals
- required_inputs: company name or ticker, `corp_code` when using DART, six-digit stock code when using KRX, period
- outputs: disclosure list, disclosure text, XBRL statements, base stock data, trade data
- validation_rules: verify company identity, filing date, report period, accounting basis, currency, and stock code
- forbidden_claims: do not infer product demand or segment revenue unless the disclosure states it

## yfinance

- provides: `price_valuation`, `market_context`, `company_snapshot`, `news_event`
- good_for: global listed company lookup, price history, market data, holders, quick peer context
- not_good_for: audited official financial statement replacement, regulatory filing truth, private market demand
- required_inputs: ticker symbol, market suffix when needed, period, interval
- outputs: ticker info, financials, price history, news, holders, options
- validation_rules: cross-check official filings for material accounting claims; record timestamp and exchange
- forbidden_claims: do not treat unofficial financial fields as final audited facts without official corroboration

## kosis

- provides: `official_statistics`, `market_transaction`, `demographic_baseline`, `long_time_series`
- good_for: official statistical baseline, transaction or population proxies, long-term trend context
- not_good_for: real-time granular SKU demand, company-specific revenue, daily trading signals
- required_inputs: table id, category code, geography, period, unit
- outputs: statistical table values, unit, period, source metadata
- validation_rules: record table id, unit, period, update date if available, and definition changes
- forbidden_claims: do not convert official category totals into company revenue without share evidence

## customs_trade_api

- provides: `export_import`, `trade_value`, `trade_weight`, `hs_code_dimension`, `country_dimension`
- good_for: item/country export-import momentum, trade base effects, geography exposure proxies
- not_good_for: company_specific_sales, local total market size, retail sell-through
- required_inputs: HS code candidate, country, import/export direction, period, currency basis if available
- outputs: value, weight, quantity, partner country, period, trade direction
- validation_rules: validate HS code mapping, latest month, FOB/CIF basis when relevant, base effect, and unit
- forbidden_claims: do not infer company-specific revenue from customs trade data alone

## google_trends

- provides: `relative_search_interest`, `regional_interest`, `related_queries`, `rising_queries`
- good_for: consumer interest direction, query momentum, regional attention, topic discovery
- not_good_for: absolute_market_size, sales_estimation_alone, market share, revenue
- required_inputs: query or topic, geography, timeframe, category if used, comparison set
- outputs: relative index, regional index, related terms, rising terms
- validation_rules: report geo, timeframe, query/topic, category, relative index caveat, and comparison normalization
- forbidden_claims: do not infer sales, revenue, or market size from search interest alone

## naver_datalab

- provides: `relative_search_interest`, `shopping_interest_proxy`, `demographic_search_split`
- good_for: Korea search interest direction, category attention proxy, demographic search mix
- not_good_for: absolute sales, total market size, company revenue, non-Korea coverage
- required_inputs: keyword groups, period, device, gender/age filters when used
- outputs: relative index, keyword group comparison, demographic splits
- validation_rules: record query set, period, filters, relative-index caveat, and comparison base
- forbidden_claims: do not treat relative Naver index as transaction volume or sales

## kotra

- provides: `market_context`, `news_event`, `export_market_context`, `regulatory_context`
- good_for: qualitative overseas market context, policy notes, market-entry issues, trade narrative
- not_good_for: verified export volume, company-specific sales, official transaction totals
- required_inputs: keyword, country or region, publication date range, topic
- outputs: report text, market notes, event summaries, qualitative caveats
- validation_rules: record publication date, geography, authoring body, and whether quantitative claims cite original sources
- forbidden_claims: do not treat KOTRA text or news as export volume

## g2b_procurement

- provides: `procurement`, `public_tender`, `award_notice`, `buyer_demand_proxy`
- good_for: public procurement demand signals, government buyer activity, tender timing
- not_good_for: total market demand, private-sector demand, company revenue unless awardee data proves it
- required_inputs: procurement keyword, buyer, period, geography, tender or award filters
- outputs: tender list, award list, buyer, value, date, classification
- validation_rules: distinguish tender from award, record procurement stage, buyer, amount, and cancellation status
- forbidden_claims: do not treat public procurement as total market demand

## ecos or macro official statistics

- provides: `macro_policy`, `macro_indicator`, `official_time_series`, `rates`, `prices`
- good_for: macro regime signals, rates, inflation, GDP, policy backdrop, official time series
- not_good_for: company-specific performance, product-level demand, immediate trading signals
- required_inputs: series id, period, geography, frequency
- outputs: official macro value, unit, frequency, release date
- validation_rules: record series id, unit, frequency, release calendar, revision risk, and seasonal adjustment
- forbidden_claims: do not attribute company earnings changes to macro data without a stated exposure mechanism

## FRED

- provides: `macro_indicator`, `official_time_series`, `rates`, `inflation`, `labor_market`
- good_for: United States macro regime context, long macro series, rates and policy backdrop
- not_good_for: company-specific sales, product demand, private transaction data
- required_inputs: FRED series id, period, frequency, transformation if used
- outputs: series observations, units, frequency, notes, last updated metadata
- validation_rules: record series id, units, frequency, seasonal adjustment, transformation, and observation window
- forbidden_claims: do not convert macro correlation into company causality without exposure evidence

## Alpha Vantage

- provides: `price_valuation`, `company_snapshot`, `technical_indicator`, `news_event`, `market_context`
- good_for: quotes, price series, technical indicators, company overview, quick global market context
- not_good_for: official filing replacement, absolute demand, audited financial statement truth
- required_inputs: symbol, function/tool, interval or period when relevant
- outputs: quote, time series, company overview, technical indicator, news sentiment
- validation_rules: record symbol, endpoint/tool, timestamp, quota limitations, and cross-check material financials
- forbidden_claims: do not treat API quote or overview fields as sole evidence for audited financial claims

## Financial Modeling Prep

- provides: `price_valuation`, `company_profile`, `financial_statement`, `analyst_estimate`, `market_context`
- good_for: company profiles, quotes, financial snapshots, estimates, ratings, market calendars
- not_good_for: official filing replacement, source-of-truth regulatory disclosure, unbounded free usage
- required_inputs: symbol, endpoint/tool, period, API plan capability
- outputs: profile, quote, statements, ratios, analyst data, market lists
- validation_rules: record endpoint/tool, plan restrictions, timestamp, and cross-check official filings for final claims
- forbidden_claims: do not state official company results from FMP alone when primary filings are available

## EDGAR

- provides: `company_disclosure`, `regulatory`, `filing_metadata`, `company_facts`
- good_for: United States issuer filings, official SEC submission metadata, company facts, annual and quarterly reports
- not_good_for: non-US official filings, market prices, search-interest signals, normalized analyst estimates
- required_inputs: CIK or ticker-to-CIK mapping, filing accession or company facts endpoint, user-agent header
- outputs: submission metadata, filing index, company facts, filing documents
- validation_rules: record CIK, accession number, filing form, filing date, period of report, and SEC user-agent compliance
- forbidden_claims: do not treat EDGAR filings as current market pricing or consumer demand evidence
