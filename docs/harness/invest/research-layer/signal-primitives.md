# Signal Primitives

Signal primitives are reusable transformations from evidence into bounded signals.
They are not product-specific use cases and must not become router categories.

Each primitive defines:

- `purpose`
- `required_inputs`
- `compatible_sources`
- `common_metrics`
- `output fields`
- `caveats`
- `claim boundaries`

## search_interest_momentum

- purpose: measure directional change in relative search attention.
- required_inputs: query/topic, geography, timeframe, comparison base.
- compatible_sources: Google Trends, Naver DataLab.
- common_metrics: relative index, moving average, period-over-period change, regional split.
- output fields: subject, geography, period, index_change, momentum_direction, confidence.
- caveats: relative index only; sensitive to query choice and comparison set.
- claim boundaries: supports consumer interest or attention claims, not sales or market size.

## export_momentum

- purpose: measure export or import direction for mapped items or categories.
- required_inputs: HS code or trade category, country pair, period, value or weight.
- compatible_sources: customs_trade_api, KOTRA when used only as context.
- common_metrics: export value growth, weight growth, base effect, partner-country mix.
- output fields: subject, geography, period, trade_direction, growth_rate, base_effect_flag.
- caveats: mapping may be approximate; company attribution requires disclosure evidence.
- claim boundaries: supports trade momentum claims, not company revenue claims by itself.

## transaction_market_size

- purpose: create a bounded market transaction baseline from official or transaction datasets.
- required_inputs: official table or transaction dataset, unit, geography, period.
- compatible_sources: KOSIS, official statistics, yfinance for market value context when appropriate.
- common_metrics: total value, total count, unit price proxy, growth rate.
- output fields: market_scope, geography, period, metric, value, unit, confidence.
- caveats: coverage definitions can change; may omit informal or private channels.
- claim boundaries: supports baseline market context only within the source definition.

## procurement_demand

- purpose: measure public procurement activity as a demand proxy.
- required_inputs: tender or award records, buyer, date, amount, procurement stage.
- compatible_sources: g2b_procurement.
- common_metrics: tender count, award count, award value, buyer concentration.
- output fields: subject, buyer_group, period, procurement_stage, value, demand_signal.
- caveats: public-sector only; tenders may be cancelled or duplicated.
- claim boundaries: does not prove total market demand or private-sector demand.

## disclosure_exposure

- purpose: identify company exposure to subjects, segments, regions, customers, or risks from filings.
- required_inputs: filing text, segment notes, revenue breakdown, risk factors, period.
- compatible_sources: DART-KRX, EDGAR, company IR, yfinance/FMP only as secondary context.
- common_metrics: disclosed revenue share, segment mention, geography exposure, risk disclosure.
- output fields: company, subject, period, exposure_type, cited_disclosure, confidence.
- caveats: disclosures can be qualitative or lagged.
- claim boundaries: supports exposure claims, not current demand unless filings quantify it.

## market_context_signal

- purpose: capture external context that frames but does not independently prove a claim.
- required_inputs: source text or statistics, geography, date, topic.
- compatible_sources: KOTRA, news sources, official statistics, FMP, Alpha Vantage.
- common_metrics: context theme, event count, reported trend, cited statistic.
- output fields: subject, context_type, geography, period, evidence_summary, caveat.
- caveats: qualitative context often needs primary numeric corroboration.
- claim boundaries: supports narrative context, not standalone quantitative conclusions.

## regulatory_risk_signal

- purpose: identify policy, rule, legal, or regulatory changes that alter risk.
- required_inputs: regulation text, filing disclosure, policy announcement, effective date.
- compatible_sources: EDGAR, DART-KRX, official regulators, KOTRA, news_event sources.
- common_metrics: effective date, affected geography, compliance cost direction, probability marker.
- output fields: regulation, geography, affected_subject, timing, risk_direction, confidence.
- caveats: proposed rules and enacted rules must be separated.
- claim boundaries: supports risk framing, not financial magnitude without company exposure evidence.

## valuation_anchor

- purpose: anchor valuation discussion in price, multiple, DCF, or peer evidence.
- required_inputs: market price, share count, financial metric, peer set or DCF assumptions.
- compatible_sources: yfinance, Alpha Vantage, FMP, DART-KRX, EDGAR.
- common_metrics: market cap, EV, PER, PBR, EV/EBITDA, FCF yield, target-implied upside.
- output fields: company, valuation_date, metric, value, source, recalculation_note.
- caveats: stale price or mismatched accounting periods can distort comparisons.
- claim boundaries: supports valuation context, not a recommendation without scenario and risk evidence.

## macro_regime_signal

- purpose: summarize macro conditions relevant to rates, inflation, growth, FX, or policy.
- required_inputs: macro series id, period, frequency, geography, transformation.
- compatible_sources: FRED, ECOS, official statistics.
- common_metrics: level, change, moving average, regime bucket, release date.
- output fields: indicator, geography, period, value, unit, regime_interpretation.
- caveats: macro series are revised and may not map directly to company exposure.
- claim boundaries: supports macro sensitivity context, not company causality alone.

## news_event_signal

- purpose: structure recent events as dated evidence with source caveats.
- required_inputs: article/event, date, source, entity/subject, event type.
- compatible_sources: yfinance news, Alpha Vantage news, FMP news, official releases, KOTRA context.
- common_metrics: event date, source count, event severity, sentiment direction.
- output fields: event_id, date, subject, source, event_summary, confidence.
- caveats: distinguish confirmed facts from commentary, rumors, and analyst interpretation.
- claim boundaries: supports event awareness, not quantified impact without corroborating evidence.
