---
name: invest-orchestrator
description: 개별 주식 투자 리포트 Harness의 입력 정규화, 역할 분배, 산출물 수집, QA 반영, 최종 보고서 확정을 조율하는 최상위 스킬
---

# invest-orchestrator

## When to Use

- 사용자가 특정 상장기업의 전체 투자 리포트 생성을 요청했을 때 사용한다.
- `invest_prompt_v2.md`의 분석 파트를 여러 전문가 스킬에 나눠 맡기고 최종 보고서로 조립해야 할 때 사용한다.
- 출처, 기준일, 회계기간, 통화, 가정이 남는 재현 가능한 리서치 워크플로우가 필요할 때 사용한다.
- 단일 섹션 보강만 필요한 경우에는 해당 전문가 스킬을 직접 사용하고, 전체 흐름이 필요할 때만 이 스킬을 사용한다.

## Entry Input Gate

오케스트레이터는 입력 정규화 전에 반드시 입력 수집 게이트를 수행한다.

게이트 산출물은 `${ACTIVE_WORKSPACE}/00_input/input-intake.md`다. 이 파일에는 사용자 원문, 자동 식별 결과, 사용자에게 되물을 선택 옵션, 선택 입력인 특정 이벤트 / 촉매, 기본값, 게이트 결과를 남긴다.

### 최소 식별자

사용자는 아래 둘 중 하나만 제공해도 된다.

- 기업명
- 티커

오케스트레이터는 제공된 값으로 대상 기업명, 티커, 거래소/국가, 상장 통화, 회계 기준을 자동 확인한다. 처음부터 기업명, 티커, 거래소/국가 3개를 모두 요구하지 않는다.

다만 아래 경우에는 사용자 확인 전까지 전문가 분석을 시작하지 않는다.

- 기업명 또는 티커가 전혀 없음
- 티커가 여러 거래소에서 중복됨
- 기업명 검색 결과가 복수 후보임
- 사용자가 제공한 기업명과 티커가 서로 다른 회사를 가리킴
- 상장 폐지, ADR/보통주, 우선주/보통주 구분이 투자 판단에 영향을 줌

### 사용자에게 되물을 항목

식별자가 충분하면 사용자에게 아래 다섯 가지 옵션만 묻는다. 각 항목에는 간단 선택지 힌트를 함께 표시한다.

| 항목 | 간단 선택지 | 기본값 |
|---|---|---|
| 진행 방식 | `> 일괄 / 순차` | 일괄 |
| 분석 초점 | `> 장기 / 분기 / 혼합` | 혼합 |
| 투자 기간 | `> 단기 / 중기 / 장기 / 전체` | 전체 |
| 비교기업 수 | `> 3 / 5 / 10 / 직접` | 5 |
| 보고서 깊이 | `> 요약 / 표준 / 심층` | 심층 |

### 선택 입력

특정 이벤트 / 촉매가 있으면 선택 입력으로 받는다. 이는 상위 분석 초점이 아니라 최근 분기 실적·센티먼트 분석의 하위 축이다.

간단 선택지: `> 없음 / 실적 / 가이던스 / M&A / 규제 / 소송 / 신제품 / 관세 / 수주 / 공급망`

### 자동 적용 기본값

| 항목 | 기본값 |
|---|---|
| 분석 기준일 | 작업 당일 |
| 투자자 유형 | 혼합형 |
| 기준 통화 | 상장 통화 |
| 회계 기준 | 회사 공시 기준 |
| 기술적 분석 포함 여부 | 포함하되 장기 리포트에서는 보조 신호로 제한 |
| 최종 의견 형식 | Rating + Price Target + 시나리오별 전략 |

### 사용자 보완 질문 폼

