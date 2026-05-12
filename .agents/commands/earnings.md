---
name: earnings
command: /earnings
maps_to_skill: earnings-update
thin_wrapper: true
status: scaffold-only
---

<!-- GENERATED-SYNC: source=plugins/vertical-plugins/invest-research/commands/earnings.md; kind=command; script=scripts/Sync-InvestSkills.ps1 -->
> [!IMPORTANT]
> Generated execution artifact. Do not edit directly; edit the vertical source and rerun pwsh ./scripts/Sync-InvestSkills.ps1.
> Common policies are synced from plugins/vertical-plugins/invest-research/policies/.
> Runtime output paths must use `${ACTIVE_WORKSPACE}`.
<!-- END GENERATED-SYNC -->


# /earnings

Thin command stub for earnings update workflow.

## Dispatch

- Resolve `${ACTIVE_WORKSPACE}`.
- Pass the ticker/company, period selector, event hints, and `${ACTIVE_WORKSPACE}` to a future `earnings-update` skill.
- Record that detailed earnings workflow logic is deferred.

## Prohibited

- Do not fetch filings, calculate beat/miss, revise ratings, or summarize guidance inside this command.

