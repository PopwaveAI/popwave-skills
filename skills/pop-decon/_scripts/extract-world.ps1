<#
.SYNOPSIS
    Phase 2.2 world-data extraction (ch1-100) for pop-novel-deconstructor v11.1
.DESCRIPTION
    Searches ch1-100 text for 7 world-building categories: deity, magic, class, species, faction, item, geography.
    Output: world-data.json
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
    $lines = Get-Content -Path $TxtPath -Encoding Default
} catch {
    Write-Error "Failed to read file: $_"
    exit 1
}
Write-Host "[extract-world] Loaded $($lines.Count) lines"

# Build chapter index
$chPrefix = [regex]::Escape('第')
$chSuffix = '章'
$chapterRegex = "^${chPrefix}(\d+)$chSuffix\S*(?:\s+\S+)?$"
$chapterMap = [System.Collections.SortedList]::new()
for ($i = 0; $i -lt $lines.Count; $i++) {
    $ln = $lines[$i].Trim()
    if ($ln -match $chapterRegex) {
        $num = [int]$Matches[1]
        if ($num -ge 1 -and $num -le 100) {
            $null = $chapterMap.Add($num, $i)
        }
    }
}
Write-Host "[extract-world] Mapped $($chapterMap.Count) chapters (1-100)"

# Category definitions: name + keywords
$categories = @(
    @{ name="deity";     kw=@('神祇','圣者','神格','神性','诸神','神灵','神明','神','半神','神之子','圣者形态','神力','信仰之力') },
    @{ name="magic";     kw=@('法术','魔法','奥术','魔力','法阵','施法','咒语','术法','法术位','环级','环位','一环','二环','三环','四环','五环','六环','七环','八环','九环','法术书','学派','法术反制','法术穿透') },
    @{ name="class";     kw=@('职业','等级','进阶','游荡者','盗贼','战士','法师','牧师','骑士','弓箭手','术士','召唤师','剑士','魔导师','刺客','猎手','祭祀','巫师','德鲁伊','圣武士','吟游诗人','野蛮人','武僧','术法','专长','技能') },
    @{ name="species";   kw=@('精灵','矮人','龙族','魔族','兽人','半精灵','半兽人','亡灵','巫妖','吸血鬼','狼人','变形怪','深渊恶魔','魔鬼','天使','妖精','元素生物','巨人','地精','豺狼人','食人魔','哥布林','种族','血脉') },
    @{ name="faction";   kw=@('势力','组织','神殿','公会','帝国','王国','联盟','联邦','教会','教派','骑士团','冒险者公会','商会','行会','晨曦','暗影','秩序','混乱','善良','邪恶','中立') },
    @{ name="item";      kw=@('神器','法器','魔杖','法杖','长剑','弯刀','匕首','皮甲','锁甲','板甲','盾牌','药剂','药水','卷轴','次元袋','魔法物品','魔法装备','金德勒','铜德勒','银币','金币','弯刀') },
    @{ name="geography"; kw=@('城','镇','村','堡','山','河','湖','海','岛','林','谷','原','沙漠','沼泽','荒野','森林','平原','山脉','遗迹','码头','港口') }
)

# Find which chapter a line belongs to
function Get-ChapterForLine($lineNum) {
    $ch = 0
    foreach ($kv in $chapterMap.GetEnumerator()) {
        if ($lineNum -lt $kv.Value) { break }
        $ch = $kv.Key
    }
    return if ($ch -ge 1 -and $ch -le 100) { $ch } else { 0 }
}

# Results collector
$results = @{}
foreach ($cat in $categories) {
    $results[$cat.name] = [System.Collections.ArrayList]::new()
}
$seen = @{}  # dedup key: "category|ch|text"

# Scan all lines in ch1-100 range
$scanStart = $chapterMap[1]
$scanEnd   = if ($chapterMap.Count -gt 100) { $chapterMap[100] } else { $lines.Count - 1 }
if ($scanStart -ge $scanEnd) { $scanEnd = $lines.Count - 1 }
Write-Host "[extract-world] Scanning lines $scanStart to $scanEnd"

for ($i = $scanStart; $i -le $scanEnd; $i++) {
    $ln = $lines[$i]
    if ($ln.Length -lt 2) { continue }
    
    $ch = Get-ChapterForLine $i
    if ($ch -eq 0) { continue }

    foreach ($cat in $categories) {
        foreach ($kw in $cat.kw) {
            if ($ln.Contains($kw)) {
                # Get context: line-2 to line+2
                $ctxStart = [Math]::Max(0, $i - 2)
                $ctxEnd   = [Math]::Min($lines.Count - 1, $i + 2)
                $ctxLines = @()
                for ($cj = $ctxStart; $cj -le $ctxEnd; $cj++) {
                    $prefix = if ($cj -eq $i) { ">>" } else { "  " }
                    $ctxLines += "$prefix$($lines[$cj])"
                }
                $ctxText = $ctxLines -join "`n"

                # Capture matched segment (up to 60 chars around keyword)
                $pos = $ln.IndexOf($kw)
                $segStart = [Math]::Max(0, $pos - 20)
                $segLen   = [Math]::Min($ln.Length - $segStart, 60)
                $matchedSegment = $ln.Substring($segStart, $segLen)

                $textKey = $ln.Trim()
                if ($textKey.Length -gt 80) { $textKey = $textKey.Substring(0, 80) }
                $dedupKey = "$($cat.name)|$ch|$textKey"
                
                if (-not $seen.ContainsKey($dedupKey)) {
                    $seen[$dedupKey] = $true
                    $null = $results[$cat.name].Add([PSCustomObject]@{
                        chapter = $ch
                        line    = $i
                        text    = $textKey
                        match   = $matchedSegment
                        keyword = $kw
                        context = $ctxText
                    })
                }
                break  # one match per category per line
            }
        }
    }
}

# Build output
$catOutputs = @{}
$stats = @{}
foreach ($cat in $categories) {
    $entries = @($results[$cat.name])
    $catOutputs[$cat.name] = [PSCustomObject]@{ count = $entries.Count; entries = $entries }
    $stats[$cat.name] = $entries.Count
}

$output = [PSCustomObject]@{
    meta = [PSCustomObject]@{
        source      = $TxtPath
        script      = "extract-world.ps1 (Phase 2.2)"
        extractedAt = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
        chapterRange = "1-100"
    }
    categories = $catOutputs
    stats      = $stats
}

$outputPath = Join-Path $OutputDir "world-data.json"
$output | ConvertTo-Json -Depth 5 | Out-File -FilePath $outputPath -Encoding UTF8

$sep = "=" * 60
Write-Host ""
Write-Host $sep
Write-Host "  extract-world.ps1 -- Done"
Write-Host $sep
foreach ($cat in $categories) {
    $n = $results[$cat.name].Count
    Write-Host ("  {0,-15}: {1,6} entries" -f $cat.name, $n)
}
Write-Host $sep
Write-Host ""
