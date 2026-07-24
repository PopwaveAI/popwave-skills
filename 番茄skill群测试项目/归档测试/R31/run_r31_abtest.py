#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
R31 AB测试: 我们的write skill v7.1.0 vs 外部AI写作平台PE
用深渊主宰C方案作为统一输入，对比两者正文质量

A组: write v7.1.0 skill（5步SOP+章型+爽感引擎+精选设定库）
B组: 外部PE（4段式骨架+19条规则+章节名要求）

统一输入（C方案）：
- Phase1.5剧情白描
- Phase2 L2+卷纲
- 白描卡ch001-005
- 精选设定库
- 前章正文（串联时注入）

测试：5章串联，对比质量
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
MAX_CHAPTERS = 5

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

# ============ 外部PE（原文照搬）============
EXTERNAL_PE = """你是一位爆款网文作家，擅长根据用户提供的章纲创作一篇完整的正文，并能完美衔接用户的前文内容。
用户会提供给你后续两章的章纲，你只需要为用户创作第一章的正文，并为后续第二章的内容留好钩子或者铺垫。
我现在需要你根据我提供的章纲进行续写。
续写要求如下：
根据用户提供的内容，按照"拆解冲突+填充细节+推动节奏"逻辑，生成一篇完整的网文章节，要求情节连贯、细节饱满、符合网文阅读节奏，结尾留悬念。
1. 第一步：拆解框架（约占章节搭建30%逻辑）
- 从核心句中提炼3要素：核心冲突/事件、人物目标、场景限定。
- 按"4段式骨架"分配篇幅：
- 开篇（650-750字）：渲染场景氛围，交代人物行动动机（为何出现在该场景）。
- 发展（950-1050字）：描写人物探索/行动过程，加入1-2个小阻碍（如寻找时的意外、环境干扰），逐步接近核心目标。
- 高潮（850-950字）：达成核心目标（如找到关键物品、触发关键事件），同步引发新冲突（如突发危险、意外人物出现）。
- 结尾（650-750字）：刻画人物即时反应，留下悬念钩子（如未解决的危险、关键线索升级、人物反转）。
2. 第二步：填充细节（约占内容扩展60%篇幅）
- 场景描写：结合场景限定，从听觉、视觉、触觉/嗅觉多维度刻画，用环境烘托情绪（如"雨夜旧仓库"需写雨声、光线、霉味等）。
- 人物刻画：通过"动作链"（拆解连续动作，避免概括性描述）、心理活动（结合事件加入回忆、疑惑、情绪波动）、简短对话/独白，塑造人物形象。
- 情节打磨：所有细节围绕"核心冲突"和"人物目标"展开，拒绝无关凑数内容。
3. 第三步：节奏与收尾（约占阅读体验10%重点）
- 节奏控制："慢描写"（场景、心理）与"快行动"（冲突、探索）交替，避免平铺直叙。
- 结尾要求：必须留下"未完成"悬念（如突发危险、线索升级、人物反转），吸引读者继续阅读。
你需要先对前文进行分析，比如前文的写作风格，矛盾冲突，主线以及情绪拉扯等。
提取前文剧情中的关键信息，包括但不限于：男女主角信息和主要事件，人物关系，各主要配角的信息，主角金手指的所有信息（功能及当前状态），前文的主要剧情概述。
开篇先输出对前文的分析，然后输出本章的创作思路，以及下一章的简要思路，再输出续写后的本章正文。
要尽量模仿前文的写作文风。请用最精简的语句写作，不要有过多的描述性描写。不要有形容声音和眼神的描写。
创作的内容必须符合文中的年代背景，尊重现实社会的规则。
要求：
1.每一章的结尾都必须是期待感的对话钩子作为结尾，不要让事件完结或者情绪落地，通过各种手法强制引导读者阅读下一章。
2.生成的正文的开头要完美衔接前文结尾，但是不要有和前文重复的剧情。
3.生成内容番茄小说爆款文风。
4.生成内容不要出现重复剧情、重复描写。
5.剧情逻辑要清楚合理。
6.每章前后文要有连接。
7.生成的正文和描写大白话一些。
8.生成的内容情绪值强烈，有吸引力。
9.输出的语句要精炼，表达清晰，不要Ai叙述词，但仍然需要保持阅读感。
10.减少形容词和比喻句和拟人句，如果没有必要不要使用。
11.增加代入感。
12.在合适的剧情里加入适当的剧情对话。
13.可以参考前后文，适当改变文章内容，但不允许大改。
14.顺带检查是否存在剧情漏洞，道具错误，系统奖励错误等。
15.根据前一章的末尾进行衔接创作。不要重复前文的内容。
16.不要生成总结性和展望未来等类似的的内容。
17.各种描写和比喻不要过多，每章控制在3-8个描写，每个描写字数不超过30字。
18.生成的内容情绪值足，有吸引力。
19.参考前文剧情框架进行创作，要完美衔接前文的剧情。
最后创作一个一句话并且有噱头或者反差的章节名。章节名放到正文的开头。
章节名要能展现本章的噱头或者爽点，或者是有反差的隐喻（可以玩梗）。10个字以上的一句话句子。
最后输出的所有文字必须为简体中文。
输出内容时前文分析，本章创作思路和下一章简要思路不需要输出 。
但是必须输出本次创作的是第几章的正文并且为第几章所做好的铺垫，用来提醒用户。然后再输出正文。"""

