#!/usr/bin/env python3
"""
SEO Pipeline Bridge - SERP 数据分析和简报生成 (独立于数据来源)

用法:
    python3 serp_bridge.py <关键词> <serp_json_path>

这个脚本不负责抓取 SERP（SERP 数据可由 Playwright 爬虫或 AI WebSearch 提供），
只负责读取 SERP JSON → 分析 → 输出内容简报。
"""

import json
import os
import re
import sys
import time
from collections import Counter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')


def guess_search_intent(keyword: str) -> str:
    kw_lower = keyword.lower()
    info_patterns = ['how ', 'what ', 'why ', 'when ', 'who ', 'guide', 'tutorial', 'learn', 'tips', 'ideas']
    commercial_patterns = ['best ', 'top ', 'review', 'vs', 'compar', 'pric', 'cheap', 'affordable']
    transactional_patterns = ['buy', 'purchase', 'sign up', 'register', 'download', 'get ', 'free trial']

    scores = {'informational': 0, 'commercial': 0, 'transactional': 0}
    for p in info_patterns:
        if p in kw_lower: scores['informational'] += 1
    for p in commercial_patterns:
        if p in kw_lower: scores['commercial'] += 1
    for p in transactional_patterns:
        if p in kw_lower: scores['transactional'] += 1

    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else 'informational'


def guess_content_type(title: str, url: str) -> str:
    t = (title + ' ' + url).lower()
    if any(x in t for x in ['best ', 'top ', ' ranked', ' vs ', 'comparison', 'compared']):
        return 'listicle'
    if any(x in t for x in ['how to', 'tutorial', 'guide', 'step by step', 'beginner']):
        return 'tutorial'
    if any(x in t for x in ['review', 'tested', 'hands-on']):
        return 'review'
    if any(x in t for x in ['what is', 'definition', 'meaning', 'explained']):
        return 'definition'
    if any(x in t for x in ['faq', 'questions']):
        return 'faq'
    return 'article'


def extract_domain(url: str) -> str:
    m = re.search(r'https?://(?:www\.)?([^/]+)', url)
    return m.group(1) if m else url


def load_serp_data(filepath: str) -> dict:
    if not os.path.exists(filepath):
        print(f"❌ 文件不存在: {filepath}")
        sys.exit(1)
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def analyze(serp_data: dict) -> dict:
    serp = serp_data.get('serp', [])
    paa = serp_data.get('paa_questions', [])
    keyword = serp_data.get('keyword', '')

    domains = Counter()
    content_types = Counter()

    for r in serp:
        domains[r.get('domain', extract_domain(r.get('url', '')))] += 1
        ct = guess_content_type(r.get('title', ''), r.get('url', ''))
        content_types[ct] += 1

    dominant_type = content_types.most_common(1)[0][0] if content_types else 'article'
    intent = guess_search_intent(keyword)

    framework_map = {
        'listicle': 'listicle', 'tutorial': 'tutorial', 'review': 'review',
        'definition': 'hybrid', 'faq': 'hybrid', 'article': 'hybrid',
    }
    framework = framework_map.get(dominant_type, 'hybrid')

    gaps = []
    titles_text = ' '.join([r.get('title', '') for r in serp]).lower()

    if dominant_type != 'tutorial' and not any(x in titles_text for x in ['how to', 'step', 'guide']):
        gaps.append({'type': 'tutorial_opportunity', 'desc': 'SERP缺少教程类内容', 'action': '加入分步教程'})
    if not any(x in titles_text for x in ['vs', 'versus', 'comparison']):
        gaps.append({'type': 'comparison_missing', 'desc': '缺少对比类内容', 'action': '加入对比表或vs段落'})
    if not any(x in titles_text for x in ['faq', 'questions']):
        gaps.append({'type': 'faq_opportunity', 'desc': '前列缺少FAQ结构', 'action': '添加FAQ section'})
    if dominant_type in ['listicle', 'commercial'] and not any(x in titles_text for x in ['price', 'cost', 'budget']):
        gaps.append({'type': 'pricing_missing', 'desc': '商业类缺少价格内容', 'action': '加入价格对比'})

    guides = {
        'listicle': {
            'h1_pattern': f'The Best {keyword.title()} in 2026: Tested & Ranked',
            'structure': [
                'H1: 榜单式标题 (数字 + 年份 + 关键词)',
                'E-E-A-T 引言: 测试方法 + 结论速览 + 更新日期',
                'H2: Quick Picks / At a Glance',
                'H2: What Is [Topic]?',
                'H2: How We Evaluated',
                'H2: Comparison Table',
                'H2: Top N — 逐个展开',
                'H2: Best by Use Case',
                'H2: Pricing Guide',
                'H2: FAQ',
                'H2: Final Verdict',
            ]
        },
        'tutorial': {
            'h1_pattern': f'How to {keyword.replace("how to ", "").title()}: A Complete Step-by-Step Guide',
            'structure': [
                'H1: How to 步骤式标题',
                '引言: 直接回答 + 前置条件',
                'H2: What You Need Before You Start',
                'H2: Step-by-Step Guide (H3 x N)',
                'H2: Common Mistakes to Avoid',
                'H2: Pro Tips',
                'H2: FAQ',
                'H2: Next Steps',
            ]
        },
        'hybrid': {
            'h1_pattern': f'{keyword.title()}: The Complete Guide for 2026',
            'structure': [
                'H1: 完整主题式标题',
                'E-E-A-T 引言段',
                'H2: Quick Answer / Summary',
                'H2: What Is [Topic]?',
                'H2: How It Works / Key Factors',
                'H2: Step-by-Step / How to Choose',
                'H2: FAQ',
                'H2: Conclusion',
            ]
        },
    }

    return {
        'keyword': keyword,
        'search_intent': intent,
        'dominant_content_type': dominant_type,
        'recommended_framework': framework,
        'top_domains': [{'domain': d, 'count': c} for d, c in domains.most_common(10)],
        'content_gaps': gaps,
        'framework_guide': guides.get(framework, guides['hybrid']),
        'paa_questions': paa[:30] if paa else [],
        'serp_count': len(serp),
    }