```text
투자 리포트 생성을 시작하기 전에 아래 옵션만 확인해 주세요.

[자동 인식 대상]
- 기업명 또는 티커 중 하나만 입력해도 됩니다.
- 예시: Apple / AAPL / 삼성전자 / 005930.KS / Constellium / CSTM
- 거래소·국가·상장 통화·회계 기준은 Harness가 우선 자동 확인합니다.
- 복수 후보가 나오면 그때만 다시 확인합니다.

[선택 옵션]
1. 진행 방식: > 일괄 / 순차
   - 일괄 = 전체 일괄 생성
   - 순차 = 순차 단계별 생성
   - 기본값: 일괄

2. 분석 초점: > 장기 / 분기 / 혼합
   - 장기 = 장기 기본형: 최근 3~5년 연간 재무, 산업, 해자, 밸류에이션 중심
   - 분기 = 최근 분기 실적·센티먼트 심층형: 최근 4~8개 분기 실적, 컨센서스, 어닝콜, 뉴스·수급·애널리스트 리비전 중심
   - 혼합 = 장기 구조 + 최근 분기 실적·센티먼트 심층 비교
   - 기본값: 혼합

3. 투자 기간: > 단기 / 중기 / 장기 / 전체
   - 단기 = 1~3개월
   - 중기 = 6~12개월
   - 장기 = 3~5년
   - 전체 = 단기·중기·장기 모두
   - 기본값: 전체

4. 비교기업 수: > 3 / 5 / 10 / 직접
   - 직접 = 사용자가 비교기업 수 또는 기업명을 직접 지정
   - 기본값: 5

5. 보고서 깊이: > 요약 / 표준 / 심층
   - 요약 = 핵심만 압축
   - 표준 = 일반 리서치 노트 수준
   - 심층 = 재무·분기·센티먼트·밸류에이션·리스크까지 상세 분석
   - 기본값: 심층

[선택 입력]
6. 특정 이벤트 / 촉매: > 없음 / 실적 / 가이던스 / M&A / 규제 / 소송 / 신제품 / 관세 / 수주 / 공급망
   - 이벤트가 없으면 "없음" 또는 공란
   - 예시: 최근 실적 발표 / 가이던스 하향 / M&A / 규제 / 소송 / 신제품 발표 / 관세 이슈 / 고객사 수주 / 공급망 이슈

나머지는 기본값으로 진행합니다.
- 분석 기준일: 작업 당일
- 투자자 유형: 혼합형
- 기준 통화: 상장 통화
- 회계 기준: 회사 공시 기준
- 기술적 분석 포함 여부: 포함
- 최종 의견 형식: Rating + Price Target + 시나리오별 전략
```

## Required Inputs

먼저 사용자가 제공한 원문 입력을 보존하고, 입력 수집 게이트를 통과한 뒤 아래 항목을 `${ACTIVE_WORKSPACE}/00_input/request-summary.md`에 정규화한다.

| 항목 | 처리 |
|---|---|
| 사용자 제공 식별자 | 필수. 기업명 또는 티커 중 하나 이상 |
| 대상 기업명 | 자동 확인. 복수 후보면 사용자 확인 |
| 티커 | 자동 확인. 복수 후보면 사용자 확인 |
| 거래소 / 국가 | 자동 확인. 충돌 시 사용자 확인 |
| 진행 방식 | 사용자에게 확인. 기본값은 일괄 |
| 분석 초점 | 사용자에게 확인. 기본값은 혼합 |
| 특정 이벤트 / 촉매 | 선택 입력. 이벤트 드리븐 독립 모드가 아니라 하위 분석 축 |
| 분석 기준일 | 기본값은 작업 당일 |
| 투자 기간 | 사용자에게 확인. 기본값은 전체 |
| 투자자 유형 | 기본값은 혼합형 |
| 보고서 깊이 | 사용자에게 확인. 기본값은 심층 |
| 기준 통화 | 상장 통화 우선 |
| 회계 기준 | 회사 공시 기준 우선 |
| 비교기업 수 | 사용자에게 확인. 기본값은 5 |
| 기술적 분석 포함 여부 | 기본값은 포함 |
| 최종 의견 형식 | 기본값은 Rating + Price Target + 시나리오별 전략 |

## Architecture

이 Harness는 `Pipeline + Fan-out/Fan-in + Producer-Reviewer` 조합으로 운영한다.

| 단계 | 패턴 | 이유 |
|---|---|---|
| 입력 정규화 | Pipeline | 모든 역할이 같은 입력 스냅샷을 사용해야 한다. |
| 전문가 분석 | Fan-out/Fan-in | 재무, 정성, 밸류에이션, 기술, 매크로, 리스크 분석은 병렬화 가능하다. |
| 초안 합성 | Pipeline | 전문가 산출물이 있어야 종합 점수와 최종 의견을 만들 수 있다. |
| QA 및 수정 | Producer-Reviewer | 출처 누락, 수치 충돌, 과도한 확신 표현을 별도 품질 게이트에서 잡는다. |

## Workflow

