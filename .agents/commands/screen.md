---
name: screen
command: /screen
maps_to_skill: idea-screener
thin_wrapper: true
---

<!-- GENERATED-SYNC: source=plugins/vertical-plugins/invest-research/commands/screen.md; kind=command; script=scripts/sync_invest_skills.py -->
> [!IMPORTANT]
> Generated execution artifact. Do not edit directly; edit the vertical source and rerun python scripts/sync_invest_skills.py (or scripts/Sync-InvestSkills.ps1 / scripts/Sync-InvestSkills.sh).
> Common policies are synced from plugins/vertical-plugins/invest-research/policies/.
> Runtime output paths must use `${ACTIVE_WORKSPACE}`.
<!-- END GENERATED-SYNC -->


# /screen

Thin command stub for idea screening.

## Dispatch

- Resolve or create `${ACTIVE_WORKSPACE}` using the workspace safety policy.
- Pass the screen prompt, constraints, market scope, and `${ACTIVE_WORKSPACE}` to `idea-screener`.
- Require `idea-screener` to write screening outputs under `${ACTIVE_WORKSPACE}/00_screen/`.

## Prohibited

- Do not rank stocks, calculate scores, or generate investment theses inside this command.
- Do not implement screening logic in the command wrapper.
