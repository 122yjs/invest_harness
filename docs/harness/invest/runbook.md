# 투자 리서치 Harness 실행 가이드

## 목적

<!-- BEGIN INPUT_GATE_POLICY_INTEGRATED -->
## 통합 입력 게이트 및 분석 초점 정책

### 1. 자동 식별

- 사용자가 기업명 또는 티커 중 하나만 제공해도 오케스트레이터가 자동 식별을 시도한다.
- 자동 식별 대상은 대상 기업명, 티커, 거래소/국가, 상장 통화, 회계 기준이다.
- 처음부터 기업명, 티커, 거래소/국가 3개를 모두 요구하지 않는다.
- 복수 후보, 티커 중복, ADR/보통주/우선주 구분, 상장폐지, 기업명-티커 충돌이 있으면 사용자 확인 전까지 전문가 분석을 시작하지 않는다.

### 2. 사용자에게 되물을 옵션

사용자에게 되물을 항목은 다섯 가지로 제한한다. 각 항목에는 간단 선택지 힌트를 함께 제공한다.

| 항목 | 간단 선택지 | 전체 선택지 | 기본값 |
|---|---|---|---|
| 진행 방식 | `> 일괄 / 순차` | 전체 일괄 생성 / 순차 단계별 생성 | 일괄 |
| 분석 초점 | `> 장기 / 분기 / 혼합` | 장기 기본형 / 최근 분기 실적·센티먼트 심층형 / 혼합형 | 혼합 |
| 투자 기간 | `> 단기 / 중기 / 장기 / 전체` | 1~3개월 / 6~12개월 / 3~5년 / 전체 | 전체 |
| 비교기업 수 | `> 3 / 5 / 10 / 직접` | 3개 / 5개 / 10개 / 직접 지정 | 5 |
| 보고서 깊이 | `> 요약 / 표준 / 심층` | 요약형 / 표준형 / 심층형 | 심층 |

선택 입력:

| 항목 | 간단 선택지 | 처리 |
|---|---|---|
| 특정 이벤트 / 촉매 | `> 없음 / 실적 / 가이던스 / M&A / 규제 / 소송 / 신제품 / 관세 / 수주 / 공급망` | 최근 분기 실적·센티먼트 분석의 하위 축 |

### 3. 자동 기본값

| 항목 | 기본값 |
|---|---|
| 분석 기준일 | 작업 당일 |
| 투자자 유형 | 혼합형 |
| 기준 통화 | 상장 통화 |
| 회계 기준 | 회사 공시 기준 |
| 기술적 분석 포함 여부 | 포함하되 장기 리포트에서는 보조 신호로 제한 |
| 최종 의견 형식 | Rating + Price Target + 시나리오별 전략 |

### 4. 분석 초점 구성

상위 `분석 초점` 선택지는 세 개만 둔다.

| 분석 초점 | 의미 |
|---|---|
| 장기 기본형 | 최근 3~5년 연간 재무, 산업, 해자, 밸류에이션 중심 |
| 최근 분기 실적·센티먼트 심층형 | 최근 4~8개 분기 실적, 컨센서스, 어닝콜, 뉴스·수급·애널리스트 리비전 중심 |
| 혼합형 | 장기 구조 분석 + 최근 분기 실적·센티먼트 심층 비교 |

`이벤트 드리븐형`은 상위 분석 초점에서 제외한다. 이벤트는 독립 옵션이 아니라 `특정 이벤트 / 촉매` 선택 입력으로 처리한다.

이벤트가 입력되면 다음 방식으로 반영한다.

- `최근 분기 실적·센티먼트 심층형`: 이벤트 전후 실적, 뉴스, 리비전, 주가·거래량 반응을 심층 분석
- `혼합형`: 장기 논지에 이벤트가 미치는 영향을 별도 하위 섹션으로 분석
- `장기 기본형`: 이벤트가 장기 투자 논지를 훼손하거나 강화하는 경우에만 리스크 또는 촉매로 반영

## 간단 선택지 표기 규칙

입력 게이트에서 각 문구에는 짧은 선택지 힌트를 함께 제공한다.

