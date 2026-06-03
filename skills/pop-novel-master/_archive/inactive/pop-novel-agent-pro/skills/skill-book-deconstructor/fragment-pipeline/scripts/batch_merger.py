"""
batch_merger.py — 多文件语料库自动拼接 + 智能分章
隶属于 novel-deconstructor v4.5 | 主题定向提取模式C 的配套工具

用法：
  python batch_merger.py --dir "/path/to/ref_book.txt"
  python batch_merger.py --dir "/path/to/ref_book.txt" --pattern "ref_book_batch*.txt"

输出：
  - _merged_book.txt     → 全本拼接+去重+分章后的单一文件
  - chapter_index.json   → 章节索引 [{"num":1,"title":"第1章"}, ...]

依赖：标准库（无需第三方包）
"""

import re
import json
import os
import glob
import argparse
from pathlib import Path


def detect_encoding(path: str) -> str:
    """自动检测文件编码（优先UTF-8，回退GBK/GB18030）"""
    for enc in ['utf-8', 'gb18030', 'gbk', 'utf-16']:
        try:
            with open(path, 'r', encoding=enc) as f:
                f.read()
                return enc
        except (UnicodeDecodeError, UnicodeError):
            continue
    return 'utf-8'


def extract_chapters(text: str) -> list:
    """
    按 '第X章/第X节/第X回' 模式切分章节。
    兼容中文数字和阿拉伯数字。
    示例匹配：第1章 / 第12章 / 第百章 / 第〇章 / 第1节 / 第1回
    """
    pattern = r'(第[一二三四五六七八九十百千\d零〇]+[章节回])'
    parts = re.split(pattern, text)

    chapters = []
    for i in range(1, len(parts), 2):
        title = parts[i].strip()
        content = (parts[i + 1] if i + 1 < len(parts) else "").strip()
        if len(content) < 50:  # 过滤明显的误切（标题行后的空内容）
            continue
        chapters.append({
            "title": title,
            "content": content
        })
    return chapters


def natural_sort_key(filepath: str) -> list:
    """
    自然排序键，确保 batch01 < batch02 < ... < batch25。
    eg: "batch12.txt" → ["batch", 12, ".txt"]
    """
    basename = os.path.basename(filepath)
    return [
        int(c) if c.isdigit() else c
        for c in re.split(r'(\d+)', basename)
    ]


def merge_batches(
    book_dir: str,
    batch_pattern: str = "batch*.txt",
    output_dir: str = None,
) -> tuple:
    """
    扫描 book_dir 下所有符合 batch_pattern 的文件，
    按自然序拼接后智能分章。

    Parameters:
        book_dir: batch 文件所在目录
        batch_pattern: 文件匹配模式（默认 batch*.txt）
        output_dir: 输出目录（默认 book_dir）

    Returns:
        (merged_path, index_path, chapters_list)
    """
    book_dir = os.path.abspath(book_dir)
    matched = sorted(
        glob.glob(os.path.join(book_dir, batch_pattern)),
        key=natural_sort_key,
    )

    if not matched:
        raise FileNotFoundError(
            f"在 {book_dir} 下未找到匹配 '{batch_pattern}' 的文件"
        )

    print(f"[batch_merger] 发现 {len(matched)} 个文件：")
    for f in matched[:5]:
        print(f"  {os.path.basename(f)}")
    if len(matched) > 5:
        print(f"  ... 等共 {len(matched)} 个")

    # --- 逐文件读取 + 分章 ---
    all_chapters = []
    for fpath in matched:
        enc = detect_encoding(fpath)
        with open(fpath, 'r', encoding=enc) as f:
            text = f.read()
        chapters = extract_chapters(text)
        all_chapters.extend(chapters)

    # --- 去重：相同标题的章节只保留第一个 ---
    seen_titles = set()
    unique_chapters = []
    for ch in all_chapters:
        key = ch["title"]
        if key not in seen_titles:
            seen_titles.add(key)
            unique_chapters.append(ch)

    # --- 生成编号 ---
    for idx, ch in enumerate(unique_chapters, start=1):
        ch["ch_num"] = idx

    # --- 输出拼接文本 ---
    merged_lines = []
    for ch in unique_chapters:
        merged_lines.append(f"\n\n{ch['title']}\n{ch['content']}")
    merged_text = "".join(merged_lines).strip()

    output_dir = output_dir or book_dir
    os.makedirs(output_dir, exist_ok=True)

    merged_path = os.path.join(output_dir, "_merged_book.txt")
    with open(merged_path, 'w', encoding='utf-8') as f:
        f.write(merged_text)

    # --- 章节索引 ---
    index_data = [
        {"num": ch["ch_num"], "title": ch["title"],
         "word_count": len(ch["content"])}
        for ch in unique_chapters
    ]
    index_path = os.path.join(output_dir, "chapter_index.json")
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, ensure_ascii=False, indent=2)

    total_chars = len(merged_text)
    total_chapters = len(unique_chapters)

    print(f"\n[batch_merger] ✅ 完成！")
    print(f"   拼接章节：{total_chapters} 章")
    print(f"   总字符数：{total_chars:,}")
    print(f"   输出文件：{merged_path}")
    print(f"   章节索引：{index_path}")

    # --- 统计信息 ---
    top_keywords = _stat_keywords(merged_text, [
        "密藏域", "诡异", "厉诡", "苏午", "师父", "金母",
    ])
    if top_keywords:
        print(f"\n   关键词频次（前10）：")
        for kw, cnt in top_keywords[:10]:
            print(f"     {kw}: {cnt}")

    return merged_path, index_path, unique_chapters


