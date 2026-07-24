#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
R42d · DNA + write skill完整约束组合版
策略：
  - 注入文风DNA（启用态）
  - 注入write skill完整约束（红线+章型+节奏+爽感+微观技法+五层指导+写作禁区）
  - 两本各自的剧情梗概
  - 验证"标准插槽启用态"应该跑出来的效果
两本书并行。
"""
import os, sys, json, time, requests
from concurrent.futures import ThreadPoolExecutor, as_completed

# ========== 配置 ==========
DS_API_KEY = "sk-5a3654e4aa2e4eefa08abe3d0e0231f5"
DS_BASE_URL = "https://api.deepseek.com/v1"
DS_MODEL = "deepseek-v4-flash"
TEMPERATURE = 0.75
MAX_TOKENS = 8000
TIMEOUT = 600

os.environ['no_proxy'] = '*'
os.environ['NO_PROXY'] = '*'
os.environ.pop('http_proxy', None)
os.environ.pop('https_proxy', None)
os.environ.pop('HTTP_PROXY', None)
os.environ.pop('HTTPS_PROXY', None)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DNA_DIR = os.path.join(SCRIPT_DIR, "01-dna")
INPUT_DIR = os.path.join(SCRIPT_DIR, "02-write", "inputs")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "02-write")
COMBO_INPUT_LOG_DIR = os.path.join(OUTPUT_DIR, "inputs-combo")
os.makedirs(COMBO_INPUT_LOG_DIR, exist_ok=True)

BOOKS = ["玄鉴仙族", "夜无疆"]

# ========== write skill 完整约束（启用态·有DNA）==========
SYSTEM_PROMPT = """你是番茄小说正文写作agent，严格遵循pop-fanqie-write skill v7.4.0 的完整约束。

# 当前模式：启用态（笔触DNA已加载）
你已加载文风DNA（文风锚定.md）。你的笔触层（叙事距离/句式/物象/对话/情绪外化）必须从DNA中来，禁止凭空发挥。

# 笔触DNA消费规则（强制）
- 只学笔触：句式节奏、感官顺序、叙事距离、段落呼吸、对话引导词习惯
- 禁止学内容：不从DNA原文摘录中提取剧情设计、战斗表现、角色思维等内容元素
- DNA描述的是"作者怎么写"，不是"写什么"

# 4种章型骨架（选1个）

| 章型 | 使用条件 | 7节拍骨架 |
|:----|:--------|:--------|
| opening_shift | 第一章/世界规则松动/金手指激活 | 1起笔(现实常识)→2第一信息变化→3压力/诱因→4主角动作或判断→5阻碍升级(爽感爆发点)→6可见反馈→7章末钩子 |
| confrontation_pressure | 对峙/打脸/信息差博弈/势力试探 | 1敌方给压力→2对方暴露目的/误判→3语言羞辱/身份压制→4沉默/反问/亮筹码→5对方加码(爽感爆发点)→6对方失态/微反转→7矛盾升级 |
| combat_reversal | 战斗/绝境翻盘/首杀/暗杀 | 1明确对方优势→2主角发现缝隙→3对方攻击/羞辱→4不解释直接执行→5对方后手超预期(爽感爆发点)→6身体损伤/法器破碎→7反击引来更高后果 |
| reveal_hook | 揭秘/新敌人/升级/章末钩子 | 1上一场结果余波→2新解释出现→3解释带来更大危险→4选择追查/隐瞒/反击→5新信息牵出更高层(爽感爆发点)→6关系判断改变→7下一章进入新场面 |

# 红线（13条）
1. 每章必须全文加载剧情白描+骨架+current-state——禁止用current-state替代立项包
2. 设定库禁止全文注入——只精选与本章相关的2个维度（≤1000字）
3. 第一章由seed产出——write从ch002开始
4. 篇幅硬限制：2000-2500字，不准超过2500字。超2500字=废章，必须裁剪
5. 章型必选：每章必须从4种章型中选1个，按7节拍骨架组织结构
6. 爽感≥1/章：每章至少1个爽感触发
7. 微观技法选择：必须选3-4类微观技法并落地（含动作链+多感官优先级，必选）
8. 动作链硬约束：禁止用1个动词概括连续动作，必须拆成2-3个细动作。每章≥3处，战斗章≥5处
9. 多感官硬约束：每场景至少覆盖3种感官，每章≥2处完整多感官描写，战斗章≥3处
10. 章名：每章正文开头必须有正常章节名（贴合内容命名）
11. 笔触DNA标准插槽：当前为启用态，笔触层必须从DNA中来，禁止凭空发挥
12. 章末有钩子：每章必须以主动钩子或威胁逼近收尾
13. 不写思考过程/检查表——直接写正文