| 항목 | 간단 선택지 | 전체 의미 |
|---|---|---|
| 진행 방식 | `> 일괄 / 순차` | 전체 일괄 생성 / 순차 단계별 생성 |
| 분석 초점 | `> 장기 / 분기 / 혼합` | 장기 기본형 / 최근 분기 실적·센티먼트 심층형 / 혼합형 |
| 투자 기간 | `> 단기 / 중기 / 장기 / 전체` | 1~3개월 / 6~12개월 / 3~5년 / 전체 |
| 비교기업 수 | `> 3 / 5 / 10 / 직접` | 피어 수 자동 선정 또는 직접 지정 |
| 보고서 깊이 | `> 요약 / 표준 / 심층` | 요약형 / 표준형 / 심층형 |
| 특정 이벤트 / 촉매 | `> 없음 / 실적 / 가이던스 / M&A / 규제 / 소송 / 신제품 / 관세 / 수주 / 공급망` | 선택 입력 |

<!-- END INPUT_GATE_POLICY_INTEGRATED -->

이 문서는 `invest_prompt_v2.md`와 `.agents/skills/*`를 반복적으로 사용해 개별 주식 투자 리포트를 생성하는 절차를 정의한다. macOS/Linux는 Python 검증 경로를 기본으로 사용하고, Windows는 PowerShell 검증 경로를 사용한다.

## 반복 실행 workspace 보존

1. 현재 실행의 작업 디렉터리를 `ACTIVE_WORKSPACE`로 정한다. 기본값은 `_workspace_{TICKER_OR_SLUG}_{YYYYMMDD}/` 형식의 동적 workspace 절대 경로다.
2. 새 리서치를 시작하기 전에 `ACTIVE_WORKSPACE`에 기존 산출물이 있는지 확인한다.
3. 기존 산출물이 있으면 삭제하거나 덮어쓰지 말고 `_workspace_runs/<YYYY-MM-DD>-<ticker-or-slug>/`로 먼저 이동한다.
4. 같은 archive 경로가 이미 있으면 `-HHMMSS` 또는 `-2`처럼 충돌 없는 suffix를 붙인다.
5. 기본 동작은 move다. 권한 또는 런타임 제약 때문에 move가 불가능할 때만 copy를 사용하고, copy 결과를 확인하기 전에는 기존 파일을 비우지 않는다.
6. archive가 끝난 뒤 새 `${ACTIVE_WORKSPACE}/`를 만들고, 모든 하위 역할에 같은 `ACTIVE_WORKSPACE` 절대 경로를 전달한다.
7. `${ACTIVE_WORKSPACE}/`는 현재 실행 전용이고, `_workspace_runs/`는 이전 실행의 감사/재현 archive다.

## 0. 진입 입력 수집 게이트

1. 사용자 원문 요청을 그대로 보존한다.
2. 원문에서 기업명 또는 티커를 파싱한다.
3. 기업명 또는 티커 중 하나라도 있으면 대상 기업명, 티커, 거래소/국가, 상장 통화, 회계 기준을 자동 확인한다.
4. 자동 식별이 단일 후보로 끝나면 사용자에게 다섯 가지 선택 옵션만 확인한다.
5. 자동 식별이 불가능하거나 복수 후보가 나오면 사용자에게 식별자 보완을 요청한다.
6. 특정 이벤트 / 촉매가 있으면 선택 입력으로 기록한다.
7. 모든 선택 문구에는 `> 일괄 / 순차`처럼 간단 선택지 힌트를 함께 제공한다.
8. `docs/harness/invest/templates/input-intake.md`를 기준으로 `${ACTIVE_WORKSPACE}/00_input/input-intake.md`를 작성한다.

사용자에게 확인할 선택 옵션:

| 항목 | 간단 선택지 | 기본값 |
|---|---|---|
| 진행 방식 | `> 일괄 / 순차` | 일괄 |
| 분석 초점 | `> 장기 / 분기 / 혼합` | 혼합 |
| 투자 기간 | `> 단기 / 중기 / 장기 / 전체` | 전체 |
| 비교기업 수 | `> 3 / 5 / 10 / 직접` | 5 |
| 보고서 깊이 | `> 요약 / 표준 / 심층` | 심층 |

