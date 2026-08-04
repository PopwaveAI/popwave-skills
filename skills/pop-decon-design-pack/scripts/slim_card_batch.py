#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
瘦身白描卡/设计包 30章合并批处理脚本

核心变化 (v6.2.0):
- 从"单章 1 次 API 调用"改为"30 章合并 1 次 API 调用"（30张合并白描）
- 每批合并 30 章原文，一次调用产出 30 张白描卡/设计包，降低 API 调用成本约 30%
- 通过 --batch-size 控制每批章数，--mode 控制输出格式（fast 白描卡 / precision 设计包）

用法:
  python slim_card_batch.py --input <小说.txt> --output <输出目录> [选项]

参数:
  --input       小说 TXT 文件路径（必填）
  --output      输出目录（默认: 写作资产/白描卡/）
  --mode        fast=瘦身白描卡 / precision=设计包v4（默认: fast）
  --batch-size  每批合并章数（默认: 30）
  --encoding    TXT 文件编码（默认: gbk，可选 utf-8）
  --volume      只处理指定卷（如 "第一卷"，默认处理全书）
  --workers     并发批数（默认: 3）
  --max-chapters  最多处理章数（用于测试，默认无限制）
  --api-key     DeepSeek API Key（默认从环境变量或内置）
  --model       模型名（默认: deepseek-v4-flash）

示例:
  # 全书 fast 模式，30章合并
  python slim_card_batch.py --input 深渊主宰.txt --output ./白描卡/ --mode fast

  # 只处理第一卷，precision 模式，30章合并
  python slim_card_batch.py --input 深渊主宰.txt --output ./设计包v4/ --mode precision --volume "第一卷"

  # 测试前10章（1批）
  python slim_card_batch.py --input 深渊主宰.txt --output ./白描卡/ --max-chapters 10

  # 单章逐章（旧行为，batch-size=1）
  python slim_card_batch.py --input 深渊主宰.txt --output ./白描卡/ --batch-size 1
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
DEFAULT_WORKERS = 3  # 每批是30章合并大调用，并发不宜过高
DEFAULT_BATCH_SIZE = 30
MAX_RETRIES = 2
TIMEOUT = 300  # 30章合并大调用，超时放宽

# ===== 系统提示词：fast mode（瘦身白描卡）=====
SYSTEM_PROMPT_FAST = """你是一个专业的小说拆解助手。你的任务是将合并输入的多章小说原文，逐章压缩为瘦身白描卡。

## 输入格式
输入会携带一个或多个连续章节，每章用 `===== 第N章 标题 =====` 分隔。

## 输出格式
你必须为输入中的每一章单独输出一张白描卡，每张卡用 `# chXXX「标题」` 作为开头标记，卡与卡之间用 `---` 分隔。格式如下：

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

1. 输入有几章，就必须输出几张卡，逐章对应，不得遗漏、不得合并
2. 事件白描必须覆盖本章全部核心剧情转折，不可遗漏
3. 🔒标记的数据必须是一行式摘要+原文定位指针，禁止全文引用能力描述
4. 爽点和钩子无则省略对应行，不要写"无"
5. 人物关系变化仅在本章确实发生关系变化时填写，否则省略整个小节
6. 章型从以下选择：日常/成长/披露/转折/社交/探索/交锋
7. 原文字数 = 对应章输入正文的字符数（不含标题）
8. 每张卡总产出控制在150-250字（不含格式标记符号），上限500字
9. 直接输出全部白描卡，不要任何解释、前言或后记
10. 标题中的XXX替换为实际章节编号

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

# ===== 系统提示词：precision mode（v4设计包 3层+1区）=====
SYSTEM_PROMPT_PRECISION = """你是一个专业的小说拆解助手。你的任务是将合并输入的多章小说原文，逐章提炼为 v4 设计包（3层+1区结构）。

## 输入格式
输入会携带一个或多个连续章节，每章用 `===== 第N章 标题 =====` 分隔。

