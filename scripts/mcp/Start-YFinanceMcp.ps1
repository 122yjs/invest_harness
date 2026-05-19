param(
    [string]$EnvPath = (Join-Path (Resolve-Path (Join-Path $PSScriptRoot '..\..')) '.env')
)

$ErrorActionPreference = 'Stop'

& (Join-Path $PSScriptRoot 'Start-McpServer.ps1') `
    -ServerName 'yfinance' `
    -CommandEnvVar 'INVEST_HARNESS_YFINANCE_MCP_COMMAND' `
    -DefaultCommand 'yfinance-mcp' `
    -ArgumentsEnvVar 'INVEST_HARNESS_YFINANCE_MCP_ARGS' `
    -RequiredVariables @() `
    -EnvPath $EnvPath
