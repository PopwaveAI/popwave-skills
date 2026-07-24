#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
R42 · 文风DNA提取脚本
策略：每本书采20章（前10章全读+中段5章+后段5章），送API按pop-shared-dna v4模板提取笔触DNA。
两本书并行提取。
"""
import os, sys, json, time, re, requests, threading
from concurrent.futures import ThreadPoolExecutor, as_completed

# 绕过代理（本地环境代理未开启）
os.environ['no_proxy'] = '*'
os.environ['NO_PROXY'] = '*'
os.environ.pop('http_proxy', None)
os.environ.pop('https_proxy', None)
os.environ.pop('HTTP_PROXY', None)
os.environ.pop('HTTPS_PROXY', None)

# ========== 配置 ==========
DS_API_KEY = "sk-5a3654e4aa2e4eefa08abe3d0e0231f5"
DS_BASE_URL = "https://api.deepseek.com/v1"
DS_MODEL = "deepseek-v4-flash"
TEMPERATURE = 0.7
MAX_TOKENS = 16000
TIMEOUT = 600

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "01-dna")
os.makedirs(OUTPUT_DIR, exist_ok=True)

BOOKS = {
    "玄鉴仙族": {
        "path": r"D:\popwave-skills\workspace\参考小说txt\起点top20\玄鉴仙族-季越人.txt",
        "total_chapters": 1482,
        "mid_start": 740,   # 中段起始章号
        "late_start": 1470,  # 后段起始章号
    },
    "夜无疆": {
        "path": r"D:\popwave-skills\workspace\参考小说txt\起点top20\夜无疆-辰东.txt",
        "total_chapters": 758,
        "mid_start": 370,
        "late_start": 748,
    },
}

# v4模板核心要求（精简版，注入API prompt）
V4_TEMPLATE = """# 文风DNA档案 · 模板 v4

## 格式规则
- 平铺，无章节编号。每个维度/场景卡一节 H2 标题。
- 每个项目 = 观察 (1-2句) + 原文 (≥500字) + 时间演变 (1-2句)，三者不可缺一。
- 原文保留原生段落感——按章逐行摘录，保持可读性。
- 来源标注用斜体——`> _——CH{N}，一句话说明_` 跟在原文块后。
- ⚠️ 消费警告：'观察'字段描述的是作者的笔触特征（句式节奏/叙事距离/感官顺序/对话方式），不是'内容改写指令'。

## 一、场景卡矩阵 (≥6个必选)
| 场景卡 | scene字段值 | 选择标准 |
|战斗·早期遭遇战|combat_early_skirmish|主角早期，对手同级或杂兵|
|战斗·中坚boss战|combat_mid_boss|单挑boss，有招式名对抗|
|对话·日常|dialogue_daily|短对话，≤2人|
|对话·情感高潮|dialogue_emotional|眼泪/告白/告别/久别重逢|
|对话·信息交换|dialogue_intel|打听/功能对话|
|描写·环境引入|description_environment|新场景首次出场，从感官进入|
|描写·角色外貌|description_character|首次出场/换装|
|叙述·孤独紧张|narration_suspense|独处/听动静/计算|
|叙述·过渡缓冲|narration_transition|战后收尾/清晨/赶路|
不硬套不存在的卡。

## 二、通用维度 (≥4个必选)
| 维度 | 要回答的问题 |
|叙事者距离|叙事者离角色多近？进入内心还是只跟视线？|
|情绪传递|情绪通过动作/对话/直述中的哪一种？|
|对话·引导词|引导词密度？零引导词/动作前置/完整引导词比例|
|外貌描写|通过身体状态还是形容词直述？|
|数据嵌入|面板/装备/升级怎么呈现？|
|环境展开|每章从什么感官启动？|
|段落呼吸|独句段的使用频率和功能？|
|物品/装备描写|物品如何呈现？|

## 三、全书稳定特征 (2条必选)

