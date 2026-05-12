---
name: preview
command: /preview
maps_to_skill: earnings-preview
thin_wrapper: true
---

<!-- GENERATED-SYNC: source=plugins/vertical-plugins/invest-research/commands/preview.md; kind=command; script=scripts/Sync-InvestSkills.ps1 -->
> [!IMPORTANT]
> Generated execution artifact. Do not edit directly; edit the vertical source and rerun pwsh ./scripts/Sync-InvestSkills.ps1.
> Common policies are synced from plugins/vertical-plugins/invest-research/policies/.
> Runtime output paths must use `${ACTIVE_WORKSPACE}`.
<!-- END GENERATED-SYNC -->


# /preview

Thin command stub for earnings preview workflow.

## Dispatch

- Resolve `${ACTIVE_WORKSPACE}`.
- Pass the ticker/company, upcoming period hints, and `${ACTIVE_WORKSPACE}` to `earnings-preview`.
- Require `earnings-preview` to preserve its contracted output paths under `${ACTIVE_WORKSPACE}`.

## Prohibited

- Do not perform earnings preview, investment analysis, product analysis, scenario analysis, or guidance summary inside this command.
- Do not write research artifacts directly except command dispatch metadata if a runtime requires it.
