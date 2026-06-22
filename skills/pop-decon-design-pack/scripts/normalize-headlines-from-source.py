"""
design-pack headline normalizer — source-file based
===================================================

Better than regex-recovering titles from already-wrong first lines.
Reads actual chapter titles from _temp/chapters/chXXX.txt source files
and rewrites design pack first lines to the canonical format:

    # 设计包 — chXXX「标题」

Usage:
    python normalize-headlines-from-source.py \\
        --design-dir 写作资产/设计包v3 \\
        --source-dir _temp/chapters

Strategy:
    For each design pack chXXX, reads chXXX.txt's first line to extract
    the chapter title as it appears in the source text (e.g. "第150章 巫行空"),
    strips the chapter-number prefix and parenthetical suffixes like （月票加）,
    then writes the canonical heading.

Edge cases handled:
    - Chinese numeral chapter numbers (第一百五十章 → 150)
    - Bracket/parenthetical suffixes: （月票800加）(300加)（订阅补更）
    - Chapter number in filename already known; never extracted from the wrong first line
"""

import os, re, sys, argparse

def parse_args():
    p = argparse.ArgumentParser(description='Normalize design-pack headings from source chapter files.')
    p.add_argument('--design-dir', default='写作资产/设计包v3',
                   help='Design pack directory (default: 写作资产/设计包v3)')
    p.add_argument('--source-dir', default='_temp/chapters',
                   help='Source chapter files directory (default: _temp/chapters)')
    p.add_argument('--dry-run', action='store_true',
                   help='Only report, do not modify')
    return p.parse_args()


def extract_title_from_source(source_path: str) -> str | None:
    """Read first line of chapter file and extract title after chapter number."""
    try:
        with open(source_path, 'r', encoding='utf-8') as fh:
            first = fh.readline().strip()
    except (FileNotFoundError, UnicodeDecodeError):
        return None

    # Pattern: 第XXX章 标题内容（可能带括号）
    m = re.search(r'^第[\d零一二三四五六七八九十百千万]+章\s*(.*)', first)
    if not m:
        return None

    title = m.group(1).strip()
    # Strip parenthetical suffixes: （月票800加）(300加)（订阅补更）
    title = re.sub(r'[（(][^）)]*[）)]', '', title).strip()
    return title if title else None


def get_chapter_number(filename: str) -> int | None:
    """Extract integer chapter number from filename like ch150-设计包.md or ch150.txt."""
    m = re.search(r'ch(\d+)', filename)
    return int(m.group(1)) if m else None


def normalize_all(design_dir: str, source_dir: str, dry_run: bool = False) -> dict:
    stats = {'total': 0, 'correct': 0, 'fixed': 0, 'missing_source': 0, 'failed': 0}

    for f in sorted(os.listdir(design_dir)):
        if not f.endswith('.md'):
            continue
        ch = get_chapter_number(f)
        if ch is None:
            continue

        stats['total'] += 1
        dp_path = os.path.join(design_dir, f)

        # Read current first line
        with open(dp_path, 'r', encoding='utf-8') as fh:
            lines = fh.readlines()
        current = lines[0].strip()

        expected = f'# 设计包 — ch{ch:03d}'
        if current.startswith(expected):
            stats['correct'] += 1
            continue

        # Get title from source file
        src_name = f'ch{ch:03d}.txt'
        src_path = os.path.join(source_dir, src_name)
        title = extract_title_from_source(src_path)

        if title is None:
            # Fallback: try to extract from current first line
            fallback_m = re.search(r'[「『"]([^」』"]+)[」』"]', current)
            title = fallback_m.group(1) if fallback_m else f'ch{ch:03d}'
            stats['missing_source'] += 1

        new_first = f'# 设计包 — ch{ch:03d}「{title}」'
        if dry_run:
            print(f'[DRY-RUN] ch{ch:03d}: {current[:50]} → {new_first}')
        else:
            lines[0] = new_first + '\n'
            with open(dp_path, 'w', encoding='utf-8') as fh:
                fh.writelines(lines)
            print(f'Fixed ch{ch:03d}: {title}')

        stats['fixed'] += 1

    return stats


if __name__ == '__main__':
    args = parse_args()
    stats = normalize_all(args.design_dir, args.source_dir, args.dry_run)
    print(f'\n--- Summary ---')
    print(f'Total:     {stats["total"]}')
    print(f'Correct:   {stats["correct"]}')
    print(f'Fixed:     {stats["fixed"]}')
    print(f'Missing src: {stats["missing_source"]}')
    print(f'Failed:    {stats["failed"]}')
    if stats['missing_source']:
        print(f'⚠️  {stats["missing_source"]} files used fallback (source TXT missing/parse error)')
