#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
R44 v13.13.0复测：验证三核心加力量体系层后的seed→world落地
1. 重跑phase2（v13.13.0新SOP，产出含力量体系层的创意.md）
2. 跑world（v1.1.0，消费seed已明确的力量体系）
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
INPUTS_DIR = os.path.join(SCRIPT_DIR, "inputs_v13.13.0")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output_v13.13.0")

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

# 加载最新skill文件（v13.13.0 seed + v1.1.0 world）
SEED_SYSTEM = read_skill_files("pop-fanqie-seed", ["SKILL.md", "steps/step2.md"])
WORLD_SYSTEM = read_skill_files("pop-fanqie-world", ["SKILL.md", "steps/step3.md", "steps/step4.md"])

# 王道1选定创意（从R44 phase1-发散.md提取）
WANGDAO1 = """#### 王道1：宗门公务员：修仙界底层改革
- **一句话描述**：灵根废柴的陈渡，被踢到濒临倒闭的外门杂物科当科长。他没法修仙，但他会写KPI、会搞资源整合、会做绩效考核。他带着一群被各峰淘汰的杂役和废灵根，用凡人的管理学，对腐朽的宗门体制进行一场自上而下的"降维打击改革"。
- **画面**："师兄，这个月的灵石补贴怎么还没发？" "别急，我正在跟丹峰谈'百草订单'的返点。另外，下午执法堂要来查卫生，把那些发霉的蒲团都收起来。" ——陈渡推了推不存在的眼镜，手里拿着一份《杂物科第四季度业绩考核表》。
- **为什么有意思**：别人修仙靠天赋，主角修仙靠《管理学原理》。看凡人如何用职场智慧在修仙宗门里搞民营化，把占着茅坑不拉屎的长老们逼得主动内卷。爽点在于"我有脑子，你们没有"。
- **市场定位**：借鉴"修仙+种田/基建"的宗门经营卖点，差异化在"管理改革"带来的权谋博弈和阶级博弈，而非纯粹的种田。
**创意类型**：阶级攀爬型 (靠管理才能打破修仙阶级)
**情绪基调**：荒诞轻喜剧 + 权谋博弈
**立项评估**：
- **世界**：一个制度僵化、长老山头林立、底层苦不堪言的修仙宗门。隐藏规则是"人力/人心也是一种修仙资源"，可生长设定是陈渡的管理模式如何从杂物科扩展到整个宗门，甚至改变修仙界的格局。
- **舞台**：宗门财政赤字、高层斗争内耗、外敌威胁下的生存危机。驱动剧情的是"如何用10%的资源撬动90%的利益"，压力源来自制度既得利益者的反扑和层出不穷的管理难题。
- **主角**：陈渡，特殊性在于"超凡的管理才能"和"跳出棋盘看问题"的凡人视角。成长路径不是升级灵根，而是扩大管理地盘、收拢人才、建立自己的"改革派"势力。

【选定创意】：王道1：宗门公务员：修仙界底层改革"""

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

