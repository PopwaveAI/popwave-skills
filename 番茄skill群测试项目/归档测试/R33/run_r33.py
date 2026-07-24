#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
R33测试: 模拟真正的write skill执行流程
- 精选注入：只注入当前卷的Phase2+Phase1.5，不是全书9卷
- 字数自检：每章写完后调用wordcount_check.py裁剪
- 单组测试（A组write v7.2.0），对比R32看输入精选后的效果

与R32的区别：
- R32: 全量注入Phase2(12109字)+Phase1.5(35318字) = 47427字
- R33: 精选注入卷1的Phase2(~1500字)+Phase1.5(~3500字) = ~5000字
- R33: 每章写完后调用wordcount_check.py裁剪
"""

import os
import sys
import json
import time
import re
import requests
import subprocess

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

# 字数自检脚本
WORDCOUNT_SCRIPT = r"d:\popwave-skills\skills\pop-fanqie-write\scripts\wordcount_check.py"

# ============ 读取skill文件（v7.2.0）============
SKILLS_BASE = r"d:\popwave-skills\skills"

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

# ============ 精选注入：按卷切分Phase1.5和Phase2 ============

def extract_volume_phase15(full_text, volume_num=1):
    """从Phase1.5全书剧情白描中提取指定卷的内容"""
    # 匹配 "# 深渊主宰 · 卷X剧情白描" 或 "# 深渊主宰·卷X·..."
    pattern = rf'# 深渊主宰\s*·\s*卷{volume_num}[^\n]*\n'
    match = re.search(pattern, full_text)
    if not match:
        return f"（卷{volume_num}剧情白描未找到）"

    start = match.start()
    # 找下一个卷标题
    next_pattern = r'# 深渊主宰\s*·\s*卷\d+[^\n]*\n'
    next_match = re.search(next_pattern, full_text[start + 1:])
    if next_match:
        end = start + 1 + next_match.start()
    else:
        end = len(full_text)

    return full_text[start:end].strip()


def extract_volume_phase2(full_text, volume_num=1):
    """从Phase2中提取指定卷的L2单元卡+卷纲"""
    # Phase2结构：先L2单元卡（### 第X卷：XXX），再卷纲（### 卷X · XXX）
    # 提取两部分

    # 1. 提取L2单元卡部分
    l2_pattern = rf'### 第{["一","二","三","四","五","六","七","八","九"][volume_num-1]}卷[^\n]*\n'
    l2_match = re.search(l2_pattern, full_text)
    l2_content = ""
    if l2_match:
        l2_start = l2_match.start()
        # 找下一个 ###
        next_l2 = re.search(r'### 第[一二三四五六七八九]卷[^\n]*\n', full_text[l2_start + 1:])
        if next_l2:
            l2_end = l2_start + 1 + next_l2.start()
        else:
            # 找 ## 2. 卷纲归纳
            next_section = re.search(r'## \d+\.\s', full_text[l2_start + 1:])
            l2_end = l2_start + 1 + next_section.start() if next_section else len(full_text)
        l2_content = full_text[l2_start:l2_end].strip()

    # 2. 提取卷纲部分
    outline_pattern = rf'### 卷{volume_num}\s*·[^\n]*\n'
    outline_match = re.search(outline_pattern, full_text)
    outline_content = ""
    if outline_match:
        outline_start = outline_match.start()
        # 找下一个 ### 卷X ·
        next_outline = re.search(r'### 卷\d+\s*·[^\n]*\n', full_text[outline_start + 1:])
        if next_outline:
            outline_end = outline_start + 1 + next_outline.start()
        else:
            # 找下一个 ## 
            next_section = re.search(r'## \d+\.\s', full_text[outline_start + 1:])
            outline_end = outline_start + 1 + next_section.start() if next_section else len(full_text)
        outline_content = full_text[outline_start:outline_end].strip()

    result = ""
    if l2_content:
        result += f"## L2单元卡（卷{volume_num}）\n\n{l2_content}\n\n"
    if outline_content:
        result += f"## 卷纲（卷{volume_num}）\n\n{outline_content}\n\n"
    if not result:
        result = f"（卷{volume_num}的Phase2内容未找到）"
    return result


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


# ============ 字数自检（集成wordcount_check.py）============

def run_wordcount_check(file_path):
    """调用wordcount_check.py裁剪"""
    if not os.path.exists(WORDCOUNT_SCRIPT):
        print(f"    ⚠️ 字数自检脚本不存在: {WORDCOUNT_SCRIPT}")
        return False, "脚本不存在"
    try:
        result = subprocess.run(
            ["python", WORDCOUNT_SCRIPT, file_path, "--auto"],
            capture_output=True, text=True, timeout=60, encoding="utf-8"
        )
        success = result.returncode == 0
        output = result.stdout + result.stderr
        return success, output[-500:] if len(output) > 500 else output
    except Exception as e:
        return False, str(e)


# ============ 加载拆书产出 ============

def load_decon_files():
    files = {}
    with open(PHASE15_PATH, "r", encoding="utf-8") as f:
        files["phase15_full"] = f.read()
    with open(PHASE2_PATH, "r", encoding="utf-8") as f:
        files["phase2_full"] = f.read()

    # 精选：只提取卷1的内容
    files["phase15_v1"] = extract_volume_phase15(files["phase15_full"], 1)
    files["phase2_v1"] = extract_volume_phase2(files["phase2_full"], 1)

    chapters = {}
    for i in range(1, MAX_CHAPTERS + 1):
        ch_num = f"ch{i:03d}"
        ch_path = os.path.join(CHAPTERS_DIR, f"{ch_num}.md")
        if os.path.exists(ch_path):
            with open(ch_path, "r", encoding="utf-8") as f:
                chapters[ch_num] = f.read()
    files["chapters"] = chapters

    return files


# ============ A组prompt构建（R33精选版）============

def build_prompt_a(decon_files, ch_num, prev_chapter):
    """A组：write v7.2.0 skill + 精选注入（只注入卷1）"""
    chapter_card = decon_files["chapters"].get(ch_num, "")

    if prev_chapter:
        prev_hint = "- **如非第一章，必须回收前章钩子**——本章前300字必须回收前章章末钩子\n- 前章正文已注入下方，用于回收钩子"
    else:
        prev_hint = "- 第一章使用黄金开篇：前3句扔炸弹，300字内完成冲突+主角+金手指+钩子"

    prompt = f"""# 任务