## 输出格式
你必须为输入中的每一章单独输出一份设计包，每份用 `# 设计包 — chXXX「章节标题」` 作为开头标记，份与份之间用 `---` 分隔。每份设计包结构如下：

```
# 设计包 — chXXX「章节标题」

## 1. beat链 (L1beat链层) - 表格格式
至少8个beat。表格列(7列): | # | beat | 类型 | scene | POV | 参与角色 | 原文证据 |
原文证据列只写定位指针（ch003-¶12 / 首句·关键词），禁止摘录完整段落。
🔒 不可替换标记(关键对白/数据)。

## 2. 爽点设计 (L2爽点层)
- 情绪弧线
- 爽点机制
- 章末钩子(L1-L5)

## 3. 角色与人设 (L3角色层)
- 登场角色行为锚定
- 关键对白(语气+潜台词)

## 4. 设定/物品提取区 (S1)
- 本章新揭示的世界设定、力量体系、规则
- 本章出现的物品及其信息
- 可简化为要点，但不得完全省略
```

## 规则

1. 输入有几章，就必须输出几份设计包，逐章对应，不得遗漏、不得合并
2. 不发明 beat，事件链必须来自原文
3. 每beat必须有 scene + POV + 原文证据指针 + 🔒 标记
4. 直接输出全部设计包，不要任何解释、前言或后记
5. 标题中的XXX替换为实际章节编号

