---
name: sector
command: /sector
maps_to_skill: sector-analyst
thin_wrapper: true
---

# /sector

Thin command stub for sector and industry research.

## Dispatch

- Resolve `${ACTIVE_WORKSPACE}`.
- Pass the sector, industry, geography hints, and `${ACTIVE_WORKSPACE}` to `sector-analyst`.
- Require `sector-analyst` to preserve its contracted output paths under `${ACTIVE_WORKSPACE}`.

## Prohibited

- Do not perform sector research, investment analysis, product analysis, peer ranking, or thesis synthesis inside this command.
- Do not write research artifacts directly except command dispatch metadata if a runtime requires it.
