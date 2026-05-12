---
name: preview
command: /preview
maps_to_skill: earnings-preview
thin_wrapper: true
---

# /preview

Thin command stub for earnings preview workflow.

## Dispatch

- Resolve `${ACTIVE_WORKSPACE}`.
- Pass the ticker/company, upcoming period hints, and `${ACTIVE_WORKSPACE}` to `earnings-preview`.
- Require `earnings-preview` to preserve its contracted output paths under `${ACTIVE_WORKSPACE}`.

## Prohibited

- Do not perform earnings preview, investment analysis, product analysis, scenario analysis, or guidance summary inside this command.
- Do not write research artifacts directly except command dispatch metadata if a runtime requires it.