<!-- BEGIN INPUT_GATE_POLICY_INTEGRATED -->
전체 리포트 생성 시에는 먼저 입력 수집 게이트를 수행합니다. 사용자가 기업명 또는 티커 중 하나를 제공하면 나머지 식별자는 자동 확인합니다. 사용자에게는 진행 방식 `> 일괄 / 순차`, 분석 초점 `> 장기 / 분기 / 혼합`, 투자 기간 `> 단기 / 중기 / 장기 / 전체`, 비교기업 수 `> 3 / 5 / 10 / 직접`, 보고서 깊이 `> 요약 / 표준 / 심층`만 되묻습니다.

```text
투자 리포트 생성을 시작하기 전에 아래 옵션만 확인해 주세요.

[자동 인식 대상]
- 기업명 또는 티커 중 하나만 입력해도 됩니다.
- 예시: Apple / AAPL / 삼성전자 / 005930.KS / Constellium / CSTM
- 거래소·국가·상장 통화·회계 기준은 Harness가 우선 자동 확인합니다.
- 복수 후보가 나오면 그때만 다시 확인합니다.

[선택 옵션]
1. 진행 방식: > 일괄 / 순차
   - 일괄 = 전체 일괄 생성
   - 순차 = 순차 단계별 생성
   - 기본값: 일괄

2. 분석 초점: > 장기 / 분기 / 혼합
   - 장기 = 장기 기본형: 최근 3~5년 연간 재무, 산업, 해자, 밸류에이션 중심
   - 분기 = 최근 분기 실적·센티먼트 심층형: 최근 4~8개 분기 실적, 컨센서스, 어닝콜, 뉴스·수급·애널리스트 리비전 중심
   - 혼합 = 장기 구조 + 최근 분기 실적·센티먼트 심층 비교
   - 기본값: 혼합

3. 투자 기간: > 단기 / 중기 / 장기 / 전체
   - 단기 = 1~3개월
   - 중기 = 6~12개월
   - 장기 = 3~5년
   - 전체 = 단기·중기·장기 모두
   - 기본값: 전체

4. 비교기업 수: > 3 / 5 / 10 / 직접
   - 직접 = 사용자가 비교기업 수 또는 기업명을 직접 지정
   - 기본값: 5

5. 보고서 깊이: > 요약 / 표준 / 심층
   - 요약 = 핵심만 압축
   - 표준 = 일반 리서치 노트 수준
   - 심층 = 재무·분기·센티먼트·밸류에이션·리스크까지 상세 분석
   - 기본값: 심층

[선택 입력]
6. 특정 이벤트 / 촉매: > 없음 / 실적 / 가이던스 / M&A / 규제 / 소송 / 신제품 / 관세 / 수주 / 공급망
   - 이벤트가 없으면 "없음" 또는 공란
   - 예시: 최근 실적 발표 / 가이던스 하향 / M&A / 규제 / 소송 / 신제품 발표 / 관세 이슈 / 고객사 수주 / 공급망 이슈

나머지는 기본값으로 진행합니다.
- 분석 기준일: 작업 당일
- 투자자 유형: 혼합형
- 기준 통화: 상장 통화
- 회계 기준: 회사 공시 기준
- 기술적 분석 포함 여부: 포함
- 최종 의견 형식: Rating + Price Target + 시나리오별 전략
```

<!-- END INPUT_GATE_POLICY_INTEGRATED -->

### 0. 실행 workspace 준비

1. 현재 실행의 작업 디렉터리를 `ACTIVE_WORKSPACE`로 정한다. 기본값은 `_workspace_{TICKER_OR_SLUG}_{YYYYMMDD}/` 형식의 동적 workspace 절대 경로다.
2. 새 리서치를 시작하기 전에 `ACTIVE_WORKSPACE`에 기존 산출물이 있는지 확인한다.
3. 기존 산출물이 있으면 삭제하거나 그대로 덮어쓰지 않는다. 먼저 `_workspace_runs/<YYYY-MM-DD>-<ticker-or-slug>/`로 이동해 보존한다.
4. archive 경로가 이미 있으면 `-HHMMSS` 또는 `-2`처럼 충돌 없는 suffix를 붙인다.
5. 기본 동작은 move다. 권한 또는 런타임 제약 때문에 move할 수 없을 때만 copy를 사용하고, copy 결과를 확인하기 전에는 기존 파일을 비우지 않는다.
6. archive가 끝난 뒤 새 `ACTIVE_WORKSPACE`를 만들고, 모든 하위 역할과 후속 읽기 단계에 같은 절대 경로를 전달한다.

