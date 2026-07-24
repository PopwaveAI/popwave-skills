#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
起点skill群 R1 全链路测试
验证三层骨架重构后的起点skill群组（pipeline v1.1.0 + seed v8.1.0 + world v2.0.0 + character v1.0.0 + plot v4.0.0 + write v3.0.0 + review v3.0.0）

链路：seed骨架层(1d+1e+1f) → seed主角层(2a+2b+2c) → world(消费骨架) → character(消费骨架) → plot(四层结构) → write(ch001黄金首章) → review(四维审核)

API: DeepSeek deepseek-v4-flash
"""

import os, sys, json, time, requests, traceback

# ============ API配置 ============
DS_API_KEY = "sk-5a3654e4aa2e4eefa08abe3d0e0231f5"
DS_BASE_URL = "https://api.deepseek.com/v1"
DS_MODEL = "deepseek-v4-flash"
PROXIES = {"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"}
TIMEOUT = 600

# ============ 路径配置 ============
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUTS_DIR = os.path.join(SCRIPT_DIR, "inputs")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")
SKILLS_BASE = r"d:\popwave-skills\skills"

# ============ 工具函数 ============
def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def read_skill(skill_name, files):
    """读取skill的SKILL.md+指定step文件，拼成system prompt"""
    parts = []
    for f in files:
        path = os.path.join(SKILLS_BASE, skill_name, f)
        if os.path.exists(path):
            parts.append(read_file(path))
        else:
            print(f"  [警告] 文件不存在: {path}")
    return "\n\n---\n\n".join(parts)

def call_ds(system_prompt, user_prompt, max_tokens=12000, temperature=0.85):
    """调用DeepSeek API"""
    url = f"{DS_BASE_URL}/chat/completions"
    headers = {"Authorization": f"Bearer {DS_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": DS_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": False
    }
    start = time.time()
    for attempt in range(3):
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=TIMEOUT, proxies=PROXIES)
            response.raise_for_status()
            elapsed = time.time() - start
            result = response.json()
            return result["choices"][0]["message"]["content"], result.get("usage", {}), elapsed
        except Exception as e:
            print(f"  第{attempt+1}次失败: {type(e).__name__}: {str(e)[:100]}")
            if attempt < 2:
                time.sleep(8)
    return None, {}, 0

def save_io(name, system_prompt, user_prompt, output, usage, elapsed):
    """落盘input+output+meta"""
    # input
    input_content = f"# SYSTEM PROMPT\n\n{system_prompt}\n\n---\n\n# USER PROMPT\n\n{user_prompt}"
    with open(os.path.join(INPUTS_DIR, f"{name}_input.md"), "w", encoding="utf-8") as f:
        f.write(input_content)
    # output
    with open(os.path.join(OUTPUT_DIR, f"{name}.md"), "w", encoding="utf-8") as f:
        f.write(output if output else "[API调用失败]")
    # meta
    meta = {
        "name": name,
        "model": DS_MODEL,
        "output_length": len(output) if output else 0,
        "elapsed": round(elapsed, 1),
        "usage": usage,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    return meta

# ============ 测试用例输入 ============
TRACK = "仙侠修真"
USER_INTENT = """赛道方向：仙侠修真
参考书：深渊主宰（D&D数据面板流派，已有decon-lite拆书）
情绪基调：暗黑复仇+热血逆袭
全书最大卖点：数据面板×修仙体系的跨界融合，杀戮经验驱动修炼
现有设定：无（全新项目）
"""

# ============ Phase 1: seed 骨架层 ============
def run_phase1_skeleton():
    """Phase 1 Step 1d+1e+1f: 力量体系设计+动力引擎设计+骨架自洽"""
    print("\n" + "=" * 60)
    print("Phase 1: seed 骨架层（力量体系+动力引擎+骨架自洽）")
    print("=" * 60)

    system = read_skill("pop-qidian-seed", ["SKILL.md", "steps/phase1-skeleton.md"])

    user = f"""# 任务

按起点seed v8.1.0 Phase 1骨架层SOP，基于以下输入，设计三层骨架。

## 输入
{USER_INTENT}

## 执行步骤