def save_input_output(phase_name, system_prompt, user_prompt, output_content, usage, elapsed):
    input_content = f"# SYSTEM PROMPT\n\n{system_prompt}\n\n---\n\n# USER PROMPT\n\n{user_prompt}"
    input_path = os.path.join(INPUTS_DIR, f"{phase_name}_input.md")
    with open(input_path, "w", encoding="utf-8") as f:
        f.write(input_content)
    output_path = os.path.join(OUTPUT_DIR, f"{phase_name}.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(output_content)
    print(f"  [{phase_name}] 完成! {elapsed:.1f}s | {len(output_content)}字符 | tokens:{usage.get('total_tokens', 0)}")
    print(f"    input  → {input_path}")
    print(f"    output → {output_path}")
    return output_path

# ============ 段2: 重跑phase2（v13.13.0新SOP）============
def build_phase2_prompt():
    return f"""# 任务

按seed Phase 2 SOP（v13.13.0），对以下选定的创意进行结构化打磨，产出完整的创意.md。

**v13.13.0核心改动**：三核心"什么样的世界"必须包含"力量体系层"——明确世界的力量体系是什么。"什么样的主角"力量路径必须对齐世界力量体系。

## Phase 1 发散产出（含选定创意）

{WANGDAO1}

## 产出要求

按step2的2a-2f完整执行。

### 2e. 故事纲领（三核心+营销层·≤1000字）

#### 核心一：什么样的世界（3-4句）

> world推导锚点：这个世界和现实的差异是什么？**世界的力量体系是什么**？这个差异如何影响日常和主角？

**质量标准——规则差异四层（缺项=走形式=重写）**：
- ✓ **力量体系层**：这个世界的力量体系是什么？（**必须明确**——修仙境界（炼气→筑基→金丹→元婴）/ 系统规则 / 规则怪谈 / 异能等级 / 职业树。这一层是world推导力量层级的唯一基底）
- ✓ **差异层**：这个世界和现实世界有什么不同？（1条核心差异——具体的运转法则）
- ✓ **日常层**：这个差异如何影响普通人的日常？（普通人怎么活？）
- ✓ **主角层**：这个差异如何影响主角的生存？（主角在这个差异里处于什么位置？）

**注意**：这个创意是修仙宗门题材，力量体系应该是修仙境界（炼气→筑基→金丹→元婴），修为决定权力。不能把"管理权限层级"当成力量体系——那是主角的金手指优势，不是世界的力量体系。

#### 核心二：什么样的舞台·世界危机（3-4句）
- 1个全书危机源头
- ≥3层敌人梯度（每层有具体对象）
- ≥1个压力源/倒计时

#### 核心三：什么样的主角（4-5句）

> **硬约束：主角的力量路径必须在核心一"力量体系层"内。** 金手指可以是加速器/特殊视角/漏洞利用，但不能是另一个维度的东西——修仙世界的主角力量路径是修仙境界（金手指加速修炼/特殊功法/系统辅助），不能是"管理权限层级"。

- 起点+拐点+终点三段完整
- ≥3级力量路径（每级有具体能力描述+对应场景）
- 力量路径直接映射幕序列
- **力量路径对齐世界力量体系**（每级力量路径=力量体系中的一个层级或跨层级）

#### 营销层
- 最大钩子（≤20字）
- 即时兑现感（2-3句）

### 2f. 落盘创意.md
按标准格式产出完整创意.md（一句话简介/创意/金手指/行为引擎/主角轮廓/番茄简介/故事纲领）。

### 番茄简介硬约束
- 至少3个连环创意点
- 至少1句情绪锚点台词（荒诞轻喜剧用荒谬的台词）
- 1个认知反转收尾
- 必须第一人称
- 情绪基调一致性

### 故事纲领自检清单（逐项检查，缺项=重写）
- 世界有力量体系层吗？
- 世界有差异层吗？
- 世界有日常层吗？
- 世界有主角层吗？
- 舞台有危机源头吗？
- 舞台有敌人梯度吗？（≥3层）
- 舞台有压力源/倒计时吗？
- 主角有三段弧线吗？
- 主角有力量路径吗？（≥3级）
- 力量路径映射幕序列吗？
- **力量路径对齐世界力量体系吗？**（每级力量路径=力量体系中的一个层级或跨层级）

直接输出完整创意.md，不要写思考过程。
"""

# ============ world: 跑world流程 ============
def build_world_prompt(phase2_output):
    return f"""# 任务

按pop-fanqie-world v1.1.0的完整SOP，基于以下创意.md，执行world流程，产出骨架.md。

**v1.1.0核心改动**：world不再自己发明力量体系，消费seed v13.13.0+已明确的力量体系层。力量层级表必须和seed力量体系对齐。

## 输入1：创意.md（seed Phase 2产出·v13.13.0）

{phase2_output}

## 执行要求

按world SOP完整执行Step 1-4：

### Step 1 · 加载三件底牌
- 从创意.md提取种子条款（创意/金手指机制+限制/行为引擎/主角轮廓/故事纲领三核心）
- **特别提取力量体系层**——创意.md"什么样的世界"明确的力量体系是什么
- 市场校准和参考书DNA标注缺失

### Step 2 · 从创意生长世界

#### 2a. 三源合流设计力量体系
**v1.1.0核心：直接消费seed已明确的力量体系层，不自己发明。**

- 创意.md明确的力量体系是什么？（修仙境界/系统规则/...）
- 直接展开为力量层级表（5-7个层级），每层基于seed力量体系展开
- **硬约束**：力量层级表必须和seed力量体系对齐。seed说力量体系是修仙境界→world展开炼气→筑基→金丹→元婴的层级表，不能展开成别的

力量层级表每个层级必须有：
- 名称（贴合本项目世界观，基于seed力量体系）
- 这个世界长什么样（MMO式等级区描述）
- 主角在这个层级面对什么
- 升级触发条件
- 参考源

#### 2b. 从力量体系+行为引擎生长地图
#### 2c. 从力量体系+地图生长势力
每层势力必须回答：1.为什么主角必须和这个势力冲突？2.主角靠什么赢？3.赢了得到什么？

#### 2d. 危机体系设计（四源）
- 世界固有危险
- 力量体系内压
- 金手指反噬
- 赛道惯例压力

### Step 3 · 第一卷弧线设计
- 第一卷终点
- 幕序列（3-4幕，每幕=一个"对赌难度升级"的弧段）
- 核心高潮点（2-3个）
- 悬念分层
- 配角设计

### Step 4 · 落盘骨架.md
按标准格式产出完整骨架.md。

## 红线
1. **力量层级表必须消费seed已明确的力量体系，不自己发明**——seed说修仙境界就展开修仙境界，不能展开成管理权限层级
2. 每项世界要素必须回溯创意.md条款
3. 第一卷敌人必须4层梯度——每层至少1个具名反派
4. 力量体系是骨架，地图/势力/危机是血肉——血肉必须塞入骨架

直接输出完整骨架.md，不要写思考过程。
"""

def main():
    os.makedirs(INPUTS_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("=" * 60)
    print(f"R44 v13.13.0复测：三核心加力量体系层→world落地验证")
    print(f"创意：王道1·宗门公务员（阶级攀爬型）")
    print("=" * 60)

    # ===== 段2: 重跑phase2 =====
    print(f"\n[段2] 重跑phase2（v13.13.0新SOP·含力量体系层）...")
    p2_prompt = build_phase2_prompt()
    try:
        p2_output, p2_usage, p2_elapsed = call_ds(SEED_SYSTEM, p2_prompt, max_tokens=8000)
        save_input_output("phase2-创意", SEED_SYSTEM, p2_prompt, p2_output, p2_usage, p2_elapsed)
    except Exception as e:
        print(f"  [段2] 失败: {e}")
        sys.exit(1)

    # ===== world: 跑world流程 =====
    print(f"\n[world] 跑world流程（v1.1.0·消费seed力量体系）...")
    world_prompt = build_world_prompt(p2_output)
    try:
        world_output, world_usage, world_elapsed = call_ds(WORLD_SYSTEM, world_prompt, max_tokens=12000)
        save_input_output("world-骨架", WORLD_SYSTEM, world_prompt, world_output, world_usage, world_elapsed)
    except Exception as e:
        print(f"  [world] 失败: {e}")
        sys.exit(1)

    print(f"\n{'='*60}")
    print("R44 v13.13.0复测完成！")
    print(f"{'='*60}")
    print(f"\n产出目录: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
