---
name: update
command: /update
maps_to_skill: report-updater
thin_wrapper: true
---

# /update

Thin command stub for report update workflow.

## Dispatch

- Resolve `${ACTIVE_WORKSPACE}`.
- Pass the report target, update scope, event hints, and `${ACTIVE_WORKSPACE}` to `report-updater`.
- Require `report-updater` to preserve its contracted output paths under `${ACTIVE_WORKSPACE}`.

## Prohibited

- Do not perform report updates, investment analysis, product analysis, source refresh, or rating-change judgment inside this command.
- Do not write research artifacts directly except command dispatch metadata if a runtime requires it.