### Step 1d: 力量体系设计（坐标系）
设计广义化阶层金字塔，四层结构：
1. 世界源力量（力量从哪来，和世界观挂钩）
2. 主养成线（5-7个阶位，每个有文化渊源+社会地位参照）
3. 子养成线（≥2条，每条有自身阶位+和主养成线挂钩）
4. 交叉规则（子养成线之间的协同/制约）

注意：这是仙侠修真赛道，但力量体系不限于传统修仙境界——可以是社会地位金字塔、术法品质坐标系等广义坐标系。选择最能支撑"数据面板×修仙"融合的坐标系形态。

### Step 1e: 动力引擎设计（众生攀登系统）
设计六组成：
1. 驱动逻辑（众生为什么爬——世界级驱动力）
2. 运转机制（输入→转化→输出→反馈的闭环——全员通用）
3. 众生攀登方式分层（有资源/没资源/爬到顶/掉下来的人分别怎么爬）
4. 代价结构（通用代价+群体差异代价+累积效应）
5. 范式归类（飞轮型/探索型/混合型/压迫型/对抗型，选一种并说明原因）
6. 演化节点（长篇中引擎是否演化+何时演化+触发事件）

### Step 1f: 骨架自洽检查
逐项检查8项自洽条件，给出通过/不通过结论。

## 产出格式
按骨架.md的落盘格式输出，包含：
- 力量体系（坐标系）四层结构
- 动力引擎（众生攀登系统）六组成
- 骨架自洽检查结论

## 参考（decon-lite表1+表9摘要，来自深渊主宰拆书）
力量体系参考：D&D面板系——主养成线=职业等级(1-20级)，子养成线=属性值(力敏体质感魅智)+技能点+专长，交叉规则=属性值决定技能上限+专长解锁条件
动力引擎参考：杀戮飞轮型——驱动逻辑=诸神黄昏危机下弱肉强食，运转机制=杀戮→经验→升级→更强杀戮，代价=杀戮吸引更高阶敌人+精神侵蚀

直接输出骨架.md完整内容，不要写思考过程。
"""
    output, usage, elapsed = call_ds(system, user, max_tokens=12000, temperature=0.75)
    meta = save_io("phase1-骨架", system, user, output, usage, elapsed)
    if output:
        print(f"  完成! {elapsed:.1f}s | {len(output)}字符 | tokens:{usage.get('total_tokens', 0)}")
    return output

# ============ Phase 2: seed 主角层 ============
def run_phase2_protagonist(skeleton_md):
    """Phase 2 Step 2a+2b+2c: 主角设计+金手指设计+爽感矛盾设计"""
    print("\n" + "=" * 60)
    print("Phase 2: seed 主角层（主角+金手指+爽感矛盾）")
    print("=" * 60)

    system = read_skill("pop-qidian-seed", ["SKILL.md", "steps/phase2-protagonist.md"])

    user = f"""# 任务

按起点seed v8.1.0 Phase 2主角层SOP，基于以下骨架，设计主角层。

## 输入：骨架.md
{skeleton_md}

## 执行步骤

### Step 2a: 主角设计
- 坐标系起点位置（在力量体系中的起点阶位+社会地位）
- 身份底色（社会角色+核心特质）
- 性格特质（3-5个标签+行为表现）
- 核心欲望（与骨架.md动力引擎驱动逻辑对齐——主角欲望是世界级驱动力的个人化表达）
- 与众生关系（在众生攀登方式分层中属于哪类群体）
- 9字段行为模式表（表层欲望/深层需要/恐惧/底线/行动偏好/第一章主动动作/决策缺陷/第一卷变化/长篇穿透方式）

### Step 2b: 金手指设计
- 金手指类型
- 加速机制（如何合理化加速主角跨越坐标系——主角攀登方式与众生相同但金手指让他快）
- 限制（**必须显性声明"不能取消坐标系本身的意义"**）
- 代价（使用金手指要付出什么——制造爽感矛盾）
- 与引擎关系（金手指是引擎运转机制的加速器，不是引擎本身）
- 梗×机制×限制公式验证
- 喧宾夺主检查（金手指是否让坐标系失去意义？）