# ============ 精选设定库（≤1000字，与R29一致）============
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
    for i in range(1, MAX_CHAPTERS + 1):
        ch_num = f"ch{i:03d}"
        ch_path = os.path.join(CHAPTERS_DIR, f"{ch_num}.md")
        if os.path.exists(ch_path):
            with open(ch_path, "r", encoding="utf-8") as f:
                chapters[ch_num] = f.read()
    files["chapters"] = chapters

    return files


# ============ A组：write v7.1.0 skill ============

def build_prompt_a(decon_files, ch_num, prev_chapter):
    """A组：write v7.1.0 skill"""
    chapter_card = decon_files["chapters"].get(ch_num, "")

    if prev_chapter:
        prev_hint = "- **如非第一章，必须回收前章钩子**——本章前300字必须回收前章章末钩子\n- 前章正文已注入下方，用于回收钩子"
    else:
        prev_hint = "- 第一章使用黄金开篇：前3句扔炸弹，300字内完成冲突+主角+金手指+钩子"

    prompt = f"""# 任务

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


# ============ B组：外部PE ============

def build_prompt_b(decon_files, ch_num, prev_chapter):
    """B组：外部PE"""
    chapter_card = decon_files["chapters"].get(ch_num, "")

    # 外部PE要求"后续两章的章纲"——我们提供当前章+下一章白描卡
    ch_idx = int(ch_num.replace("ch", ""))
    next_ch_num = f"ch{ch_idx+1:03d}"
    next_chapter_card = decon_files["chapters"].get(next_ch_num, "（无下一章白描卡）")

    prompt = f"""# 任务

请根据我提供的章纲续写{ch_num}的正文。你只需要创作{ch_num}的正文，并为{next_ch_num}留好钩子或铺垫。

---

# 章纲（{ch_num}和{next_ch_num}两章）

## {ch_num} 章纲

{chapter_card}

## {next_ch_num} 章纲（仅参考，用于留铺垫）

{next_chapter_card}

---

# 设定库

{CURATED_SETTINGS}

---

# 卷纲+L2单元卡

{decon_files['phase2']}

---

# 剧情白描（全书故事流，用于理解上下文）

