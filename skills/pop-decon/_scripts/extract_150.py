#!/usr/bin/env python3
"""
pop-novel-deconstructor v11.1 — Unified Data Extraction Script
==============================================================
Extracts structured data from a web novel TXT file (GBK encoded).
Produces JSON intermediate files for ETL pipeline.

Usage:
    python extract.py baseline <txt_path> <output_dir>
    python extract.py index    <txt_path> <output_dir>
    python extract.py world    <txt_path> <output_dir>
    python extract.py all      <txt_path> <output_dir>
"""

import sys
import os
import re
import json
from datetime import datetime

def find_chapter_lines(lines, arabic_only=True):
    """Build chapter index for Arabic-numeral chapter titles.
    Matches lines like '第1章 标题', '第20章 神之子'.
    Returns list of (chapter_num, line_index, title_text)."""
    chapters = []
    pattern = re.compile(r'^第(\d+)章\S*(?:\s+\S+)?$')
    for i, line in enumerate(lines):
        line = line.strip()
        m = pattern.match(line)
        if m:
            chapters.append((int(m.group(1)), i, line))
    return chapters


def read_file_gbk(path):
    """Read a file with GBK encoding, fallback to UTF-8."""
    encodings = ['gbk', 'utf-8', 'gb2312']
    for enc in encodings:
        try:
            with open(path, 'r', encoding=enc) as f:
                content = f.read()
            with open(path, 'r', encoding=enc) as f:
                lines = f.readlines()
            return content, lines
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Cannot decode file: {path}")


