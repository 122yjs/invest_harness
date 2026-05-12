$ErrorActionPreference = 'Stop'

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot '..')
$candidateCommands = @('python3', 'python', 'py')
$pythonCommand = $null

foreach ($candidate in $candidateCommands) {
    $resolved = Get-Command $candidate -ErrorAction SilentlyContinue
    if ($resolved) {
        $pythonCommand = $resolved.Source
        break
    }
}

if (-not $pythonCommand) {
    Write-Host 'Command runtime smoke tests failed: Python executable not found.' -ForegroundColor Red
    exit 1
}

& $pythonCommand (Join-Path $repoRoot 'scripts\test_command_runtime.py')
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}
