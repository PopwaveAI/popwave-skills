param(
    [Parameter(Mandatory=$true)][string]$Path,
    [int]$Min = 1800,
    [int]$Max = 3000
)
# write v4.2.2 验收门禁专用：字数以文件实测为准，stdout 为验收记录唯一依据
if (-not (Test-Path $Path)) {
    Write-Output ("{0}|文件不存在|FAIL" -f (Split-Path $Path -Leaf))
    exit 1
}
$text = Get-Content $Path -Raw -Encoding UTF8
$total = $text.Length
$nospace = ($text -replace '\s', '').Length
$han = ([regex]::Matches($text, '[\u4e00-\u9fff]')).Count
$verdict = if ($nospace -lt $Min) { ("FAIL(去空白{0}小于阈值{1}少写)" -f $nospace, $Min) } elseif ($nospace -gt $Max) { ("FAIL(去空白{0}超上限{1}超写)" -f $nospace, $Max) } else { "PASS" }
Write-Output ("{0}|总字符{1}|去空白{2}|汉字{3}|判定:{4}" -f (Split-Path $Path -Leaf), $total, $nospace, $han, $verdict)
exit ($(if ($verdict -eq 'PASS') { 0 } else { 1 }))
