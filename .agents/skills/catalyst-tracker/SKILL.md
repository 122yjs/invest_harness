---
name: catalyst-tracker
description: 기업/테마의 촉매 이벤트 캘린더를 작성해 시점, 근거, 기대 영향, 확인 지표를 ${ACTIVE_WORKSPACE}/05_macro_sentiment/catalysts.md에 정리하는 스킬
---

<!-- GENERATED-SYNC: source=plugins/vertical-plugins/invest-research/skills/catalyst-tracker/SKILL.md; kind=skill; script=scripts/sync_invest_skills.py -->
> [!IMPORTANT]
> Generated execution artifact. Do not edit directly; edit the vertical source and rerun `python scripts/sync_invest_skills.py` (or `scripts/Sync-InvestSkills.ps1` / `scripts/Sync-InvestSkills.sh`).
> Common policies are synced from plugins/vertical-plugins/invest-research/policies/.
> Runtime output paths must use `${ACTIVE_WORKSPACE}`.
<!-- END GENERATED-SYNC -->


# catalyst-tracker

## When to Use

- `/catalysts` command가 기업명, 테마, 기간, 이벤트 힌트를 전달했을 때 사용한다.
- 실적, 규제, 수주, 신제품, 소송, M&A, 관세 등 이벤트를 시간순으로 추적해야 할 때 사용한다.

## Required Inputs

- 기업명, 섹터, 또는 테마
- 기간 범위
- 이벤트 유형 힌트
- `${ACTIVE_WORKSPACE}`

## Output File

- `${ACTIVE_WORKSPACE}/05_macro_sentiment/catalysts.md`

## Workflow

1. 기간 범위를 확정하고 공식 일정, 공시, IR, 규제 캘린더를 우선 확인한다.
2. 이벤트별 예상 시점, 확인 출처, 영향을 받을 재무/밸류에이션 항목을 기록한다.
3. 촉매가 이미 주가에 반영되었는지 판단하려면 별도 기술적/센티먼트 입력이 필요한지 표시한다.
4. 후속 `/earnings`, `/thesis`, `/update`, `/qa` 연결 지점을 남긴다.

## Validation Notes

- 날짜가 확정되지 않은 이벤트는 예상 범위와 불확실성을 명시한다.
- 이벤트 영향은 확정 결론이 아니라 확인해야 할 가설로 표현한다.
