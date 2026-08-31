# write skill 验收门禁专用：汉字字数以文件实测为准，stdout 为验收记录唯一依据
# 口径：纯汉字字符（\u4e00-\u9fff），不含标点/空格/英文/数字/markdown标记
# 判定：2000-2500 汉字 = PASS，否则 FAIL
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

Write-Output ("{0}|汉字{1}|判定:{2}" -f (Split-Path $Path -Leaf), $han, $verdict)
exit ($(if ($verdict -eq 'PASS') { 0 } else { 1 }))
