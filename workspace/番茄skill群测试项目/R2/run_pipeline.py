#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
番茄R2测试管线 - seed(含燃料注入) → plot → write(3章) → review(3章)
与R1唯一区别：seed阶段注入创意基因库+防雷池
"""
import os, re, json, requests, time, sys

API_KEY = "sk-5a3654e4aa2e4eefa08abe3d0e0231f5"
BASE_URL = "https://api.deepseek.com/v1"
MODEL = "deepseek-v4-flash"

TEST_DIR = r"D:\workspace\番茄skill群测试项目\R2"
SKILL_DIR = r"D:\workspace\skills"
FUEL_DIR = r"D:\workspace\番茄skill群测试项目\燃料库"
PROMPTS_DIR = os.path.join(TEST_DIR, "prompts")
RESPONSES_DIR = os.path.join(TEST_DIR, "responses")
OUTPUT_DIR = os.path.join(TEST_DIR, "产出")

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def call_api(system_prompt, user_prompt, task_name):
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 16000,
        "stream": False
    }
    print(f"  调用API [{task_name}]...")
    print(f"  System: {len(system_prompt)}字符 | User: {len(user_prompt)}字符")
    start = time.time()
    response = requests.post(f"{BASE_URL}/chat/completions", headers=headers, json=payload, timeout=300)
    response.raise_for_status()
    result = response.json()
    content = result["choices"][0]["message"]["content"]
    usage = result.get("usage", {})
    elapsed = time.time() - start
    
    write_file(os.path.join(RESPONSES_DIR, f"{task_name}-output.txt"), content)
    write_file(os.path.join(RESPONSES_DIR, f"{task_name}-meta.json"), json.dumps({
        "task": task_name, "content_length": len(content),
        "usage": usage, "elapsed": round(elapsed, 1)
    }, ensure_ascii=False, indent=2))
    write_file(os.path.join(PROMPTS_DIR, f"{task_name}-system-prompt.txt"), system_prompt)
    write_file(os.path.join(PROMPTS_DIR, f"{task_name}-user-prompt.txt"), user_prompt)
    
    print(f"  完成! {elapsed:.1f}s | 输出{len(content)}字 | tokens:{usage.get('total_tokens','N/A')}")
    return content, usage, elapsed

# ============================================================
# Phase 1: fanqie-seed → 概念种子文档（注入燃料库+防雷池）
# ============================================================
def run_seed():
    print("\n" + "="*60)
    print("Phase 1: fanqie-seed → 概念种子文档（含燃料注入）")
    print("="*60)
    
    system_prompt = read_file(os.path.join(SKILL_DIR, "fanqie-seed", "SKILL.md"))
    
    # 读取燃料库
    gene_library = read_file(os.path.join(FUEL_DIR, "创意基因库.md"))
    anti_pool = read_file(os.path.join(FUEL_DIR, "已知概念防雷池.md"))
    
    user_prompt = f"""## 创意基因库（20本番茄Top20的5维度基因卡，用于交叉授粉）
{gene_library}

## 已知概念防雷池（20本核心概念一句话摘要，你的概念必须与这些全部不同）
{anti_pool}

## 任务
请基于以下**已确定的概念核心机制**，围绕它展开完整的概念种子文档。

### 概念核心机制（已锁定，不可更改）

**每天0点，随机获得一个完整可用的天赋，品质随机（灰/白/绿/蓝/紫/橙/红，DNF色阶），拿到就能用。**

**升级规则**：同色×3 = 升一级色（3灰→1白，3白→1绿，以此类推）
**槽位制**（替代重置）：
- 开局1个天赋槽位
- 后续槽位随故事推进解锁（第2槽~ch10，第3槽~ch30，第4槽~ch50，第5槽~ch80，第6槽~ch100）
- 槽位满了时新天赋覆盖旧天赋（旧天赋消失），或放弃新天赋保留旧的——每天的"赌与不赌"
**品质概率参考**：灰50%/白25%/绿15%/蓝7%/紫2%/橙0.9%/红0.1%

**限制条件**（保留张力）：
1. 每天随机品质——不知道今天是灰色还是红色（赌徒心理）
2. 槽位有限——必须做取舍（策略深度）
3. 同色才能升级——灰色太多也有用（保底机制）
4. 天赋类型随机——可能来一个用不上的天赋（适配性问题）
5. 天赋不可拆卸只可覆盖——换掉就没了（沉没成本）

### 爽感节奏要求（数学建模已验证）
- ch1：拿到第一个天赋，立刻能用 → 前300字出概念+首爽
- ch2-3：第二个天赋来了但槽位只有1个，换不换？→ 决策困境
- ch4-6：凑齐3灰合成白色，升级爽感 → 每3章1高潮
- ch7-10：解锁第2槽位，双天赋组合 → 概念进化
- ch15-20：可能直接抽到蓝色天赋！→ 随机惊喜爆发

要求：
1. 概念必须通过防雷池验证——与已知20本核心概念逐一比对，确认差异性
2. 概念必须适合番茄男频，12岁小学生能3秒理解
3. 不要起点式预设世界——最小世界≤5条规则
4. 角色为概念服务，不先建人物再推故事
5. 100章场景推导必须体现槽位解锁和色阶升级的节奏

