#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
R29测试: C方案（精选设定库）× 10章串联
每章输入包含上一章正文用于钩子回收
验证10章连续性+OOC检测
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

DECON_BASE = r"d:\popwave-skills\workspace\深渊主宰-瘦身白描测试"
PHASE15_PATH = os.path.join(DECON_BASE, "下游产出", "Phase1.5-全书剧情白描.md")
PHASE2_PATH = os.path.join(DECON_BASE, "下游产出", "Phase2-L2单元卡+卷纲+叙事技法.md")
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

# ============ 精选设定库（≤1000字）============
CURATED_SETTINGS = """# 精选设定库（write层精选注入，≤1000字）

> 来源：Phase3 L1-02力量体系 + L1-04物种与天赋
> 精选规则：开篇/战斗章→力量体系+物种天赋

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
- **二阶（5-9级职业者）**：超凡者分水岭
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

注：敏捷19接近超凡门槛20点，是主角核心优势。

## 薇薇安数据（ch027才揭示，ch001只表现为瘦弱女孩）

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
    files = {}
    with open(PHASE15_PATH, "r", encoding="utf-8") as f:
        files["phase15"] = f.read()
    with open(PHASE2_PATH, "r", encoding="utf-8") as f:
        files["phase2"] = f.read()

    chapters = {}
    for i in range(1, 11):
        ch_num = f"ch{i:03d}"
        ch_path = os.path.join(CHAPTERS_DIR, f"{ch_num}.md")
        if os.path.exists(ch_path):
            with open(ch_path, "r", encoding="utf-8") as f:
                chapters[ch_num] = f.read()
    files["chapters"] = chapters

    return files


def build_common_constraints(ch_num, prev_chapter):
    """通用约束"""
    if prev_chapter:
        prev_hint = """
- **如非第一章，必须回收前章钩子**——本章前300字必须回收前章章末钩子
- 前章正文已注入下方，用于回收钩子
"""
    else:
        prev_hint = """
- 第一章使用黄金开篇：前3句扔炸弹，300字内完成冲突+主角+金手指+钩子
"""

    return f"""# 任务

请按write skill全流程写本章（{ch_num}）正文。

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
{prev_hint}
- 不写思考过程/检查表——直接写正文+交付面板

直接输出正文+交付面板。
"""


def build_prompt_c(decon_files, ch_num, prev_chapter):
    """C方案：新skill v7.1.0 + 精选设定库"""
    chapter_card = decon_files["chapters"].get(ch_num, "")
    prompt = f"""{build_common_constraints(ch_num, prev_chapter)}

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

# 本章白描卡（{ch_num}）

{chapter_card}
"""
    if prev_chapter:
        prompt += f"\n\n---\n\n# 前一章正文（用于回收钩子）\n\n{prev_chapter}\n"
    return prompt


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("=" * 60)
    print("R29测试: C方案（精选设定库）× 10章串联")
    print("=" * 60)

    print(f"\n[0] 加载拆书产出...")
    decon_files = load_decon_files()
    print(f"  Phase1.5剧情白描: {len(decon_files['phase15'])}字")
    print(f"  Phase2 L2+卷纲: {len(decon_files['phase2'])}字")
    print(f"  白描卡: {len(decon_files['chapters'])}章")
    print(f"  精选设定库: {len(CURATED_SETTINGS)}字")

    # 串行跑10章
    print(f"\n[1] 串行跑ch01-ch10...")
    results = []
    prev_chapter = None

    for ch_idx in range(1, MAX_CHAPTERS + 1):
        ch_num = f"ch{ch_idx:03d}"

        if ch_num not in decon_files["chapters"]:
            print(f"  [{ch_idx}/10] {ch_num} 白描卡不存在，跳过")
            continue

        user_prompt = build_prompt_c(decon_files, ch_num, prev_chapter)
        prompt_len = len(user_prompt)
        print(f"  [{ch_idx}/10] {ch_num} 调用DeepSeek... (prompt: {prompt_len}字符)")

        try:
            content, usage, elapsed = call_ds(
                WRITE_SYSTEM_V71, user_prompt, max_tokens=8000, label=f"R29_{ch_num}"
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
    print("R29测试完成！")
    print(f"{'='*60}")
    print(f"\n{'章号':<10} {'输入字数':<10} {'产出字数':<10} {'耗时':<8} {'tokens':<10}")
    print("-" * 60)
    for r in results:
        if "error" in r:
            print(f"{r.get('ch_num','?'):<10} 失败: {r['error']}")
        else:
            print(f"{r['ch_num']:<10} {r['prompt_length']:<10} {r['content_length']:<10} {r['elapsed']:<8} {r['tokens']:<10}")

    # 保存meta
    meta_path = os.path.join(OUTPUT_DIR, "r29-meta.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n输出目录: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