# ============================================================================
# EXTRACT BASELINE (Phase S: ch1-20)
# ============================================================================
def extract_baseline(txt_path, output_dir):
    print(f"[extract-baseline] Reading: {txt_path}")
    content, lines = read_file_gbk(txt_path)
    print(f"[extract-baseline] Loaded {len(lines)} lines")

    chapters = find_chapter_lines(lines)
    print(f"[extract-baseline] Found {len(chapters)} chapters")

    # Get ch1-20
    ch1_20 = [c for c in chapters if 1 <= c[0] <= 20]
    if not ch1_20:
        ch1_20 = chapters[:20]
        print("[extract-baseline] No ch1-20 found, using first 20 chapters")

    # Extract ch1-20 text block
    start_line = ch1_20[0][1]
    end_ch = next((c for c in chapters if c[0] > 20), None)
    end_line = end_ch[1] if end_ch else len(lines)
    ch20_lines = lines[start_line:end_line]
    ch20_text = '\n'.join(ch20_lines)
    print(f"[extract-baseline] ch1-20: lines {start_line}-{end_line-1}, {len(ch20_text)} chars")

    # --- Search: Named characters (quoted names >=2 chars, all quote styles) ---
    # Cover: \u201c...\u201d, \u300c...\u300d, \u300e...\u300f, \u2018...\u2019
    char_pattern = re.compile(
        r'[\u201c\u300c\u300e\u2018]([\u4e00-\u9fff]{2,})[\u201d\u300d\u300f\u2019]'
    )
    characters = set()
    for m in char_pattern.finditer(ch20_text):
        name = m.group(1).strip()
        if len(name) >= 2:
            characters.add(name)

    # --- Search: Place names ---
    place_pattern = re.compile(
        r'(?:在|到|前往|来到|位于|进入|离开|返回|抵达|经过)'
        r'([\u4e00-\u9fff]{2,6}(?:城|镇|村|堡|山|河|湖|海|岛|林|谷|原|关|都|府|殿|塔|寺|窟|洞|墓|遗迹|森林|平原|山脉))'
    )
    places = set()
    for m in place_pattern.finditer(ch20_text):
        places.add(m.group(1).strip())

    # --- Search: Level/class mentions ---
    class_names = [
        '游荡者', '盗贼', '战士', '法师', '牧师', '骑士', '弓箭手',
        '术士', '召唤师', '剑士', '魔导师', '刺客', '猎手', '祭祀',
        '巫师', '德鲁伊', '圣武士', '吟游诗人', '野蛮人', '武僧', '平民'
    ]
    level_pattern = re.compile(
        r'([\u4e00-\u9fff]{0,4}(?:级|职业|阶位|段位|境界))|(' + '|'.join(class_names) + r')'
    )
    levels = set()
    for m in level_pattern.finditer(ch20_text):
        val = m.group(0).strip()
        if val:
            levels.add(val)

    # --- Search: Age mentions (Arabic and Chinese numerals) ---
    # Arabic: "8岁", Chinese: "八岁", "十六岁"
    cn_nums = '[一二三四五六七八九十百千]+'
    age_pattern = re.compile(
        rf'((?:[\u4e00-\u9fff]{{0,4}})(?:{cn_nums}|\d+)\s*岁)'
    )
    ages = sorted(set(m.group(0).strip() for m in age_pattern.finditer(ch20_text)))

    # --- Search: Monster names ---
    monster_pattern = re.compile(r'([\u4e00-\u9fff]{2,}(?:兽|龙|蛇|狼|虎|熊|鹰|鸟|虫|鱼|怪|魔|妖|精|灵))')
    monsters = set()
    for m in monster_pattern.finditer(ch20_text):
        monsters.add(m.group(1).strip())

    # --- Extract events: per-chapter first sentences (first occurrence only) ---
    events = []
    current_ch = 0
    buffer = ""
    seen_chapters = set()
    for i, line in enumerate(lines):
        stripped = line.strip()
        m = re.match(r'^第(\d+)章\S*(?:\s+\S+)?$', stripped)
        if m:
            num = int(m.group(1))
            if 1 <= num <= 20 and num not in seen_chapters:
                # First time we see this chapter number -> start new chapter
                if current_ch != 0 and buffer.strip():
                    evt = re.sub(r'\s+', '', buffer)
                    events.append({
                        "chapter": current_ch,
                        "summary": evt[:100]
                    })
                current_ch = num
                seen_chapters.add(num)
                buffer = ""
                continue
            elif num > 20 or (1 <= num <= 20 and num in seen_chapters):
                # Hit a chapter beyond 20 or a repeated chapter -> stop
                if current_ch != 0 and buffer.strip():
                    evt = re.sub(r'\s+', '', buffer)
                    events.append({
                        "chapter": current_ch,
                        "summary": evt[:100]
                    })
                current_ch = 0
                continue
        if current_ch > 0 and stripped:
            buffer += stripped
    # Last chapter
    if current_ch != 0 and buffer.strip():
        evt = re.sub(r'\s+', '', buffer)
        events.append({"chapter": current_ch, "summary": evt[:100]})

    # Build output
    output = {
        "meta": {
            "source": txt_path,
            "script": "extract.py baseline (Phase S)",
            "extractedAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "chapters": "1-20",
            "totalLines": len(lines)
        },
        "characters": sorted(characters),
        "places": sorted(places),
        "levels": sorted(levels),
        "ages": ages,
        "monsters": sorted(monsters),
        "events": sorted(events, key=lambda e: e["chapter"])
    }

    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, "baseline-data.json")
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print("")
    print("=" * 60)
    print("  extract-baseline -- Done")
    print("=" * 60)
    print(f"  Chapters    : 1-20 ({len(events)} events)")
    print(f"  Characters  : {len(characters)}")
    print(f"  Places      : {len(places)}")
    print(f"  Levels      : {len(levels)}")
    print(f"  Age mentions: {len(ages)}")
    print(f"  Monsters    : {len(monsters)}")
    print("=" * 60)
    print("")


