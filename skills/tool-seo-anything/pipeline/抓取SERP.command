#!/bin/bash
# 双击运行此脚本抓取 Google SERP
# 使用前请先运行一次"安装依赖"（见安装说明.md）

cd "$(dirname "$0")"

echo "=========================================="
echo "   Google SERP 抓取工具"
echo "=========================================="
echo ""

if [ -z "$1" ]; then
    echo "请输入要抓取的关键词（例如: ai marketing）:"
    read keyword
else
    keyword="$1"
fi

if [ -z "$keyword" ]; then
    keyword="ai marketing"
    echo "使用默认关键词: $keyword"
fi

echo ""
echo "正在抓取关键词: $keyword"
echo "请稍候..."
echo ""

python3 google_serp_scraper.py "$keyword" 20

echo ""
echo "=========================================="
echo "抓取完成！结果已保存到当前目录"
echo "=========================================="
echo ""

read -n 1 -s -r -p "按任意键退出..."
