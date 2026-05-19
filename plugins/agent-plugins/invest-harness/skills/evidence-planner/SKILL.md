---
name: evidence-planner
description: 사용자 요청을 open-ended question decomposition과 evidence plan으로 변환해 ${ACTIVE_WORKSPACE}/00_evidence 산출물을 작성하는 스킬
---

<!-- GENERATED-SYNC: source=plugins/vertical-plugins/invest-research/skills/evidence-planner/SKILL.md; kind=skill; script=scripts/sync_invest_skills.py -->
> [!IMPORTANT]
> Generated execution artifact. Do not edit directly; edit the vertical source and rerun python scripts/sync_invest_skills.py (or scripts/Sync-InvestSkills.ps1 / scripts/Sync-InvestSkills.sh).
> Common policies are synced from plugins/vertical-plugins/invest-research/policies/.
> Runtime output paths must use `${ACTIVE_WORKSPACE}`.
<!-- END GENERATED-SYNC -->


# evidence-planner

## When to Use

- 기존 analyst fan-out 전에 필요한 근거 유형, source capability, signal primitive, validation gate를 정리할 때 사용한다.
- 사용자의 요청이 회사 공시만으로 충분하지 않고 외부 증거, 시장 맥락, 검색 관심, 무역, 조달, 규제, macro evidence를 요구할 때 사용한다.
- `/evidence` 또는 `/market-intel` thin command가 evidence planning을 요청할 때 사용한다.

## Required Inputs

- 사용자 원문 요청
- `${ACTIVE_WORKSPACE}/00_input/input-intake.md`
- `${ACTIVE_WORKSPACE}/00_input/request-summary.md`
- 기준 문서: `docs/harness/invest/research-layer/question-decomposition.md`
- 기준 문서: `docs/harness/invest/research-layer/signal-primitives.md`
- 템플릿: `docs/harness/invest/templates/evidence-plan.md`

## Output Paths

- `${ACTIVE_WORKSPACE}/00_evidence/question-decomposition.md`
- `${ACTIVE_WORKSPACE}/00_evidence/evidence-plan.md`

## Rules

- Preserve user surface terms in `subjects`.
- Use open-ended `subjects`, not `product_classification`, as the core planning unit.
- Do not output `use_case:` as core routing metadata.
- Do not hard-code a fixed product taxonomy or product enum.
- If a concept is unfamiliar, keep the surface form, generate candidate search terms, and mark mapping confidence low.
- Select evidence needs from claim type and evidence type.
- Select signal primitives from evidence type and downstream analyst need.
- **다모다란 3대 내러티브 필터 검증 규칙**: 비즈니스 내러티브에 대해 다음과 같은 Validation Gate인 `narrative_plausibility` 검증 규칙을 설계에 반드시 반영한다.
  - **가능성 (Possibility)**: 제안된 스토리가 비즈니스 규칙과 물리 법칙상 가능한가? (예: 업계 총시장규모(TAM)를 초과하는 점유율 가정이 없는가?)
  - **타당성 (Plausibility)**: 역사적 선례와 경제적 원리(해자, 마진 구조 등)에 비추어 타당한가? (예: 업계에서 전례가 없는 초고속 성장과 최고 마진이 동시에 일어나는 가정의 타당성 검증)
  - **개연성 (Probability)**: 주가에 이미 반영된 시장 기대치 대비 현실화될 확률이 있는가? (예: 시장 컨센서스와의 비교)
- Do not fetch data, call APIs, store API keys, or make investment conclusions.

## Workflow

1. Read the user request and current input summary.
2. Decompose the request into entities, open-ended subjects, geographies, time horizon, investment claim types, and required evidence types.
3. For each required evidence type, explain why it is required, optional, or validation-only.
4. Select signal primitives from `docs/harness/invest/research-layer/signal-primitives.md`.
5. Add validation gates for each evidence type (특히 비즈니스 내러티브에 대해서는 다모다란의 3대 필터인 가능성, 타당성, 개연성을 평가하기 위한 `narrative_plausibility` 게이트를 필수 설계).
6. Record unresolved ambiguities and whether user input is needed.
7. Write outputs to `${ACTIVE_WORKSPACE}/00_evidence/`.

## Output Contract

`question-decomposition.md` must include:

- raw request
- entities
- subjects
- geographies
- time horizon
- investment claim types
- required evidence types
- mapping confidence

`evidence-plan.md` must include:

- raw request
- question decomposition
- required evidence types
- source capability needs
- signal primitives needed
- validation gates
- unresolved ambiguities

## Prohibited

- Do not implement source calls.
- Do not infer sales from search interest.
- Do not infer market size from relative indexes.
- Do not infer company revenue from trade or procurement data alone.
- Do not replace analyst role findings.
