#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
R42b · 交叉试写脚本
策略：
  组A：夜无疆剧情梗概 + 玄鉴仙族笔触DNA
  组B：玄鉴仙族剧情梗概 + 夜无疆笔触DNA
两轮并行，看交叉后像什么。
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

# 绕过代理
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
CROSS_INPUT_LOG_DIR = os.path.join(OUTPUT_DIR, "inputs-cross")
os.makedirs(CROSS_INPUT_LOG_DIR, exist_ok=True)

# 交叉组合：(组名, 剧情来源, DNA来源)
CROSS_PAIRS = [
    ("A-夜无疆剧情+玄鉴笔触", "夜无疆", "玄鉴仙族"),
    ("B-玄鉴剧情+夜无疆笔触", "玄鉴仙族", "夜无疆"),
]

SYSTEM_PROMPT = """你是番茄小说正文写作agent，严格遵循pop-fanqie-write skill的笔触DNA标准插槽协议。

# 笔触DNA标准插槽·启用态
你已加载文风DNA（文风锚定.md）。你的笔触层（叙事距离/句式/物象/对话/情绪外化）必须从DNA中来，禁止凭空发挥。

# 消费规则（强制）
- 只学笔触：句式节奏、感官顺序、叙事距离、段落呼吸、对话引导词习惯
- 禁止学内容：不从DNA原文摘录中提取剧情设计、战斗表现、角色思维等内容元素
- DNA描述的是"作者怎么写"，不是"写什么"

# 节奏物理量（番茄强制）
- 事件间隔≤20行
- 感官描写≤3行
- 情绪描写≤2行
- 事件密度8-12个/章
- 每章≥1个爽感点

# 章型：标准推进章
- 开场（3-5行）：用动作或感官切入，不用背景叙述开场
- 中段：事件推进，每个事件≤20行收束
- 章末钩子：主角主动决策型，禁止被动接收型

# 格式约束
- 章名：正常章节名，贴合内容命名
- 系统面板用【】内联格式，禁止markdown代码块
- 角色思考用碎片化表达，避免完整分析句
- 字数：2000-2500字，不准超过3000字（字数红线优先于DNA段落风格）

# 关键
你的任务是：根据给定的剧情梗概，用文风DNA驱动的笔触写出正文。
梗概只说"发生了什么"，你要用DNA决定"怎么写"。
笔触一致性是最高优先级——读你写出来的东西，应该像参考书作者本人写的。"""

def write_cross(pair_name, synopsis_book, dna_book):
    """交叉试写"""
    print(f"\n[{pair_name}] 开始...")
    
    # 加载DNA（来自dna_book）
    dna_path = os.path.join(DNA_DIR, f"{dna_book}-文风DNA.md")
    with open(dna_path, "r", encoding="utf-8") as f:
        dna = f.read()
    print(f"[{pair_name}] DNA来源: {dna_book} ({len(dna)}字符)")
    
    # 加载剧情梗概（来自synopsis_book）
    synopsis_path = os.path.join(INPUT_DIR, f"{synopsis_book}-ch03剧情梗概.md")
    with open(synopsis_path, "r", encoding="utf-8") as f:
        synopsis = f.read()
    print(f"[{pair_name}] 剧情来源: {synopsis_book} ({len(synopsis)}字符)")
    
    user_prompt = f"""# 文风DNA（文风锚定.md）

{dna}

---

# 本章剧情梗概（中性·不带笔触）

{synopsis}

---

# 任务

请根据上述剧情梗概，用文风DNA驱动的笔触，写出完整正文。

要求：
1. 笔触必须从DNA中来——叙事距离、句式节奏、感官顺序、对话引导词、情绪外化方式，都按DNA描述的特征来写
2. 字数2000-2500字，不准超过3000字（字数红线优先于DNA段落风格）
3. 章名用正常章节名（贴合内容）
4. 按标准推进章结构：开场(3-5行动作/感官切入)→中段事件推进→章末钩子(主角主动决策型)
5. 系统面板用【】内联格式
6. 角色思考碎片化表达

直接输出正文（含章名），不需要解释。"""

    print(f"[{pair_name}] 调用API... 输入: {len(user_prompt)}字符")
    
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
    input_log_path = os.path.join(CROSS_INPUT_LOG_DIR, f"{pair_name}_input.md")
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
        print(f"[{pair_name}] 完成! {elapsed:.1f}s | {len(content)}字 | tokens:{usage.get('total_tokens','N/A')}")
        
        # 落盘正文
        out_path = os.path.join(OUTPUT_DIR, f"交叉-{pair_name}.md")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[{pair_name}] 正文已落盘: {out_path}")
        
        return {
            "pair": pair_name,
            "synopsis_source": synopsis_book,
            "dna_source": dna_book,
            "model": DS_MODEL,
            "output_length": len(content),
            "elapsed": round(elapsed, 1),
            "usage": usage,
            "input_chars": len(user_prompt) + len(SYSTEM_PROMPT),
            "output_path": out_path,
            "input_log_path": input_log_path,
        }
    except Exception as e:
        print(f"[{pair_name}] 错误: {e}")
        return {"pair": pair_name, "error": str(e)}

def main():
    print("="*60)
    print("R42b · 交叉试写（两组并行）")
    print("="*60)
    
    metas = []
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = {executor.submit(write_cross, name, syn, dna): name 
                   for name, syn, dna in CROSS_PAIRS}
        for future in as_completed(futures):
            name = futures[future]
            try:
                metas.append(future.result())
            except Exception as e:
                print(f"[{name}] 线程错误: {e}")
                metas.append({"pair": name, "error": str(e)})
    
    metas.sort(key=lambda x: x.get("pair", ""))
    with open(os.path.join(OUTPUT_DIR, "meta-cross.json"), "w", encoding="utf-8") as f:
        json.dump({"round": "R42b", "task": "cross_write_test", "pairs": metas}, f, ensure_ascii=False, indent=2)
    
    print("\n" + "="*60)
    print("交叉试写完成!")
    for m in metas:
        if "error" in m:
            print(f"  {m['pair']}: 错误 - {m['error']}")
        else:
            print(f"  {m['pair']}: {m['output_length']}字 | {m['elapsed']}s")
    print("="*60)

if __name__ == "__main__":
    main()
