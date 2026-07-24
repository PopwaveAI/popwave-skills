#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
R26测试: 深渊主宰拆书产出 → 番茄write skill → ch01-ch10
验证目的：如果最细节的plot都写不出原文感觉，问题是write层就有问题

输入：
- Phase3 L1六件套（设定库）替代创意.md
- Phase2 L2+卷纲替代骨架.md
- Phase1.5剧情白描作为故事层
- 白描卡ch001-010作为每章锚点

对比基准：白描卡（原文节奏的压缩版）
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

# ============ 目录 ============
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")

# 深渊主宰拆书产出路径
DECON_BASE = r"d:\popwave-skills\workspace\深渊主宰-瘦身白描测试"
PHASE15_PATH = os.path.join(DECON_BASE, "下游产出", "Phase1.5-全书剧情白描.md")
PHASE2_PATH = os.path.join(DECON_BASE, "下游产出", "Phase2-L2单元卡+卷纲+叙事技法.md")
PHASE2B_PATH = os.path.join(DECON_BASE, "下游测试", "Phase2-L2单元卡+卷纲.md")
PHASE3_DIR = os.path.join(DECON_BASE, "下游测试")
CHAPTERS_DIR = os.path.join(DECON_BASE, "chapters")

# ============ 读取skill文件 ============
SKILLS_BASE = r"d:\popwave-skills\skills"

def read_skill_files(skill_name, files):
    parts = []
    for f in files:
        path = os.path.join(SKILLS_BASE, skill_name, f)
        with open(path, "r", encoding="utf-8") as fh:
            parts.append(fh.read())
    return "\n\n---\n\n".join(parts)

