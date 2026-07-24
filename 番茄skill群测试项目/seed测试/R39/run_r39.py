"""
R39 AB测试脚本
同一输入(深渊主宰卷1白描ch001-005段) + 同一金手指设定
A组: 走 pop-fanqie-write v7.3.0 SOP (动作链+多感官+系统面板【】+2000-2500字)
B组: 走 pop-zhanggang SOP (4段式骨架+期待感对话钩子+3100-3500字)
"""
import json
import concurrent.futures
from pathlib import Path
import requests

# ============ 配置 ============
DS_API_KEY = "sk-5a3654e4aa2e4eefa08abe3d0e0231f5"
DS_BASE_URL = "https://api.deepseek.com/v1"
DS_MODEL = "deepseek-v4-flash"
PROXIES = {"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"}

R39_DIR = Path(r"d:\popwave-skills\番茄skill群测试项目\R39")
WHITE_PAPER_FILE = Path(r"d:\popwave-skills\workspace\深渊主宰-瘦身白描测试\下游产出\Phase1.5-全书剧情白描.md")
DNA_FILE = Path(r"d:\popwave-skills\skills\pop-qidian-write\dna\深渊主宰-v10.md")

A_OUTPUT = R39_DIR / "A-write"
B_OUTPUT = R39_DIR / "B-zhanggang"
INPUTS_DIR = R39_DIR / "inputs"
A_OUTPUT.mkdir(parents=True, exist_ok=True)
B_OUTPUT.mkdir(parents=True, exist_ok=True)
INPUTS_DIR.mkdir(parents=True, exist_ok=True)

# ============ 加载共享输入 ============
white_paper = WHITE_PAPER_FILE.read_text(encoding="utf-8")
dna = DNA_FILE.read_text(encoding="utf-8")

# 提取卷1白描前5段（ch001-005）
# 白描是按段落写的，每个段落约对应一个章节区间
# 前5段对应卷1开篇ch001-005
lines = white_paper.split('\n')
# 找到卷1标题行开始，提取前5个段落
paper_segment = '\n'.join(lines[:80])  # 前80行约覆盖ch001-005

# ch001锚点（从白描提取）
ch001_anchor = """章号: ch001
核心事件: 索伦在贫民窟夜雨中苏醒，灵魂已融合游戏数据流，用匕首背刺巴拉斯和卡诺波获得30点杀戮经验，查看属性半精灵敏捷19智力18职业平民和一级盗贼，看到薇薇安后背淤伤决定找治疗药剂
爽点: 压力突破(首杀+金手指激活)
钩子: 预知诸神黄昏与圣者浩劫即将来临
关键数据: 杀戮经验30点, 敏捷19, 智力18, 1级盗贼"""

# ============ A组: write skill SOP ============
def build_a_prompt(ch_num="ch001"):
    """A组: 严格按 pop-fanqie-write v7.3.0 执行"""
    return f"""你是一位资深番茄网文写手，严格按 pop-fanqie-write v7.3.0 执行。

# 任务
基于以下输入，写{ch_num}的正文。2000-2500字，不准超过2500字。

# write skill SOP（5步）

## Step 1: 加载
- 加载本章锚点（章型/核心事件/爽点/钩子）
- 加载剧情白描{ch_num}段（本章的故事流参考）
- 本章是第一章，使用黄金开篇

## Step 2: 章型骨架
- opening_shift（黄金开篇）章型结构
- 前三句扔炸弹，300字内完成冲突+主角+金手指+钩子

## Step 3: 笔触渲染
- 系统面板用【】内联格式，禁止markdown代码块
- 角色思考用碎片化表达，避免完整分析句
- 动作链：连续动作拆成2-3个细动作，禁止1个动词概括
- 多感官：每场景至少3种感官（视觉/听觉/触觉/嗅觉/味觉）

## Step 4: 微观技法
- 动作链（≥3处）
- 多感官优先级（≥2处）
- 信息差博弈
- 后果链设计

## Step 5: 字数自检+交付面板
- 统计`---`前的正文字数，2000-2500字
- 末尾附交付面板

# 红线
1. 字数2000-2500字，不准超过2500字
2. 系统面板用【】内联格式
3. 动作链≥3处，多感官场景≥2处
4. 章末必须有钩子

# 深渊主宰笔触DNA（必须遵循）
{dna}

# 本章锚点
{ch001_anchor}

# 剧情白描ch001段（故事流参考）
{paper_segment}

# 开始写作
"""