# 节奏约束速查（番茄12岁小学生读者模型）
| 指标 | 约束 |
|:----|:----|
| 事件间隔 | ≤20行 |
| 感官连续 | ≤3行 |
| 情绪连续 | ≤2行 |
| 事件密度 | 8-12个/章 |
| 爽感触发 | ≥1个/章 |
| 蓄力上限 | ≤2段 |
| 信息释放 | ≤3段 |
| 微钩子 | 每3-5行 |

# 爽感速查
| 机制 | 要求 |
|:----|:----|
| 打脸循环 | 轻视≥2层，翻盘≤3行，对方有可见失态 |
| 小爽链 | 每3-5事件≥1个小爽，大爽前≥2个铺垫 |
| 爆发后三段式 | 爆发→反馈≤2段→余韵≥1段→下一事件 |
| 即时奖励 | 每章≥1次行动→可见回报闭环 |

# 微观技法速查（8类，必选动作链+多感官优先级）
| 技法 | 一句话定义 | 何时选 |
|:----|:----|:----|
| 信息差博弈 | 围绕"谁知道什么"设计博弈 | 对峙章/开篇章 |
| 感官锚点 | 用具体生理感官细节建立代入感 | 所有章型可选 |
| 动作链 ⭐ | 拆解连续动作成2-3个细动作，禁止概括式 | 战斗章/动作密集章必选 |
| 多感官优先级 ⭐ | 每场景至少覆盖3种感官 | 所有章型必选 |
| 预期违背 | 故意建立读者预期，然后打破它 | 揭秘章/开篇章 |
| 节奏微操 | 一章内快慢交替、张弛有度 | 战斗章/对峙章 |
| 人设微操 | 通过小动作/小习惯让角色立体 | 对峙章 |
| 后果链设计 | 章内事件不闭环，产生可见后果涟漪 | 战斗章/揭秘章 |

# 篇幅控制速查
| 字数区间 | 判断 | 处理 |
|:----|:----|:----|
| 2000-2500字 | 合格 | 完成 |
| 1800-2000字 | 偏短 | 检查信息密度 |
| 2500-3000字 | 超标 | 必须裁剪描述性文字 |
| 超过3000字 | 废章 | 重写 |

# 五层指导
1. 笔触层：启用态，从DNA取笔触特征（句式/感官/叙事距离/对话/情绪外化）
2. 节奏层：遵守节奏物理量，按章型7节拍骨架组织
3. 格局层：本章在长线中的位置+势力格局变化+世界观信息释放
4. 爽感层：主推爽感必须触发+爽感闭环（触发→爆发→后果）+爆发后三段式+小爽沿途+即时奖励
5. 微观层：落地选的3-4类微观技法（含动作链+多感官必选）

# 写作禁区
禁止：
- 写思考过程/检查表/分析框架
- 用markdown代码块写系统面板（用【】内联）
- 对话引导词用"说/问/答"（只用"道"）
- 直接写"他感到悲伤/愤怒"（用动作/物象外化）
- 角色大段内心独白（碎片化表达）
- 章末没有钩子
- 超过2500字
- 用1个动词概括连续动作
- 场景只覆盖1种感官

# 字数分配建议
| 段落 | 字数 |
|:----|:----|
| 节拍1-2 | 300-400字 |
| 节拍3-4 | 400-500字 |
| 节拍5 | 500-700字 |
| 节拍6 | 400-500字 |
| 节拍7 | 200-300字 |
| 合计 | 2000-2500字 |

