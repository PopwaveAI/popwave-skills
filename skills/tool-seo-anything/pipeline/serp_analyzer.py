#!/usr/bin/env python3
"""
SERP Analyzer - 分析 Google SERP 结果，提取竞品结构、内容缺口、框架建议
输出结构化分析报告供 SEO 文章生成使用
"""

import json
import os
import re
import sys
from collections import Counter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')


def load_serp_results(keyword: str) -> dict:
    """加载 SERP 抓取结果"""
    safe_name = re.sub(r'[^\w\s-]', '', keyword).strip().replace(' ', '_').lower()
    filepath = os.path.join(DATA_DIR, f'{safe_name}_serp_results.json')
    if not os.path.exists(filepath):
        alt_path = os.path.join(DATA_DIR, f'{keyword.replace(" ", "_")}_serp_results.json')
        if os.path.exists(alt_path):
            filepath = alt_path
        else:
            print(f"❌ 未找到 SERP 结果文件: {filepath}")
            sys.exit(1)
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def guess_search_intent(keyword: str) -> str:
    """猜测搜索意图"""
    kw_lower = keyword.lower()
    info_patterns = ['how ', 'what ', 'why ', 'when ', 'who ', 'guide', 'tutorial', 'learn', 'tips', 'ideas']
    commercial_patterns = ['best ', 'top ', 'review', 'vs', 'compar', 'pric', 'cheap', 'affordable', 'premium']
    transactional_patterns = ['buy', 'purchase', 'sign up', 'register', 'download', 'get ', 'free trial']
    navigational_patterns = ['login', 'official', 'website', 'homepage']

    scores = {'informational': 0, 'commercial': 0, 'transactional': 0, 'navigational': 0}

    for p in info_patterns:
        if p in kw_lower:
            scores['informational'] += 1
    for p in commercial_patterns:
        if p in kw_lower:
            scores['commercial'] += 1
    for p in transactional_patterns:
        if p in kw_lower:
            scores['transactional'] += 1
    for p in navigational_patterns:
        if p in kw_lower:
            scores['navigational'] += 1

    best = max(scores, key=scores.get)
    if scores[best] == 0:
        return 'informational'
    return best


def guess_content_type(title: str, url: str) -> str:
    """根据标题和 URL 猜测内容类型"""
    t = (title + ' ' + url).lower()
    if any(x in t for x in ['best ', 'top ', ' ranked', ' vs ', 'comparison', 'compared']):
        return 'listicle'
    if any(x in t for x in ['how to', 'tutorial', 'guide', 'step by step', 'beginner']):
        return 'tutorial'
    if any(x in t for x in ['review', 'tested', 'hands-on', 'honest']):
        return 'review'
    if any(x in t for x in ['what is', 'definition', 'meaning', 'explained']):
        return 'definition'
    if any(x in t for x in ['faq', 'questions', 'answered']):
        return 'faq'
    if any(x in t for x in ['price', 'pricing', 'cost', 'cheap', 'free']):
        return 'commercial'
    return 'article'


def analyze_serp(data: dict) -> dict:
    """分析 SERP 数据"""
    serp = data.get('serp', [])
    paa = data.get('paa_questions', [])
    keyword = data.get('keyword', '')

    # 基础统计
    domains = Counter()
    content_types = Counter()
    title_patterns = []

    for r in serp:
        domains[r.get('domain', 'unknown')] += 1
        ct = guess_content_type(r.get('title', ''), r.get('url', ''))
        content_types[ct] += 1
        title_patterns.append(r.get('title', ''))

    # 识别主导内容类型
    dominant_type = content_types.most_common(1)[0][0] if content_types else 'article'

    # 搜索意图
    intent = guess_search_intent(keyword)

    # 框架推荐
    framework_map = {
        'listicle': 'listicle',
        'tutorial': 'tutorial',
        'review': 'review',
        'definition': 'hybrid',
        'faq': 'hybrid',
        'commercial': 'listicle',
        'article': 'hybrid',
    }
    framework = framework_map.get(dominant_type, 'hybrid')

    # PAA 问题分类
    paa_by_topic = []
    for q in paa:
        q_clean = q.strip().rstrip('?').rstrip('.').strip()
        if q_clean:
            paa_by_topic.append(q_clean)

    return {
        'keyword': keyword,
        'search_intent': intent,
        'dominant_content_type': dominant_type,
        'content_type_distribution': dict(content_types.most_common()),
        'top_domains': [{'domain': d, 'count': c} for d, c in domains.most_common(10)],
        'recommended_framework': framework,
        'paa_questions': paa_by_topic[:30],
        'total_competitors_analyzed': len(serp),
        'serp_titles': [r['title'] for r in serp[:20]],
    }


