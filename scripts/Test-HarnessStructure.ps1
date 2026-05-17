$ErrorActionPreference = 'Stop'

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot '..')
$failures = New-Object System.Collections.Generic.List[string]

function Test-RequiredPath {
    param(
        [string]$RelativePath,
        [string]$Description
    )

    $path = Join-Path $repoRoot $RelativePath
    if (-not (Test-Path -LiteralPath $path)) {
        $failures.Add("Missing: $Description ($RelativePath)")
    }
}

function Test-SkillFrontmatter {
    param([string]$SkillPath)

    $content = Get-Content -LiteralPath $SkillPath -Raw
    $relativePath = $SkillPath.Replace($repoRoot.Path, "").TrimStart("\")

    if (-not $content.StartsWith("---`n") -and -not $content.StartsWith("---`r`n")) {
        $failures.Add("Missing frontmatter start: $relativePath")
        return
    }

    $normalized = $content -replace "`r`n", "`n"
    $parts = $normalized -split "`n---`n", 2
    if ($parts.Count -lt 2) {
        $failures.Add("Missing frontmatter end: $relativePath")
        return
    }

    $frontmatter = $parts[0]
    if ($frontmatter -notmatch "(?m)^name:\s*\S+") {
        $failures.Add("Missing frontmatter name: $relativePath")
    }
    if ($frontmatter -notmatch "(?m)^description:\s*\S+") {
        $failures.Add("Missing frontmatter description: $relativePath")
    }
}

$requiredPaths = @(
    @{ Path = 'AGENTS.md'; Description = 'Repository Guidelines' },
    @{ Path = 'README.md'; Description = 'User README' },
    @{ Path = 'OPENCLAW.md'; Description = 'OpenClaw Entrypoint' },
    @{ Path = 'HERMES.md'; Description = 'Hermes Entrypoint' },
    @{ Path = 'CLAUDE.md'; Description = 'Claude Entrypoint' },
    @{ Path = 'GEMINI.md'; Description = 'Gemini Entrypoint' },
    @{ Path = 'invest_prompt_v2.md'; Description = 'Core Investment Prompt' },
    @{ Path = 'docs\harness\invest\team-spec.md'; Description = 'Team Specification' },
    @{ Path = 'docs\harness\invest\runbook.md'; Description = 'Execution Guide' },
    @{ Path = 'docs\harness\invest\cross-tool-usage.md'; Description = 'Tool Usage Guide' },
    @{ Path = 'docs\harness\invest\data-source-policy.md'; Description = 'Data Source Policy Document' },
    @{ Path = 'docs\harness\invest\mcp-routing.md'; Description = 'MCP Routing Document' },
    @{ Path = 'docs\harness\invest\templates\input-intake.md'; Description = 'Input Intake Gate Template' },
    @{ Path = 'docs\harness\invest\templates\request-summary.md'; Description = 'Request Summary Template' },
    @{ Path = 'docs\harness\invest\templates\findings-common.md'; Description = 'Common Findings Template' },
    @{ Path = 'docs\harness\invest\templates\conflicts.md'; Description = 'Conflict Record Template' },
    @{ Path = 'docs\harness\invest\templates\report.md'; Description = 'Report Template' },
    @{ Path = 'docs\harness\invest\templates\qa-review.md'; Description = 'QA Template' },
    @{ Path = 'docs\harness\invest\templates\quarterly-sentiment-deep-dive.md'; Description = 'Quarterly Sentiment Deep Dive Template' },
    @{ Path = 'docs\harness\invest\templates\market-price-snapshot.md'; Description = 'Market Price Snapshot Template' },
    @{ Path = 'docs\harness\invest\templates\screen-criteria.md'; Description = 'Screening Criteria Template' },
    @{ Path = 'docs\harness\invest\templates\candidate-universe.md'; Description = 'Candidate Universe Template' },
    @{ Path = 'docs\harness\invest\templates\idea-scorecard.md'; Description = 'Idea Scorecard Template' },
    @{ Path = 'docs\harness\invest\templates\shortlist.md'; Description = 'Shortlist Template' },
    @{ Path = 'docs\harness\invest\templates\comps.md'; Description = 'Comps Template' },
    @{ Path = 'docs\harness\invest\templates\dcf.md'; Description = 'DCF Template' },
    @{ Path = 'docs\harness\invest\templates\earnings-update.md'; Description = 'Earnings Update Template' },
    @{ Path = 'docs\harness\invest\templates\earnings-preview.md'; Description = 'Earnings Preview Template' },
    @{ Path = 'docs\harness\invest\templates\sector.md'; Description = 'Sector Report Template' },
    @{ Path = 'docs\harness\invest\templates\thesis-update.md'; Description = 'Thesis Update Template' },
    @{ Path = 'docs\harness\invest\templates\catalysts.md'; Description = 'Catalysts Calendar Template' },
    @{ Path = 'docs\harness\invest\templates\html-report.md'; Description = 'HTML Report Template' },
    @{ Path = 'docs\harness\invest\templates\morning-note.md'; Description = 'Morning Note Template' },
    @{ Path = 'docs\harness\invest\templates\update-plan.md'; Description = 'Report Update Plan Template' },
    @{ Path = 'docs\harness\invest\templates\qa-fix-list.md'; Description = 'QA Fix List Template' },
    @{ Path = 'docs\harness\invest\templates\qa-final-check.md'; Description = 'QA Final Check Template' },
    @{ Path = 'scripts\invest_command_runtime.py'; Description = 'Python command runtime parser' },
    @{ Path = 'scripts\test_command_runtime.py'; Description = 'Python command runtime smoke tests' },
    @{ Path = 'scripts\Test-CommandRuntime.ps1'; Description = 'PowerShell command runtime smoke script' },
    @{ Path = '.mcp.institutional.json'; Description = 'Optional Institutional MCP Catalog' },
    @{ Path = '.agents\skills\invest-orchestrator\SKILL.md'; Description = 'Orchestrator Skill' },
    @{ Path = '.agents\skills\financial-analyst\SKILL.md'; Description = 'Financial Analyst Skill' },
    @{ Path = '.agents\skills\fundamental-analyst\SKILL.md'; Description = 'Fundamental Analyst Skill' },
    @{ Path = '.agents\skills\valuation-analyst\SKILL.md'; Description = 'Valuation Analyst Skill' },
    @{ Path = '.agents\skills\technical-analyst\SKILL.md'; Description = 'Technical Analyst Skill' },
    @{ Path = '.agents\skills\macro-sentiment-analyst\SKILL.md'; Description = 'Macro Sentiment Analyst Skill' },
    @{ Path = '.agents\skills\risk-scenario-analyst\SKILL.md'; Description = 'Risk Scenario Analyst Skill' },
    @{ Path = '.agents\skills\report-synthesizer\SKILL.md'; Description = 'Report Synthesizer Skill' },
    @{ Path = '.agents\skills\qa-reviewer\SKILL.md'; Description = 'QA Reviewer Skill' }
)

foreach ($item in $requiredPaths) {
    Test-RequiredPath -RelativePath $item.Path -Description $item.Description
}

$skillFiles = Get-ChildItem -LiteralPath (Join-Path $repoRoot '.agents\skills') -Recurse -Filter 'SKILL.md'
foreach ($skillFile in $skillFiles) {
    Test-SkillFrontmatter -SkillPath $skillFile.FullName
}

$skillDirs = Get-ChildItem -LiteralPath (Join-Path $repoRoot '.agents\skills') -Directory
foreach ($skillDir in $skillDirs) {
    $skillFile = Join-Path $skillDir.FullName 'SKILL.md'
    if (-not (Test-Path -LiteralPath $skillFile)) {
        $relativePath = $skillDir.FullName.Replace($repoRoot.Path, "").TrimStart("\")
        $failures.Add("Empty skill directory or missing SKILL.md: $relativePath")
    }
}

$handoffPaths = @(
    '${ACTIVE_WORKSPACE}/00_input/input-intake.md',
    '${ACTIVE_WORKSPACE}/00_input/request-summary.md',
    '${ACTIVE_WORKSPACE}/00_input/market-price-snapshot.md',
    '${ACTIVE_WORKSPACE}/00_input/earnings-update.md',
    '${ACTIVE_WORKSPACE}/00_input/earnings-preview.md',
    '${ACTIVE_WORKSPACE}/00_input/update-plan.md',
    '${ACTIVE_WORKSPACE}/00_screen/screen-criteria.md',
    '${ACTIVE_WORKSPACE}/00_screen/candidate-universe.md',
    '${ACTIVE_WORKSPACE}/00_screen/idea-scorecard.md',
    '${ACTIVE_WORKSPACE}/00_screen/shortlist.md',
    '${ACTIVE_WORKSPACE}/01_financial/findings.md',
    '${ACTIVE_WORKSPACE}/02_fundamental/findings.md',
    '${ACTIVE_WORKSPACE}/03_valuation/findings.md',
    '${ACTIVE_WORKSPACE}/03_valuation/comps.md',
    '${ACTIVE_WORKSPACE}/03_valuation/dcf.md',
    '${ACTIVE_WORKSPACE}/04_technical/findings.md',
    '${ACTIVE_WORKSPACE}/05_macro_sentiment/findings.md',
    '${ACTIVE_WORKSPACE}/05_macro_sentiment/thesis-update.md',
    '${ACTIVE_WORKSPACE}/05_macro_sentiment/catalysts.md',
    '${ACTIVE_WORKSPACE}/05_macro_sentiment/morning-note.md',
    '${ACTIVE_WORKSPACE}/06_risk_scenario/findings.md',
    '${ACTIVE_WORKSPACE}/06_risk_scenario/conflicts.md',
    '${ACTIVE_WORKSPACE}/07_draft/report.md',
    '${ACTIVE_WORKSPACE}/08_final/report.md',
    '${ACTIVE_WORKSPACE}/08_final/report.html',
    '${ACTIVE_WORKSPACE}/08_final/executive-summary.md',
    '${ACTIVE_WORKSPACE}/09_qa/review.md',
    '${ACTIVE_WORKSPACE}/09_qa/fix-list.md',
    '${ACTIVE_WORKSPACE}/09_qa/final-check.md'
)

$teamSpec = Get-Content -LiteralPath (Join-Path $repoRoot 'docs\harness\invest\team-spec.md') -Raw
$orchestrator = Get-Content -LiteralPath (Join-Path $repoRoot '.agents\skills\invest-orchestrator\SKILL.md') -Raw

foreach ($handoff in $handoffPaths) {
    if ($teamSpec -notlike "*$handoff*") {
        $failures.Add("Missing handoff path in team-spec: $handoff")
    }
    if ($orchestrator -notlike "*$handoff*") {
        $failures.Add("Missing handoff path in orchestrator: $handoff")
    }
}

if ($failures.Count -gt 0) {
    Write-Host "Harness structural validation failed:" -ForegroundColor Red
    foreach ($failure in $failures) {
        Write-Host "- $failure" -ForegroundColor Red
    }
    exit 1
}

Write-Host "Harness structural validation passed: required paths, skill frontmatter, and handoff contracts are valid." -ForegroundColor Green
