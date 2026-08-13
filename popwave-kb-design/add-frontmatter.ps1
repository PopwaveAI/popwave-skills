# ============================================================
# popwave 知识库 · 批量补齐 frontmatter (PowerShell)
# 给缺 frontmatter 的 md 文件按目录结构推断并写入 YAML 头
# 用法：
#   & .\add-frontmatter.ps1 -Root <库根>            # dry-run，仅预览
#   & .\add-frontmatter.ps1 -Root <库根> -Apply      # 实际写入
# ============================================================
param(
  [string]$Root = "d:\popwave-skills\popwave知识库",
  [switch]$Apply
)
$ErrorActionPreference = 'Stop'

# ---------- 编码安全读取 ----------
function Read-File {
  param([string]$Path)
  $bytes = [System.IO.File]::ReadAllBytes($Path)
  if ($bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF) {
    return @{ content = [System.Text.Encoding]::UTF8.GetString($bytes, 3, $bytes.Length - 3); bom = $true }
  }
  $utf8Strict = New-Object System.Text.UTF8Encoding($false, $true)
  try {
    return @{ content = $utf8Strict.GetString($bytes); bom = $false }
  } catch {
    return @{ content = [System.Text.Encoding]::GetEncoding('GBK').GetString($bytes); bom = $false; gbk = $true }
  }
}

# ---------- 判断是否已有 frontmatter ----------
function Has-Frontmatter {
  param([string]$Path)
  $lines = Get-Content -LiteralPath $Path -Encoding UTF8
  return ($lines.Count -ge 1 -and $lines[0].Trim() -eq '---')
}

# ---------- 推断元数据 ----------
function Infer-Meta {
  param([string]$RelPath)  # 相对 Root，如 技法库/六要素/对话六要素.md
  $parts = $RelPath -split '/'
  $lib = $parts[0]
  $fileName = $parts[-1]
  $id = [System.IO.Path]::GetFileNameWithoutExtension($fileName)
  $cat = if ($parts.Count -gt 2) { $parts[1] } elseif ($parts.Count -eq 2) { '' } else { '' }
  if ($cat -eq '' -and $lib -eq '技法库') { $cat = '散件' }
  if ($cat -eq '' -and $lib -ne '技法库') { $cat = '未分类' }

  $tags = @()
  switch ($lib) {
    '文风库' { if ($cat) { $tags += $cat }; $tags += '文风DNA' }
    '技法库' { if ($cat -and $cat -ne '散件') { $tags += $cat }; $tags += '通用' }
    '知识库' { if ($cat) { $tags += $cat } }
    default  { if ($cat) { $tags += $cat } }
  }
  $tags = @($tags | Select-Object -Unique)

  return [ordered]@{ id = $id; lib = $lib; cat = $cat; version = '1.0.0'; tags = $tags }
}

# ---------- 生成 frontmatter 文本 ----------
function New-Frontmatter {
  param($Meta)
  $tagStr = '[' + ($Meta.tags -join ', ') + ']'
  return "---`nid: $($Meta.id)`nlib: $($Meta.lib)`ncat: $($Meta.cat)`nversion: $($Meta.version)`ntags: $tagStr`n---`n"
}

# ---------- 主流程 ----------
$libraries = Get-ChildItem -LiteralPath $Root -Directory | Sort-Object Name
$toProcess = @()

foreach ($lib in $libraries) {
  $libName = $lib.Name
  # 收集 bundle 目录（跳过其内部文件）
  $bundleDirs = @()
  $allDirs = Get-ChildItem -LiteralPath $lib.FullName -Directory -Recurse -ErrorAction SilentlyContinue
  foreach ($d in $allDirs) {
    if (Get-ChildItem -LiteralPath $d.FullName -File -Filter '00-*.md' -ErrorAction SilentlyContinue) { $bundleDirs += $d }
  }
  $bundlePaths = @{}
  foreach ($bd in $bundleDirs) { $bundlePaths[$bd.FullName] = $true }

  $allMd = Get-ChildItem -LiteralPath $lib.FullName -File -Filter '*.md' -Recurse -ErrorAction SilentlyContinue
  foreach ($f in $allMd) {
    $inBundle = $false
    foreach ($bp in $bundlePaths.Keys) { if ($f.Directory.FullName.StartsWith($bp)) { $inBundle = $true; break } }
    if ($inBundle) { continue }
    if (Has-Frontmatter $f.FullName) { continue }

    $rel = $f.FullName.Substring($Root.Length).TrimStart('\').Replace('\','/')
    $meta = Infer-Meta $rel
    $toProcess += [pscustomobject]@{ Path = $f.FullName; Rel = $rel; Meta = $meta }
  }
}

# ---------- 输出 ----------
Write-Output "待补齐 frontmatter: $($toProcess.Count) 个文件"
if (-not $Apply) {
  Write-Output "== dry-run 预览（前 15 个）=="
  $toProcess | Select-Object -First 15 | ForEach-Object {
    Write-Output "  $($_.Rel)"
    Write-Output "    -> id=$($_.Meta.id) lib=$($_.Meta.lib) cat=$($_.Meta.cat) tags=[$($_.Meta.tags -join ',')]"
  }
  Write-Output ""
  Write-Output "加 -Apply 参数才会实际写入。"
  exit 0
}

# ---------- 应用 ----------
$written = 0; $failed = 0
foreach ($item in $toProcess) {
  try {
    $r = Read-File $item.Path
    $fm = New-Frontmatter $item.Meta
    $newContent = $fm + $r.content
    $enc = New-Object System.Text.UTF8Encoding($true)
    [System.IO.File]::WriteAllText($item.Path, $newContent, $enc)
    $written++
  } catch {
    $failed++
    Write-Output "  ! 写入失败: $($item.Rel) :: $($_.Exception.Message)"
  }
}
Write-Output "写入完成: $written 个，失败 $failed 个"