# ============================================================================
# EXTRACT CHAPTER INDEX (Phase 0: ch1-100)
# ============================================================================
def extract_index(txt_path, output_dir):
    print(f"[extract-index] Reading: {txt_path}")
    content, lines = read_file_gbk(txt_path)
    print(f"[extract-index] Loaded {len(lines)} lines")

    chapters = find_chapter_lines(lines)
    print(f"[extract-index] Found {len(chapters)} chapters")

    # Filter ch1-100: first occurrence of each chapter number 1-100
    ch1_100 = []
    seen_nums = set()
    for c in chapters:
        if c[0] not in seen_nums and 1 <= c[0] <= 150:
            ch1_100.append(c)
            seen_nums.add(c[0])
    ch1_100.sort(key=lambda x: x[0])
    actual_max = max(c[0] for c in ch1_100) if ch1_100 else 0
    print(f"[extract-index] Processing {len(ch1_100)} unique chapters (1-{actual_max})")

    # Keywords for tagging
    battle_keywords = [
        '战斗', '杀', '攻击', '防御', '战', '剑', '刀', '魔法', '法术',
        '箭', '武器', '怪物', '恶魔', '魔兽', '强盗', '混战', '搏杀',
        '偷袭', '伏击', '流血', '伤害', '死亡', '杀死', '击杀', '斩杀'
    ]
    world_keywords = [
        '神殿', '魔法', '神祇', '法则', '位面', '多元宇宙', '圣者', '神明',
        '神灵', '诸神', '牧师', '信仰', '教会', '宗教', '祭祀', '仪式',
        '魔力', '奥术', '法术书', '秘法', '元素', '深渊', '地狱', '天堂', '契约'
    ]
    economy_keywords = [
        '交易', '金德勒', '金币', '银币', '铜德勒', '拍卖', '商人', '商店',
        '市场', '铁匠铺', '装备', '武器铺', '药水', '药剂', '卷轴',
        '次元袋', '魔法物品', '神器', '宝藏', '财富', '金钱'
    ]

    output_chapters = []
    first100_char_count = 0

    for idx, (num, start, title) in enumerate(ch1_100):
        # End is next chapter start or around chapter 101
        if idx + 1 < len(ch1_100):
            end = ch1_100[idx + 1][1] - 1
        else:
            next_ch = next((c for c in chapters if c[0] > 150), None)
            end = next_ch[1] - 1 if next_ch else len(lines) - 1
        if end < start:
            end = start + max(0, len(lines) - start - 1)

        ch_text = '\n'.join(lines[start:end + 1])
        ch_stripped = re.sub(r'\s+', '', ch_text)
        char_count = len(ch_stripped)
        first100_char_count += char_count

        # First non-empty, non-title line
        first_sentence = ""
        for j in range(start + 1, end + 1):
            t = lines[j].strip()
            if t and not re.match(r'^第\d+章', t):
                first_sentence = t[:80] + "..." if len(t) > 80 else t
                break

        # Tag content types
        tags = []
        battle_hits = sum(1 for kw in battle_keywords if kw in ch_text)
        world_hits = sum(1 for kw in world_keywords if kw in ch_text)
        economy_hits = sum(1 for kw in economy_keywords if kw in ch_text)
        if battle_hits >= 3:
            tags.append("battle")
        if world_hits >= 3:
            tags.append("worldbuilding")
        if economy_hits >= 3:
            tags.append("economy")

        output_chapters.append({
            "chapter": num,
            "title": title,
            "lineStart": start,
            "lineEnd": end,
            "charCount": char_count,
            "firstSentence": first_sentence,
            "tags": tags
        })

    output = {
        "meta": {
            "source": txt_path,
            "script": "extract.py index (Phase 0)",
            "extractedAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "totalArabChapters": len(chapters),
            "totalLines": len(lines),
            "first100CharCount": first100_char_count
        },
        "chapters": output_chapters
    }

    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, "chapter-index.json")
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    battle_count = sum(1 for c in output_chapters if "battle" in c["tags"])
    world_count = sum(1 for c in output_chapters if "worldbuilding" in c["tags"])
    economy_count = sum(1 for c in output_chapters if "economy" in c["tags"])

    print("")
    print("=" * 60)
    print("  extract-index -- Done")
    print("=" * 60)
    print(f"  Chapters indexed  : {len(output_chapters)}")
    print(f"  Total chars (1-100): {first100_char_count}")
    print(f"  Battle chapters   : {battle_count}")
    print(f"  Worldbuilding chs : {world_count}")
    print(f"  Economy chapters  : {economy_count}")
    print("=" * 60)
    print("")


