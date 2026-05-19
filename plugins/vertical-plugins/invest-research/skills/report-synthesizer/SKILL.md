---
name: report-synthesizer
description: 전문가 findings를 invest_prompt_v2.md의 최종 출력 구조에 맞춰 ${ACTIVE_WORKSPACE}/07_draft/report.md 초안으로 조립하는 합성 스킬
---

# report-synthesizer

## When to Use

- `${ACTIVE_WORKSPACE}/01_financial/findings.md`부터 `${ACTIVE_WORKSPACE}/06_risk_scenario/findings.md`까지의 전문가 산출물을 하나의 투자 리포트 초안으로 통합할 때 사용한다.
- Executive Summary, Rating, Price Target, 투자 의견, Risk-Reward, 모니터링 체크리스트를 선행 분석과 일관되게 작성해야 할 때 사용한다.
- 출처 없는 신규 수치나 새로운 주장을 만들지 않고 기존 findings를 재구성해야 할 때 사용한다.

## Required Inputs

- `${ACTIVE_WORKSPACE}/00_input/request-summary.md`
- `${ACTIVE_WORKSPACE}/00_input/market-price-snapshot.md`
- `${ACTIVE_WORKSPACE}/01_financial/findings.md`
- `${ACTIVE_WORKSPACE}/01_financial/report.md` (섹션별 정성 해석)
- `${ACTIVE_WORKSPACE}/02_fundamental/findings.md`
- `${ACTIVE_WORKSPACE}/02_fundamental/report.md` (섹션별 정성 해석)
- `${ACTIVE_WORKSPACE}/03_valuation/findings.md`
- `${ACTIVE_WORKSPACE}/03_valuation/report.md` (섹션별 정성 해석)
- `${ACTIVE_WORKSPACE}/04_technical/findings.md`
- `${ACTIVE_WORKSPACE}/04_technical/report.md` (섹션별 정성 해석)
- `${ACTIVE_WORKSPACE}/05_macro_sentiment/findings.md`
- `${ACTIVE_WORKSPACE}/05_macro_sentiment/report.md` (섹션별 정성 해석)
- `${ACTIVE_WORKSPACE}/06_risk_scenario/findings.md`
- `${ACTIVE_WORKSPACE}/06_risk_scenario/report.md` (섹션별 정성 해석)
- 선택 입력: `${ACTIVE_WORKSPACE}/06_risk_scenario/conflicts.md`
- 기준 문서: `invest_prompt_v2.md`
- 기준 정책: `plugins/vertical-plugins/invest-research/policies/report-writing-style-policy.md`

## Workflow

<!-- BEGIN YFINANCE_MCP_TOOLS -->
## 사용 가능한 MCP 도구 (글로벌: yfinance-mcp)

`yfinance` MCP 서버는 **전 세계 상장기업**의 금융 데이터를 API 키 없이 제공한다. 모든 시장(미국, 한국, 유럽, 일본 등)의 종목을 커버하며, 한국 기업 분석 시에도 korea-stock-mcp와 함께 보조로 사용한다.

사용 규칙:
- **무조건 1순위**: 웹 검색보다 yfinance MCP 도구를 먼저 호출한다 (키 불필요, 속도 빠름)
- 기업 식별은 `yfinance_search`로 종목코드/회사명 검색 후 획득한 `symbol`을 다른 도구에 전달
- 한국 기업은 `korea-stock` MCP 서버를 1순위로 사용하고, yfinance는 보충 데이터용으로 사용
- yfinance 데이터는 비공식 출처이므로 정확한 재무 수치는 공시(DART/EDGAR)와 교차 검증 필요

