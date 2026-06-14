#!/usr/bin/env python3
"""
SEO Pipeline — 全自动 SEO 内容生产流水线

用法:
    python3 seo_pipeline.py "your keyword here"

流程:
    Step 1: 抓取 Google SERP (含 People Also Ask)
    Step 2: 分析 SERP — 内容类型、缺口、框架建议
    Step 3: 输出完整简报 (JSON + Markdown)
    Step 4: 交给 AI 按照 SEOSKILL.md SOP 写文章
"""

import json
import os
import re
import subprocess
import sys
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')


def run_serp_scraper(keyword: str, num_results: int = 20) -> bool:
    """运行 SERP 爬虫"""
    print("\n" + "=" * 80)
    print("📡 Step 1: 抓取 Google SERP")
    print("=" * 80)

    script = os.path.join(BASE_DIR, 'google_serp_scraper.py')
    cmd = ['python3', script, keyword, str(num_results)]

    try:
        result = subprocess.run(cmd, capture_output=False, text=True, timeout=120)
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("⚠️  SERP 抓取超时 (120s)，可能网络问题")
        return False
    except Exception as e:
        print(f"❌ SERP 抓取失败: {e}")
        return False


def run_serp_analyzer(keyword: str) -> dict:
    """运行 SERP 分析器"""
    print("\n" + "=" * 80)
    print("📊 Step 2: 分析 SERP 数据")
    print("=" * 80)

    safe_name = re.sub(r'[^\w\s-]', '', keyword).strip().replace(' ', '_').lower()
    analysis_path = os.path.join(DATA_DIR, f'{safe_name}_serp_analysis.json')

    if os.path.exists(analysis_path):
        with open(analysis_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    script = os.path.join(BASE_DIR, 'serp_analyzer.py')
    cmd = ['python3', script, keyword]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0 and os.path.exists(analysis_path):
            with open(analysis_path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"❌ 分析失败: {e}")

    return {}


def load_serp_data(keyword: str) -> dict:
    """加载 SERP 原始数据"""
    safe_name = re.sub(r'[^\w\s-]', '', keyword).strip().replace(' ', '_').lower()
    filepath = os.path.join(BASE_DIR, f'{safe_name}_serp_results.json')
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def generate_brief(keyword: str, serp_data: dict, analysis: dict) -> str:
    """生成完整的内容简报 (供 AI 写作使用)"""
    serp = serp_data.get('serp', [])
    paa = serp_data.get('paa_questions', [])
    ana = analysis.get('analysis', {})
    gaps = analysis.get('content_gaps', [])
    frame = analysis.get('framework_guide', {})

    lines = []
    lines.append(f"# SEO Content Brief: {keyword}")
    lines.append("")
    lines.append(f"> 自动生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"> 目标: 生成可直接发布的英文 SEO 博客文章")
    lines.append("")
    lines.append("---")
    lines.append("")

    # 基础信息
    lines.append("## 1. 基础信息")
    lines.append("")
    lines.append(f"- **主关键词**: `{keyword}`")
    lines.append(f"- **搜索意图**: {ana.get('search_intent', 'informational')}")
    lines.append(f"- **主导内容类型**: {ana.get('dominant_content_type', 'article')}")
    lines.append(f"- **推荐框架**: {ana.get('recommended_framework', 'hybrid')}")
    lines.append(f"- **分析竞品数**: {ana.get('total_competitors_analyzed', 0)}")
    lines.append("")

    # 内容类型分布
    ct_dist = ana.get('content_type_distribution', {})
    if ct_dist:
        lines.append("## 2. SERP 内容类型分布")
        lines.append("")
        lines.append("| 类型 | 数量 |")
        lines.append("|------|------|")
        for ct, count in ct_dist.items():
            lines.append(f"| {ct} | {count} |")
        lines.append("")

    # Top 竞品
    lines.append("## 3. Top 排名竞品 (前 10)")
    lines.append("")
    for r in serp[:10]:
        lines.append(f"**#{r['rank']}** [{r['title']}]({r['url']})")
        lines.append(f"- 域名: `{r.get('domain', 'N/A')}`")
        desc = r.get('description', '')
        if desc:
            lines.append(f"- 摘要: {desc[:200]}")
        lines.append("")

    # PAA 问题
    if paa:
        lines.append("## 4. People Also Ask 问题 (可用于 FAQ)")
        lines.append("")
        for q in paa[:20]:
            lines.append(f"- {q}")
        lines.append("")

    # 内容缺口
    if gaps:
        lines.append("## 5. 识别的内容缺口")
        lines.append("")
        for g in gaps:
            lines.append(f"### 🔴 {g.get('type', '')}")
            lines.append(f"- **缺口**: {g.get('description', '')}")
            lines.append(f"- **机会**: {g.get('opportunity', '')}")
            lines.append("")

    # 推荐结构
    if frame:
        lines.append("## 6. 推荐文章结构")
        lines.append("")
        lines.append(f"**推荐 H1**: `{frame.get('h1_pattern', '')}`")
        lines.append("")
        lines.append("**H2/H3 结构**:")
        for item in frame.get('structure', []):
            lines.append(f"- {item}")
        lines.append("")

    # 关键词矩阵建议
    lines.append("## 7. 关键词矩阵建议")
    lines.append("")
    lines.append("请在以下位置部署关键词:")
    lines.append("- **H1**: 包含核心关键词 + 年份 + 价值词 (best/guide/complete)")
    lines.append("- **H2**: 每 2-3 个 H2 含一个长尾变体")
    lines.append("- **FAQ**: 用 PAA 问题作为 FAQ 的 H3")
    lines.append("- **正文**: 自然融入 semantic support 词")
    lines.append("- **Meta Description**: 含核心关键词 + 价值主张")
    lines.append("")

    # SEO 元数据建议
    lines.append("## 8. SEO 元数据建议")
    lines.append("")
    lines.append(f"- **URL Slug**: `/{keyword.replace(' ', '-').lower()}`")
    lines.append(f"- **Meta Title**: {frame.get('h1_pattern', keyword.title())} (约 55-60 字符)")
    lines.append(f"- **Meta Description**: 含关键词 + 价值主张 + CTA，约 150-160 字符")
    lines.append("")

    # 竞品 URL 列表 (供内容抓取)
    lines.append("## 9. 竞品 URL 列表 (供深度内容分析)")
    lines.append("")
    for r in serp[:5]:
        lines.append(f"- [{r['title'][:80]}]({r['url']})")
    lines.append("")

    # 写作指令
    lines.append("---")
    lines.append("")
    lines.append("## 10. 写作指令")
    lines.append("")
    lines.append("请按照 SEOSKILL.md 的 SOP 流程生产文章:")
    lines.append("")
    lines.append("1. 使用上方推荐的结构框架 (H1/H2/H3)")
    lines.append("2. 抓取 Top 3-5 竞品页面，分析其 H2/H3 结构和内容深度")
    lines.append("3. 生成完整 Draft (英文，可直接发布)")
    lines.append("4. 执行 Critique Round 1 (事实/逻辑/合规检查)")
    lines.append("5. 修订后执行 Critique Round 2 (7维度评分)")
    lines.append("6. 输出最终发布包 (正文 + SEO Pack + FAQ)")
    lines.append("")
    lines.append("**关键要求:**")
    lines.append("- 默认输出英文文章")
    lines.append("- 必须有完整正文，不可只给提纲")
    lines.append("- 必须包含: Meta title, Meta description, URL slug, FAQ, 图片ALT建议")
    lines.append("- 不得有「—」破折号")
    lines.append("- 不得编造数据或来源")
    lines.append("")

    return '\n'.join(lines)


def main():
    print("""
╔══════════════════════════════════════════════════════════╗
║         SEO Pipeline — 全自动内容生产流水线              ║
╚══════════════════════════════════════════════════════════╝
    """)

    if len(sys.argv) < 2:
        print("用法: python3 seo_pipeline.py \"your keyword\" [结果数量]")
        print("示例: python3 seo_pipeline.py 'best ai website builder'")
        print("      python3 seo_pipeline.py 'how to start a blog' 15")
        sys.exit(1)

    keyword = ' '.join(sys.argv[1:]).strip()
    num_results = 20

    if keyword.split()[-1].isdigit():
        parts = keyword.split()
        num_results = int(parts[-1])
        keyword = ' '.join(parts[:-1])

    print(f"🎯 目标关键词: {keyword}")
    print(f"📊 目标结果数: {num_results}")
    print(f"📁 工作目录: {BASE_DIR}")
    print()

    # Step 1: 抓取 SERP
    success = run_serp_scraper(keyword, num_results)
    time.sleep(1)

    # Step 2: 加载 SERP 数据
    serp_data = load_serp_data(keyword)
    if not serp_data.get('serp'):
        print("⚠️  SERP 数据为空，无法继续分析")
        if not success:
            print("💡 请确认网络连接正常，Google 可访问")
        sys.exit(1)

    # Step 3: 分析 SERP
    analysis = run_serp_analyzer(keyword)
    time.sleep(1)

    # Step 4: 生成简报
    print("\n" + "=" * 80)
    print("📝 Step 3: 生成内容简报")
    print("=" * 80)

    brief = generate_brief(keyword, serp_data, analysis)

    safe_name = re.sub(r'[^\w\s-]', '', keyword).strip().replace(' ', '_').lower()
    brief_path = os.path.join(DATA_DIR, f'{safe_name}_content_brief.md')
    with open(brief_path, 'w', encoding='utf-8') as f:
        f.write(brief)

    print(f"\n✅ 简报已生成: {brief_path}")

    # 汇总
    print("\n" + "=" * 80)
    print("📋 流水线完成 - 输出文件汇总")
    print("=" * 80)
    print(f"""
  1. SERP 原始数据: {safe_name}_serp_results.json
  2. SERP 分析结果: {safe_name}_serp_analysis.json
  3. 内容简报:     {safe_name}_content_brief.md

  📌 下一步:
     将内容简报交给 AI，按 SEOSKILL.md SOP 生成完整文章
     包括: 正文 + Meta title + Meta description + URL slug + FAQ
    """)


if __name__ == '__main__':
    main()
