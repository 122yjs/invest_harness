# 03.md 미구현 + UX 피드백 통합 구현 계획

> 기준: [03_core_evidence_layer_implementation.md](/Users/junier/Documents/Develop/invest_harness-clean-feat-improvement/docs/harness/invest/planning/03_core_evidence_layer_implementation.md)> UX 피드백: 실제 리서치 운영 중 발견된 7건
> 작성일: 2026-05-16
> ~~Skill sync 누락 6건~~ → ✅ 해결 완료

---

## 변경 범위 요약

| Phase | 항목 수 | 성격 |
|---|---|---|
| **1** — Research Layer 문서 보강 | 3 | signal primitive, validation gate, claim boundary 누락 |
| **2** — Golden Scenarios 추가 | 3 | 03.md 명시 eval fixture 누락 |
| **3** — UX 피드백 반영 | 7 | 운영 중 발견한 프로세스/문서 개선 |
| **4** — 테스트 보강 | 4 | 누락 테스트 + 기존 테스트 커버리지 확대 |
| **5** — Sync + 검증 | 1 | canonical → .agents 반영 + verify |
| **합계** | **18** | |

---

## Phase 1 — Research Layer 문서 보강

### 1-1. `technical_price_signal` primitive 추가

#### [MODIFY] [signal-primitives.md](file:///Users/junier/Documents/Develop/invest_harness-clean-feat-improvement/docs/harness/invest/research-layer/signal-primitives.md)

03.md §5-4 (L539)에서 11개 primitive를 명시했으나 현재 10개만 존재. `technical_price_signal` 추가:

```markdown
## technical_price_signal

- purpose: 가격 추세, 모멘텀, 지지/저항 수준에서 기술적 신호를 추출한다.
- required_inputs: price history, volume, timeframe, indicator selection.
- compatible_sources: yfinance, Alpha Vantage, FMP.
- common_metrics: moving averages, RSI, MACD, Bollinger Bands, volume profile, support/resistance levels.
- output fields: ticker, timeframe, indicator, value, signal_direction, confidence.
- caveats: 기술적 지표는 후행성이며 단독 투자 판단 근거가 아니다. 시장 구조 변화에 민감하다.
- claim boundaries: 보조 신호로만 사용한다. 독립적 투자 결론을 도출하지 않는다.
```

---

### 1-2. `macro_series_gate` 추가

#### [MODIFY] [validation-gates.md](file:///Users/junier/Documents/Develop/invest_harness-clean-feat-improvement/docs/harness/invest/research-layer/validation-gates.md)

03.md §5-5 (L588)에서 9개 gate를 명시했으나 현재 8개만 존재. `macro_series_gate` 추가:

```markdown
## macro_series_gate

- Applies to: FRED, ECOS, official macro time series.
- Required checks: series ID, unit, frequency, latest observation date, transformation, seasonal adjustment basis, geography.
- Must flag: level vs rate of change confusion, stale observation, revision risk, misapplied geography.
- Prohibition: Do not infer company fundamentals from macro series alone.
- Prohibition: Do not treat macro correlation as causation without a stated exposure mechanism.
```

---

### 1-3. Claim Boundary 금지 조항 보강

#### [MODIFY] [claim-boundary-policy.md](file:///Users/junier/Documents/Develop/invest_harness-clean-feat-improvement/docs/harness/invest/research-layer/claim-boundary-policy.md)

`## Mandatory Prohibitions` 섹션에 2건 추가:

```markdown
- Alpha Vantage vendor data is not audited filing.
- SEC filing stale period is not current guidance.
```

---

## Phase 2 — Golden Scenarios 추가

### 2-1. FRED macro regime

#### [NEW] `docs/harness/invest/evals/golden-scenarios/fred-macro-regime.md`

03.md §11-5 (L1185-1193). FRED macro series를 valuation discount-rate, inflation, employment, liquidity context로 사용하되 개별 기업 실적 직접 근거로 오용하지 않는지 검증.

