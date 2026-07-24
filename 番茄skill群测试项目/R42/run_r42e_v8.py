#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
R42e · write skill v8.0.0 测试（减法版）
策略：
  - 组A：trial模式（无DNA）+ write skill v8.0.0结构约束
  - 组B：启用态（DNA）+ write skill v8.0.0结构约束
两本书 × 两组 = 4个并行任务。
对比R42c（trial旧版）和R42d（组合旧版）看减法效果。
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
R42E_INPUT_LOG_DIR = os.path.join(OUTPUT_DIR, "inputs-r42e")
os.makedirs(R42E_INPUT_LOG_DIR, exist_ok=True)

BOOKS = ["玄鉴仙族", "夜无疆"]

# ========== write skill v8.0.0 完整约束（减法版·只留结构）==========
# 公共结构约束（trial和启用态共用）
STRUCTURE_PROMPT = """你是番茄小说正文写作agent，严格遵循pop-fanqie-write skill v8.0.0 的结构约束。

# 4种章型骨架（选1个）

| 章型 | 使用条件 | 7节拍骨架 |
|:----|:--------|:--------|
| opening_shift | 第一章/世界规则松动/金手指激活 | 1起笔(现实常识)→2第一信息变化→3压力/诱因→4主角动作或判断→5阻碍升级(爽感爆发点)→6可见反馈→7章末钩子 |
| confrontation_pressure | 对峙/打脸/信息差博弈/势力试探 | 1敌方给压力→2对方暴露目的/误判→3语言羞辱/身份压制→4沉默/反问/亮筹码→5对方加码(爽感爆发点)→6对方失态/微反转→7矛盾升级 |
| combat_reversal | 战斗/绝境翻盘/首杀/暗杀 | 1明确对方优势→2主角发现缝隙→3对方攻击/羞辱→4不解释直接执行→5对方后手超预期(爽感爆发点)→6身体损伤/法器破碎→7反击引来更高后果 |
| reveal_hook | 揭秘/新敌人/升级/章末钩子 | 1上一场结果余波→2新解释出现→3解释带来更大危险→4选择追查/隐瞒/反击→5新信息牵出更高层(爽感爆发点)→6关系判断改变→7下一章进入新场面 |

# 红线（10条）
1. 每章必须全文加载剧情白描+骨架+current-state
2. 设定库禁止全文注入——只精选与本章相关的2个维度（≤1000字）
3. 第一章由seed产出——write从ch002开始
4. 篇幅硬限制：2000-2500字，不准超过2500字。超2500字=废章
5. 章型必选：每章必须从4种章型中选1个，按7节拍骨架组织结构
6. 爽感≥1/章：每章至少1个爽感触发
7. 章名：每章正文开头必须有正常章节名（贴合内容命名）
8. 笔触DNA标准插槽：见下方模式说明
9. 章末有钩子：每章必须以主动钩子或威胁逼近收尾
10. 不写思考过程/检查表——直接写正文

# 节奏约束速查（结构层·非风格）
| 指标 | 约束 |
|:----|:----|
| 事件间隔 | ≤20行 |
| 事件密度 | 8-12个/章 |
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

# 篇幅控制速查
| 字数区间 | 判断 | 处理 |
|:----|:----|:----|
| 2000-2500字 | 合格 | 完成 |
| 1800-2000字 | 偏短 | 检查信息密度 |
| 2500-3000字 | 超标 | 必须裁剪描述性文字 |
| 超过3000字 | 废章 | 重写 |

# 三层指导
1. 结构层：按章型7节拍骨架组织结构
2. 节奏层：遵守节奏物理量（事件间隔/密度/蓄力/信息释放/微钩子）
3. 爽感层：主推爽感必须触发+爽感闭环+爆发后三段式+小爽沿途+即时奖励

# 字数分配建议
| 段落 | 字数 |
|:----|:----|
| 节拍1-2 | 300-400字 |
| 节拍3-4 | 400-500字 |
| 节拍5 | 500-700字 |
| 节拍6 | 400-500字 |
| 节拍7 | 200-300字 |
| 合计 | 2000-2500字 |

# 写作禁区
禁止：
- 写思考过程/检查表/分析框架
- 章末没有钩子
- 超过2500字

> v8.0.0移除了风格倾向（短句/道引导词/【】面板/动作链必选/多感官必选/感官优先级表/情绪外化/碎片化思考），由DNA决定。"""

# trial模式补充说明
TRIAL_ADDON = """

# 当前模式：trial模式（无笔触DNA）
write skill v8.0.0 不内置任何默认风格。你需要根据剧情梗概自行判断合适的笔触风格，或接受质量波动。
不要套用任何特定网文的风格（如深渊主宰的系统面板/动作链等）——除非DNA明确要求。
交付面板标注"trial模式·无DNA驱动"。"""

# 启用态补充说明
ENABLED_ADDON = """

# 当前模式：启用态（笔触DNA已加载）
你已加载文风DNA（文风锚定.md）。你的笔触层（叙事距离/句式/物象/对话/情绪外化/感官顺序/段落呼吸/系统面板格式）必须从DNA中来，禁止凭空发挥。

# 笔触DNA消费规则（强制）
- 只学笔触：句式节奏、感官顺序、叙事距离、段落呼吸、对话引导词习惯、系统面板格式
- 禁止学内容：不从DNA原文摘录中提取剧情设计、战斗表现、角色思维等内容元素
- DNA描述的是"作者怎么写"，不是"写什么"
- 字数红线优先于DNA段落风格——当DNA的长段风格和字数约束冲突时，压缩段落服从字数"""