{decon_files['phase15']}
"""
    if prev_chapter:
        prompt += f"\n\n---\n\n# 前文（{ch_idx-1}章正文，用于衔接）\n\n{prev_chapter}\n"
    return prompt


# ============ 主流程 ============

def run_group(group_name, system_prompt, build_prompt_fn, decon_files, output_subdir):
    """跑一组5章串联"""
    print(f"\n[{group_name}] 开始跑5章串联...")
    results = []
    prev_chapter = None

    for ch_idx in range(1, MAX_CHAPTERS + 1):
        ch_num = f"ch{ch_idx:03d}"

        if ch_num not in decon_files["chapters"]:
            print(f"  [{ch_idx}/5] {ch_num} 白描卡不存在，跳过")
            continue

        user_prompt = build_prompt_fn(decon_files, ch_num, prev_chapter)
        prompt_len = len(user_prompt)
        print(f"  [{ch_idx}/5] {group_name}_{ch_num} 调用DeepSeek... (prompt: {prompt_len}字符)")

        try:
            # B组外部PE要求字数更多，max_tokens调大
            max_tokens = 10000 if group_name == "B" else 8000
            content, usage, elapsed = call_ds(
                system_prompt, user_prompt, max_tokens=max_tokens, label=f"R31_{group_name}_{ch_num}"
            )
            out_path = os.path.join(output_subdir, f"{ch_num}.md")
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
            print(f"    {group_name}_{ch_num}失败: {e}")
            results.append({"ch_num": ch_num, "error": str(e)})
            prev_chapter = None

    return results


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("=" * 60)
    print("R31 AB测试: write v7.1.0 vs 外部PE")
    print("统一输入：深渊主宰C方案（拆书产出）")
    print("=" * 60)

    print(f"\n[0] 加载拆书产出...")
    decon_files = load_decon_files()
    print(f"  Phase1.5剧情白描: {len(decon_files['phase15'])}字")
    print(f"  Phase2 L2+卷纲: {len(decon_files['phase2'])}字")
    print(f"  白描卡: {len(decon_files['chapters'])}章")
    print(f"  精选设定库: {len(CURATED_SETTINGS)}字")

    # A组
    a_output = os.path.join(OUTPUT_DIR, "A-write-skill")
    os.makedirs(a_output, exist_ok=True)
    a_results = run_group("A", WRITE_SYSTEM_V71, build_prompt_a, decon_files, a_output)

    # B组
    b_output = os.path.join(OUTPUT_DIR, "B-external-pe")
    os.makedirs(b_output, exist_ok=True)
    b_results = run_group("B", EXTERNAL_PE, build_prompt_b, decon_files, b_output)

    # 汇总
    print(f"\n{'='*60}")
    print("R31 AB测试完成！")
    print(f"{'='*60}")

    print(f"\n[A组 write v7.1.0]")
    print(f"{'章号':<10} {'输入字数':<10} {'产出字数':<10} {'耗时':<8} {'tokens':<10}")
    print("-" * 60)
    for r in a_results:
        if "error" in r:
            print(f"{r.get('ch_num','?'):<10} 失败: {r['error']}")
        else:
            print(f"{r['ch_num']:<10} {r['prompt_length']:<10} {r['content_length']:<10} {r['elapsed']:<8} {r['tokens']:<10}")

    print(f"\n[B组 外部PE]")
    print(f"{'章号':<10} {'输入字数':<10} {'产出字数':<10} {'耗时':<8} {'tokens':<10}")
    print("-" * 60)
    for r in b_results:
        if "error" in r:
            print(f"{r.get('ch_num','?'):<10} 失败: {r['error']}")
        else:
            print(f"{r['ch_num']:<10} {r['prompt_length']:<10} {r['content_length']:<10} {r['elapsed']:<8} {r['tokens']:<10}")

    # 保存meta
    meta = {
        "config": {
            "model": DS_MODEL,
            "temperature": TEMPERATURE,
            "chapters": MAX_CHAPTERS,
            "input": "深渊主宰C方案（拆书产出）"
        },
        "A_write_skill": a_results,
        "B_external_pe": b_results
    }
    meta_path = os.path.join(OUTPUT_DIR, "r31-meta.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    print(f"\n输出目录: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
