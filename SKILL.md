---
name: invest-harness
description: >
  개별 주식 투자 리포트 Harness.
  invest_prompt_v2.md의 16개 분석 파트를 멀티에이전트로 병렬 수행 후
  18개 섹션의 최종 리포트를 조립합니다.
  재무·정성·밸류에이션·기술적·매크로·리스크·합성·QA 역할을 포함합니다.
---

# invest-harness

## When to Use

- 사용자가 특정 상장기업의 투자 리포트를 요청했을 때
- 재현 가능한 출처 기반 리서치 워크플로우가 필요할 때
- `invest_prompt_v2.md`의 분석 프레임워크를 따를 때

## Quick Start

```text
AGENTS.md와 docs/harness/invest/runbook.md를 따른다.
invest-orchestrator를 오케스트레이터 지침으로 사용해서
Apple(AAPL, NASDAQ)을 기준일 2026-05-10, 표준형, 혼합형 투자자 관점으로 분석해줘.
모든 산출물은 docs/harness/invest/team-spec.md의 _workspace 계약을 따른다.
```

## Sub-skills

| Role | Skill Name | Scope |
|---|---|---|
| 오케스트레이터 | `invest-orchestrator` | 입력 정규화, 역할 분배, QA 반영, 최종본 확정 |
| 재무 | `financial-analyst` | 기업 개요, 재무제표, 재묵비율 |
| 정성 | `fundamental-analyst` | 산업, 경쟁, 경영진, 거버넌스, 해자, 제품/서비스 |
| 밸류에이션 | `valuation-analyst` | 상대가치, DCF/간이 DCF, 시나리오별 가치 |
| 기술적 분석 | `technical-analyst` | 가격 추세, 이동평균, RSI, MACD, 지지/저항 |
| 매크로·센티먼트 | `macro-sentiment-analyst` | 뉴스, 시장 센티먼트, 애널리스트 의견, 거시/정책 |
| 리스크·시나리오 | `risk-scenario-analyst` | 리스크 등록부, Bear/Base/Bull 시나리오 |
| 합성 | `report-synthesizer` | 전문가 findings를 18개 최종 섹션으로 조립 |
| QA | `qa-reviewer` | 출처, 수치, 구조, 논리, 문체, 투자 자문 경계 검토 |

## Key Documents

- `AGENTS.md` — 저장소 전체 작업 규칙과 canonical path
- `README.md` — Harness 개요 및 리포트 생성 흐름
- `invest_prompt_v2.md` — 원본 분석 요구사항과 최종 출력 구조
- `docs/harness/invest/runbook.md` — 실행 순서
- `docs/harness/invest/team-spec.md` — 역할 분담, 산출물 계약, 실패 정책
- `docs/harness/invest/templates/` — 반복 실행용 산출물 템플릿

## Workspace Contract

모든 산출물은 현재 실행의 active workspace인 `_workspace/`에 아래 구조로 저장됩니다:

```
_workspace/
  00_input/request-summary.md
  01_financial/findings.md
  02_fundamental/findings.md
  03_valuation/findings.md
  04_technical/findings.md
  05_macro_sentiment/findings.md
  06_risk_scenario/findings.md
  06_risk_scenario/conflicts.md
  07_draft/report.md
  08_final/report.md
  08_final/executive-summary.md  (선택)
  09_qa/review.md
```

### 반복 실행 보존 규칙

- 새 리서치를 시작하기 전에 `_workspace/`에 기존 산출물이 있으면 삭제하지 않는다.
- 기존 산출물은 `_workspace_runs/<YYYY-MM-DD>-<ticker-or-slug>/`로 먼저 이동해 보존한다. 같은 이름이 이미 있으면 `-HHMMSS` 또는 `-2`처럼 충돌 없는 suffix를 붙인다.
- 기본 동작은 **move 후 새 `_workspace/` 생성**이다. 런타임 권한상 move가 불가능할 때만 copy를 사용하고, copy가 끝난 뒤 보존 여부를 확인하기 전에는 기존 파일을 비우지 않는다.
- `_workspace/`는 현재 실행의 작업 디렉터리이고, `_workspace_runs/`는 이전 실행의 감사/재현 archive다. 새 실행은 archive 안의 파일을 덮어쓰지 않는다.
- 모든 하위 역할에는 `ACTIVE_WORKSPACE`를 절대 경로로 전달한다. `ACTIVE_WORKSPACE`는 현재 실행의 `_workspace` 디렉터리를 가리킨다.

