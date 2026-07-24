#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
R28测试: 验证write skill v7.1.0优化效果

AB测试矩阵（全部跑ch001，控制变量）：
- A组（基准）：复用R27-C结果（旧skill v7.0.0 + 无设定库）
- B组（skill优化）：新skill v7.1.0 + 无设定库
- C组（精选设定）：新skill v7.1.0 + 精选设定库（力量体系+物种天赋，≤1000字）
- D组（完整抑制）：新skill v7.1.0 + 完整输入（含全文设定库，测能否抑制负面影响）

只需跑B/C/D三组，A组直接复用R27-C结果。
"""

import os
import sys
import json
import time
import shutil
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

# R27结果（A组复用）
R27_C_PATH = r"d:\popwave-skills\番茄skill群测试项目\R27\output\r27-C-删设定库-ch001.md"

# ============ 读取skill文件 ============
SKILLS_BASE = r"d:\popwave-skills\skills"

def read_skill_files(skill_name, files):
    parts = []
    for f in files:
        path = os.path.join(SKILLS_BASE, skill_name, f)
        with open(path, "r", encoding="utf-8") as fh:
            parts.append(fh.read())
    return "\n\n---\n\n".join(parts)

# ============ Write System Prompt (v7.1.0 - 新skill) ============
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

# ============ 精选设定库（≤1000字，力量体系+物种天赋）============
CURATED_SETTINGS = """# 精选设定库（write层精选注入，≤1000字）

> 来源：Phase3 L1-02力量体系 + L1-04物种与天赋
> 精选规则：ch001是开篇/战斗章，只注入战斗相关设定（力量体系+物种天赋）

## 种族特征

**半精灵**：拥有人类和精灵血统，特性包括夜视（黑暗中视物）、左手灵活（双持武器优势）。在贫民窟常被歧视。

## 力量体系基础

### 六大属性
| 属性 | 作用 | 普通人标准 | 超凡门槛 |
|------|------|----------|---------|
| 力量(STR) | 近战攻击/负重 | 10 | 20 |
| 敏捷(DEX) | 远程/潜行/开锁/攻击速度 | 10 | 20（质变） |
| 体质(CON) | 生命值/抗性/恢复 | 10 | 20（再生） |
| 智力(INT) | 法术/技能点/学识 | 10 | 20 |
| 感知(WIS) | 侦查/预判/意志 | 10 | 20 |
| 魅力(CHA) | 社交/术士施法 | 10 | 20 |

### 等级阶位
- **平民**：最基础职业，无特殊能力
- **一阶（1-10级职业者）**：刚觉醒，拥有基础职业能力
- **二阶（5-9级职业者）**：职业能力显著提升，超凡者分水岭
- **高阶（10-14级）**：作战能力成熟
- **传奇（15级以上）**：颠覆常规的力量

### 升级机制
- 战斗击杀获得"杀戮经验"
- 撬锁/拆陷阱/阅读获得"职业经验"
- 经验值自主分配提升职业等级
- 升级获得：生命值+技能点+属性点+专长点

## 主角初始数据（ch002）

【姓名：索伦】
【种族：半精灵】
【职业：平民LV1 / 盗贼LV1】
【属性：力量12 敏捷19 体质15 智力18 感知15 魅力16】
【生命值：12/12】
【状态：濒死虚弱】
【未分配经验：150】

注：敏捷19接近超凡门槛20点，是主角的核心优势。

## 薇薇安数据（ch027才揭示，ch001只用"瘦小女孩"）

8岁，属性异常高（魅力21天生术士资质），但ch001只表现为瘦弱女孩。
"""

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

    with open(PHASE15_PATH, "r", encoding="utf-8") as f:
        files["phase15"] = f.read()

    with open(PHASE2_PATH, "r", encoding="utf-8") as f:
        files["phase2"] = f.read()

    # Phase3 L1六件套（完整版，D组用）
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

    ch_path = os.path.join(CHAPTERS_DIR, "ch001.md")
    with open(ch_path, "r", encoding="utf-8") as f:
        files["ch001"] = f.read()

    return files


def build_common_constraints():
    """通用约束（所有组共用）"""
    return """# 任务

请按write skill全流程写本章（ch001）正文。

5步SOP：
- Step 1: 加载燃料
- Step 2: 章型+技法锁定
- Step 3: 写正文，2000-2500字，不准超过2500字
- Step 4: 篇幅硬限制检查+落盘
- Step 5: 交付面板