### Step 2c: 爽感矛盾设计
- 爽感矛盾公式：坐标系门槛×天赋加速×代价约束=爽感强度
- 爽感闭环模板：触发→爆发→后果
- 爽感类型清单（至少选2种：压力→突破/弱→强/未知→揭示/被欺→反击）
- 爽感节奏建议（每章≥1个闭环，每3-5章1个小爽点，每幕1个大爽点）

## 产出格式
按主角设计.md的格式输出，包含2a+2b+2c三部分完整内容。

直接输出主角设计.md完整内容，不要写思考过程。
"""
    output, usage, elapsed = call_ds(system, user, max_tokens=12000, temperature=0.75)
    meta = save_io("phase2-主角设计", system, user, output, usage, elapsed)
    if output:
        print(f"  完成! {elapsed:.1f}s | {len(output)}字符 | tokens:{usage.get('total_tokens', 0)}")
    return output

# ============ Phase 1续: seed 创意发散+故事纲领+黄金首章 ============
def run_phase1_creative(skeleton_md, protagonist_md):
    """Phase 1 Step 1g+1h+1i: 双轨发散+故事纲领+黄金首章"""
    print("\n" + "=" * 60)
    print("Phase 1续: seed 创意发散+故事纲领+黄金首章")
    print("=" * 60)

    system = read_skill("pop-qidian-seed", [
        "SKILL.md",
        "steps/phase1-diverge.md",
        "steps/phase1-story-brief.md",
        "steps/phase1-first-chapter.md"
    ])

    user = f"""# 任务

按起点seed v8.1.0 SOP，基于已定稿的骨架和主角设计，执行创意发散+故事纲领+黄金首章。

## 输入

### 骨架.md
{skeleton_md}

### 主角设计.md
{protagonist_md}

## 执行步骤

### Step 1g: 双轨发散
在骨架框架内发散创意：
- 王道轨3个（仙侠修真赛道主流模式融合）
- 猎奇轨2个（跨领域碰撞）
每个创意用三眼法判断（画面/限制/场景），推荐1个。

### Step 1h: 故事纲领
对选定创意产出故事纲领，必须用三核心+营销层格式：
- 三核心：什么样的世界（4层，引用骨架.md）+ 什么样的舞台·世界危机（3要素）+ 什么样的主角（5要素，引用主角设计.md）
- 营销层：最大钩子（≤20字）+ 即时兑现感

### Step 1i: 黄金首章
写ch001黄金首章，2000-2500字：
- 从第1句开始有冲击力
- 首章必须体现骨架（坐标系展示——让读者感知力量体系的阶层金字塔）
- 首章必须体现金手指激活（但不能喧宾夺主）
- 首章必须有冲突
- 章末钩子（主角主动决策型）

## 产出格式
1. 双轨发散5个创意+推荐1个
2. 故事纲领（三核心+营销层）
3. ch001黄金首章正文（2000-2500字）

直接输出，不要写思考过程。
"""
    output, usage, elapsed = call_ds(system, user, max_tokens=16000, temperature=0.85)
    meta = save_io("phase1-创意首章", system, user, output, usage, elapsed)
    if output:
        print(f"  完成! {elapsed:.1f}s | {len(output)}字符 | tokens:{usage.get('total_tokens', 0)}")
    return output

# ============ Phase 3: world（消费骨架生长血肉） ============
def run_phase3_world(skeleton_md, protagonist_md, creative_md):
    """Phase 3: world消费骨架生长地图/势力/全书设定"""
    print("\n" + "=" * 60)
    print("Phase 3: world 消费骨架生长血肉")
    print("=" * 60)

    system = read_skill("pop-qidian-world", ["SKILL.md"])

    user = f"""# 任务

按起点world v2.0.0 SOP，消费骨架.md（第一优先）+主角设计.md+创意，生长血肉层。

## 输入

### 骨架.md（第一优先输入——world不自行发明力量体系和动力引擎）
{skeleton_md}

### 主角设计.md
{protagonist_md}

### 创意+首章摘要
{creative_md[:3000]}

## 执行步骤

### Step 2c: 地图设计
设计MMO式地图，空间分布必须映射坐标系（骨架.md的力量体系），空间法则由力量体系决定。

### Step 2d: 势力设计
设计势力，必须从众生攀登方式差异生长（骨架.md动力引擎组成3），每个势力标注对应的攀登方式类型。

