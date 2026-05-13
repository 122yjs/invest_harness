# Evidence Research Layer Overview

The evidence research layer is a pre-analyst planning layer for `invest_harness`.
It does not replace the existing analyst fan-out. It creates a reusable evidence
plan, source plan, ledger, signal cards, and validation record before specialist
skills write financial, fundamental, valuation, technical, macro, sentiment, and
risk findings.

## Pipeline

```text
User Request
-> Input Gate
-> Question Decomposition
-> Evidence Planner
-> Source Capability Router
-> Evidence Ledger
-> Signal Primitives
-> Validation Gate
-> Existing Analyst Fan-out
-> Draft
-> QA
-> Final
```

## Responsibilities

| Stage | Owner | Output |
|---|---|---|
| Input Gate | `invest-orchestrator` | `${ACTIVE_WORKSPACE}/00_input/input-intake.md` |
| Question Decomposition | `evidence-planner` | `${ACTIVE_WORKSPACE}/00_evidence/question-decomposition.md` |
| Evidence Planner | `evidence-planner` | `${ACTIVE_WORKSPACE}/00_evidence/evidence-plan.md` |
| Source Capability Router | `source-router` | `${ACTIVE_WORKSPACE}/00_evidence/source-call-plan.md` |
| Evidence Ledger | source-owning skills or operator | `${ACTIVE_WORKSPACE}/00_evidence/evidence-ledger.md` |
| Signal Primitives | `signal-analyst` or analyst roles | `${ACTIVE_WORKSPACE}/00_evidence/signal-cards.md` |
| Validation Gate | `source-router`, `qa-reviewer` | `${ACTIVE_WORKSPACE}/00_evidence/source-validation.md` |

## Design Rules

- Preserve the existing `00_input/`, `01_financial/`, `02_fundamental/`,
  `03_valuation/`, `04_technical/`, `05_macro_sentiment/`, `06_risk_scenario/`,
  `07_draft/`, `08_final/`, and `09_qa/` directories.
- Route sources by required evidence type and source capability.
- Keep user surface terms even when candidate mappings are uncertain.
- Use signal primitives as reusable evidence transformations, not use-case labels.
- Do not infer sales, market size, or company revenue beyond the evidence boundary.
- Commands remain dispatch-only; skills own research contracts and outputs.
