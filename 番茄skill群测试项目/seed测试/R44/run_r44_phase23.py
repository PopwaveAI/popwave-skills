#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
R44 seed测试 Phase2+Phase3：用王道1（宗门公务员）走完seed后续流程
验证v13.12.0创意类型多样化修复后，阶级攀爬型创意的故事纲领+首章质量

跳过段1发散（已由R44 phase1完成），直接用王道1作为选定创意，走段2（打磨→创意.md）+段3（首章）
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
INPUTS_DIR = os.path.join(SCRIPT_DIR, "inputs")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")

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

PHASE2_SYSTEM = read_skill_files("pop-fanqie-seed", ["SKILL.md", "steps/step2.md"])
PHASE3_SYSTEM = read_skill_files("pop-fanqie-seed", ["SKILL.md", "steps/step3.md"])

# ============ 王道1选定创意（从R44 phase1-发散.md提取）============
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

# ============ 段2: 打磨 ============
def build_phase2_prompt():
    return f"""# 任务

按seed Phase 2 SOP，对以下选定的创意进行结构化打磨，产出完整的创意.md。

## Phase 1 发散产出（含选定创意）

{WANGDAO1}

## 产出要求

按step2的2a-2f完整执行：

### 2a. 行为引擎检查
检查选定创意是否已有行为引擎（主角每章在做一件具体的事）。没有则用行为框架碰撞补上。

### 2b. 合成金手指
金手指 = 创意 × 机制 × 限制。三要素齐全，禁止只加限制不加代价。

### 2c. 四眼法验证
画面眼/限制眼/场景眼/引擎眼，四项全过才放行。

### 2e. 故事纲领（三核心+营销层·≤1000字）

> 故事纲领是world的核心输入。world拿到三核心后能直接推导设定。金手指不再是独立维度——它是主角特殊性的一部分，融入"主角"核心。
> **故事纲领不是创意摘要，是world的设定蓝图。每项必须给足结构元素，world才能推导。走形式=废纲领。**

#### 核心一：什么样的世界（2-3句）

world推导锚点：这个世界和现实的差异是什么？这个差异如何影响日常和主角？

**质量标准（缺项=走形式=重写）**——规则差异三层：
- 差异层：这个世界和现实世界有什么不同？（1条核心差异——具体的运转法则）
- 日常层：这个差异如何影响普通人的日常？（普通人怎么活？——决定世界真实感，world能从中推导出地图/经济/社会结构）
- 主角层：这个差异如何影响主角的生存？（主角在这个差异里处于什么位置？——和核心三"什么样的主角"衔接）

#### 核心二：什么样的舞台·世界危机（3-4句）

舞台 = 世界危机。危机驱动剧情持续运转100章——没有危机就没有故事。

**质量标准（缺项=走形式=重写）**：
- 1个全书危机源头（具体的、有来源的威胁）
- ≥3层敌人梯度（从底层到顶层，每层有具体对象）
- ≥1个压力源/倒计时（驱动主角不能停下来的压力）

#### 核心三：什么样的主角（4-5句）

主角特殊性 = 金手指 + 成长路径。金手指是主角特殊性的一部分，不是独立维度。

**质量标准（缺项=走形式=重写）**：
- 起点+拐点+终点三段完整（具体的状态转变）
- ≥3级力量路径（每级有具体能力描述+对应场景）
- 力量路径直接映射幕序列（每级力量路径=一幕）

#### 营销层（读者消费，非world输入）
- 最大钩子（≤20字）：路人翻三页被什么抓住
- 即时兑现感（2-3句）：前5章如何让读者感受到"已经在路上了"

### 2f. 落盘创意.md
按以下格式产出完整创意.md：

```markdown
# 创意名

## 一句话简介
（一句话说清这个创意是什么——主角是谁，在做什么，要做什么）

## 创意
（一句话创意——一个具体行为×一个反差场景）

## 创意来源
（用户选定的方向 + Phase 2打磨过程）

## 金手指
- 创意：（一句话）
- 机制：（一句话）
- 限制：（一句话）
- 合成：（创意×机制×限制的完整表述）

## 行为引擎
（主角每章在做什么具体行为）

## 轻量主角轮廓
- 名字：
- 身份：（一句话职业/社会角色）
- 核心动机：（一句话）
- 记忆点：（一句话）

## 番茄简介
（150-300字，第一人称散文体，带对话，带情绪弧线，带钩子。不是描述创意，是在讲创意的故事）

## 十、故事纲领（三核心+营销层·≤1000字）

> world的核心输入。三核心每项必须通过自检清单。金手指融入主角核心，不独立。走形式=废纲领。

### 什么样的世界
（2-3句：世界质感 + world可生长的设定方向/隐藏规则）

### 什么样的舞台·世界危机
（2-3句：全书危机压迫感 + world可推导的敌人梯度/压力源/倒计时）

### 什么样的主角
- **起点**：（初始状态/困境 + 初始能力）
- **拐点**：（什么事件迫使改变 + 特殊性/金手指觉醒）
- **终点**：（最终变成什么 + 特殊性成熟）
- **力量路径**：（从什么能力→到什么能力，world推导幕序列用）

### 最大钩子
（≤20字：路人翻三页被什么抓住）

### 即时兑现感
（2-3句：前5章如何让读者感受到"已经在路上了"）
```

### 番茄简介硬约束
- 至少3个连环创意点
- 至少1句情绪锚点台词——台词情绪基调必须匹配创意的情绪基调（荒诞轻喜剧用荒谬的台词，权谋博弈用冷的台词）。不是所有创意都用荒谬台词
- 1个认知反转收尾
- 禁止设定说明书式写法
- 必须第一人称
- 情绪基调一致性：简介的情绪基调必须和step1选创意时标注的一致

### 故事纲领硬约束
- 三核心+营销层加起来≤1000字
- 三核心（世界/舞台/主角）每项必须给出world推导锚点——world拿到后能直接推导设定
- 金手指融入"主角"核心，不再独立成维度
- 每项必须给出具体答案——不是"主角会成长"这种废话
- 走形式=废纲领——只写标签不写具体对象/场景的，必须重写

### 故事纲领自检清单（逐项检查，缺项=重写）
- 世界有差异层吗？（1条核心差异——和现实不同的具体运转法则）
- 世界有日常层吗？（这个差异如何影响普通人日常）
- 世界有主角层吗？（这个差异如何影响主角生存）
- 舞台有危机源头吗？（1个具体的、有来源的威胁）
- 舞台有敌人梯度吗？（≥3层，每层有具体对象）
- 舞台有压力源/倒计时吗？（≥1个驱动主角不能停的压力）
- 主角有三段弧线吗？（起点+拐点+终点完整）
- 主角有力量路径吗？（≥3级，每级有具体能力+场景）
- 力量路径映射幕序列吗？（每级力量路径=一幕）

直接输出完整创意.md，不要写思考过程。
"""

