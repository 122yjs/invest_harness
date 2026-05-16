# Evidence Layer 구현 체크리스트 (완료)

> **Goal:** invest_harness에 **Evidence Planning / Source Routing / Signal Primitive** 레이어를 추가한다.
> 기존 fan-out/fan-in 분석 워크플로우를 보존하면서, 분석 전 단계에 범용 증거 계획 계층을 삽입한다.

> [!IMPORTANT]
> **핵심 설계 원칙:** 이것은 **범용(General-Purpose)** 투자 하네스다.
> 화장품, 반도체, 방산 등 특정 상품/유즈케이스를 라우터 카테고리나 enum으로 하드코딩하지 않는다.
> 코어는 오픈엔디드 질문 분해 + 소스 능력 레지스트리 + 증거 유형 + 시그널 프리미티브 + 검증 게이트 + 클레임 경계 정책으로 구성한다.

- **관련 저장소:** `https://github.com/122yjs/invest_harness`
- **선행 작업:** [01_mvp_improvement_archive.md](01_mvp_improvement_archive.md) — 모든 항목 완료됨
- **완료 커밋:** `1af047d` → `e8710b9` (총 8개 커밋, 39개 파일 변경, +1873 라인)
- **완료 커밋:** `1af047d` → `e8710b9` (총 8개 커밋, 39개 파일 변경, +1873 라인)

---

## 사전 읽기 자료

작업 시작 전 아래 문서를 먼저 확인한다:

- [ ] `AGENTS.md`
- [ ] `README.md`
- [ ] `docs/harness/invest/runbook.md`
- [ ] `docs/harness/invest/team-spec.md`
- [ ] `docs/harness/invest/data-source-policy.md` (있으면)
- [ ] `docs/harness/invest/mcp-routing.md` (있으면)
- [ ] `docs/harness/invest/templates/`
- [ ] `scripts/verify_invest_harness.py`
- [ ] `scripts/test_harness_structure.py`

---

## Phase 1: Documentation Layer

> 디렉토리: `docs/harness/invest/research-layer/`

### 1-0. 디렉토리 생성

- [x] `docs/harness/invest/research-layer/` 생성 (없으면) — *d02b7cb*

### 1-1. `overview.md` — Evidence Layer 전체 흐름

- [x] 파일 생성: `docs/harness/invest/research-layer/overview.md` — *d02b7cb*
- [x] 아래 파이프라인 흐름을 설명:
  - User Request → Input Gate → Question Decomposition → Evidence Planner → Source Capability Router → Evidence Ledger → Signal Primitives → Validation Gate → **기존 Analyst Fan-out** → Draft → QA → Final
- [x] 이 레이어가 기존 분석 역할을 대체하지 않고 **선행**함을 명시

### 1-2. `question-decomposition.md` — 오픈엔디드 질문 분해 스키마

- [x] 파일 생성: `docs/harness/invest/research-layer/question-decomposition.md` — *d02b7cb*
- [x] 스키마 포함: `question_decomposition` (entities, subjects, geographies, time_horizon, investment_claim_types, required_evidence_types)
- [x] `subjects`가 코어 — `product_classification` 아님을 명시
- [x] 아래 정책 명시:

| 정책 키 | 값 |
|---|---|
| `no_fixed_product_taxonomy` | `true` |
| `no_use_case_hard_routing` | `true` |
| `preserve_user_surface_terms` | `true` |
| `allow_unseen_market_objects` | `true` |
| `use_ontology_for_candidate_mapping_only` | `true` |
| `source_selection_based_on_evidence_need` | `true` |
| `signal_selection_based_on_claim_type_and_evidence_type` | `true` |

- [x] 제약 명시:
  - subjects = 사용자 요청에서 추출한 오픈엔디드 객체
  - ontology_tags, industry_classification = 매핑 보조 용도만
  - candidate_source_identifiers = 선택적 후보, 강제 카테고리 아님
  - 매핑 불확실 시 surface_form 보존 + mapping_confidence 낮게 표기
  - 모르는 개념을 가장 가까운 기존 예시에 억지로 끼워넣지 않음

### 1-3. `source-capability-registry.md` — 소스 능력 계약

