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

## Required Inputs

먼저 사용자가 제공한 원문 입력을 보존하고, 아래 항목을 `_workspace/00_input/request-summary.md`에 정규화한다.

| 항목 | 기본 처리 |
|---|---|
| 대상 기업명 | 필수. 불명확하면 리포트 생성을 시작하지 않는다. |
| 티커 | 필수. 거래소와 상충하면 확인 필요로 표시한다. |
| 거래소 / 국가 | 필수. 국가와 회계 기준, 통화 선택의 기준으로 사용한다. |
| 분석 기준일 | 기본값은 작업 당일이며, 날짜를 명시한다. |
| 투자 기간 | 기본값은 단기 1~3개월, 중기 6~12개월, 장기 3~5년 전체 포함이다. |
| 투자자 유형 | 기본값은 혼합형이다. |
| 보고서 깊이 | 기본값은 표준형이다. |
| 기준 통화 | 거래소/국가의 상장 통화를 우선 사용하되, 가정으로 명시한다. |
| 회계 기준 | 회사 공시 기준을 따른다. 불명확하면 추가 확인 필요로 표시한다. |
| 비교기업 수 | 기본값은 3~5개다. |
| 기술적 분석 포함 여부 | 기본값은 포함이다. |
| 최종 의견 형식 | 기본값은 점수형 + 시나리오별 전략이다. |

## Architecture

이 Harness는 `Pipeline + Fan-out/Fan-in + Producer-Reviewer` 조합으로 운영한다.

| 단계 | 패턴 | 이유 |
|---|---|---|
| 입력 정규화 | Pipeline | 모든 역할이 같은 입력 스냅샷을 사용해야 한다. |
| 전문가 분석 | Fan-out/Fan-in | 재무, 정성, 밸류에이션, 기술, 매크로, 리스크 분석은 병렬화 가능하다. |
| 초안 합성 | Pipeline | 전문가 산출물이 있어야 종합 점수와 최종 의견을 만들 수 있다. |
| QA 및 수정 | Producer-Reviewer | 출처 누락, 수치 충돌, 과도한 확신 표현을 별도 품질 게이트에서 잡는다. |

## Workflow

### 1. 입력 정규화

1. 사용자 원문 요청을 보존한다.
2. 필수 식별자와 누락된 선택값을 정리한다.
3. 기본값, 해석한 가정, 제외 범위를 분리한다.
4. `docs/harness/invest/templates/request-summary.md` 형식으로 `_workspace/00_input/request-summary.md`를 작성한다.

완료 기준:

- 기업명, 티커, 거래소/국가, 분석 기준일이 명시되어 있다.
- 기본값을 적용한 항목이 별도 표에 남아 있다.
- 분석 제외 범위와 기술적 분석 포함 여부가 명시되어 있다.

### 2. 전문가 분석 분배

아래 역할은 같은 입력 스냅샷을 사용한다. 특정 산출물이 다른 역할의 전제에 필요하면 해당 파일을 명시적으로 함께 전달한다.

| 역할 | 담당 범위 | 스킬 | 산출물 |
|---|---|---|---|
| financial-analyst | Part II, III | `.agents/skills/financial-analyst/SKILL.md` | `_workspace/01_financial/findings.md` |
| fundamental-analyst | Part IV, V, VI, VII | `.agents/skills/fundamental-analyst/SKILL.md` | `_workspace/02_fundamental/findings.md` |
| valuation-analyst | Part VIII | `.agents/skills/valuation-analyst/SKILL.md` | `_workspace/03_valuation/findings.md` |
| technical-analyst | Part IX | `.agents/skills/technical-analyst/SKILL.md` | `_workspace/04_technical/findings.md` |
| macro-sentiment-analyst | Part X, XI | `.agents/skills/macro-sentiment-analyst/SKILL.md` | `_workspace/05_macro_sentiment/findings.md` |
| risk-scenario-analyst | Part XII, XIII | `.agents/skills/risk-scenario-analyst/SKILL.md` | `_workspace/06_risk_scenario/findings.md` |

분배 규칙:

- 각 역할에는 자신의 출력 계약과 공통 입력 파일만 전달한다.
- 핵심 수치에는 출처, 기준일, 회계기간, 통화, 산식이 필요하다고 명시한다.
- 데이터가 부족한 경우 추정하지 않고 `공식 자료 미확인`, `데이터 부족`, `추가 확인 필요`를 사용하게 한다.
- 기술적 분석 제외 요청이 있으면 `technical-analyst`는 생략 사유와 보조 신호 부재의 한계만 기록한다.

### 3. 중간 산출물 점검

