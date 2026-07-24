#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
R3 write测试——用pop-qidian-write v3.3.0（唯一write skill）写ch001-ch003
消费：项目A设定 + R3卷纲.md + R3章锚点表.md
流派：D&D数据面板流（加载references/流派专属/dndlike/技法包）
DNA：缺失态（项目A无素材/文风锚定.md）→ trial模式（用户声明深渊主宰风格）
"""

import os, sys, json, time, requests

# ============ API配置 ============
DS_API_KEY = "sk-5a3654e4aa2e4eefa08abe3d0e0231f5"
DS_BASE_URL = "https://api.deepseek.com/v1"
DS_MODEL = "deepseek-v4-flash"
PROXIES = {"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"}
TIMEOUT = 600

# ============ 路径配置 ============
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")
INPUTS_DIR = os.path.join(SCRIPT_DIR, "inputs")
SKILLS_BASE = r"d:\popwave-skills\skills"
PROJECT_A = r"C:\Users\AWMPRO\AppData\Roaming\popwave\paopao-workspace\projects\7-22项目a"

# ============ 工具函数 ============
def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def read_skill_file(skill_name, relative_path):
    path = os.path.join(SKILLS_BASE, skill_name, relative_path)
    if os.path.exists(path):
        return read_file(path)
    print(f"  [警告] 文件不存在: {path}")
    return ""

def call_ds(system_prompt, user_prompt, max_tokens=12000, temperature=0.85):
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

def save_output(name, content):
    path = os.path.join(OUTPUT_DIR, f"{name}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content if content else "[API调用失败]")
    return len(content) if content else 0

# ============ 构建system prompt ============
def build_system_prompt():
    """构建write v3.3.0的完整system prompt"""
    parts = []

    # 1. write SKILL.md（主SOP）
    parts.append(read_skill_file("pop-qidian-write", "SKILL.md"))

    # 2. step文件
    parts.append(read_skill_file("pop-qidian-write", "steps/step-1-consume.md"))
    parts.append(read_skill_file("pop-qidian-write", "steps/step-2-write.md"))

    # 3. references（章型定义+爽点引擎+微观技法工具箱）
    parts.append(read_skill_file("pop-qidian-write", "references/章型定义.md"))
    parts.append(read_skill_file("pop-qidian-write", "references/爽点引擎.md"))
    parts.append(read_skill_file("pop-qidian-write", "references/微观技法工具箱.md"))

    # 4. opening_shift/exploration_gain/confrontation_pressure推荐技法
    parts.append(read_skill_file("pop-qidian-write", "references/通用技法/信息差博弈.md"))
    parts.append(read_skill_file("pop-qidian-write", "references/情境技法/感官锚点.md"))
    parts.append(read_skill_file("pop-qidian-write", "references/通用技法/预期违背.md"))
    parts.append(read_skill_file("pop-qidian-write", "references/通用技法/节奏微操.md"))

    # 5. D&D流派技法包（references/流派专属/dndlike/）
    dndlike_files = [
        "面板弹出判断表.md",
        "面板叙事.md",
        "数据化分析.md",
        "战斗模式-凡人期.md",
        "场景卡.md"
    ]
    for f in dndlike_files:
        parts.append(read_skill_file("pop-qidian-write", f"references/流派专属/dndlike/{f}"))

    # 6. DNA缺失态声明
    parts.append("""# DNA三态协议·缺失态声明

素材/文风锚定.md 不存在。本轮为trial模式——用户声明风格。

## 用户声明风格
- 参考书：《深渊主宰》（D&D数据面板流）
- 风格关键词：冷硬数据流+意识流面板+武打动作写实+暗黑基调
- 叙事距离：贴身近景为主，战斗时切微观特写
- 句式：短句为主，战斗段落节奏加速，面板数据用意识流嵌入
- 对话：简洁利落，不废话，角色口头禅点睛
- 情绪外化：通过面板数据和身体反应外化，不直接写心理""")

    return "\n\n---\n\n".join(parts)

# ============ 构建每章user prompt ============
def build_chapter_prompt(ch_num, ch_anchor, skeleton_md, protagonist_md, character_md, juan_gang_md):
    """构建单章user prompt"""
    # 提取卷纲中该章相关段落（白描+场景表）
    # 这里简化处理，把整个卷纲md传进去（API token限制下截断）

    return f"""# 任务

