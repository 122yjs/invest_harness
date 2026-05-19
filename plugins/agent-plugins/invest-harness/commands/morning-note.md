---
name: morning-note
command: /morning-note
maps_to_skill: morning-note
thin_wrapper: true
---

<!-- GENERATED-SYNC: source=plugins/vertical-plugins/invest-research/commands/morning-note.md; kind=command; script=scripts/sync_invest_skills.py -->
> [!IMPORTANT]
> Generated execution artifact. Do not edit directly; edit the vertical source and rerun `python scripts/sync_invest_skills.py` (or `scripts/Sync-InvestSkills.ps1` / `scripts/Sync-InvestSkills.sh`).
> Common policies are synced from `plugins/vertical-plugins/invest-research/policies/`.
> Runtime output paths must use `${ACTIVE_WORKSPACE}`.
<!-- END GENERATED-SYNC -->


# /morning-note

Thin command stub for morning note workflow.

## Dispatch

- Resolve `${ACTIVE_WORKSPACE}`.
- Pass the watchlist, theme, date context, and `${ACTIVE_WORKSPACE}` to `morning-note`.
- Require `morning-note` to preserve its contracted output paths under `${ACTIVE_WORKSPACE}`.

## Prohibited

- Do not perform market summary, investment analysis, product analysis, watchlist triage, or note drafting inside this command.
- Do not write research artifacts directly except command dispatch metadata if a runtime requires it.
