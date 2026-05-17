# Source Capability Registry

Sources are selected by capability. A source contract says what evidence it can
provide, which claims it can support, and which claims it cannot support alone.
The router should select sources from `required_evidence_types`, not from fixed
use-case labels.

## Evidence Trust Tier Semantics

Use trust tiers alongside `connection_status`. Runtime availability says whether
a source can be called in the current session; trust tier says how authoritative
the evidence is for a claim.

- T0: company official and regulator disclosure, including Company IR, earnings
  releases, shareholder letters, SEC EDGAR, DART/KRX, and local
  exchange/regulator filings.
- T1: official market or statistical sources, including exchange official market
  data, central banks, FRED, ECOS, KOSIS, and statistical agencies.
- T2: vendor or financial data snapshots, including yfinance, FMP, Alpha
  Vantage, and optional institutional feeds.
- T3: Web Search + Fetch and secondary narrative sources used for discovery and
  context.

For reported company facts, financial statements, guidance, segment data, risk
factors, share count, and issuer identity, T0 evidence has priority over T2/T3
even when T2 is easier to call. If T0 is unavailable or stale for a current
claim, record the data gap before using lower-tier evidence.

## Contract Fields

Each source contract must include:

- `source_id`
- `provider`
- `connection_status`
- `configured_in`
- `available_tools_or_endpoints`
- `evidence_types_supported`
- `good_for`
- `not_good_for`
- `required_inputs`
- `outputs`
- `validation_rules`
- `forbidden_claims`
- `fallback_sources`
- `notes`

## Connection Status Semantics

`connection_status` is repo-evidence only, not live runtime proof. Use only:

- `connected`: repo evidence documents a callable MCP/API/tool contract with concrete tool names or a configured callable surface.
- `documented_only`: repo docs or policies mention the source, but no callable repo config or concrete tool contract is present.
- `planned`: the source is intended for future integration and is contract-described only.
- `external_manual`: the source can be used by a human/manual workflow, but is not callable by the harness.

Analyst fan-out must use a separate live runtime check. Record that result in
`${ACTIVE_WORKSPACE}/00_evidence/source-call-plan.md` as `Runtime Availability`
and `Live Tool Probe`. If repo evidence says `connected` but the current
session cannot call the tool, mark the source unavailable for that run and route
to the documented fallback.

## DART-KRX / korea-stock

- source_id: `dart_krx_korea_stock`
- provider: OpenDART, KRX, and the `korea-stock` MCP surface
- connection_status: connected
- configured_in: `AGENTS.md`, `README.md`, `.agents/skills/*/SKILL.md`, `plugins/vertical-plugins/invest-research/skills/*/SKILL.md`
- available_tools_or_endpoints: `get_corp_code`, `get_disclosure_list`, `get_disclosure`, `get_financial_statement`, `get_stock_base_info`, `get_stock_trade_info`, `get_market_type`, `get_today_date`
- evidence_types_supported: `company_disclosure`, `financial_statement`, `corporate_action`, `krx_trade_info`, `company_identifier`
- good_for: Korean listed company identification, official filings, audited statements, share count, exchange classification, and KRX trade data
- not_good_for: global peer data, non-Korean company filings, real-time product demand, or non-disclosure consumer sentiment
- required_inputs: company name or ticker, `corp_code` when using DART, six-digit stock code when using KRX, date or period
- outputs: disclosure list, disclosure text, XBRL statements, base stock data, trade data, market type, retrieval date
- validation_rules: verify company identity, filing date, report period, accounting basis, currency, stock code, and KRX date format
- forbidden_claims: do not infer product demand, segment revenue, or non-Korean regulatory facts unless the disclosure states them
- fallback_sources: web_search_fetch as universal fallback if primary tools fail, yfinance for market-data cross-checks, company IR, exchange pages
- notes: Trust tier T0 for Korean issuer identity, official filings, reported financials, share count, and DART/KRX facts. Treat DART/KRX and Company IR as primary official paths; use yfinance only as a T2 supplement.