### Step 2e: 危机设计
设计危机，必须与动力引擎驱动逻辑对齐（骨架.md），危机是引擎运转的阻力表现。

### Step 3: 全书设定（精简版——仅第一卷）
产出第一卷的设定切片：
- 第一卷坐标系位置变化区间
- 第一卷引擎状态+演化节点
- 第一卷势力格局
- 第一卷主要区域地图

## 产出格式
按world v2.0.0落盘格式输出：
- 地图.md（第一卷区域）
- 势力.md（第一卷势力，每个标注攀登方式类型）
- 危机.md（第一卷危机）
- 各卷切片.md（仅第一卷）

直接输出，不要写思考过程。
"""
    output, usage, elapsed = call_ds(system, user, max_tokens=12000, temperature=0.75)
    meta = save_io("phase3-world", system, user, output, usage, elapsed)
    if output:
        print(f"  完成! {elapsed:.1f}s | {len(output)}字符 | tokens:{usage.get('total_tokens', 0)}")
    return output

# ============ Phase 3.5: character（建角色库） ============
def run_phase3_5_character(skeleton_md, protagonist_md, world_md):
    """Phase 3.5: character建角色库"""
    print("\n" + "=" * 60)
    print("Phase 3.5: character 建角色库")
    print("=" * 60)

    system = read_skill("pop-qidian-character", ["SKILL.md", "steps/step2.md"])

    user = f"""# 任务

按起点character v1.0.0 SOP，基于骨架+主角设计+world产出，建角色库。

## 输入

### 骨架.md（动力引擎组成3——众生攀登方式分层）
{skeleton_md[:4000]}

### 主角设计.md
{protagonist_md[:4000]}

### world产出摘要
{world_md[:4000]}

## 执行步骤

按分幕设计出场角色清单建角色库（第一卷前5章出场角色）：
- 主角深度卡（从主角设计.md提取）
- 配角池（第一卷前5章出场的具名配角，每个标注攀登方式类型+等级坐标）
- 反派卡（第一卷敌人，标注攀登方式类型+等级坐标）

每个角色卡字段：姓名/攀登方式类型/等级坐标/性格(3-5标签+行为表现)/小传(200字)/口头禅/成长数据/出场记录

## 产出格式
角色库.md（角色总表+角色详细卡）

直接输出，不要写思考过程。
"""
    output, usage, elapsed = call_ds(system, user, max_tokens=12000, temperature=0.75)
    meta = save_io("phase3.5-character", system, user, output, usage, elapsed)
    if output:
        print(f"  完成! {elapsed:.1f}s | {len(output)}字符 | tokens:{usage.get('total_tokens', 0)}")
    return output

# ============ Phase 4: plot（剧情白描） ============
def run_phase4_plot(skeleton_md, protagonist_md, world_md, character_md):
    """Phase 4: plot四层结构剧情白描"""
    print("\n" + "=" * 60)
    print("Phase 4: plot 剧情白描（四层结构）")
    print("=" * 60)

    system = read_skill("pop-qidian-plot", ["SKILL.md"])

    user = f"""# 任务

按起点plot v4.0.0 SOP，消费骨架+主角设计+world+角色库，产出第一卷前5章剧情白描。

## 输入

### 骨架.md
{skeleton_md[:3000]}

### 主角设计.md（含爽感矛盾公式）
{protagonist_md[:3000]}

### world产出摘要
{world_md[:3000]}

### 角色库摘要
{character_md[:3000]}

## 执行步骤

### 2a: 本卷设定快照
圈出第一卷设定，标注：坐标系位置变化区间+引擎状态+演化节点

### 2b: 分支剧情线
≥6条（主线1~2+支线3~4+暗线1~2），每条标注对应的众生攀登方式

### 2c: 分幕设计
第一卷前5章作为第一幕，标注：
- 每幕困难来源三层面（坐标系阻力+引擎代价+天赋限制）
- 出场角色清单

### 2d: 按幕白描
第一幕前5章的剧情白描（1版直出800-2000字），每章标注：
- 场景表爽感闭环（引用主角设计.md的爽感矛盾公式）
- 爽感因子标注（坐标系门槛/天赋加速/代价约束中的哪个组合）
- 章末钩子（主角主动决策型，与坐标系跃迁或引擎演化相关）