```markdown
# Golden Scenario: fred-macro-regime

This is an eval fixture only. It must not become a core router category.

## Input

사용자: "현재 미국 금리 환경이 성장주 밸류에이션에 미치는 영향을 분석해줘."

## Expected Decomposition

- subjects from surface form:
  - 미국 금리 환경
  - 성장주 밸류에이션
- required evidence types:
  - macro_policy (FRED: Fed Funds Rate, US10Y, CPI)
  - price_valuation (growth stock multiples)
  - company_disclosure (affected company exposure)
- signal primitives:
  - macro_regime_signal
  - valuation_anchor

## Expected Boundaries

- FRED macro series는 macro sensitivity context로만 사용한다.
- 거시 지표 변동을 개별 기업 실적 변동 근거로 직접 사용하지 않는다.
- level vs rate of change를 구분한다.
- 기업 노출 경로(exposure mechanism)가 명시되지 않으면 causation을 주장하지 않는다.
```

---

### 2-2. SEC EDGAR company disclosure

#### [NEW] `docs/harness/invest/evals/golden-scenarios/sec-edgar-company-disclosure.md`

03.md §11-6 (L1196-1204). SEC filing type, filing date, fiscal period 표시 및 stale filing 오용 방지 검증.

```markdown
# Golden Scenario: sec-edgar-company-disclosure

This is an eval fixture only. It must not become a core router category.

## Input

사용자: "Tesla의 최근 10-K에서 에너지 사업 세그먼트 성장성을 분석해줘."

## Expected Decomposition

- subjects from surface form:
  - Tesla 에너지 사업 세그먼트
- required evidence types:
  - company_disclosure (SEC EDGAR 10-K filing)
  - financial_statement (segment revenue)
- signal primitives:
  - disclosure_exposure

## Expected Boundaries

- filing type (10-K, 10-Q, 8-K)을 반드시 표시한다.
- filing date와 period of report를 구분한다.
- stale filing (1년 이상 경과)을 현재 guidance로 사용하지 않는다.
- CIK/accession number를 기록하고 정확한 filing section을 인용한다.
```

---

### 2-3. Alpha Vantage market data boundary

#### [NEW] `docs/harness/invest/evals/golden-scenarios/alpha-vantage-market-data-boundary.md`

03.md §11-7 (L1207-1215). Alpha Vantage vendor data 한계 표시 및 감사 재무제표 대비 우선순위 검증.

```markdown
# Golden Scenario: alpha-vantage-market-data-boundary

This is an eval fixture only. It must not become a core router category.

## Input

사용자: "MSFT의 기술적 분석과 재무 지표를 종합해서 밸류에이션을 평가해줘."

## Expected Decomposition

- subjects from surface form:
  - MSFT 기술적 분석
  - MSFT 재무 지표
  - 밸류에이션
- required evidence types:
  - price_valuation (Alpha Vantage or yfinance)
  - technical_market_data (Alpha Vantage)
  - company_disclosure (SEC EDGAR 10-K/10-Q)
- signal primitives:
  - technical_price_signal
  - valuation_anchor

## Expected Boundaries

- Alpha Vantage 가격/기술지표는 vendor market data이다.
- vendor fundamentals를 감사 재무제표보다 우선하지 않는다.
- 기술적 지표를 독립적 투자 결론으로 사용하지 않는다.
- adjusted vs unadjusted 가격을 명시한다.
- endpoint, currency, timestamp를 기록한다.
```

---

## Phase 3 — UX 피드백 반영

> [!NOTE]
> UX 피드백은 canonical source (`plugins/vertical-plugins/invest-research/`)를 수정합니다. Phase 5에서 sync하여 `.agents/`에 반영합니다.

### 3-1. Pre-flight Connection Check (🥇)

> 문제: Tavily 401, KRX 401이 실행 중에야 발견되어 evidence plan 재설계 필요

#### [MODIFY] orchestrator SKILL.md (canonical)

`### 1. 입력 수집 게이트` 뒤에 `### 1.5 Pre-flight source check` 삽입:

```markdown
### 1.5 Pre-flight source check

입력 정규화 완료 후, evidence planning 전에 connected 소스의 연결 상태를 사전 검증한다.

1. `docs/harness/invest/research-layer/source-capability-registry.md`를 로드한다.
2. connection_status가 `connected`인 소스에 대해 최소 1회 probe call을 수행한다.
   - korea-stock: `get_today_date` 호출
   - yfinance: `yfinance_search(query=대상 티커)` 호출
3. 결과를 `${ACTIVE_WORKSPACE}/00_evidence/api-call-log.md`에 기록한다.
4. 실패한 소스는 `${ACTIVE_WORKSPACE}/00_evidence/unresolved-data-gaps.md`에 미리 등록한다.
5. evidence plan 설계 시 실패한 소스를 fallback으로 전환한다.
6. 모든 connected 소스가 실패하면 사용자에게 보고하고 web_fetch 기반 대안을 제안한다.
```