- [x] 파일 생성: `docs/harness/invest/research-layer/source-capability-registry.md` — *d02b7cb*
- [x] 아래 소스에 대해 각각 계약 정의:
  - [x] Group A: repo evidence 기준 connected 또는 문서화된 source
  - [x] DART-KRX / korea-stock
  - [x] yfinance
  - [x] FRED
  - [x] SEC EDGAR
  - [x] Alpha Vantage
  - [x] Group B: 신규 시장 인텔리전스/docs-only 후보
  - [x] KOSIS
  - [x] customs_trade_api
  - [x] Google Trends
  - [x] Naver DataLab
  - [x] KOTRA
  - [x] G2B / public procurement
  - [x] 보존 source: FMP, ECOS / macro official statistics
- [x] 각 소스에 포함할 항목:
  - `source_id` / `provider` / `connection_status` / `configured_in` / `available_tools_or_endpoints` / `evidence_types_supported`
  - `good_for` / `not_good_for` / `required_inputs` / `outputs` / `validation_rules` / `forbidden_claims` / `fallback_sources` / `notes`
- [x] 예시 계약 포함:
  - Google Trends: `provides` = relative_search_interest 등, `not_good_for` = absolute_market_size 등
  - Customs Trade: `provides` = item/country export-import value 등, `not_good_for` = company_specific_sales 등
  - KOSIS: `provides` = official statistics 등, `not_good_for` = real-time granular SKU demand 등

### 1-4. `signal-primitives.md` — 재사용 시그널 프리미티브

- [x] 파일 생성: `docs/harness/invest/research-layer/signal-primitives.md` — *d02b7cb*
- [x] 아래 프리미티브 정의:
  - [x] `search_interest_momentum`
  - [x] `export_momentum`
  - [x] `transaction_market_size`
  - [x] `procurement_demand`
  - [x] `disclosure_exposure`
  - [x] `market_context_signal`
  - [x] `regulatory_risk_signal`
  - [x] `valuation_anchor`
  - [x] `macro_regime_signal`
  - [x] `news_event_signal`
- [x] 각 프리미티브에 포함할 항목:
  - `purpose` / `required_inputs` / `compatible_sources` / `common_metrics` / `output fields` / `caveats` / `claim boundaries`
- [x] 상품별 유즈케이스를 프리미티브로 정의하지 않음을 명시

### 1-5. `validation-gates.md` — 증거/소스별 검증 게이트

- [x] 파일 생성: `docs/harness/invest/research-layer/validation-gates.md` — *d02b7cb*
- [x] 아래 게이트 정의:
  - [x] `relative_index_gate`
  - [x] `official_statistics_gate`
  - [x] `trade_data_gate`
  - [x] `company_disclosure_gate`
  - [x] `procurement_gate`
  - [x] `market_context_gate`
  - [x] `valuation_gate`
  - [x] `source_conflict_gate`
- [x] 명시적 금지 사항 포함:
  - [x] ❌ Google Trends 단독으로 매출 추론
  - [x] ❌ 상대적 검색 관심도를 시장 규모로 추론
  - [x] ❌ 관세 무역 데이터 단독으로 기업별 매출 추론
  - [x] ❌ KOTRA 텍스트/뉴스를 수출 물량으로 취급
  - [x] ❌ 공공조달을 전체 시장 수요로 취급
  - [x] ❌ 충돌하는 소스를 충돌 설명 없이 평균

### 1-6. `claim-boundary-policy.md` — 클레임 경계 정책

- [x] 파일 생성: `docs/harness/invest/research-layer/claim-boundary-policy.md` — *d02b7cb*
- [x] 구조: `claim` / `required evidence` / `allowed wording` / `forbidden wording` / `required caveats`
- [x] 예시 포함:
  - [x] **Consumer interest claim** → requires `search_interest` evidence. 거래/수출/기업 증거 없이 매출 성장 주장 불가
  - [x] **Export momentum claim** → requires `export_import` evidence. 기업 공시/세그먼트 노출 증거 없이 기업 매출 성장 주장 불가

### 1-7. `ontology.md` — 후보 매핑용 온톨로지

