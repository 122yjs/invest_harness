<!-- GENERATED-SYNC: source=plugins/vertical-plugins/invest-research/templates/market-price-snapshot.md; kind=template; script=scripts/sync_invest_skills.py -->
> [!IMPORTANT]
> Generated execution artifact. Do not edit directly; edit the vertical source and rerun `python scripts/sync_invest_skills.py` (or `scripts/Sync-InvestSkills.ps1` / `scripts/Sync-InvestSkills.sh`).
> Common policies are synced from plugins/vertical-plugins/invest-research/policies/.
> Runtime output paths must use `${ACTIVE_WORKSPACE}`.
<!-- END GENERATED-SYNC -->

# Market Price Snapshot

| Field | Value |
|---|---|
| Active workspace | `${ACTIVE_WORKSPACE}` |
| Company |  |
| Ticker |  |
| Exchange / Country |  |
| Trading currency |  |
| Reference price |  |
| Reference price date |  |
| Price source |  |
| Retrieval timestamp |  |
| Shares outstanding |  |
| Shares source |  |
| Market capitalization |  |
| Net debt / net cash |  |
| Enterprise value |  |
| EPS basis |  |
| BPS basis |  |
| EBITDA basis |  |
| FCF basis |  |

## Calculation Basis

| Metric | Formula | Inputs Used | Result |
|---|---|---|---|
| Market capitalization | Reference price x shares outstanding |  |  |
| PER | Reference price / EPS |  |  |
| PBR | Reference price / BPS |  |  |
| EV | Market capitalization + net debt |  |  |
| EV/EBITDA | EV / EBITDA |  |  |
| FCF yield | FCF / market capitalization |  |  |

## Fallbacks and Notes

- Primary market-data source:
- Fallback source, if any:
- Reason for fallback:
- Currency or fiscal-period adjustments:

