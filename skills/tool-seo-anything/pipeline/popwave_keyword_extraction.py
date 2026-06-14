#!/usr/bin/env python3
"""
从 Beacons 竞品关键词表中，为 Popwave 提取有价值的关键词
"""

keywords_data = [
    # (关键词, 搜索量, 流量, 类型判断)
    ("beacons", "89K", "42,192", "竞品品牌词"),
    ("beacons ai", "38K", "13,950", "竞品品牌词+功能"),
    ("beacons.ai", "8.4K", "8,754", "竞品品牌词"),
    ("what is beacons.ai", "1.9K", "754", "竞品品牌教育词"),
    ("beacons login", "-", "-", "竞品功能词"),
    ("download hub", "115K", "2,926", "高流量功能词"),
    ("instafest app", "38K", "1,372", "功能词-增长型"),
    ("elly clutch", "99K", "2,266", "人物流量词-高"),
    ("lilijunex", "75K", "1,668", "人物流量词-高"),
    ("pamsnusnu", "78K", "1,944", "人物流量词-高"),
    ("panentogel", "51K", "2,666", "高流量但风险词"),
    ("pokerseri", "11K", "13,214", "高带量词-垂直"),
    ("barcaslot", "8.6K", "8,890", "高带量词-垂直"),
    ("kepritogel link alternatif", "22K", "2,097", "高带量词-垂直"),
    ("kepri togel", "23K", "1,763", "高带量词-垂直"),
    ("compass dollar tree", "25K", "1,200", "工具场景词"),
    ("cnfans spreadsheet", "33K", "816", "工具场景词"),
    ("how old is salish matter", "30K", "1,272", "人物查询词"),
    ("instagram bio punjabi", "1.9K", "696", "功能场景词-小语种"),
    ("mahadev bio for instagram", "-", "-", "功能场景词-文化"),
    ("dark aesthetic bio instagram", "-", "-", "功能场景词-风格"),
    ("after long time meet caption", "-", "-", "Caption场景词"),
    ("motivational bio for instagram", "-", "-", "功能场景词"),
]

# 高价值词筛选标准
def extract_valuable_keywords():
    categories = {
        "🔴 必须拦截：竞品品牌词 (防守+进攻)": [],
        "🟠 高流量机会：大流量值得抢的词": [],
        "🟡 高带量词：点击转化高的垂直词": [],
        "🟢 功能差异化：产品功能切入点": [],
        "🔵 场景空白：你的内容机会": [],
        "⚫ 排除/风险词": [],
    }
    
    for kw, vol, traffic, note in keywords_data:
        vol_num = vol.replace("K", "000").replace(",", "") if vol != "-" else "0"
        traffic_num = traffic.replace(",", "") if traffic != "-" else "0"
        
        try:
            vol_num = int(vol_num)
            traffic_num = int(traffic_num)
        except:
            vol_num = 0
            traffic_num = 0
        
        # 1. 竞品品牌词（拦截流量）
        if "beacons" in kw.lower() or "beacon" in kw.lower():
            categories["🔴 必须拦截：竞品品牌词 (防守+进攻)"].append(
                (kw, vol, traffic, "写对比文章/替代方案页面")
            )
        # 2. 高流量词 (>10K)
        elif vol_num >= 10000 and "togel" not in kw and "slot" not in kw and "poker" not in kw:
            categories["🟠 高流量机会：大流量值得抢的词"].append(
                (kw, vol, traffic, "Landing Page/专题页面")
            )
        # 3. 高带量词 (流量/搜索量比值高)
        elif traffic_num > 1000 and vol_num > 0:
            ratio = traffic_num / vol_num if vol_num > 0 else 0
            if ratio > 0.5:  # 高点击率词
                categories["🟡 高带量词：点击转化高的垂直词"].append(
                    (kw, vol, traffic, f"高转化页面, 点击率{ratio:.1%}")
                )
        # 4. 功能词
        elif any(x in kw.lower() for x in ['bio', 'instagram', 'caption', 'spreadsheet', 'hub']):
            categories["🟢 功能差异化：产品功能切入点"].append(
                (kw, vol, traffic, "功能介绍/Bio生成器")
            )
        # 5. 人物词
        elif any(x in kw.lower() for x in ['clutch', 'junex', 'valdez', 'banks']):
            categories["🔵 场景空白：你的内容机会"].append(
                (kw, vol, traffic, "创作者案例/成功故事")
            )
        # 6. 排除
        elif any(x in kw.lower() for x in ['togel', 'slot', 'poker', 'onlyfans']):
            categories["⚫ 排除/风险词"].append((kw, vol, traffic, "跳过"))
    
    return categories

categories = extract_valuable_keywords()

print("="*80)
print("Popwave 从 Beacons 关键词表提取的高价值词")
print("="*80)
print()

for cat, items in categories.items():
    if items:
        print(f"\n{cat} ({len(items)} 个)")
        print("-"*70)
        for kw, vol, traffic, action in items[:10]:  # 只显示前10个
            print(f"  • {kw}")
            print(f"    搜索量: {vol} | 流量: {traffic}")
            print(f"    建议: {action}")
            print()

print()
print("="*80)
print("筛选逻辑总结")
print("="*80)
print("""
筛选维度：
1. 竞品品牌词 → 拦截流量（写替代方案/对比）
2. 高流量词 (>10K) → 大流量入口（专题页面）
3. 高带量词 (流量/搜索量>50%) → 转化高（优先做）
4. 功能词 → 差异化机会（Bio生成器等）
5. 人物词 → 案例/故事内容（创作者成功故事）

排除：博彩类、成人内容类（合规风险）
""")
