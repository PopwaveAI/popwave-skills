#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
R22场景A测试: 用户只给一句话创意 → seed → plot → write ch01
验证: 无参考书DNA注入时，skill能否自己完善小说创意

对比基准: R21/项目C（场景B·有DNA注入）
关键测试点: seed在只有一句话创意时，能否自动补全7产出
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

# ============ Seed System Prompt ============
SEED_SYSTEM = read_skill_files("pop-fanqie-seed", [
    "SKILL.md",
    "steps/step1.md",
    "steps/step2.md",
    "steps/step3.md",
    "steps/step4.md",
    "reference/design-guide.md",
])

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

# ============ 最小创意输入 ============
# 老板要求跑印度版，最小创意=一句话
MINIMAL_IDEA = "我想写一个中国大学生在印度被骗到地下诊所活取器官，觉醒阎摩因果棋盘系统的故事"

# ============ API调用 ============

def call_ds(system_prompt, user_prompt, max_tokens=16000, label=""):
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

    print("=" * 60)
    print("R22场景A测试: 一句话创意 → seed → plot → write ch01")
    print(f"最小创意: {MINIMAL_IDEA}")
    print("=" * 60)

    # ========== 1. Seed阶段 ==========
    print(f"\n[1/3] 调用DeepSeek执行Seed (场景A·无DNA注入)...")
    seed_user = f"""# 用户输入

{MINIMAL_IDEA}

---

# 任务

按seed skill全流程执行：
- Step 1: 用户已给创意点子（一句话），按"直接给了创意/画面/一句话"路径——跳过1b标签搜索，直接进1d（用用户创意为A画面，仍需补B限制+C反差）
- Step 2: 立项展开7个产出
- Step 3: 验证（六项检查）
- Step 4: 如果验证通过，直接输出完整立项包（创意.md格式）

注意：
- 用户只给了一句话创意，没有给赛道/元素/参考书
- 禁止问用户问题——基于这一句话创意自主推断和补全
- 金手指本质要设计（进化到尽头触及什么世界真相？）
- 主角危机必须是存在性危机（与金手指本质挂钩，不是任务式倒计时）
- 世界观必须有世界格局/力量体系（多路径）/世界危机/势力格局
- 金手指只加限制不加代价
- 世界自洽四问必须全部回答

直接输出完整立项包，不要问用户，不要分段确认。
"""
    print(f"  System: {len(SEED_SYSTEM)}字符 | User: {len(seed_user)}字符")
    try:
        seed_content, seed_usage, seed_elapsed = call_ds(SEED_SYSTEM, seed_user, max_tokens=16000, label="seed")
        seed_path = os.path.join(OUTPUT_DIR, "r22-seed.md")
        with open(seed_path, "w", encoding="utf-8") as f:
            f.write(seed_content)
        print(f"  完成! {seed_elapsed:.1f}s | {len(seed_content)}字 | tokens:{seed_usage.get('total_tokens', 'N/A')}")
        results["seed"] = {
            "model": DS_MODEL,
            "content_length": len(seed_content),
            "elapsed": round(seed_elapsed, 1),
            "usage": seed_usage,
            "path": seed_path
        }
    except Exception as e:
        print(f"  Seed失败: {e}")
        results["seed"] = {"error": str(e)}
        return

    # ========== 2. Plot阶段 ==========
    print(f"\n[2/3] 调用DeepSeek执行Plot (生成骨架)...")
    plot_user = f"""# 任务

以下是完整立项包（创意.md），请按plot skill全流程执行：
- Step 1: 加载立项包7项
- Step 2: 第一卷详规（终点+配角+幕序列+悬念+高潮+势力+反派+世界危机）
- Step 3: 落盘骨架.md

直接输出完整骨架.md，不要分段确认，不要问用户。

---

# 立项包

{seed_content}
"""
    print(f"  System: {len(PLOT_SYSTEM)}字符 | User: {len(plot_user)}字符")
    try:
        plot_content, plot_usage, plot_elapsed = call_ds(PLOT_SYSTEM, plot_user, max_tokens=16000, label="plot")
        plot_path = os.path.join(OUTPUT_DIR, "r22-plot.md")
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
    print(f"\n[3/3] 调用DeepSeek执行Write (写ch01正文)...")
    write_user = f"""# 任务

请按write skill全流程写第一章（ch01）正文。

- Step 1: 加载燃料（第一章读立项包+骨架；确定心法分支；黄金开篇）
- Step 2: 写正文（2000-2500字，不准超3000字）
- Step 3: 篇幅控制检查
- Step 4: 交付面板

注意：
- 第一章用黄金开篇——前3句扔炸弹，300字内完成冲突+主角+金手指+钩子
- 心法分支根据金手指类型自动选择
- 系统面板用【】内联格式，禁止用markdown代码块
- 对话引导词只用"道"
- 章末有钩子
- 参照主角记忆点和缺点写人物
- 不写思考过程/检查表——直接写正文

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
        write_content, write_usage, write_elapsed = call_ds(WRITE_SYSTEM, write_user, max_tokens=8000, label="write")
        write_path = os.path.join(OUTPUT_DIR, "r22-ch01.md")
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
    meta_path = os.path.join(OUTPUT_DIR, "r22-meta.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*60}")
    print("R22场景A测试完成！")
    print(f"{'='*60}")
    for stage, val in results.items():
        if "error" in val:
            print(f"  {stage}: 失败 - {val['error']}")
        else:
            print(f"  {stage}: {val['content_length']}字 | {val['elapsed']}s | tokens:{val['usage'].get('total_tokens', 'N/A')}")
    print(f"\n输出目录: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