| 도구 | 설명 | 1순위 사용처 |
|---|---|---|
| `yfinance_get_ticker_info` | 종목 기본정보, 재무 지표, 밸류에이션, 배당, 거래 데이터 | 기업 개요, 밸류에이션 |
| `yfinance_get_financials` | 손익계산서, 재무상태표, 현금흐름표 (연간/분기) | 재무 분석 |
| `yfinance_get_price_history` | OHLCV 과거 데이터 + 기술적 차트 생성(WebP) | 기술적 분석 |
| `yfinance_get_ticker_news` | 최근 뉴스 기사 | 뉴스/센티먼트 |
| `yfinance_get_holders` | 주요 주주, 기관, 뮤추얼펀드, 내부자 거래 | 경영진/거버넌스 |
| `yfinance_get_option_chain` | 옵션 체인 (콜/풋, 행사가, 내재변동성) | 기술적 분석, 리스크 |
| `yfinance_get_option_dates` | 옵션 만기일 | 기술적 분석 |
| `yfinance_search` | Yahoo Finance 검색 (종목, ETF, 뉴스) | 기업 식별 |
| `yfinance_get_top` | 섹터별 상위 종목/ETF/성장/실적 | 산업/경쟁 환경 |

사용 흐름:
1. 기업 식별이 필요한 경우 `yfinance_search(query="Apple")` 또는 `yfinance_search(query="AAPL", search_type="quote")`
2. 식별된 `symbol`로 나머지 도구 호출 (예: symbol="AAPL", symbol="005930.KS")
3. 자세한 재무/정보는 `yfinance_get_ticker_info` → `yfinance_get_financials`
4. 주가 데이터는 `yfinance_get_price_history` (차트 포함 가능)
5. 뉴스는 `yfinance_get_ticker_news`

<!-- END YFINANCE_MCP_TOOLS -->

<!-- BEGIN KOREA_STOCK_MCP_TOOLS -->
## 사용 가능한 MCP 도구 (korea-stock-mcp)

이 스킬은 아래 MCP 서버 도구를 직접 호출할 수 있다. MCP 도구가 공식 API를 통해 데이터를 제공하므로, 웹 검색보다 우선 사용한다.

| MCP 서버 | 도구 | 설명 | 1순위 사용처 |
|---|---|---|---|
| `korea-stock` | `get_corp_code` | DART 고유번호, 회사명, 종목코드 조회 (한글/영문 부분 검색, 비상장사 포함) | 모든 분석 전 기업 식별 |
| `korea-stock` | `get_disclosure_list` | 공시 유형별/회사별/날짜별 검색 | 최근 공시, 이벤트, M&A, 규제 확인 |
| `korea-stock` | `get_disclosure` | 공시보고서 원문 파싱 (1MB 초과 시 section 단위 조회) | 사업보고서, 분기보고서 원문 확인 |
| `korea-stock` | `get_financial_statement` | XBRL 재무제표 (연간/분기, IFRS/GAAP) | 재무 분석 Part III |
| `korea-stock` | `get_stock_base_info` | KRX 종목 기본정보 (종목명, 상장일, 액면가, 상장주식수) | 기업 개요 Part II |
| `korea-stock` | `get_stock_trade_info` | KRX 일별 매매정보 (종가, 등락률, 시고저, 거래량, 시총) | 기술적 분석, 주가 데이터 |
| `korea-stock` | `get_market_type` | 상장시장 정보 (Y=유가, K=코스닥, N=코넥스) | 기업 식별 확인 |
| `korea-stock` | `get_today_date` | 오늘 날짜 KST/UTC YYYYMMDD | 분석 기준일 확인 |

사용 규칙:

1. **1순위**: MCP 도구로 조회 가능한 데이터는 웹 검색보다 MCP 도구를 먼저 호출한다.
2. **식별 순서**: 한국 기업 분석 시 `get_corp_code`로 고유번호를 먼저 조회한 후, 획득한 `corp_code`를 다른 DART 도구에 전달한다.
3. **종목코드**: KRX 도구(`get_stock_base_info`, `get_stock_trade_info`)는 6자리 종목코드가 필요하다. `get_corp_code`의 `stock_code` 필드로 확인 가능하다.
4. **공시 원문**: `get_disclosure`는 문서가 클 경우 목차를 반환한다. 목차가 반환되면 필요한 section_id로 세부 조회한다.
5. **날짜 형식**: KRX 도구의 `basDd`와 DART 도구의 `bgn_de`/`end_de`는 `YYYYMMDD` 형식이다.

