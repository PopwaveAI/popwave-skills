#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
R42-A seed测试：王道1（暗巷仲裁者）验证v13.10.1世界SOP规则差异三层
对比R41王道1走形式——是否修复
"""

import os, sys, json, time, requests

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
    return "\n\n---\n\n".join([read_file(os.path.join(SKILLS_BASE, skill_name, f)) for f in files])

PHASE2_SYSTEM = read_skill_files("pop-fanqie-seed", ["SKILL.md", "steps/step2.md"])
PHASE3_SYSTEM = read_skill_files("pop-fanqie-seed", ["SKILL.md", "steps/step3.md"])

# R42-A: 王道1（暗巷仲裁者）
CREATIVE = """#### [王道] 王道1：暗巷仲裁者
- 一句话描述：主角是个开在凶宅三楼的破律师事务所老板，能看见合同上的因果线，专门替鬼魂打官司。
- 画面：法庭上，房东拿出一纸租房合同说"白纸黑字写了提前退租不退押金"。主角扫了一眼合同上缠绕的因果线——那根线是从房东的笔尖渗出来的，缠住了租客的脖子。主角微微一笑："你这合同，有个漏洞。"
- 为什么有意思：把"律政博弈"和"都市灵异"结合，每案一结的单元剧结构清晰，且"法律条款×因果规则"的设定新颖。
- 市场定位：借鉴了"律政文"的专业博弈基底，加入"因果线"灵异元素做差异化。
**立项评估**：
- 世界：灵异事件被都市规则掩盖的现代都市，超自然事件背后都有合同/协议支撑
- 舞台：因果规则正在被改写，有人想改成收割寿命的霸王条款
- 主角：能看见合同因果线，力量路径从看→改→预判→写规则

【选定创意】：王道1：暗巷仲裁者"""

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
    return result["choices"][0]["message"]["content"], result.get("usage", {}), elapsed

def save_io(phase_name, system_prompt, user_prompt, output_content, usage, elapsed):
    input_content = f"# SYSTEM PROMPT\n\n{system_prompt}\n\n---\n\n# USER PROMPT\n\n{user_prompt}"
    with open(os.path.join(INPUTS_DIR, f"{phase_name}_input.md"), "w", encoding="utf-8") as f:
        f.write(input_content)
    with open(os.path.join(OUTPUT_DIR, f"{phase_name}.md"), "w", encoding="utf-8") as f:
        f.write(output_content)
    print(f"  [{phase_name}] {elapsed:.1f}s | {len(output_content)}字符 | tokens:{usage.get('total_tokens', 0)}")

def build_phase2_prompt():
    return f"""# 任务

按seed Phase 2 SOP，对以下选定的创意进行结构化打磨，产出完整的创意.md。

## Phase 1 发散产出（含选定创意）

{CREATIVE}

## 产出要求

按step2的2a-2f完整执行。特别注意2e故事纲领的质量标准——三核心每项必须通过自检清单，缺项=重写。

### 2e. 故事纲领（三核心+营销层·≤1000字）

> 故事纲领是world的核心输入。走形式=废纲领。

#### 核心一：什么样的世界
质量标准（规则差异三层，缺项=重写）：
- 差异层：这个世界和现实有什么不同？（1条核心差异——具体的运转法则）
- 日常层：这个差异如何影响普通人日常？（普通人怎么活？这一层决定世界真实感）
- 主角层：这个差异如何影响主角生存？（主角在差异里的位置，和核心三衔接）

#### 核心二：什么样的舞台·世界危机
质量标准（缺项=重写）：
- 1个全书危机源头（具体的、有来源的威胁，不是口号）
- ≥3层敌人梯度（每层有具体对象，不是标签）
- ≥1个压力源/倒计时（驱动主角不能停的压力）

#### 核心三：什么样的主角
质量标准（缺项=重写）：
- 起点+拐点+终点三段完整（每段有具体状态）
- ≥3级力量路径（每级有具体能力+场景）
- 力量路径映射幕序列（每级=一幕）

#### 营销层
- 最大钩子（≤20字）
- 即时兑现感（2-3句）

### 2f. 落盘创意.md（完整格式）
```markdown
# 创意名

## 一句话简介
## 创意
## 创意来源
## 金手指
- 创意：（一句话）
- 机制：（一句话）
- 限制：（一句话）
- 合成：（完整表述）
## 行为引擎
## 轻量主角轮廓
- 名字/身份/核心动机/记忆点
## 番茄简介
（150-300字，第一人称散文体，至少3个连环创意点+1句荒谬台词+1个认知反转收尾）
## 十、故事纲领（三核心+营销层）

### 什么样的世界
（差异层+日常层+主角层，每层1-2句）

### 什么样的舞台·世界危机
（危机源头+敌人梯度≥3层+压力源）

### 什么样的主角
- 起点/拐点/终点/力量路径（≥3级映射幕序列）

### 最大钩子
（≤20字）

### 即时兑现感
（2-3句）
```

### 故事纲领自检清单（写完后逐项检查，缺项=重写）
- 世界有差异层吗？（1条核心差异）
- 世界有日常层吗？（普通人怎么活）
- 世界有主角层吗？（主角在差异里的位置）
- 舞台有危机源头吗？（具体的威胁）
- 舞台有敌人梯度吗？（≥3层有具体对象）
- 舞台有压力源/倒计时吗？
- 主角有三段弧线吗？
- 主角有力量路径吗？（≥3级有具体能力+场景）
- 力量路径映射幕序列吗？

直接输出完整创意.md，不要写思考过程。
"""

def build_phase3_prompt(phase2_output):
    return f"""# 任务

按seed Phase 3 SOP，基于以下创意.md，写黄金首章ch001。

## 创意.md

{phase2_output}

## 产出要求

按step3的3a-3f完整执行：
1. 前3句扔炸弹——第一句话就制造冲突/悬念/反差
2. 300字内完成4件事——冲突+主角+金手指激活+章末钩子
3. 第一章必须激活金手指+1个爽感触发+章末钩子+反差画面
4. 总字数2000-2500字

### 落盘格式
```markdown
# （10字以上章名）

[2000-2500字正文]

---

## 交付面板
| 字段 | 值 |
|------|-----|
| 章号 | ch001 |
| 章名 | |
| 章型 | opening_shift |
| 字数 | |
| 核心事件 | |
| 反差画面 | |
| 爽感闭环 | |
| 章末钩子 | |
| 笔触状态 | trial模式 |
```

trial模式（无DNA）。基础风格：简洁短句+动作驱动+对话推进。

直接输出ch001.md，不要写思考过程。
"""

def main():
    os.makedirs(INPUTS_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("=" * 60)
    print(f"R42-A: 王道1（暗巷仲裁者）验证v13.10.1世界SOP")
    print("=" * 60)

    print(f"\n[段2] 打磨——创意.md...")
    p2_prompt = build_phase2_prompt()
    p2_output, p2_usage, p2_elapsed = call_ds(PHASE2_SYSTEM, p2_prompt, max_tokens=8000)
    save_io("phase2-创意", PHASE2_SYSTEM, p2_prompt, p2_output, p2_usage, p2_elapsed)

    print(f"\n[段3] 首章——ch001.md...")
    p3_prompt = build_phase3_prompt(p2_output)
    p3_output, p3_usage, p3_elapsed = call_ds(PHASE3_SYSTEM, p3_prompt, max_tokens=8000)
    save_io("phase3-ch001", PHASE3_SYSTEM, p3_prompt, p3_output, p3_usage, p3_elapsed)

    print(f"\n完成！输出: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
