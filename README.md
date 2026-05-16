# Invest Harness

개별 상장기업 투자 리서치 리포트를 반복적으로 생성하기 위한 AI agent Harness입니다. `invest_prompt_v2.md`의 분석 요구사항을 여러 전문가 역할로 나누고, `${ACTIVE_WORKSPACE}/` 파일 핸드오프를 통해 초안, QA, 최종본까지 재현 가능하게 조립합니다.

이 레포의 결과물은 정보 제공용 분석입니다. 개인화된 투자 자문이나 매매 권유로 사용하지 않습니다.

Evidence Planning / Source Routing / Signal Primitive 레이어는 기존 analyst fan-out 전에 실행되는 근거 계획 계층입니다. 소스 선택은 고정 유즈케이스가 아니라 evidence type, source capability, claim boundary를 기준으로 하며, 예시 시나리오는 비포괄 eval fixture로만 둡니다. 자세한 계약은 `docs/harness/invest/research-layer/`를 참조합니다.

## 빠른 시작

<!-- BEGIN INPUT_GATE_USAGE_EXAMPLE_INTEGRATED -->
예시 입력:

```text
CSTM 분석해줘.
진행 방식: 일괄
분석 초점: 혼합
투자 기간: 전체
비교기업 수: 5
보고서 깊이: 심층
특정 이벤트 / 촉매: 관세
```

최소 입력도 가능하다.

```text
AAPL 분석해줘. 나머지는 기본값.
```

이 경우 Harness는 AAPL을 기준으로 기업명, 거래소, 상장 통화, 회계 기준을 자동 확인하고, 선택 옵션은 기본값을 적용한다.
<!-- END INPUT_GATE_USAGE_EXAMPLE_INTEGRATED -->

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
| `docs/harness/invest/research-layer/` | Evidence planning, source capability, signal primitive, validation, claim boundary 계약 |
| `docs/harness/invest/templates/` | 반복 실행용 산출물 템플릿 |
| `scripts/Test-HarnessStructure.ps1` | Harness 구조 검증 스크립트 |
| `docs/harness/invest/cross-tool-usage.md` | Codex, opencode, Antigravity 등 도구별 사용 방식 |
| `OPENCLAW.md` | OpenClaw 계열 에이전트를 위한 얇은 진입점 |
| `HERMES.md` | Hermes 계열 에이전트를 위한 얇은 진입점 |
| `GEMINI.md` | Gemini/Antigravity 계열 에이전트를 위한 얇은 진입점 |
| `CLAUDE.md` | Claude / Claude Code 계열 에이전트를 위한 얇은 진입점 |

## 리포트 생성 흐름

각 실행은 먼저 동적 `ACTIVE_WORKSPACE`를 확정한다. 기본 형식은 `_workspace_{TICKER_OR_SLUG}_{YYYYMMDD}/`이고, 같은 경로가 이미 있거나 legacy `_workspace` 디렉터리에 `.running` marker가 있으면 시각 suffix가 붙은 새 workspace를 사용한다. 런타임은 선택된 workspace에 `.running` marker를 남겨 후속 세션이 같은 경로를 재사용하지 않게 한다. OpenClaw, Hermes 등 여러 세션을 동시에 쓸 때도 같은 `${ACTIVE_WORKSPACE}/`를 공유하지 않는다.

1. 입력을 정리합니다.
   - 산출물: `${ACTIVE_WORKSPACE}/00_input/request-summary.md`
   - 담당: `invest-orchestrator`

2. Evidence layer를 실행합니다.
   - 산출물: `${ACTIVE_WORKSPACE}/00_evidence/evidence-plan.md`, `${ACTIVE_WORKSPACE}/00_evidence/source-call-plan.md`, `${ACTIVE_WORKSPACE}/00_evidence/evidence-ledger.md`, `${ACTIVE_WORKSPACE}/00_evidence/signal-cards.md`
   - 담당: `evidence-planner`, `source-router`, `signal-analyst`
   - 원칙: source capability 기반 선택, claim boundary 보존

3. 전문가 분석을 작성합니다.
   - 재무: `${ACTIVE_WORKSPACE}/01_financial/findings.md`
   - 산업/경쟁/해자/제품: `${ACTIVE_WORKSPACE}/02_fundamental/findings.md`
   - 밸류에이션: `${ACTIVE_WORKSPACE}/03_valuation/findings.md`
   - 기술적 분석: `${ACTIVE_WORKSPACE}/04_technical/findings.md`
   - 뉴스/센티먼트/거시: `${ACTIVE_WORKSPACE}/05_macro_sentiment/findings.md`
   - 리스크/시나리오: `${ACTIVE_WORKSPACE}/06_risk_scenario/findings.md`