def print_brief(analysis: dict):
    fg = analysis['framework_guide']

    print("\n" + "=" * 80)
    print("📋 SEO 内容简报")
    print("=" * 80)
    print(f"\n关键词: {analysis['keyword']}")
    print(f"搜索意图: {analysis['search_intent']}")
    print(f"内容类型: {analysis['dominant_content_type']}")
    print(f"推荐框架: {analysis['recommended_framework']}")
    print(f"竞品数: {analysis['serp_count']}")

    print("\n--- Top 域名 ---")
    for d in analysis['top_domains'][:5]:
        print(f"  {d['domain']} ({d['count']} 条)")

    print("\n--- 内容缺口 ---")
    for g in analysis['content_gaps']:
        print(f"  🔴 {g['type']}: {g['action']}")

    print("\n--- 推荐 H1 ---")
    print(f"  {fg['h1_pattern']}")

    print("\n--- 推荐结构 ---")
    for s in fg['structure']:
        print(f"  {s}")

    if analysis['paa_questions']:
        print("\n--- PAA 问题 (可用于 FAQ) ---")
        for q in analysis['paa_questions'][:10]:
            print(f"  Q: {q}")

    print("\n" + "=" * 80)


def main():
    if len(sys.argv) < 2:
        print("用法: python3 serp_bridge.py <关键词> [serp_json_path]")
        print("示例: python3 serp_bridge.py 'best ai website builder'")
        print("      python3 serp_bridge.py 'best ai website builder' my_serp.json")
        sys.exit(1)

    keyword = ' '.join(sys.argv[1:]).strip()

    # 尝试自动找 SERP JSON
    if len(sys.argv) == 2 or not os.path.exists(sys.argv[2]):
        safe_name = re.sub(r'[^\w\s-]', '', keyword).strip().replace(' ', '_').lower()
        json_path = os.path.join(BASE_DIR, f'{safe_name}_serp_results.json')
        if not os.path.exists(json_path):
            print(f"❌ 未找到 SERP 数据: {json_path}")
            print("💡 请先抓取 SERP 数据: python3 google_serp_scraper.py \"{keyword}\"")
            print("   或手动创建 JSON 文件")
            sys.exit(1)
    else:
        json_path = sys.argv[2]

    print(f"📂 加载 SERP: {json_path}")
    data = load_serp_data(json_path)
    analysis = analyze(data)
    print_brief(analysis)

    # 保存分析结果
    safe_name = re.sub(r'[^\w\s-]', '', keyword).strip().replace(' ', '_').lower()
    out_path = os.path.join(DATA_DIR, f'{safe_name}_serp_analysis.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)
    print(f"\n📁 分析结果: {out_path}")


if __name__ == '__main__':
    main()
