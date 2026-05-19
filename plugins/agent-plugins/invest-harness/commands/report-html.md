---
name: report-html
command: /report-html
maps_to_skill: html-report-synthesizer
thin_wrapper: true
---

<!-- GENERATED-SYNC: source=plugins/vertical-plugins/invest-research/commands/report-html.md; kind=command; script=scripts/sync_invest_skills.py -->
> [!IMPORTANT]
> Generated execution artifact. Do not edit directly; edit the vertical source and rerun `python scripts/sync_invest_skills.py` (or `scripts/Sync-InvestSkills.ps1` / `scripts/Sync-InvestSkills.sh`).
> Common policies are synced from `plugins/vertical-plugins/invest-research/policies/`.
> Runtime output paths must use `${ACTIVE_WORKSPACE}`.
<!-- END GENERATED-SYNC -->


# /report-html

Thin command stub for HTML report synthesis.

## Dispatch

- Resolve `${ACTIVE_WORKSPACE}`.
- Pass the report target, source workspace inputs, and `${ACTIVE_WORKSPACE}` to `html-report-synthesizer`.
- Require `html-report-synthesizer` to preserve its contracted output paths under `${ACTIVE_WORKSPACE}`.

## Prohibited

- Do not perform report synthesis, investment analysis, product analysis, valuation review, or HTML content drafting inside this command.
- Do not write research artifacts directly except command dispatch metadata if a runtime requires it.
