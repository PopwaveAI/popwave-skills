<#
.SYNOPSIS
    Phase S baseline extraction (ch1-20) for pop-novel-deconstructor v11.1
.DESCRIPTION
    Extracts characters, places, levels, ages, monsters, and events from ch1-20 of a web novel TXT.
    Output: baseline-data.json
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

# Read file with GBK encoding
try {
    $content = Get-Content -Path $TxtPath -Encoding Default -Raw
    $lines   = Get-Content -Path $TxtPath -Encoding Default
} catch {
    Write-Error "Failed to read file: $_"
    exit 1
}
Write-Host "[extract-baseline] Loaded $($lines.Count) lines from $TxtPath"

# Build chapter index for Arabic-numeral chapters
# Use Unicode-safe approach to avoid encoding issues with Chinese chars
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
Write-Host "[extract-baseline] Found $($chapterIndex.Count) Arabic-numeral chapters"

# Extract ch1-20 text block
$ch1to20 = $chapterIndex | Where-Object { $_.Number -ge 1 -and $_.Number -le 20 } | Sort-Object Number
if ($ch1to20.Count -eq 0) {
    Write-Warning "[extract-baseline] No ch1-20 found, using first 20 chapters by position"
    $ch1to20 = $chapterIndex | Select-Object -First 20
}
$startLine = $ch1to20[0].Line
$endChapter = $chapterIndex | Where-Object { $_.Number -gt 20 } | Select-Object -First 1
$endLine = if ($endChapter) { $endChapter.Line } else { $lines.Count }
$ch20Text = $lines[$startLine..($endLine-1)]
$ch20String = $ch20Text -join "`n"
Write-Host "[extract-baseline] ch1-20 text range: lines $startLine to $($endLine-1), $($ch20String.Length) chars"

# --- Search: Named characters (quoted Chinese names, >=2 chars) ---
$charList = [System.Collections.ArrayList]::new()
$charRegex = '["""\x{300C}\x{300E}]([\u4e00-\u9fff]{2,})["""\x{300D}\x{300F}]'
$charMatches = [regex]::Matches($ch20String, $charRegex)
$seenChars = @{}
foreach ($m in $charMatches) {
    $name = $m.Groups[1].Value.Trim()
    if ($name.Length -ge 2 -and -not $seenChars.ContainsKey($name)) {
        $seenChars[$name] = $true
        # Find which chapter this character first appears in
        $idx = $ch20String.IndexOf($m.Value)
        $null = $charList.Add($name)
    }
}

# --- Search: Place names ---
$placeList = [System.Collections.ArrayList]::new()
$placeRegex = '(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))'
$placeMatches = [regex]::Matches($ch20String, $placeRegex)
$seenPlaces = @{}
foreach ($m in $placeMatches) {
    $pname = $m.Groups[1].Value.Trim()
    if (-not $seenPlaces.ContainsKey($pname)) {
        $seenPlaces[$pname] = $true
        $null = $placeList.Add($pname)
    }
}

# --- Search: Level/class mentions ---
$levelList = [System.Collections.ArrayList]::new()
$levelRegex = '(?:([\u4e00-\u9fff]{0,4})(?:级|职业|阶位|段位|境界))|(?:游荡者|盗贼|战士|法师|牧师|骑士|弓箭手|术士|召唤师|剑士|魔导师|刺客|猎手|祭祀|平民)'
$levelMatches = [regex]::Matches($ch20String, $levelRegex)
$seenLevels = @{}
foreach ($m in $levelMatches) {
    $val = $m.Value.Trim()
    if ($val.Length -ge 1 -and -not $seenLevels.ContainsKey($val)) {
        $seenLevels[$val] = $true
        $null = $levelList.Add($val)
    }
}