## 禁止事项
- ❌ 不统计词频/句长/修辞密度
- ❌ 不写禁令清单
- ❌ 不把单章偶然细节当全书规律
- ❌ 任何维度/场景卡的原文 < 500 字 → 退回重采
- ❌ 任何项目无"时间演变"段 → 退回
- ❌ 不接受降级替换——找不到匹配段 → 退回扩采"""

# ========== 章节解析 ==========
CHAP_RE = re.compile(r'^第([0-9]+)章\s*(.*)')

def parse_chapters(path):
    """解析全书章节，返回 {章号: 正文} 字典"""
    with open(path, "r", encoding="utf-8") as f:
        lines = f.read().split('\n')
    
    marks = []
    seen = set()
    for i, line in enumerate(lines):
        m = CHAP_RE.match(line.strip())
        if m:
            ch = int(m.group(1))
            title = m.group(2).strip()
            if any(kw in title for kw in ['审核','稍等','大家','抱歉','说明','公告','上架','感言','请假','番外','悬赏','加更','爆发','总结','心路','完本','终结']):
                continue
            if ch not in seen and ch >= 1:
                marks.append((ch, i, title))
                seen.add(ch)
    marks.sort(key=lambda x: x[0])
    
    chapters = {}
    for idx, (ch, start, title) in enumerate(marks):
        end = marks[idx+1][1] if idx+1 < len(marks) else len(lines)
        text = '\n'.join(lines[start:end]).strip()
        chapters[ch] = text
    return chapters

def sample_chapters(chapters, mid_start, late_start):
    """采样20章：前10章 + 中段5章(每2章取1章) + 后段5章(每2章取1章)
    当目标章不存在时，向后找最近的可用章"""
    all_chs = sorted(chapters.keys())
    target = set()
    # 前10章
    for i in range(1, 11):
        if i in chapters:
            target.add(i)
        else:
            # 向后找最近的
            for ch in all_chs:
                if ch > i:
                    target.add(ch)
                    break
    # 中段5章（每2章取1章，目标5个）
    mid_count = 0
    i = mid_start
    while mid_count < 5 and i < mid_start + 20:
        if i in chapters and i not in target:
            target.add(i)
            mid_count += 1
        i += 2
    # 后段5章
    late_count = 0
    i = late_start
    while late_count < 5 and i < late_start + 20:
        if i in chapters and i not in target:
            target.add(i)
            late_count += 1
        i += 2
    return sorted(target)

# ========== API调用 ==========
def extract_dna(book_name, book_config):
    """提取单本书的文风DNA"""
    print(f"\n[{book_name}] 开始提取...")
    
    # 解析章节
    chapters = parse_chapters(book_config["path"])
    print(f"[{book_name}] 解析到 {len(chapters)} 章")
    
    # 采样
    sampled = sample_chapters(chapters, book_config["mid_start"], book_config["late_start"])
    print(f"[{book_name}] 采样 {len(sampled)} 章: {sampled}")
    
    # 拼接采样章节
    book_text = "\n\n".join(chapters[ch] for ch in sampled)
    total_chars = len(book_text)
    total_lines = book_text.count('\n')
    print(f"[{book_name}] 采样内容: {total_chars}字符 | {total_lines}行")
    
    # 构造prompt
    user_prompt = f"""你是网文文风分析专家。请按照以下文风DNA模板，对参考书进行笔触DNA提取。

# 文风DNA模板（v4）

{V4_TEMPLATE}

# 参考书采样正文（共{len(sampled)}章，前10章+中段5章+后段5章采样）

{book_text}

# 任务

按上述v4模板，对这本参考书进行完整笔触DNA提取。要求：
1. 选≥4个通用维度 + ≥6个场景卡（只选采样范围内真实出现的场景类型）
2. 每个维度/场景卡必须含：观察(1-2句) + 原文(≥500字) + 时间演变(1-2句)
3. 原文必须从上方采样正文中摘录，保留原生段落感，标注章节号
4. 写2条全书稳定特征
5. 观察/时间演变只描述笔触特征（句式/感官/叙事距离/对话方式），不描述剧情内容
6. 采样范围有限，在文档头部标注"采样受限·{len(sampled)}章"

直接输出完整DNA文档（markdown格式），不需要分段确认。"""

    print(f"[{book_name}] 调用API... 输入: {len(user_prompt)}字符")
    
    url = f"{DS_BASE_URL}/chat/completions"
    headers = {"Authorization": f"Bearer {DS_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": DS_MODEL,
        "messages": [{"role": "user", "content": user_prompt}],
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS,
        "stream": False
    }
    
    start = time.time()
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=TIMEOUT)
        response.raise_for_status()
        elapsed = time.time() - start
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        usage = result.get("usage", {})
        print(f"[{book_name}] 完成! {elapsed:.1f}s | {len(content)}字 | tokens:{usage.get('total_tokens','N/A')}")
        
        # 落盘DNA
        dna_path = os.path.join(OUTPUT_DIR, f"{book_name}-文风DNA.md")
        with open(dna_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[{book_name}] DNA已落盘: {dna_path}")
        
        # 落盘input（按project_memory要求）
        input_path = os.path.join(OUTPUT_DIR, f"{book_name}_dna_input.md")
        with open(input_path, "w", encoding="utf-8") as f:
            f.write(user_prompt)
        
        # 落盘meta
        meta = {
            "book": book_name,
            "model": DS_MODEL,
            "strategy": f"采样{len(sampled)}章(前10+中5+后5)",
            "content_length": len(content),
            "elapsed": round(elapsed, 1),
            "usage": usage,
            "input_chars": len(user_prompt),
            "chapters_sampled": sampled,
            "chapter_count": len(sampled),
        }
        return meta
    except Exception as e:
        print(f"[{book_name}] 错误: {e}")
        return {"book": book_name, "error": str(e)}

def main():
    print("="*60)
    print("R42 · 文风DNA提取（两本书并行）")
    print("="*60)
    
    # 并行提取两本书
    metas = []
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = {executor.submit(extract_dna, name, config): name for name, config in BOOKS.items()}
        for future in as_completed(futures):
            name = futures[future]
            try:
                meta = future.result()
                metas.append(meta)
            except Exception as e:
                print(f"[{name}] 线程错误: {e}")
                metas.append({"book": name, "error": str(e)})
    
    # 落盘总meta
    metas.sort(key=lambda x: x.get("book", ""))
    with open(os.path.join(OUTPUT_DIR, "meta.json"), "w", encoding="utf-8") as f:
        json.dump({"round": "R42", "task": "dna_extract", "books": metas}, f, ensure_ascii=False, indent=2)
    
    print("\n" + "="*60)
    print("全部完成!")
    for m in metas:
        if "error" in m:
            print(f"  {m['book']}: 错误 - {m['error']}")
        else:
            print(f"  {m['book']}: {m['content_length']}字 | {m['elapsed']}s | {m['chapter_count']}章采样")
    print("="*60)

if __name__ == "__main__":
    main()