## 红线
- 不发明beat
- 每章独立一份（保留 `# 设计包 — chXXX「标题」` 标记）
- 原文证据列只写定位指针，禁止摘录完整段落"""


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


def build_batch_prompt(batch, mode):
    """将一批章节合并为单个 prompt。batch: [(num, title, text, line_num), ...]"""
    parts = []
    for ch_num, ch_title, ch_text, _ in batch:
        parts.append(f"===== 第{ch_num}章 {ch_title} =====\n{ch_text}")
    combined = "\n\n".join(parts)
    if mode == "fast":
        return f"以下是小说连续 {len(batch)} 章（{batch[0][1]} 至 {batch[-1][1]}）的原文，请逐章输出瘦身白描卡，共 {len(batch)} 张：\n\n{combined}"
    else:
        return f"以下是小说连续 {len(batch)} 章（{batch[0][1]} 至 {batch[-1][1]}）的原文，请逐章输出 v4 设计包，共 {len(batch)} 份：\n\n{combined}"


def call_api(batch_prompt, system_prompt, api_key, api_url, model, max_tokens, retry=0):
    """调用 DS API 处理一批（30章合并）"""
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": batch_prompt}
    ]
    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
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
            return call_api(batch_prompt, system_prompt, api_key, api_url, model, max_tokens, retry + 1)
        return {
            "content": "",
            "elapsed": elapsed,
            "finish_reason": "error",
            "usage": {},
            "error": str(e)
        }


def parse_cards(content, mode):
    """解析批量输出为 {chapter_num: card_text}。返回 (cards_dict, missing_count)"""
    if mode == "fast":
        marker_re = re.compile(r'^#\s*ch(\d+)[「\[]', re.MULTILINE)
    else:
        marker_re = re.compile(r'^#\s*设计包\s*[—\-]\s*ch(\d+)[「\[]', re.MULTILINE)

    matches = list(marker_re.finditer(content))
    cards = {}
    for idx, m in enumerate(matches):
        ch_num = int(m.group(1))
        start = m.start()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(content)
        cards[ch_num] = content[start:end].strip()

    return cards, len(matches)


def process_batch(args_tuple):
    """处理一批章节（用于线程池）。args_tuple 见 main 中的构造。"""
    (batch, batch_index, output_dir, api_key, api_url, model, mode, max_tokens) = args_tuple

    batch_prompt = build_batch_prompt(batch, mode)
    system_prompt = SYSTEM_PROMPT_FAST if mode == "fast" else SYSTEM_PROMPT_PRECISION
    result = call_api(batch_prompt, system_prompt, api_key, api_url, model, max_tokens)

    batch_nums = [ch[0] for ch in batch]
    written = []
    if result["content"]:
        cards, _ = parse_cards(result["content"], mode)
        for ch in batch:
            ch_num = ch[0]
            card_text = cards.get(ch_num)
            if card_text:
                if mode == "fast":
                    filename = os.path.join(output_dir, f"ch{ch_num:03d}.md")
                else:
                    filename = os.path.join(output_dir, f"ch{ch_num:03d}-设计包.md")
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(card_text)
                written.append(ch_num)

    batch_input_chars = sum(len(ch[2]) for ch in batch)
    out_chars = len(result["content"])
    ratio = (out_chars / batch_input_chars * 100) if batch_input_chars > 0 else 0
    status = "OK" if result["content"] else "FAIL"
    print(f"  [批{batch_index}] {status} {result['elapsed']:.1f}s | "
          f"ch{batch_nums[0]:03d}-ch{batch_nums[-1]:03d} | "
          f"原文{batch_input_chars}字 → 产出{out_chars}字 ({ratio:.1f}%) | "
          f"写入{len(written)}/{len(batch)}章", flush=True)

    return {
        "batch_index": batch_index,
        "batch_nums": batch_nums,
        "written": written,
        "content": result["content"],
        "elapsed": result["elapsed"],
        "usage": result["usage"],
        "error": result["error"]
    }


def main():
    parser = argparse.ArgumentParser(description="瘦身白描卡/设计包 30章合并批处理")
    parser.add_argument("--input", required=True, help="小说 TXT 文件路径")
    parser.add_argument("--output", default="写作资产/白描卡", help="输出目录")
    parser.add_argument("--mode", default="fast", choices=["fast", "precision"],
                        help="fast=瘦身白描卡 / precision=设计包v4（默认 fast）")
    parser.add_argument("--batch-size", type=int, default=DEFAULT_BATCH_SIZE,
                        help=f"每批合并章数（默认 {DEFAULT_BATCH_SIZE}）")
    parser.add_argument("--encoding", default="gbk", help="TXT 文件编码（默认 gbk）")
    parser.add_argument("--volume", default=None, help="只处理指定卷（如 '第一卷'）")
    parser.add_argument("--workers", type=int, default=DEFAULT_WORKERS, help=f"并发批数（默认 {DEFAULT_WORKERS}）")
    parser.add_argument("--max-chapters", type=int, default=None, help="最多处理章数")
    parser.add_argument("--api-key", default=DEFAULT_API_KEY, help="DeepSeek API Key")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="模型名")
    args = parser.parse_args()

    if not args.api_key:
        print("错误: 未提供 API Key。请设置 DEEPSEEK_API_KEY 环境变量或使用 --api-key 参数。")
        return

    if args.batch_size < 1:
        print("错误: --batch-size 必须 >= 1")
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

    # 分批
    batches = [chapters_to_process[i:i + args.batch_size]
               for i in range(0, len(chapters_to_process), args.batch_size)]
    print(f"  分批: {len(batches)} 批 × {args.batch_size}章/批", flush=True)

    max_tokens = 12000 if args.mode == "fast" else 50000

    print(f"\n开始合并批处理 (模式={args.mode}, 并发批数={args.workers}, 每批{args.batch_size}章)...", flush=True)
    start_time = time.time()

    tasks = [(batch, idx, args.output, args.api_key,
              "https://api.deepseek.com/chat/completions", args.model,
              args.mode, max_tokens)
             for idx, batch in enumerate(batches)]

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(process_batch, task): task for task in tasks}
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())

    total_time = time.time() - start_time

    results.sort(key=lambda x: x["batch_index"])

    # 统计
    all_written = [n for r in results for n in r["written"]]
    fail_batches = [r for r in results if r["error"]]
    missing_chapters = [ch[0] for ch in chapters_to_process if ch[0] not in all_written]

    total_output = sum(len(r["content"]) for r in results)
    total_input = total_original
    avg_time = sum(r["elapsed"] for r in results) / len(results) if results else 0

    print(f"\n{'='*60}", flush=True)
    print(f"处理完成!", flush=True)
    print(f"  总批数: {len(results)}", flush=True)
    print(f"  成功批: {len(results) - len(fail_batches)} | 失败批: {len(fail_batches)}", flush=True)
    print(f"  写入章数: {len(all_written)}/{len(chapters_to_process)}", flush=True)
    print(f"  原文总字数: {total_input:,}", flush=True)
    print(f"  产出总字数: {total_output:,}", flush=True)
    if total_input > 0:
        print(f"  压缩比: {total_output/total_input*100:.1f}%", flush=True)
    print(f"  平均单批耗时: {avg_time:.1f}s", flush=True)
    print(f"  总耗时: {total_time:.1f}s ({total_time/60:.1f}分钟)", flush=True)
    print(f"  每批章数: {args.batch_size}", flush=True)
    print(f"  模式: {args.mode}", flush=True)
    print(f"{'='*60}", flush=True)

    if missing_chapters:
        print(f"\n缺失章节（{len(missing_chapters)}）: {missing_chapters}", flush=True)
        print(f"重试命令: python slim_card_batch.py --input '{args.input}' "
              f"--output '{args.output}' --mode {args.mode} --batch-size {args.batch_size} "
              f"--workers {max(1, args.workers - 1)}", flush=True)

    summary_name = "白描卡-汇总报告.md" if args.mode == "fast" else "设计包-汇总报告.md"
    summary_path = os.path.join(os.path.dirname(args.output), summary_name)
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(f"# {'白描卡' if args.mode == 'fast' else '设计包'}处理汇总报告\n\n")
        f.write(f"## 统计概览\n\n")
        f.write(f"| 指标 | 数值 |\n|:-----|:-----|\n")
        f.write(f"| 模式 | {args.mode} |\n")
        f.write(f"| 总章数 | {len(chapters_to_process)} |\n")
        f.write(f"| 写入章数 | {len(all_written)} |\n")
        f.write(f"| 总批数 | {len(results)} |\n")
        f.write(f"| 每批章数 | {args.batch_size} |\n")
        f.write(f"| 成功/失败批 | {len(results) - len(fail_batches)}/{len(fail_batches)} |\n")
        f.write(f"| 原文总字数 | {total_input:,} |\n")
        f.write(f"| 产出总字数 | {total_output:,} |\n")
        if total_input > 0:
            f.write(f"| 压缩比 | {total_output/total_input*100:.1f}% |\n")
        f.write(f"| 平均单批耗时 | {avg_time:.1f}s |\n")
        f.write(f"| 总耗时 | {total_time:.1f}s ({total_time/60:.1f}分钟) |\n")
        f.write(f"| 并发批数 | {args.workers} |\n\n")

        f.write(f"## 逐批统计\n\n")
        f.write(f"| 批 | 章范围 | 写入/总数 | 耗时 | 状态 |\n")
        f.write(f"|:---:|:-----|:--------:|:----:|:----:|\n")
        for r in results:
            status = "OK" if not r["error"] else "FAIL"
            f.write(f"| {r['batch_index']} | ch{r['batch_nums'][0]:03d}-ch{r['batch_nums'][-1]:03d} | "
                    f"{len(r['written'])}/{len(r['batch_nums'])} | {r['elapsed']:.1f}s | {status} |\n")

        if missing_chapters:
            f.write(f"\n## 缺失章节\n\n")
            f.write(f"{missing_chapters}\n")

    print(f"\n汇总报告: {summary_path}", flush=True)
    print(f"输出目录: {args.output}", flush=True)


if __name__ == "__main__":
    main()