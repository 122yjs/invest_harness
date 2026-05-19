---
name: section-report-writer
description: findings.md를 읽고 해당 섹션의 정성적 해석, 투자 함의, 리스크/촉매 의미를 report.md로 작성하는 전담 글쓰기 스킬
---

# section-report-writer

## When to Use

- analyst가 작성한 findings.md를 바탕으로 정성적 해석과 투자 함의를 정리할 때
- 각 파트(재무, 펀더멘털, 밸류에이션, 기술적, 매크로, 리스크)의 "So What"을 명확히 할 때
- findings에 새로운 데이터나 출처 없는 주장을 추가하지 않고, 기존 수치와 팩트를 해석할 때
- 투자 리포트의 섹션별 report.md를 작성할 때

## Required Inputs

- `${ACTIVE_WORKSPACE}/00_input/request-summary.md`
- `${ACTIVE_WORKSPACE}/00_input/market-price-snapshot.md`
- `${ACTIVE_WORKSPACE}/00_evidence/evidence-ledger.md` (선택)
- `${ACTIVE_WORKSPACE}/00_evidence/source-validation.md` (선택)
- `${ACTIVE_WORKSPACE}/{section}/findings.md` — 대상 섹션의 findings (예: `01_financial/findings.md`)
- `section_id` — 대상 섹션 식별자 (예: `01_financial`, `02_fundamental` 등)

## Workflow

1. **findings.md 읽기**
   - 해당 섹션의 findings.md를 완전히 읽는다.
   - 표, 수치, 출처, 한계를 파악한다.

2. **정성적 해석 작성**
   - findings의 핵심 데이터를 바탕으로 2~3개의 핵심 "So What"을 도출한다.
   - 표/수치의 반복 진술은 최소화하고, 데이터가 의미하는 바를 서술한다.
   - 각 핵심 해석에는 출처와 기준일을 명시한다.

3. **투자 함의 정리**
   - 해당 섹션의 데이터가 투자 논리에 어떤 영향을 미치는지 서술한다.
   - 긍정적 함의와 부정적 함의를 균형 있게 제시한다.
   - 불확실성이나 데이터 한계는 명시한다.

4. **리스크/촉매 의미 정리**
   - 해당 섹션에서 도출된 리스크와 촉매를 정리한다.
   - 리스크의 단기/중장기 영향을 구분한다.

5. **report.md 저장**
   - `${ACTIVE_WORKSPACE}/{section}/report.md`에 저장한다.

## Output Structure Contract

### 섹션별 Report 레벨 (정성적 해석)
- **역할**: section-report-writer가 수행
- **출력**: `${ACTIVE_WORKSPACE}/{section}/report.md`
- **내용**: findings를 바탕으로 한 정성적 해석과 투자 함의
- **핵심 질문**: "이 파트의 데이터가 투자적으로 무슨 의미인가(So What)"

### 금지 사항
- findings에 없던 새로운 수치나 출처 없는 주장 생성
- 표/수치의 단순 반복 진술
- 과도한 확신 표현 ("확실한 매수", "반드시" 등)
- 투자 결론이나 매매 의견 (이는 최종 report-synthesizer의 역할)

### 규칙
- 표/수치 반복 최소화: findings에 이미 있으므로 report에서는 해석 중심
- 2~3개 핵심 So What: findings의 여러 데이터를 관통하는 핵심 메시지
- 투자 함의와 리스크 분리: 긍정/부정을 균형 있게
- 불확실성 명시: "추정", "확인 필요", "가정" 등의 표현 사용
- 한국어 `합니다/입니다`체, 전문 용어는 한국어로 풀어쓰기

## Output Format

```markdown
# {섹션명} Report

## 1. 핵심 해석 (So What)

### 해석 1: {제목}
{findings 기반 해석 문단. 3~5문장}
> **근거**: {findings의 특정 표/수치 참조}
> **출처**: {출처명} | **기준일**: {YYYY-MM-DD}

### 해석 2: {제목}
...

### 해석 3: {제목}
...

## 2. 투자 함의

### 긍정적 함의
- {함의 1}
- {함의 2}

### 부정적 함의
- {함의 1}
- {함의 2}

## 3. 리스크 / 촉매

### 리스크
- {리스크 1}: {단기/중장기 영향}
- {리스크 2}: {단기/중장기 영향}

### 촉매
- {촉매 1}: {예상 시기, 확인 지표}
- {촉매 2}: {예상 시기, 확인 지표}

## 4. 데이터 한계 및 추가 확인 필요 사항
- {한계 1}
- {한계 2}
```

## Validation Notes

- findings.md에 없는 수치나 주장이 report.md에 포함되었는지 Self-check
- 표/수치가 30% 이상 반복되지 않는지 확인
- "So What" 해석이 findings 데이터에서 직접 도출되었는지 확인
- 불확실성이 적절히 명시되었는지 확인
