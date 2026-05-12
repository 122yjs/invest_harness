---
name: dcf
command: /dcf
maps_to_skill: valuation-analyst
thin_wrapper: true
---

<!-- GENERATED-SYNC: source=plugins/vertical-plugins/invest-research/commands/dcf.md; kind=command; script=scripts/Sync-InvestSkills.ps1 -->
> [!IMPORTANT]
> Generated execution artifact. Do not edit directly; edit the vertical source and rerun pwsh ./scripts/Sync-InvestSkills.ps1.
> Common policies are synced from plugins/vertical-plugins/invest-research/policies/.
> Runtime output paths must use `${ACTIVE_WORKSPACE}`.
<!-- END GENERATED-SYNC -->


# /dcf

Thin command stub for DCF workflow entry.

## Dispatch

- Resolve `${ACTIVE_WORKSPACE}`.
- Pass the target, requested scenario scope, and `${ACTIVE_WORKSPACE}` to `valuation-analyst`.
- Let the skill check whether `${ACTIVE_WORKSPACE}/03_valuation/comps.md` and `${ACTIVE_WORKSPACE}/00_input/market-price-snapshot.md` exist.
- Require the skill to write DCF output to `${ACTIVE_WORKSPACE}/03_valuation/dcf.md`.

## Prohibited

- Do not calculate DCF values, discount rates, terminal values, or price targets inside this command.
