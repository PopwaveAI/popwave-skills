#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
R30测试: seed+plot全链路产出 vs 拆书产出
验证迭代后的seed/plot能否交付R29级别的正文质量

流程：
1. 一次性调用API生成seed+plot全套产出（基于最小创意）
   - seed: 创意.md（含金手指设计+角色深度设计+世界观骨架）
   - plot: 骨架.md + 剧情白描.md + 章锚点表.md
2. 用生成的产出作为write输入，跑10章串联
3. 对比R29（拆书产出）看"好看"的差距

创意输入（最小化）：
"DND数据化面板+杀戮升级+西幻封神，贫民窟半精灵穿越者保护妹妹"
"""

import os
import sys
import json
import time
import requests

# ============ API配置 ============
DS_API_KEY = "sk-5a3654e4aa2e4eefa08abe3d0e0231f5"
DS_BASE_URL = "https://api.deepseek.com/v1"
DS_MODEL = "deepseek-v4-flash"

TEMPERATURE = 0.7
TIMEOUT = 600
MAX_CHAPTERS = 10

# ============ 目录 ============
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")

# ============ 读取skill文件 ============
SKILLS_BASE = r"d:\popwave-skills\skills"

def read_skill_files(skill_name, files):
    parts = []
    for f in files:
        path = os.path.join(SKILLS_BASE, skill_name, f)
        with open(path, "r", encoding="utf-8") as fh:
            parts.append(fh.read())
    return "\n\n---\n\n".join(parts)

SEED_SYSTEM = read_skill_files("pop-fanqie-seed", [
    "SKILL.md",
    "steps/step1.md",
    "steps/step2.md",
    "steps/step3.md",
])

PLOT_SYSTEM = read_skill_files("pop-fanqie-plot", [
    "SKILL.md",
    "steps/step1.md",
    "steps/step2.md",
    "steps/step3.md",
])

WRITE_SYSTEM_V71 = read_skill_files("pop-fanqie-write", [
    "SKILL.md",
    "steps/step1.md",
    "steps/step2.md",
    "steps/step3.md",
    "steps/step4.md",
    "steps/step5.md",
    "references/章型定义.md",
    "references/爽点引擎.md",
])

# ============ API调用 ============

def call_ds(system_prompt, user_prompt, max_tokens=12000, label=""):
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
    response = requests.post(url, headers=headers, json=payload, timeout=TIMEOUT)
    response.raise_for_status()
    elapsed = time.time() - start
    result = response.json()
    content = result["choices"][0]["message"]["content"]
    usage = result.get("usage", {})
    return content, usage, elapsed


# ============ Step 1: seed产出 ============

SEED_PROMPT = """# 任务

请按seed skill全流程，基于以下最小创意，产出完整的立项包。

## 创意输入（最小化）

**书名**：深渊主宰（测试用，复刻拆书项目的设定方向）
**核心创意**：DND数据化面板+杀戮升级+西幻封神，贫民窟半精灵穿越者保护妹妹

## 产出要求

按seed step2的7个产出+新增的角色深度设计+金手指深度设计，一次性产出：

1. 一句话故事
2. 草纲
3. 金手指（含深度设计：类型判定+功能分类+升级路径+限制条件+副作用+剧情驱动）
4. 主角设定卡+角色深度设计（含致命缺陷+人物弧光5阶段+行为模式+核心羁绊角色2人+终极对手1人）
5. 世界观骨架（6要素，含具体数值：力量体系六大属性+等级阶位+升级机制+种族特征）
6. 长线线索
7. 番茄简介

**关键约束**：
- 金手指必须有升级路径（5-7阶段，与力量体系对齐）
- 主角必须有致命缺陷（驱动矛盾的核心）
- 每个核心角色都有人物弧光（3-5阶段）
- 世界观骨架必须包含具体数值（属性数值/等级阶位/种族特征）

直接输出完整立项包，不要写思考过程。
"""


# ============ Step 2: plot产出 ============

def build_plot_prompt(seed_output):
    return f"""# 任务

请按plot skill全流程，基于以下seed立项包，产出第一卷的骨架+剧情白描+章锚点表。

## seed立项包

{seed_output}

## 产出要求

按plot step3的3个产出：

### 1. 骨架.md
第一卷结构详规（含配角设计+幕序列+悬念分层+核心高潮点+势力格局+分层反派+世界危机映射+角色关系图谱+剧情冲突表）

### 2. 剧情白描.md（最核心产出）
- 整卷一口气写完，第一卷约20章
- 含信息差标注(读者知道但角色不知道：XXX)
- 含伏笔标注(伏笔：XXX，chXX回收)
- 含钩子标注(钩子：XXX)
- 消化设定库（力量体系/种族/势力/历史融入故事流）
- 长度：6000-10000字

### 3. 章锚点表.md（新增）
每章一行，包含：章号/POV/章型/核心事件/爽点/钩子/预期回收章/关键数据
第一卷20章全部列出。

**关键约束**：
- 剧情白描必须整卷一口气写完，不拆章节标签
- 章锚点表必须有"预期回收章"字段
- 必须消化seed的设定库（不在剧情白描里列数值，而是融入故事）

