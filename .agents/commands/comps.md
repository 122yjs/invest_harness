---
name: comps
command: /comps
maps_to_skill: valuation-analyst
thin_wrapper: true
---

<!-- GENERATED-SYNC: source=plugins/vertical-plugins/invest-research/commands/comps.md; kind=command; script=scripts/Sync-InvestSkills.ps1 -->
> [!IMPORTANT]
> Generated execution artifact. Do not edit directly; edit the vertical source and rerun pwsh ./scripts/Sync-InvestSkills.ps1.
> Common policies are synced from plugins/vertical-plugins/invest-research/policies/.
> Runtime output paths must use `${ACTIVE_WORKSPACE}`.
<!-- END GENERATED-SYNC -->


# /comps

Thin command stub for comparable-company analysis.

## Dispatch

- Resolve `${ACTIVE_WORKSPACE}`.
- Pass the company identifier, peer hints, and `${ACTIVE_WORKSPACE}` to `valuation-analyst`.
- Require the skill to write any future comps output under `${ACTIVE_WORKSPACE}`.

## Prohibited

- Do not select peers, compute multiples, or draw valuation conclusions inside this command.

