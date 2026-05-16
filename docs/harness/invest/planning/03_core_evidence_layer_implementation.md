아래가 **수정된 전체 구현계획**입니다.
핵심 수정점은 이것입니다.

```text
FRED / SEC EDGAR / Alpha Vantage / yfinance / DART-KRX는 “신규 연동”이 아니라
이미 연결된 소스를 Evidence Layer가 인식하도록 source capability contract로 편입한다.

KOSIS / 관세청 / Google Trends / Naver DataLab / KOTRA / G2B는
이번 패스에서 실제 API client 구현이 아니라 문서·계약·라우팅·검증 규칙까지만 만든다.
```

---

# 0. 최종 목표

현재 `invest_harness`를 다음 구조로 확장합니다.

```text
기존:
사용자 요청
→ 00_input
→ 01~06 analyst fan-out
→ 07_draft
→ 09_qa
→ 08_final

변경 후:
사용자 요청
→ 00_input
→ 00_evidence
   ├─ question decomposition
   ├─ evidence plan
   ├─ source call plan
   ├─ evidence ledger
   ├─ signal cards
   └─ source validation
→ 01~06 analyst fan-out
→ 07_draft
→ 09_qa + source/claim audit
→ 08_final
```

즉, 기존 analyst 구조를 갈아엎는 게 아니라 **앞단에 Evidence Planning Layer를 추가**합니다.

---

# 1. 핵심 설계 원칙

## 반드시 지킬 원칙

```yaml
core_policy:
  no_fixed_product_taxonomy: true
  no_use_case_hard_routing: true
  preserve_user_surface_terms: true
  allow_unseen_market_objects: true
  use_ontology_for_candidate_mapping_only: true
  source_selection_based_on_evidence_need: true
  signal_selection_based_on_claim_type_and_evidence_type: true
```

## 금지사항

```text
금지:
- cosmetics, pet_supplies, power_equipment 같은 제품군을 core router enum으로 두기
- pet_ecommerce, cosmetics_sea_export 같은 use case를 router 본체에 넣기
- Google Trends 지수를 시장 규모나 매출로 해석하기
- 관세청 수출 데이터를 특정 기업 매출로 직접 해석하기
- KOTRA 텍스트를 수출량 데이터처럼 사용하기
- FRED / SEC EDGAR / Alpha Vantage를 중복 연동하기
```

## 허용되는 것

```text
허용:
- use case는 eval/golden scenario에만 배치
- source는 capability contract로 정의
- subject는 사용자 입력에서 자유 추출
- ontology는 강제 분류가 아니라 후보 매핑만 수행
- evidence type과 signal primitive는 재사용 가능한 범용 단위로 정의
```

---

# 2. 전체 아키텍처

```text
User Request
   ↓
Input Gate
   ↓
Question Decomposition
   ↓
Evidence Planner
   ↓
Source Capability Router
   ↓
Source Call Plan
   ↓
Evidence Ledger
   ↓
Signal Primitive Engine
   ↓
Validation Gate
   ↓
Existing Analyst Fan-out
   ├─ Financial
   ├─ Fundamental
   ├─ Valuation
   ├─ Technical
   ├─ Macro/Sentiment
   └─ Risk/Scenario
   ↓
Draft
   ↓
QA + Source/Claim Audit
   ↓
Final Report
```

---

# 3. 소스 그룹 재정의

## Group A. 이미 연결된 것으로 간주하고 먼저 탐지할 소스

Codex는 이 소스들을 **새로 만들면 안 됩니다.**
먼저 `.mcp.institutional.json`, README, AGENTS, MCP routing 문서, skill 문서를 확인해야 합니다.

```text
Existing / likely connected sources:
- yfinance-mcp
- korea-stock-mcp / DART / KRX
- FRED
- SEC EDGAR
- Alpha Vantage
```

이들은 이렇게 처리합니다.

```yaml
connection_status:
  - connected
  - connected_but_tool_contract_needs_confirmation
  - documented_only
  - planned
  - external_manual
```

예:

```yaml
source_id: fred
connection_status: connected_or_verify
role:
  - macro_policy
  - macro_regime
  - interest_rates
  - inflation
  - employment
validation:
  - report_series_id
  - report_frequency
  - report_latest_observation_date
  - distinguish_level_vs_rate_of_change
forbidden_claims:
  - do_not_infer_company_fundamentals_from_macro_series_alone
```

```yaml
source_id: sec_edgar
connection_status: connected_or_verify
role:
  - company_disclosure
  - financial_statement
  - risk_factor
  - segment_disclosure
validation:
  - report_filing_type
  - report_filing_date
  - report_period
  - cite_exact_filing_section_when_possible
forbidden_claims:
  - do_not_treat_stale_filings_as_current_guidance
```

```yaml
source_id: alpha_vantage
connection_status: connected_or_verify
role:
  - market_price
  - technical_market_data
  - fx
  - fundamentals_if_available
validation:
  - report_endpoint
  - report_adjusted_vs_unadjusted_price
  - report_currency
  - report_timestamp
forbidden_claims:
  - do_not_treat_vendor_fundamentals_as_more_authoritative_than_filings
  - do_not_use_technical_indicators_as_standalone_investment_conclusion
```

---

## Group B. 이번 패스에서는 문서·계약만 추가할 소스

```text
Planned / market-intelligence sources:
- KOSIS
- 관세청 customs_trade_api
- Google Trends
- Naver DataLab
- KOTRA
- G2B / 나라장터
- ECOS, 단 FRED나 기존 한국 macro source와 중복 여부 확인
```

이번 패스에서는 이 소스들에 대해:

```text
한다:
- source capability contract 작성
- validation gate 작성
- claim boundary 작성
- source router가 선택할 수 있는 문서 구조 작성
- evidence-ledger template 반영

하지 않는다:
- 실제 API client 구현
- API key 저장
- MCP 신규 설정
- credential 추가
```

---

# 4. Phase 0 — 사전 점검

Codex가 제일 먼저 해야 할 일입니다.

```text
확인할 파일:
- AGENTS.md
- README.md
- .mcp.institutional.json
- docs/harness/invest/runbook.md
- docs/harness/invest/team-spec.md
- docs/harness/invest/data-source-policy.md
- docs/harness/invest/mcp-routing.md
- docs/harness/invest/templates/
- .agents/skills/
- .agents/commands/
- .agents/policies/
- plugins/vertical-plugins/invest-research/ 존재 여부
- scripts/verify_invest_harness.py
- scripts/test_harness_structure.py
```

결정해야 할 것:

```text
1. .agents/skills가 generated layer인가?
2. canonical source가 plugins/vertical-plugins/invest-research/ 아래에 있는가?
3. sync script가 있는가?
4. 기존 MCP 연결 소스명이 무엇인가?
5. FRED / SEC EDGAR / Alpha Vantage가 어디에 등록되어 있는가?
```

원칙:

```text
canonical source가 있으면 canonical source를 수정하고 sync.
.agents가 generated layer면 직접 수정하지 않음.
확실하지 않으면 repo convention을 먼저 따른다.
```

---

# 5. Phase 1 — Research Layer 문서 추가

새 디렉터리:

```text
docs/harness/invest/research-layer/
```

추가할 파일:

```text
overview.md
question-decomposition.md
source-capability-registry.md
signal-primitives.md
validation-gates.md
claim-boundary-policy.md
ontology.md
```

---

## 5-1. `overview.md`

역할:

```text
Evidence Layer 전체 설명
기존 analyst fan-out 앞단에 추가되는 레이어임을 명시
기존 구조를 대체하지 않음
```

포함할 흐름:

```text
User Request
→ Input Gate
→ Question Decomposition
→ Evidence Planner
→ Source Capability Router
→ Evidence Ledger
→ Signal Primitives
→ Validation Gate
→ Existing Analyst Fan-out
→ Draft
→ QA
→ Final
```

---

## 5-2. `question-decomposition.md`

핵심입니다.

