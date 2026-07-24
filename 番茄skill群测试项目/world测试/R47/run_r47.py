#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
R47 pop-nanpin-world v1.0.0 创作模式测试

测试目标：验证男频world v1.0.0能否基于创意+参考书DNA，产出高质量的三层骨架
（力量体系+动力引擎+金手指）+血肉（地图+势力+危机）+全书设定，足以支撑高质量小说。

核心验证点（男频world v1.0.0的三大创新）：
1. 力量体系广义化——任何阶层金字塔都算力量体系，不限于修仙位阶
2. 动力引擎层（众生攀登系统）——六组成齐全且世界级
3. 金手指显性定位为"助力"——不喧宾夺主检查

测试方案：2组对比测
- A组（修仙赛道·有参考书DNA）：模拟创意 + 玄鉴仙族decon(表1力量体系+表9动力引擎)
  → 验证参考书DNA消费能力 + 标准修仙世界构筑
- B组（历史赛道·无参考书DNA）：模拟创意（寒门科举/门阀社会）
  → 验证力量体系广义化推导 + 动力引擎设计能力（核心创新点）

执行流程（每组2次API调用）：
- Call 1: Step 1-2（SKILL.md作为system + 底牌作为user）→ 三层骨架+血肉
- Call 2: Step 3-4（SKILL.md+step3+step4作为system + Call1产出作为user）→ 全书设定+落盘格式

输入：模拟创意.md + R45/R46已有decon产出（A组）
输出：
  - inputs/{组名}_step12_input.md + {组名}_step34_input.md
  - output/{组名}-step12-三层骨架.md
  - output/{组名}-step34-全书设定.md
"""

import os
import sys
import json
import time
import requests

# ============ 配置 ============
DS_API_KEY = "sk-5a3654e4aa2e4eefa08abe3d0e0231f5"
DS_BASE_URL = "https://api.deepseek.com/v1"
DS_MODEL = "deepseek-v4-flash"
TEMPERATURE = 0.85
TIMEOUT = 600
MAX_TOKENS = 16000

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUTS_DIR = os.path.join(SCRIPT_DIR, "inputs")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")

SKILLS_BASE = r"d:\popwave-skills\skills"
# R45/R46已有decon产出（参考书DNA）
R45_OUTPUT = r"d:\popwave-skills\番茄skill群测试项目\world测试\R45\output"
R46_OUTPUT = r"d:\popwave-skills\番茄skill群测试项目\world测试\R46\output"


# ============ 工具函数 ============

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def read_skill_files(skill_name, files):
    parts = []
    for f in files:
        path = os.path.join(SKILLS_BASE, skill_name, f)
        parts.append(read_file(path))
    return "\n\n---\n\n".join(parts)

def call_ds(system_prompt, user_prompt, max_tokens=MAX_TOKENS):
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

def save_input_output(group_name, step_name, system_prompt, user_prompt, output):
    input_content = f"# SYSTEM PROMPT\n\n{system_prompt}\n\n---\n\n# USER PROMPT\n\n{user_prompt}"
    input_path = os.path.join(INPUTS_DIR, f"{group_name}_{step_name}_input.md")
    with open(input_path, "w", encoding="utf-8") as f:
        f.write(input_content)

    output_path = os.path.join(OUTPUT_DIR, f"{group_name}-{step_name}.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(output)

    return input_path, output_path


# ============ System Prompt 构建 ============

def build_world_system_step12():
    """Step 1-2的system prompt：pop-nanpin-world SKILL.md（含Step 1-2内化内容）"""
    return read_skill_files("pop-nanpin-world", ["SKILL.md"])

def build_world_system_step34():
    """Step 3-4的system prompt：SKILL.md + step3.md + step4.md"""
    return read_skill_files("pop-nanpin-world", ["SKILL.md", "steps/step3.md", "steps/step4.md"])


# ============ A组：修仙赛道创意 ============

IDEA_A = """# 创意.md（模拟·修仙赛道·用于测试男频world创作模式）

## 一句话简介
一个灵根废柴在修仙宗门底层挣扎求生，意外觉醒古法炼器传承，靠修复残破法器换取修炼资源，一步步从外门杂役爬到内门核心。

## 金手指·机制+限制
- 创意：古法炼器传承——能看到法器的"器灵残影"，修复残破法器时能提取器灵记忆碎片
- 机制：修复法器=获取器灵记忆=获得该法器原主人的修炼感悟碎片
- 限制：
  ①每次修复消耗自身灵力，修复越高级法器消耗越大
  ②器灵记忆碎片有排斥反应，同时持有超过3个碎片会灵力紊乱
  ③修复失败法器会炸裂反伤
  ④器灵记忆碎片有时效，7天内不消化会消散
  ⑤只能修复有器灵的法器，普通法器无效
  ⑥修复时进入"器灵视角"，期间对外界无感知（有被偷袭风险）

