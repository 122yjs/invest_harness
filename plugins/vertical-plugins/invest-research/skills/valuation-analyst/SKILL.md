---
name: valuation-analyst
description: Part VIII 밸류에이션 분석을 수행해 상대가치, DCF/간이 DCF, Bear/Base/Bull 시나리오별 적정가치를 정리하는 전문가 스킬
---

# valuation-analyst

## When to Use
- 투자 리포트의 Part VIII. 밸류에이션 분석을 작성할 때 사용한다.
- 현재 주가가 내재가치 대비 어느 수준인지 구조적으로 판단해야 할 때 사용한다.
- 동종업계 멀티플 비교, DCF 또는 간이 DCF, 시나리오별 목표가 산정이 필요할 때 사용한다.
- 최종 산출물은 `${ACTIVE_WORKSPACE}/03_valuation/findings.md`에 저장한다.
- `/comps` 요청에서는 비교기업 분석을 `${ACTIVE_WORKSPACE}/03_valuation/comps.md`에 저장한다.
- `/dcf` 요청에서는 DCF 결과와 교차검증을 `${ACTIVE_WORKSPACE}/03_valuation/dcf.md`에 저장한다.

## Required Inputs
- 대상 기업명, 티커, 거래소/국가
- 분석 기준일
- 기준 통화
- 회계 기준(IFRS, US GAAP 등)
- `${ACTIVE_WORKSPACE}/00_input/market-price-snapshot.md`
- 최신 주가, 시가총액, 순부채 또는 순현금
- 최근 연간/분기/TTM 재무 데이터
  - 매출
  - 영업이익
  - EBITDA
  - 순이익
  - 영업활동현금흐름
  - CapEx
  - FCF
- 희석 주식 수
- 비교기업 3~5개
- 상대가치평가용 멀티플
  - PER
  - Forward PER
  - PBR
  - PSR
  - EV/EBITDA
  - EV/Sales
  - 배당수익률
  - FCF Yield
- DCF 수행에 필요한 가정 또는 출처 확인값
  - 매출 성장률
  - 영업이익률
  - 세율
  - CapEx
  - 운전자본 변화
  - FCF 성장률
  - 할인율 또는 WACC
  - Terminal Growth
  - Terminal Value
  - 순부채
- 희석 주식 수
- 선택 입력: `${ACTIVE_WORKSPACE}/03_valuation/comps.md`
- 선택 입력: `${ACTIVE_WORKSPACE}/03_valuation/dcf.md`

## Workflow

<!-- BEGIN YFINANCE_MCP_TOOLS -->
### yfinance 활용 (전체 시장)

`yfinance_get_ticker_info`에서 밸류에이션 지표를 바로 추출할 수 있다. 동종업계 상대가치 비교에도 활용한다.

밸류에이션 순서:
1. `yfinance_get_ticker_info(symbol=...)` → currentPrice, targetMeanPrice, trailingPE, forwardPE, priceToBook, enterpriseToEbitda, priceToSalesTrailing12Months, dividendYield, freeCashflow, earningsPerShare
2. 피어 비교: 대상 기업 symbol로 위 지표 획득 → 같은 방식으로 경쟁사 symbol들도 호출
3. `yfinance_get_financials(symbol=..., frequency="annual")` → DCF 입력용 FCF 계산
4. 경쟁사 검색: `yfinance_get_top(sector=..., top_type="top_companies", top_n=5)` → 섹터 내 주요 기업 목록
<!-- END YFINANCE_MCP_TOOLS -->

<!-- BEGIN KOREA_STOCK_MCP_TOOLS -->
### 2.2 MCP 도구 우선 사용 (한국 상장기업 한정)

korea-stock-mcp MCP 서버가 설치된 환경에서는 한국 상장기업 밸류에이션 시 아래 MCP 도구를 사용한다.

| 도구 | 데이터 | 활용 |
|---|---|---|
| `get_financial_statement` | 연결/개별 XBRL 재무제표 | EPS, BPS, EBITDA 계산 |
| `get_stock_base_info` | 상장주식수 | 시가총액 계산 |
| `get_stock_trade_info` | 일별 종가 | PER, PBR, EV/EBITDA 계산 |

