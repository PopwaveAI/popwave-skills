"""
R40 AB测试脚本 - 5章串行+前章钩子传递
对比write skill vs zhanggang skill写到ch005
max_tokens=32768 解决截断问题
"""
import os
import time
import json
from pathlib import Path
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

DS_API_KEY = "sk-5a3654e4aa2e4eefa08abe3d0e0231f5"
DS_BASE_URL = "https://api.deepseek.com/v1"
DS_MODEL = "deepseek-v4-flash"
PROXIES = {"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"}

R40_DIR = Path(r"d:\popwave-skills\番茄skill群测试项目\R40")
WHITE_PAPER_FILE = Path(r"d:\popwave-skills\workspace\深渊主宰-瘦身白描测试\下游产出\Phase1.5-全书剧情白描.md")
DNA_FILE = Path(r"d:\popwave-skills\skills\pop-qidian-write\dna\深渊主宰-v10.md")

A_OUTPUT = R40_DIR / "A-write"
B_OUTPUT = R40_DIR / "B-zhanggang"
INPUTS_DIR = R40_DIR / "inputs"
A_OUTPUT.mkdir(parents=True, exist_ok=True)
B_OUTPUT.mkdir(parents=True, exist_ok=True)
INPUTS_DIR.mkdir(parents=True, exist_ok=True)

white_paper = WHITE_PAPER_FILE.read_text(encoding="utf-8")
dna = DNA_FILE.read_text(encoding="utf-8")
lines = white_paper.split('\n')

# ch001-005对应的白描段（前5段）
paper_ch1 = '\n'.join(lines[8:11])    # 第1段：苏醒+首杀
paper_ch2 = '\n'.join(lines[10:13])   # 第2段：藏宝洞前
paper_ch3 = '\n'.join(lines[12:15])   # 第3段：藏宝洞+万象无常牌
paper_ch4 = '\n'.join(lines[14:17])   # 第4段：出售+术士天赋
paper_ch5 = '\n'.join(lines[16:19])   # 第5段：商队+女巫

CHAPTERS = [
    {
        "ch": "ch001",
        "anchor": "核心事件: 索伦在贫民窟夜雨中苏醒，灵魂已融合游戏数据流，用匕首背刺巴拉斯和卡诺波获得30点杀戮经验，查看属性半精灵敏捷19智力18职业平民和一级盗贼，看到薇薇安后背淤伤决定找治疗药剂\n爽点: 压力突破(首杀+金手指激活)\n钩子: 预知诸神黄昏与圣者浩劫即将来临\n关键数据: 杀戮经验30点, 敏捷19, 智力18, 1级盗贼",
        "paper": paper_ch1,
        "is_first": True
    },
    {
        "ch": "ch002",
        "anchor": "核心事件: 索伦潜入码头区仓库撬锁拆陷阱，盗贼升到2级敏捷突破20超凡门槛，计划前往藏宝洞\n爽点: 成长(升级+属性突破)\n钩子: 藏宝洞的超凡装备\n关键数据: 盗贼2级, 敏捷20(超凡)",
        "paper": paper_ch2,
        "is_first": False
    },
    {
        "ch": "ch003",
        "anchor": "核心事件: 索伦在乱葬岗下藏宝洞击杀骷髅和幽灵，发现铁木盒中奥术帝国遗物万象无常牌，第一张神偷把他全身物品偷光，第二张苦行者体质提升到18觉醒坚毅专长，第三张召唤三阶深渊蛇魔\n爽点: 未知揭示(万象无常牌)+压力突破(濒死击杀蛇魔)\n钩子: 蛇魔掉落的两把长剑+1和食人魔力量护腕\n关键数据: 盗贼4级, 体质18, 坚毅专长, 1800经验",
        "paper": paper_ch3,
        "is_first": False
    },
    {
        "ch": "ch004",
        "anchor": "核心事件: 索伦出售战利品购买次元袋，预知魔法女神将陨落魔网崩溃，带薇薇安前往冰雪国度，薇薇安觉醒天生术士魅力21感知18\n爽点: 未知揭示(薇薇安术士天赋)+成长(装备升级)\n钩子: 索伦推测薇薇安是神子，决心用生命守护她\n关键数据: 次元袋, 薇薇安魅力21感知18",
        "paper": paper_ch4,
        "is_first": False
    },
    {
        "ch": "ch005",
        "anchor": "核心事件: 商队遭遇掘地虫袭击，索伦凭记忆判断是三阶群居生物指挥击杀获得大量经验，北地女巫歌莉娅主动接近觊觎薇薇安天赋，女巫占卜预言血与火的未来\n爽点: 压力突破(指挥击杀掘地虫)+未知揭示(女巫预言)\n钩子: 女巫预言薇薇安将伴随杀戮与战争，索伦坦言在害怕和逃避\n关键数据: 掘地虫经验, 女巫歌莉娅",
        "paper": paper_ch5,
        "is_first": False
    }
]

