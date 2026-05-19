<!-- GENERATED-SYNC: source=plugins/vertical-plugins/invest-research/templates/source-call-plan.md; kind=template; script=scripts/sync_invest_skills.py -->
> [!IMPORTANT]
> Generated execution artifact. Do not edit directly; edit the vertical source and rerun `python scripts/sync_invest_skills.py` (or `scripts/Sync-InvestSkills.ps1` / `scripts/Sync-InvestSkills.sh`).
> Common policies are synced from `plugins/vertical-plugins/invest-research/policies/`.
> Runtime output paths must use `${ACTIVE_WORKSPACE}`.
<!-- END GENERATED-SYNC -->

# Source Call Plan

## Source Selection Summary

| Evidence Type | Source ID | Candidate Source | Trust Tier | Connection Status | Runtime Availability | Live Tool Probe | Configured In | Available Tools/Endpoints | Reason Selected | Fallback Sources | Source Limitations | Missing Tool/Data Gap |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|  |  |  | T0 / T1 / T2 / T3 | connected / documented_only / planned / external_manual | available / unavailable / not checked | mcporter/tool inventory/check result |  |  |  |  |  |  |

## Planned Calls

| Evidence Type | Source ID | Tool/Endpoint | Trust Tier | Connection Status | Runtime Availability | Required Parameters | Expected Output | Validation Checks |
|---|---|---|---|---|---|---|---|---|
|  |  |  | T0 / T1 / T2 / T3 | connected / documented_only / planned / external_manual | available / unavailable / not checked |  |  |  |

## Web Search + Fetch Plan

| Evidence Type | Search Query | Candidate URL | Fetch/Reader Tool | Body Retrieved | Body Type | Snippet-Only? | Validation Checks | Data Gap If Fetch Fails |
|---|---|---|---|---|---|---|---|---|
|  |  |  | web_fetch / browser / PDF reader | yes / no / pending | article / document / PDF / page | yes / no |  |  |

Rule: Search finds links; Fetch reads article, document, or PDF body. Do not use
summary snippets as primary evidence.

## Claim Boundaries

| Source | Allowed Claims | Forbidden Claims | Required Caveats |
|---|---|---|---|
|  |  |  |  |

## Unavailable Source Handling

| Source ID | Missing Tool/Endpoint | Affected Evidence Type | Fallback Source | Data Gap |
|---|---|---|---|---|
|  |  |  |  |  |

Rule: `Connection Status` is repo-evidence status, not live runtime proof.
Before analyst fan-out, record runtime source availability separately. If a
source such as yfinance is documented but not callable in the live session,
mark it unavailable, select a fallback, and preserve the limitation as a data
gap.

Rule: `Trust Tier` controls evidence priority. Use T0 company official and
regulator disclosure before T2 vendor snapshots for reported financials,
guidance, issuer identity, share count, risk factors, and segment data.
