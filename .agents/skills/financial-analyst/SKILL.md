---
name: financial-analyst
description: 기업 개요(Part II)와 재무제표·재무비율 분석(Part III)을 수행하여 ${ACTIVE_WORKSPACE}/01_financial/findings.md에 구조화된 재무 리서치 결과를 작성하는 스킬
---

<!-- GENERATED-SYNC: source=plugins/vertical-plugins/invest-research/skills/financial-analyst/SKILL.md; kind=skill; script=scripts/sync_invest_skills.py -->
> [!IMPORTANT]
> Generated execution artifact. Do not edit directly; edit the vertical source and rerun python scripts/sync_invest_skills.py (or scripts/Sync-InvestSkills.ps1 / scripts/Sync-InvestSkills.sh).
> Common policies are synced from plugins/vertical-plugins/invest-research/policies/.
> Runtime output paths must use `${ACTIVE_WORKSPACE}`.
<!-- END GENERATED-SYNC -->


# financial-analyst

## When to Use

- 상장기업의 사업 구조, 핵심 수익원, 최근 이벤트를 빠르게 정리해야 할 때
- 최근 3~5년 재무 흐름과 재무비율을 기반으로 성장성, 수익성, 안정성, 현금창출력, 자본효율성을 평가해야 할 때
- 투자 리포트의 Part II(기업 개요), Part III(재무제표 및 재무비율 분석)를 작성해야 할 때

## Required Inputs

다음 입력값을 먼저 확인한다.

- 기업명
- 티커
- 거래소
- 회계 기준: IFRS / US GAAP / 기타
- 기준 통화

추가로 확인되면 함께 활용한다.

- 분석 기준일
- 최근 연간/분기 보고서 기준일
- 본사 위치
- 비교 가능한 과거 기간 수(3년 또는 5년)

입력값 일부가 없으면 합리적 기본값을 사용할 수 있으나, findings.md 첫머리에 가정값을 명시한다.

## Workflow

<!-- BEGIN YFINANCE_MCP_TOOLS -->
### yfinance 활용 (전체 시장)

`yfinance_get_ticker_info`로 재무 지표를 빠르게 확인하고, `yfinance_get_financials`로 손익/재무상태/현금흐름을 조회한다.

재무 분석 순서:
1. `yfinance_get_ticker_info(symbol=...)` → marketCap, enterpriseValue, revenueGrowth, grossMargins, operatingMargins, returnOnEquity 등
2. `yfinance_get_financials(symbol=..., frequency="annual")` → 연간 재무제표 (3~5년)
3. `yfinance_get_financials(symbol=..., frequency="quarterly")` → 분기 재무제표 (최근 4~8분기)

한국 기업의 경우 korea-stock `get_financial_statement`를 1순위로 사용하고, yfinance는 글로벌 피어 비교나 빠른 확인용으로 보조 사용한다.
<!-- END YFINANCE_MCP_TOOLS -->

<!-- BEGIN KOREA_STOCK_MCP_TOOLS -->
### 2.2 MCP 도구 우선 사용 (한국 상장기업 한정)

korea-stock-mcp MCP 서버가 설치된 환경에서는 한국 상장기업 분석 시 DART/KRX 공식 API를 직접 호출할 수 있다. MCP 도구가 공식 API를 통해 데이터를 제공하므로, 웹 검색보다 MCP 도구를 먼저 사용한다.

사용 가능한 MCP 도구:

| 도구 | 데이터 | 활용 |
|---|---|---|
| `get_corp_code` | DART 고유번호/종목코드 조회 | 기업 식별 |
| `get_stock_base_info` | KRX 종목 기본정보 (상장일, 액면가, 상장주식수) | 기업 개요 |
| `get_financial_statement` | DART XBRL 재무제표 (연간/분기) | 재무 분석 |
| `get_disclosure_list` / `get_disclosure` | DART 공시 원문 | 최근 이벤트 확인 |
| `get_stock_trade_info` | KRX 일별 주가/거래량 | 주가 데이터 |
| `get_today_date` | KST/UTC 현재 날짜 | 기준일 확인 |

