# Cross-Tool Usage

## 결론

이 Harness는 Codex 전용으로 묶여 있지 않습니다. 핵심 동작은 다음 세 가지에만 의존합니다.

- Markdown 지침 파일
- `_workspace/` 아래의 결정적 산출물 경로
- Windows PowerShell 기반 구조 검증 스크립트

따라서 opencode, Antigravity, Gemini 계열 IDE 에이전트, 일반 LLM 에이전트에서도 사용할 수 있습니다. 다만 `.agents/skills/*/SKILL.md`의 자동 발견 여부는 도구마다 다르므로, Codex가 아닌 환경에서는 사용할 역할 파일 경로를 프롬프트에 직접 명시하는 것이 가장 안정적입니다.

## 공통 진입 문서

| 문서 | 역할 |
|---|---|
| `AGENTS.md` | 저장소 전체 규칙과 canonical path |
| `README.md` | 사용자 기준 빠른 시작 |
| `docs/harness/invest/runbook.md` | 실제 실행 순서 |
| `docs/harness/invest/team-spec.md` | 역할 분담과 산출물 계약 |
| `.agents/skills/<role>/SKILL.md` | 역할별 상세 작업 지침 |
| `GEMINI.md` | Gemini/Antigravity 계열 진입점 |

## Codex에서 사용

Codex는 이 저장소의 `AGENTS.md`와 `.agents/skills/*/SKILL.md` 구조를 그대로 사용할 수 있다.

추천 프롬프트:

```text
invest-orchestrator를 사용해서 Apple(AAPL, NASDAQ)을 기준일 2026-05-10, 표준형, 혼합형 투자자 관점으로 분석해줘.
```

## opencode에서 사용

opencode는 프로젝트 지침으로 `AGENTS.md`를 사용할 수 있다. 역할별 스킬 자동 발견은 환경 설정에 따라 달라질 수 있으므로, 필요한 역할 파일을 프롬프트에 명시한다.

추천 프롬프트:

```text
AGENTS.md와 docs/harness/invest/runbook.md를 따른다.
.agents/skills/invest-orchestrator/SKILL.md를 오케스트레이터 지침으로 사용한다.
Apple(AAPL, NASDAQ)에 대한 표준형 투자 리포트를 생성해줘.
모든 산출물은 team-spec.md의 _workspace 경로에 저장한다.
```

부분 분석만 필요할 때:

```text
AGENTS.md를 따른다.
.agents/skills/valuation-analyst/SKILL.md만 사용해서 AAPL 밸류에이션 findings를 작성한다.
출력은 _workspace/03_valuation/findings.md에 저장한다.
```

## Antigravity / Gemini 계열에서 사용

Antigravity 또는 Gemini 계열 도구에서는 `AGENTS.md`와 `GEMINI.md`를 진입점으로 둔다. 에이전트가 `.agents/skills`를 자동으로 읽지 않는 경우가 있으므로 역할 파일 경로를 직접 언급한다.

추천 프롬프트:

```text
GEMINI.md, AGENTS.md, docs/harness/invest/runbook.md를 읽고 따른다.
.agents/skills/invest-orchestrator/SKILL.md를 최상위 지침으로 사용한다.
Apple(AAPL, NASDAQ)에 대한 표준형 투자 리포트를 생성하고 _workspace 산출물 계약을 지킨다.
```

## 일반 LLM/IDE 에이전트에서 사용

일반 에이전트는 다음 문서를 순서대로 읽게 하면 된다.

1. `README.md`
2. `AGENTS.md`
3. `docs/harness/invest/runbook.md`
4. `docs/harness/invest/team-spec.md`
5. 필요한 역할의 `.agents/skills/<role>/SKILL.md`

추천 프롬프트:

```text
이 저장소는 파일 기반 투자 리서치 Harness다.
README.md, AGENTS.md, docs/harness/invest/runbook.md, docs/harness/invest/team-spec.md를 먼저 읽어라.
전체 리포트 생성이면 .agents/skills/invest-orchestrator/SKILL.md를 따른다.
부분 분석이면 해당 역할의 SKILL.md만 사용한다.
```

## 검증

어떤 도구를 쓰든 최종 구조 검증은 동일하다.

```powershell
.\scripts\Test-HarnessStructure.ps1
```

검증 대상은 도구가 아니라 저장소 구조다. 필수 스킬, frontmatter, 핸드오프 경로가 맞으면 통과한다.

## 주의사항

- `.agents/skills`는 이 저장소의 역할 지침 저장 위치다. 모든 도구가 이를 자동 스킬로 인식한다고 가정하지 않는다.
- 자동 discovery가 불명확하면 역할 파일 경로를 프롬프트에 직접 적는다.
- 최신 투자 데이터가 필요한 실제 리포트 생성에서는 에이전트가 현재 기준 공시와 웹 출처를 확인해야 한다.
- 산출물은 `_workspace/`에 남겨 감사 가능성을 유지한다.