## yfinance

- source_id: `yfinance`
- provider: Yahoo Finance through the yfinance MCP/tooling surface
- connection_status: connected
- configured_in: `README.md`, `.agents/skills/*/SKILL.md`, `plugins/vertical-plugins/invest-research/skills/*/SKILL.md`
- available_tools_or_endpoints: `yfinance_search`, `yfinance_get_ticker_info`, `yfinance_get_financials`, `yfinance_get_price_history`, `yfinance_get_ticker_news`, `yfinance_get_holders`, `yfinance_get_option_chain`, `yfinance_get_option_dates`, `yfinance_get_top`
- evidence_types_supported: `price_valuation`, `market_context`, `company_snapshot`, `financial_snapshot`, `news_event`, `holder_context`, `options_market`
- good_for: global listed company lookup, price history, market data, options, holders, quick peer context, and market news
- not_good_for: audited official financial statement replacement, regulatory filing truth, private market demand, or final accounting claims without official corroboration
- required_inputs: ticker symbol, market suffix when needed, period, interval, statement frequency, option expiration when used
- outputs: ticker info, financial snapshots, price history, news, holders, option chains, sector lists, timestamp
- validation_rules: cross-check official filings for material accounting claims; record exchange, symbol, timestamp, currency, and whether values are vendor snapshots
- forbidden_claims: do not treat unofficial financial fields as final audited facts without official corroboration
- fallback_sources: web_search_fetch as universal fallback if primary tools fail, DART-KRX for Korean official data, SEC EDGAR or company IR for US filings, FMP or Alpha Vantage only when live callable, local exchange/regulator pages for non-US filings
- notes: Trust tier T2. Use for public market data and quick coverage when live runtime availability is confirmed; separate reported facts from vendor-derived fields and do not override T0 company official or regulator disclosure.

## FRED

- source_id: `fred`
- provider: Federal Reserve Economic Data
- connection_status: documented_only
- configured_in: `docs/harness/invest/data-source-policy.md`, `docs/harness/invest/mcp-routing.md`, `plugins/vertical-plugins/invest-research/policies/data-source-policy.md`
- available_tools_or_endpoints: FRED series IDs and public series endpoints if available outside the harness; no callable repo tool contract found in this checkout
- evidence_types_supported: `macro_policy`, `macro_regime`, `interest_rates`, `inflation`, `employment`, `economic_activity`, `official_time_series`
- good_for: US macro regime checks, rates/inflation/liquidity context, labor-market context, and valuation discount-rate assumptions
- not_good_for: company-specific revenue, real-time stock pricing, product-level demand, or direct causal claims about company fundamentals
- required_inputs: series ID, period, frequency, transformation, observation window, seasonal adjustment basis
- outputs: observations, units, frequency, latest observation date, release notes when available
- validation_rules: report series ID, frequency, unit, latest observation date, transformation, and distinguish level versus rate of change
- forbidden_claims: do not infer company fundamentals from macro series alone; do not treat macro correlation as causation
- fallback_sources: web_search_fetch as universal fallback if primary tools fail, ECOS or local central-bank/statistical sources for non-US macro, official central-bank releases
- notes: Status is not proof of a live MCP call path; record missing callable tooling as a data gap when automation is required. Active FRED_API_KEY is registered and available in .env.

## SEC EDGAR

