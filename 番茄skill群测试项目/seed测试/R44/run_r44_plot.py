#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
R44 plot测试：用world骨架.md走plot流程
验证plot能否承接world的骨架.md，产出剧情白描.md+章锚点表.md

输入：world-骨架.md + phase2-创意.md + phase3-ch001.md
输出：剧情白描.md + 章锚点表.md
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

# plot SKILL.md + step2 + step3 作为system prompt
PLOT_SYSTEM = read_skill_files("pop-fanqie-plot", ["SKILL.md", "steps/step2.md", "steps/step3.md"])

# 输入：world骨架.md + 创意.md + ch001.md
SKELETON_MD = read_file(os.path.join(OUTPUT_DIR, "world-骨架.md"))
CREATIVE_MD = read_file(os.path.join(OUTPUT_DIR, "phase2-创意.md"))
CH001_MD = read_file(os.path.join(os.path.join(SCRIPT_DIR, "output"), "phase3-ch001.md"))

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

def build_plot_prompt():
    return f"""# 任务

按pop-fanqie-plot v3.0.0的完整SOP，基于以下骨架.md+创意.md+ch001.md，执行plot流程，产出剧情白描.md+章锚点表.md。

## 输入1：骨架.md（world v1.1.0产出）

{SKELETON_MD}

## 输入2：创意.md（seed v13.13.0产出）

{CREATIVE_MD}

## 输入3：ch001.md（seed Phase 3产出）

{CH001_MD}

## 执行要求

按plot SOP完整执行Step 1-3：

### Step 1 · 加载骨架.md

从骨架.md提取白描输入：
- 力量体系→确定主角当前对赌难度
- 城市舞台→确定场景发生的地标
- 势力结构→确定碰撞的势力
- 危机压力→确定推进的倒计时
- 幕序列→按幕分段写白描
- 核心高潮点→展开为三段式高潮场景
- 悬念分层→标注信息差/伏笔/钩子

从ch001提取起点：
- 核心事件→章末钩子（ch002必须从这里延续）
- 金手指激活状态→已出场角色（不可冲突）

### Step 2 · 叙事流剧情白描

#### 2a. 叙事流写法（禁止提纲式）

核心规则：
- 每一段白描必须有至少1个**具体画面**（读者能在脑子里看到的）
- 每一段白描必须有至少1个**情绪锚点**（主角/配角此时此刻的感受——不是"他感到愤怒"，是"他把茶杯捏碎了，然后一条一条地捡起碎片"）
- 不使用"ch0XX"做段落开头——段落的边界是氛围切换，不是章节号

#### 2b. 信息差/伏笔/钩子内联标注

三种标注内联在白描中：
```
（信息差：XXX）
（伏笔：XXX，chXX揭示）
（钩子：XXX）
```
每段白描至少1个标注。

#### 2c. 推演流程

基于骨架.md的幕序列+高潮点+悬念分层，按幕分段写白描。

每段白描的结构：
```markdown
## 第N幕：「幕名」

### [场景标题——气氛关键词]
[叙事流正文，3-5段，不写章节号，以氛围切换分界]
（信息差：XXX）
（伏笔：XXX，chXX揭示）
（钩子：XXX）

### [下一个场景]
...
```

推演步骤：
1. 从骨架.md幕序列取第一幕的弧线
2. 查骨架.md城市结构表→确定场景发生的地标
3. 查骨架.md力量层级表→确定主角当前对赌难度
4. 查骨架.md势力结构表→确定碰撞的势力
5. 查骨架.md危机倒计时表→确定推进的倒计时
6. 写成叙事流（氛围+情绪+画面+事件推进）
7. 标注信息差/伏笔/钩子

#### 2d. 白描质量自检

每段白描写完后，逐条自检：
- 有画面吗？读完后脑子里能浮现场景
- 有情绪吗？能感受到主角/配角的情绪
- 有温度吗？能感受到这一段是紧张/温馨/压抑/轻松
- 有标注吗？每段至少1个标注
- 不写章节号吗？段落不以"ch0XX"开头

### Step 3 · 落盘+章锚点表

#### 3a. 落盘剧情白描.md

格式：
```markdown
# 《宗门公务员》· 第一卷剧情白描（ch001-ch100）

> ch001已由seed的黄金首章产出，本白描从ch002开始。
> ch001锚点：[核心事件摘要] + [章末钩子]

（Step 2产出的整卷叙事流白描，分场景标注信息差/伏笔/钩子）

---
卷末钩子：[本卷最后的悬念]
```

#### 3b. 提取章锚点表.md

从剧情白描中提取每章的锚点信息。每章一行：

```markdown
# 《宗门公务员》· 第一卷章锚点表

| 章号 | 场景 | 章型 | 核心事件（1-2句） | 爽点 | 钩子 | 预期回收章 |
|:--|:--|:--|:--|:--|:--|:--|
| ch001 | （从seed黄金首章提取） | opening_shift | ... | ... | ... | ch002 |
| ch002 | ... | ... | ... | ... | ... | ... |
| ... | ... | ... | ... | ... | ... | ... |
```

章型映射（从白描的氛围+事件推导）：
- 遭遇新势力/被堵门/正面冲突 → confrontation_pressure
- 揭秘/发现真相/信息释放 → reveal_hook
- 战斗/绝境翻盘 → combat_reversal
- 场景切换/新地图/身份变化 → opening_shift

## 红线
1. **必须加载骨架.md**——禁止凭空编造世界
2. **剧情白描必须是叙事流，不是注水提纲**——每段必须有氛围/情绪弧/关键画面
3. **第一卷终点必须与世界危机挂钩**——不能只是打完boss就结束
4. **ch002必须从ch001章末钩子延续**——不能断线

## 注意
- 骨架.md有4幕（第一幕ch001-025/第二幕ch026-050/第三幕ch051-075/第四幕ch076-100），白描按幕分段
- 骨架.md有2个核心高潮点（火烧仓库ch015-020/长老会上的凡人ch065-075），展开为三段式高潮场景
- 骨架.md有8条悬念分层，白描中标注伏笔和钩子
- ch001章末钩子是"丹峰方向有人遁走报信"，ch002必须从这里延续
- 第一卷100章，章锚点表需要100行（ch001-ch100）

直接输出剧情白描.md和章锚点表.md（两个文件用---分隔），不要写思考过程。
"""

def main():
    os.makedirs(INPUTS_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("=" * 60)
    print(f"R44 plot：用world骨架.md走plot流程")
    print(f"输入：骨架.md + 创意.md + ch001.md → 输出：剧情白描.md + 章锚点表.md")
    print("=" * 60)

    print(f"\n[plot] 叙事流剧情白描+章锚点表...")
    plot_prompt = build_plot_prompt()
    try:
        plot_output, plot_usage, plot_elapsed = call_ds(
            PLOT_SYSTEM, plot_prompt, max_tokens=12000
        )
        save_input_output("plot-剧情白描+章锚点表", PLOT_SYSTEM, plot_prompt, plot_output, plot_usage, plot_elapsed)
    except Exception as e:
        print(f"  [plot] 失败: {e}")
        sys.exit(1)

    print(f"\n{'='*60}")
    print("R44 plot测试完成！")
    print(f"{'='*60}")
    print(f"\n产出: {os.path.join(OUTPUT_DIR, 'plot-剧情白描+章锚点表.md')}")
    print(f"下一步：人工验收plot能否承接world骨架.md")

if __name__ == "__main__":
    main()