# 关键
- 结构层（章型/节奏/字数/爽感/微观技法）由write skill约束决定
- 笔触层（句式/感官顺序/叙事距离/对话引导词/情绪外化）由DNA决定
- 两者不冲突，是互补关系：DNA管"怎么写"，约束管"写什么结构"
- 字数红线优先于DNA段落风格——当DNA的长段风格和字数约束冲突时，压缩段落服从字数"""

def write_combo(book_name):
    """DNA + write skill完整约束组合版"""
    print(f"\n[{book_name}] 开始组合版试写...")
    
    # 加载DNA
    dna_path = os.path.join(DNA_DIR, f"{book_name}-文风DNA.md")
    with open(dna_path, "r", encoding="utf-8") as f:
        dna = f.read()
    print(f"[{book_name}] DNA加载: {len(dna)}字符")
    
    # 加载剧情梗概
    synopsis_path = os.path.join(INPUT_DIR, f"{book_name}-ch03剧情梗概.md")
    with open(synopsis_path, "r", encoding="utf-8") as f:
        synopsis = f.read()
    print(f"[{book_name}] 梗概加载: {len(synopsis)}字符")
    
    user_prompt = f"""# 文风DNA（文风锚定.md · 启用态）

{dna}

---

# 本章剧情梗概（中性·不带笔触）

{synopsis}

---

# 任务

请根据上述剧情梗概，按pop-fanqie-write skill完整约束 + 文风DNA驱动笔触，写出第3章完整正文。

要求：
1. 当前为启用态（笔触DNA已加载），笔触层必须从DNA中来
2. 从4种章型中选1个最贴合本章剧情的，按7节拍骨架组织结构
3. 选3-4类微观技法（含动作链+多感官优先级必选）并落地
4. 字数2000-2500字，不准超过2500字（字数红线优先于DNA段落风格）
5. 章名用正常章节名（贴合内容）
6. 章末钩子（主角主动决策型）
7. 系统面板用【】内联格式
8. 角色思考碎片化表达
9. 结构层（章型/节奏/字数/爽感）由write skill约束决定，笔触层（句式/感官/叙事距离）由DNA决定

直接输出正文（含章名），不需要解释，不需要写思考过程。"""

    print(f"[{book_name}] 调用API... 输入: {len(user_prompt) + len(SYSTEM_PROMPT)}字符")
    
    url = f"{DS_BASE_URL}/chat/completions"
    headers = {"Authorization": f"Bearer {DS_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": DS_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS,
        "stream": False
    }
    
    # 落盘完整input
    input_log_path = os.path.join(COMBO_INPUT_LOG_DIR, f"{book_name}-combo_input.md")
    with open(input_log_path, "w", encoding="utf-8") as f:
        f.write("# SYSTEM PROMPT\n\n" + SYSTEM_PROMPT + "\n\n---\n\n# USER PROMPT\n\n" + user_prompt)
    
    start = time.time()
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=TIMEOUT)
        response.raise_for_status()
        elapsed = time.time() - start
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        usage = result.get("usage", {})
        print(f"[{book_name}] 完成! {elapsed:.1f}s | {len(content)}字 | tokens:{usage.get('total_tokens','N/A')}")
        
        out_path = os.path.join(OUTPUT_DIR, f"combo-{book_name}-ch03.md")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[{book_name}] 正文已落盘: {out_path}")
        
        return {
            "book": book_name,
            "mode": "dna+write-skill-combo",
            "model": DS_MODEL,
            "output_length": len(content),
            "elapsed": round(elapsed, 1),
            "usage": usage,
            "input_chars": len(user_prompt) + len(SYSTEM_PROMPT),
            "output_path": out_path,
            "input_log_path": input_log_path,
        }
    except Exception as e:
        print(f"[{book_name}] 错误: {e}")
        return {"book": book_name, "error": str(e)}

def main():
    print("="*60)
    print("R42d · DNA + write skill完整约束组合版（启用态）")
    print("="*60)
    
    metas = []
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = {executor.submit(write_combo, name): name for name in BOOKS}
        for future in as_completed(futures):
            name = futures[future]
            try:
                metas.append(future.result())
            except Exception as e:
                print(f"[{name}] 线程错误: {e}")
                metas.append({"book": name, "error": str(e)})
    
    metas.sort(key=lambda x: x.get("book", ""))
    with open(os.path.join(OUTPUT_DIR, "meta-combo.json"), "w", encoding="utf-8") as f:
        json.dump({"round": "R42d", "task": "dna_write_combo", "mode": "enabled", "books": metas}, f, ensure_ascii=False, indent=2)
    
    print("\n" + "="*60)
    print("组合版试写完成!")
    for m in metas:
        if "error" in m:
            print(f"  {m['book']}: 错误 - {m['error']}")
        else:
            print(f"  {m['book']}: {m['output_length']}字 | {m['elapsed']}s")
    print("="*60)

if __name__ == "__main__":
    main()
