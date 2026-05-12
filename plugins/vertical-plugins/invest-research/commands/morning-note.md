---
name: morning-note
command: /morning-note
maps_to_skill: morning-note
thin_wrapper: true
---

# /morning-note

Thin command stub for morning note workflow.

## Dispatch

- Resolve `${ACTIVE_WORKSPACE}`.
- Pass the watchlist, theme, date context, and `${ACTIVE_WORKSPACE}` to `morning-note`.
- Require `morning-note` to preserve its contracted output paths under `${ACTIVE_WORKSPACE}`.

## Prohibited

- Do not perform market summary, investment analysis, product analysis, watchlist triage, or note drafting inside this command.
- Do not write research artifacts directly except command dispatch metadata if a runtime requires it.
