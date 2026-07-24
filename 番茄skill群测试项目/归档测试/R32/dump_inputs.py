#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
R32输入落盘工具
把A组(write v7.2.0)和B组(外部PE)的完整输入(system+user)落盘成文件
不调用API，只落盘prompt
"""

import os
import json

# ============ 目录 ============
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")
INPUT_DIR = os.path.join(OUTPUT_DIR, "inputs")  # 输入落盘目录

DECON_BASE = r"d:\popwave-skills\workspace\深渊主宰-瘦身白描测试"
PHASE15_PATH = os.path.join(DECON_BASE, "下游产出", "Phase1.5-全书剧情白描.md")
PHASE2_PATH = os.path.join(DECON_BASE, "下游产出", "Phase2-L2单元卡+卷纲+叙事技法.md")
CHAPTERS_DIR = os.path.join(DECON_BASE, "chapters")

# R32 output里有前章正文，用于复用
R32_A_OUTPUT = os.path.join(OUTPUT_DIR, "A-write-v720")
R32_B_OUTPUT = os.path.join(OUTPUT_DIR, "B-external-pe")

SKILLS_BASE = r"d:\popwave-skills\skills"
MAX_CHAPTERS = 5

# ============ 读取skill文件（v7.2.0）============

def read_skill_files(skill_name, files):
    parts = []
    for f in files:
        path = os.path.join(SKILLS_BASE, skill_name, f)
        with open(path, "r", encoding="utf-8") as fh:
            parts.append(fh.read())
    return "\n\n---\n\n".join(parts)

WRITE_SYSTEM_V72 = read_skill_files("pop-fanqie-write", [
    "SKILL.md",
    "steps/step1.md",
    "steps/step2.md",
    "steps/step3.md",
    "steps/step4.md",
    "steps/step5.md",
    "references/章型定义.md",
    "references/爽点引擎.md",
])

# ============ 外部PE（与R32一致）============

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

# ============ 精选设定库（与R32一致）============

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

# ============ 加载拆书产出 ============

def load_decon_files():
    files = {}
    with open(PHASE15_PATH, "r", encoding="utf-8") as f:
        files["phase15"] = f.read()
    with open(PHASE2_PATH, "r", encoding="utf-8") as f:
        files["phase2"] = f.read()

    chapters = {}
    for i in range(1, MAX_CHAPTERS + 2):  # +1因为B组需要下一章白描卡
        ch_num = f"ch{i:03d}"
        ch_path = os.path.join(CHAPTERS_DIR, f"{ch_num}.md")
        if os.path.exists(ch_path):
            with open(ch_path, "r", encoding="utf-8") as f:
                chapters[ch_num] = f.read()
    files["chapters"] = chapters

    return files

# ============ 加载前章正文（从R32 output复用）============

def load_prev_chapters():
    """从R32 output读取前章正文，构造与R32完全一致的输入"""
    a_prev = {}
    b_prev = {}
    for i in range(1, MAX_CHAPTERS + 1):
        ch_num = f"ch{i:03d}"
        a_path = os.path.join(R32_A_OUTPUT, f"{ch_num}.md")
        b_path = os.path.join(R32_B_OUTPUT, f"{ch_num}.md")
        if os.path.exists(a_path):
            with open(a_path, "r", encoding="utf-8") as f:
                a_prev[ch_num] = f.read()
        if os.path.exists(b_path):
            with open(b_path, "r", encoding="utf-8") as f:
                b_prev[ch_num] = f.read()
    return a_prev, b_prev

# ============ A组prompt构建（与R32一致）============

def build_prompt_a(decon_files, ch_num, prev_chapter):
    chapter_card = decon_files["chapters"].get(ch_num, "")

    if prev_chapter:
        prev_hint = "- **如非第一章，必须回收前章钩子**——本章前300字必须回收前章章末钩子\n- 前章正文已注入下方，用于回收钩子"
    else:
        prev_hint = "- 第一章使用黄金开篇：前3句扔炸弹，300字内完成冲突+主角+金手指+钩子"

    prompt = f"""# 任务

请按write skill v7.2.0全流程写本章（{ch_num}）正文。

5步SOP：
- Step 1: 加载燃料
- Step 2: 章型+技法锁定（**v7.2.0新增动作链+多感官优先级+章名设计**）
- Step 3: 写正文，2000-2500字，不准超过2500字
- Step 4: 篇幅硬限制检查+落盘
- Step 5: 交付面板（**v7.2.0新增章名/动作链数量/多感官场景数量字段**）

关键约束：
- **v7.2.0动作链硬约束**：禁止用1个动词概括连续动作，必须拆成2-3个细动作。每章≥3处，战斗章≥5处
- **v7.2.0多感官硬约束**：每场景至少覆盖3种感官，每章≥2处完整多感官描写，战斗章≥3处
- **v7.2.0章名设计**：正文开头必须有10字以上设计章名（有噱头/反差/玩梗）
- 参照白描卡写
- 番茄快爽改造：节奏更紧凑、爽感更密集、章末钩子更主动
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

# ============ B组prompt构建（与R32一致）============

def build_prompt_b(decon_files, ch_num, prev_chapter):
    chapter_card = decon_files["chapters"].get(ch_num, "")

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

# ============ 落盘 ============

