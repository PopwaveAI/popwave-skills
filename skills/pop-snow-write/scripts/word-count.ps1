# write skill 字数门禁专用：汉字字数以文件实测为准，stdout 为 review 章日志"字数"栏唯一依据
# write 落盘后自跑；不足/超限由 write 自己补写或删减闭环，不交 review 补救
# 口径：纯汉字字符（\u4e00-\u9fff），不含标点/空格/英文/数字/markdown标记
# 判定：2000-2500 汉字 = PASS，否则 FAIL
# 段落节奏扫描（Mirror 06 节奏硬尺）：叙事段40-120字；60% 以上叙事段<40字 = 段落过碎 FAIL 返工
param(
    [Parameter(Mandatory=$true)][string]$Path,
    [int]$Min = 2000,
    [int]$Max = 2500
)

if (-not (Test-Path $Path)) {
    Write-Output ("{0}|文件不存在|FAIL" -f (Split-Path $Path -Leaf))
    exit 1
}

$raw = Get-Content $Path -Raw -Encoding UTF8

# 去 markdown 标记（标题/表格/分隔线/代码块/粗体/斜体）
$text = $raw
$text = $text -replace '(?m)^#+\s.*$', ''
$text = $text -replace '(?m)^\|.*\|$', ''
$text = $text -replace '(?m)^---$', ''
$text = $text -replace '```.*?```', ''
$text = $text -replace '\*\*([^*]+)\*\*', '$1'
$text = $text -replace '\*([^*]+)\*', '$1'

# 纯汉字计数
$han = ([regex]::Matches($text, '[\u4e00-\u9fff]')).Count

if ($han -lt $Min) {
    $verdict = "FAIL(汉字{0}低于下限{1}少写)" -f $han, $Min
} elseif ($han -gt $Max) {
    $verdict = "FAIL(汉字{0}超上限{1}超写)" -f $han, $Max
} else {
    $verdict = "PASS"
}

# ---- 段落节奏扫描（Mirror 06）----
# 段落：按空行切分，剔除空段。对话段=整段被中文/英文引号包住的纯对白，天然短不计入叙事段。
$paras = $text -split "`r?`n\s*`r?`n" | Where-Object { $_.Trim() -ne '' }
$narrTotal = 0   # 叙事段总数
$narrShort = 0   # 叙事段中 <40 字符的短段数
$dlogShort = 0   # 对话短段数（仅报告）
$shortSeq = @()  # 每段是否叙事短段（对话段跳过，作连续性分隔符）

foreach ($p in $paras) {
    $p2 = $p -replace '^\s+', '' -replace '\s+$', ''
    $len = ([regex]::Matches($p2, '\S')).Count
    $isDlog = ($p2 -match '^“' -and $p2 -match '”$') -or ($p2 -match '^"' -and $p2 -match '"$')
    if ($isDlog) {
        if ($len -lt 40) { $dlogShort++ }
    } else {
        $narrTotal++
        if ($len -lt 40) { $narrShort++; $shortSeq += $true } else { $shortSeq += $false }
    }
}

# 连续3短段（叙事段，对话段作分隔）
$triples = 0
$run = 0
foreach ($s in $shortSeq) {
    $run = if ($s) { $run + 1 } else { 0 }
    if ($run -eq 3) { $triples++; $run = 0 }
}

if ($narrTotal -gt 0) {
    $pct = [math]::Round(($narrShort / $narrTotal) * 100, 0)
    if (($narrShort / $narrTotal) -gt 0.60) {
        $rVerdict = "FAIL(段落过碎,短段超60%)"
    } else {
        $rVerdict = "PASS"
    }
} else {
    $pct = 0
    $rVerdict = "PASS(无叙事段)"
}

Write-Output ("{0}|汉字{1}|判定:{2}" -f (Split-Path $Path -Leaf), $han, $verdict)
Write-Output ("{0}|段落: 叙事段{1} 短段{2}({3}%) 连续3短段{4}处 对话短段{5}|判定:{6}" -f (Split-Path $Path -Leaf), $narrTotal, $narrShort, $pct, $triples, $dlogShort, $rVerdict)

if ($verdict -eq 'PASS' -and $rVerdict -match '^PASS') { exit 0 } else { exit 1 }