사용 순서:
1. `get_financial_statement`로 재무 데이터 획득
2. `get_stock_base_info`로 상장주식수 확인
3. `get_stock_trade_info`로 최근 거래일 종가 확인
4. 획득 데이터로 PER, PBR, EV/EBITDA, FCF Yield 계산

비교기업 피어 데이터는 웹 검색으로 보충한다.
<!-- END KOREA_STOCK_MCP_TOOLS -->

<!-- BEGIN INPUT_GATE_POLICY_INTEGRATED -->
## 최근 분기 실적·센티먼트 분석 추가 지시

입력 요약의 `분석 초점`이 `최근 분기 실적·센티먼트 심층형` 또는 `혼합형`이면 밸류에이션에서 다음을 별도 반영한다.

- 최근 분기 실적 이후 Forward 매출, EPS, EBITDA, FCF 컨센서스 변화
- 목표주가 및 투자의견 리비전
- 최근 분기 반영 전/후 멀티플 변화
- 피어의 최근 분기 실적 YoY/QoQ 성장과 마진 변화 대비 밸류에이션 프리미엄/디스카운트
- 특정 이벤트 / 촉매가 실적 추정과 멀티플에 미치는 영향
- 다음 1~2개 분기 컨센서스 미스/비트에 따른 Bear/Base/Bull 민감도
<!-- END INPUT_GATE_POLICY_INTEGRATED --> Steps
1. **분석 범위 확정 및 내러티브-DCF 가정 매핑 (Step 0)**
   - 분석 기준일, 통화, 회계기간(연간/최근 분기/TTM)을 명시한다.
   - `fundamental-analyst findings`의 핵심 비즈니스 내러티브(해자 종류, 성장 드라이버, 가격 결정력 등 정성적 스토리)를 정리하고, 이것이 DCF의 주요 입력값(성장률, 타겟 마진, 재투자율 등 정량적 숫자)으로 어떻게 번역되는지 보여주는 1페이지 매핑 표를 작성한다.
   - 데이터 부족 항목은 추정하지 말고 `공식 자료 미확인`, `데이터 부족`, `추가 확인 필요`로 표시한다.

2. **현재 시장지표 수집**
   - `${ACTIVE_WORKSPACE}/00_input/market-price-snapshot.md`의 기준 주가와 주식 수를 우선 사용한다.
   - 현재가, 시가총액, EV, PER, Forward PER, PBR, PSR, EV/EBITDA, EV/Sales, 배당수익률, FCF Yield를 수집하거나 재계산한다.
   - 산식 기반 값은 산식과 사용 데이터의 회계기간을 함께 적는다.
   - 서로 다른 출처 수치가 충돌하면 차이와 가능한 원인을 짧게 메모한다.

3. **동종업계 상대가치평가 수행**
   - 비교기업 3~5개를 선정하고 사업모델, 지역, 성장률, 수익성의 유사성을 확인한다.
   - PER, Forward PER, PBR, PSR, EV/EBITDA, EV/Sales, FCF Yield, 매출 성장률, 영업이익률을 비교한다.
   - 분기 비교가 가능하면 최근 분기 매출/영업이익/EPS/FCF의 YoY와 QoQ를 함께 제시한다.
   - 멀티플 수준만 비교하지 말고 YoY/QoQ 성장률과 마진 차이를 함께 해석한다.
   - reported financial fact와 guidance는 Company IR, SEC EDGAR, DART/KRX, local regulator filings 같은 T0 evidence를 우선하고, yfinance/FMP/Alpha Vantage는 T2 cross-check로 구분한다.
   - 대상 기업이 프리미엄/디스카운트 거래 중이면 정당화 요인을 제시한다.
   - `/comps` 요청이면 결과를 `${ACTIVE_WORKSPACE}/03_valuation/comps.md`에도 저장한다.

