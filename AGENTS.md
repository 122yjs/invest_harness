# AGENTS.md

## WHAT
- 이 저장소는 개별 주식 투자 리포트 Harness를 정의한다.
- 목표는 `invest_prompt_v2.md`의 16개 분석 파트와 18개 최종 리포트 섹션을 일관된 멀티에이전트 워크플로우로 분해·조립하는 것이다.

## WHY

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
- 방대한 투자 리서치를 병렬화해 속도와 깊이를 함께 확보한다.
- 모든 판단은 출처, 기준일, 회계기간, 통화, 가정을 분리해 재현 가능해야 한다.
- 최종 결과는 정보 제공용 분석이며 개인화된 투자 자문이 아니다.

## HOW
- 리서치는 Fan-out/Fan-in과 Pipeline을 결합해 진행한다.
- 기존 analyst fan-out 전에 Evidence Planning / Source Routing / Signal Primitive 레이어를 실행한다.
- 소스 선택은 고정 유즈케이스나 상품 enum이 아니라 evidence type, source capability, validation gate, claim boundary를 기준으로 한다.
- 예시 시나리오는 `docs/harness/invest/evals/golden-scenarios/` 같은 eval fixture에만 두며 core router category로 승격하지 않는다.
- 파트별 분석 결과는 `_workspace/`에 표준 파일명으로 저장하고, 최종 리포트는 조립 후 QA를 거친다.
- 확인되지 않은 수치, 출처 없는 주장, 과도한 확신 표현은 금지한다.
- 최신 연간/분기/TTM 데이터를 구분하고, 충돌 수치는 차이와 원인을 함께 적는다.
- 기술적 분석과 소셜 센티먼트는 보조 신호로만 사용한다.

## CANONICAL PATHS

<!-- BEGIN MCP_ENTRY -->
<!-- BEGIN MCP_SERVERS_LIST -->
### MCP 서버 목록

| 서버명 | 데이터 소스 | 범위 | API 키 |
|---|---|---|---|
| `korea-stock` | DART + KRX 공식 API | 한국 (코스피/코스닥/코넥스) | DART_API_KEY / KRX_API_KEY |
| `yfinance` | Yahoo Finance (yfinance) | **전 세계** | 불필요 |

사용 전략:
- **한국 기업**: korea-stock 1순위 + yfinance 보조
- **미국/글로벌 기업**: 현재 repo에서 callable tool contract가 확인되는 공개 MCP는 yfinance이며, SEC EDGAR/FRED/Alpha Vantage 같은 추가 source는 `source-capability-registry.md`의 `connection_status`와 실제 callable repo evidence를 먼저 확인한다
- repo에서 callable 설정이나 구체 tool contract가 확인되지 않은 source는 connected로 간주하지 않고 `documented_only`, `planned`, 또는 `external_manual` data gap으로 기록한다
- 연결된 MCP 서버는 웹 검색보다 우선 순위가 높다

각 역할별 상세 MCP 도구 사용법은 해당 SKILL.md의 `사용 가능한 MCP 도구` 섹션을 참조한다.
<!-- END MCP_SERVERS_LIST -->
## MCP 도구 통합

한국 상장기업 분석 시 `korea-stock-mcp` MCP 서버를 통해 DART/KRX 공식 API 데이터를 직접 조회할 수 있다.

- MCP 서버명: `korea-stock`
- 제공 도구: `get_corp_code`, `get_disclosure_list`, `get_disclosure`, `get_financial_statement`, `get_stock_base_info`, `get_stock_trade_info`, `get_market_type`, `get_today_date`
- 사용 조건: 한국 상장기업 한정. 해외 기업은 yfinance와 source capability registry를 우선 확인하고, callable source가 없을 때만 웹 검색을 source discovery 보조로 사용
- 사용 방식: 각 SKILL.md의 MCP 도구 사용 규칙 참조

전체 도구 명세와 사용 순서는 각 역할별 SKILL.md에 정의되어 있다.
<!-- END MCP_ENTRY -->
- 핵심 프롬프트: `invest_prompt_v2.md`
- 팀 명세: `docs/harness/invest/team-spec.md`
- 작업 산출물: `_workspace/`
- Evidence layer 산출물: `${ACTIVE_WORKSPACE}/00_evidence/`
- Evidence layer 계약: `docs/harness/invest/research-layer/`
- 역할 확장 경로: `docs/harness/invest/roles/`
- 실행 가이드: `docs/harness/invest/runbook.md`
