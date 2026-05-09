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
        $failures.Add("누락: $Description ($RelativePath)")
    }
}

function Test-SkillFrontmatter {
    param([string]$SkillPath)

    $content = Get-Content -LiteralPath $SkillPath -Raw
    $relativePath = [System.IO.Path]::GetRelativePath($repoRoot, $SkillPath)

    if (-not $content.StartsWith("---`n") -and -not $content.StartsWith("---`r`n")) {
        $failures.Add("frontmatter 시작 누락: $relativePath")
        return
    }

    $normalized = $content -replace "`r`n", "`n"
    $parts = $normalized -split "`n---`n", 2
    if ($parts.Count -lt 2) {
        $failures.Add("frontmatter 종료 누락: $relativePath")
        return
    }

    $frontmatter = $parts[0]
    if ($frontmatter -notmatch "(?m)^name:\s*\S+") {
        $failures.Add("frontmatter name 누락: $relativePath")
    }
    if ($frontmatter -notmatch "(?m)^description:\s*\S+") {
        $failures.Add("frontmatter description 누락: $relativePath")
    }
}

$requiredPaths = @(
    @{ Path = 'AGENTS.md'; Description = '저장소 지침' },
    @{ Path = 'README.md'; Description = '사용자 README' },
    @{ Path = 'OPENCLAW.md'; Description = 'OpenClaw 진입점' },
    @{ Path = 'HERMES.md'; Description = 'Hermes 진입점' },
    @{ Path = 'CLAUDE.md'; Description = 'Claude/Claude Code 진입점' },
    @{ Path = 'GEMINI.md'; Description = 'Gemini/Antigravity 진입점' },
    @{ Path = 'invest_prompt_v2.md'; Description = '핵심 투자 프롬프트' },
    @{ Path = 'docs\harness\invest\team-spec.md'; Description = '팀 명세' },
    @{ Path = 'docs\harness\invest\runbook.md'; Description = '실행 가이드' },
    @{ Path = 'docs\harness\invest\cross-tool-usage.md'; Description = '도구별 사용 가이드' },
    @{ Path = 'docs\harness\invest\templates\request-summary.md'; Description = '요청 요약 템플릿' },
    @{ Path = 'docs\harness\invest\templates\findings-common.md'; Description = '공통 findings 템플릿' },
    @{ Path = 'docs\harness\invest\templates\conflicts.md'; Description = '충돌 기록 템플릿' },
    @{ Path = 'docs\harness\invest\templates\report.md'; Description = '보고서 템플릿' },
    @{ Path = 'docs\harness\invest\templates\qa-review.md'; Description = 'QA 템플릿' },
    @{ Path = '.agents\skills\invest-orchestrator\SKILL.md'; Description = '오케스트레이터 스킬' },
    @{ Path = '.agents\skills\financial-analyst\SKILL.md'; Description = '재무 분석 스킬' },
    @{ Path = '.agents\skills\fundamental-analyst\SKILL.md'; Description = '정성 분석 스킬' },
    @{ Path = '.agents\skills\valuation-analyst\SKILL.md'; Description = '밸류에이션 스킬' },
    @{ Path = '.agents\skills\technical-analyst\SKILL.md'; Description = '기술적 분석 스킬' },
    @{ Path = '.agents\skills\macro-sentiment-analyst\SKILL.md'; Description = '매크로/센티먼트 스킬' },
    @{ Path = '.agents\skills\risk-scenario-analyst\SKILL.md'; Description = '리스크/시나리오 스킬' },
    @{ Path = '.agents\skills\report-synthesizer\SKILL.md'; Description = '보고서 합성 스킬' },
    @{ Path = '.agents\skills\qa-reviewer\SKILL.md'; Description = 'QA 스킬' }
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
        $relativePath = [System.IO.Path]::GetRelativePath($repoRoot, $skillDir.FullName)
        $failures.Add("빈 스킬 디렉터리 또는 SKILL.md 누락: $relativePath")
    }
}

$handoffPaths = @(
    '_workspace/00_input/request-summary.md',
    '_workspace/01_financial/findings.md',
    '_workspace/02_fundamental/findings.md',
    '_workspace/03_valuation/findings.md',
    '_workspace/04_technical/findings.md',
    '_workspace/05_macro_sentiment/findings.md',
    '_workspace/06_risk_scenario/findings.md',
    '_workspace/06_risk_scenario/conflicts.md',
    '_workspace/07_draft/report.md',
    '_workspace/08_final/report.md',
    '_workspace/08_final/executive-summary.md',
    '_workspace/09_qa/review.md'
)

$teamSpec = Get-Content -LiteralPath (Join-Path $repoRoot 'docs\harness\invest\team-spec.md') -Raw
$orchestrator = Get-Content -LiteralPath (Join-Path $repoRoot '.agents\skills\invest-orchestrator\SKILL.md') -Raw

foreach ($handoff in $handoffPaths) {
    if ($teamSpec -notlike "*$handoff*") {
        $failures.Add("team-spec 핸드오프 경로 누락: $handoff")
    }
    if ($orchestrator -notlike "*$handoff*") {
        $failures.Add("orchestrator 핸드오프 경로 누락: $handoff")
    }
}

if ($failures.Count -gt 0) {
    Write-Host "Harness 구조 검증 실패:" -ForegroundColor Red
    foreach ($failure in $failures) {
        Write-Host "- $failure" -ForegroundColor Red
    }
    exit 1
}

Write-Host "Harness 구조 검증 통과: 필수 경로, 스킬 frontmatter, 핸드오프 계약이 유효합니다." -ForegroundColor Green
