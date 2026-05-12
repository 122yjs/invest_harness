---
name: earnings
command: /earnings
maps_to_skill: earnings-update
thin_wrapper: true
status: scaffold-only
---

# /earnings

Thin command stub for earnings update workflow.

## Dispatch

- Resolve `${ACTIVE_WORKSPACE}`.
- Pass the ticker/company, period selector, event hints, and `${ACTIVE_WORKSPACE}` to a future `earnings-update` skill.
- Record that detailed earnings workflow logic is deferred.

## Prohibited

- Do not fetch filings, calculate beat/miss, revise ratings, or summarize guidance inside this command.

