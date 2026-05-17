# Set-Credentials.ps1
# This script persistently registers all data source credentials as Windows User environment variables.
# Running this script will make these variables available across all command prompts, PowerShell windows, and tools.

Write-Output "Setting user environment variables..."

$variables = @{
    "DART_API_KEY"           = "881e0ed28247a3477bc873e373632b32772590dc"
    "KRX_API_KEY"            = "FD8CBA2AC84D4FC69590C2BD30EDE21D2CE516ED"
    "FRED_API_KEY"           = "9893311efe17b7ccf95bd8dc0a177c9f"
    "ALPHA_VANTAGE_API_KEY"  = "JVCDWACTBJAEF1FZ"
    "FMP_API_KEY"            = "6Wcc5OifTGxVTGMDP2iaAXSAobkgPRVU"
    "KOSIS_API_KEY"          = "MDI1MTE1M2M1ODM5OGFjMTkwYzBjYTkzOTM1ZGM0NTM="
    "CUSTOMS_TRADE_API_KEY"  = "75f45895e8888abd20b41c1342b8034c58ed64a6d6889f66a357b3e6094d003b"
    "CUSTOMS_TRADE_FORMAT"   = "XML"
    "CUSTOMS_TRADE_ENDPOINT" = "https://apis.data.go.kr/1220000/nitemtrade"
}

foreach ($var in $variables.GetEnumerator()) {
    [Environment]::SetEnvironmentVariable($var.Key, $var.Value, "User")
    Write-Output "Successfully set User Environment Variable: $($var.Key)"
}

Write-Output "All credentials registered successfully! Please restart your terminal/IDE for changes to take effect."
