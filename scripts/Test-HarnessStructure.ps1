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
    @{ Path = 'docs\harness\invest\data-source-policy.md'; Description = '데이터 소스 정책 문서' },
    @{ Path = 'docs\harness\invest\mcp-routing.md'; Description = 'MCP 라우팅 문서' },
    @{ Path = 'docs\harness\invest\templates\input-intake.md'; Description = '입력 수집 게이트 템플릿' },
    @{ Path = 'docs\harness\invest\templates\request-summary.md'; Description = '요청 요약 템플릿' },
    @{ Path = 'docs\harness\invest\templates\findings-common.md'; Description = '공통 findings 템플릿' },
    @{ Path = 'docs\harness\invest\templates\conflicts.md'; Description = '충돌 기록 템플릿' },
    @{ Path = 'docs\harness\invest\templates\report.md'; Description = '보고서 템플릿' },
    @{ Path = 'docs\harness\invest\templates\qa-review.md'; Description = 'QA 템플릿' },
    @{ Path = 'docs\harness\invest\templates\quarterly-sentiment-deep-dive.md'; Description = '최근 분기·센티먼트 심층 비교 템플릿' },
    @{ Path = 'docs\harness\invest\templates\market-price-snapshot.md'; Description = '기준 주가 snapshot 템플릿' },
    @{ Path = 'docs\harness\invest\templates\screen-criteria.md'; Description = '스크리닝 기준 템플릿' },
    @{ Path = 'docs\harness\invest\templates\candidate-universe.md'; Description = '후보군 템플릿' },
    @{ Path = 'docs\harness\invest\templates\idea-scorecard.md'; Description = '아이디어 점수표 템플릿' },
    @{ Path = 'docs\harness\invest\templates\shortlist.md'; Description = 'shortlist 템플릿' },
    @{ Path = 'docs\harness\invest\templates\comps.md'; Description = 'comps 템플릿' },
    @{ Path = 'docs\harness\invest\templates\dcf.md'; Description = 'DCF 템플릿' },
    @{ Path = 'docs\harness\invest\templates\earnings-update.md'; Description = '실적 업데이트 템플릿' },
    @{ Path = 'docs\harness\invest\templates\earnings-preview.md'; Description = '실적 preview 템플릿' },
    @{ Path = 'docs\harness\invest\templates\sector.md'; Description = '섹터 리포트 템플릿' },
    @{ Path = 'docs\harness\invest\templates\thesis-update.md'; Description = '투자 논지 업데이트 템플릿' },
    @{ Path = 'docs\harness\invest\templates\catalysts.md'; Description = '촉매 캘린더 템플릿' },
    @{ Path = 'docs\harness\invest\templates\html-report.md'; Description = 'HTML 리포트 템플릿' },
    @{ Path = 'docs\harness\invest\templates\morning-note.md'; Description = 'morning note 템플릿' },
    @{ Path = 'docs\harness\invest\templates\update-plan.md'; Description = '리포트 업데이트 계획 템플릿' },
    @{ Path = 'docs\harness\invest\templates\qa-fix-list.md'; Description = 'QA fix-list 템플릿' },
    @{ Path = 'docs\harness\invest\templates\qa-final-check.md'; Description = 'QA final-check 템플릿' },
    @{ Path = 'scripts\invest_command_runtime.py'; Description = 'Python command runtime parser' },
    @{ Path = 'scripts\test_command_runtime.py'; Description = 'Python command runtime smoke tests' },
    @{ Path = 'scripts\Test-CommandRuntime.ps1'; Description = 'PowerShell command runtime smoke script' },
    @{ Path = '.mcp.institutional.json'; Description = '기관용 optional MCP catalog' },
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