사용 순서:
1. 한국 기업이면 `get_corp_code`로 고유번호(`corp_code`)와 종목코드(`stock_code`, 6자리) 획득
2. `get_financial_statement`로 XBRL 재무제표 조회 (`bsns_year`: 연도, `reprt_code`: 11011=사업보고서, `fs_div`: CFO=연결)
3. `get_stock_base_info`로 상장 기본정보 확인
4. `get_disclosure_list` + `get_disclosure`로 공시 원문 확인
5. MCP 도구로 부족한 데이터는 웹 검색으로 보완 (글로벌 피어 비교, 컨센서스 등)

해외 기업은 MCP 도구를 사용할 수 없으며 웹 검색을 통해 데이터를 수집한다.
<!-- END KOREA_STOCK_MCP_TOOLS -->

<!-- BEGIN INPUT_GATE_POLICY_INTEGRATED -->
## 최근 분기 실적·센티먼트 분석 추가 지시

입력 요약의 `분석 초점`이 `최근 분기 실적·센티먼트 심층형` 또는 `혼합형`이면 연간 재무 분석 외에 다음을 반드시 작성한다.

- 최근 4~8개 분기 매출, 영업이익, 영업이익률, EPS, FCF
- YoY, QoQ 변화율
- 실제치 vs 컨센서스 Beat/Miss/In-line
- 가이던스 상향/하향/유지
- 세그먼트·지역·고객군별 성장률 변화
- 재고, 매출채권, 운전자본, 일회성 손익 등 실적 품질
- 특정 이벤트 / 촉매가 있으면 이벤트 전후 분기 변화
- 최근 분기 데이터가 기존 장기 논지를 강화/유지/약화하는지 평가

권장 출력은 `docs/harness/invest/templates/quarterly-sentiment-deep-dive.md`의 분기 실적 관련 섹션을 따른다.
<!-- END INPUT_GATE_POLICY_INTEGRATED --> Steps

1. **분석 범위 고정**
   - 기업명, 티커, 거래소, 회계 기준, 기준 통화를 명시한다.
   - 연간, 최근 분기, TTM 데이터를 구분할 수 있는지 먼저 확인한다.

2. **출처 우선순위에 따라 자료 수집**
   - T0 / 1순위: 회사 공식 IR, 실적 발표 자료, 연차보고서, 분기보고서, SEC EDGAR, DART/KRX, local regulator filings
   - T1 / 2순위: 거래소 공식 데이터, 공식 통계·정책기관
   - T2 / 3순위: yfinance, FMP, Alpha Vantage 같은 금융 데이터 플랫폼
   - T3 / 4순위: Web Search + Fetch로 확인한 보조 기사·문서
   - 수치마다 출처, 기준일, 회계기간, 통화, 필요 시 산식을 남긴다.
   - 재무제표와 reported financial fact는 T0 evidence가 우선한다. vendor snapshot은 빠른 cross-check나 T0 부재 시 provisional value로만 사용한다.
   - yfinance가 repo 문서상 connected여도 live runtime에서 unavailable이면 반복 호출하지 않는다. source-call-plan의 `Runtime Availability`를 따르고, SEC EDGAR/company IR/DART/KRX/local regulator filing 같은 T0 fallback을 먼저 검토한다. 실제 callable FMP/Alpha Vantage는 보조 structured source로 사용하고, Web Search + Fetch는 source discovery와 원문 retrieval 보조로 사용한다.
   - 대형 웹 페이지를 무제한으로 탐색하지 않는다. 필요한 공시/IR/financial statement URL을 우선 고정하고, 나머지는 unresolved data gap으로 남긴다.