关键约束：
- **参照白描卡写**：白描卡是原文的压缩版
- **番茄快爽改造**：节奏更紧凑、爽感更密集、章末钩子更主动
- 系统面板用【】内联格式，禁止markdown代码块
- 对话引导词只用"道"
- 字数硬限制：2000-2500字
- 章末有钩子
- 不写思考过程/检查表——直接写正文+交付面板

直接输出正文+交付面板。
"""


def build_prompt_b(decon_files):
    """B组：新skill v7.1.0 + 无设定库"""
    return f"""{build_common_constraints()}

---

# 设定库精选注入

（本章无设定库精选注入——依赖剧情白描已消化的设定）

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


def build_prompt_c(decon_files):
    """C组：新skill v7.1.0 + 精选设定库（力量体系+物种天赋）"""
    return f"""{build_common_constraints()}

---

# 设定库精选注入（按章型精选：开篇/战斗章→力量体系+物种天赋）

{CURATED_SETTINGS}

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
    """D组：新skill v7.1.0 + 完整输入（含全文设定库）—— 测能否抑制负面影响"""
    return f"""{build_common_constraints()}

---

# 设定库（Phase3 L1六件套 - 完整版）

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


def run_test(group_name, prompt_builder, decon_files, system_prompt):
    """单组测试"""
    print(f"\n[{group_name}] 开始...")
    user_prompt = prompt_builder(decon_files)
    prompt_len = len(user_prompt)
    print(f"  Prompt长度: {prompt_len}字符")

    try:
        content, usage, elapsed = call_ds(
            system_prompt, user_prompt, max_tokens=8000, label=group_name
        )
        out_path = os.path.join(OUTPUT_DIR, f"r28-{group_name}-ch001.md")
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
    print("R28测试: 验证write skill v7.1.0优化效果")
    print("=" * 60)

    # 加载拆书产出
    print(f"\n[0] 加载拆书产出...")
    decon_files = load_decon_files()
    print(f"  Phase1.5剧情白描: {len(decon_files['phase15'])}字")
    print(f"  Phase2 L2+卷纲: {len(decon_files['phase2'])}字")
    print(f"  Phase3 L1六件套: {len(decon_files['phase3'])}字")
    print(f"  白描卡ch001: {len(decon_files['ch001'])}字")
    print(f"  精选设定库: {len(CURATED_SETTINGS)}字")

    # 复用R27-C作为A组
    print(f"\n[A-基准] 复用R27-C结果...")
    if os.path.exists(R27_C_PATH):
        shutil.copy(R27_C_PATH, os.path.join(OUTPUT_DIR, "r28-A-基准-ch001.md"))
        with open(R27_C_PATH, "r", encoding="utf-8") as f:
            a_content = f.read()
        print(f"  已复用! {len(a_content)}字")
    else:
        print(f"  R27-C不存在，A组跳过")

    # 定义B/C/D三组测试
    test_groups = [
        ("B-skill优化无设定", build_prompt_b, WRITE_SYSTEM_V71),
        ("C-精选设定库", build_prompt_c, WRITE_SYSTEM_V71),
        ("D-完整输入抑制", build_prompt_d, WRITE_SYSTEM_V71),
    ]

    # 并行跑3组
    print(f"\n[1] 并行跑3组AB测试...")
    results = {}

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {}
        for group_name, builder, sys_prompt in test_groups:
            future = executor.submit(run_test, group_name, builder, decon_files, sys_prompt)
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
    meta_path = os.path.join(OUTPUT_DIR, "r28-meta.json")
    meta_save = {}
    for k, v in results.items():
        meta_save[k] = {key: val for key, val in v.items() if key != "content"}
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta_save, f, ensure_ascii=False, indent=2)

    # 汇总
    print(f"\n{'='*60}")
    print("R28测试完成！")
    print(f"{'='*60}")
    print(f"\n{'组别':<22} {'输入字数':<10} {'产出字数':<10} {'耗时':<8} {'tokens':<10}")
    print("-" * 70)
    print(f"{'A-基准(R27-C复用)':<22} {'N/A':<10} {len(a_content):<10} {'N/A':<8} {'N/A':<10}")
    for group_name, _, _ in test_groups:
        val = results.get(group_name, {})
        if "error" in val:
            print(f"{group_name:<22} 失败: {val['error']}")
        else:
            tokens = val['usage'].get('total_tokens', 0)
            print(f"{group_name:<22} {val['prompt_length']:<10} {val['content_length']:<10} {val['elapsed']:<8} {tokens:<10}")

    print(f"\n输出目录: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