# --- Search: Age mentions ---
$ageList = [System.Collections.ArrayList]::new()
$ageRegex = '([\u4e00-\u9fff]{0,6}?(\d+)\s*岁)'
$ageMatches = [regex]::Matches($ch20String, $ageRegex)
foreach ($m in $ageMatches) {
    $null = $ageList.Add($m.Value.Trim())
}

# --- Search: Monster names ---
$monsterList = [System.Collections.ArrayList]::new()
$monRegex = '([\u4e00-\u9fff]{2,}(?:兽|龙|蛇|狼|虎|熊|鹰|鸟|虫|鱼|怪|魔|妖|精|灵))'
$monMatches = [regex]::Matches($ch20String, $monRegex)
$seenMons = @{}
foreach ($m in $monMatches) {
    $mname = $m.Groups[1].Value.Trim()
    if (-not $seenMons.ContainsKey($mname)) {
        $seenMons[$mname] = $true
        $null = $monsterList.Add($mname)
    }
}

# --- Extract events: first significant sentence of each chapter ---
$events = @()
$currentChapter = 0
$chapterBuffer = ""

for ($i = 0; $i -lt $lines.Count; $i++) {
    $ln = $lines[$i].Trim()
    if ($ln -match $chapterRegex) {
        $num = [int]$Matches[1]
        if ($num -ge 1 -and $num -le 20) {
            if ($currentChapter -ne 0 -and $chapterBuffer.Length -gt 0) {
                $evt = $chapterBuffer -replace '\s+', ''
                $events += [PSCustomObject]@{
                    chapter = $currentChapter
                    summary = $evt.Substring(0, [Math]::Min(100, $evt.Length))
                }
            }
            $currentChapter = $num
            $chapterBuffer = ""
            continue
        } elseif ($num -gt 20) {
            if ($currentChapter -ne 0 -and $chapterBuffer.Length -gt 0) {
                $evt = $chapterBuffer -replace '\s+', ''
                $events += [PSCustomObject]@{
                    chapter = $currentChapter
                    summary = $evt.Substring(0, [Math]::Min(100, $evt.Length))
                }
            }
            $currentChapter = 0
            continue
        }
    }
    if ($currentChapter -gt 0 -and $ln.Length -gt 0) {
        $chapterBuffer += $ln
    }
}
# Last chapter
if ($currentChapter -ne 0 -and $chapterBuffer.Length -gt 0) {
    $evt = $chapterBuffer -replace '\s+', ''
    $events += [PSCustomObject]@{
        chapter = $currentChapter
        summary = $evt.Substring(0, [Math]::Min(100, $evt.Length))
    }
}

# --- Build output object ---
$output = [PSCustomObject]@{
    meta = [PSCustomObject]@{
        source      = $TxtPath
        script      = "extract-baseline.ps1 (Phase S)"
        extractedAt = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
        chapters    = "1-20"
        totalLines  = $lines.Count
    }
    characters   = @($charList)
    places       = @($placeList)
    levels       = @($levelList)
    ages         = @($ageList | Sort-Object -Unique)
    monsters     = @($monsterList)
    events       = @($events | Sort-Object { $_.chapter })
}

# --- Write JSON ---
$outputPath = Join-Path $OutputDir "baseline-data.json"
$output | ConvertTo-Json -Depth 4 | Out-File -FilePath $outputPath -Encoding UTF8

# --- Print summary ---
$sep = "=" * 60
Write-Host ""
Write-Host $sep
Write-Host "  extract-baseline.ps1 -- Done"
Write-Host $sep
Write-Host "  Source      : $TxtPath"
Write-Host "  Output      : $outputPath"
Write-Host "  Chapters    : 1-20 ($($events.Count) events)"
Write-Host "  Characters  : $($charList.Count)"
Write-Host "  Places      : $($placeList.Count)"
Write-Host "  Levels       : $($levelList.Count)"
Write-Host "  Age mentions : $($ageList.Count)"
Write-Host "  Monsters    : $($monsterList.Count)"
Write-Host $sep
Write-Host ""
