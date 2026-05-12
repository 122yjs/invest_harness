---
name: risk-scenario-analyst
description: Part XII 리스크 분석과 Part XIII 시나리오 분석을 수행하여 ${ACTIVE_WORKSPACE}/06_risk_scenario/findings.md와 conflicts.md를 정리하는 전문가 스킬
---

# risk-scenario-analyst

## When to Use

- 투자 리포트의 Part XII. 리스크 분석을 작성할 때 사용한다.
- 투자 리포트의 Part XIII. 시나리오 분석을 작성할 때 사용한다.
- 기업 고유, 산업, 재무, 시장, 정책·규제 리스크를 발생 가능성과 영향도로 분류해야 할 때 사용한다.
- Bear/Base/Bull 시나리오를 선행 분석 결과와 연결해 작성해야 할 때 사용한다.

## Required Inputs

- `${ACTIVE_WORKSPACE}/00_input/request-summary.md`
- `${ACTIVE_WORKSPACE}/01_financial/findings.md`
- `${ACTIVE_WORKSPACE}/02_fundamental/findings.md`
- `${ACTIVE_WORKSPACE}/03_valuation/findings.md`
- `${ACTIVE_WORKSPACE}/04_technical/findings.md`
- `${ACTIVE_WORKSPACE}/05_macro_sentiment/findings.md`

선행 산출물이 없으면 사용 가능한 자료 범위를 명시하고, 부족한 항목을 `추가 확인 필요`로 남긴다.

## Workflow

<!-- BEGIN YFINANCE_MCP_TOOLS -->
### yfinance 활용 (전체 시장)

`yfinance_get_financials`로 부채/유동성 지표, `yfinance_get_option_chain`으로 옵션 시장 신호를 확인한다.

리스크/시나리오 순서:
1. `yfinance_get_financials(symbol=..., frequency="annual")` → 총부채, 유동부채, 현금, 이자비용
2. `yfinance_get_option_dates(symbol=...)` → 옵션 만기일 확인
3. `yfinance_get_option_chain(symbol=..., expiration_date=..., option_type="call"|"put")` → 옵션 시장 신호
4. `yfinance_get_ticker_info(symbol=...)` → beta, shortRatio, shortPercentOfFloat 등 리스크 지표
5. `yfinance_get_holders(symbol=..., max_rows=20)` → 기관/내부자 보유 변화
<!-- END YFINANCE_MCP_TOOLS -->

<!-- BEGIN KOREA_STOCK_MCP_TOOLS -->
### 2.2 MCP 도구 우선 사용 (한국 상장기업 한정)

korea-stock-mcp MCP 서버가 설치된 환경에서는 한국 상장기업 리스크/시나리오 분석 시 아래 MCP 도구를 사용한다.

| 도구 | 데이터 | 활용 |
|---|---|---|
| `get_financial_statement` | 부채, 유동성, 이자비용 | 재무 리스크 지표 |
| `get_disclosure_list` / `get_disclosure` | 공시 원문 | 소송, 규제, 공시 리스크 확인 |
| `get_stock_trade_info` | 변동성(ATR), 거래량 | 시장 리스크 확인 |

MCP 도구 결과와 웹 검색 데이터를 종합해 Bear/Base/Bull 시나리오를 구성한다.
<!-- END KOREA_STOCK_MCP_TOOLS -->

<!-- BEGIN INPUT_GATE_POLICY_INTEGRATED -->
## 최근 분기 실적·센티먼트 분석 추가 지시

입력 요약의 `분석 초점`이 `최근 분기 실적·센티먼트 심층형` 또는 `혼합형`이면 리스크와 시나리오에서 다음을 반영한다.

- 다음 1~2개 분기 실적 미스 리스크
- 가이던스 하향 리스크
- 컨센서스 리비전 둔화 또는 반전 리스크
- 센티먼트 과열/냉각 리스크
- 특정 이벤트 / 촉매가 Bear/Base/Bull 확률을 어떻게 바꾸는지
- 최근 분기 데이터가 기존 장기 논지를 강화/유지/약화하는지
<!-- END INPUT_GATE_POLICY_INTEGRATED --> Steps

1. **입력 범위 확인**
   - 어떤 선행 findings를 읽었는지 목록화한다.
   - 누락된 findings가 있으면 리스크 분석의 한계로 기록한다.