한국 기업이 아닌 경우 이 MCP 도구를 사용할 수 없으며, 웹 검색(`web_search`/`web_fetch`/`browser`)으로 데이터를 수집한다.

<!-- END KOREA_STOCK_MCP_TOOLS --> Steps

<!-- BEGIN INPUT_GATE_POLICY_INTEGRATED -->
## 최근 분기 실적·센티먼트 합성 규칙

입력 요약의 `분석 초점`이 `최근 분기 실적·센티먼트 심층형` 또는 `혼합형`이면 최종 보고서에 다음 내용을 반드시 포함한다.

- `재무 분석` 섹션: 최근 4~8개 분기 실적 표, YoY 및 QoQ 비교
- `밸류에이션` 섹션: peer financial comparison의 YoY 및 QoQ 비교
- `뉴스 및 센티먼트` 섹션: 최근 30/90일 센티먼트와 어닝콜 톤
- `밸류에이션` 섹션: 최근 분기 이후 컨센서스 리비전 반영
- `시나리오 분석` 섹션: 다음 1~2개 분기 확인 지표
- `Rating, Price Target 및 투자 의견` 섹션: 최근 분기 데이터가 장기 투자 논지와 Rating/Price Target을 강화/유지/약화하는지 명시
- 특정 이벤트 / 촉매가 있으면 이벤트 전후 영향과 이미 주가에 반영된 정도를 별도 표시한다.
<!-- END INPUT_GATE_POLICY_INTEGRATED -->

1. **입력 완전성 확인**
   - 필수 findings 존재 여부를 확인한다.
   - 누락 파일이나 빈 섹션은 초안의 한계 및 추가 확인 필요 사항에 반영한다.
   - 6개 findings가 모두 크면 각 findings의 compact handoff summary와 conflicts table을 먼저 읽고, 원문 전체는 수치 검산과 출처 확인이 필요한 구간에만 참조한다.
   - source-call-plan에서 live runtime unavailable로 표시된 source를 새로 호출해 보강하지 않는다. 해당 제한은 마지막 한계 섹션에 반영한다.

2. **섹션 매핑**
   - `invest_prompt_v2.md`의 최종 출력 템플릿 18개 섹션에 각 findings의 내용을 배치한다.
   - 동일 항목이 여러 findings에 있으면 출처와 기준일이 더 명확한 내용을 우선한다.
   - reported financial fact, guidance, share count, issuer identity, segment data는 Company IR, SEC EDGAR, DART/KRX, local regulator filings 같은 T0 evidence를 우선한다. vendor snapshot이나 web context가 더 최신이어도 T0 부재/시차를 명시하지 않고 덮어쓰지 않는다.
   - 최근 분기 실적 또는 peer financial comparison을 넣을 때는 가능한 항목마다 YoY와 QoQ를 함께 표시한다.

3. **Executive Summary 작성**
   - 핵심 투자 논지 3~5개, 핵심 리스크 3~5개, 재무 상태, 밸류에이션 판단, 기술적 흐름, 최종 의견을 1페이지 수준으로 요약한다.
   - 세부 본문과 모순되는 결론을 쓰지 않는다.
   - 모든 문장은 한국어 `합니다/습니다`체로 작성하고, 영어 약어는 필요한 경우에만 유지하되 의미를 한국어로 풀어쓴다.
   - 비개발자 재무·회계 실무자도 바로 이해할 수 있도록 전문 용어, 산식, 판단 기준을 생략하지 않는다.
   - `혁신적인`, `획기적인`, `놀라운`, `완벽한`, `최고 수준` 같은 과장된 수식어와 `~요`, `~죠` 같은 구어체 어미를 사용하지 않는다.