3. **Part II: 기업 개요 작성**
   - 회사 기본 정보: 기업명, 티커, 거래소, 본사 위치, 설립연도
   - 주요 사업 부문, 주요 매출원, 주요 지역별 매출 비중을 정리한다.
   - 사업 모델을 제품 판매형 / 구독형 / 플랫폼형 / 제조형 / 금융형 / 광고형 / 기타 중 해당 방식으로 설명한다.
   - 최근 주요 이벤트(실적 발표, M&A, 신제품, 규제 이슈, 경영진 변화, 대규모 투자, 구조조정)를 타임라인으로 정리한다.

4. **Part III-1: 재무제표 수집 및 예비 회계 조정**
   - 손익계산서: 매출, 매출총이익, 영업이익, EBITDA, 순이익, EPS
   - 재무상태표: 현금 및 현금성 자산, 총자산, 총부채, 순부채, 자기자본
   - 현금흐름표: 영업활동현금흐름, 투자활동현금흐름, 재무활동현금흐름, CapEx, FCF
   - 최신 연간보고서, 최근 분기, TTM 데이터를 구분해 표기한다.
   - **다모다란 식 회계 조정 검토 (R&D 자본화 & 운용리스 부채화)**: R&D 지출이 많거나 운용리스(Operating Lease)가 큰 비중을 차지하는 기업의 경우, 재무 비율 분석 전에 아래 예비 조정을 검토하고 기록한다.
     - *R&D 자본화*: R&D 비용을 즉시 비용 처리하지 않고 자산화(상각 기간 3~5년 적용)했을 때 조정 영업이익(Adj. EBIT)과 투하자본(Adj. Invested Capital)이 어떻게 변화하는지 계산한다.
     - *운용리스 부채화*: 향후 운용리스 의무(Operating Lease Commitments)의 현재가치를 계산하여 부채와 자산(사용권 자산)에 가산하고, 이자비용과 감가상각비로 재조정하여 조정 영업이익을 재산출한다.
   - BKNG처럼 매출원가, 매출총이익, 일부 분기 손익 항목을 별도 공시하지 않는 기업은 임의 계산을 단정하지 않는다. 역산 또는 추정이 필요하면 `e` 또는 `추정` 표시와 산식, 공식 미공시 사유를 함께 남긴다.

5. **Part III-2: 수직 분석 수행**
   - 손익계산서는 매출 대비 비율로 분석한다.
   - 재무상태표는 총자산 대비 비율로 분석한다.
   - 현금흐름표는 매출 또는 영업현금흐름 대비 비율로 분석한다.
   - 최근 연도, 전년, 3년 전 비교와 변화 요약을 작성한다.

6. **Part III-3: 추세 분석 수행**
   - 최근 3~5년 기준으로 매출 성장률, 영업이익 성장률, 순이익 성장률, EPS 성장률, FCF 성장률, 부채 증가율, 주주환원 규모를 점검한다.
   - 최근 4~8개 분기 기준으로 매출, 영업이익, EPS, FCF의 YoY와 QoQ를 함께 비교한다.
   - 추세의 방향, 변동성, 일회성 요인 여부를 서술한다.

7. **Part III-4: 재무비율 분석 수행**
   - 수익성: 매출총이익률, 영업이익률, 순이익률, ROE, ROA, ROIC
   - 안정성: 부채비율, 순부채/EBITDA, 유동비율, 이자보상배율, 현금성 자산 대비 단기부채
   - 성장성: 매출 CAGR, 영업이익 CAGR, EPS CAGR, FCF CAGR
   - 활동성: 총자산회전율, 재고자산회전율, 매출채권회전율
   - 현금흐름: FCF 마진, FCF 전환율, 영업현금흐름/순이익, CapEx/매출
   - 직접 계산 시 산식을 쓰고, 외부 수치 사용 시 출처를 병기한다.