2. **리스크 후보 추출**
   - 기업 고유 리스크: 실적 부진, 고객 집중도, 제품 경쟁력 약화, 경영진 리스크, 회계 리스크
   - 산업 리스크: 경쟁 심화, 기술 변화, 대체재, 공급망, 원자재 가격
   - 재무 리스크: 부채 부담, 현금흐름 악화, 유동성 부족, 희석 가능성
   - 시장 리스크: 금리, 환율, 경기 침체, 유동성 축소, 밸류에이션 압축
   - 정책·규제 리스크: 반독점, 수출 규제, 보조금 축소, 환경 규제, 세제 변경

3. **리스크 평가**
   - 각 리스크의 발생 가능성과 영향도를 높음 / 중간 / 낮음으로 평가한다.
   - 근거가 약하면 등급을 단정하지 말고 불확실성을 적는다.
   - 대응 또는 모니터링 지표를 함께 제시한다.

4. **충돌 및 불일치 기록**
   - 선행 산출물 사이의 수치, 기준일, 해석 충돌을 찾는다.
   - 필요한 경우 `${ACTIVE_WORKSPACE}/06_risk_scenario/conflicts.md`에 충돌 목록을 작성한다.

5. **시나리오 분석**
   - Bear, Base, Bull 시나리오별 확률, 핵심 가정, 예상 주가 방향, 촉발 요인, 리스크를 작성한다.
   - 각 시나리오에는 실적 가정, 밸류에이션 가정, 산업 환경, 거시 환경, 주가 범위, 확인 이벤트를 포함한다.
   - 확률은 정밀 예측이 아니라 분석 프레임임을 명시한다.

6. **파일 저장**
   - 최종 결과를 `${ACTIVE_WORKSPACE}/06_risk_scenario/findings.md`에 저장한다.
   - 충돌이 있으면 `${ACTIVE_WORKSPACE}/06_risk_scenario/conflicts.md`에 별도로 저장한다.

## Output Format

```markdown
# 리스크 및 시나리오 분석

## 1. 분석 기준
| 항목 | 내용 |
|---|---|
| 기업명 / 티커 |  |
| 분석 기준일 |  |
| 사용한 선행 산출물 |  |
| 투자 기간 |  |
| 사용한 가정 |  |

## 2. 리스크 등록부
| 리스크 | 분류 | 발생 가능성 | 영향도 | 설명 | 대응 또는 모니터링 지표 | 근거 |
|---|---|---|---|---|---|---|

## 3. 핵심 리스크 우선순위
| 순위 | 리스크 | 우선순위 근거 | 단기 영향 | 중장기 영향 |
|---:|---|---|---|---|

## 4. 시나리오 분석
| 시나리오 | 확률 | 핵심 가정 | 예상 주가 방향 | 촉발 요인 | 리스크 |
|---|---:|---|---|---|---|
| Bear |  |  |  |  |  |
| Base |  |  |  |  |  |
| Bull |  |  |  |  |  |

## 5. 시나리오별 세부 가정
| 시나리오 | 실적 가정 | 밸류에이션 가정 | 산업 환경 | 거시 환경 | 주가 범위 | 확인 이벤트 |
|---|---|---|---|---|---|---|
| Bear |  |  |  |  |  |  |
| Base |  |  |  |  |  |  |
| Bull |  |  |  |  |  |  |

## 6. 모니터링 연결
| 모니터링 항목 | 확인 주기 | 긍정 신호 | 부정 신호 | 연결 리스크 |
|---|---|---|---|---|

## 7. 3~5줄 요약
-
-
-

## 데이터 한계 및 추가 확인 필요 사항
- 공식 자료 미확인:
- 데이터 부족:
- 추가 확인 필요:
```

충돌 파일 형식:

```markdown
# 분석 충돌 및 재확인 필요 사항

| 유형 | 항목 | 출처 A | 출처 B | 차이 | 가능한 원인 | 처리 방안 |
|---|---|---|---|---|---|---|
```

## Validation Notes

- 리스크는 단순 나열이 아니라 발생 가능성, 영향도, 모니터링 지표를 함께 제시한다.
- 시나리오 확률과 주가 방향은 근거와 조건을 붙인다.
- 충돌 수치는 임의 평균하지 않는다.
- 선행 산출물이 부족하면 부족 자체를 한계로 표시한다.
- 최종 의견처럼 보이는 단정 표현을 피하고, 시나리오별 조건부 표현을 사용한다.
