@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ==========================================
echo    Google SERP 抓取工具
echo ==========================================
echo.

set /p keyword=请输入要抓取的关键词（例如: ai marketing）:

if "%keyword%"=="" (
    set keyword=ai marketing
    echo 使用默认关键词: ai marketing
)

echo.
echo 正在抓取关键词: %keyword%
echo 请稍候...
echo.

python google_serp_scraper.py "%keyword%" 20

echo.
echo ==========================================
echo 抓取完成！结果已保存到当前目录
echo ==========================================
echo.
pause