# ============ 段3: 首章 ============
def build_phase3_prompt(phase2_output):
    return f"""# 任务

按seed Phase 3 SOP，基于以下创意.md，写黄金首章ch001。

## 创意.md

{phase2_output}

## 产出要求

按step3的3a-3f完整执行：

### 3b. 黄金开篇法则
1. 前3句扔炸弹——第一句话就制造冲突/悬念/反差，禁止铺垫环境/背景/天气
2. 300字内完成4件事——冲突爆发+主角出场+金手指激活+章末钩子
3. 第一章必须激活金手指
4. 第一章必须有1个爽感触发
5. 章末必须有钩子
6. 必须有1个"生活化场景×金手指"的反差画面

### 3c. 首章结构（7节拍）
| 节拍 | 内容 | 字数参考 |
|------|------|---------|
| 1. 开场炸弹 | 第一句话制造冲突/悬念/反差 | 50字 |
| 2. 冲突爆发 | 主角面对的具体威胁/困境 | 300字 |
| 3. 金手指激活 | 金手指第一次展现 | 400字 |
| 4. 首次应用 | 主角用金手指应对冲突——反差画面 | 500字 |
| 5. 爽感爆发 | 金手指带来的反转/突破 | 400字 |
| 6. 危机暗示 | 暗示更大的威胁 | 300字 |
| 7. 章末钩子 | 让读者想看第二章的悬念 | 150字 |

总字数：2000-2500字，不准超过2500字

### 3e. 爽感闭环（必须）
触发→爆发→后果，三段缺一=废章

### 3f. 落盘格式
```markdown
# （10字以上章名，有噱头/反差/创意点）

[2000-2500字正文]

---

## 交付面板

| 字段 | 值 |
|------|-----|
| 章号 | ch001 |
| 章名 | （章名+字数） |
| 章型 | opening_shift（黄金开篇） |
| 字数 | XXXX字 |
| 核心事件 | （3-5句） |
| 反差画面 | （生活化场景×金手指的具体画面） |
| 爽感闭环 | （触发→爆发→后果） |
| 章末钩子 | （让读者想看第二章的悬念） |
| 笔触状态 | trial模式 |
```

### 笔触状态
trial模式（无DNA）。基础风格：简洁短句+动作驱动+对话推进。不内置系统面板格式（除非创意.md金手指明确需要面板）。

### 注意
- 这个创意是阶级攀爬型——主角生在修仙世界里，不是发现隐藏世界。开篇不要写"发现"，要写"要在世界里往上爬"
- 情绪基调是荒诞轻喜剧+权谋博弈——首章要有荒诞感但也要有权谋张力

直接输出ch001.md（正文+交付面板），不要写思考过程。
"""

