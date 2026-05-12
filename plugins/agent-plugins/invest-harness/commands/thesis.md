---
name: thesis
command: /thesis
maps_to_skill: thesis-tracker
thin_wrapper: true
---

<!-- GENERATED-SYNC: source=plugins/vertical-plugins/invest-research/commands/thesis.md; kind=command; script=scripts/Sync-InvestSkills.ps1 -->
> [!IMPORTANT]
> Generated execution artifact. Do not edit directly; edit the vertical source and rerun pwsh ./scripts/Sync-InvestSkills.ps1.
> Common policies are synced from plugins/vertical-plugins/invest-research/policies/.
> Runtime output paths must use `${ACTIVE_WORKSPACE}`.
<!-- END GENERATED-SYNC -->


# /thesis

Thin command stub for investment thesis tracking.

## Dispatch

- Resolve `${ACTIVE_WORKSPACE}`.
- Pass the ticker/company, thesis context, tracking window, and `${ACTIVE_WORKSPACE}` to `thesis-tracker`.
- Require `thesis-tracker` to preserve its contracted output paths under `${ACTIVE_WORKSPACE}`.

## Prohibited

- Do not perform thesis review, investment analysis, product analysis, evidence scoring, or rating-change judgment inside this command.
- Do not write research artifacts directly except command dispatch metadata if a runtime requires it.
