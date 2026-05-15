<!-- GENERATED-SYNC: source=plugins/vertical-plugins/invest-research/templates/api-call-log.md; kind=template; script=scripts/Sync-InvestSkills.ps1 -->
> [!IMPORTANT]
> Generated execution artifact. Do not edit directly; edit the vertical source and rerun pwsh ./scripts/Sync-InvestSkills.ps1.
> Common policies are synced from plugins/vertical-plugins/invest-research/policies/.
> Runtime output paths must use `${ACTIVE_WORKSPACE}`.
<!-- END GENERATED-SYNC -->

# API Call Log

This template records source access for auditability. It does not require the
harness to implement API clients.

| Source ID | Source | Connection Status | Configured In | Endpoint/Tool | Parameters | Timestamp | Success/Failure | Response Summary | Cache Path | Error |
|---|---|---|---|---|---|---|---|---|---|---|
|  |  | connected / documented_only / planned / external_manual |  |  |  |  |  |  |  |  |

## Notes

- Redact secrets and never store API keys.
- Record official source IDs, MCP tool names, endpoint names, or filing accessions.
- If a source is not `connected`, record the missing tool/endpoint as a data gap rather than treating the call as completed.
- For manual web retrieval, use the URL or source document title in `Endpoint/Tool`.