8. **Part III-5: 재무 종합 평가 작성**
   - 성장성, 수익성, 현금창출력, 재무 안정성, 자본효율성을 우수 / 보통 / 취약으로 평가한다.
   - 평가는 반드시 수치와 추세를 근거로 작성한다.
   - 종합 평가는 과도한 확신 없이 균형 있게 정리한다.

9. **최종 정리 및 저장**
   - 모든 표와 요약을 `${ACTIVE_WORKSPACE}/01_financial/findings.md`에 저장한다.
   - 각 섹션 끝에 3~5줄 요약을 포함한다.

## Output Structure Contract

### Findings 레벨 (원천 데이터)
- **역할**: 사실(Facts), 표, 수치, 출처 명시에 집중
- **정성적 분석 범위**: 각 파트별 2~3문단 요약으로 제한. "무엇인가(What)"에 집중
- **금지**: 투자 결론, 매매 의견, "So What" 해석, 과도한 확신 표현
- **표 비중**: 데이터 전달의 정확성과 재현성을 위해 표와 수치 중심

### 섹션별 Report 레벨 (정성적 해석)
- **역할**: 본 analyst가 수행
- **출력**: `${ACTIVE_WORKSPACE}/01_financial/report.md`
- **내용**: findings를 바탕으로 한 재무 해석, 투자 함의, 시나리오별 영향
- **핵심 질문**: "이 재무 흐름이 투자적으로 무슨 의미인가(So What)"

### 최종 Report 레벨 (종합 요약)
- **역할**: report-synthesizer가 수행
- **출력**: `${ACTIVE_WORKSPACE}/07_draft/report.md`
- **내용**: 모든 findings + 섹션별 report를 종합한 Executive Summary, Rating, Price Target

> **원칙**: Findings는 "무엇인가"를, 섹션별 Report는 "이 파트에서 왜 중요한가"를, 최종 Report는 "그래서 전체적으로 무엇인가"를 담당한다.

## Output Format

출력 파일: `${ACTIVE_WORKSPACE}/01_financial/findings.md`

### 1. 분석 전제

```markdown
# Financial Analysis Findings

## 분석 전제
| 항목 | 내용 |
|---|---|
| 기업명 |  |
| 티커 |  |
| 거래소 |  |
| 회계 기준 |  |
| 기준 통화 |  |
| 분석 기준일 |  |
| 사용한 가정 |  |
```

### 2. 기업 개요 표

```markdown
## 기업 개요

| 항목 | 내용 | 출처 | 기준일 |
|---|---|---|---|
| 기업명 |  |  |  |
| 티커 |  |  |  |
| 거래소 |  |  |  |
| 본사 위치 |  |  |  |
| 설립연도 |  |  |  |
| 주요 사업 부문 |  |  |  |
| 주요 매출원 |  |  |  |
| 사업 모델 |  |  |  |
```

### 3. 사업 부문별 / 지역별 매출 비중 표

```markdown
## 사업 부문별 매출 비중

| 사업 부문 | 매출 비중 | 설명 | 출처 | 기준 기간 |
|---|---:|---|---|---|

## 지역별 매출 비중

| 지역 | 매출 비중 | 설명 | 출처 | 기준 기간 |
|---|---:|---|---|---|
```

### 4. 최근 주요 이벤트 타임라인

```markdown
## 최근 주요 이벤트

| 날짜 | 이벤트 유형 | 내용 | 잠재 영향 | 출처 |
|---|---|---|---|---|
```

### 5. 재무제표 핵심 수치 표

