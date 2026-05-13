---
name: evidence
command: /evidence
maps_to_skill: evidence-planner
thin_wrapper: true
---

# /evidence

Thin command stub for evidence planning.

## Dispatch

- Resolve or create `${ACTIVE_WORKSPACE}` using the workspace safety policy.
- Pass the original user request, `${ACTIVE_WORKSPACE}/00_input/input-intake.md` if present, and `${ACTIVE_WORKSPACE}` to `evidence-planner`.
- Require `evidence-planner` to write `${ACTIVE_WORKSPACE}/00_evidence/question-decomposition.md` and `${ACTIVE_WORKSPACE}/00_evidence/evidence-plan.md`.

## Prohibited

- Do not fetch source data inside this command.
- Do not classify the request into a fixed product or use-case router category.
- Do not write research artifacts directly except command dispatch metadata if a runtime requires it.
