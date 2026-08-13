# ============================================================
# popwave 知识库 · frontmatter 扫描脚本 (PowerShell)
# 范式验证：frontmatter 为主 + manifest 由脚本生成
# 用法：& .\scan.ps1 [-Root <库根目录>] [-Out <manifest路径>]
# ============================================================
param(
  [string]$Root = "d:\popwave-skills\popwave知识库",
  [string]$Out  = "d:\popwave-skills\popwave知识库\manifest.json"
)
$ErrorActionPreference = 'Stop'

# ---------- 读取 YAML frontmatter（简单解析，覆盖本项目字段） ----------
function Parse-Frontmatter {
  param([string]$Path)
  $lines = Get-Content -LiteralPath $Path -Encoding UTF8
  if ($lines.Count -lt 3) { return $null }
  if ($lines[0].Trim() -ne '---') { return $null }
  $meta = @{}
  for ($i = 1; $i -lt $lines.Count; $i++) {
    $l = $lines[$i]
    if ($l.Trim() -eq '---') { break }
    if ($l -match '^([^:]+):\s*(.*)$') {
      $meta[$Matches[1].Trim()] = $Matches[2].Trim()
    }
  }
  return $meta
}

function Parse-Tags {
  param([string]$v)
  if (-not $v) { return ,@() }
  $v = $v.Trim()
  if ($v -match '^\[(.*)\]$') { $v = $Matches[1] }
  # 一元逗号包裹，防止单元素数组被函数输出解包成标量
  return ,@($v -split ',' | ForEach-Object { $_.Trim().Trim('"').Trim("'") } | Where-Object { $_ -ne '' })
}

# ---------- 统计 ----------
$stats = [ordered]@{ total = 0; withFrontmatter = 0; inferred = 0; bundles = 0; singles = 0; issues = @() }

$libraries = Get-ChildItem -LiteralPath $Root -Directory | Sort-Object Name
$manifest = [ordered]@{ schema = '1.0'; version = '0.1.0'; updatedAt = (Get-Date -Format 'yyyy-MM-dd'); libraries = [ordered]@{} }

foreach ($lib in $libraries) {
  $libName = $lib.Name
  $assets = @()

  # 1) 识别 bundle：含 00-*.md 的文件夹
  $allDirs = Get-ChildItem -LiteralPath $lib.FullName -Directory -Recurse -ErrorAction SilentlyContinue
  $bundleDirs = @()
  foreach ($d in $allDirs) {
    $idx = Get-ChildItem -LiteralPath $d.FullName -File -Filter '00-*.md' -ErrorAction SilentlyContinue
    if ($idx) { $bundleDirs += $d }
  }

  # 2) bundle 资产
  foreach ($bd in $bundleDirs) {
    $files = Get-ChildItem -LiteralPath $bd.FullName -File -Filter '*.md' | Sort-Object Name
    $idxFile = $files | Where-Object { $_.Name -match '^00-' } | Select-Object -First 1
    $meta = Parse-Frontmatter $idxFile.FullName
    $asset = [ordered]@{
      id = $bd.Name
      lib = $libName
      cat = $bd.Parent.Name
      path = $bd.FullName.Substring($Root.Length).TrimStart('\').Replace('\','/')
      version = '1.0.0'
      tags = @()
      desc = ''
      bundle = @($files | ForEach-Object { $_.Name })
    }
    if ($meta) {
      $stats.withFrontmatter++
      if ($meta['id'])    { $asset.id = $meta['id'] }
      if ($meta['cat'])   { $asset.cat = $meta['cat'] }
      if ($meta['version']){ $asset.version = $meta['version'] }
      if ($meta['desc'])  { $asset.desc = $meta['desc'] }
      if ($meta['tags'])  { $asset.tags = Parse-Tags $meta['tags'] }
    } else {
      $stats.inferred++
    }
    $assets += $asset
    $stats.bundles++
  }

  # 3) 单文件资产：不在任何 bundle 目录内的 md
  $bundlePaths = @{}
  foreach ($bd in $bundleDirs) { $bundlePaths[$bd.FullName] = $true }
  $allMd = Get-ChildItem -LiteralPath $lib.FullName -File -Filter '*.md' -Recurse -ErrorAction SilentlyContinue
  foreach ($f in $allMd) {
    $parentDir = $f.Directory.FullName
    $inBundle = $false
    foreach ($bp in $bundlePaths.Keys) { if ($parentDir.StartsWith($bp)) { $inBundle = $true; break } }
    if ($inBundle) { continue }

    $meta = Parse-Frontmatter $f.FullName
    $rel = $f.FullName.Substring($lib.FullName.Length).TrimStart('\')
    $parts = $rel -split '\\'
    $id = [System.IO.Path]::GetFileNameWithoutExtension($f.Name)
    $cat = if ($parts.Count -gt 1) { $parts[0] } else { '' }
    $asset = [ordered]@{
      id = $id
      lib = $libName
      cat = $cat
      path = $f.FullName.Substring($Root.Length).TrimStart('\').Replace('\','/')
      version = '1.0.0'
      tags = @()
      desc = ''
    }
    if ($meta) {
      $stats.withFrontmatter++
      if ($meta['id'])    { $asset.id = $meta['id'] }
      if ($meta['cat'])   { $asset.cat = $meta['cat'] }
      if ($meta['version']){ $asset.version = $meta['version'] }
      if ($meta['desc'])  { $asset.desc = $meta['desc'] }
      if ($meta['tags'])  { $asset.tags = Parse-Tags $meta['tags'] }
    } else {
      $stats.inferred++
    }
    $assets += $asset
    $stats.singles++
  }

  $manifest.libraries[$libName] = [ordered]@{ assets = $assets }
  $stats.total += $assets.Count
}

# ---------- 校验：id 唯一性（按完整相对路径判定） ----------
$seen = @{}
foreach ($libName in $manifest.libraries.Keys) {
  foreach ($a in $manifest.libraries[$libName].assets) {
    $key = $a.path
    if ($seen.ContainsKey($key)) { $stats.issues += "重复路径: $key" }
    else { $seen[$key] = $true }
  }
}
# 同名不同子分类（信息，非错误）
$nameSeen = @{}
foreach ($libName in $manifest.libraries.Keys) {
  foreach ($a in $manifest.libraries[$libName].assets) {
    $nk = "$($a.lib)/$($a.id)"
    if ($nameSeen.ContainsKey($nk)) { $stats.issues += "同名不同子分类: $nk (路径 $($a.path))" }
    else { $nameSeen[$nk] = $true }
  }
}

# ---------- 输出 ----------
$json = $manifest | ConvertTo-Json -Depth 10
[System.IO.File]::WriteAllText($Out, $json, (New-Object System.Text.UTF8Encoding($false)))

Write-Output "== 扫描完成 =="
Write-Output "库数: $($manifest.libraries.Count)"
foreach ($libName in $manifest.libraries.Keys) {
  Write-Output "  - $libName : $($manifest.libraries[$libName].assets.Count) 项"
}
Write-Output "资产总数: $($stats.total)  (bundle $($stats.bundles) / 单文件 $($stats.singles))"
Write-Output "带 frontmatter: $($stats.withFrontmatter) / 推断: $($stats.inferred)"
if ($stats.issues.Count -gt 0) {
  Write-Output "== 问题 =="
  $stats.issues | ForEach-Object { Write-Output "  ! $_" }
} else {
  Write-Output "无 id 冲突"
}
Write-Output "manifest 已写入: $Out"
