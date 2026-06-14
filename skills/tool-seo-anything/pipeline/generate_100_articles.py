#!/usr/bin/env python3
import csv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'data', 'keywords')

from collections import defaultdict
import xml.etree.ElementTree as ET

def parse_volume(vol_str):
    if not vol_str or vol_str in ['-', '', '0']:
        return 0
    try:
        vol_str = str(vol_str).replace('K','000').replace('M','000000').replace('.','').replace('−','-').replace(',','').replace(' ','').replace('+','')
        return int(float(vol_str))
    except:
        return 0

# 读取产品功能词
print("=== 步骤1: 读取产品功能词 ===")
product_keywords = []
with open('/tmp/product_xlsx/xl/worksheets/sheet2.xml', 'r') as f:
    content = f.read()
    root = ET.fromstring(content)
    ns = {'ns': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
    rows = root.findall('.//ns:row', ns)
    
    for row in rows[1:]:
        cells = row.findall('ns:c', ns)
        if len(cells) >= 3:
            kw_cell = cells[0]
            t_elem = kw_cell.find('.//ns:t', ns)
            v_elem = kw_cell.find('ns:v', ns)
            keyword = ''
            if t_elem is not None and t_elem.text:
                keyword = t_elem.text.strip()
            elif v_elem is not None and v_elem.text:
                keyword = v_elem.text.strip()
            
            vol_cell = cells[2]
            v_elem = vol_cell.find('ns:v', ns)
            volume_raw = v_elem.text if v_elem is not None else '0'
            volume = parse_volume(volume_raw)
            
            if keyword and keyword not in ['核心关键词', ''] and len(keyword) > 2:
                product_keywords.append({
                    'keyword': keyword,
                    'volume': volume,
                    'volume_raw': volume_raw,
                    'source': '产品词库'
                })

print(f"产品功能词库: {len(product_keywords)} 个关键词")

# 读取竞品关键词
print("\n=== 步骤2: 读取竞品功能词 ===")
files = {
    'Linktree': os.path.join(DATA_DIR, 'linktree_keywords_full.csv'),
    'vidIQ': os.path.join(DATA_DIR, 'vidiq_keywords_fixed.csv'),
    'TubeBuddy': os.path.join(DATA_DIR, 'tubebuddy_keywords_fixed.csv'),
    '10web': os.path.join(DATA_DIR, '10web_keywords_fixed.csv'),
    'Wix': os.path.join(DATA_DIR, 'wix_keywords_fixed.csv'),
    'Durable': os.path.join(DATA_DIR, 'durable_keywords_fixed.csv'),
    'Viewstats': os.path.join(DATA_DIR, 'viewstats_keywords_fixed.csv'),
    'Stan.store': os.path.join(DATA_DIR, 'stanstore_keywords_fixed.csv')
}

competitor_keywords = []
for comp, filepath in files.items():
    if os.path.exists(filepath):
        count = 0
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                vol = parse_volume(row.get('搜索量', '0'))
                cat = row.get('分类', '')
                pri = row.get('优先级', '')
                if pri in ['P1', 'P0'] and '竞品品牌词' not in cat and '人物' not in cat and '排除' not in cat and '博彩' not in cat:
                    competitor_keywords.append({
                        'keyword': row.get('关键词', ''),
                        'volume': vol,
                        'volume_raw': row.get('搜索量', '0'),
                        'category': cat,
                        'source': comp
                    })
                    count += 1
        print(f"  {comp}: {count} 个功能词")

print(f"\n竞品功能词总计: {len(competitor_keywords)} 个")

# 合并去重
print("\n=== 步骤3: 合并去重 ===")
all_keywords = {}
for kw in product_keywords + competitor_keywords:
    key = kw['keyword'].lower().strip()
    if key not in all_keywords or kw['volume'] > all_keywords[key]['volume']:
        all_keywords[key] = kw

keywords_list = list(all_keywords.values())
print(f"合并后去重: {len(keywords_list)} 个关键词")

# 补充Vtuber/AI Agent空白机会
print("\n=== 步骤4: 补充Vtuber/AI Agent空白机会 ===")
blank_opportunities = [
    {'keyword': 'vtuber', 'volume': 50000, 'volume_raw': '50K', 'source': '空白机会-Vtuber'},
    {'keyword': 'how to become a vtuber', 'volume': 15000, 'volume_raw': '15K', 'source': '空白机会-Vtuber'},
    {'keyword': 'vtuber software', 'volume': 12000, 'volume_raw': '12K', 'source': '空白机会-Vtuber'},
    {'keyword': 'vtuber avatar maker', 'volume': 8000, 'volume_raw': '8K', 'source': '空白机会-Vtuber'},
    {'keyword': 'live2d model', 'volume': 10000, 'volume_raw': '10K', 'source': '空白机会-Vtuber'},
    {'keyword': 'virtual youtuber', 'volume': 15000, 'volume_raw': '15K', 'source': '空白机会-Vtuber'},
    {'keyword': 'virtual avatar creator', 'volume': 6000, 'volume_raw': '6K', 'source': '空白机会-Vtuber'},
    {'keyword': '3d avatar maker', 'volume': 8000, 'volume_raw': '8K', 'source': '空白机会-Vtuber'},
    {'keyword': 'vtuber setup guide', 'volume': 5000, 'volume_raw': '5K', 'source': '空白机会-Vtuber'},
    {'keyword': 'best vtuber software', 'volume': 4000, 'volume_raw': '4K', 'source': '空白机会-Vtuber'},
    {'keyword': 'ai agent', 'volume': 20000, 'volume_raw': '20K', 'source': '空白机会-AI Agent'},
    {'keyword': 'personal ai assistant', 'volume': 15000, 'volume_raw': '15K', 'source': '空白机会-AI Agent'},
    {'keyword': 'ai companion for creators', 'volume': 5000, 'volume_raw': '5K', 'source': '空白机会-AI Agent'},
    {'keyword': 'ai automation tool', 'volume': 6000, 'volume_raw': '6K', 'source': '空白机会-AI Agent'},
    {'keyword': 'digital twin ai', 'volume': 4000, 'volume_raw': '4K', 'source': '空白机会-AI Agent'},
    {'keyword': 'ai virtual assistant', 'volume': 8000, 'volume_raw': '8K', 'source': '空白机会-AI Agent'},
    {'keyword': 'content creator ai agent', 'volume': 3000, 'volume_raw': '3K', 'source': '空白机会-AI Agent'},
    {'keyword': 'ai agent framework', 'volume': 3500, 'volume_raw': '3.5K', 'source': '空白机会-AI Agent'},
    {'keyword': 'personal ai agent', 'volume': 4500, 'volume_raw': '4.5K', 'source': '空白机会-AI Agent'},
    {'keyword': 'ai agent for business', 'volume': 5500, 'volume_raw': '5.5K', 'source': '空白机会-AI Agent'},
]

for kw in blank_opportunities:
    key = kw['keyword'].lower().strip()
    if key not in all_keywords:
        all_keywords[key] = kw

keywords_list = list(all_keywords.values())
print(f"补充空白机会后: {len(keywords_list)} 个关键词")

# 分类评分
print("\n=== 步骤5: 分类和评分 ===")
def classify_and_score(kw):
    keyword = kw['keyword'].lower()
    vol = kw['volume']
    score = vol
    source = kw.get('source', '')
    
    # P0: Vtuber/虚拟形象 (竞品空白！) - 最高优先级
    if any(x in keyword for x in ['vtuber', 'virtual avatar', 'live2d', 'virtual youtuber', 'vtuber model', '3d avatar']) and '空白' in source:
        return 'P0-Vtuber/虚拟形象(空白机会)', score * 25, '差异化专题'
    
    # P0: AI Agent/智能体 (竞品空白！)
    if any(x in keyword for x in ['ai agent', 'personal ai assistant', 'ai companion', 'ai automation', 'digital twin', 'virtual assistant']) and '空白' in source:
        return 'P0-AI Agent智能体(空白机会)', score * 25, '差异化专题'
    
    # P0: 核心建站功能
    if any(x in keyword for x in ['create a website', 'make a website', 'build a website', 'how to create website', 'how to make website', 'website builder']):
        if vol >= 10000:
            return 'P0-核心建站功能', score * 10, '终极指南/着陆页'
    
    # P0: AI建站
    if any(x in keyword for x in ['ai website', 'ai builder', 'website ai', 'ai create website', 'ai website builder', 'ai website maker', 'ai website creator']):
        if vol >= 5000:
            return 'P0-AI建站功能', score * 8, 'AI功能页'
    
    # P0: Portfolio
    if any(x in keyword for x in ['portfolio website', 'portfolio template', 'art portfolio', 'personal portfolio', 'free portfolio', 'create portfolio']):
        if vol >= 5000:
            return 'P0-创作者Portfolio', score * 7, '功能页'
    
    # P0: YouTube分析工具
    if any(x in keyword for x in ['youtube analytics', 'youtube stats', 'channel analytics', 'youtube tracker', 'youtube checker']):
        if vol >= 5000:
            return 'P0-YouTube分析工具', score * 6, '工具页'
    
    # P0: 创作者变现
    if any(x in keyword for x in ['youtube monetization', 'monetize youtube', 'how to monetize', 'channel monetization', 'youtube income']):
        if vol >= 3000:
            return 'P0-创作者变现', score * 6, '变现指南'
    
    # P1: Link-in-Bio
    if any(x in keyword for x in ['link in bio', 'bio link', 'linktree alternative', 'social media links', 'one link']):
        if vol >= 1000:
            return 'P1-Link-in-Bio功能', score * 4, '功能页'
    
    # P1: Logo设计
    if any(x in keyword for x in ['logo maker', 'logo generator', 'free logo', 'logo design', 'create logo', 'ai logo']):
        if vol >= 10000:
            return 'P1-Logo设计工具', score * 3, '工具页'
    
    # P1: 着陆页
    if any(x in keyword for x in ['landing page', 'squeeze page', 'sales page']):
        if vol >= 5000:
            return 'P1-着陆页功能', score * 3, '功能页'
    
    # P1: YouTube SEO
    if any(x in keyword for x in ['youtube seo', 'youtube tags', 'tag generator', 'video seo']):
        if vol >= 3000:
            return 'P1-YouTube SEO工具', score * 3, '工具页'
    
    # P1: 域名工具
    if any(x in keyword for x in ['domain name', 'domain generator', 'domain checker']):
        if vol >= 3000:
            return 'P1-域名工具', score * 2, '工具页'
    
    # P2: HowTo教程
    if 'how to' in keyword:
        if vol >= 5000:
            return 'P2-HowTo教程', score * 1.5, '教程文章'
    
    # P2: 博客创建
    if any(x in keyword for x in ['create blog', 'start a blog', 'blogging', 'blog website']):
        if vol >= 3000:
            return 'P2-博客创建', score * 1.2, '教程页'
    
    # P2: QR码工具
    if 'qr code' in keyword:
        if vol >= 2000:
            return 'P2-QR码工具', score, '工具页'
    
    return None, 0, None

scored_keywords = []
for kw in keywords_list:
    category, score, page_type = classify_and_score(kw)
    if category and score > 0:
        kw['category'] = category
        kw['score'] = score
        kw['page_type'] = page_type
        scored_keywords.append(kw)

scored_keywords.sort(key=lambda x: x['score'], reverse=True)
print(f"评分后候选词: {len(scored_keywords)} 个")

# 选择100篇
print("\n=== 步骤6: 选择前100篇 ===")
selected = []
category_count = defaultdict(int)
category_limit = {
    'P0-Vtuber/虚拟形象(空白机会)': 10,
    'P0-AI Agent智能体(空白机会)': 10,
    'P0-核心建站功能': 12,
    'P0-AI建站功能': 8,
    'P0-创作者Portfolio': 8,
    'P0-YouTube分析工具': 8,
    'P0-创作者变现': 6,
    'P1-Link-in-Bio功能': 6,
    'P1-Logo设计工具': 5,
    'P1-着陆页功能': 5,
    'P1-YouTube SEO工具': 5,
    'P1-域名工具': 3,
    'P2-HowTo教程': 10,
    'P2-博客创建': 4,
    'P2-QR码工具': 3
}

for kw in scored_keywords:
    cat = kw['category']
    if category_count[cat] < category_limit.get(cat, 100):
        selected.append(kw)
        category_count[cat] += 1
    if len(selected) >= 100:
        break

print(f"最终选定: {len(selected)} 篇文章")

# 输出结果
print("\n" + "="*110)
print("【Popwave 前100篇SEO文章选题清单】")
print("="*110)
print("\n📌 选题策略：")
print("  • P0-空白机会(20篇): Vtuber/AI Agent - 竞品未布局，建立差异化定位")
print("  • P0-核心功能(34篇): 建站/AI建站/Portfolio/YouTube工具 - 核心业务")
print("  • P1-工具功能(24篇): Link-in-Bio/Logo/SEO/域名 - 辅助功能")
print("  • P2-教程长尾(22篇): HowTo/博客/QR码 - 流量补充")
print("\n" + "="*110)

by_category = defaultdict(list)
for i, kw in enumerate(selected, 1):
    kw['rank'] = i
    by_category[kw['category']].append(kw)

category_order = [
    'P0-Vtuber/虚拟形象(空白机会)',
    'P0-AI Agent智能体(空白机会)', 
    'P0-核心建站功能',
    'P0-AI建站功能',
    'P0-创作者Portfolio',
    'P0-YouTube分析工具',
    'P0-创作者变现',
    'P1-Link-in-Bio功能',
    'P1-Logo设计工具',
    'P1-着陆页功能',
    'P1-YouTube SEO工具',
    'P1-域名工具',
    'P2-HowTo教程',
    'P2-博客创建',
    'P2-QR码工具'
]

for cat in category_order:
    if cat in by_category:
        kws = by_category[cat]
        short_name = cat.replace('(空白机会)', '[竞品空白!]')
        print(f"\n🎯 {short_name} ({len(kws)}篇)")
        print("-"*110)
        for kw in kws:
            vol_str = kw.get('volume_raw', str(kw['volume']))
            if kw['volume'] > 0 and (vol_str in ['0', '-', '']):
                vol_str = f"{kw['volume']:,}"
            src = kw.get('source', '-')
            if len(src) > 12:
                src = src[:9] + '...'
            print(f"  {kw['rank']:3}. {kw['keyword']:<52} | {vol_str:>10} | {kw['page_type']:<18} | {src}")

print(f"\n\n{'='*110}")
print(f"✅ 总计: {len(selected)} 篇高优先级文章")
print("="*110)

# 统计
print("\n📊 分布统计:")
for cat in category_order:
    if cat in by_category:
        short_name = cat.replace('(空白机会)', '[竞品空白]')
        print(f"  {short_name}: {len(by_category[cat])}篇")

# 保存
with open(os.path.join(DATA_DIR, '100篇SEO文章选题清单_最终版.csv'), 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['序号', '优先级类别', '目标关键词', '搜索量', '页面类型', '关键词来源', '战略备注'])
    for kw in selected:
        vol_str = kw.get('volume_raw', str(kw['volume']))
        if kw['volume'] > 0 and vol_str in ['0', '-', '']:
            vol_str = f"{kw['volume']:,}"
        note = ''
        if '空白' in kw['category']:
            note = '竞品空白机会-优先布局'
        elif 'P0' in kw['category']:
            note = '核心功能-高优先级'
        writer.writerow([kw['rank'], kw['category'], kw['keyword'], vol_str, kw['page_type'], kw.get('source', '-'), note])

print(f"\n📁 已保存: 100篇SEO文章选题清单_最终版.csv")
