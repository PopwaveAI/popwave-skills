<#
.SYNOPSIS
    Phase 0 chapter index extraction (ch1-100) for pop-novel-deconstructor v11.1
.DESCRIPTION
    Builds a chapter index for ch1-100 with titles, char counts, first sentences, and content tags.
    Output: chapter-index.json
.PARAMETER TxtPath
    Path to source TXT file (GBK encoded)
.PARAMETER OutputDir
    Directory for JSON output
#>
param(
    [Parameter(Mandatory=$true)][string]$TxtPath,
    [Parameter(Mandatory=$true)][string]$OutputDir
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $TxtPath)) {
    Write-Error "File not found: $TxtPath"
    exit 1
}
$null = New-Item -ItemType Directory -Path $OutputDir -Force

try {
    $content = Get-Content -Path $TxtPath -Encoding Default -Raw
    $lines   = Get-Content -Path $TxtPath -Encoding Default
} catch {
    Write-Error "Failed to read file: $_"
    exit 1
}
Write-Host "[extract-chapter-index] Loaded $($lines.Count) lines"

$chPrefix = [regex]::Escape('第')
$chSuffix = '章'
$chapterRegex = "^${chPrefix}(\d+)$chSuffix\S*(?:\s+\S+)?$"
$chapterIndex = @()
for ($i = 0; $i -lt $lines.Count; $i++) {
    $ln = $lines[$i].Trim()
    if ($ln -match $chapterRegex) {
        $chapterIndex += [PSCustomObject]@{ Number = [int]$Matches[1]; Title = $ln; Line = $i }
    }
}
Write-Host "[extract-chapter-index] Found $($chapterIndex.Count) Arabic-numeral chapters"

# Filter ch1-100
$ch1to100 = $chapterIndex | Where-Object { $_.Number -ge 1 -and $_.Number -le 100 } | Sort-Object Number
$totalChapters = if ($ch1to100.Count -ge 100) { 100 } else { $ch1to100.Count }
Write-Host "[extract-chapter-index] Processing $totalChapters chapters (1-$totalChapters)"

# Tag keywords
$battleKeywords = @('战斗','杀','攻击','防御','战','剑','刀','魔法','法术','箭','武器','怪物','恶魔','魔兽','强盗','战斗爆发','混战','搏杀','偷袭','伏击','流血','伤害','死亡','杀死','击杀','斩杀','刃')
$worldKeywords   = @('神殿','魔法','神祇','法则','位面','多元宇宙','圣者','神明','神灵','诸神','牧师','信仰','教会','宗教','祭祀','仪式','魔力','奥术','法术书','秘法','元素','深渊','地狱','天堂','契约')
$economyKeywords = @('交易','金德勒','金币','银币','铜德勒','拍卖','商人','商店','市场','铁匠铺','装备','武器铺','药水','药剂','卷轴','次元袋','魔法物品','神器','宝藏','财富','金钱')

$outputChapters = @()
$first100CharCount = 0

for ($idx = 0; $idx -lt $ch1to100.Count; $idx++) {
    $ch = $ch1to100[$idx]
    $start = $ch.Line
    # End is next chapter start or end of file
    if ($idx + 1 -lt $ch1to100.Count) {
        $end = $ch1to100[$idx + 1].Line - 1
    } else {
        # Find the 101st chapter
        $next = $chapterIndex | Where-Object { $_.Number -gt 100 } | Select-Object -First 1
        $end = if ($next) { $next.Line - 1 } else { $lines.Count - 1 }
    }
    if ($end -lt $start) { $end = $start + [Math]::Max(0, ($lines.Count - $start - 1)) }

    $chText = $lines[$start..$end] -join "`n"
    $chStripped = $chText -replace '\s+', ''
    $charCount  = $chStripped.Length
    $first100CharCount += $charCount

    # First non-empty, non-title line as first sentence
    $firstSentence = ""
    for ($j = $start + 1; $j -le $end; $j++) {
        $t = $lines[$j].Trim()
        if ($t.Length -gt 0 -and $t -notmatch $chapterRegex) {
            $firstSentence = if ($t.Length -gt 80) { $t.Substring(0, 80) + "..." } else { $t }
            break
        }
    }

    # Tag content types
    $tags = @()
    $battleHits  = ($battleKeywords  | ForEach-Object { if ($chText -match $_) { 1 } } | Measure-Object -Sum).Sum
    $worldHits   = ($worldKeywords   | ForEach-Object { if ($chText -match $_) { 1 } } | Measure-Object -Sum).Sum
    $economyHits = ($economyKeywords | ForEach-Object { if ($chText -match $_) { 1 } } | Measure-Object -Sum).Sum
    if ($battleHits  -ge 3) { $tags += "battle" }
    if ($worldHits   -ge 3) { $tags += "worldbuilding" }
    if ($economyHits -ge 3) { $tags += "economy" }

    $outputChapters += [PSCustomObject]@{
        chapter       = $ch.Number
        title         = $ch.Title
        lineStart     = $start
        lineEnd       = $end
        charCount     = $charCount
        firstSentence = $firstSentence
        tags          = $tags
    }
}

# Build output
$output = [PSCustomObject]@{
    meta = [PSCustomObject]@{
        source           = $TxtPath
        script           = "extract-chapter-index.ps1 (Phase 0)"
        extractedAt      = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
        totalArabChapters = $chapterIndex.Count
        totalLines        = $lines.Count
        first100CharCount = $first100CharCount
    }
    chapters = $outputChapters
}

$outputPath = Join-Path $OutputDir "chapter-index.json"
$output | ConvertTo-Json -Depth 4 | Out-File -FilePath $outputPath -Encoding UTF8

$battleChapters  = ($outputChapters | Where-Object { "battle"      -in $_.tags }).Count
$worldChapters   = ($outputChapters | Where-Object { "worldbuilding" -in $_.tags }).Count
$economyChapters = ($outputChapters | Where-Object { "economy"     -in $_.tags }).Count

$sep = "=" * 60
Write-Host ""
Write-Host $sep
Write-Host "  extract-chapter-index.ps1 -- Done"
Write-Host $sep
Write-Host "  Chapters indexed  : $($outputChapters.Count)"
Write-Host "  Total chars (1-100): $first100CharCount"
Write-Host "  Battle chapters   : $battleChapters"
Write-Host "  Worldbuilding chs : $worldChapters"
Write-Host "  Economy chapters  : $economyChapters"
Write-Host $sep
Write-Host ""
