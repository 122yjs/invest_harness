# Gemini / Antigravity Entry Point

이 저장소의 기준 지침은 `AGENTS.md`입니다.

Gemini 또는 Antigravity 계열 에이전트는 아래 문서를 함께 읽고 작업합니다.

1. `AGENTS.md`
2. `README.md`
3. `docs/harness/invest/runbook.md`
4. `docs/harness/invest/team-spec.md`
5. 필요한 역할의 `.agents/skills/<role>/SKILL.md`

역할별 `SKILL.md` 파일은 특정 런타임 전용 코드가 아니라 Markdown 작업 지침입니다. 자동 skill discovery가 동작하지 않는 도구에서는 사용할 역할 파일 경로를 프롬프트에 직접 명시합니다.

예시:

```text
AGENTS.md와 docs/harness/invest/runbook.md를 따른다.
.agents/skills/invest-orchestrator/SKILL.md를 오케스트레이터 지침으로 사용한다.
Apple(AAPL, NASDAQ)에 대한 표준형 투자 리포트를 생성해줘.
```