### 1. 입력 수집 게이트

1. 사용자 원문 요청을 보존한다.
2. 원문에서 기업명 또는 티커를 파싱한다.
3. 기업명 또는 티커 중 하나라도 있으면 공식 출처와 금융 데이터 소스를 통해 대상 기업명, 티커, 거래소/국가, 상장 통화, 회계 기준을 자동 확인한다.
4. 식별 결과가 단일 후보이면 `ready`로 진행할 수 있다.
5. 식별자가 없거나 복수 후보·충돌이 있으면 `needs_user_input` 또는 `blocked`로 판정한다.
6. 식별이 끝나면 사용자에게 `진행 방식`, `분석 초점`, `투자 기간`, `비교기업 수`, `보고서 깊이` 다섯 가지 옵션만 확인한다.
7. 각 선택 문구에는 `> 일괄 / 순차`처럼 간단 선택지 힌트를 함께 표시한다.
8. 특정 이벤트 / 촉매가 있으면 선택 입력으로 보존한다.
9. 그 외 항목은 기본값으로 적용하되 `${ACTIVE_WORKSPACE}/00_input/request-summary.md`에 남긴다.
10. `docs/harness/invest/templates/input-intake.md` 형식으로 `${ACTIVE_WORKSPACE}/00_input/input-intake.md`를 작성한다.

완료 기준:

- `${ACTIVE_WORKSPACE}/00_input/input-intake.md`가 존재한다.
- 기업명 또는 티커 기반 자동 식별 결과가 명시되어 있다.
- 사용자에게 되물은 항목은 다섯 가지 옵션으로 제한되어 있다.
- 분석 초점 선택지는 장기 기본형 / 최근 분기 실적·센티먼트 심층형 / 혼합형 세 가지다.
- 이벤트는 독립 모드가 아니라 선택 촉매로 기록되어 있다.
- 보고서 깊이 기본값은 `심층형`이고, 분석 초점 기본값은 `혼합형`이다.
- `ready`가 아닌 상태에서는 전문가 분석을 시작하지 않는다.

### 2. 입력 정규화

1. 입력 수집 게이트가 `ready`인지 확인한다.
2. 사용자 원문 요청과 게이트 결과를 보존한다.
3. 자동 식별 결과와 선택 옵션, 선택 이벤트를 정리한다.
4. 기본값, 해석한 가정, 제외 범위를 분리한다.
5. `docs/harness/invest/templates/request-summary.md` 형식으로 `${ACTIVE_WORKSPACE}/00_input/request-summary.md`를 작성한다.
6. `docs/harness/invest/templates/market-price-snapshot.md` 형식으로 `${ACTIVE_WORKSPACE}/00_input/market-price-snapshot.md`를 작성한다.

완료 기준:

- 기업명 또는 티커 기반 자동 식별이 완료되어 있다.
- `${ACTIVE_WORKSPACE}/00_input/input-intake.md`의 게이트 결과가 요약되어 있다.
- `${ACTIVE_WORKSPACE}/00_input/market-price-snapshot.md`에 기준 주가, 기준일, 출처, 주식 수, 주요 시장지표 계산 입력이 남아 있다.
- 기본값을 적용한 항목이 별도 표에 남아 있다.
- 분석 초점과 진행 방식이 명시되어 있다.
- 특정 이벤트 / 촉매가 있으면 별도 행으로 남아 있다.
- 분석 제외 범위와 기술적 분석 포함 여부가 명시되어 있다.

### 3. 전문가 분석 분배

아래 역할은 같은 입력 스냅샷을 사용한다. 특정 산출물이 다른 역할의 전제에 필요하면 해당 파일을 명시적으로 함께 전달한다.

| 역할 | 담당 범위 | 스킬 | 산출물 |
|---|---|---|---|
| financial-analyst | Part II, III | `.agents/skills/financial-analyst/SKILL.md` | `${ACTIVE_WORKSPACE}/01_financial/findings.md` |
| fundamental-analyst | Part IV, V, VI, VII | `.agents/skills/fundamental-analyst/SKILL.md` | `${ACTIVE_WORKSPACE}/02_fundamental/findings.md` |
| valuation-analyst | Part VIII | `.agents/skills/valuation-analyst/SKILL.md` | `${ACTIVE_WORKSPACE}/03_valuation/findings.md`, 선택 시 `${ACTIVE_WORKSPACE}/03_valuation/comps.md`, `${ACTIVE_WORKSPACE}/03_valuation/dcf.md` |
| technical-analyst | Part IX | `.agents/skills/technical-analyst/SKILL.md` | `${ACTIVE_WORKSPACE}/04_technical/findings.md` |
| macro-sentiment-analyst | Part X, XI | `.agents/skills/macro-sentiment-analyst/SKILL.md` | `${ACTIVE_WORKSPACE}/05_macro_sentiment/findings.md` |
| risk-scenario-analyst | Part XII, XIII | `.agents/skills/risk-scenario-analyst/SKILL.md` | `${ACTIVE_WORKSPACE}/06_risk_scenario/findings.md` |

