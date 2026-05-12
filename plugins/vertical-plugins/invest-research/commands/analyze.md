---
name: analyze
command: /analyze
maps_to_skill: invest-orchestrator
thin_wrapper: true
---

# /analyze

Thin command stub for full single-company analysis.

## Dispatch

- Resolve or create `${ACTIVE_WORKSPACE}` using the workspace safety policy.
- Pass the original user request and `${ACTIVE_WORKSPACE}` to `invest-orchestrator`.
- Let `invest-orchestrator` own input normalization, skill fan-out, synthesis, and QA.

## Prohibited

- Do not perform investment analysis inside this command.
- Do not write research artifacts directly except command dispatch metadata if a runtime requires it.

