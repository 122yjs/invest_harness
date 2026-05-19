---
name: comps
command: /comps
maps_to_skill: valuation-analyst
thin_wrapper: true
---

<!-- GENERATED-SYNC: source=plugins/vertical-plugins/invest-research/commands/comps.md; kind=command; script=scripts/sync_invest_skills.py -->
> [!IMPORTANT]
> Generated execution artifact. Do not edit directly; edit the vertical source and rerun `python scripts/sync_invest_skills.py` (or `scripts/Sync-InvestSkills.ps1` / `scripts/Sync-InvestSkills.sh`).
> Common policies are synced from `plugins/vertical-plugins/invest-research/policies/`.
> Runtime output paths must use `${ACTIVE_WORKSPACE}`.
<!-- END GENERATED-SYNC -->


# /comps

Thin command stub for comparable-company analysis.

## Dispatch

- Resolve `${ACTIVE_WORKSPACE}`.
- Pass the company identifier, peer hints, and `${ACTIVE_WORKSPACE}` to `valuation-analyst`.
- Require the skill to write comparable-company output to `${ACTIVE_WORKSPACE}/03_valuation/comps.md`.

## Prohibited

- Do not select peers, compute multiples, or draw valuation conclusions inside this command.