선택 입력:

| 항목 | 간단 선택지 | 처리 |
|---|---|---|
| 특정 이벤트 / 촉매 | `> 없음 / 실적 / 가이던스 / M&A / 규제 / 소송 / 신제품 / 관세 / 수주 / 공급망` | 최근 분기 실적·센티먼트 분석의 하위 축으로 반영 |

나머지 기본값:

| 항목 | 기본값 |
|---|---|
| 분석 기준일 | 작업 당일 |
| 투자자 유형 | 혼합형 |
| 기준 통화 | 상장 통화 |
| 회계 기준 | 회사 공시 기준 |
| 기술적 분석 포함 여부 | 포함 |
| 최종 의견 형식 | Rating + Price Target + 시나리오별 전략 |

필수 보완 입력 폼:

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


게이트 상태:

| 상태 | 의미 |
|---|---|
| `ready` | 정규화 진행 가능 |
| `needs_user_input` | 사용자 보완 입력 필요 |
| `blocked` | 대상 식별 충돌로 중단 |

## 1. 입력 정리

1. 입력 수집 게이트 상태가 `ready`인지 확인한다.
2. 자동 식별된 기업명, 티커, 거래소/국가, 상장 통화, 회계 기준을 확인한다.
3. 사용자가 선택한 진행 방식, 분석 초점, 투자 기간, 비교기업 수, 보고서 깊이를 기록한다.
4. 특정 이벤트 / 촉매가 있으면 선택 입력으로 기록한다.
5. 미지정 선택 옵션은 기본값을 적용한다.
6. `docs/harness/invest/templates/request-summary.md`를 기준으로 `${ACTIVE_WORKSPACE}/00_input/request-summary.md`를 작성한다.
7. `docs/harness/invest/templates/market-price-snapshot.md`를 기준으로 `${ACTIVE_WORKSPACE}/00_input/market-price-snapshot.md`를 작성한다.

필수 확인:

- `${ACTIVE_WORKSPACE}/00_input/input-intake.md`에 게이트 결과가 남아 있는지 확인한다.
- `${ACTIVE_WORKSPACE}/00_input/market-price-snapshot.md`에 기준 주가, 기준일, 출처, 주식 수, 주요 시장지표 계산 입력이 남아 있는지 확인한다.
- 자동 식별 결과와 사용자 원문이 충돌하지 않는지 확인한다.
- 분석 초점 선택지는 세 가지로 제한한다.
- 이벤트 드리븐은 독립 모드가 아니라 선택 촉매로 처리한다.
- 보고서 깊이 기본값은 `심층형`이고, 분석 초점 기본값은 `혼합형`이다.
- 진행 방식이 `순차 단계별 생성`이면 각 파트 종료 후 다음 단계 진행 여부를 묻는다.
- 진행 방식이 `전체 일괄 생성`이면 PART 전체를 한 번에 실행한다.

## 2. 병렬 분석 산출물 생성

아래 전문가 스킬을 사용해 산출물을 만든다.

| 스킬 | 산출물 |
|---|---|
| `financial-analyst` | `${ACTIVE_WORKSPACE}/01_financial/findings.md` |
| `fundamental-analyst` | `${ACTIVE_WORKSPACE}/02_fundamental/findings.md` |
| `valuation-analyst` | `${ACTIVE_WORKSPACE}/03_valuation/findings.md`, 선택 시 `${ACTIVE_WORKSPACE}/03_valuation/comps.md`, `${ACTIVE_WORKSPACE}/03_valuation/dcf.md` |
| `technical-analyst` | `${ACTIVE_WORKSPACE}/04_technical/findings.md` |
| `macro-sentiment-analyst` | `${ACTIVE_WORKSPACE}/05_macro_sentiment/findings.md` |
| `risk-scenario-analyst` | `${ACTIVE_WORKSPACE}/06_risk_scenario/findings.md` |

공통 규칙:

- 모든 핵심 수치에는 출처, 기준일, 회계기간, 통화, 산식을 붙인다.
- 데이터 부족 시 추정하지 않고 `공식 자료 미확인`, `데이터 부족`, `추가 확인 필요`로 표기한다.
- 충돌이 있으면 `${ACTIVE_WORKSPACE}/06_risk_scenario/conflicts.md`에 남긴다.

## 3. 초안 합성

`report-synthesizer`를 사용해 `${ACTIVE_WORKSPACE}/07_draft/report.md`를 작성한다.

초안은 아래 18개 섹션을 반드시 포함한다.

1. Executive Summary
2. 기업 개요
3. 핵심 투자 포인트
4. 재무 분석
5. 산업 및 경쟁 환경
6. 경영진 및 거버넌스
7. 경제적 해자
8. 제품 및 서비스
9. 밸류에이션
10. 기술적 분석
11. 뉴스 및 센티먼트
12. 거시경제 및 정책 환경
13. 리스크 분석
14. 시나리오 분석
15. Rating, Price Target 및 투자 의견
16. 투자 기간별 전략과 Risk-Reward
17. 모니터링 체크리스트
18. 한계 및 추가 확인 필요 사항

## 4. QA 및 최종본

1. `qa-reviewer`로 `${ACTIVE_WORKSPACE}/09_qa/review.md`, `${ACTIVE_WORKSPACE}/09_qa/fix-list.md`, `${ACTIVE_WORKSPACE}/09_qa/final-check.md`를 작성한다.
2. QA 판정이 `승인` 또는 `수정 후 승인`인지 확인한다.
3. 치명적 결함이 있으면 `${ACTIVE_WORKSPACE}/09_qa/fix-list.md`를 기준으로 관련 findings를 보강하고 초안 합성을 다시 실행한다.
4. 최종본은 `${ACTIVE_WORKSPACE}/08_final/report.md`에 저장한다.
5. 사용자 전달용 짧은 요약이 필요하면 `${ACTIVE_WORKSPACE}/08_final/executive-summary.md`를 작성한다.

## 5. Command runtime smoke

Slash command 런타임은 command stub을 실행 로직으로 확장하지 않는다. 역할은 입력 파싱, thin wrapper 메타데이터 검증, `${ACTIVE_WORKSPACE}` 생성, mapped skill로 넘길 dispatch handoff 기록까지다.

예시:

```bash
python3 scripts/invest_command_runtime.py "/screen AI 전력 인프라 2차 수혜주"
python3 scripts/invest_command_runtime.py "/earnings TSLA Q1 2026"
python3 scripts/invest_command_runtime.py "/dcf AAPL base"
```

각 실행은 `${ACTIVE_WORKSPACE}/00_input/command-dispatch.json`을 만들고, 실제 분석 산출물은 mapped skill이 작성해야 할 `expected_outputs`로만 기록한다.

## 6. 구조 검증

macOS/Linux에서는 Python 검증 경로를 기본으로 사용한다. 이 경로는 전역 PowerShell 설치가 없어도 동작해야 한다.

```bash
python3 scripts/verify_invest_harness.py
```

Windows에서는 기존 PowerShell 검증 경로를 사용한다.

```powershell
pwsh ./scripts/Sync-InvestSkills.ps1
pwsh ./scripts/Test-SkillDrift.ps1
pwsh ./scripts/Test-CommandRuntime.ps1
pwsh ./scripts/Test-WorkspaceSafety.ps1
pwsh ./scripts/Test-HarnessStructure.ps1
```

검증이 실패하면 메시지에 나온 경로, frontmatter, sync drift, 또는 workspace safety 위반을 수정한 뒤 다시 실행한다.

## 7. 운영 원칙

- 최신 데이터가 필요한 실제 종목 분석에서는 반드시 현재 기준으로 웹 또는 공식 공시를 확인한다.
- 기술적 분석과 소셜 센티먼트는 보조 신호로만 사용한다.
- 최종 보고서는 정보 제공용 분석이며 개인화된 투자 자문이 아니다.
- `${ACTIVE_WORKSPACE}/`의 기존 산출물은 새 실행 전 `_workspace_runs/`로 archive하여 감사와 재현을 위해 보존한다.
