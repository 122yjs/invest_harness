<!-- GENERATED-SYNC: source=plugins/vertical-plugins/invest-research/templates/source-validation.md; kind=template; script=scripts/sync_invest_skills.py -->
> [!IMPORTANT]
> Generated execution artifact. Do not edit directly; edit the vertical source and rerun python scripts/sync_invest_skills.py (or scripts/Sync-InvestSkills.ps1 / scripts/Sync-InvestSkills.sh).
> Common policies are synced from plugins/vertical-plugins/invest-research/policies/.
> Runtime output paths must use `${ACTIVE_WORKSPACE}`.
<!-- END GENERATED-SYNC -->

# Source Validation

## Validation Status

| Gate | Status | Evidence IDs | Notes |
|---|---|---|---|
| relative_index_gate | pass / fail / review |  |  |
| official_statistics_gate | pass / fail / review |  |  |
| trade_data_gate | pass / fail / review |  |  |
| company_disclosure_gate | pass / fail / review |  |  |
| procurement_gate | pass / fail / review |  |  |
| market_context_gate | pass / fail / review |  |  |
| valuation_gate | pass / fail / review |  |  |
| source_conflict_gate | pass / fail / review |  |  |

## Source Availability Checks

| Source ID | Connection Status | Configured In | Available Tools/Endpoints | Missing Tool/Data Gap | Fallback |
|---|---|---|---|---|---|
|  | connected / documented_only / planned / external_manual |  |  |  |  |

## Web Body Retrieval Checks

| Evidence ID | Candidate URL | Search Snippet Used? | Full Body Retrieved? | Body Type | Publication Date Check | Retrieval Timestamp | Status |
|---|---|---|---|---|---|---|---|
|  |  | no / yes | yes / no | article / document / PDF / page | pass / fail / review |  | pass / fail / review |

Snippet-only evidence fails validation. If the article, document, or PDF body
cannot be fetched or read, record an unresolved data gap before analyst fan-out.

## Missing Data

| Missing Item | Impact | Follow-up |
|---|---|---|
|  |  |  |

## Unit/Date Checks

| Evidence ID | Unit Check | Date Check | Period Check |
|---|---|---|---|
|  |  |  |  |

## Source Conflicts

| Claim | Source A | Source B | Conflict | Resolution |
|---|---|---|---|---|
|  |  |  |  |  |

## Relative vs Absolute Checks

| Evidence ID | Relative or Absolute | Claim Boundary | Pass/Fail |
|---|---|---|---|
|  |  |  |  |

## Forbidden Claim Checks

| Claim | Forbidden Pattern | Status | Fix |
|---|---|---|---|
|  |  | pass / fail / review |  |

## Unresolved Data Gaps

- 