분배 규칙:

- 각 역할에는 자신의 출력 계약과 공통 입력 파일만 전달한다.
- **delegate_task 사용 시 절대 경로 명시:** 서브에이전트는 자신의 기본 워크스페이스에 파일을 저장할 수 있으므로, 현재 실행의 동적 workspace 절대 경로를 `ACTIVE_WORKSPACE`로 전달한다. `write_file`과 `read_file` 경로는 `${ACTIVE_WORKSPACE}/01_financial/findings.md`처럼 통일하고, 후속 단계에서도 동일한 절대 경로를 사용한다. Hermes 기본 workspace가 있더라도 모든 실행은 명시적으로 전달된 `ACTIVE_WORKSPACE`를 사용한다.
- 핵심 수치에는 출처, 기준일, 회계기간, 통화, 산식이 필요하다고 명시한다.
- 데이터가 부족한 경우 추정하지 않고 `공식 자료 미확인`, `데이터 부족`, `추가 확인 필요`를 사용하게 한다.
- 기술적 분석 제외 요청이 있으면 `technical-analyst`는 생략 사유와 보조 신호 부재의 한계만 기록한다.

> **Pitfall — Group 2 내부 순환 오류:** `technical-analyst`, `macro-sentiment-analyst`, `risk-scenario-analyst`를 동일한 `delegate_task`의 같은 `tasks` 배열에 담으면 서브에이전트 간 순환 의존성이 발생한다. `risk-scenario-analyst`가 `04_technical`과 `05_macro_sentiment`을 읽으려고 할 때 파일이 아직 생성되지 않은 채로 판단할 수 있다. `risk-scenario-analyst`는 선행 산출물(01~05)이 모두 존재하는 것을 확인한 후에 독립적으로 실행하거나, 혹은 단일 `delegate_task`에서 모든 6개 역할을 한 번에 담으면 순환을 방지할 수 있다.

### 4. 중간 산출물 점검

1. `${ACTIVE_WORKSPACE}/01_financial/findings.md`부터 `${ACTIVE_WORKSPACE}/06_risk_scenario/findings.md`까지 존재 여부를 확인한다.
2. `${ACTIVE_WORKSPACE}/00_input/market-price-snapshot.md`가 valuation과 QA의 기준 주가로 사용되는지 확인한다.
3. 각 파일의 분석 전제, 출처 목록, 요약, 데이터 한계 섹션을 확인한다.
4. 수치나 판단이 충돌하면 `${ACTIVE_WORKSPACE}/06_risk_scenario/conflicts.md`에 기록한다.
5. 누락이 치명적이면 해당 역할에 보강을 요청한다.

충돌 기록 기준:

| 충돌 유형 | 처리 |
|---|---|
| 수치 충돌 | 출처, 기준일, 회계기간, 산식 차이를 표로 비교한다. |
| 판단 충돌 | 어떤 전제 차이가 결론 차이를 만들었는지 적는다. |
| 데이터 신선도 충돌 | 최신 자료 우선순위를 적용하되, 오래된 자료 사용 한계를 남긴다. |

### 5. 초안 합성

`report-synthesizer`가 아래 입력을 읽고 `${ACTIVE_WORKSPACE}/07_draft/report.md`를 작성한다.

- `${ACTIVE_WORKSPACE}/00_input/request-summary.md`
- `${ACTIVE_WORKSPACE}/00_input/market-price-snapshot.md`
- `${ACTIVE_WORKSPACE}/01_financial/findings.md`
- `${ACTIVE_WORKSPACE}/02_fundamental/findings.md`
- `${ACTIVE_WORKSPACE}/03_valuation/findings.md`
- `${ACTIVE_WORKSPACE}/04_technical/findings.md`
- `${ACTIVE_WORKSPACE}/05_macro_sentiment/findings.md`
- `${ACTIVE_WORKSPACE}/06_risk_scenario/findings.md`
- 필요 시 `${ACTIVE_WORKSPACE}/06_risk_scenario/conflicts.md`
- 필요 시 `${ACTIVE_WORKSPACE}/03_valuation/comps.md`
- 필요 시 `${ACTIVE_WORKSPACE}/03_valuation/dcf.md`
- 필요 시 `${ACTIVE_WORKSPACE}/00_input/earnings-update.md`