## Quality Rules

- 모든 핵심 수치에는 출처, 기준일, 회계기간, 통화, 산식을 남긴다.
- Company IR, SEC EDGAR, DART/KRX, local regulator filing 같은 T0 official disclosure를 reported financial fact의 우선 근거로 사용한다.
- 최신 연간, 최근 분기, TTM 데이터를 구분한다.
- 최근 분기 재무 비교와 peer financial comparison에는 가능한 경우 YoY와 QoQ를 함께 제공한다.
- 출처가 충돌하면 임의로 평균 내지 않고 차이와 원인을 기록한다.
- 데이터가 부족하면 `공식 자료 미확인`, `데이터 부족`, `추가 확인 필요`로 표시한다.
- 기술적 분석과 소셜 센티먼트는 보조 신호로만 사용한다.
- 최종 보고서는 정보 제공용 분석이며 개인화된 투자 자문이 아님을 명시한다.

## Pitfalls & Operating Notes

### 1. Delegate Task Path Mismatch

`delegate_task`로 서브에이전트를 실행할 때, 서브에이전트는 자신의 기본 워크스페이스에 파일을 저장할 수 있다. 오케스트레이터가 별도의 프로젝트 디렉터리나 run archive를 생성해도 서브에이전트는 그 경로를 자동으로 알지 못한다.

**해결:** 오케스트레이터가 현재 실행의 `_workspace` 절대 경로를 `ACTIVE_WORKSPACE`로 정하고, `delegate_task`의 `context`에 명시한다. 서브에이전트의 `write_file`과 `read_file`은 `${ACTIVE_WORKSPACE}/01_financial/findings.md`처럼 같은 active workspace 아래를 사용한다. `~/.hermes/workspace/_workspace/`는 Hermes 기본값일 뿐이며, 모든 실행에 고정하지 않는다.

**증상:** risk-scenario-analyst가 `04_technical/findings.md`와 `05_macro_sentiment/findings.md`를 "존재하지 않음"으로 판단할 수 있다. 이는 파일이 실제로 존재하지만 경로 불일치로 인해 접근하지 못한 경우다.

### 2. Report-Synthesizer Numerical Drift

`report-synthesizer`가 여러 findings를 조립할 때, 경쟁사 비교 테이블 등에서 원천 findings의 수치와 불일치하는 "드리프트"가 발생할 수 있다. 특히:
- PER, EV/EBITDA, PBR 등 멀티플
- 영업이익률 vs 순이익률 혼동
- Adjusted vs GAAP 수치 교차

**해결:** report-synthesizer가 초안을 작성한 후, 반드시 원천 findings의 핵심 테이블과 수치를 교차 대조하는 self-check 단계를 거친다. 경쟁사 테이블은 03_valuation findings의 멀티플을 우선 따른다.

### 3. Conflicts.md Handling

선행 산출물 간 수치 충돌이 발생하면 `06_risk_scenario/conflicts.md`에 기록된다. report-synthesizer는 이 충돌 목록을:
- 초안의 해당 섹션에 주석으로 반영하고
- "한계 및 추가 확인 필요 사항" 섹션에 종합적으로 명시해야 한다.

충돌 수치를 임의로 평균 내거나 하나를 무작위로 선택해서는 안 된다.

## References

- `references/session-notes/` — 실제 Harness 실행 세션에서 발견된 함정, 수정 기록, 워크플로우 개선 사항
