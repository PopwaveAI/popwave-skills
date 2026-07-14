#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
瘦身白描卡 DS API 并发处理脚本

用法:
  python slim_card_batch.py --input <小说.txt> --output <输出目录> [选项]

参数:
  --input       小说 TXT 文件路径（必填）
  --output      输出目录（默认: 写作资产/白描卡/）
  --encoding    TXT 文件编码（默认: gbk，可选 utf-8）
  --volume      只处理指定卷（如 "第一卷"，默认处理全书）
  --workers     并发数（默认: 10）
  --max-chapters  最多处理章数（用于测试，默认无限制）
  --api-key     DeepSeek API Key（默认从环境变量或内置）
  --model       模型名（默认: deepseek-v4-flash）

示例:
  # 处理全书
  python slim_card_batch.py --input 深渊主宰.txt --output ./白描卡/

  # 只处理第一卷
  python slim_card_batch.py --input 深渊主宰.txt --output ./白描卡/ --volume "第一卷"

  # 测试前10章
  python slim_card_batch.py --input 深渊主宰.txt --output ./白描卡/ --max-chapters 10
"""

import json
import os
import re
import time
import argparse
import concurrent.futures
import urllib.request
import urllib.error

# ===== 默认配置 =====
DEFAULT_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
DEFAULT_API_URL = "https://api.deepseek.com/chat/completions"
DEFAULT_MODEL = "deepseek-v4-flash"
DEFAULT_WORKERS = 10
MAX_RETRIES = 2
TIMEOUT = 120

# ===== 系统提示词 =====
SYSTEM_PROMPT = """你是一个专业的小说拆解助手。你的任务是将小说章节压缩为瘦身版白描卡。

## 输出格式

```
# chXXX「标题」

POV: xxx | 章型: xxx | 原文: XXXX字

## 事件白描（3-5句，覆盖本章核心）
[3-5句话覆盖本章全部核心剧情，每句一个事件节点，不可遗漏关键转折]

## 关键数据
🔒 [属性面板摘要/关键对白/升级数据，一行式+原文定位指针。无则标"本章无"]

## 爽点·钩子
爽点: [信息差/数值/打脸/情绪，无则省略整行]
钩子: [悬念内容] → 预期回收 chXXX（强度 L1-L5，无则省略整行）

## 人物关系变化（可选）
[A→B: 动词（利用/背叛/信任…），仅本章确实发生关系变化时填。无则省略整个小节]
```

## 规则

1. 事件白描必须覆盖本章全部核心剧情转折，不可遗漏
2. 🔒标记的数据必须是一行式摘要+原文定位指针，禁止全文引用能力描述
3. 爽点和钩子无则省略对应行，不要写"无"
4. 人物关系变化仅在本章确实发生关系变化时填写，否则省略整个小节
5. 章型从以下选择：日常/成长/披露/转折/社交/探索/交锋
6. 原文字数 = 输入正文的字符数（不含标题）
7. 总产出控制在150-250字（不含格式标记符号），上限500字
8. 直接输出白描卡，不要任何解释、前言或后记
9. 标题中的XXX替换为实际章节编号

## 🔒 数据格式要求

正确：🔒 索伦属性：力量12/敏捷19(+1)/体质15/智力18(+1) | 平民5级/盗贼1级 | ch002-属性面板段
正确：🔒 "燃烧之手！"——暗红狗头人术士释放 | ch050-战斗高潮段
错误：🔒 【弱等寒冷抗性【个人专长】：在对抗寒冷的过程中...（全文引用200+字）

