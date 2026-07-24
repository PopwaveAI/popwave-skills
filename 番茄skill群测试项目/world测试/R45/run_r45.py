#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
R45 world v1.5.0力量体系四层结构测试

测试目标：验证world v1.5.0能否正确消费decon-lite拆出的力量体系规则级产出，
产出力量体系四层结构（世界源力量/主养成线含社会地位/子养成线含阶位+挂钩/交叉规则）

测试方案：2本修仙对比测
- 参考书A：《玄鉴仙族》（季越人）→ decon-lite拆表1 → world消费
- 参考书B：《没钱修什么仙》（熊狼狗）→ decon-lite拆表1 → world消费

每本书独立跑decon-lite + world，对比两本书的力量体系设计差异。

输入：参考小说txt前100章采样
输出：
  - decon-lite-{书名}.md（表1力量体系规则级）
  - world-力量体系-{书名}.md（world v1.5.0四层结构产出）
  - inputs/{书名}_decon_input.md + {书名}_world_input.md
"""

import os
import sys
import json
import time
import requests

# ============ 配置 ============
DS_API_KEY = "sk-5a3654e4aa2e4eefa08abe3d0e0231f5"
DS_BASE_URL = "https://api.deepseek.com/v1"
DS_MODEL = "deepseek-v4-flash"
PROXIES = {"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"}
TEMPERATURE = 0.85
TIMEOUT = 600
MAX_TOKENS = 12000

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUTS_DIR = os.path.join(SCRIPT_DIR, "inputs")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")

SKILLS_BASE = r"d:\popwave-skills\skills"
NOVEL_DIR = r"d:\popwave-skills\workspace\参考小说txt\起点top20"

BOOKS = [
    {
        "name": "玄鉴仙族",
        "txt": os.path.join(NOVEL_DIR, "玄鉴仙族-季越人.txt"),
    },
    {
        "name": "没钱修什么仙",
        "txt": os.path.join(NOVEL_DIR, "没钱修什么仙？-熊狼狗.txt"),
    },
]

# ============ 工具函数 ============

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def read_skill_files(skill_name, files):
    parts = []
    for f in files:
        path = os.path.join(SKILLS_BASE, skill_name, f)
        parts.append(read_file(path))
    return "\n\n---\n\n".join(parts)

def sample_txt(txt_path, max_chapters=100):
    """交替采样法：1~10章全读，后续每两章读一章，取前max_chapters章"""
    with open(txt_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 按章分隔（常见分隔符：第X章 / Chapter X）
    import re
    # 匹配 "第X章" 或 "第X回" 或 "Chapter X"
    chapters = re.split(r'(?=第[一二三四五六七八九十百千零\d]+[章回])', content)
    # 第一段通常是简介/楔子，保留
    if chapters and not re.match(r'第[一二三四五六七八九十百千零\d]+[章回]', chapters[0]):
        intro = chapters[0]
        chapters = chapters[1:]
    else:
        intro = ""

    print(f"  总章数: {len(chapters)}")

    # 采样：1-10全读，11-max_chapters每两章读一章
    sampled = []
    for i, ch in enumerate(chapters[:max_chapters]):
        chapter_num = i + 1
        if chapter_num <= 10 or chapter_num % 2 == 1:
            sampled.append(ch)

    result = intro + "\n\n".join(sampled)
    return result, len(sampled)

def call_ds(system_prompt, user_prompt, max_tokens=MAX_TOKENS):
    url = f"{DS_BASE_URL}/chat/completions"
    headers = {"Authorization": f"Bearer {DS_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": DS_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": TEMPERATURE,
        "max_tokens": max_tokens,
        "stream": False
    }
    start = time.time()
    response = requests.post(url, headers=headers, json=payload, timeout=TIMEOUT, proxies=PROXIES)
    response.raise_for_status()
    elapsed = time.time() - start
    result = response.json()
    content = result["choices"][0]["message"]["content"]
    usage = result.get("usage", {})
    return content, usage, elapsed

def save_input_output(book_name, step_name, system_prompt, user_prompt, output):
    """落盘input和output"""
    input_content = f"# SYSTEM PROMPT\n\n{system_prompt}\n\n---\n\n# USER PROMPT\n\n{user_prompt}"
    input_path = os.path.join(INPUTS_DIR, f"{book_name}_{step_name}_input.md")
    with open(input_path, "w", encoding="utf-8") as f:
        f.write(input_content)

    output_path = os.path.join(OUTPUT_DIR, f"{step_name}-{book_name}.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(output)

    return input_path, output_path

# ============ Step 1: decon-lite拆表1 ============

def build_decon_system():
    """decon-lite的system prompt：pop-research SKILL.md的decon-lite SOP"""
    research_skill = read_skill_files("pop-research", ["SKILL.md"])
    return research_skill

def build_decon_prompt(book_name, sampled_text, sample_count):
    return f"""# 任务

