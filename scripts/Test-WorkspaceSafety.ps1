$ErrorActionPreference = 'Stop'

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot '..')
$failures = New-Object System.Collections.Generic.List[string]

$scanRoots = @(
    'docs/harness/invest',
    'plugins/vertical-plugins/invest-research',
    'plugins/agent-plugins/invest-harness',
    '.agents/skills',
    '.agents/commands',
    '.agents/policies',
    'scripts'
)

$legacyWorkspace = Join-Path $repoRoot '_workspace'
$fixedWorkspacePattern = '(?<![A-Za-z0-9])_workspace[\\/]'
$activeWorkspacePattern = '\$\{ACTIVE_WORKSPACE\}'

function Get-RepoRelativePath {
    param([string]$Path)
    return ([System.IO.Path]::GetRelativePath($repoRoot, $Path) -replace '\\', '/')
}

function Get-ScannableFiles {
    $files = @()
    foreach ($root in $scanRoots) {
        $absoluteRoot = Join-Path $repoRoot $root
        if (-not (Test-Path -LiteralPath $absoluteRoot)) {
            continue
        }

        $files += Get-ChildItem -LiteralPath $absoluteRoot -Recurse -File | Where-Object {
            $_.Name -notin @('.DS_Store') -and
            $_.FullName -notlike (Join-Path $legacyWorkspace '*')
        }
    }
    return $files
}

$scannableFiles = Get-ScannableFiles

foreach ($file in $scannableFiles) {
    $content = Get-Content -LiteralPath $file.FullName -Raw
    $relative = Get-RepoRelativePath -Path $file.FullName

    if ($content -match $fixedWorkspacePattern) {
        $matches = [regex]::Matches($content, $fixedWorkspacePattern)
        $failures.Add("fixed legacy workspace path found in $relative ($($matches.Count) occurrence(s))")
    }
}

$sourceSkillFiles = Get-ChildItem -LiteralPath (Join-Path $repoRoot 'plugins/vertical-plugins/invest-research/skills') -Recurse -Filter 'SKILL.md' -File -ErrorAction SilentlyContinue
foreach ($skillFile in $sourceSkillFiles) {
    $content = Get-Content -LiteralPath $skillFile.FullName -Raw
    if ($content -notmatch $activeWorkspacePattern) {
        $failures.Add("source skill does not reference `${ACTIVE_WORKSPACE}: $(Get-RepoRelativePath -Path $skillFile.FullName)")
    }
}

$commandFiles = Get-ChildItem -LiteralPath (Join-Path $repoRoot 'plugins/vertical-plugins/invest-research/commands') -Recurse -File -ErrorAction SilentlyContinue
foreach ($commandFile in $commandFiles) {
    $content = Get-Content -LiteralPath $commandFile.FullName -Raw
    if ($content -notmatch $activeWorkspacePattern) {
        $failures.Add("command stub does not reference `${ACTIVE_WORKSPACE}: $(Get-RepoRelativePath -Path $commandFile.FullName)")
    }
    if ($content -notmatch 'thin_wrapper:\s*true') {
        $failures.Add("command stub is missing thin_wrapper:true metadata: $(Get-RepoRelativePath -Path $commandFile.FullName)")
    }
}

if (-not (Test-Path -LiteralPath $legacyWorkspace -PathType Container)) {
    Write-Host 'Legacy sample workspace not present; nothing to preserve.' -ForegroundColor Yellow
} else {
    Write-Host "Legacy sample workspace preserved and excluded: $(Get-RepoRelativePath -Path $legacyWorkspace)"
}

if ($failures.Count -gt 0) {
    Write-Host 'Workspace safety check failed:' -ForegroundColor Red
    foreach ($failure in $failures) {
        Write-Host "- $failure" -ForegroundColor Red
    }
    exit 1
}

Write-Host 'Workspace safety check passed: dynamic workspace rules are enforced for scanned docs, skills, commands, scripts, and templates.' -ForegroundColor Green