## 章型判定标准
- 日常: 无重大事件，角色日常活动
- 成长: 主角能力/认知提升，获得新技能或属性
- 披露: 重要信息揭示，世界观展开
- 转折: 剧情方向改变，命运转折点
- 社交: 角色间互动为主，建立/改变关系
- 探索: 发现新地点/新人物/新事物
- 交锋: 战斗/对抗/智斗"""


def split_chapters(content, volume_filter=None):
    """将全文按章节分割。返回 [(chapter_num, title, text, line_num), ...] 和卷边界信息。"""
    pattern = r'^(第(\d+)章\s+.+)$'
    lines = content.split('\n')

    vol_boundaries = {}
    for i, line in enumerate(lines):
        line = line.strip()
        if re.match(r'^第.卷\s', line) or re.match(r'^第.卷$', line):
            vol_name = line.split()[0] if line.split() else line.strip()
            vol_boundaries[vol_name] = i + 1

    chapters = []
    current_ch_num = None
    current_title = None
    current_line_num = None
    current_lines = []

    for i, line in enumerate(lines):
        match = re.match(pattern, line.strip())
        if match:
            if current_ch_num is not None:
                chapters.append((current_ch_num, current_title,
                                 '\n'.join(current_lines).strip(), current_line_num))
            current_title = match.group(1)
            current_ch_num = int(match.group(2))
            current_line_num = i + 1
            current_lines = []
        else:
            if current_ch_num is not None:
                current_lines.append(line)

    if current_ch_num is not None:
        chapters.append((current_ch_num, current_title,
                         '\n'.join(current_lines).strip(), current_line_num))

    if volume_filter:
        vol_start = 0
        vol_end = float('inf')
        for vol_name, line_num in vol_boundaries.items():
            if vol_name == volume_filter:
                vol_start = line_num
                vol_names = list(vol_boundaries.keys())
                idx = vol_names.index(vol_name)
                if idx + 1 < len(vol_names):
                    vol_end = vol_boundaries[vol_names[idx + 1]]
                break
        chapters = [(num, title, text, ln) for num, title, text, ln in chapters
                    if vol_start < ln < vol_end]

    return chapters, vol_boundaries


def call_api(chapter_num, chapter_title, chapter_text, api_key, api_url, model, retry=0):
    """调用 DS API 处理单章"""
    user_prompt = f"以下是小说{chapter_title}的原文，请压缩为白描卡：\n\n{chapter_text}"

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt}
    ]
    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": 2000,
        "temperature": 0.3,
        "top_p": 0.9,
        "stream": False,
        "response_format": {"type": "text"}
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(api_url, data=data, headers=headers, method="POST")

    start = time.time()
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            elapsed = time.time() - start
            content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
            finish = result.get("choices", [{}])[0].get("finish_reason", "")
            usage = result.get("usage", {})
            return {
                "chapter_num": chapter_num,
                "chapter_title": chapter_title,
                "content": content,
                "elapsed": elapsed,
                "finish_reason": finish,
                "usage": usage,
                "error": None
            }
    except Exception as e:
        elapsed = time.time() - start
        if retry < MAX_RETRIES:
            time.sleep(3)
            return call_api(chapter_num, chapter_title, chapter_text, api_key, api_url, model, retry + 1)
        return {
            "chapter_num": chapter_num,
            "chapter_title": chapter_title,
            "content": "",
            "elapsed": elapsed,
            "finish_reason": "error",
            "usage": {},
            "error": str(e)
        }


def process_chapter(args_tuple):
    """处理单章（用于线程池）"""
    ch_num, ch_title, ch_text, output_dir, api_key, api_url, model = args_tuple
    result = call_api(ch_num, ch_title, ch_text, api_key, api_url, model)

    if result["content"]:
        filename = os.path.join(output_dir, f"ch{ch_num:03d}.md")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(result["content"])

    status = "OK" if result["content"] else "FAIL"
    ch_chars = len(ch_text)
    out_chars = len(result["content"])
    ratio = (out_chars / ch_chars * 100) if ch_chars > 0 else 0
    print(f"  [ch{ch_num:03d}] {status} {result['elapsed']:.1f}s | "
          f"原文{ch_chars}字 → 产出{out_chars}字 ({ratio:.1f}%)", flush=True)

    return result


def main():
    parser = argparse.ArgumentParser(description="瘦身白描卡 DS API 并发处理")
    parser.add_argument("--input", required=True, help="小说 TXT 文件路径")
    parser.add_argument("--output", default="写作资产/白描卡", help="输出目录")
    parser.add_argument("--encoding", default="gbk", help="TXT 文件编码（默认 gbk）")
    parser.add_argument("--volume", default=None, help="只处理指定卷（如 '第一卷'）")
    parser.add_argument("--workers", type=int, default=DEFAULT_WORKERS, help="并发数")
    parser.add_argument("--max-chapters", type=int, default=None, help="最多处理章数")
    parser.add_argument("--api-key", default=DEFAULT_API_KEY, help="DeepSeek API Key")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="模型名")
    args = parser.parse_args()

    if not args.api_key:
        print("错误: 未提供 API Key。请设置 DEEPSEEK_API_KEY 环境变量或使用 --api-key 参数。")
        return

    os.makedirs(args.output, exist_ok=True)

    print(f"正在读取 {args.input} (编码: {args.encoding})...", flush=True)
    try:
        with open(args.input, encoding=args.encoding) as f:
            content = f.read()
    except UnicodeDecodeError:
        for enc in ["gb18030", "utf-8", "utf-8-sig", "big5"]:
            try:
                with open(args.input, encoding=enc) as f:
                    content = f.read()
                print(f"  自动检测编码: {enc}", flush=True)
                break
            except UnicodeDecodeError:
                continue
        else:
            print("错误: 无法解码文件，请手动指定 --encoding 参数")
            return

    print(f"  读取完成: {len(content)} 字符", flush=True)

    print("正在分割章节...", flush=True)
    all_chapters, vol_boundaries = split_chapters(content, args.volume)

    if args.volume:
        print(f"  卷过滤: {args.volume}", flush=True)
        print(f"  卷范围: {vol_boundaries.get(args.volume, '?')}", flush=True)

    chapters_to_process = all_chapters
    if args.max_chapters:
        chapters_to_process = all_chapters[:args.max_chapters]

    print(f"  全书共 {len(all_chapters)} 章", flush=True)
    print(f"  本次处理: {len(chapters_to_process)} 章", flush=True)

    total_original = sum(len(text) for _, _, text, _ in chapters_to_process)
    print(f"  原文总字数: {total_original}", flush=True)

    print(f"\n开始并发处理 (并发数={args.workers})...", flush=True)
    start_time = time.time()

    tasks = [(num, title, text, args.output, args.api_key,
              "https://api.deepseek.com/chat/completions", args.model)
             for num, title, text, _ in chapters_to_process]

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(process_chapter, task): task for task in tasks}
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())

    total_time = time.time() - start_time

    results.sort(key=lambda x: x["chapter_num"])

    success_count = sum(1 for r in results if r["content"])
    fail_count = sum(1 for r in results if not r["content"])
    total_output = sum(len(r["content"]) for r in results)
    total_input = sum(len(ch[2]) for ch in chapters_to_process)
    avg_time = sum(r["elapsed"] for r in results) / len(results) if results else 0

    print(f"\n{'='*60}", flush=True)
    print(f"处理完成!", flush=True)
    print(f"  总章数: {len(results)}", flush=True)
    print(f"  成功: {success_count} | 失败: {fail_count}", flush=True)
    print(f"  原文总字数: {total_input:,}", flush=True)
    print(f"  产出总字数: {total_output:,}", flush=True)
    if total_input > 0:
        print(f"  压缩比: {total_output/total_input*100:.1f}%", flush=True)
    print(f"  平均单章耗时: {avg_time:.1f}s", flush=True)
    print(f"  总耗时: {total_time:.1f}s ({total_time/60:.1f}分钟)", flush=True)
    print(f"  并发数: {args.workers}", flush=True)
    print(f"{'='*60}", flush=True)

    if fail_count > 0:
        failed = [r["chapter_num"] for r in results if not r["content"]]
        print(f"\n失败章节: {failed}", flush=True)
        print(f"重试命令: python slim_card_batch.py --input '{args.input}' "
              f"--output '{args.output}' --encoding {args.encoding} --workers 3", flush=True)

    summary_path = os.path.join(os.path.dirname(args.output), "白描卡-汇总报告.md")
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(f"# 白描卡处理汇总报告\n\n")
        f.write(f"## 统计概览\n\n")
        f.write(f"| 指标 | 数值 |\n|:-----|:-----|\n")
        f.write(f"| 总章数 | {len(results)} |\n")
        f.write(f"| 成功/失败 | {success_count}/{fail_count} |\n")
        f.write(f"| 原文总字数 | {total_input:,} |\n")
        f.write(f"| 产出总字数 | {total_output:,} |\n")
        if total_input > 0:
            f.write(f"| 压缩比 | {total_output/total_input*100:.1f}% |\n")
        f.write(f"| 平均单章耗时 | {avg_time:.1f}s |\n")
        f.write(f"| 总耗时 | {total_time:.1f}s ({total_time/60:.1f}分钟) |\n")
        f.write(f"| 并发数 | {args.workers} |\n\n")

        f.write(f"## 逐章统计\n\n")
        f.write(f"| 章 | 标题 | 原文字数 | 产出字数 | 压缩比 | 耗时 | 状态 |\n")
        f.write(f"|:---:|:-----|:--------:|:--------:|:------:|:----:|:----:|\n")
        ch_map = {ch[0]: ch for ch in chapters_to_process}
        for r in results:
            ch = ch_map.get(r["chapter_num"])
            if ch:
                ch_chars = len(ch[2])
            else:
                ch_chars = 0
            out_chars = len(r["content"])
            ratio = (out_chars / ch_chars * 100) if ch_chars > 0 else 0
            status = "OK" if r["content"] else "FAIL"
            f.write(f"| {r['chapter_num']} | {r['chapter_title']} | {ch_chars} | {out_chars} | {ratio:.1f}% | {r['elapsed']:.1f}s | {status} |\n")

    print(f"\n汇总报告: {summary_path}", flush=True)
    print(f"白描卡目录: {args.output}", flush=True)


if __name__ == "__main__":
    main()
