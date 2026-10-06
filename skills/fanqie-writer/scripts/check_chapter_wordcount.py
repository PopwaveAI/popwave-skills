#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
章节字数检查脚本
检查字数是否落在**本书／本题材**的最佳区间（区间从哪来见 scripts/word_range.py）

区间来源与优先级（2026-09-30 新增 · 治「文档按题材分档、脚本却硬编码 2200-2800」）：
    ① 命令行 --min/--max ＞ ② 本书 .learnings/立项参数.json（自动向上找）
    ＞ ③ --range-config <分档表 json> ＋ --genre <题材> ＞ ④ 内置默认 2200-2800。
    报告里会逐章打印「来源」——**降级到默认档必须可见，不许静默糊过去**。
    黄金三章选「递减结构」时（本书参数里 黄金三章.mode=descending），
    第 1-3 章按递减序列放行，**不让递减结构被本门禁误判 FAIL**。

统计口径（2026-09-21 修正）：
    章节文件由四块构成——元数据块（本章概要/承接上章…）、正文、章节备注、写后自检清单。
    提交平台的只有「正文」，元数据与自检清单不计入。旧版只跳过标题行，
    把元数据+备注+自检清单一并算进字数，实测高估 400+ 字，
    会把正文实际不足 2200 字的章节误判为达标。
    现改为：优先只统计 `## 正文` 节；无该标记时回落到旧口径。
"""

import os
import re
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from word_range import resolve as resolve_range  # noqa: E402

# 处理 Windows 控制台编码问题
if sys.platform == 'win32':
    import io
    # 更稳健的编码替换方式
    if hasattr(sys.stdout, 'buffer'):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    if hasattr(sys.stderr, 'buffer'):
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


def count_chinese_words(text: str) -> int:
    """统计中文字符个数（不含Markdown格式符号）"""
    # 移除Markdown标题符号
    text = re.sub(r'#{1,6}\s*', '', text)
    # 移除加粗、斜体、删除线
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    text = re.sub(r'~~(.*?)~~', r'\1', text)
    # 移除行内代码
    text = re.sub(r'`(.*?)`', r'\1', text)
    # 移除链接，保留文本
    text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)
    # 统计中文字符（Unicode汉字区间）
    chinese_chars = re.findall(r'[\u4e00-\u9fff]', text)
    return len(chinese_chars)


def extract_content_from_chapter(file_path: Path) -> str:
    """从章节文件中提取**正文**内容（不含元数据块、章节备注、写后自检清单）

    规则：
    1. 优先定位 `## 正文` 节，统计到下一个 Markdown 标题为止。
       正文内部的 `---` 是场景分隔符，**不视为结束边界**。
    2. 没有 `## 正文` 标记时，回落到旧口径：从含「章」的一级标题下一行起统计
       （这种情况下请确认文件是否含元数据块）。
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')

    # 规则 1：定位 `## 正文` 节
    for i, line in enumerate(lines):
        if re.match(r'^#{2,}\s*正文\s*$', line.strip()):
            end = len(lines)
            for j in range(i + 1, len(lines)):
                if re.match(r'^#{1,6}\s', lines[j].strip()):
                    end = j
                    break
            return '\n'.join(lines[i + 1:end])

    # 规则 2：回落口径
    for i, line in enumerate(lines):
        if line.startswith('#') and '章' in line:
            return '\n'.join(lines[i + 1:])

    return content


def check_chapter(file_path: str, min_words=None, max_words=None,
                  range_config=None, genre=None, book_dir=None) -> dict:
    """检查单个章节的字数。

    区间由 word_range.resolve 解析：命令行 ＞ 本书立项参数 ＞ 分档表 ＞ 内置默认。
    """
    rng = resolve_range(min_words=min_words, max_words=max_words,
                        range_config=range_config, genre=genre,
                        book_dir=book_dir, chapter_path=file_path)
    min_words, max_words = rng['min'], rng['max']
    path = Path(file_path)
    if not path.exists():
        return {
            'file': str(path),
            'exists': False,
            'word_count': 0,
            'status': 'error',
            'message': f'文件不存在: {file_path}',
            'range': f'{min_words}-{max_words}',
            'range_label': rng['label'],
        }

    main_content = extract_content_from_chapter(path)
    word_count = count_chinese_words(main_content)

    if word_count < min_words:
        status = 'short'
        message = f'字数: {word_count} (不足，需要至少 {min_words} 字)'
    elif word_count > max_words:
        status = 'long'
        message = f'字数: {word_count} (超标，建议精简至 {max_words} 字以内)'
    else:
        status = 'pass'
        message = f'字数: {word_count} (最佳区间 {min_words}-{max_words} 字)'

    return {
        'file': str(path),
        'exists': True,
        'word_count': word_count,
        'status': status,
        'message': message,
        'range': f'{min_words}-{max_words}',
        'range_label': rng['label'],
    }


