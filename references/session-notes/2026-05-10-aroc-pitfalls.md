# AROC Session Notes (2026-05-10)

실제 Harness 실행 세션에서 발견된 함정과 해결 과정 기록.

---

## 1. Delegate Task Path Mismatch

**문제:** 오케스트레이터가 `~/invest-harness-aroc/_workspace/`를 생성했으나, `delegate_task`로 실행된 서브에이전트들은 기본 경로 `~/.hermes/workspace/_workspace/`에 파일을 저장했다.

**경과:**
- financial-analyst, fundamental-analyst, valuation-analyst — Group 1은 `~/.hermes/workspace/_workspace/01~03`에 저장
- technical-analyst, macro-sentiment-analyst, risk-scenario-analyst — Group 2도 동일한 기본 경로에 저장
- 오케스트레이터의 `~/invest-harness-aroc/_workspace/`에는 최초 입력 정규화 파일만 존재

**해결:** 후속 단계(report-synthesizer, qa-reviewer)에서 모든 읽기/uc4f0기 경로를 `~/.hermes/workspace/_workspace/`로 통일했다. 범용 방식: 최초 프로젝트 디렉터리 생성 대신, 기본 워크스페이스의 `_workspace/`를 직접 사용하는 것이 간단하다.

## 2. Risk-Scenario Misjudgment of Missing Files

**문제:** risk-scenario-analyst가 `04_technical/findings.md`와 `05_macro_sentiment/findings.md`가 "존재하지 않음"으로 판단했다.

**원인:** Group 1(financial, fundamental, valuation)과 Group 2(technical, macro, risk)가 `delegate_task`의 동일한 호출에서 병렬 실행되었다. risk-scenario-analyst는 Group 2 내부의 하나였으므로, technical과 macro의 출력이 완료되기 전에 자신의 작업을 시작하였다.

**해결:** 실제로는 technical/macro findings이 나중에 생성되었으므로 report-synthesizer에서는 모든 6개 findings를 사용할 수 있었다. 다음에는 risk-scenario-analyst를 technical/macro 완료 후에 또는 동일 delegate_task의 변수로 배치해야 한다.

## 3. Report-Synthesizer Numerical Drift

**문제:** QA 검토에서 경쟁사 비교 테이블의 수치 불일치 4건 발견:

| 항목 | 초안 오류 | 정정 값 | 출처 |
|---|---|---|---|
| AROC PER | 14.5x | 20.7x (TTM) | 03_valuation findings |
| AROC 영업이익률 | 21.6% | 36.5% | 01_financial findings |
| AROC EV/EBITDA | 8.5x | 10.3x (TTM) | 03_valuation findings |
| 종합 점수 | 72 | 71.75 | 15.1 산출 테이블 |

**원인:** report-synthesizer가 02_fundamental의 추정치를 03_valuation의 검증된 값대신 사용했고, 순이익률과 영업이익률을 혼동했다.

**해결:** 패치 적용 후 QA가 "수정 후 승인"을 내렸다. 다음에는 report-synthesizer가 초안 작성 후 원천 findings의 핵심 수치와 cross-check하는 단계를 독립적으로 도입해야 한다.

## 4. Missing Executive Summary in 08_final

**문제:** 처음 최종본을 확정할 때 `08_final/executive-summary.md`가 없었다.

**해결:** 오케스트레이터가 직접 `08_final/executive-summary.md`를 별도 작성했다. 이는 runbook에 명시된 흐름이지만, report-synthesizer가 자동으로 생성하지 못하는 경우가 있음을 확인했다.

## 5. Conflicts.md Recorded 9 Items

충돌 유형:
- Contract Operations 매출 비중: 87% vs 89%
- 순부채/EBITDA: 2.92x vs 2.7x
- 시가총액/EV: $6.68B vs $6.48B vs $8.86B
- GAAP vs Adjusted FCF Yield: 1.85% vs 5.36%
- Q1 EPS miss 기준: GAAP $0.41 vs Adjusted $0.42
- 배당 인상률: 16% vs 20%
- 기술적 지표 출처 불일치: RSI 48.97 vs 75.13, MACD 방향 상이

모든 충돌는 최종 보고서의 "한계 및 추가 확인 필요 사항"에 반영되었다.
