---
name: idea-screener
description: 투자 아이디어 발굴 요청을 후보군, 점수표, 예비 Rating, 리스크, 다음 단계로 정리해 ${ACTIVE_WORKSPACE}/00_screen/에 저장하는 스크리닝 스킬
---

<!-- GENERATED-SYNC: source=plugins/vertical-plugins/invest-research/skills/idea-screener/SKILL.md; kind=skill; script=scripts/sync_invest_skills.py -->
> [!IMPORTANT]
> Generated execution artifact. Do not edit directly; edit the vertical source and rerun `python scripts/sync_invest_skills.py` (or `scripts/Sync-InvestSkills.ps1` / `scripts/Sync-InvestSkills.sh`).
> Common policies are synced from plugins/vertical-plugins/invest-research/policies/.
> Runtime output paths must use `${ACTIVE_WORKSPACE}`.
<!-- END GENERATED-SYNC -->


# idea-screener

## When to Use

- 사용자가 아직 특정 종목을 정하지 않고 투자 아이디어, 테마, 조건 기반 후보군 발굴을 요청할 때 사용한다.
- `/screen` command가 전달한 원문 프롬프트, 제약 조건, 시장 범위, `${ACTIVE_WORKSPACE}`를 받아 스크리닝 산출물을 작성한다.
- 실제 command wrapper는 얇게 유지하고, 후보 정의와 점수화 기준은 이 스킬이 소유한다.

## Required Inputs

- 사용자 원문 스크리닝 프롬프트
- 시장 / 지역 / 거래소 범위
- 테마, 산업, 팩터, 이벤트, 재무 조건 등 사용자가 지정한 조건
- 제외 조건 또는 금지 대상
- 기준일
- 비교기업 수 또는 shortlist 개수
- `${ACTIVE_WORKSPACE}`

## Output Files

모든 결과는 `${ACTIVE_WORKSPACE}/00_screen/` 아래에 저장한다.

| 파일 | 목적 |
|---|---|
| `${ACTIVE_WORKSPACE}/00_screen/screen-criteria.md` | 원문 요청, 해석한 조건, 포함/제외 기준, 데이터 소스 |
| `${ACTIVE_WORKSPACE}/00_screen/candidate-universe.md` | 초기 후보군, 식별자, 포함 사유, 제외 후보 |
| `${ACTIVE_WORKSPACE}/00_screen/idea-scorecard.md` | 후보별 점수표, 예비 Rating, 핵심 리스크 |
| `${ACTIVE_WORKSPACE}/00_screen/shortlist.md` | 최종 shortlist, 투자 논지, 다음 분석 단계 |

## Scoring Contract

후보별 점수는 0~5점으로 평가하고, 근거가 부족하면 점수 대신 `데이터 부족`을 기록한다.

| 항목 | 의미 |
|---|---|
| Thesis Fit | 사용자 테마 또는 조건과의 직접성 |
| Market Tailwind | 산업 성장, 정책, 수요, 사이클의 우호도 |
| Financial Quality | 수익성, 성장, 현금흐름, 재무 안정성 |
| Valuation / Risk-Reward | 기준 주가 대비 멀티플, FCF Yield, downside buffer |
| Catalyst Clarity | 3~12개월 확인 가능한 촉매의 명확성 |
| Data Confidence | 공식 출처와 시장 데이터의 확인 가능성 |

예비 Rating은 `Buy / Outperform / Neutral / Hold / Underperform / Sell` 중 하나를 사용할 수 있다. 예비 Rating은 심층 리포트의 최종 Rating이 아니며, `shortlist.md`에 근거와 한계를 함께 적는다.

## Workflow

1. **스크리닝 기준 정리**
   - 사용자 요청을 보존하고, 테마 / 조건 / 제외 범위 / 기준일을 분리한다.
   - 기준이 모호하면 가능한 해석을 명시하고 보수적으로 후보군을 넓게 잡는다.
   - 결과를 `${ACTIVE_WORKSPACE}/00_screen/screen-criteria.md`에 저장한다.

2. **후보군 수집**
   - 한국 기업은 DART/KRX 또는 `korea-stock` 사용 가능 시 우선한다.
   - 미국/글로벌 기업은 yfinance, 공식 IR, 거래소, 공시, 신뢰 가능한 공개 자료를 우선한다.
   - 후보별 기업명, 티커, 거래소, 통화, 포함 사유, 주요 출처를 정리한다.
   - 제외 후보는 제외 사유를 기록한다.
   - 결과를 `${ACTIVE_WORKSPACE}/00_screen/candidate-universe.md`에 저장한다.

3. **점수표 작성**
   - Scoring Contract의 6개 항목으로 후보를 평가한다.
   - 단순 인기, 뉴스 빈도, 가격 급등만으로 높은 점수를 주지 않는다.
   - 산식이나 시장지표가 필요한 경우 기준일과 출처를 기록한다.
   - 예비 Rating, 주요 리스크, 데이터 신뢰도를 함께 작성한다.
   - 결과를 `${ACTIVE_WORKSPACE}/00_screen/idea-scorecard.md`에 저장한다.

4. **Shortlist 작성**
   - 상위 후보를 3~10개 범위에서 정리한다. 사용자 지정 개수가 있으면 그 값을 따른다.
   - 각 후보에 대해 투자 논지, 확인할 지표, 주요 리스크, 다음 단계(`/analyze`, `/comps`, `/dcf`, `/earnings`)를 적는다.
   - 결과를 `${ACTIVE_WORKSPACE}/00_screen/shortlist.md`에 저장한다.

## Output Format

`shortlist.md`는 최소한 아래 구조를 포함한다.

```markdown
# Idea Shortlist

## 1. Screening Summary
- User prompt:
- 기준일:
- 시장 / 지역:
- 핵심 조건:
- 제외 조건:

## 2. Shortlist

| 순위 | 기업 | 티커 | 거래소/국가 | 총점 | 예비 Rating | 핵심 논지 | 주요 리스크 | 다음 단계 |
|---:|---|---|---|---:|---|---|---|---|
| 1 |  |  |  |  |  |  |  |  |

## 3. Follow-up Actions
- `/analyze ...`:
- `/comps ...`:
- `/dcf ...`:
- `/earnings ...`:

## 4. Data Limits
-
```

## Validation Notes

- 모든 산출물 경로는 `${ACTIVE_WORKSPACE}`를 사용한다.
- 후보 식별자는 기업명, 티커, 거래소/국가를 함께 기록한다.
- 예비 Rating은 근거와 한계를 동반해야 하며 개인화된 투자 자문처럼 쓰지 않는다.
- 스크리닝 결과는 심층 리포트의 대체물이 아니며 다음 분석 단계의 입력이다.