def identify_content_gaps(analysis: dict) -> list:
    """识别内容缺口"""
    gaps = []
    ct = analysis.get('dominant_content_type', 'article')
    titles = analysis.get('serp_titles', [])
    titles_text = ' '.join(titles).lower()

    # 检查是否缺少教程类内容
    if ct != 'tutorial' and not any(x in titles_text for x in ['how to', 'step', 'guide']):
        gaps.append({
            'type': 'tutorial_missing',
            'description': 'SERP 中缺少教程/分步指南类内容',
            'opportunity': '可提供完整的 How-to 教程，抢占信息型搜索流量'
        })

    # 检查是否缺少对比类内容
    if not any(x in titles_text for x in ['vs', 'versus', 'comparison']):
        gaps.append({
            'type': 'comparison_missing',
            'description': 'SERP 中缺少直接对比类内容',
            'opportunity': '可做工具/方案对比表，占据商业调查型搜索'
        })

    # 检查是否有 FAQ 缺口
    if not any(x in titles_text for x in ['faq', 'questions', 'common ']):
        gaps.append({
            'type': 'faq_opportunity',
            'description': 'SERP 前列缺少 FAQ 结构',
            'opportunity': '可在文章末尾添加 FAQ section，抢占 People Also Ask 流量'
        })

    # 检查是否需要价格/预算内容
    if ct in ['listicle', 'commercial'] and not any(x in titles_text for x in ['price', 'cost', 'budget', 'free']):
        gaps.append({
            'type': 'pricing_missing',
            'description': '商业类 SERP 缺少价格/预算相关内容',
            'opportunity': '可加入价格对比表或不同预算选择建议'
        })

    return gaps


def generate_framework_guide(analysis: dict) -> dict:
    """根据框架生成结构指南"""
    framework = analysis['recommended_framework']
    keyword = analysis['keyword']

    guides = {
        'listicle': {
            'structure': [
                'H1: 包含数字 + 年份 + 核心关键词的标题',
                'E-E-A-T 引言段: 测试方法 + 结论速览 + 更新日期',
                'H2: Quick Picks / At a Glance (快速选择表)',
                'H2: What Is [Topic]? (定义段)',
                'H2: Do You Actually Need [Topic]? (适用判断)',
                'H2: How We Evaluated / Chose (评选标准)',
                'H2: Comparison Table (完整对比表)',
                'H2: Top N [Items] — 逐个展开 (每个含评分、优缺点、适合谁)',
                'H2: Best by Use Case (按场景推荐)',
                'H2: Pricing / How Much Does It Cost (价格指南)',
                'H2: Benefits / Why Use (好处)',
                'H2: Limitations / Common Myths (限制与误区)',
                'H2: FAQ',
                'H2: Final Verdict / Conclusion',
            ],
            'h1_pattern': f'The {keyword.title()} in 2026: Tested & Ranked',
        },
        'tutorial': {
            'structure': [
                'H1: How to [Achieve Goal] (步骤式标题)',
                '引言: 直接回答问题 + 前置条件说明',
                'H2: What You Need Before You Start (前置要求)',
                'H2: Step-by-Step Guide (分步操作)',
                'H3: Step 1: ...',
                'H3: Step 2: ...',
                'H2: Common Mistakes to Avoid (常见错误)',
                'H2: Pro Tips / Advanced (进阶技巧)',
                'H2: FAQ',
                'H2: What\'s Next (下一步)',
            ],
            'h1_pattern': f'How to {keyword.replace("how to ", "").title()}: A Step-by-Step Guide',
        },
        'review': {
            'structure': [
                'H1: [Product] Review: 包含核心结论的标题',
                '引言: 明确结论 + 测试条件',
                'H2: Quick Verdict (结论速览)',
                'H2: Pros and Cons (优缺点)',
                'H2: In-Depth Analysis (深度分析，按维度展开)',
                'H2: Who Is It For / Not For (适合谁)',
                'H2: Alternatives (替代方案)',
                'H2: FAQ',
                'H2: Final Verdict',
            ],
            'h1_pattern': f'{keyword.title()} Review: Is It Worth It in 2026?',
        },
        'hybrid': {
            'structure': [
                'H1: 完整的主题式标题',
                'E-E-A-T 引言段: 直接回答 + 权威信号',
                'H2: Quick Answer / Summary',
                'H2: What Is [Topic]?',
                'H2: How [Topic] Works',
                'H2: Key Factors / Main Approaches',
                'H2: Step-by-Step / How to Choose',
                'H2: Common Questions / FAQ',
                'H2: Conclusion / Next Steps',
            ],
            'h1_pattern': f'{keyword.title()}: The Complete Guide for 2026',
        },
    }

    return guides.get(framework, guides['hybrid'])


