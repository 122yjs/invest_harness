---
name: earnings-preview
description: 예정 실적 발표 전 핵심 지표, 기대치, Beat/Miss 시나리오, 발표 후 업데이트 항목을 ${ACTIVE_WORKSPACE}/00_input/earnings-preview.md에 정리하는 스킬
---

<!-- GENERATED-SYNC: source=plugins/vertical-plugins/invest-research/skills/earnings-preview/SKILL.md; kind=skill; script=scripts/sync_invest_skills.py -->
> [!IMPORTANT]
> Generated execution artifact. Do not edit directly; edit the vertical source and rerun python scripts/sync_invest_skills.py (or scripts/Sync-InvestSkills.ps1 / scripts/Sync-InvestSkills.sh).
> Common policies are synced from plugins/vertical-plugins/invest-research/policies/.
> Runtime output paths must use `${ACTIVE_WORKSPACE}`.
<!-- END GENERATED-SYNC -->


# earnings-preview

## When to Use

- `/preview` command가 기업명/티커와 예정 분기 또는 `latest` 힌트를 전달했을 때 사용한다.
- 실적 발표 전 확인할 KPI, 시장 기대치, 시나리오, 발표 후 갱신해야 할 산출물을 정리해야 할 때 사용한다.

## Required Inputs

- 기업명 또는 티커
- 예정 실적 기간 또는 이벤트 힌트
- 거래소/국가, 기준 통화, 회계 기준
- `${ACTIVE_WORKSPACE}`
- 선택 입력: `${ACTIVE_WORKSPACE}/00_input/request-summary.md`
- 선택 입력: `${ACTIVE_WORKSPACE}/00_input/market-price-snapshot.md`

## Output File

- `${ACTIVE_WORKSPACE}/00_input/earnings-preview.md`

## Workflow

1. 발표 예정 기간과 확인 가능한 공식 일정, IR 캘린더, 공시 일정을 구분한다.
2. 이번 실적에서 봐야 할 핵심 지표를 매출, 마진, EPS, FCF, 수주/재고/CAPEX 등으로 분리한다.
3. 컨센서스가 확인되면 출처와 기준일을 명시하고, 확인되지 않으면 `데이터 부족`으로 표시한다.
4. Beat / In-line / Miss 시나리오별로 Rating, Price Target, 밸류에이션, 리스크에 미칠 수 있는 업데이트 항목을 정리한다.
5. 발표 후 `/earnings`, `/dcf`, `/qa`, `/update`로 이어질 후속 작업을 명시한다.

## Validation Notes

- 예측 수치는 출처가 확인된 경우에만 사용한다.
- 시나리오는 가능성 정리이며 확정 결론으로 쓰지 않는다.
- command wrapper는 preview 분석을 수행하지 않고 이 스킬로 입력을 전달한다.
