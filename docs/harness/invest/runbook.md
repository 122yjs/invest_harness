# 투자 리서치 Harness 실행 가이드

## 목적

이 문서는 `invest_prompt_v2.md`와 `.agents/skills/*`를 반복적으로 사용해 개별 주식 투자 리포트를 생성하는 절차를 정의한다. 실행 환경은 Windows PowerShell을 기준으로 한다.

## 1. 입력 정리

1. 사용자 요청에서 기업명, 티커, 거래소/국가, 분석 기준일을 확인한다.
2. 누락된 선택값은 `invest-orchestrator`의 기본값 규칙을 적용한다.
3. `docs/harness/invest/templates/request-summary.md`를 기준으로 `_workspace/00_input/request-summary.md`를 작성한다.

필수 확인:

- 티커와 거래소가 같은 회사를 가리키는지 확인한다.
- 기준 통화와 회계 기준을 명시한다.
- 기술적 분석 포함 여부와 보고서 깊이를 기록한다.

## 2. 병렬 분석 산출물 생성

아래 전문가 스킬을 사용해 산출물을 만든다.

| 스킬 | 산출물 |
|---|---|
| `financial-analyst` | `_workspace/01_financial/findings.md` |
| `fundamental-analyst` | `_workspace/02_fundamental/findings.md` |
| `valuation-analyst` | `_workspace/03_valuation/findings.md` |
| `technical-analyst` | `_workspace/04_technical/findings.md` |
| `macro-sentiment-analyst` | `_workspace/05_macro_sentiment/findings.md` |
| `risk-scenario-analyst` | `_workspace/06_risk_scenario/findings.md` |

공통 규칙:

- 모든 핵심 수치에는 출처, 기준일, 회계기간, 통화, 산식을 붙인다.
- 데이터 부족 시 추정하지 않고 `공식 자료 미확인`, `데이터 부족`, `추가 확인 필요`로 표기한다.
- 충돌이 있으면 `_workspace/06_risk_scenario/conflicts.md`에 남긴다.

## 3. 초안 합성

`report-synthesizer`를 사용해 `_workspace/07_draft/report.md`를 작성한다.

초안은 아래 18개 섹션을 반드시 포함한다.

1. Executive Summary
2. 기업 개요
3. 핵심 투자 포인트
4. 재무 분석
5. 산업 및 경쟁 환경
6. 경영진 및 거버넌스
7. 경제적 해자
8. 제품 및 서비스
9. 밸류에이션
10. 기술적 분석
11. 뉴스 및 센티먼트
12. 거시경제 및 정책 환경
13. 리스크 분석
14. 시나리오 분석
15. 종합 점수 및 최종 의견
16. 투자 기간별 전략
17. 모니터링 체크리스트
18. 한계 및 추가 확인 필요 사항

## 4. QA 및 최종본

1. `qa-reviewer`로 `_workspace/09_qa/review.md`를 작성한다.
2. QA 판정이 `승인` 또는 `수정 후 승인`인지 확인한다.
3. 치명적 결함이 있으면 관련 findings를 보강하고 초안 합성을 다시 실행한다.
4. 최종본은 `_workspace/08_final/report.md`에 저장한다.
5. 사용자 전달용 짧은 요약이 필요하면 `_workspace/08_final/executive-summary.md`를 작성한다.

## 5. 구조 검증

최종 확정 전 Windows PowerShell에서 아래 명령을 실행한다.

```powershell
.\scripts\Test-HarnessStructure.ps1
```

검증이 실패하면 메시지에 나온 경로 또는 frontmatter를 수정한 뒤 다시 실행한다.

## 6. 운영 원칙

- 최신 데이터가 필요한 실제 종목 분석에서는 반드시 현재 기준으로 웹 또는 공식 공시를 확인한다.
- 기술적 분석과 소셜 센티먼트는 보조 신호로만 사용한다.
- 최종 보고서는 정보 제공용 분석이며 개인화된 투자 자문이 아니다.
- `_workspace/` 산출물은 감사와 재현을 위해 보존한다.
