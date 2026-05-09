# AGENTS.md

## WHAT
- 이 저장소는 개별 주식 투자 리포트 Harness를 정의한다.
- 목표는 `invest_prompt_v2.md`의 16개 분석 파트와 18개 최종 리포트 섹션을 일관된 멀티에이전트 워크플로우로 분해·조립하는 것이다.

## WHY
- 방대한 투자 리서치를 병렬화해 속도와 깊이를 함께 확보한다.
- 모든 판단은 출처, 기준일, 회계기간, 통화, 가정을 분리해 재현 가능해야 한다.
- 최종 결과는 정보 제공용 분석이며 개인화된 투자 자문이 아니다.

## HOW
- 리서치는 Fan-out/Fan-in과 Pipeline을 결합해 진행한다.
- 파트별 분석 결과는 `_workspace/`에 표준 파일명으로 저장하고, 최종 리포트는 조립 후 QA를 거친다.
- 확인되지 않은 수치, 출처 없는 주장, 과도한 확신 표현은 금지한다.
- 최신 연간/분기/TTM 데이터를 구분하고, 충돌 수치는 차이와 원인을 함께 적는다.
- 기술적 분석과 소셜 센티먼트는 보조 신호로만 사용한다.

## CANONICAL PATHS
- 핵심 프롬프트: `invest_prompt_v2.md`
- 팀 명세: `docs/harness/invest/team-spec.md`
- 작업 산출물: `_workspace/`
- 역할 확장 경로: `docs/harness/invest/roles/`
- 실행 가이드: `docs/harness/invest/runbook.md`
