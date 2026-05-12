---
name: qa
command: /qa
maps_to_skill: qa-reviewer
thin_wrapper: true
---

# /qa

Thin command stub for QA review.

## Dispatch

- Resolve `${ACTIVE_WORKSPACE}` or accept an explicit report path.
- Pass the report path, source workspace, and `${ACTIVE_WORKSPACE}` to `qa-reviewer`.
- Let `qa-reviewer` own recalculation checks and final review output.

## Prohibited

- Do not perform recalculation, source validation, or rating consistency review inside this command.

