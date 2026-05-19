---
name: market-intel
command: /market-intel
maps_to_skill: evidence-planner
thin_wrapper: true
---

<!-- GENERATED-SYNC: source=plugins/vertical-plugins/invest-research/commands/market-intel.md; kind=command; script=scripts/sync_invest_skills.py -->
> [!IMPORTANT]
> Generated execution artifact. Do not edit directly; edit the vertical source and rerun `python scripts/sync_invest_skills.py` (or `scripts/Sync-InvestSkills.ps1` / `scripts/Sync-InvestSkills.sh`).
> Common policies are synced from `plugins/vertical-plugins/invest-research/policies/`.
> Runtime output paths must use `${ACTIVE_WORKSPACE}`.
<!-- END GENERATED-SYNC -->


# /market-intel

Thin command stub for evidence planning plus source routing.

## Dispatch

- Resolve or create `${ACTIVE_WORKSPACE}` using the workspace safety policy.
- Pass the market intelligence prompt and `${ACTIVE_WORKSPACE}` to `evidence-planner`.
- Handoff from `evidence-planner` to `source-router` and optional `signal-analyst` should preserve `${ACTIVE_WORKSPACE}/00_evidence/` contracts.
- Expected outputs include `${ACTIVE_WORKSPACE}/00_evidence/evidence-plan.md`, `${ACTIVE_WORKSPACE}/00_evidence/source-call-plan.md`, and `${ACTIVE_WORKSPACE}/00_evidence/signal-cards.md`.

## Prohibited

- Do not implement market data retrieval in the command wrapper.
- Do not compute signal values inside the command wrapper.
- Do not write research artifacts directly except command dispatch metadata if a runtime requires it.