## 动力引擎（种子框架）
- 驱动逻辑：修仙世界弱肉强食，不攀登就是死
- 运转机制：修复法器→获取资源/感悟→修炼提升→接更高级法器
- 代价结构：灵力消耗+碎片排斥风险+修复时无防备

## 主角轮廓
- 名字：陆沉
- 身份：外门杂役（灵根废柴）
- 核心动机：靠炼器手艺换取修炼资源，弥补灵根劣势
- 记忆点：总能从废品堆里淘宝

## 前期成长路线
- 街头期（1-15章）：在外门杂役区修复低级法器换灵石
- 起家期（16-35章）：靠修复积攒资源突破胎息境
- 扩张期（36-55章）：进入内门，接触中阶法器
- 立足期（56-80章）：成为宗门炼器师，获得正式地位

## 故事纲领三核心+营销层

### 什么样的世界（4层）
- 力量体系层：修仙境界体系（胎息→练气→筑基→紫府→金丹→元婴），修为决定权力、地位和寿命
- 差异层：法器是修士的第二生命，炼器师是稀缺资源，但古法炼器已失传
- 日常层：宗门弟子日常修炼/接任务/交易法器/探索秘境
- 主角层：灵根废柴靠炼器手艺在修士世界攀爬

### 什么样的舞台·世界危机（3要素）
- 危机源头：古法炼器传承重现，引来各方势力争夺
- 敌人梯度：外门欺凌者→内门派系斗争→宗门长老→跨宗门势力
- 压力源：修复法器消耗灵力→修炼进度受阻→必须接更危险的任务

### 什么样的主角（5要素）
- 起点：灵根废柴，外门杂役，最底层
- 拐点：觉醒古法炼器传承
- 终点：一代炼器宗师，靠手艺立足修仙界
- 力量路径：炼器换资源→修炼提升→接触更高级法器→炼器水平提升
- 前期成长路线：见上

### 最大钩子（≤20字）
废柴靠修复废品法器逆袭成炼器宗师

### 即时兑现感
每章修复一个法器获得即时反馈（资源/感悟/技能）"""


# ============ B组：历史赛道创意（验证力量体系广义化）============

IDEA_B = """# 创意.md（模拟·历史赛道·用于测试男频world力量体系广义化）

## 一句话简介
穿越成寒门子弟，靠过目不忘的记忆力和前世历史知识，在九品中正制的门阀社会靠科举和预判政治走向，从寒门小吏一步步爬到权倾朝野。

## 金手指·机制+限制
- 创意：前世历史记忆+过目不忘——知道未来三十年的政治走向、人物命运和战争结局
- 机制：前世记忆提供政治预判+人物弱点信息，过目不忘让科举背书无敌
- 限制：
  ①蝴蝶效应——改变历史后记忆逐渐失效，越改越不准
  ②前世记忆是另一个平行历史，有人物偏差
  ③过目不忘只对文字有效，不能过目不忘人脸/声音
  ④每次动用前世记忆会头痛，频繁使用会流鼻血昏厥
  ⑤前世记忆有时效，只覆盖未来30年，之后完全未知
  ⑥知道结局但不能改变大势——能预判但不能阻止战争/政变

## 动力引擎（种子框架）
- 驱动逻辑：九品中正制下，门阀垄断仕途，寒门无出头之日，不攀爬就是世代为吏
- 运转机制：科举/军功/联姻/投靠→获得品级→扩大势力→接触更高品级
- 代价结构：寒门出身被歧视+政治站队风险+联姻牺牲

## 主角轮廓
- 名字：沈默
- 身份：寒门子弟（县衙小吏之子）
- 核心动机：打破门阀垄断，靠才学和预判为家族挣一个士族身份
- 记忆点：总能在关键时刻说出"未来会发生什么"

## 前期成长路线
- 街头期（1-15章）：县学读书，靠过目不忘碾压同窗，准备科举
- 起家期（16-35章）：中举入仕，从县尉做起，靠预判立功
- 扩张期（36-55章）：进入州府，卷入派系斗争，靠政治预判上位
- 立足期（56-80章）：入朝为官，对抗门阀，推行改制

## 故事纲领三核心+营销层

