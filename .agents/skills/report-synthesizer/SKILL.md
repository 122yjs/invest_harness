---
name: report-synthesizer
description: 전문가 findings를 invest_prompt_v2.md의 최종 출력 구조에 맞춰 _workspace/07_draft/report.md 초안으로 조립하는 합성 스킬
---

# report-synthesizer

## When to Use

- `_workspace/01_financial/findings.md`부터 `_workspace/06_risk_scenario/findings.md`까지의 전문가 산출물을 하나의 투자 리포트 초안으로 통합할 때 사용한다.
- Executive Summary, 종합 점수, 최종 의견, 투자 기간별 전략, 모니터링 체크리스트를 선행 분석과 일관되게 작성해야 할 때 사용한다.
- 출처 없는 신규 수치나 새로운 주장을 만들지 않고 기존 findings를 재구성해야 할 때 사용한다.

## Required Inputs

- `_workspace/00_input/request-summary.md`
- `_workspace/01_financial/findings.md`
- `_workspace/02_fundamental/findings.md`
- `_workspace/03_valuation/findings.md`
- `_workspace/04_technical/findings.md`
- `_workspace/05_macro_sentiment/findings.md`
- `_workspace/06_risk_scenario/findings.md`
- 선택 입력: `_workspace/06_risk_scenario/conflicts.md`
- 기준 문서: `invest_prompt_v2.md`

## Workflow Steps

1. **입력 완전성 확인**
   - 필수 findings 존재 여부를 확인한다.
   - 누락 파일이나 빈 섹션은 초안의 한계 및 추가 확인 필요 사항에 반영한다.

2. **섹션 매핑**
   - `invest_prompt_v2.md`의 최종 출력 템플릿 18개 섹션에 각 findings의 내용을 배치한다.
   - 동일 항목이 여러 findings에 있으면 출처와 기준일이 더 명확한 내용을 우선한다.

3. **Executive Summary 작성**
   - 핵심 투자 논지 3~5개, 핵심 리스크 3~5개, 재무 상태, 밸류에이션 판단, 기술적 흐름, 최종 의견을 1페이지 수준으로 요약한다.
   - 세부 본문과 모순되는 결론을 쓰지 않는다.

4. **종합 점수 작성**
   - `invest_prompt_v2.md`의 가중치 표를 사용한다.
   - 점수는 선행 근거가 있는 항목만 부여한다.
   - 근거가 부족하면 점수를 낮추거나 신뢰도를 낮게 표시하고 이유를 적는다.

5. **최종 의견과 전략 작성**
   - 최종 의견은 정보 제공용 일반 분석으로 표현한다.
   - 단기, 중기, 장기 전략은 시나리오, 리스크, 기술적 분석, 밸류에이션과 연결한다.
   - 가격 전략이 포함될 경우 개인화된 매매 권유처럼 쓰지 않는다.

6. **한계 정리**
   - 데이터 부족, 출처 충돌, 오래된 기준일, 공식 자료 미확인 항목을 마지막 섹션에 모은다.
   - 충돌 파일이 있으면 핵심 충돌과 처리 방안을 반영한다.

7. **파일 저장**
   - 초안을 `_workspace/07_draft/report.md`에 저장한다.

## Output Format

초안은 아래 섹션 순서를 그대로 따른다.

```markdown
# 투자 리서치 리포트 초안

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

## 15. 종합 점수 및 최종 의견

## 16. 투자 기간별 전략

## 17. 모니터링 체크리스트

## 18. 한계 및 추가 확인 필요 사항
```

## Validation Notes

- 신규 수치나 출처 없는 판단을 추가하지 않는다.
- Executive Summary와 최종 의견은 본문 근거와 일치해야 한다.
- 각 핵심 수치에는 출처, 기준일, 회계기간, 통화가 유지되어야 한다.
- 모든 섹션에는 최소한 요약 또는 데이터 부족 사유가 있어야 한다.
- 과도한 확신 표현과 개인화된 투자 자문 표현을 제거한다.