# ============ B组: zhanggang skill SOP ============
def build_b_prompt(ch_num="ch001"):
    """B组: 严格按 pop-zhanggang 执行"""
    return f"""你是一位资深网文写手，严格按 pop-zhanggang 章纲流执行。

# 任务
基于以下输入，写{ch_num}的正文。3100-3500字，不准低于3100字，不准超过3500字。

# zhanggang skill SOP（2步）

## Step 1: 前文分析
（本章是第一章，无前文，直接进入Step 2）

## Step 2: 拆解框架 + 填充细节 + 节奏与收尾

### 2a. 4段式骨架分配篇幅
| 段 | 字数 | 内容 |
|----|------|------|
| 开篇 | 650-750字 | 渲染场景氛围，交代人物行动动机 |
| 发展 | 950-1050字 | 探索/行动过程，1-2个小阻碍，逐步接近核心目标 |
| 高潮 | 850-950字 | 达成核心目标，同步引发新冲突 |
| 结尾 | 650-750字 | 即时反应，留悬念钩子 |

总字数目标：3100-3500字

### 2b. 填充细节
- 多维场景描写 + 动作链 + 心理 + 对话，全部围绕核心冲突
- 描写每章控制在3-8个，每个≤30字——拒绝过多形容词/比喻/拟人
- 大白话，强情绪，高代入感

### 2c. 节奏与收尾
- 慢描写与快行动交替
- 留未完成悬念

# 红线
1. 每章结尾必须是期待感对话钩子——禁止事件完结或情绪落地，强制引导读者读下一章
2. 正文开头完美衔接前文结尾——禁止与前文重复剧情
3. 描写每章控制在3-8个，每个≤30字
4. 禁止AI叙述词和总结性/展望性内容
5. 字数3100-3500字

# 输出格式
```
【第1章正文 | 为第2章铺垫：XXX】

章节名

正文内容...
```

# 深渊主宰笔触DNA（必须遵循）
{dna}

# 本章章纲（核心事件）
{ch001_anchor}

# 剧情白描ch001段（故事流参考）
{paper_segment}

# 开始写作
"""

# ============ 并行调用API ============
def call_api(group, prompt, output_file):
    """调用API写章节"""
    print(f"[{group}] 开始写作...")
    headers = {
        "Authorization": f"Bearer {DS_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": DS_MODEL,
        "messages": [
            {"role": "system", "content": "你是一位资深网文写手，严格按skill SOP执行。"},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 5000,
        "temperature": 0.85,
        "stream": False
    }
    try:
        response = requests.post(
            f"{DS_BASE_URL}/chat/completions",
            headers=headers,
            json=payload,
            timeout=300,
            proxies=PROXIES
        )
        response.raise_for_status()
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        output_file.write_text(content, encoding="utf-8")
        print(f"[{group}] 完成，{len(content)}字符")
        return group, content
    except Exception as e:
        print(f"[{group}] 失败: {e}")
        return group, None


# ============ 构造两组prompt ============
a_prompt = build_a_prompt()
b_prompt = build_b_prompt()

# 保存input
(INPUTS_DIR / "A-write_input.md").write_text(a_prompt, encoding="utf-8")
(INPUTS_DIR / "B-zhanggang_input.md").write_text(b_prompt, encoding="utf-8")

print("=" * 60)
print("R39 AB测试 - 同输入对比write vs zhanggang")
print("=" * 60)
print(f"A组(write skill): {len(a_prompt)}字符")
print(f"B组(zhanggang skill): {len(b_prompt)}字符")
print("=" * 60)

# 并行调用
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    futures = {
        executor.submit(call_api, "A-write", a_prompt, A_OUTPUT / "ch001.md"): "A",
        executor.submit(call_api, "B-zhanggang", b_prompt, B_OUTPUT / "ch001.md"): "B"
    }
    for future in concurrent.futures.as_completed(futures):
        group = futures[future]
        try:
            result_group, content = future.result()
            print(f"[{result_group}] 完成")
        except Exception as e:
            print(f"[{group}] 异常: {e}")

print("\n" + "=" * 60)
print("AB测试完成！")
print("=" * 60)