### 什么样的世界（4层）
- 力量体系层：九品中正制——社会地位金字塔（庶民→寒门→士族→高门→宗王→皇帝），品级决定权力、土地和免役权
- 差异层：门阀世代垄断高品级，寒门只能做低级吏员，科举是唯一突破口但被门阀把持
- 日常层：县学读书/衙门理政/士族社交/科举应试
- 主角层：寒门子弟靠才学和预判在门阀社会攀爬

### 什么样的舞台·世界危机（3要素）
- 危机源头：王朝衰落，边疆战乱将起，朝堂党争激化
- 敌人梯度：县学纨绔→士族子弟→地方豪强→朝堂权臣→宗王
- 压力源：门阀打压寒门→科举受阻→政治站队→家族安危

### 什么样的主角（5要素）
- 起点：寒门子弟，县衙小吏之子，最底层
- 拐点：觉醒前世历史记忆+过目不忘
- 终点：权倾朝野，打破门阀垄断，推行科举改制
- 力量路径：科举背书→政治预判立功→扩大势力→对抗门阀
- 前期成长路线：见上

### 最大钩子（≤20字）
寒门靠预知未来三十年在门阀朝堂逆袭

### 即时兑现感
每章用前世记忆预判一件事获得即时反馈（立功/避祸/碾压）"""


# ============ User Prompt 构建 ============

def build_world_prompt_step12(group):
    """Step 1-2的user prompt：底牌（创意+参考书DNA+市场校准）"""
    group_name = group["name"]
    idea = group["idea"]
    dna_intro = group.get("dna_intro", "")
    dna_content = group.get("dna_content", "")

    dna_section = ""
    if dna_content:
        dna_section = f"""## 输入2：参考书DNA（第二源）

{dna_intro}

```markdown
{dna_content}
```

"""
    else:
        dna_section = """## 输入2：参考书DNA（第二源）

（缺失——本项目无参考书decon-lite拆解结果。world需从赛道惯例+创意.md要素推导力量体系，标注"参考书DNA缺失，world从创意推导"。不阻塞流程。）

"""

    return f"""# 任务

按pop-nanpin-world v1.0.0的**创作模式**SOP，执行Step 1-2：加载底牌 → 按三层骨架生长世界。

## 输入1：创意.md（第三源）

```markdown
{idea}
```

{dna_section}## 输入3：市场校准.md

（缺失——标注缺失，不阻塞）

## 执行要求

**完整执行Step 1-2的创作模式**，产出三层骨架+血肉：

### Step 1：加载底牌
- 从创意.md提取种子条款（创意/金手指/动力引擎/主角轮廓/前期成长路线/故事纲领三核心+营销层）
- 标注底牌缺失项（参考书DNA/市场校准如缺失）

### Step 2：按三层骨架生长世界

**2a. 力量体系设计（广义坐标系·四层结构）**
- 第一层：世界源力量（源力量名称/来源/转化链/敌分级标准）
- 第二层：主养成线（展开5-7个阶位，每个阶位必须有文化渊源+社会地位参照+预计展开卷）
- 第三层：子养成线（从decon-lite逐条消费，每条含自身阶位+主养成线挂钩+规则+参考源）
- 第四层：交叉规则（从decon-lite逐条消费，每条含涉及子养成线/协同制约类型/具体规则/参考源）

**2b. 动力引擎设计（众生攀登系统·六组成）**
- 组成1：驱动逻辑（世界级驱动力+主角欲望对齐）
- 组成2：运转机制（输入→转化→输出→反馈闭环）
- 组成3：众生攀登方式分层（有资源/没资源/爬到顶层/掉下来的人分别怎么爬——直接对应势力来源）
- 组成4：代价结构（通用代价+群体差异代价+累积效应）
- 组成5：范式归类（飞轮型/探索型/混合型/压迫型/对抗型+1句说明）
- 组成6：演化节点（是否演化+触发事件+演化方向+预计演化卷）

**2c. 地图**（从坐标系空间分布生长——城市结构表）

**2d. 势力**（从众生攀登方式差异生长——4层全具名，每层标注攀登方式来源）

**2e. 危机体系**（三层面：坐标系内压+引擎代价+金手指限制——1条终极+2-3条阶段性）

**2f. 金手指定位**（助力定位+不喧宾夺主检查）

## 红线
1. 力量体系必须广义化——任何阶层金字塔都算力量体系，不限于修仙位阶。历史赛道的门阀社会地位、经济赛道的资本等级都是力量体系。力量体系必须四层结构完整。
2. 动力引擎三组成齐全且世界级——设计的是众生如何爬，不是主角如何爬。decon-lite拆出的子养成线/交叉规则必须逐条处理（照搬转化or标注不需要原因），禁止丢条自编。
3. 众生攀登方式差异=势力来源——势力从众生攀登方式的差异中生长，不脱离引擎凭空设计势力。全书4层势力全具名。
4. 金手指是助力不喧宾夺主——金手指降低跨越难度但不能取消坐标系本身的意义。必须有限制+代价。