按pop-research v2.1.0的decon-lite SOP，拆解《{book_name}》的力量体系。

## 输入

书名：《{book_name}》
采样范围：前100章（交替采样法——1~10章全读，后续每两章读一章，共{sample_count}章）

## 采样正文

{sampled_text[:80000]}

（注：如正文超长已截断至80000字符，覆盖前{sample_count}章采样内容）

## 执行要求

**只拆表1：力量体系结构（规则级深度）**。不需要拆表2-8。

按decon-lite表1的字段逐项拆解：
1. 力量体系类型
2. 主养成线（位阶）——至少覆盖前4阶，每阶标注章范围+质变标志
3. 子养成线清单——先识别这本书有几条子养成线，再列名称
4. 子养成线N规则——每条拆获取规则+消耗+上限+与主养成线关系+原文chXX出处
5. 子养成线交叉规则——子养成线之间怎么互相影响
6. 升级触发
7. 强度膨胀
8. 破局手段演变
9. 设计亮点

## 红线
1. 表1必须拆到规则级——不能只列阶位骨架，必须识别子养成线并逐条拆规则+交叉规则
2. 每条规则标注原文chXX出处
3. 子养成线数量不固定——先识别这本书有几条，再逐条拆

直接输出表1完整拆解结果，markdown格式。"""

# ============ Step 2: world v1.5.0力量体系四层结构 ============

def build_world_system():
    """world的system prompt：world SKILL.md + step3 + step4"""
    return read_skill_files("pop-fanqie-world", ["SKILL.md", "steps/step3.md", "steps/step4.md"])

def build_world_prompt(book_name, decon_output):
    return f"""# 任务

按pop-fanqie-world v1.5.0的SOP，基于以下decon-lite拆出的力量体系规则级产出，设计world力量体系四层结构。

## 输入1：decon-lite表1（参考书DNA·第二源）

{decon_output}

## 输入2：创意.md（第三源·模拟一个修仙创意）

```markdown
# 创意.md（模拟·用于测试world消费decon-lite的能力）

## 一句话简介
一个灵根废柴在修仙宗门底层挣扎求生，意外觉醒了古法炼器传承，靠修复残破法器换取修炼资源，一步步从外门杂役爬到内门核心。

## 金手指
- 创意：古法炼器传承——能看到法器的"器灵残影"，修复残破法器时能提取器灵记忆碎片
- 机制：修复法器=获取器灵记忆=获得该法器原主人的修炼感悟碎片
- 限制：①每次修复消耗自身灵力，修复越高级法器消耗越大 ②器灵记忆碎片有排斥反应，同时持有超过3个碎片会灵力紊乱 ③修复失败法器会炸裂反伤

## 行为引擎
主角每章在修复法器——收法器→鉴定→修复→交付→获得报酬/修炼感悟

## 轻量主角轮廓
- 名字：测试主角
- 身份：外门杂役
- 核心动机：靠炼器手艺换取修炼资源，弥补灵根劣势
```

## 输入3：市场校准.md
（缺失——标注缺失，不阻塞）

## 执行要求

**只执行Step 2的2a：三源合流设计力量体系四层结构**。不需要做地图/势力/危机/全书设定。

按world v1.5.0 SKILL.md的"三源合流产出：力量体系四层结构"执行：

### 第一层：世界源力量
- 源力量名称（贴合修仙世界观）
- 源力量来源（和世界观挂钩）
- 源力量→主养成线转化链
- 源力量→诡/怪/敌分级标准

### 第二层：主养成线（位阶）
展开5-7个阶位，每个阶位必须有：
- 阶位名称（≤6字，**必须有文化渊源**——修仙用境界名/道教佛教词汇，禁止"觉醒者/承载者"通用词）
- 这个世界长什么样
- 主角在这个层级面对什么
- 升级触发条件
- **社会地位参照**（这个阶位有多少人？什么社会地位？）
- 预计展开卷

### 第三层：子养成线
**从decon-lite表1逐条消费**——decon拆出N条子养成线，world必须逐条处理（照搬转化or标注"本项目不需要因为XX"）。禁止丢条自己另编。

每条子养成线必须有：
- 子养成线名称（从decon-lite照搬或微调）
- 自身阶位（≥2级）
- 和主养成线挂钩关系
- 规则（获取/消耗/上限）
- 参考源（decon·表1·子养成线N）

