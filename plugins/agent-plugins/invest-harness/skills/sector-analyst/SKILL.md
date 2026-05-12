---
name: sector-analyst
description: 섹터/산업 리포트를 작성해 산업 구조, 수요 동인, 피어, 리스크, 모니터링 지표를 ${ACTIVE_WORKSPACE}/02_fundamental/sector.md에 정리하는 스킬
---

<!-- GENERATED-SYNC: source=plugins/vertical-plugins/invest-research/skills/sector-analyst/SKILL.md; kind=skill; script=scripts/Sync-InvestSkills.ps1 -->
> [!IMPORTANT]
> Generated execution artifact. Do not edit directly; edit the vertical source and rerun pwsh ./scripts/Sync-InvestSkills.ps1.
> Common policies are synced from plugins/vertical-plugins/invest-research/policies/.
> Runtime output paths must use `${ACTIVE_WORKSPACE}`.
<!-- END GENERATED-SYNC -->


# sector-analyst

## When to Use

- `/sector` command가 산업, 테마, 지역, 시장 범위를 전달했을 때 사용한다.
- 단일 기업 분석 전에 섹터 구조와 후보군을 파악해야 할 때 사용한다.

## Required Inputs

- 섹터/산업/테마 원문
- 지역, 거래소, 통화 범위
- 분석 기준일
- `${ACTIVE_WORKSPACE}`

## Output File

- `${ACTIVE_WORKSPACE}/02_fundamental/sector.md`

## Workflow

1. 산업 정의, value chain, 주요 수요/공급 동인을 정리한다.
2. 핵심 피어와 관련 기업을 식별하고, 기업명/티커/거래소/국가를 함께 기록한다.
3. 규제, 원재료, 금리, 환율, 기술 변화 등 섹터별 민감도를 분리한다.
4. 3~12개월 확인 가능한 촉매와 장기 구조 변수를 구분한다.
5. 후속 `/screen`, `/analyze`, `/comps` 입력으로 사용할 후보와 지표를 정리한다.

## Validation Notes

- 섹터 결론은 단일 종목 Rating을 대체하지 않는다.
- 모든 핵심 지표에는 출처, 기준일, 통화 또는 단위를 남긴다.
- 데이터가 부족하면 `추가 확인 필요`로 표시한다.
