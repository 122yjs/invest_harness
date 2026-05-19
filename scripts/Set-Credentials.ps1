[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [string]$EnvPath = (Join-Path (Resolve-Path (Join-Path $PSScriptRoot '..')) '.env'),
    [switch]$AllowPlaceholders
)

$ErrorActionPreference = 'Stop'

$requiredVariables = @(
    'DART_API_KEY',
    'KRX_API_KEY',
    'FRED_API_KEY',
    'ALPHA_VANTAGE_API_KEY',
    'FMP_API_KEY',
    'KOSIS_API_KEY',
    'CUSTOMS_TRADE_API_KEY',
    'CUSTOMS_TRADE_FORMAT',
    'CUSTOMS_TRADE_ENDPOINT'
)

function Test-PlaceholderValue {
    param([string]$Value)

    return [string]::IsNullOrWhiteSpace($Value) -or
        $Value -match '^(your_|YOUR_|changeme|CHANGE_ME|placeholder|PLACEHOLDER)'
}

$importScript = Join-Path $PSScriptRoot 'env\Import-HarnessEnv.ps1'
$loadedVariables = & $importScript -EnvPath $EnvPath -PassThru

Write-Output "환경 파일 로드 완료: $EnvPath"

$missingVariables = New-Object System.Collections.Generic.List[string]
foreach ($name in $requiredVariables) {
    $value = [Environment]::GetEnvironmentVariable($name, 'Process')
    if ((Test-PlaceholderValue -Value $value) -and -not $AllowPlaceholders) {
        $missingVariables.Add($name)
    }
}

if ($missingVariables.Count -gt 0) {
    $joined = $missingVariables -join ', '
    throw "실제 값이 필요한 환경변수가 비어 있거나 placeholder입니다: $joined"
}

foreach ($name in $loadedVariables) {
    $value = [Environment]::GetEnvironmentVariable($name, 'Process')
    if ([string]::IsNullOrWhiteSpace($value)) {
        Write-Output "건너뜀: $name 값이 비어 있습니다."
        continue
    }

    if ($PSCmdlet.ShouldProcess("Windows User 환경변수 $name", '등록 또는 갱신')) {
        [Environment]::SetEnvironmentVariable($name, $value, 'User')
        Write-Output "등록 완료: $name"
    }
}

Write-Output "Windows User 환경변수 등록이 완료되었습니다. 새 터미널 또는 IDE 세션에서 적용됩니다."