直接输出3个产出，用---分隔。
"""


# ============ Step 3: write 10章串联 ============

def build_write_prompt(seed_output, plot_output, ch_num, prev_chapter):
    """构建write prompt"""
    chapter_hint = ""
    if ch_num == "ch001":
        chapter_hint = "第一章使用黄金开篇：前3句扔炸弹，300字内完成冲突+主角+金手指+钩子"
    else:
        chapter_hint = f"如非第一章，必须回收前章钩子——本章前300字必须回收前章章末钩子。前章正文已注入下方。"

    prompt = f"""# 任务

请按write skill全流程写本章（{ch_num}）正文。

5步SOP：
- Step 1: 加载燃料（下方seed立项包+plot产出）
- Step 2: 章型+技法锁定
- Step 3: 写正文，2000-2500字，不准超过2500字
- Step 4: 篇幅硬限制检查
- Step 5: 交付面板

关键约束：
- **参照章锚点表写**：章锚点表是每章导航
- **番茄快爽改造**：节奏更紧凑、爽感更密集、章末钩子更主动
- 系统面板用【】内联格式，禁止markdown代码块
- 对话引导词只用"道"
- 字数硬限制：2000-2500字
- 章末有钩子
- {chapter_hint}
- 不写思考过程/检查表——直接写正文+交付面板

直接输出正文+交付面板。

---

# seed立项包（含设定库）

{seed_output}

---

# plot产出（骨架+剧情白描+章锚点表）

{plot_output}
"""
    if prev_chapter:
        prompt += f"\n\n---\n\n# 前一章正文（用于回收钩子）\n\n{prev_chapter}\n"
    return prompt


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("=" * 60)
    print("R30测试: seed+plot全链路产出 vs 拆书产出")
    print("=" * 60)

    # Step 1: seed产出
    print(f"\n[Step 1] seed产出...")
    start = time.time()
    seed_output, seed_usage, seed_elapsed = call_ds(
        SEED_SYSTEM, SEED_PROMPT, max_tokens=12000, label="seed"
    )
    print(f"  完成! {seed_elapsed:.1f}s | {len(seed_output)}字 | tokens:{seed_usage.get('total_tokens', 0)}")

    seed_path = os.path.join(OUTPUT_DIR, "seed-立项包.md")
    with open(seed_path, "w", encoding="utf-8") as f:
        f.write(seed_output)

    # Step 2: plot产出
    print(f"\n[Step 2] plot产出...")
    plot_prompt = build_plot_prompt(seed_output)
    plot_output, plot_usage, plot_elapsed = call_ds(
        PLOT_SYSTEM, plot_prompt, max_tokens=16000, label="plot"
    )
    print(f"  完成! {plot_elapsed:.1f}s | {len(plot_output)}字 | tokens:{plot_usage.get('total_tokens', 0)}")

    plot_path = os.path.join(OUTPUT_DIR, "plot-产出.md")
    with open(plot_path, "w", encoding="utf-8") as f:
        f.write(plot_output)

    # Step 3: write 10章串联
    print(f"\n[Step 3] write 10章串联...")
    results = []
    prev_chapter = None

    for ch_idx in range(1, MAX_CHAPTERS + 1):
        ch_num = f"ch{ch_idx:03d}"
        user_prompt = build_write_prompt(seed_output, plot_output, ch_num, prev_chapter)
        prompt_len = len(user_prompt)
        print(f"  [{ch_idx}/10] {ch_num} 调用DeepSeek... (prompt: {prompt_len}字符)")

        try:
            content, usage, elapsed = call_ds(
                WRITE_SYSTEM_V71, user_prompt, max_tokens=8000, label=f"R30_{ch_num}"
            )
            out_path = os.path.join(OUTPUT_DIR, f"{ch_num}.md")
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(content)
            tokens = usage.get('total_tokens', 0)
            print(f"    完成! {elapsed:.1f}s | {len(content)}字 | tokens:{tokens}")

            results.append({
                "ch_num": ch_num,
                "prompt_length": prompt_len,
                "content_length": len(content),
                "elapsed": round(elapsed, 1),
                "tokens": tokens,
                "path": out_path
            })
            prev_chapter = content

        except Exception as e:
            print(f"    {ch_num}失败: {e}")
            results.append({"ch_num": ch_num, "error": str(e)})
            prev_chapter = None

    # 汇总
    print(f"\n{'='*60}")
    print("R30测试完成！")
    print(f"{'='*60}")
    print(f"\nSeed产出: {len(seed_output)}字 / {seed_elapsed:.1f}s")
    print(f"Plot产出: {len(plot_output)}字 / {plot_elapsed:.1f}s")
    print(f"\n{'章号':<10} {'输入字数':<10} {'产出字数':<10} {'耗时':<8} {'tokens':<10}")
    print("-" * 60)
    for r in results:
        if "error" in r:
            print(f"{r.get('ch_num','?'):<10} 失败: {r['error']}")
        else:
            print(f"{r['ch_num']:<10} {r['prompt_length']:<10} {r['content_length']:<10} {r['elapsed']:<8} {r['tokens']:<10}")

    # 保存meta
    meta = {
        "seed": {"length": len(seed_output), "elapsed": seed_elapsed, "tokens": seed_usage.get('total_tokens', 0)},
        "plot": {"length": len(plot_output), "elapsed": plot_elapsed, "tokens": plot_usage.get('total_tokens', 0)},
        "chapters": [{k: v for k, v in r.items() if k != "path"} for r in results]
    }
    meta_path = os.path.join(OUTPUT_DIR, "r30-meta.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    print(f"\n输出目录: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
