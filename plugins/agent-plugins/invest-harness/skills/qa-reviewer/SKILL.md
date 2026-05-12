---
name: qa-reviewer
description: 투자 리포트 초안과 원천 findings를 대조해 출처, 수치, 구조, 논리, 문체 결함을 ${ACTIVE_WORKSPACE}/09_qa/review.md에 보고하는 QA 스킬
---

<!-- GENERATED-SYNC: source=plugins/vertical-plugins/invest-research/skills/qa-reviewer/SKILL.md; kind=skill; script=scripts/Sync-InvestSkills.ps1 -->
> [!IMPORTANT]
> Generated execution artifact. Do not edit directly; edit the vertical source and rerun pwsh ./scripts/Sync-InvestSkills.ps1.
> Common policies are synced from plugins/vertical-plugins/invest-research/policies/.
> Runtime output paths must use `${ACTIVE_WORKSPACE}`.
<!-- END GENERATED-SYNC -->


# qa-reviewer

## When to Use

- `${ACTIVE_WORKSPACE}/07_draft/report.md` 초안이 최종본으로 확정 가능한지 검토할 때 사용한다.
- 출처 누락, 기준일 누락, 수치 충돌, 섹션 누락, 결론-근거 불일치를 찾아야 할 때 사용한다.
- 투자 자문처럼 보이는 표현이나 과도한 확신 표현을 제거해야 할 때 사용한다.

## Required Inputs

- `${ACTIVE_WORKSPACE}/00_input/request-summary.md`
- `${ACTIVE_WORKSPACE}/01_financial/findings.md`
- `${ACTIVE_WORKSPACE}/02_fundamental/findings.md`
- `${ACTIVE_WORKSPACE}/03_valuation/findings.md`
- `${ACTIVE_WORKSPACE}/04_technical/findings.md`
- `${ACTIVE_WORKSPACE}/05_macro_sentiment/findings.md`
- `${ACTIVE_WORKSPACE}/06_risk_scenario/findings.md`
- `${ACTIVE_WORKSPACE}/07_draft/report.md`
- 선택 입력: `${ACTIVE_WORKSPACE}/06_risk_scenario/conflicts.md`
- 기준 문서: `invest_prompt_v2.md`

## Review Scope

| 검토 영역 | 핵심 질문 |
|---|---|
| 구조 | 최종 출력 18개 섹션이 모두 존재하는가? |
| 출처 | 핵심 수치와 사실에 출처, 기준일, 회계기간, 통화가 붙어 있는가? |
| 수치 | findings와 초안의 수치가 일치하는가? 충돌이 설명되었는가? |
| 논리 | 투자 의견, 점수, 시나리오, 리스크가 서로 모순되지 않는가? |
| 불확실성 | 데이터 부족과 공식 자료 미확인 항목이 명시되었는가? |
| 문체 | 한국어 투자 리포트 문체이며 과도한 확신 표현이 없는가? |
| 자문 경계 | 개인화된 투자 자문처럼 보이는 표현이 없는가? |

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

<!-- END KOREA_STOCK_MCP_TOOLS -->

<!-- BEGIN INPUT_GATE_POLICY_INTEGRATED -->
## 최근 분기 실적·센티먼트 QA 항목

입력 요약의 `분석 초점`이 `최근 분기 실적·센티먼트 심층형` 또는 `혼합형`이면 다음을 추가 검수한다.

- 최근 분기 표에 YoY, QoQ, 컨센서스 대비가 빠지지 않았는가?
- 실적 발표일, 기준일, 출처가 명시되어 있는가?
- 어닝콜 톤 판단에 근거가 있는가?
- 애널리스트 리비전과 뉴스 센티먼트가 루머와 구분되어 있는가?
- 최근 분기 데이터와 연간 장기 논지가 충돌할 때 이를 명시했는가?
- 주가 반응을 실적 자체와 센티먼트 변화로 구분했는가?
- 특정 이벤트 / 촉매를 독립 모드처럼 처리하지 않고 하위 분석 축으로 처리했는가?
<!-- END INPUT_GATE_POLICY_INTEGRATED --> Steps

1. **필수 파일 확인**
   - 모든 입력 파일의 존재 여부를 확인한다.
   - 누락 파일이 있으면 QA 판정을 `재검토 필요`로 둔다.

