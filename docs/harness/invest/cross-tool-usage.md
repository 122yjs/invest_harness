# Cross-Tool Usage

## 결론

이 Harness는 Codex 전용으로 묶여 있지 않습니다. 핵심 동작은 다음 세 가지에만 의존합니다.

- Markdown 지침 파일
- `_workspace/` 아래의 결정적 산출물 경로
- Windows PowerShell 기반 구조 검증 스크립트

따라서 opencode, OpenClaw, Hermes, Claude, Antigravity, Gemini 계열 IDE 에이전트, 일반 LLM 에이전트에서도 사용할 수 있습니다. 다만 `.agents/skills/*/SKILL.md`의 자동 발견 여부는 도구마다 다르므로, Codex가 아닌 환경에서는 사용할 역할 파일 경로를 프롬프트에 직접 명시하는 것이 가장 안정적입니다.

## 공통 진입 문서

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
| 최종 의견 형식 | 점수형 + 시나리오별 전략 |

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

| 문서 | 역할 |
|---|---|
| `AGENTS.md` | 저장소 전체 규칙과 canonical path |
| `README.md` | 사용자 기준 빠른 시작 |
| `docs/harness/invest/runbook.md` | 실제 실행 순서 |
| `docs/harness/invest/team-spec.md` | 역할 분담과 산출물 계약 |
| `.agents/skills/<role>/SKILL.md` | 역할별 상세 작업 지침 |
| `OPENCLAW.md` | OpenClaw 계열 진입점 |
| `HERMES.md` | Hermes 계열 진입점 |
| `CLAUDE.md` | Claude / Claude Code 계열 진입점 |
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

## OpenClaw에서 사용

OpenClaw에서는 `AGENTS.md`와 `OPENCLAW.md`를 진입점으로 두고, 역할별 스킬 자동 발견이 불명확하면 `SKILL.md` 파일 경로를 프롬프트에 명시한다.

추천 프롬프트:

```text
OPENCLAW.md, AGENTS.md, docs/harness/invest/runbook.md를 읽고 따른다.
.agents/skills/invest-orchestrator/SKILL.md를 최상위 지침으로 사용한다.
Apple(AAPL, NASDAQ)에 대한 표준형 투자 리포트를 생성하고 _workspace 산출물 계약을 지킨다.
```

## Hermes에서 사용

Hermes에서는 `AGENTS.md`와 `HERMES.md`를 진입점으로 두고, 역할별 스킬 자동 발견이 불명확하면 `SKILL.md` 파일 경로를 프롬프트에 명시한다.

추천 프롬프트:

```text
HERMES.md, AGENTS.md, docs/harness/invest/runbook.md를 읽고 따른다.
.agents/skills/invest-orchestrator/SKILL.md를 최상위 지침으로 사용한다.
Apple(AAPL, NASDAQ)에 대한 표준형 투자 리포트를 생성하고 _workspace 산출물 계약을 지킨다.
```

## Claude / Claude Code에서 사용

Claude 또는 Claude Code 계열 도구에서는 `AGENTS.md`와 `CLAUDE.md`를 진입점으로 둔다. 역할별 스킬 자동 발견은 환경 설정에 따라 달라질 수 있으므로, 필요한 역할 파일을 프롬프트에 명시한다.

추천 프롬프트:

```text
CLAUDE.md, AGENTS.md, docs/harness/invest/runbook.md를 읽고 따른다.
.agents/skills/invest-orchestrator/SKILL.md를 최상위 지침으로 사용한다.
Apple(AAPL, NASDAQ)에 대한 표준형 투자 리포트를 생성하고 _workspace 산출물 계약을 지킨다.
```

부분 분석만 필요할 때:

```text
CLAUDE.md와 AGENTS.md를 따른다.
.agents/skills/financial-analyst/SKILL.md를 사용해서 AAPL의 기업 개요와 재무 분석 findings를 작성한다.
출력은 _workspace/01_financial/findings.md에 저장한다.
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