#### [MODIFY] [runbook.md](file:///Users/junier/Documents/Develop/invest_harness-clean-feat-improvement/docs/harness/invest/runbook.md)

`## 1. 입력 정리`와 `## 2. Evidence planning` 사이에 `## 1.5 Pre-flight source check` 삽입. 내용은 위와 동일.

---

### 3-2. CFS/OFS 이중 수집 의무화 (🥇)

> 문제: 한국 기업에서 `fs_div=OFS`만 기본 호출하여 연결(CFS) 데이터를 놓침 (1.97조 vs 3.76조 차이)

#### [MODIFY] financial-analyst SKILL.md (canonical)

`### 2.2 MCP 도구 우선 사용` 사용 순서 뒤에 추가:

```markdown
### 연결(CFS) vs 별도(OFS) 이중 수집 규칙 (한국 기업)

한국 상장기업의 재무제표 수집 시 연결(CFS)과 별도(OFS) 모두 조회한다.

1. `get_financial_statement(fs_div="OFS", ...)` — 별도 먼저 조회 (빠름, 분량 적음)
2. `get_financial_statement(fs_div="CFS", ...)` — 연결 반드시 추가 조회
3. 연결 vs 별도 수치가 크게 다를 경우 (매출 기준 20% 이상 차이):
   - `${ACTIVE_WORKSPACE}/06_risk_scenario/conflicts.md`에 차이와 원인을 기록
   - 분석 본문에서는 **연결(CFS) 기준으로 우선 사용**
   - 별도(OFS) 수치는 참고용으로 병기
4. CFS 조회 실패 시 OFS만으로 진행하되, findings.md에 "연결 재무제표 미확인" 명시
```

---

### 3-3. Source Registry 사전 로드 의무화 (🥇)

> 문제: registry (22KB)를 제때 읽지 않아 evidence plan에서 소스가 빠지고, 왜 빠졌는지 기록도 없음

#### [MODIFY] orchestrator SKILL.md (canonical)

`### 3. Evidence planning / source routing` 첫 문단에 추가:

```markdown
Evidence planning 필수 사전 조건:

1. `docs/harness/invest/research-layer/source-capability-registry.md`를 반드시 먼저 읽는다.
2. 각 source의 connection_status를 평가한다.
3. evidence-plan에 "연결 불가 소스"를 data gap으로 기록하는 템플릿을 적용한다.
4. registry에 등재된 소스만 후보로 사용한다.
```

#### [MODIFY] evidence-planner SKILL.md (canonical)

Required Inputs에 추가:
```markdown
- 기준 문서: `docs/harness/invest/research-layer/source-capability-registry.md` (필수 사전 로드)
```

---

### 3-4. web_fetch를 공식 fallback으로 등록 (🥈)

> 문제: web_search/tavily 실패 시 대안이 없었으나 web_fetch는 잘 작동함

#### [MODIFY] [source-call-plan.md (template)](file:///Users/junier/Documents/Develop/invest_harness-clean-feat-improvement/docs/harness/invest/templates/source-call-plan.md)

`## Unavailable Source Handling` 섹션 뒤에 추가:

```markdown
### web_fetch Fallback 정책

web_search 또는 tavily_search가 실패(401, timeout 등)하면:

1. **web_fetch를 첫 번째 대안으로 사용한다.**
2. 알려진 유용한 URL 템플릿 (한국 기업):
   - 네이버 금융: `https://finance.naver.com/item/main.nhn?code={stock_code}`
   - 네이버 뉴스: `https://search.naver.com/search.naver?where=news&query={company_name}`
   - WiseReport: `https://comp.wisereport.co.kr/company/c1010001.aspx?cmp_cd={stock_code}`
   - 한경 컨센서스: `https://consensus.hankyung.com/apps.analysis/analysis.list?search_text={company_name}`
3. web_fetch 결과는 evidence-ledger에 URL, 조회 시각, 성공/실패를 기록한다.
4. web_fetch도 실패하면 unresolved-data-gaps.md에 기록한다.
```

---

### 3-5. 분기보고서 목차 기반 섹션 선택 가이드 (🥈)

> 문제: DART 보고서가 수 MB로 목차만 반환될 때 어떤 섹션을 조회할지 판단 기준이 없음

#### [MODIFY] financial-analyst SKILL.md (canonical)

`### 2.2 MCP 도구 우선 사용` 뒤에 추가:

```markdown
### DART 대형 보고서 목차 수신 시 섹션 선택 가이드

`get_disclosure`로 대형 보고서 조회 시 목차만 반환되면, 아래 우선순위로 하위 섹션을 개별 조회한다. 섹션 ID는 DART 보고서마다 다를 수 있으므로 목차 텍스트의 제목을 기준으로 매칭한다.

| 우선순위 | 섹션 제목 키워드 | 내용 | 필수 |
|---|---|---|---|
| 1 | 요약재무정보 | 연결 + 별도 요약 수치 | 必 |
| 2 | 연결재무제표 | CFS 전문 | 必 |
| 3 | 사업의 내용 | 사업 구조, 매출원, 시장 현황 | 必 |
| 4 | 재무제표 주석 | 부채, 재고, 우발부채, 관계사 거래 | 권장 |
| 5 | 이사의 경영진단 | 경영진 전망 (사업보고서만 해당) | 조건부 |
| 6 | 별도재무제표 | OFS 대조용 | 참고 |

주의:
- 분기보고서에는 "이사의 경영진단" 섹션이 없을 수 있음 (해당사항 없음 확인)
- 연결재무제표 섹션은 100KB+ 가능하나 반드시 조회
```

---

### 3-6. conflicts.md 작성 시점 명확화 (🥉)

> 문제: 순차 모드에서 conflicts.md가 6단계에서 임의 작성되나, 전체 findings 대조 후 보강이 필요

#### [MODIFY] [runbook.md](file:///Users/junier/Documents/Develop/invest_harness-clean-feat-improvement/docs/harness/invest/runbook.md)

`## 6. 병렬 분석 산출물 생성` 공통 규칙 뒤에 추가:

```markdown
### 6.5 충돌 감지 패스

01~06 findings가 모두 완료된 후, 초안 합성(7단계) 전에 충돌 감지 패스를 수행한다.

1. 오케스트레이터가 01~06 findings 전체를 읽는다.
2. 수치, 판단, 데이터 신선도 충돌을 감지한다.
3. `${ACTIVE_WORKSPACE}/06_risk_scenario/conflicts.md`에 기록을 작성하거나 기존 내용을 보강한다.
4. `report-synthesizer`는 초안 합성 전에 반드시 conflicts.md를 참조한다.

순차 모드에서 risk-scenario-analyst가 선행 findings를 일부 참조해 conflicts를 먼저 작성할 수 있으나, 6.5 단계에서 전체 대조를 추가 수행한다.
```

#### [MODIFY] orchestrator SKILL.md (canonical)

`### 5. 중간 산출물 점검` 충돌 기록 기준 뒤에 추가:

```markdown
- `conflicts.md`는 모든 analyst findings(01~06) 완료 후에 전체 대조 패스로 작성하거나 보강한다.
```

---

### 3-7. 산출물 전달 정책 문서화 (🥉)

> 문제: 최종 파일을 외부(Telegram 등)로 전송할 때 경로 제약이 있음

#### [MODIFY] [cross-tool-usage.md](file:///Users/junier/Documents/Develop/invest_harness-clean-feat-improvement/docs/harness/invest/cross-tool-usage.md)

`## 주의사항` 뒤에 추가:

```markdown
## 산출물 전달 정책

### 외부 전송 시 경로 제약

일부 외부 전송 도구(Telegram bot, Slack webhook 등)는 특정 디렉터리만 접근을 허용합니다.

- `${ACTIVE_WORKSPACE}/` 경로는 직접 전송이 불가능할 수 있습니다.
- 전송이 필요하면 최종 산출물을 허용 경로(예: `~/Downloads/`)로 복사한 후 전송합니다.
- 복사 후 원본 경로의 파일은 삭제하지 않습니다 (감사 보존).

### 전달 가능 파일

| 파일 | 용도 |
|---|---|
| `08_final/report.md` | Markdown 최종 리포트 |
| `08_final/report.html` | HTML 최종 리포트 |
| `08_final/executive-summary.md` | 핵심 요약 |
```

---

## Phase 4 — 테스트 보강

### 4-1. 신규 테스트

#### [NEW] `scripts/test_existing_connected_sources_not_duplicated.py`

