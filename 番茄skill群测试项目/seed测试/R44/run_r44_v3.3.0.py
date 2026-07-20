#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
R44 v3.3.0复测：验证world全书设定+plot四层结构
world v1.3.0（全书设定3-8卷）→ plot v3.3.0（本卷设定快照→分支线≥6条→分幕→白描）

seed v13.14.0未改动，复用已有phase2-创意.md
输出：world-骨架.md → plot-剧情白描.md
"""

import os
import sys
import json
import time
import requests

DS_API_KEY = "sk-5a3654e4aa2e4eefa08abe3d0e0231f5"
DS_BASE_URL = "https://api.deepseek.com/v1"
DS_MODEL = "deepseek-v4-flash"
PROXIES = {"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"}
TEMPERATURE = 0.85
TIMEOUT = 600

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUTS_DIR = os.path.join(SCRIPT_DIR, "inputs_v3.3.0")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output_v3.3.0")
PREV_PHASE2 = os.path.join(SCRIPT_DIR, "output_v13.14.0", "phase2-创意.md")

SKILLS_BASE = r"d:\popwave-skills\skills"

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def read_skill_files(skill_name, files):
    parts = []
    for f in files:
        path = os.path.join(SKILLS_BASE, skill_name, f)
        parts.append(read_file(path))
    return "\n\n---\n\n".join(parts)

WORLD_SYSTEM = read_skill_files("pop-fanqie-world", ["SKILL.md", "steps/step3.md", "steps/step4.md"])
PLOT_SYSTEM = read_skill_files("pop-fanqie-plot", ["SKILL.md", "steps/step2.md", "steps/step3.md"])

def call_ds(system_prompt, user_prompt, max_tokens=12000):
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

def save_io(phase_name, system_prompt, user_prompt, output_content, usage, elapsed):
    input_content = f"# SYSTEM PROMPT\n\n{system_prompt}\n\n---\n\n# USER PROMPT\n\n{user_prompt}"
    input_path = os.path.join(INPUTS_DIR, f"{phase_name}_input.md")
    with open(input_path, "w", encoding="utf-8") as f:
        f.write(input_content)
    output_path = os.path.join(OUTPUT_DIR, f"{phase_name}.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(output_content)
    print(f"  [{phase_name}] 完成! {elapsed:.1f}s | {len(output_content)}字符 | tokens:{usage.get('total_tokens', 0)}")
    print(f"    output → {output_path}")
    return output_path

def build_world_prompt(phase2_output):
    return f"""# 任务

按pop-fanqie-world v1.3.0的SOP，基于以下创意.md，执行world流程，产出骨架.md。

**v1.3.0核心改动**：world产出**全书设定**（3-8卷200万字级），不是仅第一卷设定。力量体系5-7层完整展开、地图所有区域、势力4层全具名、主要危机终极+阶段性，每项标注各卷覆盖范围。

**幕/卷统一格式**：幕=8~12章起承转合单元，卷=40~60章（4~5幕）。

## 输入：创意.md（seed v13.14.0产出）

{phase2_output}

## 执行要求

按world SOP完整执行Step 1-4：

### Step 1 · 加载底牌
从创意.md提取种子条款

### Step 2 · 从创意生长世界
- 2a. 力量体系：消费seed已明确的力量体系层，全书5-7层完整展开，每层标注预计展开卷
- 2b. 地图：所有区域，每个标注预计进入卷
- 2c. 势力：4层全具名，每层标注预计碰撞卷。每层回答：①控制什么资源？②有什么弱点？③和上层什么关系？
- 2d. 危机：1条终极危机+2-3条阶段性危机，每条标注预计爆发卷

### Step 3 · 全书设定（v1.3.0·不是第一卷设定范围）
- 3a. 全书设定总览：力量体系全书展开表/地图全书展开表/势力全书展开表/危机全书展开表
- 3b. 全书配角设计：每个标注预计出场卷
- 3c. 各卷设定切片预览：给plot的导航索引（第一卷/第二卷/...各取哪些设定）

### Step 4 · 落盘骨架.md

## 红线
1. 力量体系5-7层完整展开，每层标注预计展开卷
2. 势力4层全具名，每层标注预计碰撞卷
3. 危机1条终极+2-3条阶段性，每条标注预计爆发卷
4. 全书设定每项标注各卷覆盖范围
5. world只做设定，不做剧情结构

直接输出完整骨架.md，不要写思考过程。
"""

def build_plot_prompt(phase2_output, world_output):
    return f"""# 任务

按pop-fanqie-plot v3.3.0的SOP，基于以下创意.md+骨架.md，执行plot流程，产出第一卷剧情白描.md。

**v3.3.0核心改动**：①统一幕/卷格式（幕8~12章起承转合/卷40~60章4~5幕）②重构step2为四层：2a本卷设定快照→2b分支剧情线≥6条→2c分幕设计→2d叙事流白描

