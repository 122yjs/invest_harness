---
name: qa
command: /qa
maps_to_skill: qa-reviewer
thin_wrapper: true
---

<!-- GENERATED-SYNC: source=plugins/vertical-plugins/invest-research/commands/qa.md; kind=command; script=scripts/sync_invest_skills.py -->
> [!IMPORTANT]
> Generated execution artifact. Do not edit directly; edit the vertical source and rerun `python scripts/sync_invest_skills.py` (or `scripts/Sync-InvestSkills.ps1` / `scripts/Sync-InvestSkills.sh`).
> Common policies are synced from plugins/vertical-plugins/invest-research/policies/.
> Runtime output paths must use `${ACTIVE_WORKSPACE}`.
<!-- END GENERATED-SYNC -->


# /qa

Thin command stub for QA review.

## Dispatch

- Resolve `${ACTIVE_WORKSPACE}` or accept an explicit report path.
- Pass the report path, source workspace, and `${ACTIVE_WORKSPACE}` to `qa-reviewer`.
- Let `qa-reviewer` own recalculation checks, rating consistency checks, and QA outputs under `${ACTIVE_WORKSPACE}/09_qa/`.

## Prohibited

- Do not perform recalculation, source validation, or rating consistency review inside this command.