按pop-qidian-write v3.3.0 SOP，写{ch_num}正文。

**本轮为DNA trial模式——按用户声明风格（深渊主宰D&D数据面板流风格）执行笔触层。**
**本轮流派=D&D数据面板流——必须加载流派专属/dndlike/技法包，执行D&D专属红线。**

## 输入

### 骨架.md（力量体系+动力引擎）
{skeleton_md[:3000]}

### 主角设计.md（含爽感矛盾公式）
{protagonist_md[:3000]}

### 角色库摘要
{character_md[:3000]}

### 卷纲.md（第一卷四层结构）
{juan_gang_md[:6000]}

### 本章锚点（从章锚点表提取——4硬锚点必须遵守+3软指导可调整）

{ch_anchor}

## 执行步骤

### Step 1: 加载
- 骨架.md（力量体系+动力引擎）
- 主角设计.md（爽感矛盾公式：坐标系门槛×天赋加速×代价约束）
- 角色库.md（角色唯一源）
- 卷纲.md（本卷四层结构）
- 本章锚点（4硬锚点+3软指导）

### Step 2: 章意图思考 + 面板弹出判断
按面板弹出判断表，判断本章需要弹出哪些面板。

### Step 3: 选章型
按锚点表的章型🔒字段执行。

### Step 4: 加载流派技法
D&D数据面板流：面板弹出判断表+面板叙事+数据化分析+战斗模式-凡人期+场景卡

### Step 5: 微观技法选择
按章型推荐组合选择微观技法。

### Step 6: 写正文
五层指导：
- 笔触层：trial模式——按深渊主宰风格（冷硬数据流+意识流面板+武打写实+短句加速）
- 节奏层：事件密度8-12/章，爽感≥1/章，微钩子每3-5行
- 格局层：空间尺度+侧面定级
- 爽感层：锚定坐标系跃迁——D&D专属=面板弹出瞬间
- 微观层：按选定技法执行

**D&D专属硬约束**：
1. 击杀敌人必弹伤害结算面板
2. 升级必弹职业提升面板
3. 首次遭遇新怪物必弹怪物鉴定面板
4. 面板以意识流数据流形式嵌入叙述，不以弹窗/光屏形式出现
5. 属性数值必须有具象参照物锚定
6. 2000-2500字

### Step 7: 验收
- 字数2000-2500
- 4硬锚点全部执行
- 角色库一致性
- 爽感锚定坐标系跃迁
- 面板弹出节点全部执行

## 产出格式
{ch_num}正文（2000-2500字）+ 执行报告（含面板弹出清单+硬锚点执行确认+技法落地标注）

直接输出正文+执行报告，不要写思考过程。
"""

# ============ 章锚点（从R3章锚点表提取） ============
CHAPTER_ANCHORS = {
    "ch001": """| 章 | 章型🔒 | 核心事件🔒 | 爽感节点🔒 | 章末钩子🔒 | 主角变化💡 | 爽感因子💡 | 章名💡 |
| ch001 | opening_shift | 尘心重生苏醒，面板激活，确认距影之王降临仅20天 | 面板首次激活——气池/武技/禅定数据可视化，确认时间线 | 确认倒计时后立刻制定行动计划——先找尤里买情报 | 从浑噩重生者切换到冷静规划者 | 坐标系门槛×天赋加速 | 二十天 |""",

    "ch002": """| 章 | 章型🔒 | 核心事件🔒 | 爽感节点🔒 | 章末钩子🔒 | 主角变化💡 | 爽感因子💡 | 章名💡 |
| ch002 | exploration_gain | 码头区酒馆与尤里情报交易，用前世独家情报换灰鼠帮内部情报 | 用"三天后血牙帮袭商会车队"的未来信息换取尤里信任——信息差碾压 | 尤里提供灰鼠帮情报后，尘心决定先解决灰鼠帮威胁 | 建立第一个外部情报源 | 天赋加速×代价约束 | 酒馆里的未来人 |""",

    "ch003": """| 章 | 章型🔒 | 核心事件🔒 | 爽感节点🔒 | 章末钩子🔒 | 主角变化💡 | 爽感因子💡 | 章名💡 |
