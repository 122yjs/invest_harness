$ErrorActionPreference = 'Stop'

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot '..')

$sourceRoot = Join-Path $repoRoot 'plugins/vertical-plugins/invest-research'
$agentPluginRoot = Join-Path $repoRoot 'plugins/agent-plugins/invest-harness'
$agentsRoot = Join-Path $repoRoot '.agents'

$policyNames = @(
    'workspace-safety.md',
    'market-price-anchor.md',
    'data-source-policy.md',
    'qa-recalculation-policy.md',
    'rating-price-target-policy.md',
    'report-writing-style-policy.md'
)

function Get-RepoRelativePath {
    param([string]$Path)
    return ([System.IO.Path]::GetRelativePath($repoRoot, $Path) -replace '\\', '/')
}

function Assert-Directory {
    param([string]$Path, [string]$Description)
    if (-not (Test-Path -LiteralPath $Path -PathType Container)) {
        throw "Required directory missing: $Description ($Path)"
    }
}

function Reset-GeneratedDirectory {
    param([string]$Path)
    if (Test-Path -LiteralPath $Path) {
        Remove-Item -LiteralPath $Path -Recurse -Force
    }
    New-Item -ItemType Directory -Path $Path -Force | Out-Null
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

function Sync-MarkdownTree {
    param(
        [string]$SourceDirectory,
        [string[]]$DestinationDirectories,
        [string]$Kind
    )

    Assert-Directory -Path $SourceDirectory -Description "$Kind source"

    foreach ($destinationDirectory in $DestinationDirectories) {
        Reset-GeneratedDirectory -Path $destinationDirectory
    }

    $sourceFiles = Get-ChildItem -LiteralPath $SourceDirectory -Recurse -File | Where-Object {
        $_.Name -notin @('.DS_Store')
    }

    foreach ($sourceFile in $sourceFiles) {
        $sourceRelativeToTree = [System.IO.Path]::GetRelativePath($SourceDirectory, $sourceFile.FullName)
        $repoRelative = Get-RepoRelativePath -Path $sourceFile.FullName
        $raw = Get-Content -LiteralPath $sourceFile.FullName -Raw
        $generated = Add-GeneratedNotice -Content $raw -SourceRelativePath $repoRelative -Kind $Kind

        foreach ($destinationDirectory in $DestinationDirectories) {
            $destinationPath = Join-Path $destinationDirectory $sourceRelativeToTree
            $destinationParent = Split-Path -Parent $destinationPath
            New-Item -ItemType Directory -Path $destinationParent -Force | Out-Null
            Set-Content -LiteralPath $destinationPath -Value $generated -NoNewline
            Write-Host "synced ${Kind}: $repoRelative -> $(Get-RepoRelativePath -Path $destinationPath)"
        }
    }
}

Assert-Directory -Path $sourceRoot -Description 'vertical source root'

foreach ($policyName in $policyNames) {
    $policyPath = Join-Path (Join-Path $sourceRoot 'policies') $policyName
    if (-not (Test-Path -LiteralPath $policyPath -PathType Leaf)) {
        throw "Required policy missing: plugins/vertical-plugins/invest-research/policies/$policyName"
    }
}

Sync-MarkdownTree `
    -SourceDirectory (Join-Path $sourceRoot 'skills') `
    -DestinationDirectories @((Join-Path $agentPluginRoot 'skills'), (Join-Path $agentsRoot 'skills')) `
    -Kind 'skill'

Sync-MarkdownTree `
    -SourceDirectory (Join-Path $sourceRoot 'commands') `
    -DestinationDirectories @((Join-Path $agentPluginRoot 'commands'), (Join-Path $agentsRoot 'commands')) `
    -Kind 'command'

Sync-MarkdownTree `
    -SourceDirectory (Join-Path $sourceRoot 'policies') `
    -DestinationDirectories @((Join-Path $agentPluginRoot 'policies'), (Join-Path $agentsRoot 'policies')) `
    -Kind 'policy'

Sync-MarkdownTree `
    -SourceDirectory (Join-Path $sourceRoot 'templates') `
    -DestinationDirectories @((Join-Path $agentPluginRoot 'templates')) `
    -Kind 'template'

Write-Host 'Invest skill sync completed successfully.' -ForegroundColor Green