4. **Rating / Price Target 작성**
   - Rating은 `Buy / Outperform / Neutral / Hold / Underperform / Sell` 중 하나를 사용한다.
   - Price Target 또는 가치 범위는 `${ACTIVE_WORKSPACE}/00_input/market-price-snapshot.md`의 기준 주가와 `03_valuation`의 산출 근거를 사용한다.
   - Implied Upside / Downside는 `Price Target / 기준 주가 - 1`로 계산하고 산식을 남긴다.
   - 근거가 부족하면 Rating 신뢰도를 낮게 표시하고 이유를 적는다.

5. **최종 의견과 전략 작성**
   - 최종 의견은 정보 제공용 일반 분석으로 표현한다.
   - 단기, 중기, 장기 전략과 Risk-Reward는 시나리오, 리스크, 기술적 분석, 밸류에이션과 연결한다.
   - 가격 전략이 포함될 경우 개인화된 매매 권유처럼 쓰지 않는다.

6. **Self-Check: 원천 findings 수치 교착**
   - 초안 작성 후, 핵심 테이블(경쟁사 비교, 재무제표, 재묵비율, 밸류에이션 지표)의 수치가 원천 findings와 일치하는지 확인한다.
   - 특히 경쟁사 비교 테이블은 `03_valuation`의 멀티플을 우선 따른다. `02_fundamental`의 추정치를 valuation findings의 검증된 값대신 사용하지 않도록 주의한다.
   - 영업이익률과 순이익률을 혼동하지 않도록 확인한다.
   - Adjusted vs GAAP 수치가 교차되지 않도록 구분한다.
   - 최근 분기 표와 peer financial comparison에서 YoY와 QoQ 중 하나만 있으면 누락 사유를 한계 섹션에 남긴다.
   - Rating, Price Target, implied upside/downside가 기준 주가와 밸류에이션 findings에 맞는지 확인한다.
   - 불일치가 발견되면 원천 findings의 값을 적용한다.

7. **한계 정리**
   - 데이터 부족, 출처 충돌, 오래된 기준일, 공식 자료 미확인 항목을 마지막 섹션에 모은다.
   - 충돌 파일이 있으면 핵심 충돌과 처리 방안을 반영한다.

8. **파일 저장**
   - 초안을 `${ACTIVE_WORKSPACE}/07_draft/report.md`에 저장한다.
   - 보고서 최상단에는 작성일, 작성자, 분석 기준일, 기준 통화, 회계 기준을 표로 명시한다. 값이 확인되지 않으면 `미확인`으로 적고 한계 섹션에 이유를 남긴다.
   - 마크다운 글머리 기호는 단일 하이픈(`-`)만 사용하고, 헤더 뒤에는 빈 행 없이 바로 본문, 표, 목록, 콜아웃, 코드블록 중 하나를 배치한다.
   - Harness 표준 경로를 유지하며 임의의 `results/` 폴더나 날짜 기반 파일명을 새로 만들지 않는다.

9. **📊 대시보드 데이터 블록 / 🔍 검증 로그 블록 보존**
   - 각 findings.md의 `dashboard_data` YAML 코드블록과 `verification_log` YAML 코드블록을 report.md 맨 끝 `## 대시보드 데이터 집합` 섹션에 원본 그대로 복사한다.
   - 각 블록은 출처 파일명을 주석으로 남겨 `html-report-synthesizer`가 파싱할 때 구분할 수 있게 한다.
   - 형식: `# source: 01_financial/findings.md` 주석 후 해당 YAML 블록 복사.
   - 블록이 없는 findings는 `# source: XX_xxx/findings.md - 데이터 블록 없음` 주석만 남긴다.
   - **절대로 블록의 내용을 수정하거나 재해석하지 않는다.** 원본 그대로 복사만 한다.

## Output Structure Contract

