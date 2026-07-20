#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
R43 seed测试：验证v13.11.0发散多样性修复
只跑段1（发散），验证10个创意是否覆盖≥5种情绪基调
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

PHASE1_SYSTEM = read_file(os.path.join(SKILLS_BASE, "pop-fanqie-seed", "SKILL.md")) + "\n\n---\n\n" + read_file(os.path.join(SKILLS_BASE, "pop-fanqie-seed", "steps", "step1.md"))

TRACK = "都市异能"

def call_ds(system_prompt, user_prompt, max_tokens=8000):
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

PHASE1_PROMPT = f"""# 任务

按seed Phase 1双轨发散SOP，基于以下赛道方向，产出10个开书创意。

## 赛道方向
{TRACK}

## 产出要求

按step1的1d-A（王道赛道）和1d-B（猎奇赛道）各产出5个创意，共10个。

### 王道赛道（5个）
基于{TRACK}赛道已验证的常见卖点（隐藏身份/能力觉醒/都市悬案/逆袭打脸等），做差异化微调。

### 猎奇赛道（5个）
纯自由发散，追求反差/画面/原创性。

### 每个创意格式
```
#### [赛道标签] 创意名称
- 一句话描述：[主角是谁，在做什么，遇到了什么]
- 画面：[脑补的场景，最好带一句台词]
- 为什么有意思：[吸引人的点——读者视角]
- 市场定位：[王道：借鉴了什么卖点+做了什么差异化 / 猎奇：原创度说明]
**情绪基调**：[热血逆袭/暗黑复仇/悬疑烧脑/都市恐怖/情感治愈/荒诞轻喜剧/末世求生/权谋博弈]
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
- 有世界：创意能定义出什么样的世界？有什么隐藏规则/可生长设定？
- 有舞台：创意自带什么样的世界危机？什么驱动剧情持续运转100章？
- 有主角：主角有什么特殊性（含金手指）？特殊性有升级空间吗？

六项全过才放行。

### 情绪基调强制多样化（v13.11.0核心约束）
10个创意（王道5+猎奇5）必须覆盖≥5种不同情绪基调，禁止全偏一种调性。情绪基调清单（不限于）：
- 热血逆袭（弱→强，打脸翻盘）
- 暗黑复仇（被背叛→复仇，冷酷烧脑）
- 悬疑烧脑（解谜推理，反转不断）
- 都市恐怖（民俗/规则恐怖，细思极恐）
- 情感治愈（温情救赎，以情动人）
- 荒诞轻喜剧（反差幽默，荒谬对话）
- 末世求生（资源管理，生存压力）
- 权谋博弈（势力操盘，智斗）

王道5个必须覆盖≥3种不同情绪基调。10个创意整体必须覆盖≥5种。

### 禁止产出的类型
- "主角穿越到XX世界，获得XX系统，开始升级" — 纯事件
- "主角有XX能力，限制是XX，通过XX变强" — 纯机制

## 注意
- 无需WebSearch扫榜，直接基于赛道常识发散
- 10个创意必须差异最大化——不同切入点、不同主角类型、不同情绪基调

## 最后
10个创意产出后，统计覆盖了哪几种情绪基调，从王道赛道选1个最有潜力的创意，标注"【选定创意】"。

直接输出10个创意+情绪基调统计+选定标注，不要写思考过程。
"""

def main():
    os.makedirs(INPUTS_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("=" * 60)
    print(f"R43: 验证v13.11.0发散多样性（情绪基调≥5种）")
    print(f"赛道：{TRACK}")
    print("=" * 60)

    print(f"\n[段1] 发散——10个创意（情绪基调强制多样化）...")
    try:
        output, usage, elapsed = call_ds(PHASE1_SYSTEM, PHASE1_PROMPT, max_tokens=8000)
        
        input_content = f"# SYSTEM PROMPT\n\n{PHASE1_SYSTEM}\n\n---\n\n# USER PROMPT\n\n{PHASE1_PROMPT}"
        with open(os.path.join(INPUTS_DIR, "phase1-发散_input.md"), "w", encoding="utf-8") as f:
            f.write(input_content)
        with open(os.path.join(OUTPUT_DIR, "phase1-发散.md"), "w", encoding="utf-8") as f:
            f.write(output)
        
        print(f"  完成! {elapsed:.1f}s | {len(output)}字符 | tokens:{usage.get('total_tokens', 0)}")
        print(f"  output → {os.path.join(OUTPUT_DIR, 'phase1-发散.md')}")
    except Exception as e:
        print(f"  失败: {e}")
        sys.exit(1)

    print(f"\n完成！下一步人工复盘验收情绪基调多样性")

if __name__ == "__main__":
    main()