2. **구조 검토**
   - 초안의 18개 최종 섹션이 순서대로 존재하는지 확인한다.
   - 빈 섹션이나 템플릿 잔여 문구를 찾는다.

3. **출처와 기준일 검토**
   - 핵심 재무 수치, 시장지표, 매크로 지표, 뉴스 이벤트에 출처와 기준일이 있는지 확인한다.
   - 통화와 회계기간 혼용이 설명되어 있는지 확인한다.

4. **수치와 주장 대조**
   - 초안의 핵심 수치를 원천 findings와 대조한다.
   - 수치가 다르면 충돌로 기록하고 수정 요청을 작성한다.

5. **결론 정합성 검토**
   - 종합 점수, 최종 의견, 투자 기간별 전략, 리스크, 시나리오가 같은 방향으로 설명되는지 확인한다.
   - 기술적 분석과 소셜 센티먼트가 보조 신호로만 쓰였는지 확인한다.

6. **문체 및 경계 검토**
   - `반드시 상승`, `확실한 매수`, `무조건 매도` 같은 표현을 결함으로 기록한다.
   - 정보 제공용 분석이라는 한계 문구가 있는지 확인한다.

7. **판정 작성**
   - 결함을 심각도별로 정리하고 최종 판정을 내린다.
   - 결과를 `${ACTIVE_WORKSPACE}/09_qa/review.md`에 저장한다.

## Output Format

```markdown
# 투자 리포트 QA Review

## 1. QA 판정
| 항목 | 내용 |
|---|---|
| 판정 | 승인 / 수정 후 승인 / 재검토 필요 |
| 검토 기준일 |  |
| 검토 대상 초안 | `${ACTIVE_WORKSPACE}/07_draft/report.md` |
| 치명적 결함 수 |  |
| 주요 수정 필요 항목 |  |

## 2. 결함 목록
| 심각도 | 위치 | 문제 | 근거 | 수정 요청 |
|---|---|---|---|---|
| 치명 / 중요 / 경미 |  |  |  |  |

## 3. 구조 체크리스트
| 섹션 | 존재 여부 | 비고 |
|---|---|---|
| 1. Executive Summary |  |  |
| 2. 기업 개요 |  |  |
| 3. 핵심 투자 포인트 |  |  |
| 4. 재무 분석 |  |  |
| 5. 산업 및 경쟁 환경 |  |  |
| 6. 경영진 및 거버넌스 |  |  |
| 7. 경제적 해자 |  |  |
| 8. 제품 및 서비스 |  |  |
| 9. 밸류에이션 |  |  |
| 10. 기술적 분석 |  |  |
| 11. 뉴스 및 센티먼트 |  |  |
| 12. 거시경제 및 정책 환경 |  |  |
| 13. 리스크 분석 |  |  |
| 14. 시나리오 분석 |  |  |
| 15. 종합 점수 및 최종 의견 |  |  |
| 16. 투자 기간별 전략 |  |  |
| 17. 모니터링 체크리스트 |  |  |
| 18. 한계 및 추가 확인 필요 사항 |  |  |

## 4. 출처 및 수치 검토
| 항목 | 상태 | 비고 |
|---|---|---|
| 핵심 재무 수치 출처 |  |  |
| 밸류에이션 수치 출처 |  |  |
| 뉴스 기준일 |  |  |
| 거시 지표 기준일 |  |  |
| 통화 / 회계기간 표기 |  |  |
| 충돌 수치 처리 |  |  |

## 5. 결론 정합성 검토
- 점수와 최종 의견:
- 시나리오와 전략:
- 리스크와 모니터링:
- 보조 신호 사용 경계:

## 6. 최종 권고
- 승인 가능 여부:
- 최종본 확정 전 필수 수정:
- 남은 한계:
```

## Validation Notes

- QA는 새로운 분석을 추가하지 않고 결함과 수정 방향만 제시한다.
- 치명적 결함이 있으면 `승인` 판정을 내리지 않는다.
- 수치 충돌은 원천 findings와 초안의 위치를 함께 적는다.
- 경미한 문체 수정과 치명적 근거 누락을 구분한다.