```markdown
## 재무제표 핵심 수치

### 손익계산서
| 항목 | 최근 연도 | 전년 | 2년 전 | 3년 전 | TTM/최근 분기 | 통화 | 출처 |
|---|---:|---:|---:|---:|---:|---|---|
| 매출 |  |  |  |  |  |  |  |
| 매출총이익 |  |  |  |  |  |  |  |
| 영업이익 |  |  |  |  |  |  |  |
| EBITDA |  |  |  |  |  |  |  |
| 순이익 |  |  |  |  |  |  |  |
| EPS |  |  |  |  |  |  |  |

### 재무상태표
| 항목 | 최근 연도 | 전년 | 2년 전 | 3년 전 | 통화 | 출처 |
|---|---:|---:|---:|---:|---|---|
| 현금 및 현금성 자산 |  |  |  |  |  |  |
| 총자산 |  |  |  |  |  |  |
| 총부채 |  |  |  |  |  |  |
| 순부채 |  |  |  |  |  |  |
| 자기자본 |  |  |  |  |  |  |

### 현금흐름표
| 항목 | 최근 연도 | 전년 | 2년 전 | 3년 전 | 통화 | 출처 |
|---|---:|---:|---:|---:|---|---|
| 영업활동현금흐름 |  |  |  |  |  |  |
| 투자활동현금흐름 |  |  |  |  |  |  |
| 재무활동현금흐름 |  |  |  |  |  |  |
| CapEx |  |  |  |  |  |  |
| FCF |  |  |  |  |  |  |
```

### 5-1. 회계 조정 내역 (R&D 자본화 & 운용리스 부채화)

```markdown
## 회계 조정 내역 (다모다란 프레임워크)

### A. R&D 자본화 조정 (R&D Capitalization)
- R&D 자산화 대상 비용 (최근 3~5년):
- R&D 상각기간 (Amortization Period): 년 (기본 3~10년 중 비즈니스 주기 고려 선택)
- 조정 전 영업이익 (Reported EBIT):
- 조정 후 영업이익 (Adjusted EBIT): 
- R&D 자산 가치 (Amortizable Asset Value):
- 조정 후 투하자본 (Adjusted Invested Capital):

### B. 운용리스 부채화 조정 (Operating Lease Capitalization)
- 향후 리스 의무(Lease Commitments) 현재가치 (PV of Lease Obligations):
- 적용 할인율 (Pre-tax Cost of Debt): %
- 조정 후 영업이익 (Adjusted EBIT = Reported EBIT + Current Lease Expense - Depr. of Leased Asset):
- 조정 후 총부채 (Adjusted Debt):
- 조정 후 자기자본 (Adjusted Equity):

*주의: 미국 US GAAP / IFRS 16 도입 여부 및 실제 공시 데이터를 확인하여 리스 부채가 이미 재무상태표상 '사용권자산 및 리스부채'로 완전히 반영되어 있는 경우, 이중 계상을 피하기 위해 원 공시 수치를 확인하고 '조정 불요(이미 자산/부채화 완료)'로 명시한다.*
```

### 6. 수직 분석 표

```markdown
## 수직 분석

| 항목 | 기준값 | 최근 연도 | 전년 | 3년 전 | 변화 요약 |
|---|---:|---:|---:|---:|---|
```

### 7. 추세 분석 표

```markdown
## 추세 분석

| 항목 | 최근 값 | 3~5년 추세 | 변동성 | 핵심 해석 | 출처 |
|---|---:|---|---|---|---|
| 매출 성장률 |  |  |  |  |  |
| 영업이익 성장률 |  |  |  |  |  |
| 순이익 성장률 |  |  |  |  |  |
| EPS 성장률 |  |  |  |  |  |
| FCF 성장률 |  |  |  |  |  |
| 부채 증가율 |  |  |  |  |  |
| 주주환원 규모 |  |  |  |  |  |
```

### 8. 최근 분기 재무 비교 표

```markdown
## 최근 분기 재무 비교

| 분기 | 매출 | 매출 YoY | 매출 QoQ | 영업이익 | 영업이익 YoY | 영업이익 QoQ | EPS | EPS YoY | EPS QoQ | FCF | FCF YoY | FCF QoQ | 출처 / 기준일 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
```

### 9. 재무비율 분석 표

