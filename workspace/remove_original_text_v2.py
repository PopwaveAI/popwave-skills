"""
Remove all directly exposed original text from chapter design packs (v2).
More aggressive: removes ALL columns that contain direct quotes from the novel,
allows only short quoted phrases (<20 chars) and analysis text.
"""
import re
import os
import glob

DESIGN_DIR = r"D:\workspace\深渊主宰-重写测试\写作资产\设计包v3"


def remove_original_text(md: str) -> str:
    lines = md.split('\n')
    result = []
    i = 0
    total = len(lines)

    while i < total:
        line = lines[i]
        stripped = line.strip()

        # ==================== SECTION REMOVAL (entire blocks) ====================
        
        # 4.3 氛围渲染要点 section - remove entirely (line-by-line original text)
        if re.match(r'^###\s+4\.3\s+氛围渲染要点', stripped):
            i += 1
            while i < total:
                nl = lines[i].strip()
                if nl == '---' or re.match(r'^##\s', nl) or re.match(r'^###\s+4\.4', nl):
                    break
                i += 1
            continue

        # 感官描写 section (old format, e.g. ch055) - aggressive removal of quote lines
        if stripped.startswith('### 感官描写') or stripped == '### 感官描写':
            result.append(line)
            i += 1
            while i < total:
                nl = lines[i].strip()
                if nl.startswith('### ') or nl == '---' or nl.startswith('## '):
                    break
                # Remove lines that are >30 chars inside "quotes" = full sentence quotes
                # Only keep short fragments/keywords
                quote_matches = re.findall(r'"([^"]+)"', lines[i])
                if quote_matches and any(len(q) > 30 for q in quote_matches):
                    # Replace with shortened version (label only if has one)
                    label = re.match(r'^(\s*-\s*\*{0,2}[^*"]+\*{0,2}[：:]\s*)', lines[i])
                    if label:
                        result.append(label.group(1).rstrip())
                    # else skip this line entirely
                else:
                    result.append(lines[i])
                i += 1
            continue

        # ==================== TABLE TRANSFORMATIONS ====================

        # --- Event chain table (L1骨架) with 原文证据 column ---
        if stripped.startswith('|') and '原文证据' in stripped:
            # Remove 原文证据 column from ALL table rows (including header)
            result.append(_remove_column(line, -2))  # remove second-to-last column
            i += 1
            sep_processed = False
            while i < total and lines[i].strip().startswith('|'):
                if not sep_processed and ':-' in lines[i]:
                    sep_processed = True
                    result.append(_remove_column(lines[i], -2))
                else:
                    result.append(_remove_column(lines[i], -2))
                i += 1
            continue

        # --- 2.1 套路 table with 原文案例 column ---
        if stripped.startswith('|') and '原文案例' in stripped:
            result.append(_remove_column(line, -2))
            i += 1
            while i < total and lines[i].strip().startswith('|'):
                result.append(_remove_column(lines[i], -2))
                i += 1
            continue

        # --- 3.2 关键对白标注 table with 对白 column ---
        if re.match(r'^###\s+3\.2\s+关键对白标注', stripped):
            result.append(line)
            i += 1
            # Pass through blank lines
            while i < total and lines[i].strip() == '':
                result.append(lines[i])
                i += 1
            # Pass through any non-table lines
            while i < total and not lines[i].strip().startswith('|'):
                result.append(lines[i])
                i += 1
            # Process table rows (including header and separator)
            while i < total and lines[i].strip().startswith('|'):
                result.append(_remove_dialogue_column(lines[i]))
                i += 1
            continue

        # --- 对白分析 table (old format: 说话者 | 内容 | 功能) ---
        if stripped.startswith('|') and '说话者' in stripped and '内容' in stripped and '功能' in stripped:
            # Remove 内容 column
            result.append(_remove_column(line, -2))
            i += 1
            while i < total and lines[i].strip().startswith('|'):
                result.append(_remove_column(lines[i], -2))
                i += 1
            continue

        # --- 4.2 关键场景三段式 table - remove 感官锚点 column (3rd data column) ---
        if re.match(r'^###\s+4\.2\s+关键场景三段式', stripped):
            result.append(line)
            i += 1
            while i < total and not lines[i].strip().startswith('|'):
                result.append(lines[i])
                i += 1
            while i < total and lines[i].strip().startswith('|'):
                parts = lines[i].split('|')
                # Columns: 阶段 | 动作/画面 | 感官锚点 | 节奏
                # Remove 感官锚点 (index 3, 0-based counting columns)
                if len(parts) >= 5:
                    new_parts = parts[:3] + parts[4:]
                    new_row = '|'.join(new_parts)
                    if lines[i].strip().endswith('|') and not new_row.strip().endswith('|'):
                        new_row += '|'
                    result.append(new_row)
                else:
                    result.append(lines[i])
                i += 1
            continue

        # ==================== LINE TRANSFORMATIONS ====================

        # --- 🔒 不可替换 / 🔔 不可替换 - remove quoted text ---
        if re.match(r'^>\s*[🔒🔔]\s*', stripped):
            # Remove all "..." + （"..."） + 「...」 style quotes
            new_line = re.sub(r'[（(]\s*"[^"]*"\s*[）)]', '', line)
            new_line = re.sub(r'"[^"]{5,}"', '', new_line)
            new_line = re.sub(r'「[^」]+」', '', new_line)
            new_line = re.sub(r'《[^》]+》', '', new_line)
            # Clean up double dashes and spaces
            new_line = re.sub(r'——{2,}', '——', new_line)
            new_line = re.sub(r'\s{2,}', ' ', new_line)
            new_line = new_line.rstrip()
            if new_line.strip() in ('>', '', '> ') or (new_line.strip().endswith('：') or new_line.strip().endswith(':')) and not re.search(r'[^\s：:]', new_line.strip()[:-1]):
                i += 1
                continue
            result.append(new_line)
            i += 1
            continue

        # --- 名句 section items (old format) - quoted text removal ---
        # e.g., `- 名句： "xxx"` or `- **名句**: "xxx"`
        if '名句' in line and re.match(r'^\s*[-*]\s*\*{0,2}名句\*{0,2}', stripped):
            # Remove the quote part, keep label
            label = re.match(r'^(\s*[-*]\s*\*{0,2}名句\*{0,2}[：:]\s*).*$', line)
            if label:
                result.append(label.group(1).rstrip())
            else:
                result.append(line)
            i += 1
            continue

        # --- 台词集 items - remove quotes ---
        if stripped.startswith('- 台词：') or stripped.startswith('- 台词:'):
            label = re.match(r'^(\s*-\s*台词[：:]\s*).*$', line)
            if label:
                result.append(label.group(1).rstrip())
            else:
                result.append(line)
            i += 1
            continue

        # --- 爽点机制 section - inline long quotes removal ---
        # These often have: `"long original text quote"——analysis`
        # Remove quoted strings > 25 chars, but keep the surrounding analysis
        if re.match(r'^\s*-\s*\*{0,2}', stripped) and '：' not in stripped[:5]:
            # Check for long quotes
            new_line = _remove_long_quotes(line)
            if new_line != line:
                result.append(new_line)
                i += 1
                continue

        # Default: keep line
        result.append(line)
        i += 1

    # Post-process
    cleaned = '\n'.join(result)
    cleaned = re.sub(r'\n{4,}', '\n\n\n', cleaned)
    cleaned = '\n'.join(l.rstrip() for l in cleaned.split('\n'))
    return cleaned


