---
name: sector
command: /sector
maps_to_skill: sector-analyst
thin_wrapper: true
---

<!-- GENERATED-SYNC: source=plugins/vertical-plugins/invest-research/commands/sector.md; kind=command; script=scripts/sync_invest_skills.py -->
> [!IMPORTANT]
> Generated execution artifact. Do not edit directly; edit the vertical source and rerun `python scripts/sync_invest_skills.py` (or `scripts/Sync-InvestSkills.ps1` / `scripts/Sync-InvestSkills.sh`).
> Common policies are synced from `plugins/vertical-plugins/invest-research/policies/`.
> Runtime output paths must use `${ACTIVE_WORKSPACE}`.
<!-- END GENERATED-SYNC -->


# /sector

Thin command stub for sector and industry research.

## Dispatch

- Resolve `${ACTIVE_WORKSPACE}`.
- Pass the sector, industry, geography hints, and `${ACTIVE_WORKSPACE}` to `sector-analyst`.
- Require `sector-analyst` to preserve its contracted output paths under `${ACTIVE_WORKSPACE}`.

## Prohibited

- Do not perform sector research, investment analysis, product analysis, peer ranking, or thesis synthesis inside this command.
- Do not write research artifacts directly except command dispatch metadata if a runtime requires it.
