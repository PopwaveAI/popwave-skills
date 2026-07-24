"""
R38 write skill 测试脚本
严格按 pop-fanqie-write v7.3.0 执行
精选注入: 前章ch001 + 当前章锚点 + 剧情白描相关段
并行调用API写ch002~ch005
"""
import json
import concurrent.futures
from pathlib import Path
import requests

# ============ 配置 ============
DS_API_KEY = "sk-5a3654e4aa2e4eefa08abe3d0e0231f5"
DS_BASE_URL = "https://api.deepseek.com/v1"
DS_MODEL = "deepseek-v4-flash"

R38_DIR = Path(r"d:\popwave-skills\番茄skill群测试项目\R38")
CH001_FILE = R38_DIR / "01-seed" / "ch001.md"
WHITE_PAPER_FILE = R38_DIR / "02-plot" / "卷1剧情白描.md"
SKELETON_FILE = R38_DIR / "02-plot" / "骨架.md"
IDEA_FILE = R38_DIR / "01-seed" / "创意.md"
OUTPUT_DIR = R38_DIR / "03-write"
INPUT_DIR = R38_DIR / "03-write" / "inputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
INPUT_DIR.mkdir(parents=True, exist_ok=True)

# ============ 加载共享文件 ============
ch001 = CH001_FILE.read_text(encoding="utf-8")
white_paper = WHITE_PAPER_FILE.read_text(encoding="utf-8")
skeleton = SKELETON_FILE.read_text(encoding="utf-8")
idea_doc = IDEA_FILE.read_text(encoding="utf-8")

# ============ 章节场景卡（从骨架.md章锚点表提取） ============
CHAPTERS = [
    {
        "ch": "ch002",
        "章型": "成长",
        "核心事件": "加列夫抱薇薇安到达德鲁伊树林，与提夫林首领哈林建立临时关系，发现树林里有两个蝌蚪宿主，影心出场",
        "爽点": "未知揭示：发现树林里有蝌蚪宿主+蝌蚪识别反应",
        "钩子": "影心的Shar圣徽+加列夫的蝌蚪扭动指向影心",
        "预期回收章": "ch003",
        "关键数据": "种子96%→95%，蝌蚪5%→6%",
        "白描段关键词": "从月出之塔的绿光开始",
        "白描段起止": (3, 95)  # 行号
    },
    {
        "ch": "ch003",
        "章型": "披露",
        "核心事件": "德鲁伊草药师内蒂检查加列夫，影心试探加列夫，薇薇安首次术士觉醒，哈林请求加列夫清除地精",
        "爽点": "未知揭示：薇薇安的术士体质+加列夫主动提出跟影心合作",
        "钩子": "薇薇安能感应帝皇余烬+加列夫一个人走向地精营地",
        "预期回收章": "ch004",
        "关键数据": "种子95%→94%，薇薇安魔力觉醒",
        "白描段关键词": "德鲁伊的草药师·影心的试探",
        "白描段起止": (97, 183)
    },
    {
        "ch": "ch004",
        "章型": "对抗",
        "核心事件": "加列夫前往地精营地，与明萨拉第一次冲突，灵能感知LV2激活，明萨拉用水晶球逃走",
        "爽点": "压力突破：灵能感知LV2激活+帝皇之焰对明萨拉",
        "钩子": "明萨拉逃走报告凯瑟里克，加速追杀节奏",
        "预期回收章": "ch005",
        "关键数据": "种子94%→92%，蝌蚪6%→9%，LV2激活",
        "白描段关键词": "地精营地外围·明萨拉的伏击",
        "白描段起止": (185, 257)
    },
    {
        "ch": "ch005",
        "章型": "揭示",
        "核心事件": "地精营地核心清除三首领，帝皇之焰·解放，发现余烬能烧断蝌蚪绑定（隐藏属性），明萨拉投降，获得月出之塔三件宝物情报",
        "爽点": "压力突破+未知揭示：帝皇之焰·解放+隐藏属性发现",
        "钩子": "月出之塔三件宝物+三天时间窗口+需要影心",
        "预期回收章": "ch006",
        "关键数据": "种子92%→88%，蝌蚪9%→12%",
        "白描段关键词": "地精营地核心",
        "白描段起止": (259, 339)
    }
]