1. `_workspace/01_financial/findings.md`부터 `_workspace/06_risk_scenario/findings.md`까지 존재 여부를 확인한다.
2. 각 파일의 분석 전제, 출처 목록, 요약, 데이터 한계 섹션을 확인한다.
3. 수치나 판단이 충돌하면 `_workspace/06_risk_scenario/conflicts.md`에 기록한다.
4. 누락이 치명적이면 해당 역할에 보강을 요청한다.

충돌 기록 기준:

| 충돌 유형 | 처리 |
|---|---|
| 수치 충돌 | 출처, 기준일, 회계기간, 산식 차이를 표로 비교한다. |
| 판단 충돌 | 어떤 전제 차이가 결론 차이를 만들었는지 적는다. |
| 데이터 신선도 충돌 | 최신 자료 우선순위를 적용하되, 오래된 자료 사용 한계를 남긴다. |

### 4. 초안 합성

`report-synthesizer`가 아래 입력을 읽고 `_workspace/07_draft/report.md`를 작성한다.

- `_workspace/00_input/request-summary.md`
- `_workspace/01_financial/findings.md`
- `_workspace/02_fundamental/findings.md`
- `_workspace/03_valuation/findings.md`
- `_workspace/04_technical/findings.md`
- `_workspace/05_macro_sentiment/findings.md`
- `_workspace/06_risk_scenario/findings.md`
- 필요 시 `_workspace/06_risk_scenario/conflicts.md`

초안은 `invest_prompt_v2.md`의 최종 출력 템플릿 18개 섹션 순서를 따른다.

### 5. QA

`qa-reviewer`가 `_workspace/07_draft/report.md`와 원천 findings 전체를 검토하고 `_workspace/09_qa/review.md`를 작성한다.

QA 판정:

| 판정 | 의미 | 후속 조치 |
|---|---|---|
| 승인 | 치명적 결함 없음 | 최종본 확정 가능 |
| 수정 후 승인 | 제한적 결함 있음 | 오케스트레이터가 수정 후 최종본 확정 |
| 재검토 필요 | 출처, 구조, 결론 정합성에 치명적 결함 있음 | 관련 역할 보강 후 초안 재작성 |

### 6. 최종본 확정

1. QA 지적을 반영한다.
2. 최종 보고서를 `_workspace/08_final/report.md`에 저장한다.
3. 사용자 전달용 핵심 요약이 필요하면 `_workspace/08_final/executive-summary.md`를 추가로 작성한다.
4. 최종 응답에는 리포트 위치, QA 상태, 남은 한계를 짧게 알린다.

## Handoff Files

| 순서 | 경로 | 소유 역할 | 필수 내용 |
|---|---|---|---|
| 00 | `_workspace/00_input/request-summary.md` | invest-orchestrator | 입력값, 기본 가정, 분석 범위, 제외 범위 |
| 01 | `_workspace/01_financial/findings.md` | financial-analyst | 기업 개요, 재무제표, 비율, 최근 이벤트 |
| 02 | `_workspace/02_fundamental/findings.md` | fundamental-analyst | 산업/경쟁, 경영진, 해자, 제품·서비스 |
| 03 | `_workspace/03_valuation/findings.md` | valuation-analyst | 멀티플 비교, DCF 가정, 시나리오별 가치 |
| 04 | `_workspace/04_technical/findings.md` | technical-analyst | 추세, 지표, 지지·저항, 기술적 리스크 |
| 05 | `_workspace/05_macro_sentiment/findings.md` | macro-sentiment-analyst | 뉴스, 센티먼트, 거시·정책 영향 |
| 06 | `_workspace/06_risk_scenario/findings.md` | risk-scenario-analyst | 리스크 등록부, 시나리오 표, 촉발 요인 |
| 06a | `_workspace/06_risk_scenario/conflicts.md` | invest-orchestrator | 출처 충돌, 수치 충돌, 해석 충돌 |
| 07 | `_workspace/07_draft/report.md` | report-synthesizer | 통합 초안 전체 |
| 08 | `_workspace/08_final/report.md` | invest-orchestrator | QA 반영 완료 최종본 |
| 08a | `_workspace/08_final/executive-summary.md` | invest-orchestrator | 선택적 사용자 요약본 |
| 09 | `_workspace/09_qa/review.md` | qa-reviewer | 결함 목록, 수정 요청, 승인 여부 |

## Failure Policy

- 기업 식별 정보가 부족하면 분석을 중단하고 보완 필요 항목을 적는다.
- 특정 전문가 산출물이 누락되면 1회 보강을 요청한다.
- 보강 후에도 부족하면 최종 리포트의 한계 섹션에 미완료 범위와 영향도를 명시한다.
- 출처 충돌은 임의 평균이나 임의 선택으로 해결하지 않는다.
- QA에서 치명적 결함이 나오면 `_workspace/08_final/report.md`를 확정하지 않는다.

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