초안은 `invest_prompt_v2.md`의 최종 출력 템플릿 18개 섹션 순서를 따른다.

### 6. QA

`qa-reviewer`가 `${ACTIVE_WORKSPACE}/07_draft/report.md`와 원천 findings 전체를 검토하고 `${ACTIVE_WORKSPACE}/09_qa/review.md`, `${ACTIVE_WORKSPACE}/09_qa/fix-list.md`, `${ACTIVE_WORKSPACE}/09_qa/final-check.md`를 작성한다.

QA 판정:

| 판정 | 의미 | 후속 조치 |
|---|---|---|
| 승인 | 치명적 결함 없음 | 최종본 확정 가능 |
| 수정 후 승인 | 제한적 결함 있음 | 오케스트레이터가 수정 후 최종본 확정 |
| 재검토 필요 | 출처, 구조, 결론 정합성에 치명적 결함 있음 | 관련 역할 보강 후 초안 재작성 |

### 7. 최종본 확정

1. QA 지적을 반영한다.
2. 최종 보고서를 `${ACTIVE_WORKSPACE}/08_final/report.md`에 저장한다.
3. 사용자 전달용 핵심 요약이 필요하면 `${ACTIVE_WORKSPACE}/08_final/executive-summary.md`를 추가로 작성한다.
4. 최종 응답에는 리포트 위치, QA 상태, 남은 한계를 짧게 알린다.

## Handoff Files

<!-- BEGIN YFINANCE_MCP_TOOLS -->
## MCP 도구 라우팅 지침

두 개의 MCP 서버가 설치되어 있으며, 대상 시장에 따라 사용 전략이 다르다.

### 시장별 전략

| 대상 시장 | 1순위 | 2순위 (보조) | 비고 |
|---|---|---|---|
| 한국 (코스피/코스닥/코넥스) | `korea-stock` (DART/KRX 공식 API) | `yfinance` (Yahoo Finance) | 공식 데이터 우선, yfinance는 보충용 |
| 미국 (NYSE/NASDAQ) | `yfinance` (Yahoo Finance) | web_search (EDGAR 등) | yfinance가 주력 |
| 그 외 글로벌 | `yfinance` (Yahoo Finance) | web_search | yfinance가 유일한 MCP 데이터 소스 |

### 한국 기업 분석 시 yfinance 병행 사용 예시

| 항목 | korea-stock (1순위) | yfinance (보조) |
|---|---|---|
| 기업 식별 | `get_corp_code(stock_code="005930")` | `yfinance_search(query="Samsung")` |
| 재무제표 | `get_financial_statement(corp_code=..., ...)` | `yfinance_get_financials(symbol="005930.KS")` |
| 주가 데이터 | `get_stock_trade_info(codeList=["005930"], ...)` | `yfinance_get_price_history(symbol="005930.KS")` |
| 글로벌 피어 비교 | 불가능 | `yfinance_get_ticker_info(symbol="AAPL")` 등 |
| 뉴스 | `get_disclosure_list` (공식 공시만) | `yfinance_get_ticker_news(symbol="005930.KS")` |

### 기업 식별 흐름 (orchestrator 우선 수행)

1. 사용자 입력에서 기업명 또는 티커 파싱
2. 한국 기업 의심 시: `get_corp_code`로 DART 고유번호 + 종목코드 조회
3. 글로벌 기업 또는 한국 기업 확인용: `yfinance_search(query=...)`로 Yahoo Finance symbol 획득
4. 두 결과를 교차 검증하여 단일 후보 확정
5. 확정된 식별자(corp_code, stock_code, yahoo_symbol)를 각 전문가 역할에 전달

### yfinance symbol 규칙

| 시장 | symbol 형식 | 예시 |
|---|---|---|
| 미국 | 티커 그대로 | AAPL, MSFT, GOOGL |
| 한국 | 6자리코드.KS 또는 .KQ | 005930.KS (코스피), 035420.KQ (코스닥) |
| 일본 | 숫자.T | 6758.T (소니) |
| 기타 | 보통 XXX.XX 형식 | 종목 검색으로 확인 필요 |

