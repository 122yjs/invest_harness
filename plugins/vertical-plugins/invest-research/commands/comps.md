---
name: comps
command: /comps
maps_to_skill: valuation-analyst
thin_wrapper: true
---

# /comps

Thin command stub for comparable-company analysis.

## Dispatch

- Resolve `${ACTIVE_WORKSPACE}`.
- Pass the company identifier, peer hints, and `${ACTIVE_WORKSPACE}` to `valuation-analyst`.
- Require the skill to write any future comps output under `${ACTIVE_WORKSPACE}`.

## Prohibited

- Do not select peers, compute multiples, or draw valuation conclusions inside this command.

