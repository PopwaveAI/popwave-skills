#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
R21全链路测试: seed → plot → write ch01 (DeepSeek only)
验证DNA约束在整个pipeline中的传递效果
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
TIMEOUT = 300

# ============ 目录 ============
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")

# ============ 读取skill文件 ============
SKILLS_BASE = r"d:\popwave-skills\skills"

def read_skill_files(skill_name, files):
    """读取skill的多个文件并拼接"""
    parts = []
    for f in files:
        path = os.path.join(SKILLS_BASE, skill_name, f)
        with open(path, "r", encoding="utf-8") as fh:
            parts.append(fh.read())
    return "\n\n---\n\n".join(parts)

# ============ Plot System Prompt ============
PLOT_SYSTEM = read_skill_files("pop-fanqie-plot", [
    "SKILL.md",
    "steps/step1.md",
    "steps/step2.md",
    "steps/step3.md",
])

# ============ Write System Prompt ============
WRITE_SYSTEM = read_skill_files("pop-fanqie-write", [
    "SKILL.md",
    "steps/step1.md",
    "steps/step2.md",
    "steps/step3.md",
    "steps/step4.md",
])

# ============ API调用 ============

def call_ds(system_prompt, user_prompt, max_tokens=16000):
    """调用DeepSeek API"""
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

    # ========== 1. 读取seed产出 ==========
    seed_path = os.path.join(OUTPUT_DIR, "r21-ds-seed.md")
    print("=" * 60)
    print("R21全链路测试: seed → plot → write ch01")
    print("=" * 60)

    with open(seed_path, "r", encoding="utf-8") as f:
        seed_content = f.read()
    print(f"\n[0/3] 已加载seed产出: {len(seed_content)}字")

    # ========== 2. Plot阶段 ==========
    print(f"\n[1/3] 调用DeepSeek执行Plot (生成骨架)...")
    plot_user = f"""# 任务

以下是完整立项包（创意.md），请按plot skill全流程执行：
- Step 1: 加载立项包7项
- Step 2: 第一卷详规（终点+配角+幕序列+悬念+高潮+势力+反派+世界危机）
- Step 3: 落盘骨架.md

直接输出完整骨架.md，不要分段确认，不要问用户。

特别注意立项包末尾的"心法备忘"部分——这是从参考书DNA提取的约束，plot骨架设计必须遵守：
- 单元剧循环：每3-4章一个战斗闭环
- 战斗vs非战斗比例 = 3:2
- Boss设计：ch02-03首次暗示，8章铺垫，第一次交互是谈判不是战斗
- NPC标注：每章至少1次主动标注新NPC

---

# 立项包

{seed_content}
"""
    print(f"  System: {len(PLOT_SYSTEM)}字符 | User: {len(plot_user)}字符")
    try:
        plot_content, plot_usage, plot_elapsed = call_ds(PLOT_SYSTEM, plot_user, max_tokens=16000)
        plot_path = os.path.join(OUTPUT_DIR, "r21-ds-plot.md")
        with open(plot_path, "w", encoding="utf-8") as f:
            f.write(plot_content)
        print(f"  完成! {plot_elapsed:.1f}s | {len(plot_content)}字 | tokens:{plot_usage.get('total_tokens', 'N/A')}")
        results["plot"] = {
            "model": DS_MODEL,
            "content_length": len(plot_content),
            "elapsed": round(plot_elapsed, 1),
            "usage": plot_usage,
            "path": plot_path
        }
    except Exception as e:
        print(f"  Plot失败: {e}")
        results["plot"] = {"error": str(e)}
        return

    # ========== 3. Write ch01阶段 ==========
    print(f"\n[2/3] 调用DeepSeek执行Write (写ch01正文)...")
    write_user = f"""# 任务

请按write skill全流程写第一章（ch01）正文。

- Step 1: 加载燃料（第一章读立项包+骨架；确定心法分支=系统流；黄金开篇）
- Step 2: 写正文（2000-2500字，不准超3000字）
- Step 3: 篇幅控制检查
- Step 4: 交付面板

注意：
- 第一章用黄金开篇——前3句扔炸弹，300字内完成冲突+主角+金手指+钩子
- 心法分支选A（系统流）：系统交互即爽点/战术博弈>蛮力/弱→强反差/冷性满足/每章≥1次系统交互
- 系统面板用【】内联格式，禁止用markdown代码块
- 对话引导词只用"道"
- 章末有钩子
- 参照主角记忆点和缺点写人物
- 不写思考过程/检查表——直接写正文

立项包末尾的"心法备忘"是DNA约束，写作时参照执行：
- 系统面板格式：每章开局/收尾用系统面板展示状态变化
- NPC标注节奏：每章至少1次主动标注新NPC

直接输出正文+交付面板，不要问用户。

---

# 立项包（创意.md）

{seed_content}

---

# 骨架（骨架.md）

{plot_content}
"""
    print(f"  System: {len(WRITE_SYSTEM)}字符 | User: {len(write_user)}字符")
    try:
        write_content, write_usage, write_elapsed = call_ds(WRITE_SYSTEM, write_user, max_tokens=8000)
        write_path = os.path.join(OUTPUT_DIR, "r21-ds-ch01.md")
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

    # ========== 4. 汇总 ==========
    meta_path = os.path.join(OUTPUT_DIR, "r21-pipeline-meta.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*60}")
    print("R21全链路测试完成！")
    print(f"{'='*60}")
    for stage, val in results.items():
        if "error" in val:
            print(f"  {stage}: 失败 - {val['error']}")
        else:
            print(f"  {stage}: {val['content_length']}字 | {val['elapsed']}s | tokens:{val['usage'].get('total_tokens', 'N/A')}")
    print(f"\n输出目录: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
