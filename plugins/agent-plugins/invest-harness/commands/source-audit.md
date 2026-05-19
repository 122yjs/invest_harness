---
name: source-audit
command: /source-audit
maps_to_skill: qa-reviewer
thin_wrapper: true
---

<!-- GENERATED-SYNC: source=plugins/vertical-plugins/invest-research/commands/source-audit.md; kind=command; script=scripts/sync_invest_skills.py -->
> [!IMPORTANT]
> Generated execution artifact. Do not edit directly; edit the vertical source and rerun python scripts/sync_invest_skills.py (or scripts/Sync-InvestSkills.ps1 / scripts/Sync-InvestSkills.sh).
> Common policies are synced from plugins/vertical-plugins/invest-research/policies/.
> Runtime output paths must use `${ACTIVE_WORKSPACE}`.
<!-- END GENERATED-SYNC -->


# /source-audit

Thin command stub for source and claim-boundary audit.

## Dispatch

- Resolve `${ACTIVE_WORKSPACE}` or accept an explicit report/workspace path.
- Pass the report path, `${ACTIVE_WORKSPACE}/00_evidence/source-validation.md`, and `${ACTIVE_WORKSPACE}` to `qa-reviewer`.
- Require `qa-reviewer` to include source/claim boundary findings in `${ACTIVE_WORKSPACE}/09_qa/review.md` and `${ACTIVE_WORKSPACE}/09_qa/fix-list.md`.

## Prohibited

- Do not perform QA inside this command.
- Do not fetch data or rewrite reports inside this command.
- Do not write research artifacts directly except command dispatch metadata if a runtime requires it.
