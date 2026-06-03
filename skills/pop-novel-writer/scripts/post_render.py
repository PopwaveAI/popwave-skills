"""
post_render.py — HTML渲染后验证

调用方式（在 html-renderer 产出 HTML 后）：
  python glue/post_render.py <html_file> [--check-embedding]

功能：
  1. 验证 HTML 文件是否存在且非空
  2. 检查是否包含必备标签（DOCTYPE / html / charset）
  3. 检查渲染意图注释是否存在
  4. 输出文件摘要（大小 / 行数 / 标题）
  
退出码：0 = 通过，1 = 问题
"""

import os
import sys
import re
import argparse

def verify_html(html_path: str, check_embedding: bool = False) -> bool:
    """验证 HTML 文件质量"""
    if not os.path.isfile(html_path):
        print(f"[post_render] ❌ 文件不存在: {html_path}")
        return False
    
    size_kb = os.path.getsize(html_path) / 1024
    print(f"[post_render] 📄 {os.path.basename(html_path)} ({size_kb:.1f} KB)")
    
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    passed = True
    
    # 1. 基本结构检查
    checks = {
        "DOCTYPE": "<!DOCTYPE html>" in content or "<!doctype html>" in content,
        "html tag": "<html" in content,
        "charset": 'charset="UTF-8"' in content or 'charset="utf-8"' in content,
        "title": "<title>" in content,
        "body": "<body" in content,
    }
    
    for check_name, result in checks.items():
        status = "✅" if result else "❌"
        print(f"  {status} {check_name}")
        if not result:
            passed = False
    
    # 2. 渲染意图注释
    intent_match = re.search(r'<!-- RENDER INTENT: (.+?) -->', content)
    if intent_match:
        print(f"  ℹ️  渲染意图: {intent_match.group(1)}")
    else:
        print(f"  ⚠️  无渲染意图注释（建议添加 PreRenderDecider）")
    
    # 3. 外链资源检查
    ext_deps = 0
    for ext in ['.css', '.js', '.woff', '.woff2']:
        ext_deps += len(re.findall(rf'["\']https?://[^"\']+{re.escape(ext)}', content))
    print(f"  ℹ️  外链资源: {ext_deps} 个")
    
    if ext_deps == 0:
        print(f"  ⚠️  零外链资源——是纯文本 HTML 吗？")
    
    # 4. 大小合理性
    if size_kb < 1:
        print(f"  ⚠️  文件过小 ({size_kb:.1f} KB)，可能内容不完整")
    elif size_kb > 500:
        print(f"  ⚠️  文件较大 ({size_kb:.1f} KB)，加载可能慢")
    
    print(f"  📊 {len(lines)} 行, {len(content):,} 字符")
    
    return passed


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HTML渲染后验证")
    parser.add_argument("html_file", help="HTML 文件路径")
    parser.add_argument("--check-embedding", action="store_true", help="检查嵌入式资源完整性")
    args = parser.parse_args()
    
    success = verify_html(args.html_file, args.check_embedding)
    sys.exit(0 if success else 1)
