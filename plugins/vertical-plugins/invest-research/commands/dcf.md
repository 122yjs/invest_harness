---
name: dcf
command: /dcf
maps_to_skill: valuation-analyst
thin_wrapper: true
---

# /dcf

Thin command stub for DCF workflow entry.

## Dispatch

- Resolve `${ACTIVE_WORKSPACE}`.
- Pass the target, requested scenario scope, and `${ACTIVE_WORKSPACE}` to `valuation-analyst`.
- Let the skill check whether comps or market-price snapshot inputs exist.

## Prohibited

- Do not calculate DCF values, discount rates, terminal values, or price targets inside this command.

