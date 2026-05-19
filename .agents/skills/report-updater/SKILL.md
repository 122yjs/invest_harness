---
name: report-updater
description: 기존 리포트를 새 이벤트나 실적 기준으로 갱신할 범위와 재실행 작업을 ${ACTIVE_WORKSPACE}/00_input/update-plan.md에 정리하는 스킬
---

<!-- GENERATED-SYNC: source=plugins/vertical-plugins/invest-research/skills/report-updater/SKILL.md; kind=skill; script=scripts/sync_invest_skills.py -->
> [!IMPORTANT]
> Generated execution artifact. Do not edit directly; edit the vertical source and rerun python scripts/sync_invest_skills.py (or scripts/Sync-InvestSkills.ps1 / scripts/Sync-InvestSkills.sh).
> Common policies are synced from plugins/vertical-plugins/invest-research/policies/.
> Runtime output paths must use `${ACTIVE_WORKSPACE}`.
<!-- END GENERATED-SYNC -->


# report-updater

## When to Use

- `/update` command가 기존 리포트, 기업명, 이벤트, 또는 갱신 범위를 전달했을 때 사용한다.
- 전체 재작성 전에 어떤 산출물을 다시 실행해야 하는지 결정해야 할 때 사용한다.

## Required Inputs

- 기존 report path 또는 기업명/티커
- 업데이트 범위: 실적, 가이던스, M&A, 규제, 소송, 신제품, 관세, 수주, 공급망 등
- `${ACTIVE_WORKSPACE}`

## Output File

- `${ACTIVE_WORKSPACE}/00_input/update-plan.md`

## Workflow

1. 기존 리포트와 새 이벤트의 기준일을 비교한다.
2. 영향을 받을 산출물을 `00_input`, `03_valuation`, `05_macro_sentiment`, `06_risk_scenario`, `07_draft`, `09_qa` 중에서 지정한다.
3. 재실행해야 할 command와 skill을 순서대로 적는다.
4. Rating / Price Target 재검증 필요 여부를 표시한다.

## Validation Notes

- update-plan은 갱신 실행 계획이며 최종 리포트 변경 자체가 아니다.
- 새 수치가 필요한 경우 원천 데이터와 재계산 책임 skill을 명확히 지정한다.
