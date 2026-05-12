---
name: thesis
command: /thesis
maps_to_skill: thesis-tracker
thin_wrapper: true
---

# /thesis

Thin command stub for investment thesis tracking.

## Dispatch

- Resolve `${ACTIVE_WORKSPACE}`.
- Pass the ticker/company, thesis context, tracking window, and `${ACTIVE_WORKSPACE}` to `thesis-tracker`.
- Require `thesis-tracker` to preserve its contracted output paths under `${ACTIVE_WORKSPACE}`.

## Prohibited

- Do not perform thesis review, investment analysis, product analysis, evidence scoring, or rating-change judgment inside this command.
- Do not write research artifacts directly except command dispatch metadata if a runtime requires it.