4. **DCF 또는 간이 DCF 수행 (가정의 일관성 및 할인율 세분화)**
   - 가능한 경우 5년 내외 예측 기반 DCF를 우선한다.
   - 데이터가 부족하면 FCF Yield 기반 간이 DCF 또는 보수적 범위 추정으로 대체한다.
   - 다음 가정을 반드시 표로 명시한다: 매출 성장률, 영업이익률, 세율, CapEx, 운전자본 변화, FCF 성장률, WACC, Terminal Growth, Terminal Value, 순부채, 희석 주식 수.
   - **WACC 구성 세분화**: WACC 가정을 단순 단일 숫자로 기입하지 않고, 무위험률, 주식위험프리미엄(ERP), 베타, 국가위험프리미엄, 자기자본비용(k_e), 세전 부채비용(k_d), 시장가치 가중치 E/(D+E) 및 D/(D+E)로 명시적으로 분해하여 상세 표로 작성한다. 실패확률(Probability of Failure) 조정이 필요한 경우 명시한다.
   - **성장-재투자-자본효율 일관성**: 성장률 가정은 `재투자율(Reinvestment Rate) × ROIC` 공식의 값과 정합성을 교차 검증하여, 터무니없는 성장 시나리오(재투자는 없는데 성장만 고공행진하는 등)가 나오지 않도록 조율한다.
   - 모든 가정은 출처 또는 합리적 근거를 붙이고, 확인되지 않은 가정을 임의로 넣지 않는다.
   - `/dcf` 요청이면 결과를 `${ACTIVE_WORKSPACE}/03_valuation/dcf.md`에도 저장한다.

5. **DCF / Comps / 역사적 밴드 교차검증**
   - DCF implied EV/EBITDA, 피어 EV/EBITDA, 역사적 PER 밴드, 현재 Forward PER, FCF Yield를 비교한다.
   - DCF만으로 `저평가` 결론을 확정하지 않는다.
   - 방법론 간 결론이 충돌하면 충돌 원인과 추가 확인 필요 항목을 분리한다.

6. **Bear / Base / Bull 시나리오 가치평가**
   - 시나리오별로 실적 경로, 멀티플 또는 DCF 핵심 가정, 적정가치, 현재가 대비 괴리를 정리한다.
   - 단일 숫자보다 범위와 조건을 우선 제시한다.
   - 상승여력/하락위험은 계산 기준을 명시한다.

7. **Rating / Price Target 입력값 정리**
   - Base-case 가치, 기준 주가, implied upside/downside, 주요 리스크를 연결한다.
   - Rating은 `Buy / Outperform / Neutral / Hold / Underperform / Sell` 중 하나만 사용한다.
   - Price Target 산출 방식은 DCF, 피어 멀티플, 역사적 밴드 중 어떤 방법을 사용했는지 명시한다.

8. **결론 작성**
   - 현재 주가가 `저평가`, `적정`, `고평가` 중 어디에 가까운지 신중한 문장으로 정리한다.
   - 가장 큰 민감도 변수(성장률, 마진, WACC, 터미널 성장률, 멀티플 정상화 등)를 분리해 적는다.
   - `확실한 매수` 같은 과도한 확신 표현은 사용하지 않는다.

9. **파일 저장**
   - 최종 결과를 `${ACTIVE_WORKSPACE}/03_valuation/findings.md`에 저장한다.

## Output Format

