# 다모다란 내러티브-숫자 프레임워크 × Harness 반영도 점검

## 점검 범위

- **프레임워크 문서**: [다모다란 교수의 내러티브-숫자 가치평가 프레임워크.md](file:///e:/invest_harness/docs/harness/invest/planning/%EB%8B%A4%EB%AA%A8%EB%8B%A4%EB%9E%80%20%EA%B5%90%EC%88%98%EC%9D%98%20%EB%82%B4%EB%9F%AC%ED%8B%B0%EB%B8%8C-%EC%88%AB%EC%9E%90%20%EA%B0%80%EC%B9%98%ED%8F%89%EA%B0%80%20%ED%94%84%EB%A0%88%EC%9E%84%EC%9B%8C%ED%81%AC.md)
- **Harness 핵심 문서**: [invest_prompt_v2.md](file:///e:/invest_harness/invest_prompt_v2.md), [team-spec.md](file:///e:/invest_harness/docs/harness/invest/team-spec.md), [AGENTS.md](file:///e:/invest_harness/AGENTS.md)
- **Skill 파일**: valuation-analyst, evidence-planner, source-router, signal-analyst, report-synthesizer, risk-scenario-analyst, report-updater, qa-reviewer, fundamental-analyst

---

## 1. 총괄 평가

| 다모다란 7대 원칙 | 반영도 | 판정 |
|---|---|---|
| ① 내러티브 선행 → 숫자 번역 | ⚠️ 부분 반영 | 구조가 존재하나 명시적 강제 부족 |
| ② 내러티브 현실 검증 (가능·타당·개연) | ⚠️ 부분 반영 | evidence-planner에 질문 분해는 있으나 3단계 테스트 미명시 |
| ③ 일관된 DCF 모형 (FCFF/WACC/Terminal) | ✅ 잘 반영 | valuation-analyst에 가정 표, 교차검증, 민감도가 설계됨 |
| ④ 가격 vs 가치의 구분 | ✅ 잘 반영 | market-price-snapshot ↔ DCF 내재가치 분리 구조 |
| ⑤ 시나리오·민감도·피드백 루프 | ⚠️ 부분 반영 | Bear/Base/Bull + 민감도 있으나 피드백 루프가 약함 |
| ⑥ 회계 조정 (R&D 자본화, 리스 부채화) | ❌ 미반영 | 어디에도 R&D 자본화 또는 리스 부채 전환 지시 없음 |
| ⑦ 할인율 세분화 (국가위험, 실패확률, total beta) | ❌ 미반영 | WACC 구성요소의 세분화 가이드 없음 |

---

## 2. 원칙별 상세 분석

### ① 내러티브 선행 → 숫자 번역

**다모다란 요구**: "이 회사는 어떤 사업이며 어떻게 돈을 벌 것인가"를 먼저 서사로 만들고, 그 서사를 시장 규모·점유율·마진·재투자·자본효율성으로 분해한 뒤 DCF 입력으로 연결.

**현재 Harness**:
- Part II 기업 개요에서 사업 구조와 수익원을 정리
- Part VI 경제적 해자에서 경쟁우위를 식별
- Part VIII 밸류에이션에서 DCF 가정을 표로 명시

**갭**:
- 비즈니스 내러티브 → DCF 입력 매핑이 **암묵적**이다. fundamental-analyst가 해자·경쟁우위를 정리하고, valuation-analyst가 별도로 DCF 가정을 잡는데, 두 산출물 사이에 **"이 내러티브가 이 숫자로 번역된다"는 명시적 연결 단계가 없다.**
- 다모다란의 체크리스트(TAM→점유율→마진→재투자→WACC)처럼 "서사 → 입력 시트" 1페이지를 강제하는 구조가 없다.

> [!IMPORTANT]
> **권고**: valuation-analyst Workflow에 "Step 0: 투자 내러티브 요약 → DCF 입력 매핑" 단계를 추가. fundamental-analyst findings의 해자·사업구조를 읽고, 각 DCF 가정이 어떤 서사 요소에서 도출되었는지를 1페이지 매핑 표로 작성하게 한다.

---

### ② 내러티브 현실 검증 (가능·타당·개연)

**다모다란 요구**: 내러티브가 **가능한지**(물리적/법적), **타당한지**(역사·산업 증거), **개연적인지**(대부분 분석가가 동의할 수 있는지) 3단계로 검증.

**현재 Harness**:
- evidence-planner: 질문 분해, evidence type 선정, validation gate 설정
- source-router: source capability 기반 검증
- qa-reviewer: 출처·수치·논리 일관성 검토

**갭**:
- evidence-planner의 validation gate는 **데이터 검증**(출처·수치 일치)에 초점이 맞춰져 있고, **서사 검증**(이 성장 스토리가 역사적으로 가능한가? 산업 구조상 타당한가?)을 묻는 게이트가 없다.
- qa-reviewer도 "수치 충돌, 출처 누락" 위주이지 "이 투자 논지 자체가 개연적인가?"를 검토하는 항목이 없다.

> [!TIP]
> **권고**: evidence-planner의 validation gates에 `narrative_plausibility` 타입 추가. "해당 성장률이 산업 역사적 선례가 있는가?", "TAM 정의가 점유율·마진·규제와 일관되는가?" 같은 가능·타당·개연 게이트를 1~2개씩 포함.

---

### ③ 일관된 DCF 모형

**다모다란 요구**: FCFF/WACC 기반, 성장-재투자-자본효율 일관성, 터미널가치 경고, 명목/실질 구분.

**현재 Harness**:
- valuation-analyst SKILL.md Step 4: DCF 가정 표 필수 (매출 성장률, 영업이익률, WACC, Terminal Growth 등 11개 항목)
- Step 5: DCF/comps/역사적 밴드 교차검증
- Step 6: Bear/Base/Bull 시나리오별 가치
- 민감도 매트릭스 (WACC × PGR 5×5)

**평가**: ✅ 이 부분은 **잘 설계되어 있다.** 다모다란의 핵심 요구사항 대부분이 반영됨.

**미세 갭**:
- "성장률과 재투자율의 일관성 검증" (g = Reinvestment Rate × ROIC)이 명시적으로 요구되지 않음
- "Terminal Growth ≤ 경제성장률" 경고가 Validation Notes에 없음
- Sales-to-Capital ratio 개념이 없음

> [!NOTE]
> **권고**: valuation-analyst Validation Notes에 다음 추가:
> - `Terminal Growth는 해당 경제의 장기 명목 GDP 성장률을 초과할 수 없다`
> - `성장률 가정은 재투자율 × ROIC와 교차 검증해야 한다`

---

### ④ 가격 vs 가치의 구분

**다모다란 요구**: 내재가치(현금흐름·성장·위험) vs 시장가격(심리·모멘텀·유동성)을 분리.

**현재 Harness**:
- `market-price-snapshot.md`: 시장 가격 기록 (가격 측)
- `03_valuation/findings.md`: 내재가치 산출 (가치 측)
- `04_technical/findings.md`: 기술적 분석 = 가격 행동
- "기술적 분석은 보조 신호로만 사용" 규칙

**평가**: ✅ 구조적으로 가격과 가치가 **물리적으로 분리된 파일**에 담기므로 자연스럽게 구분된다. 기술적 분석의 보조 지위 규정도 다모다란 철학과 일치.

---

### ⑤ 시나리오·민감도·피드백 루프

**다모다란 요구**: Bear/Base/Bull + 민감도 + 새 정보에 의한 서사 수정 루프.

**현재 Harness**:
- ✅ risk-scenario-analyst: Bear/Base/Bull 시나리오 (확률, 가정, 촉발 요인, 주가 범위)
- ✅ valuation-analyst: WACC × PGR 민감도 5×5 매트릭스
- ⚠️ report-updater: 기존 리포트 갱신 범위를 정리하는 스킬 존재
- ⚠️ thesis-tracker: 기존 투자 논지 대비 새 데이터 비교 스킬 존재
- ⚠️ earnings-update: 실적 발표 후 업데이트 스킬 존재

**갭**:
- 피드백 루프가 **별도 유틸리티 스킬**(report-updater, thesis-tracker, earnings-update)로만 존재하고, **핵심 워크플로우의 필수 단계가 아니다.**
- 다모다란은 "초기 내러티브 → 새 정보 → 내러티브 수정 → 가치 재계산"을 **DCF 자체의 본질적 단계**로 본다. 현재 harness에서 이건 선택적 후속 작업이다.
- 민감도가 WACC × PGR에만 집중되어 있고, 다모다란이 강조하는 **매출·마진·재투자 민감도**가 표준 산출물에 포함되지 않는다.

> [!IMPORTANT]
> **권고 1**: valuation-analyst의 민감도 매트릭스를 확장. WACC × PGR 외에 "매출 성장률 × 영업이익률" 2차원 민감도를 추가해 "스토리가 바뀌면 숫자도 함께 움직인다"는 원칙을 반영.
>
> **권고 2**: report-synthesizer의 "모니터링 체크리스트" 섹션에 "내러티브 변경 트리거" 열 추가. "이 지표가 X를 벗어나면 기존 투자 서사를 재검토해야 한다"는 명시적 피드백 루프 트리거를 정의.

---

### ⑥ 회계 조정 (R&D 자본화, 리스 부채화)

**다모다란 요구**: R&D를 비용이 아닌 자본적 지출로 보고, 운용리스를 부채로 전환. 이 두 조정이 ROIC, WACC, 재투자율에 모두 영향.

**현재 Harness**:
- financial-analyst SKILL.md: 재무제표 수집과 비율 분석 지시만 있고, R&D 자본화나 리스 부채 전환 절차 없음
- valuation-analyst SKILL.md: DCF 가정에 CapEx는 있지만 "R&D 자본화 여부"나 "리스 부채화" 항목 없음
- invest_prompt_v2.md Part III: R&D 투자 규모는 Part VII 제품·서비스에서 언급되지만, 가치평가용 자본화 조정 없음

**평가**: ❌ **명백한 누락.** 특히 기술/제약/바이오 기업의 경우 R&D 자본화 없이는 ROIC, FCF, 재투자율이 모두 왜곡된다. IFRS 16 이후 리스 부채화는 표준이 되었지만, 명시적 점검 항목이 없다.

> [!WARNING]
> **권고**: financial-analyst 또는 valuation-analyst에 다음 체크리스트 추가:
> 1. R&D 비용이 매출의 10% 이상인 기업 → R&D 자본화 조정 검토 (자본화 자산, 상각 기간, 조정 EBIT, 조정 자본 계산)
> 2. 운용리스 의무가 유의미한 기업 → 리스 부채 전환이 부채비율과 WACC에 미치는 영향 점검 (IFRS 16/ASC 842 이전 기준 vs 이후 기준 구분)
> 3. 조정 전/후 ROIC 비교 표 포함

---

### ⑦ 할인율 세분화

**다모다란 요구**:
- WACC는 **시장가치 비중** 사용 (장부가치 비중 금지)
- 국가위험은 **법인 소재지가 아니라 실제 영업 노출** 기준
- **실패확률**은 할인율이 아닌 별도 확률로 조정
- 비상장/집중투자 시 **total beta** 고려

**현재 Harness**:
- valuation-analyst: "WACC / 할인율" 항목만 존재, 구성요소 분해 없음
- invest_prompt_v2.md: "할인율 또는 WACC" 한 줄만 존재
- 어디에도 시장가중치, ERP, 국가위험프리미엄, 실패확률 가이드 없음

**평가**: ❌ **할인율 산정이 블랙박스.** WACC를 단일 숫자로 넣게만 되어 있고, 무위험률·ERP·베타·국가위험프리미엄·부채비용을 어떻게 구하는지 가이드가 전혀 없다.

> [!CAUTION]
> **권고**: valuation-analyst에 WACC 구성 명세 표 추가:
>
> | 구성요소 | 값 | 출처/근거 |
> |---|---|---|
> | 무위험률 | | |
> | 주식위험프리미엄 (ERP) | | |
> | 베타 (레버드) | | |
> | 국가위험프리미엄 (매출 지역 가중) | | |
> | 자기자본비용 (k_e) | | |
> | 세전 부채비용 (k_d) | | |
> | 세율 | | |
> | 시장가치 기준 E/(D+E) | | |
> | 시장가치 기준 D/(D+E) | | |
> | WACC | | |
>
> 추가 선택 항목: 실패확률 조정, total beta (비상장/집중투자 시)

---

## 3. 기타 관찰

### 양적 성장 vs 질적 성장 (Ferrari 교훈)
- 다모다란 Ferrari 사례: "더 많이 파는 것보다 희소성 유지가 가치를 높인다"
- 현재 Harness의 경제적 해자(Part VI)에서 "가격 결정력" 항목이 있지만, **성장이 해자를 훼손하는 역설**을 점검하는 구조는 없다.
- **권고**: risk-scenario-analyst에 "Bull 시나리오가 해자를 약화시키는지" 교차점검 항목 추가

### 옵션가치 / Real Options
- 다모다란: 특허, 미개발 자원, 투자 연기/확장/포기 같은 real option이 유의미한 경우 별도 반영
- 현재 Harness: 옵션 체인 데이터는 yfinance로 수집하지만, **real option valuation**은 고려 대상에 없음
- **권고**: 현 단계에서 필수는 아님. 장기적으로 valuation-analyst에 "선택적: Real Option 검토 대상 여부" 체크 항목만 추가

### 데이터 자료원 매핑
- 다모다란의 핵심 자료원(Damodaran Current Data 페이지: ERP, 국가위험프리미엄, 산업별 베타)은 WACC 산정의 1차 기준점
- 현재 source-capability-registry에 이 자료원이 **등록되어 있지 않음**
- **권고**: source-capability-registry에 `damodaran-data` source 추가 (ERP, CRP, industry beta 제공, connection_status=external_manual)

---

## 4. 우선순위 정리

| 순위 | 개선 항목 | 영향 범위 | 난이도 |
|---|---|---|---|
| 1 | WACC 구성 명세 표 추가 | valuation-analyst SKILL.md | 낮음 (문서 추가) |
| 2 | R&D 자본화 / 리스 부채화 체크리스트 | financial-analyst 또는 valuation-analyst | 중간 |
| 3 | 내러티브→DCF 매핑 단계 추가 | valuation-analyst Workflow Step 0 | 낮음 (문서 추가) |
| 4 | 내러티브 검증 게이트 추가 | evidence-planner Rules/Workflow | 낮음 |
| 5 | 매출×마진 민감도 추가 | valuation-analyst dashboard_data | 중간 |
| 6 | Terminal Growth ≤ GDP 경고 | valuation-analyst Validation Notes | 낮음 (1줄 추가) |
| 7 | g = Reinvestment × ROIC 교차검증 | valuation-analyst Validation Notes | 낮음 |
| 8 | 피드백 루프 트리거 명시화 | report-synthesizer 모니터링 체크리스트 | 낮음 |
| 9 | Damodaran data source 등록 | source-capability-registry | 낮음 |
| 10 | Real Option 체크 항목 | valuation-analyst (선택적) | 낮음 |

---

## 5. 결론

현재 Harness는 다모다란 프레임워크의 **구조적 골격**(DCF, 시나리오, 교차검증, 가격-가치 분리)을 잘 반영하고 있다. 특히 멀티에이전트 파이프라인이 "분석 → 합성 → QA"로 이어지는 점은 다모다란의 "서사 → 숫자 → 검증" 흐름과 자연스럽게 대응된다.

그러나 **다모다란 철학의 핵심 차별점**인 다음 3가지가 아직 구조에 녹아들지 않았다:

1. **내러티브가 숫자를 지배한다는 강제**: 서사에서 숫자로의 매핑이 암묵적
2. **회계 조정의 체계화**: R&D 자본화, 리스 부채화 같은 "가치평가용 재무제표 정비" 단계 부재
3. **할인율의 투명한 분해**: WACC가 단일 숫자 입력으로 남아 있어 국가위험, ERP, 실패확률 같은 핵심 판단이 보이지 않음

이 3가지는 모두 문서 수준의 추가로 해결 가능하며, 코드 변경은 불필요하다. 우선순위 1~4를 먼저 반영하면 harness의 밸류에이션 품질이 의미 있게 개선될 것이다.