def check_all_chapters(directory: str, pattern: str = '第*.md',
                       min_words=None, max_words=None,
                       range_config=None, genre=None) -> list:
    """检查目录下所有章节文件（**逐章**解析区间：本书参数与黄金三章递减要按章号判）"""
    dir_path = Path(directory)
    if not dir_path.exists():
        print(f'错误: 目录不存在 - {directory}')
        return []

    chapter_files = sorted(dir_path.glob(pattern))
    results = [check_chapter(str(f), min_words, max_words, range_config, genre)
               for f in chapter_files]
    return results


def print_results(results: list):
    """打印检查报告。

    **区间来源逐章打印**——降级到内置默认档时必须一眼可见。
    """
    if not results:
        print('没有找到章节文件')
        return

    total_words = 0
    passed = short = long = error = 0

    ranges = sorted({r.get('range') for r in results if r.get('range')})
    print('\n' + '=' * 60)
    print('章节字数检查报告（仅统计正文，不含元数据/备注/自检清单）')
    print('最佳区间: ' + ('／'.join(ranges) if ranges else '（未解析出区间）'))
    print('=' * 60)

    for result in results:
        if not result['exists']:
            error += 1
            icon = '[X]'
        elif result['status'] == 'pass':
            passed += 1
            icon = '[OK]'
            total_words += result['word_count']
        elif result['status'] == 'short':
            short += 1
            icon = '[!]'
            total_words += result['word_count']
        elif result['status'] == 'long':
            long += 1
            icon = '[>]'
            total_words += result['word_count']
        else:
            error += 1
            icon = '[X]'

        print(f'\n{icon} {Path(result["file"]).name}')
        print(f'   {result["message"]}')
        if result.get('range_label'):
            print(f'   来源: {result["range_label"]}')

    print('\n' + '-' * 60)
    print(f'总计: {len(results)} 章 | {passed} 章达标 | {short} 章不足 | {long} 章超标 | 总字数: {total_words:,}')
    print('-' * 60)

    if short > 0:
        print(f'\n有 {short} 章内容不足各自区间的下限，建议回写前配额表补「场上其他人的反应与对白来回」')
    if long > 0:
        print(f'\n有 {long} 章内容超过各自区间的上限，建议精简：超长会稀释本章重点。')

    degraded = [Path(r['file']).name for r in results
                if str(r.get('range_label', '')).startswith('⚠️')]
    if degraded:
        print('\n⚠️ 有 %d 章没解析到本书字数口径（%s）——用的是内置默认 2200-2800。'
              % (len(degraded), '、'.join(degraded[:5])))
        print('   请确认本书 .learnings/立项参数.json 已写好单章字数区间（生成方式见 SKILL.md）。')


USAGE = '''用法:
  python check_chapter_wordcount.py <章节文件路径> [最小字数] [最大字数]
  python check_chapter_wordcount.py --all <目录路径> [最小字数] [最大字数]

可选参数（一般不用给——脚本会自己找本书立项参数）:
  --min <n> / --max <n>            显式指定区间（优先级最高）
  --genre <题材名>                  配合 --range-config 用
  --range-config <json>             分档表（各技能自带的字数分档 json）
  -h / --help                       看这段

区间解析顺序: 命令行 ＞ 本书 .learnings/立项参数.json ＞ 分档表 ＞ 内置默认 2200-2800。
'''


def _take_flag(argv, name):
    """从 argv 里摘掉 `--name value`，返回 (值, 剩余列表)"""
    out, val, i = [], None, 0
    while i < len(argv):
        if argv[i] == name and i + 1 < len(argv):
            val = argv[i + 1]
            i += 2
            continue
        out.append(argv[i])
        i += 1
    return val, out


def main():
    argv = sys.argv[1:]
    if not argv or argv[0] in ('-h', '--help'):
        print(USAGE)
        return

    min_words, rest = _take_flag(argv, '--min')
    if min_words is None:
        min_words, rest = _take_flag(rest, '--min-words')
    max_words, rest = _take_flag(rest, '--max')
    range_config, rest = _take_flag(rest, '--range-config')
    genre, rest = _take_flag(rest, '--genre')
    min_words = int(min_words) if min_words else None
    max_words = int(max_words) if max_words else None

    if not rest:
        print(USAGE)
        return

    if rest[0] == '--all':
        if len(rest) < 2:
            print('错误: 使用 --all 时需要指定目录路径')
            return
        directory = rest[1]
        # 兼容老写法：--all <目录> [最小字数] [最大字数]
        if len(rest) >= 4:
            min_words, max_words = int(rest[2]), int(rest[3])
        elif len(rest) == 3:
            min_words = int(rest[2])
        results = check_all_chapters(directory, min_words=min_words, max_words=max_words,
                                     range_config=range_config, genre=genre)
        print_results(results)
    else:
        file_path = rest[0]
        if len(rest) >= 3:
            min_words, max_words = int(rest[1]), int(rest[2])
        elif len(rest) == 2:
            min_words = int(rest[1])
        result = check_chapter(file_path, min_words, max_words,
                               range_config=range_config, genre=genre)
        print_results([result])


if __name__ == '__main__':
    main()
