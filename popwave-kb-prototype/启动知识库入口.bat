@echo off
chcp 65001 >nul
title popwave 知识库 · 正式入口
cd /d "%~dp0"
echo ==============================================
echo   popwave 知识库 · 正式入口
echo   正在启动本地服务，稍后自动打开浏览器...
echo   关闭本窗口即停止服务
echo ==============================================
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0server.ps1"
pause
