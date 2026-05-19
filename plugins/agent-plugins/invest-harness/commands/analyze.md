---
name: analyze
command: /analyze
maps_to_skill: invest-orchestrator
thin_wrapper: true
---

<!-- GENERATED-SYNC: source=plugins/vertical-plugins/invest-research/commands/analyze.md; kind=command; script=scripts/sync_invest_skills.py -->
> [!IMPORTANT]
> Generated execution artifact. Do not edit directly; edit the vertical source and rerun python scripts/sync_invest_skills.py (or scripts/Sync-InvestSkills.ps1 / scripts/Sync-InvestSkills.sh).
> Common policies are synced from plugins/vertical-plugins/invest-research/policies/.
> Runtime output paths must use `${ACTIVE_WORKSPACE}`.
<!-- END GENERATED-SYNC -->


# /analyze

Thin command stub for full single-company analysis.

## Dispatch

- Resolve or create `${ACTIVE_WORKSPACE}` using the workspace safety policy.
- Pass the original user request and `${ACTIVE_WORKSPACE}` to `invest-orchestrator`.
- Let `invest-orchestrator` own input normalization, skill fan-out, synthesis, and QA.

## Prohibited

- Do not perform investment analysis inside this command.
- Do not write research artifacts directly except command dispatch metadata if a runtime requires it.

