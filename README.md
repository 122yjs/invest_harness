# Invest Harness

개별 상장기업 투자 리서치 리포트를 반복적으로 생성하기 위한 AI agent Harness입니다. `invest_prompt_v2.md`의 분석 요구사항을 여러 전문가 역할로 나누고, `_workspace/` 파일 핸드오프를 통해 초안, QA, 최종본까지 재현 가능하게 조립합니다.

이 레포의 결과물은 정보 제공용 분석입니다. 개인화된 투자 자문이나 매매 권유로 사용하지 않습니다.

## 빠른 시작

Windows PowerShell에서 레포 구조를 먼저 검증합니다.

```powershell
cd E:\invest_harness
.\scripts\Test-HarnessStructure.ps1
```

검증이 통과하면 사용하는 에이전트에 아래처럼 요청합니다.

```text
AGENTS.md와 docs/harness/invest/runbook.md를 따른다.
.agents/skills/invest-orchestrator/SKILL.md를 오케스트레이터 지침으로 사용해서 Apple(AAPL, NASDAQ)을 기준일 2026-05-10, 표준형, 혼합형 투자자 관점으로 분석해줘.
```

## 주요 파일

| 경로 | 용도 |
|---|---|
| `invest_prompt_v2.md` | 투자 리포트의 원본 요구사항과 최종 출력 구조 |
| `AGENTS.md` | 저장소 전체 작업 규칙과 canonical path |
| `.agents/skills/invest-orchestrator/SKILL.md` | 전체 리서치 흐름을 조율하는 최상위 스킬 |
| `.agents/skills/*/SKILL.md` | 재무, 정성, 밸류에이션, 기술적 분석, 매크로, 리스크, 합성, QA 역할 |
| `docs/harness/invest/team-spec.md` | 역할 분담, 산출물 계약, 실패 정책 |
| `docs/harness/invest/runbook.md` | 실제 실행 순서 |
| `docs/harness/invest/templates/` | 반복 실행용 산출물 템플릿 |
| `scripts/Test-HarnessStructure.ps1` | Harness 구조 검증 스크립트 |
| `docs/harness/invest/cross-tool-usage.md` | Codex, opencode, Antigravity 등 도구별 사용 방식 |
| `OPENCLAW.md` | OpenClaw 계열 에이전트를 위한 얇은 진입점 |
| `HERMES.md` | Hermes 계열 에이전트를 위한 얇은 진입점 |
| `GEMINI.md` | Gemini/Antigravity 계열 에이전트를 위한 얇은 진입점 |
| `CLAUDE.md` | Claude / Claude Code 계열 에이전트를 위한 얇은 진입점 |

## 리포트 생성 흐름

1. 입력을 정리합니다.
   - 산출물: `_workspace/00_input/request-summary.md`
   - 담당: `invest-orchestrator`

2. 전문가 분석을 작성합니다.
   - 재무: `_workspace/01_financial/findings.md`
   - 산업/경쟁/해자/제품: `_workspace/02_fundamental/findings.md`
   - 밸류에이션: `_workspace/03_valuation/findings.md`
   - 기술적 분석: `_workspace/04_technical/findings.md`
   - 뉴스/센티먼트/거시: `_workspace/05_macro_sentiment/findings.md`
   - 리스크/시나리오: `_workspace/06_risk_scenario/findings.md`

3. 충돌을 기록합니다.
   - 산출물: `_workspace/06_risk_scenario/conflicts.md`
   - 수치, 출처, 기준일, 회계기간이 충돌할 때만 작성합니다.

4. 초안을 합성합니다.
   - 산출물: `_workspace/07_draft/report.md`
   - 담당: `report-synthesizer`

5. QA를 수행합니다.
   - 산출물: `_workspace/09_qa/review.md`
   - 담당: `qa-reviewer`

6. 최종본을 확정합니다.
   - 산출물: `_workspace/08_final/report.md`
   - 선택 요약본: `_workspace/08_final/executive-summary.md`

## 역할별 스킬

