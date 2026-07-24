#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
R41 seed测试：验证v13.9.0三核心重构效果

对比R40的改动点：
1. 发散选创意：好创意标准从读者三标准→读者三+作者三（六项全过）
2. 展示格式：立项评估从三容量→三核心（世界/舞台/主角）
3. 故事纲领：从五维框架→三核心+营销层（金手指融入主角核心）
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
PROXIES = {"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"}

TEMPERATURE = 0.85
TIMEOUT = 600

# ============ 目录 ============
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUTS_DIR = os.path.join(SCRIPT_DIR, "inputs")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")

# ============ 读取skill文件 ============
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

PHASE1_SYSTEM = read_skill_files("pop-fanqie-seed", ["SKILL.md", "steps/step1.md"])
PHASE2_SYSTEM = read_skill_files("pop-fanqie-seed", ["SKILL.md", "steps/step2.md"])
PHASE3_SYSTEM = read_skill_files("pop-fanqie-seed", ["SKILL.md", "steps/step3.md"])

TRACK = "都市异能"

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


# ============ 段1: 发散（对齐v13.9.0六项标准+三核心立项评估）============
PHASE1_PROMPT = f"""# 任务

按seed Phase 1双轨发散SOP，基于以下赛道方向，产出10个开书创意。

## 赛道方向
{TRACK}

## 产出要求

按step1的1d-A（王道赛道）和1d-B（猎奇赛道）各产出5个创意，共10个。

### 王道赛道（5个）
基于{TRACK}赛道已验证的常见卖点（隐藏身份/能力觉醒/都市悬案/逆袭打脸等），做差异化微调。每个创意保留已验证卖点做基底，但加新元素不撞车。

### 猎奇赛道（5个）
纯自由发散，追求反差/画面/原创性。不套框架，不想机制，只管有没有意思。

### 每个创意格式
```
#### [赛道标签] 创意名称
- 一句话描述：[主角是谁，在做什么，遇到了什么]
- 画面：[脑补的场景，最好带一句台词]
- 为什么有意思：[吸引人的点——读者视角]
- 市场定位：[王道：借鉴了什么卖点+做了什么差异化 / 猎奇：原创度说明]
**立项评估**：
- 世界：[什么样的世界——隐藏规则/可生长设定]
- 舞台：[什么世界危机驱动剧情——敌人梯度/压力源/倒计时]
- 主角：[主角什么特殊性（含金手指）——成长路径/升级空间]
```

### 好创意标准（自检，不通过重新发散）

读者三标准（验证吸引力）：
- 有画面：读完脑子里立刻浮现场景
- 有反差：两个不该在一起的东西放在一起了
- 有意思：读者看完会不会"卧槽这个我想看"？

作者三标准（验证可立项）：
- 有世界：创意能定义出什么样的世界？有什么隐藏规则/可生长设定？（world能推导力量体系/地图/势力）
- 有舞台：创意自带什么样的世界危机？什么驱动剧情持续运转100章？（world能推导敌人梯度/压力源/倒计时）
- 有主角：主角有什么特殊性（含金手指）？特殊性有升级空间吗？（world能推导成长路径/幕序列）

六项全过才放行。

### 禁止产出的类型
- "主角穿越到XX世界，获得XX系统，开始升级" — 纯事件
- "主角有XX能力，限制是XX，通过XX变强" — 纯机制
- "主角在XX势力中崛起，对抗XX敌人" — 纯势力操盘

## 注意
- 无需WebSearch扫榜，直接基于赛道常识发散
- 10个创意必须差异最大化——不同切入点、不同主角类型、不同情绪基调

## 最后
10个创意产出后，从王道赛道选1个最有潜力的创意，标注"【选定创意】"，用于进入Phase 2打磨。

直接输出10个创意+选定标注，不要写思考过程。
"""


