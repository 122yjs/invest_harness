$ErrorActionPreference = 'Stop'

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot '..')
$failures = New-Object System.Collections.Generic.List[string]

$sourceRoot = Join-Path $repoRoot 'plugins/vertical-plugins/invest-research'
$agentPluginRoot = Join-Path $repoRoot 'plugins/agent-plugins/invest-harness'
$agentsRoot = Join-Path $repoRoot '.agents'

function Get-RepoRelativePath {
    param([string]$Path)
    return ([System.IO.Path]::GetRelativePath($repoRoot, $Path) -replace '\\', '/')
}

function Add-GeneratedNotice {
    param(
        [string]$Content,
        [string]$SourceRelativePath,
        [string]$Kind
    )

    $normalized = $Content -replace "`r`n", "`n"
    $notice = "<!-- GENERATED-SYNC: source=$SourceRelativePath; kind=$Kind; script=scripts/sync_invest_skills.py -->`n" +
        "> [!IMPORTANT]`n" +
        "> Generated execution artifact. Do not edit directly; edit the vertical source and rerun `python scripts/sync_invest_skills.py` (or `scripts/Sync-InvestSkills.ps1` / `scripts/Sync-InvestSkills.sh`).`n" +
        "> Common policies are synced from `plugins/vertical-plugins/invest-research/policies/`.`n" +
        '> Runtime output paths must use `${ACTIVE_WORKSPACE}`.' + "`n" +
        "<!-- END GENERATED-SYNC -->`n"

    if ($normalized -match '(?s)^(---\n.*?\n---\n)(.*)$') {
        return $matches[1] + "`n" + $notice + "`n" + $matches[2]
    }

    return $notice + "`n" + $normalized
}

function Test-GeneratedTree {
    param(
        [string]$SourceDirectory,
        [string[]]$DestinationDirectories,
        [string]$Kind
    )

    if (-not (Test-Path -LiteralPath $SourceDirectory -PathType Container)) {
        $failures.Add("source directory missing: $(Get-RepoRelativePath -Path $SourceDirectory)")
        return
    }

    $sourceFiles = Get-ChildItem -LiteralPath $SourceDirectory -Recurse -File | Where-Object {
        $_.Name -notin @('.DS_Store')
    }

    $expectedRelativePaths = New-Object System.Collections.Generic.HashSet[string]

    foreach ($sourceFile in $sourceFiles) {
        $relativeToTree = [System.IO.Path]::GetRelativePath($SourceDirectory, $sourceFile.FullName) -replace '\\', '/'
        [void]$expectedRelativePaths.Add($relativeToTree)

        $repoRelative = Get-RepoRelativePath -Path $sourceFile.FullName
        $expected = Add-GeneratedNotice -Content (Get-Content -LiteralPath $sourceFile.FullName -Raw) -SourceRelativePath $repoRelative -Kind $Kind

        foreach ($destinationDirectory in $DestinationDirectories) {
            $destinationPath = Join-Path $destinationDirectory $relativeToTree
            if (-not (Test-Path -LiteralPath $destinationPath -PathType Leaf)) {
                $failures.Add("missing generated ${Kind}: $(Get-RepoRelativePath -Path $destinationPath)")
                continue
            }

            $actual = Get-Content -LiteralPath $destinationPath -Raw
            if ($actual -ne $expected) {
                $failures.Add("drift detected in generated ${Kind}: $(Get-RepoRelativePath -Path $destinationPath) (source: $repoRelative)")
            }
        }
    }

    foreach ($destinationDirectory in $DestinationDirectories) {
        if (-not (Test-Path -LiteralPath $destinationDirectory -PathType Container)) {
            $failures.Add("generated directory missing: $(Get-RepoRelativePath -Path $destinationDirectory)")
            continue
        }

        $generatedFiles = Get-ChildItem -LiteralPath $destinationDirectory -Recurse -File | Where-Object {
            $_.Name -notin @('.DS_Store')
        }

        foreach ($generatedFile in $generatedFiles) {
            $relativeToDestination = [System.IO.Path]::GetRelativePath($destinationDirectory, $generatedFile.FullName) -replace '\\', '/'
            if (-not $expectedRelativePaths.Contains($relativeToDestination)) {
                $failures.Add("stale generated ${Kind} not present in source: $(Get-RepoRelativePath -Path $generatedFile.FullName)")
            }
        }
    }
}

Test-GeneratedTree `
    -SourceDirectory (Join-Path $sourceRoot 'skills') `
    -DestinationDirectories @((Join-Path $agentPluginRoot 'skills'), (Join-Path $agentsRoot 'skills')) `
    -Kind 'skill'

Test-GeneratedTree `
    -SourceDirectory (Join-Path $sourceRoot 'commands') `
    -DestinationDirectories @((Join-Path $agentPluginRoot 'commands'), (Join-Path $agentsRoot 'commands')) `
    -Kind 'command'

Test-GeneratedTree `
    -SourceDirectory (Join-Path $sourceRoot 'policies') `
    -DestinationDirectories @((Join-Path $agentPluginRoot 'policies'), (Join-Path $agentsRoot 'policies')) `
    -Kind 'policy'

Test-GeneratedTree `
    -SourceDirectory (Join-Path $sourceRoot 'templates') `
    -DestinationDirectories @((Join-Path $agentPluginRoot 'templates')) `
    -Kind 'template'

if ($failures.Count -gt 0) {
    Write-Host 'Invest skill drift check failed:' -ForegroundColor Red
    foreach ($failure in $failures) {
        Write-Host "- $failure" -ForegroundColor Red
    }
    exit 1
}

Write-Host 'Invest skill drift check passed: generated layers match vertical source.' -ForegroundColor Green