- [x] 파일 생성: `docs/harness/invest/research-layer/ontology.md` — *d02b7cb*
- [x] 고정 분류체계가 아닌 **후보 매핑**임을 명시
- [x] 자유텍스트 subjects → 후보 식별자 매핑:
  - aliases / HS codes / KOSIS categories / Naver categories / Google Trends queries / KOTRA keywords / DART business segment terms / GICS·KSIC·SIC·NAICS codes
- [x] `unknown_concept_behavior` 정의:
  - `keep_surface_form`
  - `generate_search_terms`
  - `mark_low_confidence_mapping`
  - `do_not_force_to_existing_category`
  - `proceed_with_best_effort_evidence_plan`

---

## Phase 2: Templates

> 디렉토리: `docs/harness/invest/templates/`

### 2-1. `evidence-plan.md`

- [x] 파일 생성 — *24c79a1*
- [x] 포함 항목: raw request / question decomposition / required evidence types / source capability needs / signal primitives needed / validation gates / unresolved ambiguities

### 2-2. `source-call-plan.md`

- [x] 파일 생성 — *24c79a1*
- [x] 포함 항목: evidence type / candidate source / reason selected / required parameters / fallback sources / expected output / validation checks / source limitations

### 2-3. `evidence-ledger.md`

- [x] 파일 생성 — *24c79a1*
- [x] 테이블 포함:

| Evidence ID | Source | Source Type | Retrieved At | Period | Metric | Value | Unit | Transformation | Used By | Claim Boundary | Caveat |
|---|---|---|---|---|---|---|---|---|---|---|---|

### 2-4. `signal-card.md`

- [x] 파일 생성 — *24c79a1*
- [x] 포함 항목: signal id / signal primitive / subject / geography / period / inputs / calculations / output signal / confidence / caveats / downstream analyst usage

### 2-5. `source-validation.md`

- [x] 파일 생성 — *24c79a1*
- [x] 포함 항목: validation status / missing data / unit/date checks / source conflicts / relative vs absolute checks / forbidden claim checks / unresolved data gaps

### 2-6. `api-call-log.md`

- [x] 파일 생성 (API 미구현이더라도 로그 템플릿 정의) — *24c79a1*
- [x] 포함 항목: source / endpoint·tool / parameters / timestamp / success·failure / response summary / cache path (있으면) / error (있으면)

---

## Phase 3: Workspace / Runbook 통합

### 3-1. Runbook · Team-spec 워크플로우 업데이트

- [x] `docs/harness/invest/runbook.md` 업데이트 — *24c79a1*
- [x] `docs/harness/invest/team-spec.md` 업데이트 — *24c79a1*
- [x] 워크플로우를 아래 순서로 변경:

| 단계 | 설명 |
|---|---|
| 0 | Input gate |
| 1 | Input summary |
| 2 | Evidence planning |
| 3 | Source call planning |
| 4 | Evidence ledger + signal cards |
| 5 | Validation gates |
| 6 | 기존 analyst fan-out |
| 7 | Draft synthesis |
| 8 | QA + source/claim audit |
| 9 | Final report |

### 3-2. `00_evidence/` Workspace 섹션 추가

- [x] 아래 구조 정의 및 문서화: — *24c79a1*

```
${ACTIVE_WORKSPACE}/00_evidence/
  question-decomposition.md
  evidence-plan.md
  source-call-plan.md
  evidence-ledger.md
  signal-cards.md
  source-validation.md
  api-call-log.md
  unresolved-data-gaps.md
```

### 3-3. 기존 Workspace 호환성 확인

- [x] 아래 기존 디렉토리 삭제/변경 없음 확인: — *24c79a1*
  - `00_input/` / `01_financial/` / `02_fundamental/` / `03_valuation/` / `04_technical/` / `05_macro_sentiment/` / `06_risk_scenario/` / `07_draft/` / `09_qa/` / `08_final/`
- [x] 기존 analyst 산출물이 호환됨을 검증

---

## Phase 4: Skills / Agent 지침

### 4-0. 사전 확인

- [x] 현재 skill 구조 확인: canonical source가 `.agents/skills/`인지, 다른 곳에서 생성되는지 파악 — *04334f1*
- [x] canonical source가 아닌 곳을 직접 수정하지 않도록 주의