```markdown
# 밸류에이션 분석

## 0. 비즈니스 내러티브 - DCF 가정 매핑 (Step 0)

| 정성적 비즈니스 내러티브 (스토리) | DCF 핵심 가정을 위한 정량적 해석 | DCF 입력값 (성장률, 타겟 마진 등) |
|---|---|---|
| (예: 강력한 브랜드 해자로 가격 결정력 유지) | (가격 인상 효과가 매출 성장 및 이익률 방어로 연결) | (매출 성장률: 5.5%, 타겟 OPM: 24%) |
| (예: 신규 시장 진출 및 CapEx 확장) | (단기 성장 가속화 및 재투자율 증가, ROIC 일시 하락) | (1~3년차 성장률: 12%, 재투자율: 45%) |

- 정성적 스토리의 타당성 (Plausibility) 검토:
- 정량적 수치로의 번역 논리:

## 1. 분석 기준
- 기업명 / 티커:
- 분석 기준일:
- 기준 통화:
- 회계기간 기준:
- 사용 데이터 출처:

## 2. 현재 시장지표

| 항목 | 값 | 기준일 | 회계기간/산식 | 출처 |
|---|---:|---|---|---|
| 현재가 |  |  |  |  |
| 시가총액 |  |  |  |  |
| EV |  |  |  |  |
| PER |  |  |  |  |
| Forward PER |  |  |  |  |
| PBR |  |  |  |  |
| PSR |  |  |  |  |
| EV/EBITDA |  |  |  |  |
| EV/Sales |  |  |  |  |
| 배당수익률 |  |  |  |  |
| FCF Yield |  |  |  |  |

## 3. 동종업계 상대가치평가

| 기업 | 티커 | PER | Forward PER | EV/EBITDA | PSR | 최근 분기 매출 YoY | 최근 분기 매출 QoQ | 최근 분기 EPS YoY | 최근 분기 EPS QoQ | 영업이익률 | 평가 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 대상 기업 |  |  |  |  |  |  |  |  |  |  |  |
| 비교기업 1 |  |  |  |  |  |  |  |  |  |  |  |
| 비교기업 2 |  |  |  |  |  |  |  |  |  |  |  |
| 비교기업 3 |  |  |  |  |  |  |  |  |  |  |  |

### 상대가치 해석
- 프리미엄/디스카운트 여부:
- 정당화 요인:
- 비교 한계:

## 4. DCF / 간이 DCF 가정

| 가정 항목 | 값 | 적용 구간 | 근거 | 출처 |
|---|---|---|---|---|
| 매출 성장률 |  |  |  |  |
| 영업이익률 |  |  |  |  |
| 세율 |  |  |  |  |
| CapEx |  |  |  |  |
| 운전자본 변화 |  |  |  |  |
| FCF 성장률 |  |  |  |  |
| WACC / 할인율 |  |  |  |  |
| Terminal Growth |  |  |  |  |
| Terminal Value |  |  |  |  |
| 순부채 |  |  |  |  |
| 희석 주식 수 |  |  |  |  |

## 4-1. WACC 세부 구성 및 성장-재투자 일관성 검증 (Step 4)

### A. WACC 세부 분해 및 부도확률 조정
- **무위험자산 금리 (Risk-free Rate)**: % (예: 미국 10년물 국채 금리)
- **주식위험프리미엄 (ERP)**: % (기본 ERP % + 국가위험프리미엄 %)
- **베타 (Beta)**: (자산 베타 및 레버리지 조정 베타 명시)
- **자기자본비용 (k_e)**: %
- **세전 부채비용 (k_d)**: %
- **가중치**: 자기자본 E/(D+E) = %, 타인자본 D/(D+E) = %
- **최종 WACC**: %
- **부도확률 (Probability of Failure) 조정 여부 및 근거**: (조정 시 부도확률 및 부도시 잔존가치 회수율 적용 내역 기술)

### B. 성장-재투자-자본효율 일관성 교차검증
- **예상 영업이익 성장률 (g)**: %
- **기대 재투자율 (Reinvestment Rate = (CapEx - D&A + ΔNWC) / EBIT(1-t))**: %
- **기대 투하자본수익률 (ROIC)**: %
- **일관성 검증 공식 결과 (Expected g = Reinvestment Rate × ROIC)**: %
- **가정 정합성 평가 (예: 성장은 높으나 재투자가 거의 없는 모순 등 검증)**:

## 5. DCF / 간이 DCF 결과

| 항목 | 값 | 비고 |
|---|---:|---|
| 영업가치 합계 |  |  |
| 비영업 조정 |  |  |
| 순부채 반영 후 지분가치 |  |  |
| 주당 적정가치 |  |  |
| 현재가 대비 괴리 |  |  |

## 6. DCF / Comps / 역사적 밴드 교차검증

| 검증 항목 | 대상 기업 | 비교 기준 | 결론 | 한계 |
|---|---:|---:|---|---|
| DCF implied EV/EBITDA |  |  |  |  |
| 피어 EV/EBITDA |  |  |  |  |
| 역사적 PER 밴드 |  |  |  |  |
| 현재 Forward PER |  |  |  |  |
| FCF Yield |  |  |  |  |

## 7. 시나리오별 가치평가

| 시나리오 | 핵심 가정 | 적정가치 / 목표가 | 현재가 대비 상승여력 | 주요 조건 |
|---|---|---:|---:|---|
| Bear |  |  |  |  |
| Base |  |  |  |  |
| Bull |  |  |  |  |

## 8. Rating / Price Target 근거
- 기준 주가:
- Price Target / 가치 범위:
- Implied Upside / Downside:
- 예비 Rating:
- Rating 근거:
- Risk-Reward 요약:

## 9. 민감도 및 핵심 불확실성
- 가장 민감한 변수:
- 멀티플 정상화 위험:
- 추정 한계:

### 2차원 민감도 분석 (매출 성장률 × 영업이익률)
*참고: 아래 표는 할인율(WACC) 외에 사업적 가정이 기업 가치에 미치는 영향을 다모다란 프레임워크에 의거하여 추가 산출한 결과입니다.*

| 매출 성장률 \ 영업이익률 | OPM (Bear/최소) | OPM (Base/적정) | OPM (Bull/최고) |
|---|---|---|---|
| **성장률 (Low)** | 주당 가치: | 주당 가치: | 주당 가치: |
| **성장률 (Base)** | 주당 가치: | 주당 가치: **(Base Case)** | 주당 가치: |
| **성장률 (High)** | 주당 가치: | 주당 가치: | 주당 가치: |

## 10. 밸류에이션 결론
- 현재 주가 판단:
- 비교기업 대비 프리미엄/디스카운트 해석:
- 목표가 또는 가치범위 산출 근거:
- 가장 큰 불확실성:

## 11. 3~5줄 요약
-
-
-
```

