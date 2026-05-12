---
name: catalysts
command: /catalysts
maps_to_skill: catalyst-tracker
thin_wrapper: true
---

# /catalysts

Thin command stub for catalyst tracking.

## Dispatch

- Resolve `${ACTIVE_WORKSPACE}`.
- Pass the company, theme, time window, event hints, and `${ACTIVE_WORKSPACE}` to `catalyst-tracker`.
- Require `catalyst-tracker` to preserve its contracted output paths under `${ACTIVE_WORKSPACE}`.

## Prohibited

- Do not perform catalyst research, investment analysis, product analysis, event scoring, or calendar synthesis inside this command.
- Do not write research artifacts directly except command dispatch metadata if a runtime requires it.
