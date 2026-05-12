# 투자 리서치 Harness Team Spec

## 1. 목적
이 Harness는 `invest_prompt_v2.md`를 기준으로 개별 주식 투자 리포트를 병렬 분석 후 순차 종합하는 팀 구조를 정의한다. 목표는 **출처 명시, 파트별 전문성, 재현 가능한 핸드오프, 최종 QA**를 확보하는 것이다. 최종 보고서는 16개 분석 파트를 바탕으로 `invest_prompt_v2.md`의 18개 최종 출력 섹션에 맞춰 작성한다.

## 2. 아키텍처

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

| 패턴 | 적용 방식 | 목적 |
|---|---|---|
| Fan-out / Fan-in | 입력 요약 후 분석 역할에 병렬 분배, 결과를 한곳으로 회수 | 속도와 범위 확보 |
| Pipeline | 입력 정리 → 병렬 분석 → 초안 조립 → QA → 최종본 확정 | 단계별 책임 분리 |
| Producer-Reviewer | 작성 역할이 산출물을 만들고 `qa-reviewer`가 검수 | 누락·오류·문체 불일치 방지 |

## 3. 순차 흐름

| 단계 | 담당 | 주요 작업 | 산출물 |
|---|---|---|---|
| 0 | invest-orchestrator | 입력 수집 게이트, 기업명/티커 기반 자동 식별, 선택 옵션 확인 | `${ACTIVE_WORKSPACE}/00_input/input-intake.md` |
| 1 | invest-orchestrator | 사용자 입력 정규화, 가정 명시, 작업 범위 확정, 기준 주가 snapshot 작성 | `${ACTIVE_WORKSPACE}/00_input/request-summary.md`, `${ACTIVE_WORKSPACE}/00_input/market-price-snapshot.md` |
| 2 | 분석 역할 6종 | 파트별 병렬 조사 및 근거 표준화 | `01`~`06` findings, 필요 시 `06a` conflicts |
| 3 | report-synthesizer | 병렬 결과를 리포트 구조에 맞춰 초안 조립 | `${ACTIVE_WORKSPACE}/07_draft/report.md` |
| 4 | qa-reviewer | 출처, 수치, 일관성, 누락, 문체 검토 | `${ACTIVE_WORKSPACE}/09_qa/review.md` |
| 5 | invest-orchestrator | QA 반영 후 최종본 확정 | `${ACTIVE_WORKSPACE}/08_final/report.md`

## 4. 역할 정의 및 입출력 계약

| 역할 | 담당 파트 | 입력 | 출력 | 완료 기준 |
|---|---|---|---|---|
| invest-orchestrator | 전체 조율 | 사용자 요청, `invest_prompt_v2.md` | 요청 요약, 작업 지시, 최종 리포트 | 필수 입력·가정·분석 기준일·투자 기간이 정리되고 최종본이 QA 반영 상태임 |
| financial-analyst | Part II, III | 요청 요약, 기업 식별 정보 | `${ACTIVE_WORKSPACE}/01_financial/findings.md` | 기업 개요, 사업 구조, 최근 이벤트, 재무제표·비율·종합평가가 출처와 기준일과 함께 정리됨 |
| fundamental-analyst | Part IV, V, VI, VII | 요청 요약, 기업 식별 정보 | `${ACTIVE_WORKSPACE}/02_fundamental/findings.md` | 산업/경쟁, 경영진/거버넌스, 해자, 제품·서비스가 표와 서술로 정리됨 |
| valuation-analyst | Part VIII | 요청 요약, market-price snapshot, 재무 결과, 비교기업 가정 | `${ACTIVE_WORKSPACE}/03_valuation/findings.md`, `${ACTIVE_WORKSPACE}/03_valuation/comps.md`, `${ACTIVE_WORKSPACE}/03_valuation/dcf.md` | 상대가치와 DCF 또는 대체 평가, Bear/Base/Bull 가치 범위, Rating/Price Target 입력값이 명시됨 |
| technical-analyst | Part IX | 요청 요약, 가격 데이터 사용 범위 | `${ACTIVE_WORKSPACE}/04_technical/findings.md` | 추세, 지지·저항, 이평선, RSI/MACD 등 기술 신호와 한계가 정리됨 |
| macro-sentiment-analyst | Part X, XI | 요청 요약, 국가/통화/기간 정보 | `${ACTIVE_WORKSPACE}/05_macro_sentiment/findings.md` | 뉴스, 센티먼트, 애널리스트 의견, 거시·정책 영향 경로가 정리됨 |
| risk-scenario-analyst | Part XII, XIII | 요청 요약, 선행 분석 결과 | `${ACTIVE_WORKSPACE}/06_risk_scenario/findings.md` | 리스크 표와 Bear/Base/Bull 시나리오가 모니터링 지표와 함께 정리됨 |
| report-synthesizer | Part I, XIV, XV, XVI | `00`~`06` 산출물 전체 | `${ACTIVE_WORKSPACE}/07_draft/report.md` | Executive Summary, Rating, Price Target, Risk-Reward, 체크리스트, 한계가 전체 파트와 일관됨 |
| qa-reviewer | 최종 QA | 초안 리포트, 원천 findings, market-price snapshot | `${ACTIVE_WORKSPACE}/09_qa/review.md`, `${ACTIVE_WORKSPACE}/09_qa/fix-list.md`, `${ACTIVE_WORKSPACE}/09_qa/final-check.md` | 출처 누락, 수치 충돌, Rating/Price Target 근거, 재계산 항목, 문체 문제가 체크리스트 형태로 보고됨 |

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
| 01 | `${ACTIVE_WORKSPACE}/01_financial/findings.md` | financial-analyst | 기업 개요, 재무표, 비율, 최근 이벤트 |
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
| 06a | `${ACTIVE_WORKSPACE}/06_risk_scenario/conflicts.md` | invest-orchestrator / risk-scenario-analyst | 출처 충돌, 수치 충돌, 해석 충돌, 재확인 요청 |
| 07 | `${ACTIVE_WORKSPACE}/07_draft/report.md` | report-synthesizer | 통합 초안 전체 |
| 08 | `${ACTIVE_WORKSPACE}/08_final/report.md` | invest-orchestrator | QA 반영 완료 최종본 |
| 08h | `${ACTIVE_WORKSPACE}/08_final/report.html` | html-report-synthesizer | Markdown 최종 리포트의 정적 HTML 출력 |
| 08a | `${ACTIVE_WORKSPACE}/08_final/executive-summary.md` | invest-orchestrator | 선택적 사용자 요약본 |
| 09 | `${ACTIVE_WORKSPACE}/09_qa/review.md` | qa-reviewer | 결함 목록, 수정 요청, 승인 여부 |
| 09a | `${ACTIVE_WORKSPACE}/09_qa/fix-list.md` | qa-reviewer | 수정 작업 목록, 담당 산출물, 완료 여부 |
| 09b | `${ACTIVE_WORKSPACE}/09_qa/final-check.md` | qa-reviewer | 최종 승인 전 확인표 |

