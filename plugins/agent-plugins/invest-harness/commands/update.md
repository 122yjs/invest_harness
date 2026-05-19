---
name: update
command: /update
maps_to_skill: report-updater
thin_wrapper: true
---

<!-- GENERATED-SYNC: source=plugins/vertical-plugins/invest-research/commands/update.md; kind=command; script=scripts/sync_invest_skills.py -->
> [!IMPORTANT]
> Generated execution artifact. Do not edit directly; edit the vertical source and rerun `python scripts/sync_invest_skills.py` (or `scripts/Sync-InvestSkills.ps1` / `scripts/Sync-InvestSkills.sh`).
> Common policies are synced from `plugins/vertical-plugins/invest-research/policies/`.
> Runtime output paths must use `${ACTIVE_WORKSPACE}`.
<!-- END GENERATED-SYNC -->


# /update

Thin command stub for report update workflow.

## Dispatch

- Resolve `${ACTIVE_WORKSPACE}`.
- Pass the report target, update scope, event hints, and `${ACTIVE_WORKSPACE}` to `report-updater`.
- Require `report-updater` to preserve its contracted output paths under `${ACTIVE_WORKSPACE}`.

## Prohibited

- Do not perform report updates, investment analysis, product analysis, source refresh, or rating-change judgment inside this command.
- Do not write research artifacts directly except command dispatch metadata if a runtime requires it.