# ============ 段2: 打磨（对齐v13.9.0三核心+营销层故事纲领）============
def build_phase2_prompt(phase1_output):
    return f"""# 任务

按seed Phase 2 SOP，对以下选定的创意进行结构化打磨，产出完整的创意.md。

## Phase 1 发散产出（含选定创意）

{phase1_output}

## 产出要求

按step2的2a-2f完整执行：

### 2a. 行为引擎检查
检查选定创意是否已有行为引擎（主角每章在做一件具体的事）。没有则用行为框架碰撞补上。

### 2b. 合成金手指
金手指 = 创意 × 机制 × 限制。三要素齐全，禁止只加限制不加代价。

### 2c. 四眼法验证
画面眼/限制眼/场景眼/引擎眼，四项全过才放行。

### 2e. 故事纲领（三核心+营销层·800字）

> 故事纲领是world的核心输入。world拿到三核心后能直接推导设定。金手指不再是独立维度——它是主角特殊性的一部分，融入"主角"核心。

#### 核心一：什么样的世界（2-3句）
world推导锚点：世界有什么隐藏规则？有哪些可生长的设定方向？world能从这里推导出力量体系/地图/势力。
写法：第一句给世界质感（读者也能闻到空气），后续句给world推导方向（隐藏规则/可生长设定）。

#### 核心二：什么样的舞台·世界危机（2-3句）
舞台 = 世界危机。危机驱动剧情持续运转100章——没有危机就没有故事。
world推导锚点：这个危机的源头是什么？能推导出什么敌人梯度/压力源/倒计时？
写法：第一句给读者压迫感（全书危机本质），后续句给world推导方向（危机源头→敌人梯度→压力源矩阵）。

#### 核心三：什么样的主角（3-4句）
主角特殊性 = 金手指 + 成长路径。金手指是主角特殊性的一部分，不是独立维度。
world推导锚点：主角的特殊性有升级空间吗？能推导出什么幕序列/对赌难度升级？
写法：三句话——起点（初始状态/困境+初始能力）、拐点（什么事件迫使改变+特殊性觉醒）、终点（最终变成什么+特殊性成熟）。特殊性包含金手指，金手指的机制和限制在这里交代。

#### 营销层（读者消费，非world输入）
- 最大钩子（≤20字）：路人翻三页被什么抓住
- 即时兑现感（2-3句）：前5章如何让读者感受到"已经在路上了"

### 2f. 落盘创意.md
按以下格式产出完整创意.md：

```markdown
# 创意名

## 一句话简介
（一句话说清这个创意是什么）

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

## 十、故事纲领（三核心+营销层）

> world的核心输入。三核心每项必须给world推导锚点。金手指融入主角核心，不独立。

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
- 至少1句荒谬台词
- 1个认知反转收尾
- 禁止设定说明书式写法
- 必须第一人称

### 故事纲领硬约束
- 三核心+营销层加起来≤800字
- 三核心（世界/舞台/主角）每项必须给出world推导锚点——world拿到后能直接推导设定
- 金手指融入"主角"核心，不再独立成维度
- 每项必须给出具体答案——不是"主角会成长"这种废话

直接输出完整创意.md，不要写思考过程。
"""


# ============ 段3: 首章（不变，和R40一致）============
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

直接输出ch001.md（正文+交付面板），不要写思考过程。
"""


# ============ 主流程 ============
def main():
    os.makedirs(INPUTS_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("=" * 60)
    print(f"R41 seed测试：验证v13.9.0三核心重构效果")
    print(f"赛道：{TRACK}")
    print("=" * 60)

    meta = {"track": TRACK, "phases": []}

    # ===== 段1: 发散 =====
    print(f"\n[段1] 发散——产出10个创意（六项标准+三核心立项评估）...")
    try:
        p1_output, p1_usage, p1_elapsed = call_ds(
            PHASE1_SYSTEM, PHASE1_PROMPT, max_tokens=8000, label="phase1"
        )
        save_input_output("phase1-发散", PHASE1_SYSTEM, PHASE1_PROMPT, p1_output, p1_usage, p1_elapsed)
        meta["phases"].append({
            "name": "phase1-发散",
            "length": len(p1_output),
            "elapsed": round(p1_elapsed, 1),
            "tokens": p1_usage.get("total_tokens", 0)
        })
    except Exception as e:
        print(f"  [段1] 失败: {e}")
        sys.exit(1)

    # ===== 段2: 打磨 =====
    print(f"\n[段2] 打磨——产出创意.md（三核心+营销层故事纲领）...")
    p2_prompt = build_phase2_prompt(p1_output)
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

    # ===== 汇总 =====
    print(f"\n{'='*60}")
    print("R41 seed测试完成！")
    print(f"{'='*60}")
    print(f"\n{'段':<15} {'产出字数':<10} {'耗时':<8} {'tokens':<10}")
    print("-" * 50)
    for p in meta["phases"]:
        print(f"{p['name']:<15} {p['length']:<10} {p['elapsed']:<8} {p['tokens']:<10}")

    meta_path = os.path.join(OUTPUT_DIR, "r41-meta.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    print(f"\n输出目录: {OUTPUT_DIR}")
    print(f"\n下一步: 人工复盘验收三个目标（对比R40）")


if __name__ == "__main__":
    main()