**四层结构**：
- 2a. 本卷设定快照：从骨架全书设定圈出第一卷范围+充实（力量范围主角起终点快照/卷级敌人/登场势力角色/涉及地图填充势力矛盾/整卷主要矛盾）
- 2b. 分支剧情线≥6条：主线1~2+支线3~4+暗线1~2，每条标注起止/涉及势力地图/和主线关系
- 2c. 分幕设计：卷40~60章/幕8~12章/4~5幕，每幕起承转合+推进≥2条分支线
- 2d. 叙事流白描：每幕内部多线交织推进

## 输入1：创意.md（seed v13.14.0产出）

{phase2_output}

## 输入2：骨架.md（world v1.3.0产出·全书设定）

{world_output}

## 执行要求

按plot SOP完整执行Step 1-3，**只写第一卷**：

### Step 1 · 加载骨架.md
从骨架.md全书设定中准备切片

### Step 2 · 本卷设定快照+分支剧情线+分幕设计+叙事流白描

#### 2a. 本卷设定快照（第一卷）
- 力量体系范围：主角起点快照→终点快照 + 卷级敌人的力量范围
- 登场势力/角色：从骨架4层中取第一卷涉及的层级
- 涉及地图：从骨架所有区域中取第一卷涉及的2-3个，**填充势力和彼此矛盾**（不是空地图）
- 整卷主要矛盾/主要剧情走向

#### 2b. 分支剧情线（≥6条）
- 主线1~2条 + 支线3~4条 + 暗线1~2条
- 每条标注：起止/涉及势力/涉及地图/和主线关系（支线）/预计揭示卷（暗线）

#### 2c. 分幕设计（第一卷40~60章，4~5幕）
- 每幕8~12章，完整起承转合
- 每幕推进≥2条分支线
- 对赌难度逐幕升级

#### 2d. 叙事流白描
- 按幕分段写白描，每幕内部多线交织
- 每段有画面+情绪锚点
- 标注信息差/伏笔/钩子

### Step 3 · 落盘剧情白描.md

## 红线
1. 必须加载骨架.md
2. 剧情白描必须是叙事流，不是注水提纲
3. 分支剧情线≥6条（主线1~2+支线3~4+暗线1~2）
4. 地图要填充势力和彼此矛盾，不是空地图
5. 幕/卷格式统一（卷40~60章4~5幕，幕8~12章起承转合）
6. 本卷设定快照从骨架全书设定圈出，不能自己发明设定

## 注意
- 由于token限制，白描可以只写前两幕的详细叙事流，后续幕给分幕结构+关键场景概述
- 重点是验证：①world产出全书设定 ②plot本卷设定快照充实地图 ③≥6条分支线 ④分幕基于分支线串起

直接输出第一卷剧情白描.md（本卷设定快照+分支剧情线+分幕设计+叙事流白描），不要写思考过程。
"""

def main():
    os.makedirs(INPUTS_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("=" * 60)
    print(f"R44 v3.3.0复测：world全书设定+plot四层结构验证")
    print(f"world v1.3.0 → plot v3.3.0（复用seed v13.14.0 phase2）")
    print("=" * 60)

    # ===== 复用seed phase2 =====
    print(f"\n[seed phase2] 复用v13.14.0产出...")
    if not os.path.exists(PREV_PHASE2):
        print(f"  失败: {PREV_PHASE2} 不存在")
        sys.exit(1)
    phase2_output = read_file(PREV_PHASE2)
    print(f"  复用完成: {len(phase2_output)}字符")

    # ===== world v1.3.0 =====
    print(f"\n[world v1.3.0] 产出全书设定（3-8卷200万字级）...")
    world_prompt = build_world_prompt(phase2_output)
    try:
        world_output, world_usage, world_elapsed = call_ds(WORLD_SYSTEM, world_prompt, max_tokens=12000)
        save_io("world-骨架", WORLD_SYSTEM, world_prompt, world_output, world_usage, world_elapsed)
    except Exception as e:
        print(f"  失败: {e}")
        sys.exit(1)

    # ===== plot v3.3.0 =====
    print(f"\n[plot v3.3.0] 本卷设定快照+分支线≥6条+分幕+白描（四层结构）...")
    plot_prompt = build_plot_prompt(phase2_output, world_output)
    try:
        plot_output, plot_usage, plot_elapsed = call_ds(PLOT_SYSTEM, plot_prompt, max_tokens=16000)
        save_io("plot-剧情白描", PLOT_SYSTEM, plot_prompt, plot_output, plot_usage, plot_elapsed)
    except Exception as e:
        print(f"  失败: {e}")
        sys.exit(1)

    print(f"\n{'='*60}")
    print("R44 v3.3.0复测完成！")
    print(f"{'='*60}")
    print(f"\n产出目录: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