- source_id: `sec_edgar`
- provider: SEC EDGAR
- connection_status: external_manual
- configured_in: `docs/harness/invest/data-source-policy.md`, `plugins/vertical-plugins/invest-research/policies/data-source-policy.md`, earnings and QA skill guidance
- available_tools_or_endpoints:
  - SEC Submission List: https://data.sec.gov/submissions/CIK##########.json
  - XBRL Company Concept History: https://data.sec.gov/api/xbrl/companyconcept/CIK##########/us-gaap/{ConceptName}.json (e.g. AccountsPayableCurrent)
  - XBRL Company Facts: https://data.sec.gov/api/xbrl/companyfacts/CIK##########.json
  - XBRL Period/Concept Frames: https://data.sec.gov/api/xbrl/frames/us-gaap/{ConceptName}/USD/CY{YYYYQ#I}.json (e.g. CY2019Q1I)
  - Complete XBRL Bulk Facts ZIP: http://www.sec.gov/Archives/edgar/daily-index/xbrl/companyfacts.zip
- evidence_types_supported: `company_disclosure`, `financial_statement`, `risk_factor`, `segment_disclosure`, `filing_metadata`, `company_facts`, `ownership_if_available`
- good_for: US issuer filings, 10-K/10-Q/8-K review, segment evidence, risk-factor evidence, and official filing metadata
- not_good_for: real-time market price, non-US local filings unless cross-listed, consumer search interest, or normalized analyst estimates
- required_inputs: company name, ticker or CIK, filing type, filing date range, accession number when available, report period
- outputs: filing metadata, filing documents, company facts, form type, filing date, period of report, cited section
- validation_rules: report filing type, filing date, period, CIK/accession, and cite exact filing section when possible
- forbidden_claims: do not use stale filings as current guidance; do not infer current quarter performance without newer evidence
- fallback_sources: web_search_fetch as universal fallback if primary tools fail, company IR, earnings releases, exchange pages, yfinance only for market-data context
- notes: Trust tier T0 for US issuer filings, reported financials, risk factors, segment disclosure, and filing metadata. Treat as official disclosure evidence when manually or programmatically retrieved through the specified routes; record missing callable tooling as a data gap for automated runs.

## Alpha Vantage

- source_id: `alpha_vantage`
- provider: Alpha Vantage
- connection_status: documented_only
- configured_in: `docs/harness/invest/data-source-policy.md`, `plugins/vertical-plugins/invest-research/policies/data-source-policy.md`
- available_tools_or_endpoints: Alpha Vantage functions/endpoints when separately available; no callable repo tool contract found in this checkout
- evidence_types_supported: `price_valuation`, `technical_market_data`, `fundamentals_if_available`, `fx`, `commodities_if_available`, `macro_if_available`, `news_event`
- good_for: price history, technical indicators, market-data fallback, FX/commodity/economic data depending on available endpoint access
- not_good_for: primary audited financial statement source, final valuation without cross-check, official regulatory disclosure
- required_inputs: symbol, function or endpoint, interval, period, adjusted/unadjusted basis, currency when applicable
- outputs: quote, time series, company overview, technical indicator, news sentiment, timestamp, response status
- validation_rules: report endpoint/function, adjusted versus unadjusted prices, currency, timestamp, and rate-limit or stale-response warnings
- forbidden_claims: do not treat vendor fundamentals as more authoritative than filings; do not use technical indicators as standalone investment conclusions
- fallback_sources: web_search_fetch as universal fallback if primary tools fail, yfinance for public market data, official filings for reported financials, company IR, exchange pages
- notes: Trust tier T2. Keep as a documented capability until a callable repo tool/config appears; do not override T0 official filings or Company IR. Active ALPHA_VANTAGE_API_KEY is registered and available in .env.

## KOSIS

- source_id: `kosis`
- provider: Korean Statistical Information Service
- connection_status: planned
- configured_in: `docs/harness/invest/research-layer/source-capability-registry.md`
- available_tools_or_endpoints: table IDs and public/manual statistical downloads; no callable repo tool contract in this pass
- evidence_types_supported: `official_statistics`, `market_transaction`, `demographic_baseline`, `long_time_series`
- good_for: official statistical baseline, transaction or population proxies, long-term trend context, Korea category-level indicators
- not_good_for: real-time granular SKU demand, company-specific revenue, daily trading signals, or private-sector share without additional evidence
- required_inputs: table ID, category code, geography, period, unit, update date when available
- outputs: statistical table values, unit, period, source metadata, definition notes
- validation_rules: record table ID, unit, period, update date, geography, and definition changes
- forbidden_claims: do not convert official category totals into company revenue without share evidence
- fallback_sources: web_search_fetch as universal fallback if primary tools fail, ECOS for macro series, DART-KRX/company disclosure for company exposure
- notes: Docs-only market-intelligence contract for this pass. Active KOSIS_API_KEY is registered and available in .env.