直接输出Step 1-2完整产出，markdown格式。不要写思考过程。"""


def build_world_prompt_step34(group, step12_output):
    """Step 3-4的user prompt：基于Step 1-2产出执行全书设定+落盘"""
    group_name = group["name"]
    return f"""# 任务

基于以下pop-nanpin-world v1.0.0 Step 1-2的产出（三层骨架+血肉），执行Step 3-4：全书设定 + 落盘多文件格式。

## 输入：Step 1-2产出（三层骨架+血肉）

```markdown
{step12_output}
```

## 执行要求

### Step 3：全书设定（3-8卷200万字级）

按step3.md执行，产出：

**3a. 全书设定总览**（5张表）：
1. 力量体系全书展开表（5-7层完整，每层标注预计展开卷+社会地位参照+源力量转化）
2. **动力引擎全书演化表**（每卷标注引擎状态+演化节点+众生攀登方式变化+代价结构变化+主角在引擎中的位置）
3. 地图全书展开表（所有区域，每个标注预计进入卷）
4. 势力全书展开表（4层全具名，每层标注攀登方式来源+预计碰撞卷）
5. 危机全书展开表（1条终极+2-3条阶段性，每条标注属于哪个层面+预计爆发卷）

**3b. 全书配角设计**（补充seed未覆盖的配角，每个标注攀登方式代表+预计出场卷）

**3c. 各卷设定切片预览**（给plot的导航索引，每卷含力量范围+动力引擎切片+地理范围+势力范围+危机范围+卷末设定边界）

### Step 4：落盘全书设定（多文件格式）

按step4.md的落盘格式，将全书设定按维度拆分为8个文件的格式输出：
1. 力量体系.md
2. 动力引擎.md（六组成完整+全书演化表）
3. 地图.md
4. 势力.md
5. 危机.md
6. 金手指.md（助力定位+不喧宾夺主检查）
7. 全书配角.md
8. 各卷切片.md

每个文件用 `### 设计/全书设定/<文件名>` 作为标题分隔。

## 红线
1. 全书设定每项标注各卷覆盖范围——力量体系每层标注哪卷展开、地图每区域标注哪卷进入、势力每层标注哪卷碰撞、危机每条标注哪卷爆发
2. 动力引擎全书演化表必须完整——每卷标注引擎状态+演化节点（这是男频world v1.0.0的核心新增）
3. 势力4层全具名，每层标注攀登方式来源（回溯Step 2b组成3）
4. 全书3-8卷，不能只做第一卷

直接输出Step 3-4完整产出，markdown格式。不要写思考过程。"""


# ============ 测试组配置 ============

def load_group_a():
    """A组：修仙赛道·有参考书DNA"""
    decon_table1 = read_file(os.path.join(R45_OUTPUT, "decon-玄鉴仙族.md"))
    decon_table9 = read_file(os.path.join(R46_OUTPUT, "decon-full-玄鉴仙族-表9补拆.md"))
    dna_content = f"""### 参考书decon-lite表1：力量体系结构（规则级深度）

{decon_table1}

---

### 参考书decon表9：动力引擎提取表