## 产出格式
1. 本卷设定快照
2. 分支剧情线≥6条
3. 第一幕分幕设计（含困难三层面）
4. 前五章剧情白描（含场景表+爽感因子+章末钩子）

直接输出，不要写思考过程。
"""
    output, usage, elapsed = call_ds(system, user, max_tokens=16000, temperature=0.80)
    meta = save_io("phase4-plot", system, user, output, usage, elapsed)
    if output:
        print(f"  完成! {elapsed:.1f}s | {len(output)}字符 | tokens:{usage.get('total_tokens', 0)}")
    return output

# ============ Phase 5: write（ch001黄金首章——由plot驱动） ============
def run_phase5_write(skeleton_md, protagonist_md, plot_md, character_md):
    """Phase 5: write写ch001正文"""
    print("\n" + "=" * 60)
    print("Phase 5: write ch001正文")
    print("=" * 60)

    system = read_skill("pop-qidian-write", ["SKILL.md"])

    user = f"""# 任务

按起点write v3.0.0 SOP，基于剧情白描+角色库+主角设计，写ch001正文。

## 输入

### 主角设计.md（含爽感矛盾公式）
{protagonist_md[:3000]}

### 角色库摘要
{character_md[:3000]}

### 剧情白描ch001段
{plot_md[:5000]}

## 执行步骤

### Step 1: 加载
- 加载主角设计.md（爽感矛盾公式：坐标系门槛×天赋加速×代价约束）
- 加载角色库.md（角色唯一源）
- 加载剧情白描ch001段

### Step 2: 设定库精选注入
- 力量体系（坐标系）维度（≤500字）
- 角色库维度（本章出场角色卡，必选）
- 总计≤1500字

### Step 3: 选章型
ch001 = opening_shift（黄金开篇）

### Step 5: 写正文
- 2000-2500字硬限制
- 爽感锚定"跨越坐标系的瞬间"——爆发时刻体现天赋加速vs代价约束的张力
- 每章爽感爆发必须锚定坐标系位置跃迁

### Step 6: 验收
- 字数2000-2500
- 角色库一致性（出场角色在角色库中）
- 爽感锚定坐标系跃迁

## 产出格式
ch001正文（2000-2500字）+ 交付面板

直接输出正文+交付面板，不要写思考过程。
"""
    output, usage, elapsed = call_ds(system, user, max_tokens=8000, temperature=0.85)
    meta = save_io("phase5-write-ch001", system, user, output, usage, elapsed)
    if output:
        print(f"  完成! {elapsed:.1f}s | {len(output)}字符 | tokens:{usage.get('total_tokens', 0)}")
    return output

# ============ Phase 6: review（四维审核） ============
def run_phase6_review(ch001_text, skeleton_md, protagonist_md, plot_md):
    """Phase 6: review四维审核ch001"""
    print("\n" + "=" * 60)
    print("Phase 6: review 四维审核ch001")
    print("=" * 60)

    system = read_skill("pop-qidian-review", ["SKILL.md"])

    user = f"""# 任务

按起点review v3.0.0 SOP，对ch001执行四维审核。

## 输入

### ch001正文
{ch001_text}

### 骨架.md（审核参照）
{skeleton_md[:3000]}

### 主角设计.md（审核参照）
{protagonist_md[:3000]}

### 剧情白描ch001段（审核参照）
{plot_md[:3000]}

## 执行四维审核

### 维度一：符合性检查
- 1a 核心事件对照（偏离=废章）
- 1b 骨架一致性（1b-1力量体系一致性+1b-2动力引擎一致性）
- 1c 天赋约束检查（金手指是否喧宾夺主/天赋代价是否兑现）
- 1d 剧情映射检查（血肉是否映射坐标系）
- 1e 角色一致性（对照角色库+攀登方式一致性）
- 1f 爽感闭环检查（触发→爆发→后果+爽感因子检查）

### 维度二：笔触检查
- 2a AI味7项
- 2b 笔触DNA一致性

### 维度三：好看度检查
- 有没有劲？
- 记忆点？
- 哪里无聊？
- 代入感？

### 维度四：剧情沉淀
- 主角变化五项（位置/能力/资产/心态/关系）
- 钩子追踪