def _remove_column(line: str, col_index: int) -> str:
    """Remove a column by index from the right (negative). col_index=-2 removes second-to-last."""
    parts = line.split('|')
    if len(parts) >= -col_index:
        new_parts = parts[:col_index] + parts[col_index+1:]
        new_row = '|'.join(new_parts)
        if line.strip().endswith('|') and not new_row.strip().endswith('|'):
            new_row += '|'
        return new_row
    return line


def _remove_dialogue_column(line: str) -> str:
    """Remove the 对白 (dialogue) column from 关键对白标注 table.
    Columns: 谁说 | 对谁说 | 语气 | 对白 | 潜台词
    Remove index 4 (0-based), which is the 4th data column.
    """
    parts = line.split('|')
    # header: | 谁说 | 对谁说 | 语气 | 对白 | 潜台词 |
    # data:   | X    | Y      | Z    | "..."| 潜台词 |
    if len(parts) >= 6:
        # Remove the 对白 column (index 4, before 潜台词 at index 5)
        new_parts = parts[:4] + parts[5:]
        new_row = '|'.join(new_parts)
        if line.strip().endswith('|') and not new_row.strip().endswith('|'):
            new_row += '|'
        return new_row
    return line


def _remove_long_quotes(text: str) -> str:
    """Remove quoted strings > 25 chars from the text, but keep the surrounding analysis."""
    def replace_quote(m):
        q = m.group(1)
        if len(q) > 25:
            return ''
        return m.group(0)
    
    new_text = re.sub(r'"([^"]*)"', replace_quote, text)
    # Clean up artifacts
    new_text = re.sub(r'：\s*——', '——', new_text)
    new_text = re.sub(r'——{2,}', '——', new_text)
    new_text = re.sub(r'\s{2,}', ' ', new_text)
    return new_text.strip()


def process_all_files():
    files = sorted(glob.glob(os.path.join(DESIGN_DIR, 'ch*-设计包.md')))
    total = len(files)
    modified = 0
    errors = []

    for idx, filepath in enumerate(files, 1):
        basename = os.path.basename(filepath)
        print(f"[{idx}/{total}] {basename}...", end=' ')
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                original = f.read()
            
            cleaned = remove_original_text(original)
            
            if cleaned != original:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(cleaned)
                print("✓")
                modified += 1
            else:
                print("·")
        
        except Exception as e:
            print(f"✗ ERROR: {e}")
            errors.append((basename, str(e)))

    print(f"\n=== Summary ===")
    print(f"Total: {total} | Modified: {modified} | Errors: {len(errors)}")
    for name, err in errors:
        print(f"  ERROR: {name}: {err}")


if __name__ == '__main__':
    process_all_files()
