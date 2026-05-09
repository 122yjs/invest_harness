# 투자 리서치 Harness Team Spec

## 1. 목적
이 Harness는 `invest_prompt_v2.md`를 기준으로 개별 주식 투자 리포트를 병렬 분석 후 순차 종합하는 팀 구조를 정의한다. 목표는 **출처 명시, 파트별 전문성, 재현 가능한 핸드오프, 최종 QA**를 확보하는 것이다. 최종 보고서는 16개 분석 파트를 바탕으로 `invest_prompt_v2.md`의 18개 최종 출력 섹션에 맞춰 작성한다.

## 2. 아키텍처

| 패턴 | 적용 방식 | 목적 |
|---|---|---|
| Fan-out / Fan-in | 입력 요약 후 분석 역할에 병렬 분배, 결과를 한곳으로 회수 | 속도와 범위 확보 |
| Pipeline | 입력 정리 → 병렬 분석 → 초안 조립 → QA → 최종본 확정 | 단계별 책임 분리 |
| Producer-Reviewer | 작성 역할이 산출물을 만들고 `qa-reviewer`가 검수 | 누락·오류·문체 불일치 방지 |

## 3. 순차 흐름

| 단계 | 담당 | 주요 작업 | 산출물 |
|---|---|---|---|
| 1 | invest-orchestrator | 사용자 입력 정리, 가정 명시, 작업 범위 확정 | `_workspace/00_input/request-summary.md` |
| 2 | 분석 역할 6종 | 파트별 병렬 조사 및 근거 표준화 | `01`~`06` findings, 필요 시 `06a` conflicts |
| 3 | report-synthesizer | 병렬 결과를 리포트 구조에 맞춰 초안 조립 | `_workspace/07_draft/report.md` |
| 4 | qa-reviewer | 출처, 수치, 일관성, 누락, 문체 검토 | `_workspace/09_qa/review.md` |
| 5 | invest-orchestrator | QA 반영 후 최종본 확정 | `_workspace/08_final/report.md` |

## 4. 역할 정의 및 입출력 계약

| 역할 | 담당 파트 | 입력 | 출력 | 완료 기준 |
|---|---|---|---|---|
| invest-orchestrator | 전체 조율 | 사용자 요청, `invest_prompt_v2.md` | 요청 요약, 작업 지시, 최종 리포트 | 필수 입력·가정·분석 기준일·투자 기간이 정리되고 최종본이 QA 반영 상태임 |
| financial-analyst | Part II, III | 요청 요약, 기업 식별 정보 | `_workspace/01_financial/findings.md` | 기업 개요, 사업 구조, 최근 이벤트, 재무제표·비율·종합평가가 출처와 기준일과 함께 정리됨 |
| fundamental-analyst | Part IV, V, VI, VII | 요청 요약, 기업 식별 정보 | `_workspace/02_fundamental/findings.md` | 산업/경쟁, 경영진/거버넌스, 해자, 제품·서비스가 표와 서술로 정리됨 |
| valuation-analyst | Part VIII | 요청 요약, 재무 결과, 비교기업 가정 | `_workspace/03_valuation/findings.md` | 상대가치와 DCF 또는 대체 평가, Bear/Base/Bull 가치 범위가 명시됨 |
| technical-analyst | Part IX | 요청 요약, 가격 데이터 사용 범위 | `_workspace/04_technical/findings.md` | 추세, 지지·저항, 이평선, RSI/MACD 등 기술 신호와 한계가 정리됨 |
| macro-sentiment-analyst | Part X, XI | 요청 요약, 국가/통화/기간 정보 | `_workspace/05_macro_sentiment/findings.md` | 뉴스, 센티먼트, 애널리스트 의견, 거시·정책 영향 경로가 정리됨 |
| risk-scenario-analyst | Part XII, XIII | 요청 요약, 선행 분석 결과 | `_workspace/06_risk_scenario/findings.md` | 리스크 표와 Bear/Base/Bull 시나리오가 모니터링 지표와 함께 정리됨 |
| report-synthesizer | Part I, XIV, XV, XVI | `01`~`06` findings 전체 | `_workspace/07_draft/report.md` | Executive Summary, 종합 점수, 최종 의견, 체크리스트, 한계가 전체 파트와 일관됨 |
| qa-reviewer | 최종 QA | 초안 리포트, 원천 findings 전체 | `_workspace/09_qa/review.md` | 출처 누락, 수치 충돌, 논리 비약, 문체 문제, 미완성 표가 체크리스트 형태로 보고됨 |

## 5. 공통 작성 규칙

| 항목 | 규칙 |
|---|---|
| 출처 | 모든 핵심 수치와 사실에 출처, 기준일, 회계기간, 통화 명시 |
| 불확실성 | 데이터 부족 시 추정하지 말고 `공식 자료 미확인`, `데이터 부족`, `추가 확인 필요`로 표기 |
| 비교 가능성 | IFRS/US GAAP 차이, 환율 기준일, TTM/연간/분기 구분 명시 |
| 문체 | 한국어, 간결한 투자 리포트 문체, 과도한 확신 표현 금지 |
| 구조 | 표 우선, 각 섹션 말미 3~5줄 요약, Executive Summary와 최종 결론 일치 |