请完整输出概念种子文档，包含以下7个部分：
1. 概念定义（一句话+矛盾+画面+灵感来源+防雷验证）
2. 概念生成机制（核心机制+生成模式+进化路径+限制条件）
3. 100章场景推导（3阶段：1-30展示期/31-70进化期/71-100爆发期，每章1句，标注槽位解锁节点）
4. 最小世界规则（≤5条）
5. 兑现者设计（主角+2-3配角）
6. 番茄节奏框架
7. 笔触风格"""
    
    content, _, _ = call_api(system_prompt, user_prompt, "fanqie-seed")
    
    output_path = os.path.join(OUTPUT_DIR, "概念种子文档.md")
    write_file(output_path, content)
    print(f"  已保存: {output_path}")
    return content

# ============================================================
# Phase 2: fanqie-plot → 场景卡（前5章）
# ============================================================
def run_plot(seed_content):
    print("\n" + "="*60)
    print("Phase 2: fanqie-plot → 场景卡（前5章）")
    print("="*60)
    
    system_prompt = read_file(os.path.join(SKILL_DIR, "fanqie-plot", "SKILL.md"))
    chapter_types = read_file(os.path.join(SKILL_DIR, "fanqie-write", "references", "章型定义.md"))
    system_prompt += "\n\n---\n\n# 附录：章型定义\n\n" + chapter_types
    
    user_prompt = f"""## 概念种子文档
{seed_content}

## 任务
请基于以上概念种子文档，生成前5章的场景卡。

要求：
1. 从100章推导中选取前5章的概念变体
2. 每章场景卡≤500字
3. 严格执行番茄节奏红线7条
4. ch1必须是opening_shift章型（概念首次展示）
5. 前5章至少1章是combat_reversal
6. 不得连续2章同章型
7. 每章必须标注：概念变体、核心爽点、爽点触发位、钩子、节奏约束、边界、前章衔接、章型

请输出5张场景卡，格式如下：
## ch001 · 章名
概念变体：V0XX - 描述
核心爽点：类型
爽点触发位：位置
钩子：1句话
节奏约束：事件密度X/概念交互≥X次/前300字出冲突
边界：写到哪停/不能碰什么
前章衔接：无（第一章）
章型：opening_shift

## ch002 · 章名
...（同上格式）"""
    
    content, _, _ = call_api(system_prompt, user_prompt, "fanqie-plot-batch1")
    
    output_path = os.path.join(OUTPUT_DIR, "场景卡", "场景卡-batch1.md")
    write_file(output_path, content)
    print(f"  已保存: {output_path}")
    return content

# ============================================================
# Phase 3: fanqie-write → 正文（逐章，3章）
# ============================================================
def parse_scene_cards(plot_content):
    cards = {}
    pattern = r'## (ch\d{3})[^\n]*'
    headers = list(re.finditer(pattern, plot_content))
    for i, h in enumerate(headers):
        ch_id = h.group(1)
        start = h.start()
        end = headers[i+1].start() if i+1 < len(headers) else len(plot_content)
        cards[ch_id] = plot_content[start:end].strip()
    return cards

def get_prev_ending(ch_num, output_dir):
    if ch_num == 1:
        return "本作第一章，无前章结尾。"
    prev_file = os.path.join(output_dir, "正文", f"ch{ch_num-1:03d}.md")
    if not os.path.exists(prev_file):
        return f"前一章(ch{ch_num-1:03d})未找到。"
    content = read_file(prev_file)
    report_idx = content.find("## 执行报告")
    if report_idx > 0:
        content = content[:report_idx]
    content = content.strip()
    return content[-800:] if len(content) > 800 else content

def run_write(seed_content, plot_content, num_chapters=3):
    print("\n" + "="*60)
    print(f"Phase 3: fanqie-write → 正文（{num_chapters}章）")
    print("="*60)
    
    skill_md = read_file(os.path.join(SKILL_DIR, "fanqie-write", "SKILL.md"))
    chapter_types = read_file(os.path.join(SKILL_DIR, "fanqie-write", "references", "章型定义.md"))
    system_prompt = skill_md + "\n\n---\n\n# 附录：章型定义\n\n" + chapter_types
    
    scene_cards = parse_scene_cards(plot_content)
    print(f"  解析到 {len(scene_cards)} 张场景卡: {list(scene_cards.keys())}")
    
    snapshot = "## 事实快照\n\n### 概念状态\n- 当前概念阶段：初始\n- 已使用变体：无\n\n### 角色状态\n- 主角：初始状态\n\n### 世界状态\n- 已揭示世界规则：无\n\n### 已确立事实\n（空）\n\n### 待确认偏离\n（无）"
    snapshot_path = os.path.join(OUTPUT_DIR, "事实快照.md")
    write_file(snapshot_path, snapshot)
    
    for i in range(1, num_chapters + 1):
        ch_id = f"ch{i:03d}"
        print(f"\n  [{ch_id}] ({i}/{num_chapters})")
        
        if ch_id not in scene_cards:
            print(f"    跳过：找不到 {ch_id} 的场景卡")
            continue
        
        scene_card = scene_cards[ch_id]
        prev_ending = get_prev_ending(i, OUTPUT_DIR)
        
        user_prompt = f"""## 权威设定区