```markdown
## 재무비율 분석

### 수익성
| 지표 | 최근 값 | 비교 기간 | 해석 | 출처 |
|---|---:|---|---|---|

### 안정성
| 지표 | 최근 값 | 비교 기간 | 해석 | 출처 |
|---|---:|---|---|---|

### 성장성
| 지표 | 최근 값 | 비교 기간 | 해석 | 출처 |
|---|---:|---|---|---|

### 활동성
| 지표 | 최근 값 | 비교 기간 | 해석 | 출처 |
|---|---:|---|---|---|

### 현금흐름
| 지표 | 최근 값 | 비교 기간 | 해석 | 출처 |
|---|---:|---|---|---|
```

### 10. 재무 종합 평가 표

```markdown
## 재무 종합 평가

| 항목 | 평가 | 근거 |
|---|---|---|
| 성장성 | 우수 / 보통 / 취약 |  |
| 수익성 | 우수 / 보통 / 취약 |  |
| 현금창출력 | 우수 / 보통 / 취약 |  |
| 재무 안정성 | 우수 / 보통 / 취약 |  |
| 자본효율성 | 우수 / 보통 / 취약 |  |
| 종합 평가 |  |  |
```

### 11. 섹션 요약 및 한계

```markdown
## 요약
-
-
-

## 데이터 한계 및 추가 확인 필요 사항
- 공식 자료 미확인:
- 데이터 부족:
- 추가 확인 필요:
```

### 12. 📊 대시보드 데이터 블록

findings.md 맨 끝에 아래 YAML 코드블록을 **반드시** 추가한다. `html-report-synthesizer`가 이 블록을 파싱하여 Chart.js 차트와 지표 그리드에 데이터를 주입한다. 값이 확인되지 않은 항목은 `null`로 두고, 임의 추정값을 넣지 않는다.

````markdown
```yaml
# === 대시보드 데이터 블록 ===
dashboard_data:
  currency: ""           # 기준 통화 (예: USD, KRW)
  fiscal_years: ["FY2022", "FY2023", "FY2024"]  # 최근 3개년 라벨
  revenue:       [null, null, null]   # 매출액 (단위: 백만)
  net_income:    [null, null, null]   # 순이익
  fcf:           [null, null, null]   # 잉여현금흐름
  roe:           [null, null, null]   # ROE (%)
  roic:          [null, null, null]   # ROIC (%)
  metrics_grid:
    revenue_growth:   null   # 최근 매출 성장률 (%)
    operating_margin: null   # 영업이익률 (%)
    net_margin:       null   # 순이익률 (%)
    debt_to_equity:   null   # 부채비율 (%)
    fcf_margin:       null   # FCF 마진 (%)
    net_debt:         null   # 순부채 (백만)
```
````

## Validation Notes

- 확인되지 않은 데이터는 추정하지 않는다.
- 데이터가 없거나 공식 자료에서 직접 확인되지 않으면 다음 표현만 사용한다.
  - `공식 자료 미확인`
  - `데이터 부족`
  - `추가 확인 필요`
- 출처 간 수치가 충돌하면 하나를 임의 선택하지 말고 차이를 표 또는 주석으로 설명한다.
- 최신 연간, 최근 분기, TTM은 반드시 구분한다.
- 통화가 다르면 환율 기준일과 변환 기준을 적는다.
- 회계 기준 차이로 비교 왜곡 가능성이 있으면 주석으로 명시한다.
- 각 핵심 표에는 가능하면 `출처`, `기준일` 또는 `기준 기간` 열을 둔다.
- 각 섹션 마지막에는 3~5줄 요약을 추가한다.
- 문체는 한국어 투자 리포트 스타일로 유지하며, `반드시 상승`, `확실한 매수` 같은 과도한 확신 표현은 사용하지 않는다.
- **`📊 대시보드 데이터 블록`이 findings.md 끝에 반드시 포함되어야 한다.** 이 블록이 없으면 html-report-synthesizer가 차트를 렌더링할 수 없다.