<!-- END YFINANCE_MCP_TOOLS -->

<!-- BEGIN KOREA_STOCK_MCP_TOOLS -->
## MCP 도구 활용 지침

korea-stock-mcp MCP 서버가 설치되어 있으면 한국 상장기업 분석 시 아래 도구를 사용할 수 있다.

| 도구 | 역할 | 사용 주체 |
|---|---|---|
| `get_corp_code` | DART 고유번호/종목코드 조회 | 오케스트레이터가 먼저 호출, 결과를 모든 역할에 전달 |
| `get_disclosure_list` | 공시 검색 | fundamental-analyst, macro-sentiment-analyst |
| `get_disclosure` | 공시 원문 조회 | fundamental-analyst, macro-sentiment-analyst |
| `get_financial_statement` | XBRL 재무제표 | financial-analyst, valuation-analyst |
| `get_stock_base_info` | 종목 기본정보 | financial-analyst, fundamental-analyst |
| `get_stock_trade_info` | 일별 주가/거래량 | technical-analyst, macro-sentiment-analyst |
| `get_market_type` | 상장시장 확인 | 모든 역할 (기업 식별 확인용) |
| `get_today_date` | 오늘 날짜 | 오케스트레이터 (기준일 확인용) |

오케스트레이터는 입력 수집 게이트에서 한국 기업이라고 판단되면 `get_corp_code`를 먼저 호출하여 `corp_code`와 `stock_code`를 확보한 후, 이를 각 전문가 역할의 입력에 포함시킨다.

한국 기업이 아닌 경우 MCP 도구를 사용할 수 없으며, 기존 웹 검색 방식으로 데이터를 수집한다.
<!-- END KOREA_STOCK_MCP_TOOLS -->

