---
name: morning-note
description: 관심종목 또는 테마의 일일 점검 노트를 ${ACTIVE_WORKSPACE}/05_macro_sentiment/morning-note.md에 작성하는 스킬
---

# morning-note

## When to Use

- `/morning-note` command가 관심종목, 테마, 또는 공란 입력을 전달했을 때 사용한다.
- 전일/당일 주요 이벤트, 가격 변동, 실적/공시, 후속 작업을 짧게 정리해야 할 때 사용한다.

## Required Inputs

- 관심종목 또는 테마 목록
- 기준일
- `${ACTIVE_WORKSPACE}`
- 선택 입력: 기존 shortlist 또는 watchlist

## Output File

- `${ACTIVE_WORKSPACE}/05_macro_sentiment/morning-note.md`

## Workflow

1. 점검 대상과 기준일을 명시한다.
2. 주요 뉴스, 공시, 가격/거래량 변화, 일정 변화를 분리한다.
3. 각 항목을 `무시 가능`, `관찰`, `업데이트 필요`, `QA 필요`로 태깅한다.
4. 후속 `/earnings`, `/thesis`, `/catalysts`, `/update`, `/qa` 작업을 정리한다.

## Validation Notes

- 일일 노트는 심층 리포트를 대체하지 않는다.
- 최신 데이터가 필요한 항목은 기준일과 출처를 반드시 남긴다.