### 3단계 리포트 구조
1. **Findings (01~06)**: 각 analyst가 작성 — 표/수치 중심 원천 데이터 ("무엇인가")
2. **섹션별 Report (01~06/report.md)**: 각 analyst가 작성 — 해당 파트의 정성적 해석과 투자 함의 ("이 파트에서 왜 중요한가")
3. **최종 Report (07_draft/report.md)**: report-synthesizer가 작성 — findings + 섹션별 report 종합 요약 ("그래서 전체적으로 무엇인가")

### Findings + 섹션별 Report → 최종 Report 종합 규칙
- findings의 표/수치를 단순 복사하지 말 것 — 이미 섹션별 report에서 해석되었음
- 각 섹션별 report.md의 핵심 해석과 투자 함의를 요약하여 최종 report에 반영할 것
- 최종 report의 각 섹션은 해당 파트의 "So What"을 2~3문단으로 압축 제시할 것
- Executive Summary, 핵심 투자 포인트, Risk-Reward, 시나리오 투자 함의는 모든 섹션별 report를 교차 검토하여 종합할 것
- findings에 없던 투자 결론이나 매매 의견을 새로 도출하지 말 것 (findings + 섹션별 report 기반 해석만 종합)
- "~입니다", "~합니다" 체를 사용하고, 과장된 수식어와 구어체를 피할 것

> **원칙**: Findings는 "무엇인가"를, 섹션별 Report는 "이 파트에서 왜 중요한가"를, 최종 Report는 "그래서 전체적으로 무엇인가"를 담당한다.

## Output Format

초안은 아래 섹션 순서를 그대로 따른다.

```markdown
# 투자 리서치 리포트 초안
| 항목 | 내용 |
|---|---|
| 작성일 | YYYY-MM-DD |
| 작성자 | invest-harness report-synthesizer |
| 분석 기준일 | YYYY-MM-DD |
| 기준 통화 |  |
| 회계 기준 |  |

## 1. Executive Summary

## 2. 기업 개요

## 3. 핵심 투자 포인트

## 4. 재무 분석

## 5. 산업 및 경쟁 환경

## 6. 경영진 및 거버넌스

## 7. 경제적 해자

## 8. 제품 및 서비스

## 9. 밸류에이션

## 10. 기술적 분석

## 11. 뉴스 및 센티먼트

## 12. 거시경제 및 정책 환경

## 13. 리스크 분석

## 14. 시나리오 분석

## 15. Rating, Price Target 및 투자 의견

## 16. 투자 기간별 전략과 Risk-Reward

## 17. 모니터링 체크리스트

## 18. 한계 및 추가 확인 필요 사항

## 19. 대시보드 데이터 집합
<!-- 각 findings의 dashboard_data / verification_log YAML 블록을 원본 그대로 복사 -->
```

## Validation Notes

- 신규 수치나 출처 없는 판단을 추가하지 않는다.
- Executive Summary와 최종 의견은 본문 근거와 일치해야 한다.
- 각 핵심 수치에는 출처, 기준일, 회계기간, 통화가 유지되어야 한다.
- Rating, Price Target, Implied Upside / Downside는 market-price snapshot과 valuation findings로 재계산 가능해야 한다.
- 모든 섹션에는 최소한 요약 또는 데이터 부족 사유가 있어야 한다.
- 과도한 확신 표현과 개인화된 투자 자문 표현을 제거한다.
- 모든 응답과 산출물은 한국어로 작성하고 `report-writing-style-policy.md`의 문체, 마크다운, 파일 경로 규칙을 따른다.
- 투자 리포트에는 블로그용 인사말인 `안녕하세요, PROCPA입니다.`나 다음 글 예고를 넣지 않는다.
- **`## 19. 대시보드 데이터 집합` 섹션이 report.md 맨 끝에 반드시 포함되어야 한다.** 이 섹션이 없으면 html-report-synthesizer가 차트/카드를 렌더링할 수 없다.
