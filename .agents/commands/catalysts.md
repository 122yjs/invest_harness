---
name: catalysts
command: /catalysts
maps_to_skill: catalyst-tracker
thin_wrapper: true
---

<!-- GENERATED-SYNC: source=plugins/vertical-plugins/invest-research/commands/catalysts.md; kind=command; script=scripts/sync_invest_skills.py -->
> [!IMPORTANT]
> Generated execution artifact. Do not edit directly; edit the vertical source and rerun `python scripts/sync_invest_skills.py` (or `scripts/Sync-InvestSkills.ps1` / `scripts/Sync-InvestSkills.sh`).
> Common policies are synced from `plugins/vertical-plugins/invest-research/policies/`.
> Runtime output paths must use `${ACTIVE_WORKSPACE}`.
<!-- END GENERATED-SYNC -->


# /catalysts

Thin command stub for catalyst tracking.

## Dispatch

- Resolve `${ACTIVE_WORKSPACE}`.
- Pass the company, theme, time window, event hints, and `${ACTIVE_WORKSPACE}` to `catalyst-tracker`.
- Require `catalyst-tracker` to preserve its contracted output paths under `${ACTIVE_WORKSPACE}`.

## Prohibited

- Do not perform catalyst research, investment analysis, product analysis, event scoring, or calendar synthesis inside this command.
- Do not write research artifacts directly except command dispatch metadata if a runtime requires it.