请按write skill v7.2.0全流程写本章（{ch_num}）正文。

5步SOP：
- Step 1: 加载燃料（**已精选注入卷1内容，非全书**）
- Step 2: 章型+技法锁定（**v7.2.0新增动作链+多感官优先级+章名设计**）
- Step 3: 写正文，2000-2500字，不准超过2500字
- Step 4: 篇幅硬限制检查+落盘（**集成字数自检脚本**）
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

# 卷1骨架+L2单元卡（Phase2精选卷1）

{decon_files['phase2_v1']}

---

# 卷1剧情白描（Phase1.5精选卷1，非全书）

{decon_files['phase15_v1']}

---

# 本章白描卡（{ch_num}）

{chapter_card}
"""
    if prev_chapter:
        prompt += f"\n\n---\n\n# 前一章正文（用于回收钩子）\n\n{prev_chapter}\n"
    return prompt


# ============ 主流程 ============

def run_group(decon_files, output_subdir):
    """跑5章串联，每章写完调字数自检"""
    print(f"\n[A组 write v7.2.0 精选注入+字数自检] 开始跑5章串联...")
    results = []
    prev_chapter = None

    for ch_idx in range(1, MAX_CHAPTERS + 1):
        ch_num = f"ch{ch_idx:03d}"

        if ch_num not in decon_files["chapters"]:
            print(f"  [{ch_idx}/5] {ch_num} 白描卡不存在，跳过")
            continue

        user_prompt = build_prompt_a(decon_files, ch_num, prev_chapter)
        prompt_len = len(user_prompt)
        print(f"  [{ch_idx}/5] {ch_num} 调用DeepSeek... (prompt: {prompt_len}字符)")

        try:
            content, usage, elapsed = call_ds(
                WRITE_SYSTEM_V72, user_prompt, max_tokens=8000, label=f"R33_A_{ch_num}"
            )
            out_path = os.path.join(output_subdir, f"{ch_num}.md")
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(content)
            tokens = usage.get('total_tokens', 0)
            pre_check_len = len(content)
            print(f"    完成! {elapsed:.1f}s | {pre_check_len}字 | tokens:{tokens}")

            # 字数自检
            print(f"    [字数自检] 调用wordcount_check.py...")
            check_ok, check_output = run_wordcount_check(out_path)
            with open(out_path, "r", encoding="utf-8") as f:
                post_check_content = f.read()
            post_check_len = len(post_check_content)
            if pre_check_len != post_check_len:
                print(f"    [字数自检] 裁剪: {pre_check_len}→{post_check_len}字")
            else:
                print(f"    [字数自检] 无需裁剪")

            results.append({
                "ch_num": ch_num,
                "prompt_length": prompt_len,
                "pre_check_length": pre_check_len,
                "post_check_length": post_check_len,
                "elapsed": round(elapsed, 1),
                "tokens": tokens,
                "path": out_path,
                "wordcount_check": "裁剪" if pre_check_len != post_check_len else "无变化"
            })
            prev_chapter = post_check_content

        except Exception as e:
            print(f"    {ch_num}失败: {e}")
            import traceback
            traceback.print_exc()
            results.append({"ch_num": ch_num, "error": str(e)})
            prev_chapter = None

    return results


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("=" * 60)
    print("R33测试: 模拟真正的write skill执行流程")
    print("精选注入(只注入卷1) + 字数自检(wordcount_check.py)")
    print("=" * 60)

    print(f"\n[0] 加载拆书产出...")
    decon_files = load_decon_files()
    print(f"  Phase1.5全书: {len(decon_files['phase15_full'])}字")
    print(f"  Phase1.5卷1精选: {len(decon_files['phase15_v1'])}字")
    print(f"  Phase2全书: {len(decon_files['phase2_full'])}字")
    print(f"  Phase2卷1精选: {len(decon_files['phase2_v1'])}字")
    print(f"  白描卡: {len(decon_files['chapters'])}章")
    print(f"  精选设定库: {len(CURATED_SETTINGS)}字")
    print(f"  字数自检脚本: {os.path.exists(WORDCOUNT_SCRIPT)}")

    # A组
    a_output = os.path.join(OUTPUT_DIR, "A-write-v720-curated")
    os.makedirs(a_output, exist_ok=True)
    a_results = run_group(decon_files, a_output)

    # 汇总
    print(f"\n{'='*60}")
    print("R33测试完成！")
    print(f"{'='*60}")

    print(f"\n[A组 write v7.2.0 精选注入+字数自检]")
    print(f"{'章号':<10} {'输入字数':<10} {'裁剪前':<10} {'裁剪后':<10} {'耗时':<8} {'tokens':<10} {'自检'}")
    print("-" * 80)
    for r in a_results:
        if "error" in r:
            print(f"{r.get('ch_num','?'):<10} 失败: {r['error']}")
        else:
            print(f"{r['ch_num']:<10} {r['prompt_length']:<10} {r['pre_check_length']:<10} {r['post_check_length']:<10} {r['elapsed']:<8} {r['tokens']:<10} {r['wordcount_check']}")

    # 保存meta
    meta = {
        "config": {
            "model": DS_MODEL,
            "temperature": TEMPERATURE,
            "chapters": MAX_CHAPTERS,
            "input": "深渊主宰C方案（精选注入卷1+字数自检）",
            "A_version": "write v7.2.0（精选注入+字数自检）",
            "vs_R32": "R32全量注入47427字 vs R33精选注入约5000字"
        },
        "A_write_v720_curated": a_results
    }
    meta_path = os.path.join(OUTPUT_DIR, "r33-meta.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    print(f"\n输出目录: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
