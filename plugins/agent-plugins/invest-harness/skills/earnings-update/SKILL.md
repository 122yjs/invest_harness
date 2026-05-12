---
name: earnings-update
description: Scaffold-only skill target for future earnings update workflows; command stubs may route here but first-pass infrastructure must not implement earnings analysis logic.
---

<!-- GENERATED-SYNC: source=plugins/vertical-plugins/invest-research/skills/earnings-update/SKILL.md; kind=skill; script=scripts/Sync-InvestSkills.ps1 -->
> [!IMPORTANT]
> Generated execution artifact. Do not edit directly; edit the vertical source and rerun pwsh ./scripts/Sync-InvestSkills.ps1.
> Common policies are synced from plugins/vertical-plugins/invest-research/policies/.
> Runtime output paths must use `${ACTIVE_WORKSPACE}`.
<!-- END GENERATED-SYNC -->


# earnings-update

## Status

This is a first-pass scaffold so `/earnings` has a real skill target.

## Boundary

- Use `${ACTIVE_WORKSPACE}` for any future output path.
- Do not fetch filings, calculate beat/miss, revise ratings, or summarize guidance in the infrastructure-freeze pass.
- Future implementation should write earnings artifacts under `${ACTIVE_WORKSPACE}/00_input/` or a dedicated dynamic workspace subfolder defined by the next pass.

## Deferred Workflow

The actual earnings update workflow is deferred to the next product-logic pass.