def print_analysis(analysis: dict, gaps: list, framework_guide: dict):
    """打印分析报告"""
    print("\n" + "=" * 80)
    print("📊 SERP 分析报告")
    print("=" * 80)

    print(f"\n关键词: {analysis['keyword']}")
    print(f"搜索意图: {analysis['search_intent']}")
    print(f"主导内容类型: {analysis['dominant_content_type']}")
    print(f"推荐框架: {analysis['recommended_framework']}")
    print(f"分析竞品数: {analysis['total_competitors_analyzed']}")

    print("\n--- 内容类型分布 ---")
    for ct, count in analysis['content_type_distribution'].items():
        bar = '█' * count
        print(f"  {ct:15s} {bar} ({count})")

    print("\n--- Top 域名 ---")
    for d in analysis['top_domains'][:5]:
        print(f"  {d['domain']} ({d['count']} 条)")

    print("\n--- 内容缺口 ---")
    for g in gaps:
        print(f"  🔴 {g['type']}")
        print(f"     {g['description']}")
        print(f"     💡 {g['opportunity']}")

    print("\n--- 推荐文章结构 ---")
    for item in framework_guide['structure']:
        print(f"  {item}")
    print(f"\n  推荐 H1: {framework_guide['h1_pattern']}")

    if analysis['paa_questions']:
        print("\n--- PAA 问题 (可用于 FAQ) ---")
        for q in analysis['paa_questions'][:15]:
            print(f"  Q: {q}?")

    print("\n--- SERP 标题参考 ---")
    for i, t in enumerate(analysis['serp_titles'][:10], 1):
        print(f"  {i}. {t}")

    print("\n" + "=" * 80)


def save_analysis(analysis, gaps, framework_guide):
    """保存分析结果"""
    safe_name = re.sub(r'[^\w\s-]', '', analysis['keyword']).strip().replace(' ', '_').lower()
    filepath = os.path.join(DATA_DIR, f'{safe_name}_serp_analysis.json')

    output = {
        'analysis': analysis,
        'content_gaps': [{'type': g['type'], 'description': g['description'], 'opportunity': g['opportunity']} for g in gaps],
        'framework_guide': framework_guide,
    }

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n📁 分析结果已保存: {filepath}")
    return filepath


def main():
    if len(sys.argv) < 2:
        print("用法: python3 serp_analyzer.py <关键词>")
        print("示例: python3 serp_analyzer.py 'best ai website builder'")
        sys.exit(1)

    keyword = ' '.join(sys.argv[1:]).strip()
    print(f"\n🔍 正在分析 SERP 数据: {keyword}")

    data = load_serp_results(keyword)
    analysis = analyze_serp(data)
    gaps = identify_content_gaps(analysis)
    framework_guide = generate_framework_guide(analysis)

    print_analysis(analysis, gaps, framework_guide)
    save_analysis(analysis, gaps, framework_guide)


if __name__ == '__main__':
    main()