### 핸드오프 규약
- 각 `findings.md` 첫머리에 **범위, 사용 데이터 기준일, 핵심 가정, 출처 목록**을 둔다.
- 수치 표에는 **단위와 통화**를 반드시 적는다.
- 상위 역할은 하위 역할 산출물을 덮어쓰지 않고, 수정이 필요하면 QA 또는 orchestrator 메모로 지시한다.
- `report-synthesizer`는 원본 findings를 재해석하되, 출처 없는 신규 수치를 추가하지 않는다.

### 반복 실행 workspace 규약
- `${ACTIVE_WORKSPACE}/`는 현재 실행의 active workspace다.
- 새 리서치 시작 전 `${ACTIVE_WORKSPACE}/`에 기존 산출물이 있으면 삭제하거나 덮어쓰지 않고 `_workspace_runs/<YYYY-MM-DD>-<ticker-or-slug>/`로 먼저 archive한다.
- archive 경로가 이미 있으면 `-HHMMSS` 또는 `-2`처럼 충돌 없는 suffix를 붙인다.
- archive는 move를 기본으로 한다. move가 불가능한 런타임에서만 copy를 사용하고, copy 검증 전에는 기존 파일을 비우지 않는다.
- 하위 역할과 합성/QA 단계는 같은 `ACTIVE_WORKSPACE` 절대 경로를 공유한다. 논리적 산출물 이름은 `${ACTIVE_WORKSPACE}/...`로 유지하되, 절대 경로가 필요할 때는 `${ACTIVE_WORKSPACE}/01_financial/findings.md`처럼 작성한다.

## 7. 반복 실행 템플릿

| 템플릿 | 용도 |
|---|---|
| `docs/harness/invest/templates/request-summary.md` | `${ACTIVE_WORKSPACE}/00_input/request-summary.md` 작성 기준 |
| `docs/harness/invest/templates/findings-common.md` | 전문가 findings 공통 머리말과 한계 섹션 기준 |
| `docs/harness/invest/templates/conflicts.md` | `${ACTIVE_WORKSPACE}/06_risk_scenario/conflicts.md` 작성 기준 |
| `docs/harness/invest/templates/report.md` | `${ACTIVE_WORKSPACE}/07_draft/report.md` 및 `${ACTIVE_WORKSPACE}/08_final/report.md` 작성 기준 |
| `docs/harness/invest/templates/qa-review.md` | `${ACTIVE_WORKSPACE}/09_qa/review.md` 작성 기준 |
| `docs/harness/invest/templates/earnings-preview.md` | `${ACTIVE_WORKSPACE}/00_input/earnings-preview.md` 작성 기준 |
| `docs/harness/invest/templates/sector.md` | `${ACTIVE_WORKSPACE}/02_fundamental/sector.md` 작성 기준 |
| `docs/harness/invest/templates/thesis-update.md` | `${ACTIVE_WORKSPACE}/05_macro_sentiment/thesis-update.md` 작성 기준 |
| `docs/harness/invest/templates/catalysts.md` | `${ACTIVE_WORKSPACE}/05_macro_sentiment/catalysts.md` 작성 기준 |
| `docs/harness/invest/templates/html-report.md` | `${ACTIVE_WORKSPACE}/08_final/report.html` 작성 기준 |
| `docs/harness/invest/templates/morning-note.md` | `${ACTIVE_WORKSPACE}/05_macro_sentiment/morning-note.md` 작성 기준 |
| `docs/harness/invest/templates/update-plan.md` | `${ACTIVE_WORKSPACE}/00_input/update-plan.md` 작성 기준 |

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
- `${ACTIVE_WORKSPACE}/00`~`09`의 필수 파일이 모두 존재한다.
- 초안과 최종본의 섹션 순서가 `invest_prompt_v2.md` 요구 구조와 일치한다.
- 핵심 수치에는 출처와 기준일이 붙어 있다.
- 최종 의견은 점수, 시나리오, 리스크, 모니터링 체크리스트와 상호 일관된다.
- Rating, Price Target, Implied Upside / Downside는 `${ACTIVE_WORKSPACE}/00_input/market-price-snapshot.md` 기준 주가와 재계산 가능하다.
- `qa-reviewer`가 치명적 누락 없음으로 마감했을 때만 `${ACTIVE_WORKSPACE}/08_final/report.md`를 확정한다.
- Windows PowerShell에서 `.\scripts\Test-HarnessStructure.ps1` 검증이 통과한다.