# ============ A组: write skill SOP ============
def build_a_prompt(chapter, prev_text=None):
    ch = chapter["ch"]
    is_first = chapter["is_first"]
    
    prev_section = ""
    if prev_text:
        # 取前章最后30行作为钩子参考
        prev_lines = prev_text.split('\n')
        prev_segment = '\n'.join(prev_lines[-30:])
        prev_section = f"""
# 前章结尾（{ch}必须回收前章钩子）
{prev_segment}
"""
    else:
        prev_section = "\n# 本章是第一章，使用黄金开篇\n"
    
    return f"""你是一位资深番茄网文写手，严格按 pop-fanqie-write v7.3.0 执行。

# 任务
基于以下输入，写{ch}的正文。2000-2500字，不准超过2500字。

# write skill SOP（5步）

## Step 1: 加载
- 加载本章锚点
- 加载剧情白描{ch}段
{prev_section}
## Step 2: 章型骨架
- {"opening_shift（黄金开篇）——前三句扔炸弹，300字内完成冲突+主角+金手指+钩子" if is_first else "成长/披露/对抗/揭示章型"}
- 章锚点表锁定：严格按锚点表的核心事件写，禁止跳章

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
3. {"第一章用黄金开篇" if is_first else f"本章必须回收前章钩子"}
4. 动作链≥3处，多感官场景≥2处
5. 章末必须有钩子

# 深渊主宰笔触DNA（必须遵循）
{dna}

# 本章锚点
- 章号: {ch}
{chapter["anchor"]}

# 剧情白描{ch}段（故事流参考）
{chapter["paper"]}

# 开始写作
"""

# ============ B组: zhanggang skill SOP ============
def build_b_prompt(chapter, prev_text=None):
    ch = chapter["ch"]
    is_first = chapter["is_first"]
    
    prev_section = ""
    if prev_text:
        prev_lines = prev_text.split('\n')
        prev_segment = '\n'.join(prev_lines[-30:])
        prev_section = f"""
# 前章结尾（{ch}必须完美衔接前文结尾，禁止与前文重复剧情）
{prev_segment}
"""
    else:
        prev_section = "\n# 本章是第一章，无前文\n"
    
    return f"""你是一位资深网文写手，严格按 pop-zhanggang 章纲流执行。

# 任务
基于以下输入，写{ch}的正文。3100-3500字，不准低于3100字，不准超过3500字。

# zhanggang skill SOP（2步）

## Step 1: 前文分析
{prev_section}
## Step 2: 拆解框架 + 填充细节 + 节奏与收尾

### 2a. 4段式骨架分配篇幅
| 段 | 字数 | 内容 |
|----|------|------|
| 开篇 | 650-750字 | {"渲染场景氛围，交代人物行动动机" if is_first else "衔接前文结尾，渲染场景氛围"} |
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
【第{ch[2:]}章正文 | 为下章铺垫：XXX】

章节名

正文内容...
```

# 深渊主宰笔触DNA（必须遵循）
{dna}

# 本章章纲（核心事件）
{chapter["anchor"]}

# 剧情白描{ch}段（故事流参考）
{chapter["paper"]}

# 开始写作
"""

# ============ API调用 ============
def make_session():
    s = requests.Session()
    s.proxies.update(PROXIES)
    s.verify = False
    return s

def call_api(group, prompt, output_file, max_retries=5):
    session = make_session()
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
        "max_tokens": 32768,
        "temperature": 0.85,
        "stream": False
    }
    
    for attempt in range(max_retries):
        try:
            response = session.post(
                f"{DS_BASE_URL}/chat/completions",
                headers=headers,
                json=payload,
                timeout=300
            )
            response.raise_for_status()
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            output_file.write_text(content, encoding="utf-8")
            return content
        except Exception as e:
            print(f"  第{attempt+1}次失败: {type(e).__name__}: {str(e)[:80]}")
            if attempt < max_retries - 1:
                time.sleep(8)
    return None


# ============ 主程序 ============
print("=" * 60)
print("R40 AB测试 - 5章串行+前章钩子传递")
print("=" * 60)

# A组串行
print("\n>>> A组(write skill)开始 <<<")
a_prev = None
for chapter in CHAPTERS:
    ch = chapter["ch"]
    print(f"\n[A-{ch}] 写作中...")
    prompt = build_a_prompt(chapter, a_prev)
    (INPUTS_DIR / f"A-{ch}_input.md").write_text(prompt, encoding="utf-8")
    
    content = call_api("A", prompt, A_OUTPUT / f"{ch}.md")
    if content:
        print(f"[A-{ch}] 完成，{len(content)}字符")
        a_prev = content
    else:
        print(f"[A-{ch}] 失败，跳过")
        a_prev = None

# B组串行
print("\n>>> B组(zhanggang skill)开始 <<<")
b_prev = None
for chapter in CHAPTERS:
    ch = chapter["ch"]
    print(f"\n[B-{ch}] 写作中...")
    prompt = build_b_prompt(chapter, b_prev)
    (INPUTS_DIR / f"B-{ch}_input.md").write_text(prompt, encoding="utf-8")
    
    content = call_api("B", prompt, B_OUTPUT / f"{ch}.md")
    if content:
        print(f"[B-{ch}] 完成，{len(content)}字符")
        b_prev = content
    else:
        print(f"[B-{ch}] 失败，跳过")
        b_prev = None

print("\n" + "=" * 60)
print("R40 AB测试完成！")
print("=" * 60)
print("\n--- 字符数统计 ---")
for i in range(1, 6):
    ch = f"ch00{i}"
    a_file = A_OUTPUT / f"{ch}.md"
    b_file = B_OUTPUT / f"{ch}.md"
    a_count = len(a_file.read_text(encoding="utf-8")) if a_file.exists() else 0
    b_count = len(b_file.read_text(encoding="utf-8")) if b_file.exists() else 0
    print(f"{ch}: A组={a_count}字符, B组={b_count}字符")