### 第四层：交叉规则
**从decon-lite表1逐条消费**——decon拆出N条交叉规则，world必须逐条映射到本项目（照搬转化or标注"不需要因为XX"）。禁止标"参考decon·XX"但实际另编。

每条交叉规则必须有：
- 规则名称
- 涉及哪些子养成线
- 协同/制约类型
- 具体规则
- 参考源

## 红线
1. decon-lite拆出的主养成线N阶/子养成线N条/交叉规则N条必须逐条处理，禁止丢条自编
2. 阶位名称必须有文化渊源，禁止通用词
3. 力量体系必须四层结构完整——缺任何一层=废设定
4. 子养成线必须有自身阶位+和主养成线挂钩
5. 主养成线阶位必须有社会地位参照

直接输出力量体系四层结构完整设计，markdown格式。不要写思考过程。"""

# ============ 主流程 ============

def process_book(book):
    """对每本书执行decon-lite + world两步"""
    book_name = book["name"]
    txt_path = book["txt"]

    print(f"\n{'='*60}")
    print(f"处理《{book_name}》")
    print(f"{'='*60}")

    # Step 0: 采样
    print(f"\n[采样] 读取txt并交替采样前100章...")
    sampled_text, sample_count = sample_txt(txt_path, max_chapters=100)
    print(f"  采样完成: {sample_count}章, {len(sampled_text)}字符")

    # Step 1: decon-lite拆表1
    print(f"\n[decon-lite] 拆解表1力量体系规则级...")
    decon_system = build_decon_system()
    decon_prompt = build_decon_prompt(book_name, sampled_text, sample_count)

    try:
        decon_output, decon_usage, decon_elapsed = call_ds(
            decon_system, decon_prompt, max_tokens=MAX_TOKENS
        )
        decon_in_path, decon_out_path = save_input_output(
            book_name, "decon", decon_system, decon_prompt, decon_output
        )
        print(f"  完成! {decon_elapsed:.1f}s | {len(decon_output)}字符 | tokens:{decon_usage.get('total_tokens', 0)}")
        print(f"    input  → {decon_in_path}")
        print(f"    output → {decon_out_path}")
    except Exception as e:
        print(f"  decon-lite失败: {e}")
        return None

    # Step 2: world力量体系四层结构
    print(f"\n[world v1.5.0] 设计力量体系四层结构...")
    world_system = build_world_system()
    world_prompt = build_world_prompt(book_name, decon_output)

    try:
        world_output, world_usage, world_elapsed = call_ds(
            world_system, world_prompt, max_tokens=MAX_TOKENS
        )
        world_in_path, world_out_path = save_input_output(
            book_name, "world", world_system, world_prompt, world_output
        )
        print(f"  完成! {world_elapsed:.1f}s | {len(world_output)}字符 | tokens:{world_usage.get('total_tokens', 0)}")
        print(f"    input  → {world_in_path}")
        print(f"    output → {world_out_path}")
    except Exception as e:
        print(f"  world失败: {e}")
        return None

    return {
        "book": book_name,
        "decon_output": decon_output,
        "world_output": world_output,
    }

def main():
    os.makedirs(INPUTS_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("=" * 60)
    print("R45 world v1.5.0力量体系四层结构测试")
    print("测试方案：2本修仙对比测")
    print(f"  A：《玄鉴仙族》（季越人）")
    print(f"  B：《没钱修什么仙》（熊狼狗）")
    print("=" * 60)

    results = []
    for book in BOOKS:
        result = process_book(book)
        if result:
            results.append(result)

    # 汇总
    print(f"\n{'='*60}")
    print("R45测试完成！")
    print(f"{'='*60}")
    print(f"\n产出文件:")
    for book_name in [b["name"] for b in BOOKS]:
        print(f"  《{book_name}》:")
        print(f"    decon-lite → output/decon-{book_name}.md")
        print(f"    world四层  → output/world-{book_name}.md")
        print(f"    inputs     → inputs/{book_name}_decon_input.md")
        print(f"                 inputs/{book_name}_world_input.md")

    print(f"\n下一步：人工验收")
    print(f"  1. decon-lite表1是否拆到规则级（子养成线+交叉规则+chXX出处）")
    print(f"  2. world四层结构是否完整（源力量/主养成线含社会地位/子养成线含阶位+挂钩/交叉规则）")
    print(f"  3. world是否逐条消费decon-lite（禁止丢条自编）")
    print(f"  4. 阶位名是否有文化渊源（禁止通用词）")
    print(f"  5. 两本书的world产出是否反映了decon差异（不是同质化）")

if __name__ == "__main__":
    main()