| 스킬 | 담당 범위 |
|---|---|
| `invest-orchestrator` | 입력 정규화, 역할 분배, QA 반영, 최종본 확정 |
| `financial-analyst` | 기업 개요, 재무제표, 재무비율 |
| `fundamental-analyst` | 산업, 경쟁, 경영진, 거버넌스, 해자, 제품/서비스 |
| `valuation-analyst` | 상대가치, DCF 또는 간이 DCF, 시나리오별 가치 |
| `technical-analyst` | 가격 추세, 이동평균, RSI, MACD, 지지/저항 |
| `macro-sentiment-analyst` | 뉴스, 시장 센티먼트, 애널리스트 의견, 거시/정책 환경 |
| `risk-scenario-analyst` | 리스크 등록부, Bear/Base/Bull 시나리오 |
| `report-synthesizer` | 전문가 findings를 18개 최종 섹션으로 조립 |
| `qa-reviewer` | 출처, 수치, 구조, 논리, 문체, 투자 자문 경계 검토 |

## 품질 기준

- 모든 핵심 수치에는 출처, 기준일, 회계기간, 통화, 산식을 남깁니다.
- 최신 연간, 최근 분기, TTM 데이터를 구분합니다.
- 출처가 충돌하면 임의로 평균 내거나 하나를 고르지 않고 차이와 원인을 기록합니다.
- 데이터가 부족하면 `공식 자료 미확인`, `데이터 부족`, `추가 확인 필요`로 표시합니다.
- 기술적 분석과 소셜 센티먼트는 보조 신호로만 사용합니다.
- 최종 보고서는 개인화된 투자 자문이 아니라 정보 제공용 분석임을 명시합니다.

## 브랜치 운영

기본 브랜치는 `main`입니다. 새 Harness 개선이나 리포트 생성 자동화 작업은 별도 브랜치에서 진행한 뒤 검증 후 병합합니다.

권장 흐름:

```powershell
git switch main
git pull --ff-only
git switch -c feat/<작업-이름>
```

작업 후에는 구조 검증을 실행합니다.

```powershell
.\scripts\Test-HarnessStructure.ps1
```

## 도구 호환성

이 Harness는 특정 에이전트 런타임에 의존하지 않도록 설계되어 있습니다. 핵심 계약은 모두 Markdown 파일과 `_workspace/` 산출물 경로로 표현됩니다.

| 도구 | 사용 가능 여부 | 사용 방식 |
|---|---|---|
| Codex | 가능 | `AGENTS.md`와 `.agents/skills/*/SKILL.md`를 직접 사용 |
| opencode | 가능 | `AGENTS.md`를 프로젝트 지침으로 읽고, 필요한 역할 `SKILL.md` 파일 경로를 프롬프트에 명시 |
| OpenClaw | 가능 | `AGENTS.md` 또는 `OPENCLAW.md`를 진입점으로 사용하고, 역할별 `SKILL.md`를 명시적으로 참조 |
| Hermes | 가능 | `AGENTS.md` 또는 `HERMES.md`를 진입점으로 사용하고, 역할별 `SKILL.md`를 명시적으로 참조 |
| Claude / Claude Code | 가능 | `AGENTS.md` 또는 `CLAUDE.md`를 진입점으로 사용하고, 역할별 `SKILL.md`를 명시적으로 참조 |
| Antigravity / Gemini 계열 | 가능 | `AGENTS.md` 또는 `GEMINI.md`를 진입점으로 사용하고, 역할별 `SKILL.md`를 명시적으로 참조 |
| 일반 LLM/IDE 에이전트 | 가능 | `README.md`, `team-spec.md`, `runbook.md`, 역할별 `SKILL.md`를 프롬프트에 첨부 또는 경로로 지시 |

자세한 내용은 `docs/harness/invest/cross-tool-usage.md`를 봅니다.

## 참고 문서

- 전체 역할 구조: `docs/harness/invest/team-spec.md`
- 실행 절차: `docs/harness/invest/runbook.md`
- 도구별 사용법: `docs/harness/invest/cross-tool-usage.md`
- 산출물 템플릿: `docs/harness/invest/templates/`