### 4-1. `evidence-planner` Skill 추가/업데이트

- [x] Skill 생성 — *04334f1*
- [x] 기능: 사용자 요청 → 오픈엔디드 question decomposition 파싱
- [x] 산출물: `00_evidence/question-decomposition.md`, `00_evidence/evidence-plan.md`
- [x] **금지:** `use_case: cosmetics_sea_export`, `use_case: pet_ecommerce_trend` 같은 코어 라우팅 출력
- [x] **필수 출력:** `required_evidence_types`, `signal_primitives_needed`

### 4-2. `source-router` Skill 추가/업데이트

- [x] Skill 생성 — *04334f1*
- [x] 기능: `evidence-plan.md` 읽고 → 능력 기반으로 소스 선택 (고정 유즈케이스 기반 아님)
- [x] 산출물: `source-call-plan.md`
- [x] 각 소스 선택 이유, 폴백 소스, 한계 포함

### 4-3. `signal-analyst` Skill (선택적)

- [x] 경량 추가 가능 시 Skill 생성 — *04334f1*
- [x] 기능: `evidence-ledger.md` 읽고 → `signal-cards.md` 생성
- [x] 시그널 프리미티브 사용, 상품 유즈케이스 사용 안 함

### 4-4. `invest-orchestrator` 업데이트

- [x] 사용자 요청이 일반 기업 재무 이상의 외부 증거가 필요할 때 `00_evidence`를 생성/요구 — *04334f1*
- [x] `evidence-ledger`와 `signal-cards`를 analysts에게 전달
- [x] 기존 input gate 동작 보존

### 4-5. `qa-reviewer` 업데이트

- [x] source/claim 일관성 검사 추가 — *04334f1*
- [x] Google Trends, Naver DataLab, KOTRA, KOSIS, customs, procurement, DART 증거의 과대주장 검사
- [x] 최종 리포트에서 상대적 검색 관심도를 시장 규모/매출로 사용하지 않는지 검사

---

## Phase 5: Commands

> 기존 command 스타일과 일관되게 유지. 무거운 API 실행은 구현하지 않음.

### 5-1. Command 추가

- [x] `evidence.md` — `evidence-planner`로 dispatch — *04334f1*
- [x] `market-intel.md` — `evidence-planner` + `source-router` + (선택) `signal-analyst`로 dispatch — *04334f1*
- [x] `source-audit.md` — `qa-reviewer` 또는 data/source audit 로직으로 dispatch — *04334f1*

### 5-2. Command 원칙

- [x] Command runtime은 파싱/dispatch + handoff metadata 기록만 수행 — *04334f1*
- [x] 전체 분석을 command 자체에서 수행하지 않음

---

## Phase 6: Evals / Golden Scenarios

> 디렉토리: `docs/harness/invest/evals/golden-scenarios/`
> 이들은 **eval 픽스처**이며 라우터 카테고리가 아님.

### 6-1. `pet-ecommerce-trend.md`

- [x] 파일 생성 — *59b0a07*
- [x] 검증: planner가 국내 펫 이커머스 트렌드 질문을 아래로 분해하는지:
  - surface form에서 subjects 추출
  - `search_interest` / `market_transaction` / optional pet population proxy
  - 검색 지수 ≠ 시장 규모 검증

### 6-2. `cosmetics-sea-export.md`

- [x] 파일 생성 — *59b0a07*
- [x] 검증: K-beauty 동남아 질문을 아래로 분해하는지:
  - `search_interest` / `export_import` / `market_context` / `company_disclosure`
  - 고정 `use_case` 라우팅 없음

### 6-3. `unseen-market-object.md`

- [x] 파일 생성 — *59b0a07*
- [x] 입력: `"인도네시아 니켈 수출 제한이 한국 배터리 소재주에 미치는 영향 분석해줘."`
- [x] 기대 분해:
  - subjects: 니켈, 수출 제한, 한국 배터리 소재주
  - geographies: Indonesia, Korea
  - evidence types: regulatory, supply_chain, export_import, company_disclosure, price_valuation
  - 화장품/펫/전력 등에 강제 매핑 없음

