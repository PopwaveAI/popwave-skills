#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
R44 v13.14.0全链路复测：验证三个skill边界修复
seed phase2（v13.14.0·前期成长路线+金手指≥3限制）→ world（v1.2.0·只做设定）→ plot（v3.1.0·接回剧情结构+无章锚点表）

输入：R44 phase1王道1·宗门公务员
输出：phase2-创意.md → world-骨架.md → plot-剧情白描.md
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
INPUTS_DIR = os.path.join(SCRIPT_DIR, "inputs_v13.14.0")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output_v13.14.0")

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

SEED_SYSTEM = read_skill_files("pop-fanqie-seed", ["SKILL.md", "steps/step2.md"])
WORLD_SYSTEM = read_skill_files("pop-fanqie-world", ["SKILL.md", "steps/step3.md", "steps/step4.md"])
PLOT_SYSTEM = read_skill_files("pop-fanqie-plot", ["SKILL.md", "steps/step2.md", "steps/step3.md"])

WANGDAO1 = """#### 王道1：宗门公务员：修仙界底层改革
- **一句话描述**：灵根废柴的陈渡，被踢到濒临倒闭的外门杂物科当科长。他没法修仙，但他会写KPI、会搞资源整合、会做绩效考核。他带着一群被各峰淘汰的杂役和废灵根，用凡人的管理学，对腐朽的宗门体制进行一场自上而下的"降维打击改革"。
- **画面**："师兄，这个月的灵石补贴怎么还没发？" "别急，我正在跟丹峰谈'百草订单'的返点。另外，下午执法堂要来查卫生，把那些发霉的蒲团都收起来。" ——陈渡推了推不存在的眼镜，手里拿着一份《杂物科第四季度业绩考核表》。
**创意类型**：阶级攀爬型 (靠管理才能打破修仙阶级)
**情绪基调**：荒诞轻喜剧 + 权谋博弈"""

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

def build_seed_prompt():
    return f"""# 任务

按seed Phase 2 SOP（v13.14.0），对以下选定创意进行结构化打磨，产出完整创意.md。

**v13.14.0核心改动**：①金手指限制≥3条 ②故事纲领核心三新增"前期成长路线"字段（3-4个成长阶段，每阶段有处境+目标+对手）

## 选定创意

{WANGDAO1}

## 产出要求

按step2完整执行2a-2f。重点：

### 金手指合成（v13.14.0）
- 创意×机制×限制
- **限制至少3条**——单条限制不够支撑100章张力

### 故事纲领核心一·什么样的世界
- 规则差异四层：力量体系层+差异层+日常层+主角层
- 力量体系必须明确（修仙境界/系统规则/...）

### 故事纲领核心三·什么样的主角（v13.14.0新增）
- 起点+拐点+终点三段完整
- ≥3级力量路径（对齐世界力量体系）
- 力量路径映射幕序列
- **前期成长路线**：3-4个成长阶段，每阶段有处境+目标+对手（world定第一卷章节预算和敌人梯度用）

### 自检清单（v13.14.0新增两项）
- 主角有前期成长路线吗？
- 金手指限制≥3条吗？

直接输出完整创意.md，不要写思考过程。
"""

def build_world_prompt(phase2_output):
    return f"""# 任务

按pop-fanqie-world v1.2.0的SOP，基于以下创意.md，执行world流程，产出骨架.md。

**v1.2.0核心改动**：world只做设定设计（力量体系/地图/势力/危机/第一卷设定范围），不做剧情结构设计（幕序列/高潮/悬念移到plot）。势力三问改为设定视角（控制什么资源/有什么弱点/和上层什么关系）。

## 输入：创意.md（seed v13.14.0产出）

{phase2_output}

## 执行要求

按world SOP完整执行Step 1-4：

### Step 1 · 加载底牌
从创意.md提取种子条款（创意/金手指机制+限制≥3条/行为引擎/主角轮廓/故事纲领三核心/前期成长路线）

### Step 2 · 从创意生长世界
- 2a. 力量体系：消费seed已明确的力量体系层，不自己发明
- 2b. 地图：从力量体系+行为引擎推导
- 2c. 势力：4层梯度。每层回答：①控制什么资源？②有什么弱点/裂缝？③和上层什么关系？（不回答"主角靠什么赢"——那是plot的活）
- 2d. 危机：四源+倒计时

### Step 3 · 第一卷设定范围（v1.2.0重定位·不是弧线设计）
- 3a. 设定范围：力量范围/地理范围/势力范围/危机范围/卷末设定边界
- 3b. 配角设计：只设计角色设定，不设计剧情角色

### Step 4 · 落盘骨架.md

## 红线
1. **world只做设定，不做剧情结构**——不产出幕序列弧线/高潮场景展开/悬念分层
2. 力量层级表必须消费seed已明确的力量体系
3. 势力三问是设定视角（资源/弱点/关系），不是剧情视角（主角靠什么赢）

直接输出完整骨架.md，不要写思考过程。
"""