### 12. 📊 대시보드 데이터 블록

findings.md 맨 끝에 아래 YAML 코드블록을 **반드시** 추가한다. `html-report-synthesizer`가 이 블록을 파싱하여 풀밼 필드, 민감도 매트릭스, 피어 비교 표에 데이터를 주입한다.

````markdown
```yaml
# === 대시보드 데이터 블록 ===
dashboard_data:
  currency: ""
  current_price: null
  shares_outstanding: null  # 희석 주식 수 (백만)
  scenarios:
    bear:
      target_price: null
      rating: ""
      upside_pct: null
      key_assumption: ""
      fcf_estimate: null  # Bear 시나리오 예상 FCF
    base:
      target_price: null
      rating: ""
      upside_pct: null
      key_assumption: ""
      fcf_estimate: null
    bull:
      target_price: null
      rating: ""
      upside_pct: null
      key_assumption: ""
      fcf_estimate: null
  sensitivity_matrix:  # WACC(rows) x PGR(cols) 5x5
    wacc_values: [8.0, 9.0, 10.0, 11.0, 12.0]
    pgr_values:  [1.0, 1.5, 2.0, 2.5, 3.0]
    implied_prices:    # 5x5 배열 (WACC 행, PGR 열)
      - [null, null, null, null, null]
      - [null, null, null, null, null]
      - [null, null, null, null, null]
      - [null, null, null, null, null]
      - [null, null, null, null, null]
  peers:  # 피어 멀티플 비교
    - {name: "", ticker: "", pe: null, fwd_pe: null, ev_ebitda: null, ps: null, opm_pct: null}
```
````

## Validation Notes
- 모든 핵심 수치에 출처, 기준일, 회계기간, 통화를 붙인다.
- 최신 연간/분기/TTM 데이터를 혼용할 경우 구분을 명확히 적는다.
- EV, FCF Yield, 주당 가치 등 계산값은 산식을 남긴다.
- 기준 주가와 시가총액은 `${ACTIVE_WORKSPACE}/00_input/market-price-snapshot.md`와 일치해야 한다.
- DCF 가정값은 임의 숫자 사용 금지, 근거 불충분 시 범위 또는 `추가 확인 필요`로 표기한다.
- 비교기업은 사업구조와 지역 노출이 크게 다르면 한계를 명시한다.
- DCF, comps, 역사적 밴드가 충돌하면 단일 결론으로 덮지 말고 교차검증 한계를 기록한다.
- 결론은 일반적 분석 의견이어야 하며 투자 자문처럼 단정하지 않는다.
- **`📊 대시보드 데이터 블록`이 findings.md 끝에 반드시 포함되어야 한다.** 이 블록이 없으면 html-report-synthesizer가 풀밼 필드, 민감도 매트릭스, 피어 표를 렌더링할 수 없다.