### 6-4. `google-trends-claim-boundary.md`

- [x] 파일 생성 — *59b0a07*
- [x] 검증: Google Trends가 상대적 검색 관심도로만 취급되는지

---

## Phase 7: Tests

> Python 테스트. PowerShell 전용 검증은 피한다 (Linux/macOS 호환).

### 7-1. `test_evidence_layer_structure.py`

- [x] 파일 생성 — *e6b13f8*
- [x] 검사: 필수 docs/templates/evals 존재 여부

### 7-2. `test_no_fixed_product_taxonomy.py`

- [x] 파일 생성 — *e6b13f8*
- [x] 검사: 코어 research-layer 문서에 고정 상품/유즈케이스 카테고리가 필수 라우터 enum으로 정의되지 않음
  - 금지 키워드: cosmetics, pet_supplies, semiconductors, power_equipment, defense, k_food (필수 라우터 enum 값으로)
  - 허용: evals/golden-scenarios 또는 명시적 예시에서만

### 7-3. `test_signal_primitives.py`

- [x] 파일 생성 — *e6b13f8*
- [x] 검사: `signal-primitives.md`에 범용 프리미티브와 필수 섹션 포함

### 7-4. `test_source_capability_registry.py`

- [x] 파일 생성 — *e6b13f8*
- [x] 검사: 각 소스 계약에 `provides` / `good_for` / `not_good_for` / `validation_rules` / `forbidden_claims` 포함

### 7-5. `test_claim_boundary_policy.py`

- [x] 파일 생성 — *e6b13f8*
- [x] 검사: `claim-boundary-policy.md`에 아래 금지 사항 포함:
  - [x] Google Trends ≠ 시장 규모
  - [x] 검색 관심도 ≠ 매출
  - [x] 관세 무역 ≠ 기업 매출
  - [x] KOTRA 텍스트 ≠ 수출 물량

### 7-6. `test_workspace_evidence_contracts.py`

- [x] 파일 생성 — *e6b13f8*
- [x] 검사: `00_evidence` 산출물 템플릿에 필수 heading/field 포함

### 7-7. 기존 검증 스크립트 통합

- [x] `scripts/verify_invest_harness.py` 업데이트 — 위 테스트 포함 — *e6b13f8*
- [x] 기존 테스트 보존

---

## Phase 8: README / AGENTS 업데이트

- [x] `README.md` 경량 업데이트: — *24c79a1*
  - [x] Evidence Layer 언급
  - [x] `00_evidence` workspace 언급
  - [x] 소스 선택이 능력 기반임을 언급
  - [x] 유즈케이스 예시는 비포괄적 eval 픽스처임을 언급
  - [x] 기존 투자 면책 조항 보존
  - [x] 과도한 확장 금지 — research-layer docs로 링크
- [x] `AGENTS.md` 경량 업데이트: — *24c79a1*
  - [x] 동일한 변경 사항 반영

---

## Non-Goals

> [!WARNING]
> 이 작업의 범위에서 **명시적으로 제외**된 항목:

- ❌ 실제 API 클라이언트 구현
- ❌ API 키 저장
- ❌ 데이터베이스 구축
- ❌ 하드코딩된 유즈케이스 분류기 생성
- ❌ 기존 analyst skill 대체
- ❌ 모든 리서치를 Google Trends/KOSIS/Customs 경유 강제
- ❌ 단일 대안 데이터 시그널로 투자 추천 추론

---

## Acceptance Criteria

> [!IMPORTANT]
> 아래 10개 기준을 모두 충족해야 완료:

- [ ] **AC-1:** 기존 검증 스크립트가 여전히 통과한다
- [ ] **AC-2:** 새 검증 테스트가 `python3 scripts/verify_invest_harness.py`로 통과한다
- [ ] **AC-3:** 기존 workspace 구조가 하위 호환된다
- [ ] **AC-4:** 새 `00_evidence` 구조가 문서화·템플릿화되었다
- [ ] **AC-5:** 코어 planner 문서가 오픈엔디드 subjects를 사용한다 (고정 상품 카테고리 아님)
- [ ] **AC-6:** 소스 라우팅이 증거 유형 + 소스 능력 기반이다
- [ ] **AC-7:** Golden scenario가 `evals/` 아래에만 위치한다
- [ ] **AC-8:** QA 정책에 클레임 경계 검사가 포함된다
- [ ] **AC-9:** 어떤 소스도 증거 경계를 넘어 시장 규모/매출/매출을 주장하지 않는다
- [ ] **AC-10:** 구현이 Markdown-first이며 기존 하네스 스타일과 일관된다

