#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
R24测试: plot skill剧情白描验证
- 复用R22的seed产出
- 在现有plot skill基础上，加入"剧情白描"步骤
- 产出：骨架.md + 剧情白描.md（完整故事流）
- 验证：plot对剧情改造的把控力
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

# ============ 目录 ============
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")

# R22产出路径（复用seed）
R22_OUTPUT = r"d:\popwave-skills\番茄skill群测试项目\R22\output"

# ============ 读取skill文件 ============
SKILLS_BASE = r"d:\popwave-skills\skills"

def read_skill_files(skill_name, files):
    parts = []
    for f in files:
        path = os.path.join(SKILLS_BASE, skill_name, f)
        with open(path, "r", encoding="utf-8") as fh:
            parts.append(fh.read())
    return "\n\n---\n\n".join(parts)

# ============ Plot System Prompt ============
PLOT_SYSTEM = read_skill_files("pop-fanqie-plot", [
    "SKILL.md",
    "steps/step1.md",
    "steps/step2.md",
    "steps/step3.md",
])

# ============ 剧情白描专用prompt（新增步骤）============
NARRATIVE_DEPICTION_PROMPT = """# 剧情白描（Plot层核心环节）

> 剧情白描是plot层最重要的环节，需投入50%注意力。
> 不是骨架表，不是幕弧线描述，是整卷故事一口气写完的完整叙事流。

## 产出要求

把第一卷的完整故事一口气写完，像给朋友讲故事一样自然流畅。

### 必须包含：
1. **完整故事流**——从ch01到卷末，一章接一章讲完，不拆章节/不标签
2. **具体场景**——每个关键场景有具体的地点/人物/动作/对话
3. **信息差标注**——用"（读者知道但角色不知道：XXX）"标注信息差
4. **伏笔标注**——用"（伏笔：XXX，chXX回收）"标注伏笔
5. **爽感闭环**——每个爽感爆发点写清楚：触发→爆发→后果
6. **章末钩子**——每章末有钩子，标注"（钩子：XXX）"
7. **画面/情绪/内心融入叙事**——不单独拆出来，融入故事流

### 格式参考（时停邪神Phase 1.5样式）：

> 他解开脚链坐到李右对面，故意说疯话拖延时间——自称吃了毒蘑菇才治好了疯病，又揪着"说谁眼瞎"的由头和李右斗嘴，硬生生从23:55拖到最后一分钟。命运轮盘的左轮装填了六发子弹，所有人都当他自杀，可白野在扣动扳机的瞬间发动了时间静止，从弹仓里抠出那颗即将发射的子弹塞进了口袋。（读者知道但角色不知道：这是他从文明世界带来的时差能力，大灾变世界的一天比他少了整整一分钟。）时间恢复流动，左轮击发为空枪，禁忌物【骸骨之息】认可了他，骨白色的枪体转为黑色哑光金属。

### 篇幅要求
- 第一卷50章的故事白描，约8000-12000字
- 不是每章详细写，是关键场景详细写+过渡场景一笔带过
- 像给朋友讲故事——该详细的地方详细，该快进的地方快进

### 禁止
- 禁止用表格
- 禁止用幕序列结构
- 禁止用"弧线描述"
- 禁止拆章节标签（如"## 第一幕"）
- 禁止写思考过程/检查表
- 直接写故事，一口气写完
"""

# ============ API调用 ============

def call_ds(system_prompt, user_prompt, max_tokens=16000, label=""):
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


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    results = {}

    print("=" * 60)
    print("R24测试: plot skill剧情白描验证")
    print("复用R22的seed产出 + 剧情白描步骤")
    print("=" * 60)

    # ========== 加载R22产出 ==========
    print(f"\n[0] 加载R22产出...")
    r22_seed_path = os.path.join(R22_OUTPUT, "r22-seed.md")
    with open(r22_seed_path, "r", encoding="utf-8") as f:
        seed_content = f.read()
    print(f"  Seed: {len(seed_content)}字")

    # ========== 1. Plot骨架阶段 ==========
    print(f"\n[1/2] 调用DeepSeek执行Plot (骨架.md)...")
    plot_user = f"""# 任务

以下是完整立项包（创意.md），请按plot skill全流程执行：
- Step 1: 加载立项包7项
- Step 2: 第一卷详规（终点+配角+幕序列+悬念+高潮+势力+反派+世界危机）
- Step 3: 落盘骨架.md

直接输出完整骨架.md，不要分段确认，不要问用户。

---

# 立项包

{seed_content}
"""
    print(f"  System: {len(PLOT_SYSTEM)}字符 | User: {len(plot_user)}字符")
    try:
        plot_content, plot_usage, plot_elapsed = call_ds(PLOT_SYSTEM, plot_user, max_tokens=16000, label="plot")
        plot_path = os.path.join(OUTPUT_DIR, "r24-plot.md")
        with open(plot_path, "w", encoding="utf-8") as f:
            f.write(plot_content)
        print(f"  完成! {plot_elapsed:.1f}s | {len(plot_content)}字 | tokens:{plot_usage.get('total_tokens', 'N/A')}")
        results["plot"] = {
            "model": DS_MODEL,
            "content_length": len(plot_content),
            "elapsed": round(plot_elapsed, 1),
            "usage": plot_usage,
            "path": plot_path
        }
    except Exception as e:
        print(f"  Plot失败: {e}")
        results["plot"] = {"error": str(e)}
        return

    # ========== 2. 剧情白描阶段（新增）==========
    print(f"\n[2/2] 调用DeepSeek执行剧情白描 (剧情白描.md)...")
    narrative_user = f"""# 任务

基于以下立项包和骨架，执行剧情白描——把第一卷的完整故事一口气写完。

{NARRATIVE_DEPICTION_PROMPT}

直接写故事，不要问用户，不要分段确认，不要写思考过程。

---

# 立项包（创意.md）

{seed_content}

---

# 骨架（骨架.md）

{plot_content}
"""
    # 剧情白描用骨架+立项包作为context，max_tokens设大一点
    narrative_system = "你是网文创作专家，擅长把骨架表转化为完整的剧情白描——整卷故事一口气写完的叙事流。"
    print(f"  System: {len(narrative_system)}字符 | User: {len(narrative_user)}字符")
    try:
        narrative_content, narrative_usage, narrative_elapsed = call_ds(narrative_system, narrative_user, max_tokens=16000, label="narrative")
        narrative_path = os.path.join(OUTPUT_DIR, "r24-剧情白描.md")
        with open(narrative_path, "w", encoding="utf-8") as f:
            f.write(narrative_content)
        print(f"  完成! {narrative_elapsed:.1f}s | {len(narrative_content)}字 | tokens:{narrative_usage.get('total_tokens', 'N/A')}")
        results["narrative"] = {
            "model": DS_MODEL,
            "content_length": len(narrative_content),
            "elapsed": round(narrative_elapsed, 1),
            "usage": narrative_usage,
            "path": narrative_path
        }
    except Exception as e:
        print(f"  剧情白描失败: {e}")
        results["narrative"] = {"error": str(e)}

    # ========== 汇总 ==========
    meta_path = os.path.join(OUTPUT_DIR, "r24-meta.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*60}")
    print("R24测试完成！")
    print(f"{'='*60}")
    for stage, val in results.items():
        if "error" in val:
            print(f"  {stage}: 失败 - {val['error']}")
        else:
            print(f"  {stage}: {val['content_length']}字 | {val['elapsed']}s | tokens:{val['usage'].get('total_tokens', 'N/A')}")
    print(f"\n输出目录: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