## 6. 핸드오프 파일 규칙

| 순서 | 경로 | 소유 역할 | 필수 내용 |
|---|---|---|---|
| 00 | `_workspace/00_input/request-summary.md` | invest-orchestrator | 입력값, 기본 가정, 분석 범위, 제외 범위 |
| 01 | `_workspace/01_financial/findings.md` | financial-analyst | 기업 개요, 재무표, 비율, 최근 이벤트 |
| 02 | `_workspace/02_fundamental/findings.md` | fundamental-analyst | 산업/경쟁, 경영진, 해자, 제품·서비스 |
| 03 | `_workspace/03_valuation/findings.md` | valuation-analyst | 멀티플 비교, DCF 가정, 시나리오별 가치 |
| 04 | `_workspace/04_technical/findings.md` | technical-analyst | 추세, 지표, 지지·저항, 기술적 리스크 |
| 05 | `_workspace/05_macro_sentiment/findings.md` | macro-sentiment-analyst | 뉴스, 센티먼트, 거시·정책 영향 |
| 06 | `_workspace/06_risk_scenario/findings.md` | risk-scenario-analyst | 리스크 등록부, 시나리오 표, 촉발 요인 |
| 06a | `_workspace/06_risk_scenario/conflicts.md` | invest-orchestrator / risk-scenario-analyst | 출처 충돌, 수치 충돌, 해석 충돌, 재확인 요청 |
| 07 | `_workspace/07_draft/report.md` | report-synthesizer | 통합 초안 전체 |
| 08 | `_workspace/08_final/report.md` | invest-orchestrator | QA 반영 완료 최종본 |
| 08a | `_workspace/08_final/executive-summary.md` | invest-orchestrator | 선택적 사용자 요약본 |
| 09 | `_workspace/09_qa/review.md` | qa-reviewer | 결함 목록, 수정 요청, 승인 여부 |

### 핸드오프 규약
- 각 `findings.md` 첫머리에 **범위, 사용 데이터 기준일, 핵심 가정, 출처 목록**을 둔다.
- 수치 표에는 **단위와 통화**를 반드시 적는다.
- 상위 역할은 하위 역할 산출물을 덮어쓰지 않고, 수정이 필요하면 QA 또는 orchestrator 메모로 지시한다.
- `report-synthesizer`는 원본 findings를 재해석하되, 출처 없는 신규 수치를 추가하지 않는다.

## 7. 반복 실행 템플릿

| 템플릿 | 용도 |
|---|---|
| `docs/harness/invest/templates/request-summary.md` | `_workspace/00_input/request-summary.md` 작성 기준 |
| `docs/harness/invest/templates/findings-common.md` | 전문가 findings 공통 머리말과 한계 섹션 기준 |
| `docs/harness/invest/templates/conflicts.md` | `_workspace/06_risk_scenario/conflicts.md` 작성 기준 |
| `docs/harness/invest/templates/report.md` | `_workspace/07_draft/report.md` 및 `_workspace/08_final/report.md` 작성 기준 |
| `docs/harness/invest/templates/qa-review.md` | `_workspace/09_qa/review.md` 작성 기준 |

## 8. 실패 및 재시도 정책

| 실패 유형 | 처리 원칙 | 재시도 방식 |
|---|---|---|
| 공식 출처 부재 | 비공식 수치로 대체 결론을 확정하지 않음 | 2순위·3순위 출처로 보완 후 불확실성 표기 |
| 수치 충돌 | 하나를 임의 채택하지 않음 | 차이 표 작성, 기준일·회계 기준·산식 차이 설명 |
| 파트 누락 | 초안 단계에서 종료하지 않음 | 누락 역할이 findings 보강 후 synthesize 재실행 |
| 논리 불일치 | 상충 결론을 그대로 병합하지 않음 | orchestrator가 쟁점 정리, 관련 역할 재검토 요청 |
| QA 실패 | 최종본 확정 금지 | 수정 후 `qa-reviewer` 재검토 |
| 데이터 신선도 부족 | 오래된 데이터로 현재 결론을 단정하지 않음 | 최신 분기/최근 뉴스 기준으로 업데이트, 불가 시 기준일 경고 |

## 9. 최종 승인 기준
- `_workspace/00`~`09`의 필수 파일이 모두 존재한다.
- 초안과 최종본의 섹션 순서가 `invest_prompt_v2.md` 요구 구조와 일치한다.
- 핵심 수치에는 출처와 기준일이 붙어 있다.
- 최종 의견은 점수, 시나리오, 리스크, 모니터링 체크리스트와 상호 일관된다.
- `qa-reviewer`가 치명적 누락 없음으로 마감했을 때만 `_workspace/08_final/report.md`를 확정한다.
- Windows PowerShell에서 `.\scripts\Test-HarnessStructure.ps1` 검증이 통과한다.
