---
name: earnings-update
description: 최신 또는 지정 분기 실적 발표를 확인해 매출, 이익, EPS, 가이던스, 컨센서스, Rating/Price Target 변화 영향을 ${ACTIVE_WORKSPACE}/00_input/earnings-update.md에 정리하는 스킬
---

<!-- GENERATED-SYNC: source=plugins/vertical-plugins/invest-research/skills/earnings-update/SKILL.md; kind=skill; script=scripts/sync_invest_skills.py -->
> [!IMPORTANT]
> Generated execution artifact. Do not edit directly; edit the vertical source and rerun `python scripts/sync_invest_skills.py` (or `scripts/Sync-InvestSkills.ps1` / `scripts/Sync-InvestSkills.sh`).
> Common policies are synced from plugins/vertical-plugins/invest-research/policies/.
> Runtime output paths must use `${ACTIVE_WORKSPACE}`.
<!-- END GENERATED-SYNC -->


# earnings-update

## When to Use

- `/earnings` command가 특정 기업과 `latest` 또는 분기/연도 선택자를 전달했을 때 사용한다.
- 기존 리포트의 입력 스냅샷을 최신 실적 기준으로 업데이트해야 할 때 사용한다.
- 실적 발표 후 Rating, Price Target, 밸류에이션, 리스크 시나리오가 바뀌는지 판단해야 할 때 사용한다.

## Required Inputs

- 대상 기업명 또는 티커
- 기간 선택자: `latest`, `Q1 2026`, `2026Q1` 등
- 거래소/국가와 기준 통화
- `${ACTIVE_WORKSPACE}`
- 선택 입력: 기존 `${ACTIVE_WORKSPACE}/00_input/request-summary.md`
- 선택 입력: 기존 `${ACTIVE_WORKSPACE}/00_input/market-price-snapshot.md`

## Output File

실적 업데이트 결과는 `${ACTIVE_WORKSPACE}/00_input/earnings-update.md`에 저장한다. 후속 리포트 생성 또는 QA는 이 파일을 입력으로 사용할 수 있다.

## Workflow

1. **대상과 기간 확정**
   - 기업명/티커, 거래소, 통화, 회계 기준, 실적 기간을 확인한다.
   - `latest` 요청이면 가장 최근 공식 실적 발표일과 대상 분기를 확인한다.

2. **공식 자료 우선 확인**
   - 한국 기업은 DART/KRX와 회사 IR을 우선한다.
   - 미국 기업은 SEC EDGAR, 회사 IR, 실적 발표 자료를 우선한다.
   - 글로벌 기업은 회사 IR, 거래소/규제 공시, yfinance 보조 데이터를 사용한다.
   - 공식 자료가 없으면 `공식 자료 미확인`으로 표시하고 비공식 출처를 보조로 분리한다.

3. **실적 변화 정리**
   - 매출, 영업이익, 순이익, EPS, 주요 마진, FCF의 YoY/QoQ 변화를 정리한다.
   - 컨센서스가 확인되면 Beat / In-line / Miss를 명시한다.
   - 컨센서스 출처, 기준일, 조정/GAAP 여부를 분리한다.

4. **가이던스와 코멘트 분석**
   - 가이던스 상향/유지/하향 여부와 핵심 원인을 정리한다.
   - 어닝콜 또는 경영진 코멘트가 있으면 수요, 가격, 비용, 재고, 수주, CAPEX, 규제 이슈로 분류한다.

5. **Rating / Price Target 영향 판단**
   - 기존 또는 예비 Rating이 있으면 유지/상향 가능/하향 가능으로만 표현한다.
   - Price Target 변경 필요성이 있으면 기준 주가, EPS/EBITDA/FCF 변화, 멀티플 또는 DCF 가정을 연결한다.
   - 근거가 부족하면 `추가 확인 필요`로 표시한다.

6. **파일 저장**
   - 결과를 `${ACTIVE_WORKSPACE}/00_input/earnings-update.md`에 저장한다.

## Output Format

```markdown
# Earnings Update

## 1. 대상 및 기준
- 기업명 / 티커:
- 실적 기간:
- 발표일:
- 기준 통화:
- 회계 기준:
- 주요 출처:

## 2. 실적 요약

| 항목 | 실제 | YoY | QoQ | 컨센서스 | Beat/Miss | 출처 |
|---|---:|---:|---:|---:|---|---|
| 매출 |  |  |  |  |  |  |
| 영업이익 |  |  |  |  |  |  |
| EPS |  |  |  |  |  |  |
| FCF |  |  |  |  |  |  |

## 3. 가이던스 및 경영진 코멘트
- 가이던스 변화:
- 수요 / 가격:
- 비용 / 마진:
- CAPEX / 현금흐름:

## 4. Rating / Price Target 영향
- 기존 또는 예비 Rating:
- 변경 방향:
- Price Target 영향:
- 핵심 근거:
- 추가 확인 필요:

## 5. 후속 업데이트 대상
- `${ACTIVE_WORKSPACE}/00_input/market-price-snapshot.md`:
- `${ACTIVE_WORKSPACE}/03_valuation/findings.md`:
- `${ACTIVE_WORKSPACE}/07_draft/report.md`:
- `${ACTIVE_WORKSPACE}/09_qa/review.md`:
```

## Validation Notes

- 실적 수치는 기준일, 회계기간, 통화, 출처를 함께 기록한다.
- Beat/Miss는 컨센서스 출처가 확인된 경우에만 판정한다.
- Rating / Price Target 변화는 근거가 확인된 범위에서만 제시한다.
- command wrapper는 실적 분석을 수행하지 않고 이 스킬로 입력을 전달한다.