## 产出格式
审核-ch001.md，包含四维审核结论+骨架一致性结论+天赋约束结论+剧情映射结论+好看度4问结论+主角变化五项+钩子追踪

直接输出审核报告，不要写思考过程。
"""
    output, usage, elapsed = call_ds(system, user, max_tokens=8000, temperature=0.70)
    meta = save_io("phase6-review-ch001", system, user, output, usage, elapsed)
    if output:
        print(f"  完成! {elapsed:.1f}s | {len(output)}字符 | tokens:{usage.get('total_tokens', 0)}")
    return output

# ============ 主程序 ============
def main():
    os.makedirs(INPUTS_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("=" * 60)
    print("起点skill群 R1 全链路测试")
    print(f"赛道：{TRACK}")
    print(f"API: {DS_MODEL}")
    print(f"链路: seed骨架→seed主角→seed创意首章→world→character→plot→write→review")
    print("=" * 60)

    all_meta = []
    start_time = time.time()

    # Phase 1: 骨架层
    skeleton_md = run_phase1_skeleton()
    if not skeleton_md:
        print("[FATAL] Phase 1骨架层失败，终止测试")
        sys.exit(1)

    # Phase 2: 主角层
    protagonist_md = run_phase2_protagonist(skeleton_md)
    if not protagonist_md:
        print("[FATAL] Phase 2主角层失败，终止测试")
        sys.exit(1)

    # Phase 1续: 创意发散+故事纲领+黄金首章
    creative_md = run_phase1_creative(skeleton_md, protagonist_md)
    if not creative_md:
        print("[WARN] Phase 1创意首章失败，继续后续测试")

    # Phase 3: world
    world_md = run_phase3_world(skeleton_md, protagonist_md, creative_md or "")
    if not world_md:
        print("[WARN] Phase 3 world失败，继续后续测试")

    # Phase 3.5: character
    character_md = run_phase3_5_character(skeleton_md, protagonist_md, world_md or "")
    if not character_md:
        print("[WARN] Phase 3.5 character失败，继续后续测试")

    # Phase 4: plot
    plot_md = run_phase4_plot(skeleton_md, protagonist_md, world_md or "", character_md or "")
    if not plot_md:
        print("[WARN] Phase 4 plot失败，继续后续测试")

    # Phase 5: write
    ch001_text = run_phase5_write(skeleton_md, protagonist_md, plot_md or "", character_md or "")
    if not ch001_text:
        print("[WARN] Phase 5 write失败，继续后续测试")

    # Phase 6: review
    review_md = run_phase6_review(ch001_text or "[ch001未产出]", skeleton_md, protagonist_md, plot_md or "")

    # 总结
    total_time = time.time() - start_time
    print("\n" + "=" * 60)
    print(f"R1全链路测试完成！总耗时: {total_time:.1f}s")
    print("=" * 60)
    print("\n--- 产出文件清单 ---")
    for f in sorted(os.listdir(OUTPUT_DIR)):
        fpath = os.path.join(OUTPUT_DIR, f)
        size = os.path.getsize(fpath)
        print(f"  {f}: {size}字节")

    # 保存meta
    meta_all = {
        "round": "R1",
        "track": TRACK,
        "model": DS_MODEL,
        "total_elapsed": round(total_time, 1),
        "phases": [
            {"name": "phase1-骨架", "status": "done" if skeleton_md else "failed"},
            {"name": "phase2-主角设计", "status": "done" if protagonist_md else "failed"},
            {"name": "phase1-创意首章", "status": "done" if creative_md else "failed"},
            {"name": "phase3-world", "status": "done" if world_md else "failed"},
            {"name": "phase3.5-character", "status": "done" if character_md else "failed"},
            {"name": "phase4-plot", "status": "done" if plot_md else "failed"},
            {"name": "phase5-write-ch001", "status": "done" if ch001_text else "failed"},
            {"name": "phase6-review-ch001", "status": "done" if review_md else "failed"},
        ]
    }
    with open(os.path.join(OUTPUT_DIR, "r1-meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta_all, f, ensure_ascii=False, indent=2)

    print(f"\nmeta → {os.path.join(OUTPUT_DIR, 'r1-meta.json')}")

if __name__ == "__main__":
    main()