| ch003 | confrontation_pressure | 灰鼠帮打手到武馆收保护费，巴鲁克对峙，尘心出面摆平 | 尘心以二阶实力压制灰鼠帮打手，展示武僧正面战力 | 芬恩扬言报复，尘心决定加速地下城发育计划 | 从被动防御转向主动备战 | 坐标系门槛×代价约束 | 保护费 |"""
}

# ============ 主程序 ============
def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(INPUTS_DIR, exist_ok=True)

    print("=" * 60)
    print("R3 write测试——pop-qidian-write v3.3.0")
    print(f"流派: D&D数据面板流（references/流派专属/dndlike/技法包）")
    print(f"DNA: 缺失态→trial模式（深渊主宰风格）")
    print(f"消费: 项目A设定 + R3卷纲.md + R3章锚点表.md")
    print(f"产出: ch001-ch003正文")
    print(f"API: {DS_MODEL}")
    print("=" * 60)

    # 读取项目A设定
    print("\n读取项目A设定...")
    skeleton_md = read_file(os.path.join(PROJECT_A, "设计", "骨架.md"))
    protagonist_md = read_file(os.path.join(PROJECT_A, "设计", "主角设计.md"))
    character_md = read_file(os.path.join(PROJECT_A, "设计", "角色库", "角色库.md"))
    print(f"  骨架.md: {len(skeleton_md)}字符")
    print(f"  主角设计.md: {len(protagonist_md)}字符")
    print(f"  角色库.md: {len(character_md)}字符")

    # 读取R3卷纲
    print("\n读取R3卷纲...")
    juan_gang_md = read_file(os.path.join(OUTPUT_DIR, "卷纲.md"))
    print(f"  卷纲.md: {len(juan_gang_md)}字符")

    # 构建system prompt
    print("\n构建system prompt...")
    system_prompt = build_system_prompt()
    print(f"  system prompt: {len(system_prompt)}字符")

    # 保存system prompt
    with open(os.path.join(INPUTS_DIR, "write_system_prompt.md"), "w", encoding="utf-8") as f:
        f.write(system_prompt)

    # 写3章
    chapters = ["ch001", "ch002", "ch003"]
    all_meta = []
    start_time = time.time()

    for ch in chapters:
        print(f"\n{'='*60}")
        print(f"写 {ch} 正文...")
        print(f"{'='*60}")

        user_prompt = build_chapter_prompt(
            ch, CHAPTER_ANCHORS[ch],
            skeleton_md, protagonist_md, character_md, juan_gang_md
        )

        # 保存user prompt
        with open(os.path.join(INPUTS_DIR, f"write-{ch}_input.md"), "w", encoding="utf-8") as f:
            f.write(user_prompt)

        output, usage, elapsed = call_ds(system_prompt, user_prompt, max_tokens=8000, temperature=0.85)

        if output:
            size = save_output(f"write-{ch}", output)
            print(f"  完成! {elapsed:.1f}s | {len(output)}字符 | tokens:{usage.get('total_tokens', 0)}")
            all_meta.append({
                "chapter": ch,
                "status": "done",
                "output_length": len(output),
                "elapsed": round(elapsed, 1),
                "tokens": usage.get('total_tokens', 0)
            })
        else:
            print(f"  失败!")
            all_meta.append({
                "chapter": ch,
                "status": "failed",
                "output_length": 0,
                "elapsed": 0,
                "tokens": 0
            })

    # 总结
    total_time = time.time() - start_time
    print(f"\n{'='*60}")
    print(f"R3 write测试完成！总耗时: {total_time:.1f}s")
    print(f"{'='*60}")
    print("\n--- 产出文件 ---")
    for f in sorted(os.listdir(OUTPUT_DIR)):
        if f.startswith("write-"):
            fpath = os.path.join(OUTPUT_DIR, f)
            size = os.path.getsize(fpath)
            print(f"  {f}: {size}字节")

    # 保存meta
    meta = {
        "round": "R3-write",
        "write_skill": "pop-qidian-write v3.3.0",
        "genre": "D&D数据面板流（references/流派专属/dndlike/技法包）",
        "dna_state": "缺失态→trial模式（深渊主宰风格）",
        "model": DS_MODEL,
        "total_elapsed": round(total_time, 1),
        "chapters": all_meta
    }
    with open(os.path.join(OUTPUT_DIR, "r3-write-meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    print(f"\nmeta → {os.path.join(OUTPUT_DIR, 'r3-write-meta.json')}")

if __name__ == "__main__":
    main()
