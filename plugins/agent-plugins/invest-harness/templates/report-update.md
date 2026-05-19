<!-- GENERATED-SYNC: source=plugins/vertical-plugins/invest-research/templates/report-update.md; kind=template; script=scripts/sync_invest_skills.py -->
> [!IMPORTANT]
> Generated execution artifact. Do not edit directly; edit the vertical source and rerun `python scripts/sync_invest_skills.py` (or `scripts/Sync-InvestSkills.ps1` / `scripts/Sync-InvestSkills.sh`).
> Common policies are synced from plugins/vertical-plugins/invest-research/policies/.
> Runtime output paths must use `${ACTIVE_WORKSPACE}`.
<!-- END GENERATED-SYNC -->

# Report Update Plan

| Field | Value |
|---|---|
| Active workspace | `${ACTIVE_WORKSPACE}` |
| Company / ticker |  |
| Update date |  |
| Source report | `${ACTIVE_WORKSPACE}/07_draft/report.md` |

## New Inputs

| 입력 | 파일 / 출처 | 기준일 | 신뢰도 | 메모 |
|---|---|---|---|---|
| Earnings update | `${ACTIVE_WORKSPACE}/00_input/earnings-update.md` |  |  |  |
| Thesis tracker | `${ACTIVE_WORKSPACE}/05_macro_sentiment/thesis-update.md` |  |  |  |
| Catalyst calendar | `${ACTIVE_WORKSPACE}/05_macro_sentiment/catalysts.md` |  |  |  |
| QA review | `${ACTIVE_WORKSPACE}/09_qa/review.md` |  |  |  |

## Section Impact Map

| 리포트 섹션 | 유지 / 수정 / 추가 확인 | 변경 이유 | 필요한 후속 작업 |
|---|---|---|---|
| Executive Summary |  |  |  |
| 재무 분석 |  |  |  |
| 밸류에이션 |  |  |  |
| Rating, Price Target 및 투자 의견 |  |  |  |
| 리스크 분석 |  |  |  |
| 모니터링 체크리스트 |  |  |  |

## Rating / Price Target Impact

- 기준 주가 변경:
- 실적 입력값 변경:
- 시나리오 변경:
- Rating 변화 가능성:
- Price Target 재계산 필요:

## QA Targets

- `${ACTIVE_WORKSPACE}/09_qa/review.md`:
- `${ACTIVE_WORKSPACE}/09_qa/fix-list.md`:
- `${ACTIVE_WORKSPACE}/09_qa/final-check.md`:

## Data Limits

-