**절대 `product_classification`을 core로 두지 않습니다.**
대신 `subjects`를 사용합니다.

```yaml
question_decomposition:
  raw_request: string

  entities:
    companies:
      - surface_form: string
        ticker: null
        market: null
        canonical_id: null
        confidence: null

    peer_groups:
      - surface_form: string
        members: []
        confidence: null

  subjects:
    - surface_form: string
      description: string
      object_type_guess:
        - product
        - service
        - technology
        - theme
        - sector
        - commodity
        - regulation
        - macro_indicator
        - supply_chain_node
        - customer_segment
        - geography_market
        - unknown

      ontology_tags: []
      industry_classification:
        primary: null
        secondary: []
        systems:
          gics: []
          ksic: []
          sic: []
          naics: []

      candidate_source_identifiers:
        hs_codes: []
        kosis_categories: []
        naver_categories: []
        google_trends_queries: []
        kotra_keywords: []
        dart_business_segments: []

      requires_ontology_resolution: true
      mapping_confidence: null

  geographies:
    - surface_form: string
      country_or_region_code: null
      geo_type:
        - country
        - region
        - city
        - economic_bloc
        - sales_region
        - unknown

  time_horizon:
    surface_form: string
    bucket:
      - short_term
      - medium_term
      - long_term
      - unknown
    start_date: null
    end_date: null
    frequency_guess:
      - daily
      - weekly
      - monthly
      - quarterly
      - annual
      - unknown

  investment_claim_types:
    - demand_growth
    - export_momentum
    - valuation_gap
    - earnings_revision
    - regulatory_risk
    - procurement_tailwind
    - margin_change
    - supply_chain_shift
    - consumer_interest
    - competitive_position
    - macro_sensitivity
    - price_momentum
    - balance_sheet_risk
    - unknown

  required_evidence_types:
    - evidence_type:
        - company_disclosure
        - market_transaction
        - search_interest
        - export_import
        - market_context
        - macro_policy
        - price_valuation
        - procurement
        - regulatory
        - supply_chain
        - news_event
        - alternative_data
      reason: string
      priority:
        - required
        - optional
        - validation_only
      source_capabilities_needed: []
      validation_gates: []
```

명시할 금지 출력:

```yaml
forbidden:
  - use_case: cosmetics_sea_export
  - use_case: pet_ecommerce_trend
  - product: cosmetics_as_required_enum
  - product: pet_supplies_as_required_enum
```

---

## 5-3. `source-capability-registry.md`

소스를 “API 이름”이 아니라 **능력 계약**으로 정의합니다.

각 source contract 형식:

```yaml
source_id:
provider:
connection_status:
configured_in:
available_tools_or_endpoints:
evidence_types_supported:
provides:
good_for:
not_good_for:
required_inputs:
outputs:
validation_rules:
forbidden_claims:
fallback_sources:
notes:
```

반드시 포함할 소스:

```text
Existing / verify:
- yfinance-mcp
- korea-stock-mcp / DART / KRX
- FRED
- SEC EDGAR
- Alpha Vantage

Planned / contract only:
- KOSIS
- customs_trade_api
- Google Trends
- Naver DataLab
- KOTRA
- G2B procurement
- ECOS or Korean official macro source if not already covered
```

---

## 5-4. `signal-primitives.md`

제품별 use case가 아니라 범용 signal primitive만 정의합니다.

포함할 primitive:

```text
search_interest_momentum
export_momentum
transaction_market_size
procurement_demand
disclosure_exposure
market_context_signal
regulatory_risk_signal
valuation_anchor
macro_regime_signal
news_event_signal
technical_price_signal
```

각 primitive 구조:

```yaml
primitive_id:
purpose:
required_inputs:
compatible_sources:
common_metrics:
output_fields:
caveats:
claim_boundaries:
```

예:

```yaml
primitive_id: search_interest_momentum
purpose: 소비자 관심도 또는 키워드 확산 신호 감지
compatible_sources:
  - google_trends
  - naver_datalab
common_metrics:
  - latest_4w_change
  - latest_12w_change
  - regional_interest
  - rising_queries
caveats:
  - relative_index_not_absolute_volume
claim_boundaries:
  - can_support_consumer_interest_claim
  - cannot_support_market_size_or_sales_claim_alone
```

---

## 5-5. `validation-gates.md`

포함할 gate:

```text
relative_index_gate
official_statistics_gate
trade_data_gate
company_disclosure_gate
procurement_gate
market_context_gate
valuation_gate
macro_series_gate
source_conflict_gate
```

주요 금지 규칙:

```text
Google Trends:
- 시장규모 아님
- 매출 아님
- 절대 검색량 아님

관세청:
- 기업별 매출 아님
- 현지 전체 시장 규모 아님
- HS code 매핑 필요

KOTRA:
- 정성 market context
- 수출량/매출 데이터로 사용 금지

FRED:
- 거시 지표
- 개별 기업 실적 추정 직접 근거 아님

SEC EDGAR:
- 공시 기준일과 filing period 확인
- stale filing을 현재 가이던스로 쓰지 않음

Alpha Vantage:
- vendor market data
- 감사 재무제표보다 우선하지 않음
```

---

## 5-6. `claim-boundary-policy.md`

Claim별로 필요한 evidence를 정의합니다.

형식:

```yaml
claim_type:
required_evidence:
allowed_wording:
forbidden_wording:
required_caveats:
```

예:

```yaml
claim_type: consumer_interest_growth
required_evidence:
  - search_interest
allowed_wording:
  - "검색 관심도가 상승했다"
  - "소비자 관심도 프록시가 개선됐다"
forbidden_wording:
  - "매출이 증가했다"
  - "시장 규모가 커졌다"
required_caveats:
  - "검색 지수는 상대 지표이며 매출 또는 시장규모가 아니다"
```

```yaml
claim_type: export_momentum
required_evidence:
  - export_import
allowed_wording:
  - "한국발 수출 모멘텀이 개선됐다"
forbidden_wording:
  - "해당 기업의 매출이 증가했다"
required_caveats:
  - "수출 데이터는 기업별 매출이 아니라 품목/국가 단위 통관 데이터다"
```

---

## 5-7. `ontology.md`

온톨로지는 **고정 taxonomy가 아니라 후보 매핑 도우미**입니다.

```yaml
ontology_resolution_policy:
  purpose:
    - Convert user surface terms into candidate data-source identifiers.
    - Do not restrict research to known concepts.
    - If concept is unknown, preserve the original surface term.

resolution_targets:
  - aliases
  - HS codes
  - KOSIS categories
  - Naver categories
  - Google Trends queries
  - KOTRA keywords
  - DART business segment terms
  - GICS / KSIC / SIC / NAICS codes

unknown_concept_behavior:
  - keep_surface_form
  - generate_search_terms
  - mark_low_confidence_mapping
  - do_not_force_to_existing_category
  - proceed_with_best_effort_evidence_plan
```

---

# 6. Phase 2 — 템플릿 추가

경로:

```text
docs/harness/invest/templates/
```

추가 파일:

```text
evidence-plan.md
source-call-plan.md
evidence-ledger.md
signal-card.md
source-validation.md
api-call-log.md
unresolved-data-gaps.md
```

---

## 6-1. `evidence-plan.md`

포함:

```text
# Evidence Plan

## Raw Request
## Question Decomposition
## Subjects
## Entities
## Geographies
## Time Horizon
## Investment Claim Types
## Required Evidence Types
## Signal Primitives Needed
## Source Capabilities Needed
## Validation Gates
## Unresolved Ambiguities
```

---

## 6-2. `source-call-plan.md`

포함:

```text
# Source Call Plan

| Evidence Type | Candidate Source | Connection Status | Reason Selected | Required Parameters | Fallback Sources | Expected Output | Validation Checks | Limitations |
```

---

## 6-3. `evidence-ledger.md`

포함:

```text
# Evidence Ledger

| Evidence ID | Source | Source Type | Retrieved At | Period | Metric | Value | Unit | Transformation | Used By | Claim Boundary | Caveat |
```

---

## 6-4. `signal-card.md`

포함:

```text
# Signal Cards

## Signal ID
## Signal Primitive
## Subject
## Geography
## Period
## Inputs
## Calculations
## Output Signal
## Confidence
## Caveats
## Downstream Analyst Usage
```

---

## 6-5. `source-validation.md`

포함:

```text
# Source Validation

## Validation Status
## Missing Data
## Unit Checks
## Date/Freshness Checks
## Relative vs Absolute Checks
## Source Conflicts
## Forbidden Claim Checks
## Unresolved Data Gaps
```

---

## 6-6. `api-call-log.md`

이번 패스에서 실제 API client를 구현하지 않아도 로그 형식은 정의합니다.

```text
# API Call Log

| Source | Tool/Endpoint | Parameters | Timestamp | Success/Failure | Response Summary | Cache Path | Error |
```

---

# 7. Phase 3 — Workspace 구조 확장

새 workspace 구조:

```text
_workspace_{ticker_or_slug}_{yyyymmdd}/
├─ 00_input/
│  ├─ input-intake.md
│  ├─ request-summary.md
│  └─ market-price-snapshot.md
│
├─ 00_evidence/
│  ├─ question-decomposition.md
│  ├─ evidence-plan.md
│  ├─ source-call-plan.md
│  ├─ evidence-ledger.md
│  ├─ signal-cards.md
│  ├─ source-validation.md
│  ├─ api-call-log.md
│  └─ unresolved-data-gaps.md
│
├─ 01_financial/
├─ 02_fundamental/
├─ 03_valuation/
├─ 04_technical/
├─ 05_macro_sentiment/
├─ 06_risk_scenario/
├─ 07_draft/
├─ 09_qa/
└─ 08_final/
```

기존 경로는 유지합니다.

```text
삭제 금지:
- 00_input
- 01_financial
- 02_fundamental
- 03_valuation
- 04_technical
- 05_macro_sentiment
- 06_risk_scenario
- 07_draft
- 09_qa
- 08_final
```

---

# 8. Phase 4 — Runbook / Team Spec 수정

수정 대상:

```text
docs/harness/invest/runbook.md
docs/harness/invest/team-spec.md
```

새 흐름:

```text
0. Input gate
1. Request summary
2. Evidence planning
3. Source call planning
4. Evidence ledger + signal cards
5. Validation gates
6. Existing analyst fan-out
7. Draft synthesis
8. QA + source/claim audit
9. Final report
```

중요 문구:

```text
Analysts must read 00_evidence outputs when available.
Analysts must not overclaim beyond the evidence ledger.
QA must verify that final report claims respect source claim boundaries.
```

---

# 9. Phase 5 — Skills 추가/수정

먼저 canonical source 확인:

```text
if plugins/vertical-plugins/invest-research exists:
  edit there
  run sync script
else:
  follow existing .agents convention
```

---

## 9-1. 신규 skill: `evidence-planner`

역할:

```text
사용자 요청을 open-ended question decomposition으로 분해
evidence-plan 작성
절대 fixed use_case name을 출력하지 않음
```

출력:

```text
00_evidence/question-decomposition.md
00_evidence/evidence-plan.md
```

금지:

```yaml
forbidden_outputs:
  - use_case: cosmetics_sea_export
  - use_case: pet_ecommerce_trend
  - product_enum: cosmetics
  - product_enum: pet_supplies
```

필수 출력:

```yaml
required_outputs:
  - subjects
  - entities
  - geographies
  - investment_claim_types
  - required_evidence_types
  - signal_primitives_needed
  - validation_gates
```

---

## 9-2. 신규 skill: `source-router`

역할:

```text
evidence-plan을 읽고 source capability 기준으로 source 선택
기존 연결 소스는 재사용
신규 API client 구현하지 않음
```

출력:

```text
00_evidence/source-call-plan.md
```

필수 구분:

```yaml
source_connection_status:
  - connected
  - connected_but_tool_contract_needs_confirmation
  - documented_only
  - planned
  - external_manual
```

---

## 9-3. 선택 skill: `signal-analyst`

처음부터 무리하게 구현하지 않아도 됩니다.
문서/템플릿만 추가하고 다음 패스로 미뤄도 됩니다.

역할:

```text
evidence-ledger를 읽고 signal-card 생성
signal primitive 기반으로만 작성
use case 기반 작성 금지
```

출력:

```text
00_evidence/signal-cards.md
```

---

## 9-4. `invest-orchestrator` 수정

추가 책임:

```text
- 외부 evidence가 필요한 요청이면 00_evidence 생성을 먼저 지시
- analyst fan-out 전에 evidence-plan/source-call-plan 존재 확인
- analyst들에게 evidence-ledger/signal-cards를 참고하도록 지시
```

---

## 9-5. `qa-reviewer` 수정

추가 책임:

```text
- source/claim consistency 검토
- Google Trends/Naver DataLab 상대지수 오용 확인
- 관세청 데이터의 기업 매출 오용 확인
- KOTRA 텍스트의 수치 데이터 오용 확인
- FRED 거시지표를 개별기업 실적 근거로 쓰는 오류 확인
- SEC EDGAR filing date/period 확인
- Alpha Vantage vendor data claim boundary 확인
```

---

# 10. Phase 6 — Commands 추가

기존 command runtime이 얇은 wrapper라면 동일하게 유지합니다.
실제 API 실행을 command에 넣지 않습니다.

추가 후보:

```text
.agents/commands/evidence.md
.agents/commands/market-intel.md
.agents/commands/source-audit.md
```

역할:

```text
/evidence
→ evidence-planner 실행

/market-intel
→ evidence-planner + source-router + optional signal-analyst 실행

/source-audit
→ qa-reviewer 또는 source-claim audit 실행
```

금지:

```text
command stub에서 실제 API client 구현 금지
credential 처리 금지
중복 connector 구현 금지
```

---

# 11. Phase 7 — Golden Scenarios 추가

경로:

```text
docs/harness/invest/evals/golden-scenarios/
```

추가 파일:

```text
pet-ecommerce-trend.md
cosmetics-sea-export.md
unseen-market-object.md
google-trends-claim-boundary.md
fred-macro-regime.md
sec-edgar-company-disclosure.md
alpha-vantage-market-data-boundary.md
```

중요:
여기 있는 use case는 **router category가 아니라 테스트 fixture**입니다.

---

## 11-1. `pet-ecommerce-trend.md`

목적:

```text
국내 반려동물 이커머스 질문을 fixed use case가 아니라 evidence type으로 분해하는지 검증
```

기대 evidence:

```text
- search_interest
- market_transaction
- optional admin/pet population proxy
- validation: search index is not market size
```

---

## 11-2. `cosmetics-sea-export.md`

기대 evidence:

```text
- search_interest
- export_import
- market_context
- company_disclosure
```

금지:

```text
use_case: cosmetics_sea_export
```

---

## 11-3. `unseen-market-object.md`

입력:

```text
인도네시아 니켈 수출 제한이 한국 배터리 소재주에 미치는 영향 분석해줘.
```

기대 분해:

```yaml
subjects:
  - 니켈
  - 수출 제한
  - 한국 배터리 소재주

geographies:
  - Indonesia
  - Korea

required_evidence_types:
  - regulatory
  - supply_chain
  - export_import
  - company_disclosure
  - price_valuation
```

검증 목적:

```text
cosmetics/pet/power 같은 기존 예시에 억지 매핑하지 않는지 확인
```

---

## 11-4. `google-trends-claim-boundary.md`

검증:

```text
Google Trends = relative search interest
시장규모/매출/판매량으로 오용 금지
```

---

## 11-5. `fred-macro-regime.md`

검증:

```text
FRED macro series를 valuation discount-rate, inflation, employment, liquidity context로 사용
개별 기업 실적 직접 근거로 오용 금지
```

