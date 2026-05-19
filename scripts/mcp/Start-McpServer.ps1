param(
    [Parameter(Mandatory = $true)]
    [string]$ServerName,

    [Parameter(Mandatory = $true)]
    [string]$CommandEnvVar,

    [Parameter(Mandatory = $true)]
    [string]$DefaultCommand,

    [Parameter(Mandatory = $true)]
    [string]$ArgumentsEnvVar,

    [string[]]$RequiredVariables = @(),

    [string]$EnvPath = (Join-Path (Resolve-Path (Join-Path $PSScriptRoot '..\..')) '.env')
)

$ErrorActionPreference = 'Stop'

function Split-CommandLine {
    param([string]$CommandLine)

    if ([string]::IsNullOrWhiteSpace($CommandLine)) {
        return @()
    }

    $matches = [regex]::Matches($CommandLine, '("[^"]*"|''[^'']*''|\S+)')
    $items = New-Object System.Collections.Generic.List[string]
    foreach ($match in $matches) {
        $value = $match.Value
        if ($value.Length -ge 2) {
            $first = $value.Substring(0, 1)
            $last = $value.Substring($value.Length - 1, 1)
            if (($first -eq '"' -and $last -eq '"') -or ($first -eq "'" -and $last -eq "'")) {
                $value = $value.Substring(1, $value.Length - 2)
            }
        }
        $items.Add($value)
    }

    return $items.ToArray()
}

$importScript = Join-Path $PSScriptRoot '..\env\Import-HarnessEnv.ps1'
if (Test-Path -LiteralPath $EnvPath) {
    & $importScript -EnvPath $EnvPath | Out-Null
}

$missingVariables = New-Object System.Collections.Generic.List[string]
foreach ($name in $RequiredVariables) {
    $value = [Environment]::GetEnvironmentVariable($name, 'Process')
    if ([string]::IsNullOrWhiteSpace($value) -or $value -match '^(your_|YOUR_|changeme|CHANGE_ME|placeholder|PLACEHOLDER)') {
        $missingVariables.Add($name)
    }
}

if ($missingVariables.Count -gt 0) {
    $joined = $missingVariables -join ', '
    throw "$ServerName MCP 실행에 필요한 환경변수가 없습니다: $joined"
}

$command = [Environment]::GetEnvironmentVariable($CommandEnvVar, 'Process')
if ([string]::IsNullOrWhiteSpace($command)) {
    $command = $DefaultCommand
}

$argumentsLine = [Environment]::GetEnvironmentVariable($ArgumentsEnvVar, 'Process')
$arguments = Split-CommandLine -CommandLine $argumentsLine

$resolvedCommand = Get-Command -Name $command -ErrorAction SilentlyContinue
if ($null -eq $resolvedCommand) {
    throw "$ServerName MCP 실행 파일을 찾을 수 없습니다: $command. $CommandEnvVar 환경변수로 실제 명령을 지정하세요."
}

Write-Error "$ServerName MCP 시작: $($resolvedCommand.Source)"
& $resolvedCommand.Source @arguments
