# Hermes Entry Point

이 저장소의 기준 지침은 `AGENTS.md`입니다.

<!-- BEGIN INPUT_GATE_POLICY_INTEGRATED -->
전체 리포트 생성 시에는 먼저 입력 수집 게이트를 수행합니다. 사용자가 기업명 또는 티커 중 하나를 제공하면 나머지 식별자는 자동 확인합니다. 사용자에게는 진행 방식 `> 일괄 / 순차`, 분석 초점 `> 장기 / 분기 / 혼합`, 투자 기간 `> 단기 / 중기 / 장기 / 전체`, 비교기업 수 `> 3 / 5 / 10 / 직접`, 보고서 깊이 `> 요약 / 표준 / 심층`만 되묻습니다.
<!-- END INPUT_GATE_POLICY_INTEGRATED -->

Hermes 계열 에이전트는 아래 문서를 함께 읽고 작업합니다.

1. `AGENTS.md`
2. `README.md`
3. `docs/harness/invest/runbook.md`
4. `docs/harness/invest/team-spec.md`
5. 필요한 역할의 `.agents/skills/<role>/SKILL.md`

역할별 `SKILL.md` 파일은 특정 런타임 전용 코드가 아니라 Markdown 작업 지침입니다. Hermes 환경에서 skill discovery가 자동으로 동작하지 않으면 사용할 역할 파일 경로를 프롬프트에 직접 명시합니다.

예시:

```text
AGENTS.md와 docs/harness/invest/runbook.md를 따른다.
.agents/skills/invest-orchestrator/SKILL.md를 오케스트레이터 지침으로 사용한다.
Apple(AAPL, NASDAQ)에 대한 표준형 투자 리포트를 생성해줘.
모든 산출물은 docs/harness/invest/team-spec.md의 _workspace 계약을 따른다.
```
