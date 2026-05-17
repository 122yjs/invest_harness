---
name: html-report-synthesizer
description: Markdown 최종 리포트와 QA 결과를 HTML 리포트 계약으로 변환해 ${ACTIVE_WORKSPACE}/08_final/report.html에 저장하는 스킬
---

# html-report-synthesizer

## When to Use

- `/report-html` command가 최종 report 또는 workspace를 전달했을 때 사용한다.
- Markdown 리포트를 브라우저에서 읽기 좋은 HTML 산출물로 변환해야 할 때 사용한다.

## Required Inputs

- `${ACTIVE_WORKSPACE}/08_final/report.md` 또는 `${ACTIVE_WORKSPACE}/07_draft/report.md`
- `${ACTIVE_WORKSPACE}/00_input/market-price-snapshot.md`
- 선택 입력: `${ACTIVE_WORKSPACE}/09_qa/final-check.md`
- `${ACTIVE_WORKSPACE}`

## Output File

- `${ACTIVE_WORKSPACE}/08_final/report.html`

## Workflow

1. **입력 데이터 수집**: 
   - `${ACTIVE_WORKSPACE}/01_financial/findings.md`부터 `06_risk_scenario/findings.md`까지의 모든 중간 findings 파일과 `07_draft/report.md`, `08_final/report.md` 최종 보고서 전문을 순회하며 읽어 들인다.
   - `${ACTIVE_WORKSPACE}/00_input/market-price-snapshot.md` 및 `09_qa/review.md` 정보를 수집한다.

2. **100% 한글화 원칙 준수**:
   - 최종 대시보드 UI의 단추, 탭 이름, 차트 라벨(매출액, 순이익, FCF, ROE, ROIC, 상승여력 등), 리스크 등급, 그리고 내러티브 및 검증 로그 등 **모든 화면 텍스트는 예외 없이 100% 한국어**로 작성되어야 한다.

3. **CORS 우회 인라인 마크다운 바인더**:
   - 로컬 브라우저 구동 시 발생할 수 있는 CORS(동일출처 정책) 보안 오류 및 파일 로딩 지연을 방지하기 위해, 수집된 모든 개별 마크다운(.md) 문서의 전문을 JSON 객체 형태(`const mdData = { ... };`)로 HTML 템플릿의 지정된 플레이스홀더(`\${MD_DATA_JSON}`)에 문자열로 인라인 인코딩하여 주입한다.
   - 브라우저 단에서 `marked.js` 파서를 활용하여 사이드바의 각 분석 파트 탭(01~08)을 클릭할 때 해당 마크다운 전문을 동적으로 렌더링하고, 대시보드 하단에 `📑 원본 마크다운(MD) 보고서 전문 보기` 토글 단추를 제공하여 원본 문서를 간편하게 열람·숨김 처리할 수 있도록 구현한다.

4. **다차원 정량 시각화 설계 (01, 03, 04 파트)**:
   - **재무 분석 (01)**: 
     - 매출액, 순이익, FCF의 최근 3개년 추이를 **Chart.js 단일 차트 내에서 다중 혼합형(매출액은 Bar, 순이익/FCF는 Line)**으로 구성한다.
     - 자본 효율성을 파악하기 위해 **ROE vs ROIC 동시 비교 선형 차트**를 결합 탑재한다.
     - 매출액 성장률, 영업이익률(OPM), Net Debt 등 6대 재무지표 그리드 테이블을 한글 매핑하여 시각화한다.
   - **밸류에이션 (03)**:
     - 목표가 궤적을 직관적으로 이해할 수 있는 **상자가로형 '풋볼 필드' 차트**(하락, 기본, 상승 시나리오 범위 및 현재 시장 가격)를 CSS로 시각화한다.
     - 영구성장률(PGR) vs 가중평균자본비용(WACC)의 변화에 따른 내재가치 변동을 파악할 수 있는 **WACC 민감도 5x5 매트릭스 테이블**을 동적 컴포넌트로 구성한다.
     - 글로벌 피어 4~5개사의 밸류에이션 멀티플(P/E, EV/EBITDA, P/S 등)을 종합 비교하는 피어 테이블을 수록한다.
   - **기술적 분석 (04)**:
     - **RSI 중립/과매수/과매도 게이지 바** 및 **MACD 골든/데드크로스 경고 위젯**, SMA 이격 상태, 그리고 **3단계 핵심 지지/저항 가격 밴드**를 수록하여 입체적인 정량 분석을 수행한다.

5. **심층 내러티브 및 검증 로그 시각화 (02, 05, 06 파트)**:
     - 단순 요약이나 표 나열을 지양하고, **정교한 분석적 문장형 서사(Narrative)**로 주요 테마를 기술한다.
     - 각 정성 탭에는 해당 주장의 정밀한 뒷받침 근거를 담은 **'검증 로그(Verification Evidence Log)'** 섹션을 구체적인 출처 및 판정 결과와 함께 CSS 카드 스타일로 가시성 높게 포함한다. (예: SWOT 세부설명, M&A/규제 타격 영향 검증, 환율 민감도 등)

6. **인터랙티브 시나리오 시뮬레이터 구성**:
   - 상단 헤더에 `하락(Bear)`, `기본(Base)`, `상승(Bull)` 시나리오 조절 버튼을 배치한다.
   - 이 버튼과 상호작용하여 화면 내의 투자 의견, 목표 주가, 상승 여력(Upside/Downside) 수치가 동적으로 변경되며, 재무 추이 복합 차트의 FCF 추세 및 밸류에이션 풋볼 필드, 민감도 표가 연동되어 실시간으로 업데이트되도록 JavaScript 상태 관리 이벤트를 인라인으로 코딩한다.

7. **글래스모피즘 프리미엄 CSS 테마 적용**:
   - 투명하고 입체감 있는 어두운 계열의 프리미엄 글래스모피즘(Glassmorphism) 테마를 구현한다.
   - Harmonious HSL 컬러 세트, Inter/Outfit 및 Noto Sans KR 고급 서체, 부드러운 호버 전환 효과, 그라데이션 보더 라인 등을 적용하여 사용자 경험을 최고 수준으로 끌어올린다.

## Validation Notes

- **무결성 검증**: HTML 화면에 표시되는 시나리오별 목표가, 상승 여력, 재무 수치 등의 모든 수치는 원본 findings 및 `market-price-snapshot.md`에 기술된 공식 수치와 소수점까지 한 치의 오차도 없이 일치해야 한다.
- **QA 보류 표시**: 만약 `${ACTIVE_WORKSPACE}/09_qa/review.md` 또는 `final-check.md` 상태에서 결함이 확인되거나 미승인 상태인 경우, 대시보드 상단 또는 QA 카드에 눈에 띄는 빨간색 `⚠️ QA 검증 진행 중 (QA Pending)` 배지를 표시하여 투명성을 보장한다.
- **CORS 우회 검증**: 생성된 HTML 파일을 별도 로컬 서버 없이 파일 탐색기에서 직접 더블클릭(`file:///` 스키마)하여 열었을 때, 모든 탭 전환, 마크다운 전문 토글, 시나리오 컨트롤러, Chart.js 동적 드로잉이 어떠한 오류나 지연 없이 완벽하게 작동하는지 검증한다.