## Korea Customs Service / customs_trade_api

- source_id: `customs_trade_api`
- provider: Korea Customs Service or official customs trade data
- connection_status: planned
- configured_in: `docs/harness/invest/research-layer/source-capability-registry.md`
- available_tools_or_endpoints: HS-code trade data endpoints or manual customs trade tables when separately available; no callable repo tool contract in this pass
- evidence_types_supported: `export_import`, `trade_value`, `trade_weight`, `hs_code_dimension`, `country_dimension`, `supply_chain_proxy`
- good_for: item/country export-import momentum, trade base effects, geography exposure proxies, and supply-chain context
- not_good_for: company-specific sales, local total market size, retail sell-through, or product-level demand without additional evidence
- required_inputs: HS code candidate, country, import/export direction, period, currency basis, quantity/weight unit
- outputs: value, weight, quantity, partner country, period, trade direction, unit, revision/update date
- validation_rules: validate HS code mapping, latest month, FOB/CIF basis when relevant, base effect, currency, and unit
- forbidden_claims: do not infer company-specific revenue from customs trade data alone
- fallback_sources: web_search_fetch as universal fallback if primary tools fail, DART/EDGAR segment exposure, company IR, KOTRA context, official trade publications
- notes: Docs-only market-intelligence contract for this pass. Active CUSTOMS_TRADE_API_KEY, format (XML), and endpoint (https://apis.data.go.kr/1220000/nitemtrade) are registered and available in .env.

## Google Trends

- source_id: `google_trends`
- provider: Google Trends
- connection_status: planned
- configured_in: `docs/harness/invest/research-layer/source-capability-registry.md`
- available_tools_or_endpoints: Google Trends UI/export or third-party/manual workflow when separately available; no callable repo tool contract in this pass
- evidence_types_supported: `relative_search_interest`, `regional_interest`, `related_queries`, `rising_queries`, `consumer_attention_proxy`
- good_for: consumer interest direction, query momentum, regional attention, topic discovery, and relative attention comparison
- not_good_for: absolute market size, sales estimation alone, market share, revenue, or transaction volume
- required_inputs: query or topic, geography, timeframe, category if used, comparison set
- outputs: relative index, regional index, related terms, rising terms, normalization context
- validation_rules: report geography, timeframe, query/topic, category, relative-index caveat, and comparison normalization
- forbidden_claims: do not infer sales, revenue, or market size from search interest alone
- fallback_sources: web_search_fetch as universal fallback if primary tools fail, Naver DataLab for Korea search context, transaction/statistics sources for market size, company disclosures for revenue exposure
- notes: Docs-only market-intelligence contract for this pass.

## Naver DataLab

- source_id: `naver_datalab`
- provider: Naver DataLab
- connection_status: planned
- configured_in: `docs/harness/invest/research-layer/source-capability-registry.md`
- available_tools_or_endpoints: Naver DataLab UI/API when separately available; no callable repo tool contract in this pass
- evidence_types_supported: `relative_search_interest`, `shopping_interest_proxy`, `demographic_search_split`, `korea_attention_proxy`
- good_for: Korea search interest direction, category attention proxy, keyword group comparison, and demographic search mix
- not_good_for: absolute sales, total market size, company revenue, non-Korea coverage, or transaction volume
- required_inputs: keyword groups, period, device, gender/age filters when used, category context
- outputs: relative index, keyword group comparison, demographic splits, period and filter metadata
- validation_rules: record query set, period, filters, relative-index caveat, and comparison base
- forbidden_claims: do not treat relative Naver index as transaction volume or sales
- fallback_sources: web_search_fetch as universal fallback if primary tools fail, Google Trends for global attention context, KOSIS or transaction sources for market baselines, company disclosures
- notes: Docs-only market-intelligence contract for this pass.

## KOTRA

- source_id: `kotra`
- provider: Korea Trade-Investment Promotion Agency
- connection_status: external_manual
- configured_in: `docs/harness/invest/research-layer/source-capability-registry.md`
- available_tools_or_endpoints:
  - OpenAPI 추천 자료 서비스: https://www.data.go.kr/data/15034830/openapi.do?recommendDataYn=Y#tab_layer_recommend_data
  - 파일 데이터 자료실: https://www.data.go.kr/data/15083202/fileData.do?recommendDataYn=Y
- evidence_types_supported: `market_context`, `news_event`, `export_market_context`, `regulatory_context`, `qualitative_trade_context`
- good_for: qualitative overseas market context, policy notes, market-entry issues, trade narrative, and local event context
- not_good_for: verified export volume, company-specific sales, official transaction totals, or audited financial figures
- required_inputs: keyword, country or region, publication date range, topic, document title or URL
- outputs: report text, market notes, event summaries, qualitative caveats, cited original sources when present
- validation_rules: record publication date, geography, authoring body, and whether quantitative claims cite original sources
- forbidden_claims: do not treat KOTRA text or news as export volume
- fallback_sources: web_search_fetch as universal fallback if primary tools fail, customs trade data for trade totals, company disclosures for company exposure, official regulator or statistics sources
- notes: Manual source contract; use the specified OpenAPI and file download paths for manual or programmatic retrieval; cite underlying official data when KOTRA quotes quantitative figures.

## G2B / public procurement

- source_id: `g2b_procurement`
- provider: Korea ON-line E-Procurement System or public procurement portals
- connection_status: planned
- configured_in: `docs/harness/invest/research-layer/source-capability-registry.md`
- available_tools_or_endpoints: public tender and award search/manual exports when separately available; no callable repo tool contract in this pass
- evidence_types_supported: `procurement`, `public_tender`, `award_notice`, `buyer_demand_proxy`, `public_sector_signal`
- good_for: public procurement demand signals, government buyer activity, tender timing, award notices, and public-sector demand proxies
- not_good_for: total market demand, private-sector demand, company revenue unless awardee data proves it, or consumer sell-through
- required_inputs: procurement keyword, buyer, period, geography, tender or award filters, procurement stage
- outputs: tender list, award list, buyer, amount, date, classification, status
- validation_rules: distinguish tender from award, record procurement stage, buyer, amount, cancellation status, and whether awardee identity is confirmed
- forbidden_claims: do not treat public procurement as total market demand
- fallback_sources: web_search_fetch as universal fallback if primary tools fail, company disclosures for award materiality, public agency releases, market statistics for broader demand
- notes: Docs-only market-intelligence contract for this pass.

## Web Search + Web Fetch

- source_id: `web_search_fetch`
- provider: Search engine result discovery plus URL fetch/browser body retrieval
- connection_status: external_manual
- configured_in: `docs/harness/invest/research-layer/source-capability-registry.md`, `docs/harness/invest/mcp-routing.md`, source-router guidance
- available_tools_or_endpoints: search query result pages, URL fetch/open tools, browser/PDF/document readers when available in the execution environment
- evidence_types_supported: `source_discovery`, `news_event`, `market_context`, `company_disclosure_context`, `policy_context`, `document_body`, `pdf_document`
- good_for: finding candidate URLs, retrieving article or document body text, reading public PDFs, checking source dates, and filling context gaps when structured sources are insufficient
- not_good_for: replacing official filings for audited facts, bypassing paywalls or access controls, treating search snippets as evidence, or creating a standalone scraping infrastructure
- required_inputs: search query, entity or subject, geography, date range, preferred source type, candidate URL, retrieval timestamp
- outputs: candidate URL list, fetched article/document/PDF body, title, publisher, publication date, retrieval date, quoted or paraphrased evidence excerpts, fetch failure notes
- validation_rules: Search finds candidate URLs; Fetch reads full article, document, or PDF body; do not rely on summary snippets alone; record URL, title, publisher, publication date, retrieval timestamp, and whether the body was fully fetched
- forbidden_claims: do not cite search snippets as primary evidence; do not infer facts from result ranking; do not summarize an article, filing, document, or PDF unless the fetched body was read
- fallback_sources: official source pages, company IR, regulator pages, exchange pages, MCP/API sources when structured data is required
- notes: Use search plus fetch as the default public-web retrieval pair. This avoids a separate scraping layer for ordinary articles, documents, and PDFs while preserving citation and body-read validation.

## Financial Modeling Prep

- source_id: `financial_modeling_prep`
- provider: Financial Modeling Prep
- connection_status: documented_only
- configured_in: `docs/harness/invest/research-layer/source-capability-registry.md`, `plugins/vertical-plugins/invest-research/skills/source-router/SKILL.md`, `plugins/vertical-plugins/invest-research/policies/data-source-policy.md`
- available_tools_or_endpoints: FMP endpoints when separately available; no callable repo tool contract found in this checkout
- evidence_types_supported: `price_valuation`, `company_profile`, `financial_statement`, `analyst_estimate`, `market_context`
- good_for: company profiles, quotes, financial snapshots, estimates, ratings, and market calendars when access is available
- not_good_for: official filing replacement, source-of-truth regulatory disclosure, or unbounded free usage
- required_inputs: symbol, endpoint/tool, period, API plan capability, timestamp
- outputs: profile, quote, statements, ratios, analyst data, market lists, response metadata
- validation_rules: record endpoint/tool, plan restrictions, timestamp, and cross-check official filings for final claims
- forbidden_claims: do not state official company results from FMP alone when primary filings are available
- fallback_sources: web_search_fetch as universal fallback if primary tools fail, company IR, SEC EDGAR or DART-KRX for official filings, local regulator filings, yfinance for public market data when live callable
- notes: Preserved existing/public contract; not a new runtime dependency in this pass. Active FMP_API_KEY is registered and available in .env.

## ECOS or macro official statistics

- source_id: `ecos_macro_official_statistics`
- provider: Bank of Korea ECOS or official macro/statistical sources
- connection_status: external_manual
- configured_in: `docs/harness/invest/research-layer/source-capability-registry.md`, `docs/harness/invest/mcp-routing.md`, `plugins/vertical-plugins/invest-research/skills/source-router/SKILL.md`
- available_tools_or_endpoints: ECOS/manual official statistics tables or central-bank releases when separately available; no callable repo tool contract found in this checkout
- evidence_types_supported: `macro_policy`, `macro_indicator`, `official_time_series`, `rates`, `prices`, `economic_activity`
- good_for: macro regime signals, rates, inflation, GDP, policy backdrop, official time series, Korea macro context
- not_good_for: company-specific performance, product-level demand, immediate trading signals, or direct company causality
- required_inputs: series ID, period, geography, frequency, unit, seasonal adjustment basis
- outputs: official macro value, unit, frequency, release date, revision notes when available
- validation_rules: record series ID, unit, frequency, release calendar, revision risk, and seasonal adjustment
- forbidden_claims: do not attribute company earnings changes to macro data without a stated exposure mechanism
- fallback_sources: web_search_fetch as universal fallback if primary tools fail, FRED for US macro, KOSIS for Korean official statistics, central-bank/statistical agency releases
- notes: Preserved macro capability; use as official context and keep company-level causal claims bounded.