| 순서 | 경로 | 소유 역할 | 필수 내용 |
|---|---|---|---|
| 00a | `${ACTIVE_WORKSPACE}/00_input/input-intake.md` | invest-orchestrator | 원문 요청, 자동 식별 결과, 선택 옵션, 특정 이벤트 / 촉매, 게이트 상태 |
| 00b | `${ACTIVE_WORKSPACE}/00_input/request-summary.md` | invest-orchestrator | 정규화 입력값, 기본 가정, 분석 범위, 제외 범위 |
| 00c | `${ACTIVE_WORKSPACE}/00_input/market-price-snapshot.md` | invest-orchestrator / valuation-analyst | 기준 주가, 기준일, 가격 출처, 주식 수, 시장지표 계산 입력 |
| 00d | `${ACTIVE_WORKSPACE}/00_input/earnings-update.md` | earnings-update | 최신 또는 지정 분기 실적, 컨센서스 대비, 가이던스, Rating/Price Target 영향 |
| 00e | `${ACTIVE_WORKSPACE}/00_input/earnings-preview.md` | earnings-preview | 예정 실적 핵심 지표, 기대치, Beat/Miss 시나리오, 발표 후 업데이트 항목 |
| 00u | `${ACTIVE_WORKSPACE}/00_input/update-plan.md` | report-updater | 기존 리포트 갱신 범위, 재실행 command/skill, Rating/Price Target 재검증 필요 여부 |
| 00s1 | `${ACTIVE_WORKSPACE}/00_screen/screen-criteria.md` | idea-screener | 스크리닝 원문, 포함/제외 기준, 데이터 소스 계획 |
| 00s2 | `${ACTIVE_WORKSPACE}/00_screen/candidate-universe.md` | idea-screener | 후보군, 식별자, 포함/제외 사유 |
| 00s3 | `${ACTIVE_WORKSPACE}/00_screen/idea-scorecard.md` | idea-screener | 후보별 점수표, 예비 Rating, 주요 리스크 |
| 00s4 | `${ACTIVE_WORKSPACE}/00_screen/shortlist.md` | idea-screener | 최종 후보, 투자 논지, 다음 단계 |
| 01 | `${ACTIVE_WORKSPACE}/01_financial/findings.md` | financial-analyst | 기업 개요, 재무제표, 비율, 최근 이벤트 |
| 02 | `${ACTIVE_WORKSPACE}/02_fundamental/findings.md` | fundamental-analyst | 산업/경쟁, 경영진, 해자, 제품·서비스 |
| 03 | `${ACTIVE_WORKSPACE}/03_valuation/findings.md` | valuation-analyst | 멀티플 비교, DCF 가정, 시나리오별 가치 |
| 03a | `${ACTIVE_WORKSPACE}/03_valuation/comps.md` | valuation-analyst | 피어 그룹, 멀티플 비교, 프리미엄/디스카운트 해석 |
| 03b | `${ACTIVE_WORKSPACE}/03_valuation/dcf.md` | valuation-analyst | DCF 가정, Bear/Base/Bull 결과, comps/역사적 밴드 교차검증 |
| 04 | `${ACTIVE_WORKSPACE}/04_technical/findings.md` | technical-analyst | 추세, 지표, 지지·저항, 기술적 리스크 |
| 05 | `${ACTIVE_WORKSPACE}/05_macro_sentiment/findings.md` | macro-sentiment-analyst | 뉴스, 센티먼트, 거시·정책 영향 |
| 05a | `${ACTIVE_WORKSPACE}/05_macro_sentiment/thesis-update.md` | thesis-tracker | 기존 투자 논지 대비 새 데이터, 강화/약화 증거, 다음 추적 지표 |
| 05b | `${ACTIVE_WORKSPACE}/05_macro_sentiment/catalysts.md` | catalyst-tracker | 촉매 이벤트 캘린더, 확인 지표, 후속 작업 |
| 05c | `${ACTIVE_WORKSPACE}/05_macro_sentiment/morning-note.md` | morning-note | 관심종목/테마 일일 점검, 우선순위, 후속 command |
| 06 | `${ACTIVE_WORKSPACE}/06_risk_scenario/findings.md` | risk-scenario-analyst | 리스크 등록부, 시나리오 표, 촉발 요인 |
| 06a | `${ACTIVE_WORKSPACE}/06_risk_scenario/conflicts.md` | invest-orchestrator | 출처 충돌, 수치 충돌, 해석 충돌 |
| 07 | `${ACTIVE_WORKSPACE}/07_draft/report.md` | report-synthesizer | 통합 초안 전체 |
| 08 | `${ACTIVE_WORKSPACE}/08_final/report.md` | invest-orchestrator | QA 반영 완료 최종본 |
| 08h | `${ACTIVE_WORKSPACE}/08_final/report.html` | html-report-synthesizer | Markdown 최종 리포트의 정적 HTML 출력 |
| 08a | `${ACTIVE_WORKSPACE}/08_final/executive-summary.md` | invest-orchestrator | 선택적 사용자 요약본 |
| 09 | `${ACTIVE_WORKSPACE}/09_qa/review.md` | qa-reviewer | 결함 목록, 수정 요청, 승인 여부 |
| 09a | `${ACTIVE_WORKSPACE}/09_qa/fix-list.md` | qa-reviewer | 수정 작업 목록, 담당 산출물, 완료 여부 |
| 09b | `${ACTIVE_WORKSPACE}/09_qa/final-check.md` | qa-reviewer | 최종 승인 전 확인표 |

## Failure Policy

- 기업 식별 정보가 부족하면 분석을 중단하고 보완 필요 항목을 적는다.
- 특정 전문가 산출물이 누락되면 1회 보강을 요청한다.
- 보강 후에도 부족하면 최종 리포트의 한계 섹션에 미완료 범위와 영향도를 명시한다.
- 출처 충돌은 임의 평균이나 임의 선택으로 해결하지 않는다.
- QA에서 치명적 결함이 나오면 `${ACTIVE_WORKSPACE}/08_final/report.md`를 확정하지 않는다.

## Validation

최종 확정 전 아래 명령을 Windows PowerShell에서 실행한다.

```powershell
.\scripts\Test-HarnessStructure.ps1
```

검증 기준:

- 모든 필수 스킬과 문서가 존재한다.
- 모든 `SKILL.md`가 YAML frontmatter의 `name`, `description`을 가진다.
- `team-spec.md`, 오케스트레이터 스킬, 템플릿의 필수 핸드오프 경로가 서로 맞는다.
- 빈 역할 스킬 디렉터리가 남아 있지 않다.

## Boundaries

- 이 스킬은 투자 리포트 생성 과정을 조율하는 Harness이며, 특정 종목에 대한 개인화된 투자 자문을 제공하지 않는다.
- 오케스트레이터는 전문가 스킬의 분석을 대신 발명하지 않는다.
- 최신 시장 데이터가 필요한 실제 리포트 생성 시에는 반드시 현재 기준으로 출처를 확인한다.