### 概念种子文档
{seed_content}

### 本章场景卡
{scene_card}

### 事实快照（当前状态）
{snapshot}

## AI生成参考区

### 前章结尾（约800字）
{prev_ending}

## 写作要求

1. 篇幅：3000-5000中文字（不含执行报告）
2. 章型执行：按场景卡和章型定义的7节拍推进
3. 概念兑现：本章概念变体必须在正文中可见且推动剧情
4. 节奏物理量：事件间隔≤20行/感官≤3行/情绪≤2行/事件密度8-12个/爽感≥1个
5. 前300字必须出冲突或概念展示
6. 对话引导词只用"道"
7. 爽感公式：压力→突破/弱→强/未知→揭示/被欺→反击（每章≥1个且有爆发感）
8. 12岁读者模型：每30秒需新内容，连续3次纯氛围则退出

输出格式：直接输出正文（以章名开头），正文结束后用"---"分隔，附"## 执行报告"（微观技法选择卡+验收检查表8维度）"""
        
        content, _, elapsed = call_api(system_prompt, user_prompt, f"fanqie-write-{ch_id}")
        
        output_path = os.path.join(OUTPUT_DIR, "正文", f"{ch_id}.md")
        write_file(output_path, content)
        print(f"    已保存: {output_path}")
        
        snapshot = update_snapshot(ch_id, content, snapshot)
        write_file(snapshot_path, snapshot)
        print(f"    事实快照已更新")
    
    return num_chapters

def update_snapshot(ch_id, content, snapshot):
    new_facts = f"\n### {ch_id} 结束时\n- 正文字数: {len(content)}\n"
    gold = re.findall(r'金币[+\-]*(\d+)', content)
    exp = re.findall(r'经验[值]*[+\-]*(\d+)', content)
    level = re.findall(r'等级[提升到]*?(\d+)', content)
    if gold: new_facts += f"- 金币: {gold}\n"
    if exp: new_facts += f"- 经验: {exp}\n"
    if level: new_facts += f"- 等级: {level}\n"
    
    if "## 已确立事实" in snapshot:
        snapshot = snapshot.replace("## 已确立事实", new_facts + "\n## 已确立事实")
    else:
        snapshot += "\n" + new_facts
    return snapshot

# ============================================================
# Phase 4: fanqie-review → 审核（逐章）
# ============================================================
def run_review(seed_content, plot_content, num_chapters=3):
    print("\n" + "="*60)
    print(f"Phase 4: fanqie-review → 审核（{num_chapters}章）")
    print("="*60)
    
    system_prompt = read_file(os.path.join(SKILL_DIR, "fanqie-review", "SKILL.md"))
    scene_cards = parse_scene_cards(plot_content)
    
    for i in range(1, num_chapters + 1):
        ch_id = f"ch{i:03d}"
        print(f"\n  [审核 {ch_id}] ({i}/{num_chapters})")
        
        ch_file = os.path.join(OUTPUT_DIR, "正文", f"{ch_id}.md")
        if not os.path.exists(ch_file):
            print(f"    跳过：找不到 {ch_id} 的正文")
            continue
        
        ch_content = read_file(ch_file)
        scene_card = scene_cards.get(ch_id, "场景卡未找到")
        
        user_prompt = f"""## 概念种子文档
{seed_content}

## 本章场景卡
{scene_card}

## 本章正文
{ch_content}

## 任务
请审核本章正文：
1. 概念兑现度检查（5维度评分，<60%不合格）
2. 番茄节奏检查（9项检查表）
3. 快照更新
4. 下章建议"""
        
        content, _, _ = call_api(system_prompt, user_prompt, f"fanqie-review-{ch_id}")
        
        output_path = os.path.join(OUTPUT_DIR, "审核", f"审核-{ch_id}.md")
        write_file(output_path, content)
        print(f"    已保存: {output_path}")

# ============================================================
# Main
# ============================================================
def main():
    os.makedirs(PROMPTS_DIR, exist_ok=True)
    os.makedirs(RESPONSES_DIR, exist_ok=True)
    
    total_start = time.time()
    
    print("="*60)
    print("番茄R2测试管线 - seed(含燃料) → plot → write(3章) → review(3章)")
    print("="*60)
    
    seed_content = run_seed()
    plot_content = run_plot(seed_content)
    num_chapters = run_write(seed_content, plot_content, num_chapters=3)
    run_review(seed_content, plot_content, num_chapters=num_chapters)
    
    total_elapsed = time.time() - total_start
    print(f"\n{'='*60}")
    print(f"番茄R2测试完成!")
    print(f"  总耗时: {total_elapsed/60:.1f}分钟")
    print(f"  产出目录: {OUTPUT_DIR}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