# ============================================================================
# EXTRACT WORLD DATA (Phase 2.2: ch1-100 worldview)
# ============================================================================
def extract_world(txt_path, output_dir):
    print(f"[extract-world] Reading: {txt_path}")
    content, lines = read_file_gbk(txt_path)
    print(f"[extract-world] Loaded {len(lines)} lines")

    chapters = find_chapter_lines(lines)
    print(f"[extract-world] Found {len(chapters)} chapters")

    # Build chapter map: line_number -> chapter_number (first occurrence only)
    ch_map = {}
    current_chapter = 0
    seen_ch_nums = set()
    for i, line in enumerate(lines):
        stripped = line.strip()
        m = re.match(r'^第(\d+)章\S*(?:\s+\S+)?$', stripped)
        if m:
            num = int(m.group(1))
            if 1 <= num <= 150 and num not in seen_ch_nums:
                current_chapter = num
                seen_ch_nums.add(num)
            elif 1 <= num <= 150 and num in seen_ch_nums:
                current_chapter = 0  # stop mapping once we see repeats
        if current_chapter > 0:
            ch_map[i] = current_chapter

    # Category definitions
    categories = [
        ("deity",     ["神祇", "圣者", "神格", "神性", "诸神", "神灵", "神明", "神之子", "半神", "圣者形态", "神力", "信仰之力"]),
        ("magic",     ["法术", "魔法", "奥术", "魔力", "法阵", "施法", "咒语", "术法", "法术位", "环级", "环位", "一环", "二环", "三环", "四环", "五环", "六环", "七环", "八环", "九环", "法术书", "学派"]),
        ("class",     ["职业", "等级", "进阶", "游荡者", "盗贼", "战士", "法师", "牧师", "骑士", "弓箭手", "术士", "召唤师", "剑士", "魔导师", "刺客", "猎手", "祭祀", "巫师", "德鲁伊", "圣武士", "吟游诗人", "野蛮人", "武僧", "专长", "技能"]),
        ("species",   ["精灵", "矮人", "龙族", "魔族", "兽人", "半精灵", "半兽人", "亡灵", "巫妖", "吸血鬼", "狼人", "变形怪", "深渊恶魔", "魔鬼", "天使", "妖精", "元素生物", "巨人", "地精", "豺狼人", "食人魔", "哥布林", "种族", "血脉"]),
        ("faction",   ["势力", "组织", "神殿", "公会", "帝国", "王国", "联盟", "联邦", "教会", "教派", "骑士团", "冒险者公会", "商会", "行会", "晨曦", "暗影", "秩序", "混乱", "善良", "邪恶", "中立"]),
        ("item",      ["神器", "法器", "魔杖", "法杖", "长剑", "弯刀", "匕首", "皮甲", "锁甲", "板甲", "盾牌", "药剂", "药水", "卷轴", "次元袋", "魔法物品", "魔法装备", "金德勒", "铜德勒", "银币", "金币"]),
        ("geography", ["城", "镇", "村", "堡", "山", "河", "湖", "海", "岛", "林", "谷", "原", "沙漠", "沼泽", "荒野", "森林", "平原", "山脉", "遗迹", "码头", "港口"]),
    ]

    # Find ch1-100 line range: use first occurrence of each
    ch1_start = None
    ch100_end = None
    for num, line_idx, _ in chapters:
        if num == 1 and ch1_start is None:
            ch1_start = line_idx
        if num == 100:
            ch100_end = line_idx
            break  # first occurrence of ch100
    if ch1_start is None:
        ch1_start = 0
    # Find first chapter >100 to stop
    if ch100_end is None:
        first_beyond = next((c for c in chapters if c[0] > 150), None)
        ch100_end = first_beyond[1] if first_beyond else len(lines) - 1
    else:
        # Scan ends at the chapter AFTER ch100's first occurrence
        ch101 = next((c for c in chapters if c[0] > 150 and c[1] > ch100_end), None)
        if ch101:
            ch100_end = ch101[1] - 1
    print(f"[extract-world] Scanning lines {ch1_start} to {ch100_end}")

    results = {cat_name: [] for cat_name, _ in categories}
    seen = set()

    for i in range(ch1_start, ch100_end + 1):
        ch = ch_map.get(i, 0)
        if ch == 0:
            continue

        line_text = lines[i].rstrip('\n').rstrip('\r')
        if len(line_text.strip()) < 2:
            continue

        for cat_name, keywords in categories:
            matched_kw = None
            for kw in keywords:
                if kw in line_text:
                    matched_kw = kw
                    break
            if not matched_kw:
                continue

            # Context: 2 lines before and after
            ctx_lines = []
            for cj in range(max(0, i - 2), min(len(lines), i + 3)):
                prefix = ">>" if cj == i else "  "
                ctx_lines.append(f"{prefix}{lines[cj].rstrip()}")
            ctx_text = '\n'.join(ctx_lines)

            # Matched segment
            pos = line_text.find(matched_kw)
            seg_start = max(0, pos - 20)
            seg = line_text[seg_start:seg_start + 60]

            text_key = line_text.strip()
            if len(text_key) > 80:
                text_key = text_key[:80]

            dedup_key = f"{cat_name}|{ch}|{text_key}"
            if dedup_key not in seen:
                seen.add(dedup_key)
                results[cat_name].append({
                    "chapter": ch,
                    "line": i,
                    "text": text_key,
                    "match": seg,
                    "keyword": matched_kw,
                    "context": ctx_text
                })

    # Build output
    cat_outputs = {}
    stats = {}
    for cat_name, _ in categories:
        cat_outputs[cat_name] = {
            "count": len(results[cat_name]),
            "entries": results[cat_name]
        }
        stats[cat_name] = len(results[cat_name])

    output = {
        "meta": {
            "source": txt_path,
            "script": "extract.py world (Phase 2.2)",
            "extractedAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "chapterRange": "1-100"
        },
        "categories": cat_outputs,
        "stats": stats
    }

    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, "world-data.json")
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print("")
    print("=" * 60)
    print("  extract-world -- Done")
    print("=" * 60)
    for cat_name, _ in categories:
        print(f"  {cat_name:15}: {stats[cat_name]:6} entries")
    print("=" * 60)
    print("")


# ============================================================================
# MAIN
# ============================================================================
def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    mode = sys.argv[1]

    if mode == "all":
        if len(sys.argv) < 4:
            print("Usage: python extract.py all <txt_path> <output_dir>")
            sys.exit(1)
        txt_path = sys.argv[2]
        output_dir = sys.argv[3]
        extract_baseline(txt_path, output_dir)
        extract_index(txt_path, output_dir)
        extract_world(txt_path, output_dir)
    else:
        if len(sys.argv) < 4:
            print(f"Usage: python extract.py {mode} <txt_path> <output_dir>")
            sys.exit(1)
        txt_path = sys.argv[2]
        output_dir = sys.argv[3]
        if mode == "baseline":
            extract_baseline(txt_path, output_dir)
        elif mode == "index":
            extract_index(txt_path, output_dir)
        elif mode == "world":
            extract_world(txt_path, output_dir)
        else:
            print(f"Unknown mode: {mode}")
            print("Valid modes: baseline, index, world, all")
            sys.exit(1)


if __name__ == "__main__":
    main()

