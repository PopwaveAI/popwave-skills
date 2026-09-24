#!/usr/bin/env python3
"""
章节文件分隔符处理脚本

用途：清理章节文件**头部（`## 正文` 之前）**多余的空行 `---` 分隔符，只保留第一个。

2026-09-21 修正（实测踩坑）：
    旧版"只保留首尾两个 `---`"的策略会连**正文与「章节备注」之间的结构分隔线一起删掉**
    （实测：保留的是「备注／自检清单」之间那根，正文与备注直接粘在一起，文件结构错位），
    且无法区分"结构分隔"与"正文内的场景分隔"。
    现改为：只处理两件事——
      ① 头部区（`## 正文` 之前）多余空行 `---` 合并为一根；
      ② 正文区内的 `---` 清理为空白行（正文不得含 Markdown 语法残留，见 audit-checklist P0「格式混乱」）。
    正文区之外的结构分隔符**一律不动**。
"""

import os
import sys
import re


BODY_HEADING = re.compile(r'^#{2,}\s*正文\s*$')


def _find_body_range(lines):
    """返回 (正文节标题行号, 正文结束行号)；找不到标题返回 (None, None)

    正文结束 = 下一个 Markdown 标题行。正文内部的 `---` 不视为边界。
    """
    start = None
    for i, line in enumerate(lines):
        if BODY_HEADING.match(line.strip()):
            start = i
            break
    if start is None:
        return None, None
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if re.match(r'^#{1,6}\s', lines[j].strip()):
            end = j
            break
    return start, end


def normalize_punctuation(lines, body_start, body_end):
    """正文标点规范化：ASCII 直引号 → 全角成对引号

    实测踩坑（2026-09-21）：模型生成的中文对白常用 ASCII `"`，
    既是 audit-checklist P0「标点全半角混乱」，也会让"对话占比"这类
    自动统计直接失真（统计到 0%）。这里只做最稳的一步——成对替换双引号；
    单引号与省略号只统计不改（改写风险高，交人工）。

    返回 (处理后的行列表, 替换对数, 单引号残留数)
    """
    if body_start is None:
        return lines, 0, 0

    replaced = 0
    leftover_single = 0
    out = list(lines)
    for i in range(body_start + 1, body_end):
        line = out[i]
        if '"' not in line and "'" not in line:
            continue
        chars = []
        open_next = True
        for ch in line:
            if ch == '"':
                chars.append('“' if open_next else '”')
                open_next = not open_next
                replaced += 1
            else:
                if ch == "'":
                    leftover_single += 1
                chars.append(ch)
        out[i] = ''.join(chars)
    return out, replaced // 2, leftover_single


def process_chapter_file(file_path, output_path=None):
    """
    处理章节文件：
      ① 头部（`## 正文` 之前）多余的空行 `---` 合并为一根；
      ② 正文区内的 `---` 清理为空白行；正文区外的结构分隔符不动；
      ③ 正文标点规范化：ASCII 直引号 → 全角成对引号。

    Args:
        file_path: 输入文件路径
        output_path: 输出文件路径，默认为原文件（覆盖）
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    body_start, body_end = _find_body_range(lines)

    remove = set()

    # ① 头部区间隔符合并
    head_limit = body_start if body_start is not None else len(lines)
    head_seps = [i for i in range(head_limit) if lines[i].strip() == '---']
    head_removed = 0
    if len(head_seps) >= 2:
        remove.update(head_seps[1:])
        head_removed = len(head_seps) - 1

    # ② 正文区内的 `---` 清理为空白行
    #    例外：正文区末尾那根（其后到下一个标题之间全是空行）是**结构分隔符**，
    #    位于正文与「章节备注」之间，必须保留——实测旧版把它一起删了，
    #    导致正文与备注直接粘在一起。
    body_removed = 0
    trailing_sep = None
    if body_start is not None:
        last_content = body_end - 1
        while last_content > body_start and lines[last_content].strip() == '':
            last_content -= 1
        if lines[last_content].strip() == '---':
            trailing_sep = last_content
        for i in range(body_start + 1, body_end):
            if lines[i].strip() == '---' and i != trailing_sep:
                remove.add(i)
                body_removed += 1

    kept = [line for i, line in enumerate(lines) if i not in remove]

    # ③ 标点规范化（在删行后的行表上重新定位正文区）
    b_start, b_end = _find_body_range(kept)
    kept, quote_pairs, single_left = normalize_punctuation(kept, b_start, b_end)

    changed = bool(remove) or quote_pairs > 0

    if not changed:
        print(f"文件 {file_path} 无需处理（头部间隔符 {len(head_seps)} 根，正文内 0 根，"
              f"ASCII 引号 0 对）")
        return

    if output_path is None:
        output_path = file_path

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(kept))

    print(f"处理完成: {file_path}")
    print(f"  - 头部多余分隔符合并: 删除 {head_removed} 根")
    print(f"  - 正文内 Markdown 残留 `---` 清理: {body_removed} 根（改为空白行）")
    print(f"  - 正文末尾结构分隔符: {'已保留（原第%d行）' % (trailing_sep + 1) if trailing_sep is not None else '无'}")
    print(f"  - 标点规范化: ASCII 直引号 → 全角成对引号 {quote_pairs} 对")
    if single_left:
        print(f"  - ⚠️ 正文内仍有 ASCII 单引号 {single_left} 个，需确认（脚本不改）")
    print(f"  - 其余结构分隔符（正文区之外）: 全部保留")


def process_directory(directory):
    """
    处理目录下所有章节文件

    Args:
        directory: 目录路径
    """
    pattern = re.compile(r'^第\d+章.*\.md$')

    files_processed = 0
    for filename in sorted(os.listdir(directory)):
        if pattern.match(filename):
            file_path = os.path.join(directory, filename)
            process_chapter_file(file_path)
            files_processed += 1

    print(f"\n共处理 {files_processed} 个章节文件")


def main():
    """主函数"""
    if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'):
        print("""用法:
  python format_chapter.py <文件路径>            # 处理单个文件（就地覆盖）
  python format_chapter.py <目录路径>            # 处理目录下所有章节文件
  python format_chapter.py <文件路径> <输出路径>  # 处理并输出到指定路径

做的事:
  ① 头部多余 `---` 合并
  ② 正文内 Markdown 残留 `---` 清理（末尾结构分隔符保留）
  ③ ASCII 直引号 → 全角成对引号

注: 只做格式归一，不改内容。破折号等硬伤须回正文改写（换标点凑数会撞死线）。""")
        return 0 if len(sys.argv) > 1 else 1
    if len(sys.argv) < 2:
        print("用法:")
        print("  python format_chapter.py <文件路径>           # 处理单个文件")
        print("  python format_chapter.py <目录路径>           # 处理目录下所有章节文件")
        print("  python format_chapter.py <文件路径> <输出路径> # 处理单个文件并输出到指定路径")
        sys.exit(1)

    input_path = sys.argv[1]

    if len(sys.argv) >= 3:
        output_path = sys.argv[2]
        process_chapter_file(input_path, output_path)
    elif os.path.isdir(input_path):
        process_directory(input_path)
    elif os.path.isfile(input_path):
        process_chapter_file(input_path)
    else:
        print(f"路径不存在: {input_path}")
        sys.exit(1)


if __name__ == '__main__':
    main()