# ============ Write System Prompt (v7.0.0) ============
WRITE_SYSTEM = read_skill_files("pop-fanqie-write", [
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

def call_ds(system_prompt, user_prompt, max_tokens=8000, label=""):
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


def load_decon_files():
    """加载所有拆书产出"""
    files = {}

    # Phase1.5 剧情白描
    with open(PHASE15_PATH, "r", encoding="utf-8") as f:
        files["phase15"] = f.read()

    # Phase2 L2+卷纲（用下游产出版本，更完整）
    with open(PHASE2_PATH, "r", encoding="utf-8") as f:
        files["phase2"] = f.read()

    # Phase3 L1六件套
    phase3_files = [
        "Phase3-L1-01-世界蓝图.md",
        "Phase3-L1-02-力量体系.md",
        "Phase3-L1-03-历史与驱动力.md",
        "Phase3-L1-04-物种与天赋.md",
        "Phase3-L1-05-势力格局.md",
        "Phase3-L1-06-资源与物品.md",
    ]
    phase3_content = []
    for fname in phase3_files:
        fpath = os.path.join(PHASE3_DIR, fname)
        if os.path.exists(fpath):
            with open(fpath, "r", encoding="utf-8") as f:
                phase3_content.append(f"### {fname}\n\n{f.read()}")
    files["phase3"] = "\n\n---\n\n".join(phase3_content)

    # 白描卡ch001-010
    chapters = {}
    for i in range(1, 11):
        ch_num = f"ch{i:03d}"
        ch_path = os.path.join(CHAPTERS_DIR, f"{ch_num}.md")
        if os.path.exists(ch_path):
            with open(ch_path, "r", encoding="utf-8") as f:
                chapters[ch_num] = f.read()
    files["chapters"] = chapters

    return files


def build_write_prompt(ch_num, decon_files, prev_chapter=None):
    """构建每章的write prompt"""

    chapter_card = decon_files["chapters"].get(ch_num, "")

    # 构建Phase1.5的ch段（提取对应章节段落）
    phase15 = decon_files["phase15"]
    # Phase1.5包含ch001-411的故事流，直接全文注入（让模型自己找对应段落）

    user_prompt = f"""# 任务

请按write skill v7.0.0全流程写本章（{ch_num}）正文。

5步SOP：
- Step 1: 加载燃料（设定库+卷纲+剧情白描+白描卡+心法分支+前章钩子回收）
- Step 2: 章型+技法锁定（根据白描卡的POV/章型，选番茄章型+微观技法+爽感引擎）
- Step 3: 写正文（五层指导：笔触/节奏/格局/爽感/微观），2000-2500字，不准超过2500字
- Step 4: 篇幅硬限制检查+落盘
- Step 5: 交付面板

关键约束：
- **参照白描卡写**：白描卡是原文的压缩版，包含POV/章型/事件/爽点/钩子/人物关系变化。写正文时参照白描卡的事件，但用番茄快爽笔触渲染。
- **番茄快爽改造**：原文是西幻DnD风格（半精灵/盗贼/属性面板），用番茄快爽逻辑改造——节奏更紧凑、爽感更密集、章末钩子更主动。
- 章型选择：根据白描卡的章型映射番茄章型（转折→confrontation_pressure，成长→combat_reversal或reveal_hook，开篇→opening_shift）
- 微观技法选2-3类
- 爽感引擎根据章型选择
- 系统面板用【】内联格式，禁止markdown代码块
- 对话引导词只用"道"
- 字数硬限制：2000-2500字
- 章末有钩子
- **如非第一章，必须回收前章钩子**
- 不写思考过程/检查表——直接写正文+交付面板

直接输出正文+交付面板。

---

# 设定库（Phase3 L1六件套）— 创意.md替代

{decon_files['phase3']}

---

# 卷纲+L2单元卡（Phase2）— 骨架.md替代

{decon_files['phase2']}

---

# 剧情白描（Phase1.5全书故事流）— 剧情白描.md替代

{phase15}

---

# 本章白描卡（{ch_num}）— 本章锚点

{chapter_card}
"""

    if prev_chapter:
        user_prompt += f"\n\n---\n\n# 前一章正文（用于回收钩子）\n\n{prev_chapter}\n"

    return user_prompt


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    results = {}

    print("=" * 60)
    print("R26测试: 深渊主宰拆书产出 → 番茄write skill → ch01-ch10")
    print("=" * 60)

    # ========== 加载拆书产出 ==========
    print(f"\n[0] 加载拆书产出...")
    decon_files = load_decon_files()
    print(f"  Phase1.5剧情白描: {len(decon_files['phase15'])}字")
    print(f"  Phase2 L2+卷纲: {len(decon_files['phase2'])}字")
    print(f"  Phase3 L1六件套: {len(decon_files['phase3'])}字")
    print(f"  白描卡: {len(decon_files['chapters'])}章")

    # ========== 逐章生成ch01-ch03（先验证，好再跑ch04-10）==========
    prev_chapter = None

    # 限制只跑前3章验证
    end_ch = 4  # 跑ch01-ch03
    for ch_idx in range(1, end_ch):
        ch_num = f"ch{ch_idx:03d}"

        if ch_num not in decon_files["chapters"]:
            print(f"\n[{ch_idx}/10] {ch_num} 白描卡不存在，跳过")
            continue

        print(f"\n[{ch_idx}/10] 调用DeepSeek写{ch_num}...")

        write_user = build_write_prompt(ch_num, decon_files, prev_chapter)
        print(f"  User prompt: {len(write_user)}字符")

        try:
            write_content, write_usage, write_elapsed = call_ds(
                WRITE_SYSTEM, write_user, max_tokens=8000, label=f"write_{ch_num}"
            )
            write_path = os.path.join(OUTPUT_DIR, f"r26-{ch_num}.md")
            with open(write_path, "w", encoding="utf-8") as f:
                f.write(write_content)
            print(f"  完成! {write_elapsed:.1f}s | {len(write_content)}字 | tokens:{write_usage.get('total_tokens', 'N/A')}")

            results[ch_num] = {
                "model": DS_MODEL,
                "content_length": len(write_content),
                "elapsed": round(write_elapsed, 1),
                "usage": write_usage,
                "path": write_path
            }

            # 保存前章正文用于下一章钩子回收
            prev_chapter = write_content

            # 保存meta
            meta_path = os.path.join(OUTPUT_DIR, "r26-meta.json")
            with open(meta_path, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)

        except Exception as e:
            print(f"  {ch_num}失败: {e}")
            results[ch_num] = {"error": str(e)}
            # 失败后继续下一章，但前章正文用空
            prev_chapter = None

    # ========== 汇总 ==========
    print(f"\n{'='*60}")
    print("R26测试完成！")
    print(f"{'='*60}")
    total_tokens = 0
    for ch_num, val in results.items():
        if "error" in val:
            print(f"  {ch_num}: 失败 - {val['error']}")
        else:
            tokens = val['usage'].get('total_tokens', 0)
            total_tokens += tokens
            print(f"  {ch_num}: {val['content_length']}字 | {val['elapsed']}s | tokens:{tokens}")
    print(f"\n总tokens消耗: {total_tokens}")
    print(f"输出目录: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
