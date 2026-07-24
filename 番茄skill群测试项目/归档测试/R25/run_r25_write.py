#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
R25测试: 剧情白描对write的影响
- 复用R22的seed产出
- 复用R24的骨架+剧情白描产出
- 复用R23的笔触DNA
- 跑write v7.0.0产出ch01
- 对比R23（只有骨架+笔触DNA，无剧情白描）的ch01产出
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

# 复用产出路径
R22_OUTPUT = r"d:\popwave-skills\番茄skill群测试项目\R22\output"
R24_OUTPUT = r"d:\popwave-skills\番茄skill群测试项目\R24\output"
R23_INPUT = r"d:\popwave-skills\番茄skill群测试项目\R23\input"

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


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    results = {}

    print("=" * 60)
    print("R25测试: 剧情白描对write的影响")
    print("复用R22 seed + R24骨架+剧情白描 + R23笔触DNA")
    print("=" * 60)

    # ========== 加载所有产出 ==========
    print(f"\n[0] 加载产出...")
    r22_seed_path = os.path.join(R22_OUTPUT, "r22-seed.md")
    r24_plot_path = os.path.join(R24_OUTPUT, "r24-plot.md")
    r24_narrative_path = os.path.join(R24_OUTPUT, "r24-剧情白描.md")
    dna_path = os.path.join(R23_INPUT, "笔触DNA.md")

    with open(r22_seed_path, "r", encoding="utf-8") as f:
        seed_content = f.read()
    with open(r24_plot_path, "r", encoding="utf-8") as f:
        plot_content = f.read()
    with open(r24_narrative_path, "r", encoding="utf-8") as f:
        narrative_content = f.read()
    with open(dna_path, "r", encoding="utf-8") as f:
        dna_content = f.read()

    print(f"  Seed: {len(seed_content)}字")
    print(f"  Plot骨架: {len(plot_content)}字")
    print(f"  剧情白描: {len(narrative_content)}字")
    print(f"  笔触DNA: {len(dna_content)}字")

    # ========== Write ch01 (v7.0.0 + 剧情白描 + 笔触DNA) ==========
    print(f"\n[1/1] 调用DeepSeek执行Write ch01 (v7.0.0+剧情白描+笔触DNA)...")

    write_user = f"""# 任务

请按write skill v7.0.0全流程写第一章（ch01）正文。

5步SOP：
- Step 1: 加载燃料（创意+骨架+**剧情白描**+笔触DNA+心法分支+黄金开篇）
- Step 2: 章型+技法锁定（选章型+章意图思考+微观技法选择+爽感引擎选择+笔触DNA绑定）
- Step 3: 写正文（五层指导：笔触/节奏/格局/爽感/微观），2000-2500字，不准超过2500字
- Step 4: 篇幅硬限制检查+落盘
- Step 5: 交付面板

关键约束：
- 第一章用黄金开篇——前3句扔炸弹，300字内完成冲突+主角+金手指+钩子
- 第一章章型必选opening_shift
- 微观技法选2-3类（推荐：信息差博弈+感官锚点+预期违背）
- 爽感引擎选压力突破（主推）+未知揭示（次推）
- 笔触DNA已提供，必须绑定叙事距离/句式/物象/对话/情绪外化
- 系统面板用【】内联格式，禁止markdown代码块
- 对话引导词只用"道"
- 字数硬限制：2000-2500字，超2500字=废章
- 章末有钩子
- 不写思考过程/检查表——直接写正文+交付面板

**重要：剧情白描提供了ch01的完整故事流，写正文时参照剧情白描的ch01场景（手术室觉醒+因果棋盘激活+结算护士+逃出诊所），把白描转化为正文笔触。不是复制白描，是把白描的节奏和画面转化为番茄正文。**

直接输出正文+交付面板。

---

# 立项包（创意.md）

{seed_content}

---

# 骨架（骨架.md）

{plot_content}

---

# 剧情白描（1-骨架/剧情白描.md）— ch01场景参照

{narrative_content}

---

# 笔触DNA（0-立项/参考书拆书/笔触DNA.md）

{dna_content}
"""
    print(f"  System: {len(WRITE_SYSTEM)}字符 | User: {len(write_user)}字符")

    try:
        write_content, write_usage, write_elapsed = call_ds(WRITE_SYSTEM, write_user, max_tokens=8000, label="write")
        write_path = os.path.join(OUTPUT_DIR, "r25-ch01.md")
        with open(write_path, "w", encoding="utf-8") as f:
            f.write(write_content)
        print(f"  完成! {write_elapsed:.1f}s | {len(write_content)}字 | tokens:{write_usage.get('total_tokens', 'N/A')}")
        results["write_ch01"] = {
            "model": DS_MODEL,
            "content_length": len(write_content),
            "elapsed": round(write_elapsed, 1),
            "usage": write_usage,
            "path": write_path
        }
    except Exception as e:
        print(f"  Write失败: {e}")
        results["write_ch01"] = {"error": str(e)}

    # ========== 汇总 ==========
    meta_path = os.path.join(OUTPUT_DIR, "r25-meta.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*60}")
    print("R25测试完成！")
    print(f"{'='*60}")
    for stage, val in results.items():
        if "error" in val:
            print(f"  {stage}: 失败 - {val['error']}")
        else:
            print(f"  {stage}: {val['content_length']}字 | {val['elapsed']}s | tokens:{val['usage'].get('total_tokens', 'N/A')}")
    print(f"\n输出目录: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