4. 충돌을 기록합니다.
   - 산출물: `${ACTIVE_WORKSPACE}/06_risk_scenario/conflicts.md`
   - 수치, 출처, 기준일, 회계기간이 충돌할 때만 작성합니다.

5. 초안을 합성합니다.
   - 산출물: `${ACTIVE_WORKSPACE}/07_draft/report.md`
   - 담당: `report-synthesizer`

6. QA를 수행합니다.
   - 산출물: `${ACTIVE_WORKSPACE}/09_qa/review.md`
   - 담당: `qa-reviewer`
   - source/claim audit에서 relative search interest, trade data, procurement, market context가 과잉 주장되지 않았는지 확인합니다.

7. 최종본을 확정합니다.
   - 산출물: `${ACTIVE_WORKSPACE}/08_final/report.md`
   - 선택 요약본: `${ACTIVE_WORKSPACE}/08_final/executive-summary.md`

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

<!-- BEGIN MCP_README -->
<!-- BEGIN YFINANCE_README -->
### yfinance-mcp 통합 (글로벌)

`yfinance-mcp` MCP 서버를 통해 Yahoo Finance 데이터를 API 키 없이 바로 조회할 수 있다. 미국/글로벌 기업 분석의 주력 데이터 소스이며, 한국 기업 분석 시에도 korea-stock-mcp와 함께 보조로 사용한다.

| MCP 도구 | 데이터 | 사용 역할 |
|---|---|---|
| `yfinance_get_ticker_info` | 기업 정보, 재무, 밸류에이션 | all roles |
| `yfinance_get_financials` | 재무제표 (연간/분기) | financial-analyst, valuation-analyst |
| `yfinance_get_price_history` | OHLCV + 차트 생성 | technical-analyst |
| `yfinance_get_ticker_news` | 최근 뉴스 | macro-sentiment-analyst |
| `yfinance_get_holders` | 주요 주주, 기관 보유 | fundamental-analyst |
| `yfinance_get_option_chain` | 옵션 체인 데이터 | technical-analyst, risk-scenario-analyst |
| `yfinance_search` | 종목/ETF 검색 | orchestrator |
| `yfinance_get_top` | 섹터별 상위 종목 | fundamental-analyst |

사용 규칙은 각 역할별 SKILL.md의 MCP 도구 사용 규칙 섹션을 참조한다.
<!-- END YFINANCE_README -->
### MCP 도구 통합

korea-stock-mcp MCP 서버가 설치된 환경에서는 한국 상장기업 분석 시 DART/KRX 공식 API를 직접 호출할 수 있다.

| MCP 도구 | 데이터 출처 | 사용 역할 |
|---|---|---|
| `get_financial_statement` | DART XBRL 재무제표 | financial-analyst, valuation-analyst |
| `get_stock_trade_info` | KRX 일별 주가/거래량 | technical-analyst, macro-sentiment-analyst |
| `get_disclosure_list` / `get_disclosure` | DART 공시 원문 | fundamental-analyst, macro-sentiment-analyst |
| `get_stock_base_info` | KRX 종목 기본정보 | financial-analyst, fundamental-analyst |
| `get_corp_code` | DART 고유번호/종목코드 | orchestrator (기업 식별) |

자세한 사용 규칙은 각 역할별 SKILL.md의 MCP 도구 사용 규칙 섹션을 참조한다.

### Source capability registry와 MCP 범위

이 README에 명시된 callable 공개 MCP는 `yfinance-mcp`와 `korea-stock-mcp`이다. 추가 source는 `docs/harness/invest/research-layer/source-capability-registry.md`의 `connection_status`로 판단한다.

현재 기본 repo 설정에서 `.mcp.institutional.json`은 `enabled: false`이고 `mcpServers`가 비어 있으므로, FRED, SEC EDGAR, Alpha Vantage를 connected MCP로 단정하지 않는다. 이 source들은 registry에서 repo evidence에 따라 `documented_only` 또는 `external_manual` source contract로 표현하고, 실제 callable tool/config가 확인될 때만 connected로 승격한다.

KOSIS, customs_trade_api, Google Trends, Naver DataLab, KOTRA, G2B는 이번 패스에서 docs-only source contract와 routing/validation 규칙만 제공한다. 중복 API client, 새 credentials, 또는 `.mcp.institutional.json` 변경은 이 README의 기본 실행 경로에 포함하지 않는다.
<!-- END MCP_README -->

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

이 Harness는 특정 에이전트 런타임에 의존하지 않도록 설계되어 있습니다. 핵심 계약은 모두 Markdown 파일과 `${ACTIVE_WORKSPACE}/` 산출물 경로로 표현됩니다.

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