---

## 완료 후 확인 사항

- [ ] 변경된 파일 목록 정리
- [ ] 새 흐름을 5~8개 bullet으로 설명
- [ ] 검증 명령어 출력 확인
- [ ] 실행 불가 테스트가 있으면 사유와 미검증 항목 설명

---

## 추가 구현 패스: Source Capability Connection Status

> 목적: 기존/문서화/예정/수동 source를 같은 registry 계약으로 표현하고, source-router가 callable 여부를 과대해석하지 않도록 검증한다.

### Non-goals

- [x] 이미 MCP/API/config로 제공되는 source에 중복 API client를 구현하지 않는다.
- [x] 새 credentials를 추가하지 않는다.
- [x] `.mcp.institutional.json`은 기본적으로 수정하지 않으며, 이번 패스에서는 `enabled: false`와 빈 `mcpServers`를 유지한다.
- [x] 기존 FRED / SEC EDGAR / Alpha Vantage / yfinance / DART-KRX 연결 또는 문서화 상태를 대체하지 않는다.
- [x] KOSIS, customs_trade_api, Google Trends, Naver DataLab, KOTRA, G2B의 runtime API client는 이번 패스에서 만들지 않는다.
- [x] 이번 패스는 documentation, contracts, templates, validation tests first로 제한한다.

- [x] 기존 또는 repo-evidence source를 Group A로 정리: FRED, SEC EDGAR, Alpha Vantage, yfinance, DART-KRX/korea-stock
- [x] 신규 시장 인텔리전스 후보를 docs-only Group B로 정리: KOSIS, customs, Google Trends, Naver DataLab, KOTRA, G2B
- [x] FMP와 ECOS 기존 계약을 보존
- [x] `connection_status` enum 정의: `connected`, `documented_only`, `planned`, `external_manual`
- [x] `connection_status`가 repo-evidence status이며 live runtime proof가 아님을 명시
- [x] 각 source section에 `source_id`, `provider`, `connection_status`, `configured_in`, `available_tools_or_endpoints`, `evidence_types_supported`, `fallback_sources`, `notes` 등을 추가
- [x] source-router가 unavailable source를 data gap으로 기록하도록 지침 업데이트
- [x] source-call-plan, source-validation, api-call-log 템플릿에 source status/tool/gap 필드 추가
- [x] `scripts/test_source_capability_registry.py`를 per-source section validator로 강화
- [x] RED 확인: 강화된 validator가 기존 registry의 누락 필드와 status semantic 누락을 실패로 보고함
- [x] GREEN 확인: registry/templates/router 업데이트 후 `python3 scripts/test_source_capability_registry.py` 통과

### Web Search + Web Fetch 보강

- [x] Web Search를 evidence source가 아니라 candidate URL discovery 단계로 정의
- [x] Search snippet만 있는 경우 Web Fetch/browser/PDF reader로 URL 본문을 읽도록 source-router 규칙 추가
- [x] 기사, 문서, PDF 본문을 fetch/read한 경우에만 evidence로 사용할 수 있도록 validation template 추가
- [x] body fetch 실패 시 snippet으로 대체하지 않고 unresolved data gap으로 기록
- [x] 별도 scraping infrastructure를 이번 패스의 non-goal로 유지
- [x] `Web Search + Web Fetch` source capability contract 추가
- [x] RED 확인: registry validator가 Web Search + Web Fetch source와 routing rule 누락을 실패로 보고함
- [x] GREEN 확인: registry/router/template 업데이트 후 `python3 scripts/test_source_capability_registry.py` 통과

---

> **범례:** `- [ ]` = 미착수 · `- [x]` = 완료