03.md §12-7 (L1338-1354). FRED/SEC EDGAR/Alpha Vantage/yfinance/DART-KRX에 대해 새 connector/client/credential 중복 생성 방지 검사:

- 새 API key 파일 추가 여부
- 새 credentials 파일 추가 여부
- 중복 connector 디렉터리 추가 여부
- `.mcp.institutional.json` 불필요 수정 여부

---

### 4-2. 기존 테스트 보강

#### [MODIFY] [test_claim_boundary_policy.py](file:///Users/junier/Documents/Develop/invest_harness-clean-feat-improvement/scripts/test_claim_boundary_policy.py)

REQUIRED 리스트에 2건 추가:

```python
"Alpha Vantage vendor data is not audited filing",
"SEC filing stale period is not current guidance",
```

#### [MODIFY] [test_evidence_layer_structure.py](file:///Users/junier/Documents/Develop/invest_harness-clean-feat-improvement/scripts/test_evidence_layer_structure.py)

GOLDEN 리스트에 3건 추가:

```python
"fred-macro-regime.md",
"sec-edgar-company-disclosure.md",
"alpha-vantage-market-data-boundary.md",
```

#### [MODIFY] [verify_invest_harness.py](file:///Users/junier/Documents/Develop/invest_harness-clean-feat-improvement/scripts/verify_invest_harness.py)

COMMANDS에 1건 추가:

```python
("Check existing connected sources not duplicated", [sys.executable, "scripts/test_existing_connected_sources_not_duplicated.py"]),
```

---

## Phase 5 — Sync + 검증

```bash
# 1. canonical → .agents 동기화
python3 scripts/sync_invest_skills.py

# 2. 전체 검증
python3 scripts/verify_invest_harness.py
```

---

## 파일 변경 요약

| 유형 | 파일 | Phase |
|---|---|---|
| MODIFY | `docs/harness/invest/research-layer/signal-primitives.md` | 1-1 |
| MODIFY | `docs/harness/invest/research-layer/validation-gates.md` | 1-2 |
| MODIFY | `docs/harness/invest/research-layer/claim-boundary-policy.md` | 1-3 |
| NEW | `docs/harness/invest/evals/golden-scenarios/fred-macro-regime.md` | 2-1 |
| NEW | `docs/harness/invest/evals/golden-scenarios/sec-edgar-company-disclosure.md` | 2-2 |
| NEW | `docs/harness/invest/evals/golden-scenarios/alpha-vantage-market-data-boundary.md` | 2-3 |
| MODIFY | `plugins/.../invest-orchestrator/SKILL.md` (canonical) | 3-1, 3-3, 3-6 |
| MODIFY | `plugins/.../financial-analyst/SKILL.md` (canonical) | 3-2, 3-5 |
| MODIFY | `plugins/.../evidence-planner/SKILL.md` (canonical) | 3-3 |
| MODIFY | `docs/harness/invest/runbook.md` | 3-1, 3-6 |
| MODIFY | `docs/harness/invest/templates/source-call-plan.md` | 3-4 |
| MODIFY | `docs/harness/invest/cross-tool-usage.md` | 3-7 |
| NEW | `scripts/test_existing_connected_sources_not_duplicated.py` | 4-1 |
| MODIFY | `scripts/test_claim_boundary_policy.py` | 4-2 |
| MODIFY | `scripts/test_evidence_layer_structure.py` | 4-2 |
| MODIFY | `scripts/verify_invest_harness.py` | 4-2 |

---

## Open Questions

> [!IMPORTANT]
> **Q1. Pre-flight check 구현 방식**: 별도 스크립트(`scripts/check-connections.sh`)까지 만들지, SKILL.md 지침만으로 충분한지? MCP 서버가 실행 중이어야 의미가 있으므로 **우선 지침 추가만** 하고 스크립트는 후속으로 제안합니다.

> [!IMPORTANT]
> **Q2. DART 섹션 ID 유연성**: 보고서마다 섹션 ID가 다를 수 있으므로, ID 패턴 대신 **섹션 제목 키워드 매칭**으로 가이드하는 것을 제안합니다.

> [!IMPORTANT]
> **Q3. canonical 편집 확인**: Phase 3의 UX 피드백은 `plugins/vertical-plugins/invest-research/`를 직접 수정하고 sync합니다. 이 방식이 맞는지 확인 부탁드립니다.
