param(
    [string]$EnvPath = (Join-Path (Resolve-Path (Join-Path $PSScriptRoot '..\..')) '.env')
)

$ErrorActionPreference = 'Stop'

& (Join-Path $PSScriptRoot 'Start-McpServer.ps1') `
    -ServerName 'korea-stock' `
    -CommandEnvVar 'INVEST_HARNESS_KOREA_STOCK_MCP_COMMAND' `
    -DefaultCommand 'korea-stock-mcp' `
    -ArgumentsEnvVar 'INVEST_HARNESS_KOREA_STOCK_MCP_ARGS' `
    -RequiredVariables @('DART_API_KEY', 'KRX_API_KEY') `
    -EnvPath $EnvPath
