# ============================================================
# popwave 知识库 · 正式静态入口服务 (PowerShell HttpListener)
# 用法:
#   & .\server.ps1                 # 默认端口 8899，自动开浏览器
#   & .\server.ps1 -Port 9000      # 指定端口
#   & .\server.ps1 -NoBrowser      # 不自动开浏览器
# ============================================================
param(
  [int]$Port = 8899,
  [switch]$NoBrowser
)
$ErrorActionPreference = 'Stop'

# 服务根目录：d:\popwave-skills（同时承载原型与知识库目录）
$root = 'd:\popwave-skills'
# 默认入口：原型首页
$entry = '/popwave-kb-prototype/index.html'

# ---------- 自动挑选空闲端口 ----------
$listener = New-Object System.Net.HttpListener
$chosen = $Port
while ($true) {
  try {
    $listener.Prefixes.Clear()
    $listener.Prefixes.Add("http://localhost:$chosen/")
    $listener.Start()
    break
  } catch {
    if ($chosen -gt $Port + 20) { throw "无法找到空闲端口 (起始 $Port)" }
    $chosen++
  }
}

Write-Output "=============================================="
Write-Output " popwave 知识库 · 正式入口"
Write-Output " 地址 : http://localhost:$chosen/popwave-kb-prototype/"
Write-Output " 根目录: $root"
Write-Output " 按 Ctrl+C 停止服务"
Write-Output "=============================================="

if (-not $NoBrowser) {
  Start-Process "http://localhost:$chosen/popwave-kb-prototype/"
}

$mime = @{
  '.html' = 'text/html; charset=utf-8'
  '.json' = 'application/json; charset=utf-8'
  '.md'   = 'text/markdown; charset=utf-8'
  '.css'  = 'text/css; charset=utf-8'
  '.js'   = 'application/javascript; charset=utf-8'
  '.png'  = 'image/png'
  '.jpg'  = 'image/jpeg'
  '.jpeg' = 'image/jpeg'
  '.gif'  = 'image/gif'
  '.svg'  = 'image/svg+xml'
  '.webp' = 'image/webp'
  '.woff2'= 'font/woff2'
}

while ($listener.IsListening) {
  $ctx = $listener.GetContext()
  $req = $ctx.Request
  $res = $ctx.Response
  try {
    $urlPath = [Uri]::UnescapeDataString($req.Url.AbsolutePath)
    if ($urlPath -eq '/' -or $urlPath -eq '') { $urlPath = $entry }
    $fsPath = Join-Path $root ($urlPath.TrimStart('/').Replace('/', [IO.Path]::DirectorySeparatorChar))
    if (Test-Path -LiteralPath $fsPath -PathType Container) {
      $fsPath = Join-Path $fsPath 'index.html'
    }
    if (Test-Path -LiteralPath $fsPath -PathType Leaf) {
      $ext = [IO.Path]::GetExtension($fsPath).ToLower()
      $ct = if ($mime.ContainsKey($ext)) { $mime[$ext] } else { 'application/octet-stream' }
      $bytes = [IO.File]::ReadAllBytes($fsPath)
      $res.ContentType = $ct
      $res.ContentLength64 = $bytes.Length
      $res.OutputStream.Write($bytes, 0, $bytes.Length)
    } else {
      $res.StatusCode = 404
      $msg = [Text.Encoding]::UTF8.GetBytes("404 Not Found: $urlPath")
      $res.OutputStream.Write($msg, 0, $msg.Length)
    }
  } catch {
    $res.StatusCode = 500
  } finally {
    $res.OutputStream.Close()
  }
}
