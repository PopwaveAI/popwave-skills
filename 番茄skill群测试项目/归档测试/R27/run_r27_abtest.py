#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
R27测试: AB测试输入最有效方式
对R26的输入进行较大尺度改造（删减/精炼），看哪种输入组合最有效

AB测试矩阵（全部跑ch001，控制变量）：
- A组（基准）：Phase3 + Phase2 + Phase1.5 + 白描卡（R26完整版）
- B组（删故事层）：Phase3 + Phase2 + 白描卡（删Phase1.5剧情白描）
- C组（删设定库）：Phase2 + Phase1.5 + 白描卡（删Phase3 L1六件套）
- D组（极简/单卡）：只白描卡ch001（最小输入）

目的：找出每个输入组件的贡献度，找到最有效输入方式
"""

import os
import sys
import json
import time
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

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

    # Phase2 L2+卷纲
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

    # 白描卡ch001
    ch_path = os.path.join(CHAPTERS_DIR, "ch001.md")
    with open(ch_path, "r", encoding="utf-8") as f:
        files["ch001"] = f.read()

    return files


def build_prompt_a(decon_files):
    """A组：完整输入（R26基准）"""
    return f"""# 任务

请按write skill v7.0.0全流程写本章（ch001）正文。

5步SOP：
- Step 1: 加载燃料（设定库+卷纲+剧情白描+白描卡+心法分支）
- Step 2: 章型+技法锁定（根据白描卡的POV/章型，选番茄章型+微观技法+爽感引擎）
- Step 3: 写正文（五层指导：笔触/节奏/格局/爽感/微观），2000-2500字，不准超过2500字
- Step 4: 篇幅硬限制检查+落盘
- Step 5: 交付面板

关键约束：
- **参照白描卡写**：白描卡是原文的压缩版，包含POV/章型/事件/爽点/钩子/人物关系变化
- **番茄快爽改造**：节奏更紧凑、爽感更密集、章末钩子更主动
- 章型选择：根据白描卡的章型映射番茄章型（转折→confrontation_pressure，成长→combat_reversal或reveal_hook，开篇→opening_shift）
- 微观技法选2-3类
- 爽感引擎根据章型选择
- 系统面板用【】内联格式，禁止markdown代码块
- 对话引导词只用"道"
- 字数硬限制：2000-2500字
- 章末有钩子
- 不写思考过程/检查表——直接写正文+交付面板

直接输出正文+交付面板。

---

# 设定库（Phase3 L1六件套）

{decon_files['phase3']}

---

# 卷纲+L2单元卡（Phase2）

{decon_files['phase2']}

---

# 剧情白描（Phase1.5全书故事流）

{decon_files['phase15']}

---

# 本章白描卡（ch001）

{decon_files['ch001']}
"""


def build_prompt_b(decon_files):
    """B组：删故事层（删Phase1.5剧情白描）"""
    return f"""# 任务

请按write skill v7.0.0全流程写本章（ch001）正文。

5步SOP：
- Step 1: 加载燃料（设定库+卷纲+白描卡+心法分支）
- Step 2: 章型+技法锁定
- Step 3: 写正文，2000-2500字，不准超过2500字
- Step 4: 篇幅硬限制检查+落盘
- Step 5: 交付面板

关键约束：
- **参照白描卡写**：白描卡是原文的压缩版
- **番茄快爽改造**：节奏更紧凑、爽感更密集、章末钩子更主动
- 系统面板用【】内联格式
- 对话引导词只用"道"
- 字数硬限制：2000-2500字
- 章末有钩子
- 不写思考过程/检查表

直接输出正文+交付面板。

---

# 设定库（Phase3 L1六件套）

{decon_files['phase3']}

---

# 卷纲+L2单元卡（Phase2）

{decon_files['phase2']}

---

# 本章白描卡（ch001）

{decon_files['ch001']}
"""


def build_prompt_c(decon_files):
    """C组：删设定库（删Phase3 L1六件套）"""
    return f"""# 任务

请按write skill v7.0.0全流程写本章（ch001）正文。

5步SOP：
- Step 1: 加载燃料（卷纲+剧情白描+白描卡+心法分支）
- Step 2: 章型+技法锁定
- Step 3: 写正文，2000-2500字，不准超过2500字
- Step 4: 篇幅硬限制检查+落盘
- Step 5: 交付面板

关键约束：
- **参照白描卡写**：白描卡是原文的压缩版
- **番茄快爽改造**：节奏更紧凑、爽感更密集、章末钩子更主动
- 系统面板用【】内联格式
- 对话引导词只用"道"
- 字数硬限制：2000-2500字
- 章末有钩子
- 不写思考过程/检查表