def write_r42e(task_name, book_name, mode):
    """R42e单任务"""
    print(f"\n[{task_name}] 开始...")
    
    # 加载剧情梗概
    synopsis_path = os.path.join(INPUT_DIR, f"{book_name}-ch03剧情梗概.md")
    with open(synopsis_path, "r", encoding="utf-8") as f:
        synopsis = f.read()
    
    # 构造system prompt
    if mode == "trial":
        system_prompt = STRUCTURE_PROMPT + TRIAL_ADDON
        dna_text = ""
    else:  # enabled
        dna_path = os.path.join(DNA_DIR, f"{book_name}-文风DNA.md")
        with open(dna_path, "r", encoding="utf-8") as f:
            dna_text = f.read()
        system_prompt = STRUCTURE_PROMPT + ENABLED_ADDON
    
    # 构造user prompt
    if mode == "trial":
        user_prompt = f"""# 本章剧情梗概（中性·不带笔触）

{synopsis}

---

# 任务

请根据上述剧情梗概，按pop-fanqie-write skill v8.0.0结构约束，写出第3章完整正文。

要求：
1. 当前为trial模式（无笔触DNA），write skill不内置任何默认风格
2. 从4种章型中选1个最贴合本章剧情的，按7节拍骨架组织结构
3. 字数2000-2500字，不准超过2500字
4. 章名用正常章节名（贴合内容）
5. 章末钩子（主角主动决策型）
6. 不要套用任何特定网文的风格（如系统面板/动作链等），除非DNA明确要求

直接输出正文（含章名），不需要解释。"""
    else:  # enabled
        user_prompt = f"""# 文风DNA（文风锚定.md · 启用态）

{dna_text}

---

# 本章剧情梗概（中性·不带笔触）

{synopsis}

---

# 任务

请根据上述剧情梗概，按pop-fanqie-write skill v8.0.0结构约束 + 文风DNA驱动笔触，写出第3章完整正文。

要求：
1. 当前为启用态（笔触DNA已加载），笔触层必须从DNA中来
2. 从4种章型中选1个最贴合本章剧情的，按7节拍骨架组织结构
3. 字数2000-2500字，不准超过2500字（字数红线优先于DNA段落风格）
4. 章名用正常章节名（贴合内容）
5. 章末钩子（主角主动决策型）
6. 结构层（章型/节奏/字数/爽感）由write skill约束决定，笔触层（句式/感官/叙事距离）由DNA决定

直接输出正文（含章名），不需要解释。"""

    print(f"[{task_name}] 调用API... 输入: {len(user_prompt) + len(system_prompt)}字符")
    
    url = f"{DS_BASE_URL}/chat/completions"
    headers = {"Authorization": f"Bearer {DS_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": DS_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS,
        "stream": False
    }
    
    # 落盘完整input
    input_log_path = os.path.join(R42E_INPUT_LOG_DIR, f"{task_name}_input.md")
    with open(input_log_path, "w", encoding="utf-8") as f:
        f.write("# SYSTEM PROMPT\n\n" + system_prompt + "\n\n---\n\n# USER PROMPT\n\n" + user_prompt)
    
    start = time.time()
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=TIMEOUT)
        response.raise_for_status()
        elapsed = time.time() - start
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        usage = result.get("usage", {})
        print(f"[{task_name}] 完成! {elapsed:.1f}s | {len(content)}字 | tokens:{usage.get('total_tokens','N/A')}")
        
        out_path = os.path.join(OUTPUT_DIR, f"r42e-{task_name}.md")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[{task_name}] 正文已落盘: {out_path}")
        
        return {
            "task": task_name,
            "book": book_name,
            "mode": mode,
            "model": DS_MODEL,
            "output_length": len(content),
            "elapsed": round(elapsed, 1),
            "usage": usage,
            "input_chars": len(user_prompt) + len(system_prompt),
            "output_path": out_path,
        }
    except Exception as e:
        print(f"[{task_name}] 错误: {e}")
        return {"task": task_name, "error": str(e)}

def main():
    print("="*60)
    print("R42e · write skill v8.0.0 测试（减法版）")
    print("="*60)
    
    # 4个任务并行：2本书 × 2模式
    tasks = [
        ("trial-玄鉴仙族", "玄鉴仙族", "trial"),
        ("trial-夜无疆", "夜无疆", "trial"),
        ("enabled-玄鉴仙族", "玄鉴仙族", "enabled"),
        ("enabled-夜无疆", "夜无疆", "enabled"),
    ]
    
    metas = []
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(write_r42e, name, book, mode): name for name, book, mode in tasks}
        for future in as_completed(futures):
            name = futures[future]
            try:
                metas.append(future.result())
            except Exception as e:
                print(f"[{name}] 线程错误: {e}")
                metas.append({"task": name, "error": str(e)})
    
    metas.sort(key=lambda x: x.get("task", ""))
    with open(os.path.join(OUTPUT_DIR, "meta-r42e.json"), "w", encoding="utf-8") as f:
        json.dump({"round": "R42e", "task": "v8.0.0_test", "tasks": metas}, f, ensure_ascii=False, indent=2)
    
    print("\n" + "="*60)
    print("R42e测试完成!")
    for m in metas:
        if "error" in m:
            print(f"  {m['task']}: 错误 - {m['error']}")
        else:
            print(f"  {m['task']}: {m['output_length']}字 | {m['elapsed']}s")
    print("="*60)

if __name__ == "__main__":
    main()
