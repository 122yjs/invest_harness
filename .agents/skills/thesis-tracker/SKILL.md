---
name: thesis-tracker
description: 기존 투자 논지를 새 데이터와 비교해 강화/약화 증거, Rating 변화 가능성, 다음 추적 지표를 ${ACTIVE_WORKSPACE}/05_macro_sentiment/thesis-update.md에 정리하는 스킬
---

<!-- GENERATED-SYNC: source=plugins/vertical-plugins/invest-research/skills/thesis-tracker/SKILL.md; kind=skill; script=scripts/sync_invest_skills.py -->
> [!IMPORTANT]
> Generated execution artifact. Do not edit directly; edit the vertical source and rerun python scripts/sync_invest_skills.py (or scripts/Sync-InvestSkills.ps1 / scripts/Sync-InvestSkills.sh).
> Common policies are synced from plugins/vertical-plugins/invest-research/policies/.
> Runtime output paths must use `${ACTIVE_WORKSPACE}`.
<!-- END GENERATED-SYNC -->


# thesis-tracker

## When to Use

- `/thesis` command가 특정 기업, 기존 논지, 새 이벤트 또는 추적 기간을 전달했을 때 사용한다.
- 기존 리포트의 핵심 투자 포인트가 최신 데이터로 유지되는지 점검해야 할 때 사용한다.

## Required Inputs

- 기업명 또는 티커
- 기존 투자 논지 또는 기존 report path
- 새 데이터, 이벤트, 기간 힌트
- `${ACTIVE_WORKSPACE}`

## Output File

- `${ACTIVE_WORKSPACE}/05_macro_sentiment/thesis-update.md`

## Workflow

1. 기존 논지를 3~5개 claim으로 분해하고 각 claim의 원래 근거를 기록한다.
2. 새 데이터가 각 claim을 강화, 유지, 약화, 미확인 중 어디에 해당하는지 분류한다.
3. Rating 또는 Price Target 변경 가능성이 있으면 어떤 산출물을 다시 계산해야 하는지 적는다.
4. 다음 추적 지표와 확인 주기를 지정한다.

## Validation Notes

- 기존 논지와 새 데이터를 섞어 확정 결론을 만들지 않는다.
- 출처 없는 claim은 `근거 미확인`으로 표시한다.
- 변경 판단은 QA와 valuation 재검증 대상으로 남긴다.
