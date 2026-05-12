---
name: html-report-synthesizer
description: Markdown 최종 리포트와 QA 결과를 HTML 리포트 계약으로 변환해 ${ACTIVE_WORKSPACE}/08_final/report.html에 저장하는 스킬
---

<!-- GENERATED-SYNC: source=plugins/vertical-plugins/invest-research/skills/html-report-synthesizer/SKILL.md; kind=skill; script=scripts/Sync-InvestSkills.ps1 -->
> [!IMPORTANT]
> Generated execution artifact. Do not edit directly; edit the vertical source and rerun pwsh ./scripts/Sync-InvestSkills.ps1.
> Common policies are synced from plugins/vertical-plugins/invest-research/policies/.
> Runtime output paths must use `${ACTIVE_WORKSPACE}`.
<!-- END GENERATED-SYNC -->


# html-report-synthesizer

## When to Use

- `/report-html` command가 최종 report 또는 workspace를 전달했을 때 사용한다.
- Markdown 리포트를 브라우저에서 읽기 좋은 HTML 산출물로 변환해야 할 때 사용한다.

## Required Inputs

- `${ACTIVE_WORKSPACE}/08_final/report.md` 또는 `${ACTIVE_WORKSPACE}/07_draft/report.md`
- `${ACTIVE_WORKSPACE}/00_input/market-price-snapshot.md`
- 선택 입력: `${ACTIVE_WORKSPACE}/09_qa/final-check.md`
- `${ACTIVE_WORKSPACE}`

## Output File

- `${ACTIVE_WORKSPACE}/08_final/report.html`

## Workflow

1. 원본 Markdown 리포트와 market-price snapshot, QA 상태를 읽는다.
2. 핵심 요약 카드, Rating / Price Target, 기준 주가, Upside / Downside를 상단에 배치한다.
3. 재무 추이, 피어 비교, DCF/역사적 밴드, 시나리오, 리스크 매트릭스, 출처 목록을 섹션으로 배치한다.
4. 원본에 없는 신규 수치나 판단을 만들지 않는다.
5. HTML은 로컬 정적 파일로 열 수 있게 외부 런타임 의존 없이 작성한다.

## Validation Notes

- HTML의 모든 핵심 숫자는 원본 Markdown 또는 findings에서 온 것이어야 한다.
- QA 상태가 미승인이면 HTML 상단에 `QA pending`을 표시한다.
- command wrapper는 HTML 내용을 생성하지 않고 이 스킬로 입력을 전달한다.
