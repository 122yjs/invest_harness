param(
    [string]$EnvPath = (Join-Path (Resolve-Path (Join-Path $PSScriptRoot '..\..')) '.env'),
    [switch]$PassThru
)

$ErrorActionPreference = 'Stop'

function ConvertFrom-EnvValue {
    param([string]$Value)

    $trimmed = $Value.Trim()
    if ($trimmed.Length -ge 2) {
        $first = $trimmed.Substring(0, 1)
        $last = $trimmed.Substring($trimmed.Length - 1, 1)
        if (($first -eq '"' -and $last -eq '"') -or ($first -eq "'" -and $last -eq "'")) {
            return $trimmed.Substring(1, $trimmed.Length - 2)
        }
    }

    return $trimmed
}

if (-not (Test-Path -LiteralPath $EnvPath)) {
    throw "환경 파일을 찾을 수 없습니다: $EnvPath"
}

$loaded = New-Object System.Collections.Generic.List[string]
$lines = Get-Content -LiteralPath $EnvPath

foreach ($line in $lines) {
    $trimmedLine = $line.Trim()
    if ($trimmedLine -eq '' -or $trimmedLine.StartsWith('#')) {
        continue
    }

    $separatorIndex = $trimmedLine.IndexOf('=')
    if ($separatorIndex -le 0) {
        throw "잘못된 .env 항목입니다: $line"
    }

    $name = $trimmedLine.Substring(0, $separatorIndex).Trim()
    $value = ConvertFrom-EnvValue -Value $trimmedLine.Substring($separatorIndex + 1)

    if ($name -notmatch '^[A-Za-z_][A-Za-z0-9_]*$') {
        throw "잘못된 환경변수 이름입니다: $name"
    }

    [Environment]::SetEnvironmentVariable($name, $value, 'Process')
    $loaded.Add($name)
}

if ($PassThru) {
    $loaded
}
