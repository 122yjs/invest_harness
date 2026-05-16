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
- For Web Search + Web Fetch retrieval, log the search query separately from the fetched URL. Search snippets are discovery metadata only; evidence requires the fetched article, document, or PDF body.