---

## 11-6. `sec-edgar-company-disclosure.md`

검증:

```text
SEC filing type, filing date, fiscal period를 표시
stale filing을 현재 guidance로 오용하지 않음
```

---

## 11-7. `alpha-vantage-market-data-boundary.md`

검증:

```text
Alpha Vantage 가격/기술지표/벤더 데이터의 한계 표시
감사 재무제표보다 우선하지 않음
```

---

# 12. Phase 8 — 테스트 추가

경로:

```text
scripts/
```

추가 테스트:

```text
test_evidence_layer_structure.py
test_no_fixed_product_taxonomy.py
test_signal_primitives.py
test_source_capability_registry.py
test_claim_boundary_policy.py
test_workspace_evidence_contracts.py
test_existing_connected_sources_not_duplicated.py
```

---

## 12-1. `test_evidence_layer_structure.py`

확인:

```text
research-layer docs 존재 여부
templates 존재 여부
evals/golden-scenarios 존재 여부
```

---

## 12-2. `test_no_fixed_product_taxonomy.py`

목적:

```text
core docs에 fixed product/use-case router enum이 생기는 것 방지
```

금지어 예시:

```python
FORBIDDEN_CORE_PRODUCT_ENUMS = [
    "cosmetics",
    "pet_supplies",
    "semiconductors",
    "power_equipment",
    "defense",
    "k_food",
]
```

단, 허용 위치:

```text
docs/harness/invest/evals/
examples/
clearly marked example sections
```

---

## 12-3. `test_signal_primitives.py`

확인:

```text
signal-primitives.md에 generic primitive 존재
각 primitive에 purpose, required_inputs, compatible_sources, caveats, claim_boundaries 존재
```

---

## 12-4. `test_source_capability_registry.py`

확인:

```text
각 source contract에 아래 항목 존재:
- provides
- good_for
- not_good_for
- required_inputs
- outputs
- validation_rules
- forbidden_claims
- connection_status
```

---

## 12-5. `test_claim_boundary_policy.py`

확인:

```text
필수 금지 claim 존재:
- Google Trends is not market size
- Search interest is not sales
- Customs trade is not company revenue
- KOTRA text is not export volume
- FRED macro series is not company fundamentals
- Alpha Vantage vendor data is not audited filing
```

---

## 12-6. `test_workspace_evidence_contracts.py`

확인:

```text
00_evidence 템플릿 필드 존재
```

---

## 12-7. `test_existing_connected_sources_not_duplicated.py`

목적:

```text
FRED / SEC EDGAR / Alpha Vantage / yfinance / DART-KRX에 대해
새 connector/client를 중복 생성하지 않았는지 확인
```

검사:

```text
- 새 API key 파일 추가 여부
- 새 credentials 파일 추가 여부
- 중복 connector 디렉터리 추가 여부
- .mcp.institutional.json 불필요 수정 여부
```

---

# 13. Phase 9 — `verify_invest_harness.py` 확장

기존 검증은 유지하고 새 테스트를 추가합니다.

예상 구조:

```python
CHECKS = [
    ("Check generated-layer drift", ...),
    ("Check workspace safety", ...),
    ("Check harness structure", ...),

    # NEW
    ("Check evidence layer structure", ...),
    ("Check no fixed product taxonomy", ...),
    ("Check signal primitives", ...),
    ("Check source capability registry", ...),
    ("Check claim boundary policy", ...),
    ("Check workspace evidence contracts", ...),
    ("Check existing connected sources not duplicated", ...),
]
```

실행:

```bash
python3 scripts/verify_invest_harness.py
```

---

# 14. Phase 10 — README / AGENTS 업데이트

가볍게만 수정합니다.

## README 추가 내용

```text
- Evidence Planning Layer 소개
- 00_evidence workspace 설명
- source capability 기반 routing 설명
- use case는 eval fixture이지 core router가 아님
- 기존 analyst fan-out은 유지됨
```

## AGENTS 추가 내용

```text
- 외부 데이터가 필요한 요청은 먼저 evidence planning 수행
- 기존 connected source는 중복 연동하지 않음
- source claim boundary 준수
- fixed product taxonomy 금지
```

---

# 15. Codex 실행 순서

Codex에는 이 순서로 지시하는 게 좋습니다.

```text
1. repo 구조와 MCP 설정 탐지
2. 기존 연결 소스 목록 작성
3. research-layer docs 추가
4. templates 추가
5. runbook/team-spec 업데이트
6. skill source 위치 확인
7. evidence-planner/source-router skill 추가 또는 canonical source에 반영
8. qa-reviewer/invest-orchestrator 업데이트
9. golden scenarios 추가
10. tests 추가
11. verify_invest_harness.py 업데이트
12. 검증 실행
13. 변경 파일 요약
```

---

# 16. 이번 패스의 Non-goals

```text
하지 않는다:
- 실제 KOSIS API client 구현
- 실제 관세청 API client 구현
- Google Trends client 구현
- Naver DataLab client 구현
- KOTRA client 구현
- G2B client 구현
- API key 추가
- credential 저장
- FRED/SEC EDGAR/Alpha Vantage 중복 연동
- 기존 analyst 구조 전면 교체
- use case hard router 구현
```

이번 패스는:

```text
문서
계약
템플릿
스킬 지침
검증 테스트
라우팅 원칙
claim boundary
```

까지만 구현하는 것이 적절합니다.

---

# 17. 최종 Acceptance Criteria

완료 조건:

```text
1. 기존 검증이 깨지지 않는다.
2. python3 scripts/verify_invest_harness.py 통과.
3. 00_evidence workspace 구조가 문서화되어 있다.
4. evidence-plan/source-call-plan/evidence-ledger/signal-card 템플릿이 있다.
5. question decomposition이 subject 기반 open-ended 구조다.
6. core docs에 fixed product taxonomy가 없다.
7. use case 예시는 eval/golden-scenarios에만 있다.
8. source routing은 evidence type + source capability 기반이다.
9. 기존 연결 소스는 중복 구현하지 않았다.
10. FRED / SEC EDGAR / Alpha Vantage는 connected source contract로 편입되어 있다.
11. Google Trends / Naver DataLab / KOSIS / 관세청 / KOTRA / G2B는 docs-only planned source로 정의되어 있다.
12. QA가 source claim boundary를 검토하도록 업데이트되어 있다.
13. README/AGENTS가 새 evidence layer를 간결하게 설명한다.
```

---

# 18. Codex용 최종 축약 프롬프트

Codex에 줄 때는 이 핵심을 맨 위에 붙이는 게 좋습니다.

```text
Implement a minimal, reviewable documentation-and-contract PR for a generic Evidence Planning Layer in invest_harness.

Do not rewrite the existing analyst workflow.
Do not hard-code product/use-case categories.
Do not reconnect FRED, SEC EDGAR, Alpha Vantage, yfinance, or DART/KRX.
Discover existing connected sources and wrap them in source capability contracts.
Add 00_evidence workspace contracts, source routing docs, signal primitives, validation gates, claim-boundary policy, templates, golden scenarios, and tests.
Use cases are eval fixtures only, not router categories.
```

---

# 결론

이번 구현의 핵심은 **API를 더 많이 붙이는 것**이 아닙니다.

정확한 목표는 이것입니다.

```text
기존 연결 API:
FRED / SEC EDGAR / Alpha Vantage / yfinance / DART-KRX
→ source capability registry에 편입

신규 시장 인텔리전스 후보:
KOSIS / 관세청 / Google Trends / Naver DataLab / KOTRA / G2B
→ 이번 패스에서는 docs-only contract로 추가

전체 harness:
질문 → evidence plan → source routing → signal primitive → validation → analyst report
```

한 줄로 정리하면:

> **기존 invest_harness를 “리포트 작성 harness”에서 “증거 설계 후 리포트를 작성하는 범용 투자 리서치 harness”로 확장하는 계획입니다.**