def dump_prompt(output_subdir, ch_num, system_prompt, user_prompt):
    """把一个完整输入落盘成1个文件"""
    out_path = os.path.join(output_subdir, f"{ch_num}_input.md")
    content = f"""# {ch_num} 完整输入

## === SYSTEM PROMPT ===

{system_prompt}

## === USER PROMPT ===

{user_prompt}

## === 元信息 ===

- system_prompt长度: {len(system_prompt)} 字符
- user_prompt长度: {len(user_prompt)} 字符
- 总输入长度: {len(system_prompt) + len(user_prompt)} 字符
"""
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)
    return out_path, len(system_prompt), len(user_prompt)

# ============ 主流程 ============

def main():
    os.makedirs(INPUT_DIR, exist_ok=True)
    a_input_dir = os.path.join(INPUT_DIR, "A-write-v720")
    b_input_dir = os.path.join(INPUT_DIR, "B-external-pe")
    os.makedirs(a_input_dir, exist_ok=True)
    os.makedirs(b_input_dir, exist_ok=True)

    print("=" * 60)
    print("R32输入落盘工具")
    print("把A组(write v7.2.0)和B组(外部PE)的完整输入落盘")
    print("=" * 60)

    print(f"\n[0] 加载拆书产出...")
    decon_files = load_decon_files()
    print(f"  Phase1.5剧情白描: {len(decon_files['phase15'])}字")
    print(f"  Phase2 L2+卷纲: {len(decon_files['phase2'])}字")
    print(f"  白描卡: {len(decon_files['chapters'])}章")
    print(f"  精选设定库: {len(CURATED_SETTINGS)}字")

    print(f"\n[0.1] 加载R32前章正文...")
    a_prev, b_prev = load_prev_chapters()
    print(f"  A组前章: {len(a_prev)}章")
    print(f"  B组前章: {len(b_prev)}章")

    # A组
    print(f"\n[A组 write v7.2.0] 落盘5章输入...")
    a_meta = []
    prev_chapter = None
    for ch_idx in range(1, MAX_CHAPTERS + 1):
        ch_num = f"ch{ch_idx:03d}"
        if ch_num not in decon_files["chapters"]:
            print(f"  [{ch_idx}/5] {ch_num} 白描卡不存在，跳过")
            continue

        # 用R32实际产生的前章正文
        if ch_idx > 1:
            prev_ch_num = f"ch{ch_idx-1:03d}"
            prev_chapter = a_prev.get(prev_ch_num)

        user_prompt = build_prompt_a(decon_files, ch_num, prev_chapter)
        out_path, sys_len, user_len = dump_prompt(
            a_input_dir, ch_num, WRITE_SYSTEM_V72, user_prompt
        )
        total = sys_len + user_len
        print(f"  [{ch_idx}/5] {ch_num} 落盘完成 | system:{sys_len} user:{user_len} total:{total}")
        a_meta.append({
            "ch_num": ch_num,
            "system_length": sys_len,
            "user_length": user_len,
            "total_length": total,
            "path": out_path
        })

    # B组
    print(f"\n[B组 外部PE] 落盘5章输入...")
    b_meta = []
    prev_chapter = None
    for ch_idx in range(1, MAX_CHAPTERS + 1):
        ch_num = f"ch{ch_idx:03d}"
        if ch_num not in decon_files["chapters"]:
            print(f"  [{ch_idx}/5] {ch_num} 白描卡不存在，跳过")
            continue

        if ch_idx > 1:
            prev_ch_num = f"ch{ch_idx-1:03d}"
            prev_chapter = b_prev.get(prev_ch_num)

        user_prompt = build_prompt_b(decon_files, ch_num, prev_chapter)
        out_path, sys_len, user_len = dump_prompt(
            b_input_dir, ch_num, EXTERNAL_PE, user_prompt
        )
        total = sys_len + user_len
        print(f"  [{ch_idx}/5] {ch_num} 落盘完成 | system:{sys_len} user:{user_len} total:{total}")
        b_meta.append({
            "ch_num": ch_num,
            "system_length": sys_len,
            "user_length": user_len,
            "total_length": total,
            "path": out_path
        })

    # 汇总
    print(f"\n{'='*60}")
    print("R32输入落盘完成！")
    print(f"{'='*60}")

    print(f"\n[A组 write v7.2.0]")
    print(f"{'章号':<10} {'system':<10} {'user':<10} {'total':<10} {'文件'}")
    print("-" * 80)
    for r in a_meta:
        print(f"{r['ch_num']:<10} {r['system_length']:<10} {r['user_length']:<10} {r['total_length']:<10} {r['path']}")

    print(f"\n[B组 外部PE]")
    print(f"{'章号':<10} {'system':<10} {'user':<10} {'total':<10} {'文件'}")
    print("-" * 80)
    for r in b_meta:
        print(f"{r['ch_num']:<10} {r['system_length']:<10} {r['user_length']:<10} {r['total_length']:<10} {r['path']}")

    # 保存meta
    meta = {
        "A_write_v720": a_meta,
        "B_external_pe": b_meta
    }
    meta_path = os.path.join(INPUT_DIR, "inputs-meta.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    print(f"\n输入文件目录: {INPUT_DIR}")
    print(f"A组: {a_input_dir}")
    print(f"B组: {b_input_dir}")


if __name__ == "__main__":
    main()
