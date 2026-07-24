#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
R21·b: 交替采样DNA提取 v4
策略: ch01-10全读 + ch11/13/15...49每两章读一章 = 30章
覆盖前50章范围
"""

import os, sys, json, time, requests, re

DS_API_KEY = "sk-5a3654e4aa2e4eefa08abe3d0e0231f5"
DS_BASE_URL = "https://api.deepseek.com/v1"
DS_MODEL = "deepseek-v4-flash"
TEMPERATURE = 0.7
MAX_TOKENS = 16000
TIMEOUT = 600

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")
TXT_PATH = r"d:\popwave-skills\downloads\我在美国搞内战-捕梦者.txt"

CN_MAP = {'零':0,'一':1,'二':2,'三':3,'四':4,'五':5,'六':6,'七':7,'八':8,'九':9,'十':10,'百':100,'千':1000}

def parse_cn_num(s):
    s = s.strip()
    if s.isdigit(): return int(s)
    if s in CN_MAP: return CN_MAP[s]
    if len(s)==2 and s[0]=='十': return 10+CN_MAP.get(s[1],0)
    if len(s)==2 and s[1]=='十': return CN_MAP.get(s[0],0)*10
    if len(s)==3 and s[1]=='十': return CN_MAP.get(s[0],0)*10+CN_MAP.get(s[2],0)
    return None

def extract_chapters():
    with open(TXT_PATH, "r", encoding="utf-8") as f:
        lines = f.read().split('\n')
    
    chapter_marks = []
    seen = set()
    for i, line in enumerate(lines):
        m = re.match(r'^# 第(.+?)章\s*(.+)?', line.strip())
        if m:
            ch_num = parse_cn_num(m.group(1).strip())
            title = (m.group(2) or "").strip()
            if ch_num and ch_num not in seen and 1 <= ch_num <= 50:
                if not any(kw in title for kw in ['审核','稍等','大家','抱歉','说明','公告']):
                    chapter_marks.append((ch_num, i))
                    seen.add(ch_num)
    chapter_marks.sort(key=lambda x: x[0])
    
    # ch01-10全读 + ch11-49奇数章
    target = set(range(1, 11))
    for i in range(11, 50, 2):
        target.add(i)
    
    chapters = {}
    for idx, (ch_num, start) in enumerate(chapter_marks):
        if ch_num not in target: continue
        end = chapter_marks[idx+1][1] if idx+1 < len(chapter_marks) else len(lines)
        chapters[ch_num] = '\n'.join(lines[start:end]).strip()
    return chapters

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("="*60)
    print("R21·b: 交替采样DNA提取 (ch01-10全读 + ch11-49奇数章)")
    print("="*60)
    
    chapters = extract_chapters()
    ch_list = sorted(chapters.keys())
    total = sum(len(v) for v in chapters.values())
    print(f"\n[1/3] 提取: {len(chapters)}章 | {total}字 | 章节: {ch_list}")
    
    book = "\n\n".join(chapters[k] for k in ch_list)
    
    with open(os.path.join(r"d:\popwave-skills\skills\pop-fanqie-seed\steps", "step0.md"), "r", encoding="utf-8") as f:
        step0 = f.read()
    
    user_prompt = f"""你是网文创作专家。请按照以下DNA提取方法，对参考书进行8维DNA提取。

# DNA提取方法

{step0}

# 参考书正文（交替采样：ch01-10全读 + ch11-49奇数章，共{len(chapters)}章）

{book}

# 任务

按step0的8维模板，对以上参考书内容进行完整DNA提取。特别注意：
1. 钩子vs核心方法论区分——对每个元素标注出现章节范围，只在开篇出现后续不复现的标注[钩子]，跨章节复现的标注[核心]
2. beat sheet要覆盖所有读到的{len(chapters)}章，按10章一组分块
3. 0b-后检分类清单要完整
4. 每个维度的原文证据要标注具体章节号

直接输出完整DNA文档（markdown格式），不需要分段确认。"""

    print(f"\n[2/3] 调用DS... User prompt: {len(user_prompt)}字符 | 预估tokens: ~{int(len(user_prompt)/1.4)}")
    
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
    response = requests.post(url, headers=headers, json=payload, timeout=TIMEOUT)
    response.raise_for_status()
    elapsed = time.time() - start
    result = response.json()
    content = result["choices"][0]["message"]["content"]
    usage = result.get("usage", {})
    print(f"  完成! {elapsed:.1f}s | {len(content)}字 | tokens:{usage.get('total_tokens','N/A')}")
    
    with open(os.path.join(OUTPUT_DIR, "r21b-dna-交替采样30章.md"), "w", encoding="utf-8") as f:
        f.write(content)
    
    meta = {"strategy": f"交替采样{len(chapters)}章(ch01-10全读+ch11-49奇数章)", "model": DS_MODEL,
            "content_length": len(content), "elapsed": round(elapsed,1), "usage": usage,
            "input_chars": len(user_prompt), "chapters_read": ch_list, "chapter_count": len(chapters)}
    with open(os.path.join(OUTPUT_DIR, "r21b-dna-meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    
    print(f"\n完成！产出: {len(content)}字 | 输入: {len(user_prompt)}字符 | {len(chapters)}章")

if __name__ == "__main__":
    main()
