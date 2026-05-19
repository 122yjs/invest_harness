<!-- GENERATED-SYNC: source=plugins/vertical-plugins/invest-research/policies/qa-recalculation-policy.md; kind=policy; script=scripts/sync_invest_skills.py -->
> [!IMPORTANT]
> Generated execution artifact. Do not edit directly; edit the vertical source and rerun `python scripts/sync_invest_skills.py` (or `scripts/Sync-InvestSkills.ps1` / `scripts/Sync-InvestSkills.sh`).
> Common policies are synced from plugins/vertical-plugins/invest-research/policies/.
> Runtime output paths must use `${ACTIVE_WORKSPACE}`.
<!-- END GENERATED-SYNC -->

# QA Recalculation Policy

## Purpose

QA must verify that market metrics and valuation outputs are arithmetically consistent with the market-price snapshot and stated financial inputs.

## Required Recalculations

QA should recalculate, when inputs are present:

- market capitalization = reference price x diluted shares outstanding
- PER = reference price / EPS
- PBR = reference price / BPS
- EV = market capitalization + net debt
- EV/EBITDA = EV / EBITDA
- FCF yield = free cash flow / market capitalization
- DCF discount or premium = DCF per-share value / reference price - 1
- implied upside or downside = price target / reference price - 1

## Failure Handling

If the report value differs from the recalculated value beyond the stated tolerance, QA must flag the item and identify the likely cause:

- stale price
- mismatched share count
- currency mismatch
- fiscal-period mismatch
- reported versus adjusted metric mismatch
- missing source

## Output

QA findings belong under `${ACTIVE_WORKSPACE}/09_qa/`:

- `${ACTIVE_WORKSPACE}/09_qa/review.md`
- `${ACTIVE_WORKSPACE}/09_qa/fix-list.md`
- `${ACTIVE_WORKSPACE}/09_qa/final-check.md`

QA must explicitly state whether each recalculation passed, failed, or could not run because required inputs were missing.