# ============ 构造每章的精选注入 ============
def build_prompt(chapter, prev_chapter_text=None):
    """构造每章的精选注入prompt"""
    ch = chapter["ch"]
    
    # 从白描提取相关段
    lines = white_paper.split('\n')
    start, end = chapter["白描段起止"]
    white_paper_segment = '\n'.join(lines[start-1:end])
    
    # 构造system prompt
    system_prompt = f"""你是一位资深番茄网文写手，严格按 pop-fanqie-write v7.3.0 执行。

# 任务
基于以下输入，写{ch}的正文。2000-2500字，不准超过2500字。

# write skill SOP（5步）

## Step 1: 加载
- 加载本章锚点（章型/核心事件/爽点/钩子）
- 加载剧情白描{ch}段（本章的故事流参考）
- {"加载前章ch001的章末钩子（本章前300字必须回收）" if prev_chapter_text else "本章是第一章，使用黄金开篇"}

## Step 2: 章型骨架
- {chapter["章型"]}章型结构
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
3. ch002必须回收ch001的章末钩子（月出之塔绿光+蝌蚪指向塔）
4. 动作链≥3处，多感官场景≥2处
5. 章末必须有钩子

# 本章锚点
- 章号: {ch}
- 章型: {chapter["章型"]}
- 核心事件: {chapter["核心事件"]}
- 爽点: {chapter["爽点"]}
- 钩子: {chapter["钩子"]}
- 关键数据: {chapter["关键数据"]}

# 剧情白描{ch}段（故事流参考）
{white_paper_segment}

# 金手指设定（创意文档摘要）
- 帝皇余烬：基因种子被夺心魔蝌蚪催化成"帝皇余烬"
- 限制：基因种子不可再生，每次使用消耗；蝌蚪在学习灵能
- 升级路径: LV1余烬初燃→LV2灵能感知→LV3灵能屏障→LV4审判之火→LV5帝皇投影

# 笔触约束
- 系统面板格式：【状态 | 字段：值】
- 角色思考：碎片化，不写完整分析句
- 动作链：拆细动作
- 多感官：每场景≥3种感官
"""

    # ch002+需要前章
    if prev_chapter_text:
        # 只取前章的正文+交付面板的章末钩子
        prev_lines = prev_chapter_text.split('\n')
        prev_segment = '\n'.join(prev_lines[:50])  # 前50行作为前章参考
        system_prompt += f"\n# 前章参考（ch001黄金首章）\n{prev_segment}\n"

    return system_prompt


def call_api(chapter, prev_text=None):
    """调用API写章节"""
    ch = chapter["ch"]
    prompt = build_prompt(chapter, prev_text)
    
    # 保存input
    input_file = INPUT_DIR / f"{ch}_input.md"
    input_file.write_text(prompt, encoding="utf-8")
    
    print(f"[{ch}] 开始写作...")
    
    headers = {
        "Authorization": f"Bearer {DS_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": DS_MODEL,
        "messages": [
            {"role": "system", "content": "你是一位资深番茄网文写手，严格按write skill SOP执行。"},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 4000,
        "temperature": 0.85,
        "stream": False
    }
    
    try:
        response = requests.post(
            f"{DS_BASE_URL}/chat/completions",
            headers=headers,
            json=payload,
            timeout=300
        )
        response.raise_for_status()
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        
        # 落盘output
        output_file = OUTPUT_DIR / f"{ch}.md"
        output_file.write_text(content, encoding="utf-8")
        print(f"[{ch}] 完成，{len(content)}字符")
        return ch, content
    except Exception as e:
        print(f"[{ch}] 失败: {e}")
        return ch, None


# ============ 串行执行（每章依赖前章）============
print("=" * 60)
print("R38 write skill 测试 - ch002~ch005 串行执行")
print("=" * 60)

results = {}
prev_text = ch001  # ch002的前章是ch001

for chapter in CHAPTERS:
    ch, content = call_api(chapter, prev_text)
    results[ch] = content
    if content:
        prev_text = content  # 下一章的前章是本章
    print(f"[{ch}] 已完成，作为下一章的前章输入")
    print("-" * 40)

print("\n" + "=" * 60)
print("全部完成！")
print("=" * 60)
for ch, content in results.items():
    if content:
        print(f"{ch}: {len(content)}字符")
    else:
        print(f"{ch}: 失败")