def _stat_keywords(text: str, keywords: list) -> list:
    """辅助：统计关键词出现频次"""
    counts = {}
    for kw in keywords:
        counts[kw] = text.count(kw)
    return sorted(counts.items(), key=lambda x: -x[1])


def locate_hits(
    merged_path: str,
    keyword_list: list,
    chapter_index_path: str = None,
) -> list:
    """
    在拼接文本中按关键词组定位命中章节。
    配合模式C 的 Step 1：全局 grep 定位。

    Parameters:
        merged_path: 拼接文件路径
        keyword_list: 关键词列表
        chapter_index_path: 章节索引路径（可选，不提供则重新解析）

    Returns:
        [{"ch_num":1, "title":"第1章", "hit_count":3, "hit_keywords":[...]}, ...]
    """
    with open(merged_path, 'r', encoding='utf-8') as f:
        text = f.read()

    if chapter_index_path and os.path.exists(chapter_index_path):
        with open(chapter_index_path, 'r', encoding='utf-8') as f:
            chapters = json.load(f)
    else:
        chapters = extract_chapters(text)
        for idx, ch in enumerate(chapters, start=1):
            ch["ch_num"] = idx

    # 重新按章节切分以定位命中
    parts = re.split(r'(第[一二三四五六七八九十百千\d零〇]+[章节回])', text)

    results = []
    for ch_info in chapters:
        ch_idx = (ch_info["num"] - 1) * 2 + 1
        if ch_idx >= len(parts):
            continue
        title = parts[ch_idx] if ch_idx < len(parts) else ""
        content = parts[ch_idx + 1] if ch_idx + 1 < len(parts) else ""

        hit_keywords = [
            kw for kw in keyword_list
            if kw in content or kw in title
        ]
        if hit_keywords:
            results.append({
                "ch_num": ch_info["num"],
                "title": ch_info["title"],
                "hit_count": len(hit_keywords),
                "hit_keywords": hit_keywords,
            })

    total_hit = len(results)
    total_ch = len(chapters)
    coverage_pct = round(total_hit / total_ch * 100, 1) if total_ch else 0

    print(f"\n[locate_hits] 关键词命中统计：")
    print(f"   总章节：{total_ch}")
    print(f"   命中章节：{total_hit}（覆盖 {coverage_pct}%）")
    print(f"   命中关键词：{keyword_list}")

    return results


# ===========================================================================
# CLI
# ===========================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="batch_merger — 多文件语料库自动拼接 + 智能分章 + 关键词定位"
    )
    parser.add_argument(
        "--dir", required=True,
        help="batch 文件所在目录（如 e:/AI小说/参考小说txt/我的诡异人生_全本）"
    )
    parser.add_argument(
        "--pattern", default="batch*.txt",
        help="文件匹配模式（默认: batch*.txt，如 ref_book_batch*.txt）"
    )
    parser.add_argument(
        "--output",
        help="输出目录（默认: book_dir）"
    )
    parser.add_argument(
        "--locate", nargs="+", default=None,
        help="关键词定位模式，传入关键词列表（如 --locate 密藏域 大雪山 精莲）"
    )
    args = parser.parse_args()

    merged_path, index_path, chapters = merge_batches(
        args.dir, args.pattern, args.output
    )

    if args.locate:
        print("\n" + "=" * 60)
        locate_hits(merged_path, args.locate, index_path)