直接输出正文+交付面板。

---

# 卷纲+L2单元卡（Phase2）

{decon_files['phase2']}

---

# 剧情白描（Phase1.5全书故事流）

{decon_files['phase15']}

---

# 本章白描卡（ch001）

{decon_files['ch001']}
"""


def build_prompt_d(decon_files):
    """D组：极简/单卡（只白描卡ch001）"""
    return f"""# 任务

请按write skill v7.0.0全流程写本章（ch001）正文。

5步SOP：
- Step 1: 加载燃料（白描卡+心法分支）
- Step 2: 章型+技法锁定
- Step 3: 写正文，2000-2500字，不准超过2500字
- Step 4: 篇幅硬限制检查+落盘
- Step 5: 交付面板

关键约束：
- **参照白描卡写**：白描卡是原文的压缩版
- **番茄快爽改造**：节奏更紧凑、爽感更密集、章末钩子更主动
- 系统面板用【】内联格式
- 对话引导词只用"道"
- 字数硬限制：2000-2500字
- 章末有钩子
- 不写思考过程/检查表

直接输出正文+交付面板。

---

# 本章白描卡（ch001）

{decon_files['ch001']}
"""


def run_test(group_name, prompt_builder, decon_files):
    """单组测试"""
    print(f"\n[{group_name}] 开始...")
    user_prompt = prompt_builder(decon_files)
    prompt_len = len(user_prompt)
    print(f"  Prompt长度: {prompt_len}字符")

    try:
        content, usage, elapsed = call_ds(
            WRITE_SYSTEM, user_prompt, max_tokens=8000, label=group_name
        )
        out_path = os.path.join(OUTPUT_DIR, f"r27-{group_name}-ch001.md")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  完成! {elapsed:.1f}s | {len(content)}字 | tokens:{usage.get('total_tokens', 'N/A')}")
        return {
            "group": group_name,
            "prompt_length": prompt_len,
            "content_length": len(content),
            "elapsed": round(elapsed, 1),
            "usage": usage,
            "path": out_path,
            "content": content
        }
    except Exception as e:
        print(f"  失败: {e}")
        return {"group": group_name, "error": str(e)}


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("=" * 60)
    print("R27测试: AB测试输入最有效方式")
    print("=" * 60)

    # 加载拆书产出
    print(f"\n[0] 加载拆书产出...")
    decon_files = load_decon_files()
    print(f"  Phase1.5剧情白描: {len(decon_files['phase15'])}字")
    print(f"  Phase2 L2+卷纲: {len(decon_files['phase2'])}字")
    print(f"  Phase3 L1六件套: {len(decon_files['phase3'])}字")
    print(f"  白描卡ch001: {len(decon_files['ch001'])}字")

    # 定义4组测试
    test_groups = [
        ("A-完整", build_prompt_a),       # 基准：完整输入
        ("B-删故事层", build_prompt_b),    # 删Phase1.5
        ("C-删设定库", build_prompt_c),    # 删Phase3
        ("D-单卡", build_prompt_d),        # 只白描卡
    ]

    # 并行跑4组
    print(f"\n[1] 并行跑4组AB测试...")
    results = {}

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {}
        for group_name, builder in test_groups:
            future = executor.submit(run_test, group_name, builder, decon_files)
            futures[future] = group_name

        for future in as_completed(futures):
            group_name = futures[future]
            try:
                result = future.result()
                results[group_name] = result
            except Exception as e:
                results[group_name] = {"error": str(e)}
                print(f"\n[{group_name}] 异常: {e}")

    # 保存meta
    meta_path = os.path.join(OUTPUT_DIR, "r27-meta.json")
    meta_save = {}
    for k, v in results.items():
        meta_save[k] = {key: val for key, val in v.items() if key != "content"}
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta_save, f, ensure_ascii=False, indent=2)

    # 汇总
    print(f"\n{'='*60}")
    print("R27测试完成！")
    print(f"{'='*60}")
    print(f"\n{'组别':<12} {'输入字数':<10} {'产出字数':<10} {'耗时':<8} {'tokens':<10}")
    print("-" * 60)
    for group_name, _ in test_groups:
        val = results.get(group_name, {})
        if "error" in val:
            print(f"{group_name:<12} 失败: {val['error']}")
        else:
            tokens = val['usage'].get('total_tokens', 0)
            print(f"{group_name:<12} {val['prompt_length']:<10} {val['content_length']:<10} {val['elapsed']:<8} {tokens:<10}")

    print(f"\n输出目录: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
