---
name: earnings
command: /earnings
maps_to_skill: earnings-update
thin_wrapper: true
---

# /earnings

Thin command stub for earnings update workflow.

## Dispatch

- Resolve `${ACTIVE_WORKSPACE}`.
- Pass the ticker/company, period selector, event hints, and `${ACTIVE_WORKSPACE}` to `earnings-update`.
- Require `earnings-update` to write `${ACTIVE_WORKSPACE}/00_input/earnings-update.md`.

## Prohibited

- Do not fetch filings, calculate beat/miss, revise ratings, or summarize guidance inside this command.