def main():
    os.makedirs(INPUTS_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("=" * 60)
    print(f"R44 Phase2+Phase3：王道1（宗门公务员）走完seed后续流程")
    print(f"创意类型：阶级攀爬型 | 情绪基调：荒诞轻喜剧+权谋博弈")
    print("=" * 60)

    meta = {"creative": "王道1-宗门公务员", "creative_type": "阶级攀爬型", "emotion": "荒诞轻喜剧+权谋博弈", "phases": []}

    # ===== 段2: 打磨 =====
    print(f"\n[段2] 打磨——产出创意.md（三核心+营销层故事纲领）...")
    p2_prompt = build_phase2_prompt()
    try:
        p2_output, p2_usage, p2_elapsed = call_ds(
            PHASE2_SYSTEM, p2_prompt, max_tokens=8000, label="phase2"
        )
        save_input_output("phase2-创意", PHASE2_SYSTEM, p2_prompt, p2_output, p2_usage, p2_elapsed)
        meta["phases"].append({
            "name": "phase2-创意",
            "length": len(p2_output),
            "elapsed": round(p2_elapsed, 1),
            "tokens": p2_usage.get("total_tokens", 0)
        })
    except Exception as e:
        print(f"  [段2] 失败: {e}")
        sys.exit(1)

    # ===== 段3: 首章 =====
    print(f"\n[段3] 首章——产出ch001.md...")
    p3_prompt = build_phase3_prompt(p2_output)
    try:
        p3_output, p3_usage, p3_elapsed = call_ds(
            PHASE3_SYSTEM, p3_prompt, max_tokens=8000, label="phase3"
        )
        save_input_output("phase3-ch001", PHASE3_SYSTEM, p3_prompt, p3_output, p3_usage, p3_elapsed)
        meta["phases"].append({
            "name": "phase3-ch001",
            "length": len(p3_output),
            "elapsed": round(p3_elapsed, 1),
            "tokens": p3_usage.get("total_tokens", 0)
        })
    except Exception as e:
        print(f"  [段3] 失败: {e}")
        sys.exit(1)

    print(f"\n{'='*60}")
    print("R44 Phase2+Phase3 seed测试完成！")
    print(f"{'='*60}")
    print(f"\n{'段':<15} {'产出字数':<10} {'耗时':<8} {'tokens':<10}")
    print("-" * 50)
    for p in meta["phases"]:
        print(f"{p['name']:<15} {p['length']:<10} {p['elapsed']:<8} {p['tokens']:<10}")

    meta_path = os.path.join(OUTPUT_DIR, "r44-meta.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    print(f"\n输出目录: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
