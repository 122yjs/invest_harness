---
name: signal-analyst
description: evidence-ledger를 signal primitives로 변환해 ${ACTIVE_WORKSPACE}/00_evidence/signal-cards.md를 작성하는 경량 스킬
---

# signal-analyst

## When to Use

- `${ACTIVE_WORKSPACE}/00_evidence/evidence-ledger.md`가 있고 analyst fan-out 전에 reusable signal cards가 필요할 때 사용한다.
- evidence-planner가 `signal_primitives_needed`를 지정했을 때 사용한다.

## Required Inputs

- `${ACTIVE_WORKSPACE}/00_evidence/evidence-plan.md`
- `${ACTIVE_WORKSPACE}/00_evidence/evidence-ledger.md`
- 기준 문서: `docs/harness/invest/research-layer/signal-primitives.md`
- 기준 문서: `docs/harness/invest/research-layer/claim-boundary-policy.md`
- 템플릿: `docs/harness/invest/templates/signal-card.md`

## Output Paths

- `${ACTIVE_WORKSPACE}/00_evidence/signal-cards.md`

## Rules

- Use signal primitives, not product use-cases.
- Each signal card must preserve subject, geography, period, input evidence IDs, calculation, output signal, confidence, caveats, and downstream analyst usage.
- If input evidence is insufficient, write a low-confidence or blocked signal instead of inventing a metric.
- Keep claim boundaries visible next to the signal.

## Prohibited

- Do not create investment recommendations.
- Do not turn relative indexes into market size or sales.
- Do not turn trade or procurement evidence into company revenue without disclosure evidence.
- Do not replace analyst findings.