def build_plot_prompt(phase2_output, world_output):
    return f"""# 任务

按pop-fanqie-plot v3.1.0的SOP，基于以下创意.md+骨架.md，执行plot流程，产出剧情白描.md。

**v3.1.0核心改动**：①接回剧情结构设计（幕序列/高潮/悬念）——从world剔除的内容plot接回 ②删除章锚点表 ③plot先设计剧情结构，再写叙事流白描

## 输入1：创意.md（seed v13.14.0产出）

{phase2_output}

## 输入2：骨架.md（world v1.2.0产出）

{world_output}

## 执行要求

按plot SOP完整执行Step 1-3：

### Step 1 · 加载骨架.md
从骨架.md提取：力量体系/地图/势力/危机/第一卷设定范围/配角

### Step 2 · 剧情结构设计+叙事流白描

#### 2a. 剧情结构设计（v3.1.0接回）
- 2a-1. 幕序列（3-4幕）：从骨架势力结构+危机倒计时+第一卷设定范围推导。每幕有功能位/对赌难度/弧线/碰撞势力/场景地标/章节预算/幕末钩子
- 2a-2. 核心高潮点（2-3个）：从骨架危机倒计时叠加节点推导。每个有低谷/高潮/变化
- 2a-3. 悬念分层：从骨架危机+金手指限制推导。每条有触发章/预计揭示章

#### 2b. 叙事流白描
- 2b-1. 叙事流写法（禁止提纲式）：每段有画面+情绪锚点
- 2b-2. 信息差/伏笔/钩子内联标注
- 2b-3. 推演流程：基于2a剧情结构+骨架设定，按幕分段写白描
- 2b-4. 白描质量自检

### Step 3 · 落盘剧情白描.md（v3.1.0删除章锚点表）
只产出剧情白描.md（含剧情结构+叙事流白描），不产出章锚点表。

## 红线
1. 必须加载骨架.md——禁止凭空编造世界
2. 剧情白描必须是叙事流，不是注水提纲
3. 剧情结构设计必须基于骨架设定——幕序列/高潮/悬念从骨架的势力/危机/设定范围推导
4. **不产出章锚点表**——v3.1.0已删除

## 注意
- 由于token限制（12000），白描可以只写前两幕的详细叙事流，后两幕给幕序列结构+关键场景概述即可
- 重点是验证plot能接回剧情结构设计，且基于骨架设定推导

直接输出剧情白描.md（剧情结构+叙事流白描），不要写思考过程。
"""

def main():
    os.makedirs(INPUTS_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("=" * 60)
    print(f"R44 v13.14.0全链路复测：三个skill边界修复验证")
    print(f"seed v13.14.0 → world v1.2.0 → plot v3.1.0")
    print("=" * 60)

    # ===== seed phase2 =====
    print(f"\n[seed phase2] 打磨创意.md（v13.14.0·前期成长路线+金手指≥3限制）...")
    seed_prompt = build_seed_prompt()
    try:
        seed_output, seed_usage, seed_elapsed = call_ds(SEED_SYSTEM, seed_prompt, max_tokens=8000)
        save_io("phase2-创意", SEED_SYSTEM, seed_prompt, seed_output, seed_usage, seed_elapsed)
    except Exception as e:
        print(f"  失败: {e}")
        sys.exit(1)

    # ===== world =====
    print(f"\n[world] 从创意生长世界（v1.2.0·只做设定不做剧情）...")
    world_prompt = build_world_prompt(seed_output)
    try:
        world_output, world_usage, world_elapsed = call_ds(WORLD_SYSTEM, world_prompt, max_tokens=12000)
        save_io("world-骨架", WORLD_SYSTEM, world_prompt, world_output, world_usage, world_elapsed)
    except Exception as e:
        print(f"  失败: {e}")
        sys.exit(1)

    # ===== plot =====
    print(f"\n[plot] 剧情结构设计+叙事流白描（v3.1.0·接回剧情结构+无章锚点表）...")
    plot_prompt = build_plot_prompt(seed_output, world_output)
    try:
        plot_output, plot_usage, plot_elapsed = call_ds(PLOT_SYSTEM, plot_prompt, max_tokens=12000)
        save_io("plot-剧情白描", PLOT_SYSTEM, plot_prompt, plot_output, plot_usage, plot_elapsed)
    except Exception as e:
        print(f"  失败: {e}")
        sys.exit(1)

    print(f"\n{'='*60}")
    print("R44 v13.14.0全链路复测完成！")
    print(f"{'='*60}")
    print(f"\n产出目录: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