{decon_table9}
"""
    return {
        "name": "A-修仙",
        "idea": IDEA_A,
        "dna_intro": "参考书：《玄鉴仙族》（季越人）。以下为decon-lite拆出的表1力量体系结构（规则级）+表9动力引擎提取表。world必须逐条消费表1的子养成线/交叉规则和表9的动力引擎六组成。",
        "dna_content": dna_content,
    }

def load_group_b():
    """B组：历史赛道·无参考书DNA（验证力量体系广义化）"""
    return {
        "name": "B-历史",
        "idea": IDEA_B,
        "dna_intro": "",
        "dna_content": "",
    }


# ============ 主流程 ============

def process_group(group):
    """对每组执行Step 1-2 + Step 3-4两步"""
    group_name = group["name"]

    print(f"\n{'='*60}")
    print(f"处理 {group_name} 组")
    print(f"{'='*60}")

    # Step 1-2: 三层骨架+血肉（断点续传：若产出已存在则跳过API调用）
    step12_out_path = os.path.join(OUTPUT_DIR, f"{group_name}-step12.md")
    if os.path.exists(step12_out_path):
        print(f"\n[Step 1-2] 检测到已有产出，跳过API调用: {step12_out_path}")
        step12_output = read_file(step12_out_path)
        print(f"  读取完成 | {len(step12_output)}字符")
    else:
        print(f"\n[Step 1-2] 三层骨架+血肉设计...")
        step12_system = build_world_system_step12()
        step12_prompt = build_world_prompt_step12(group)
        try:
            step12_output, step12_usage, step12_elapsed = call_ds(
                step12_system, step12_prompt, max_tokens=MAX_TOKENS
            )
            step12_in, step12_out = save_input_output(
                group_name, "step12", step12_system, step12_prompt, step12_output
            )
            print(f"  完成! {step12_elapsed:.1f}s | {len(step12_output)}字符 | tokens:{step12_usage.get('total_tokens', 0)}")
            print(f"    input  → {step12_in}")
            print(f"    output → {step12_out}")
        except Exception as e:
            print(f"  Step 1-2失败: {e}")
            return None

    # Step 3-4: 全书设定+落盘（断点续传）
    step34_out_path = os.path.join(OUTPUT_DIR, f"{group_name}-step34.md")
    if os.path.exists(step34_out_path):
        print(f"\n[Step 3-4] 检测到已有产出，跳过API调用: {step34_out_path}")
        step34_output = read_file(step34_out_path)
        print(f"  读取完成 | {len(step34_output)}字符")
    else:
        print(f"\n[Step 3-4] 全书设定+落盘...")
        step34_system = build_world_system_step34()
        step34_prompt = build_world_prompt_step34(group, step12_output)
        try:
            step34_output, step34_usage, step34_elapsed = call_ds(
                step34_system, step34_prompt, max_tokens=MAX_TOKENS
            )
            step34_in, step34_out = save_input_output(
                group_name, "step34", step34_system, step34_prompt, step34_output
            )
            print(f"  完成! {step34_elapsed:.1f}s | {len(step34_output)}字符 | tokens:{step34_usage.get('total_tokens', 0)}")
            print(f"    input  → {step34_in}")
            print(f"    output → {step34_out}")
        except Exception as e:
            print(f"  Step 3-4失败: {e}")
            return None

    return {
        "group": group_name,
        "step12_output": step12_output,
        "step34_output": step34_output,
    }


def main():
    os.makedirs(INPUTS_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("=" * 60)
    print("R47 pop-nanpin-world v1.0.0 创作模式测试")
    print("测试方案：2组对比测")
    print("  A组：修仙赛道 + 玄鉴仙族decon（验证参考书DNA消费）")
    print("  B组：历史赛道 + 无参考书（验证力量体系广义化）")
    print(f"  每组2次API调用：Step1-2骨架 → Step3-4全书设定")
    print("=" * 60)

    total_start = time.time()

    # 加载测试组
    groups = []
    print("\n[加载测试组]")
    groups.append(load_group_a())
    print(f"  A组加载完成：参考书DNA {len(groups[-1]['dna_content'])}字符")
    groups.append(load_group_b())
    print(f"  B组加载完成：无参考书DNA（验证广义化）")

    results = []
    for group in groups:
        result = process_group(group)
        if result:
            results.append(result)

    total_elapsed = time.time() - total_start

    # 汇总
    print(f"\n{'='*60}")
    print("R47测试完成！")
    print(f"  总耗时: {total_elapsed/60:.1f}分钟")
    print(f"{'='*60}")
    print(f"\n产出文件:")
    for group_name in [g["name"] for g in groups]:
        print(f"  {group_name}组:")
        print(f"    Step1-2骨架  → output/{group_name}-step12.md")
        print(f"    Step3-4设定  → output/{group_name}-step34.md")
        print(f"    inputs       → inputs/{group_name}_step12_input.md")
        print(f"                  → inputs/{group_name}_step34_input.md")

    print(f"\n下一步：人工验收（7维度）")
    print(f"  1. 三层骨架完整性（力量体系四层+动力引擎六组+金手指定位）")
    print(f"  2. 血肉从骨架生长（地图从坐标系/势力从攀登方式/危机三层面）")
    print(f"  3. 力量体系广义化（B组历史赛道的门阀社会地位是否被识别为力量体系）")
    print(f"  4. 参考书DNA消费（A组是否逐条消费decon的子养成线/交叉规则/动力引擎）")
    print(f"  5. 全书设定完整性（3-8卷/每项标注卷覆盖/动力引擎全书演化表）")
    print(f"  6. 金手指不喧宾夺主检查")
    print(f"  7. 阶位名文化渊源（禁止通用词）")


if __name__ == "__main__":
    main()
