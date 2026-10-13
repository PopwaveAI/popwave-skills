#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""钩子轮换校验（章级钩子类型）——随包脚本，作者/编辑与 AI 都可跑。

判据（v1.29.22 定，v1.29.22 前无机械判据）
------------------------------------------
HARD-1  章级钩子类型只能取 **A/B/C/D/E 五型**之一
        （空、"待写"、"写作期回填"、"结局"等非类型写法**不算违规**，只列为"未识别"）
HARD-2  **相邻两章（章号差 = 1）不得同型**——这是"轮换"的硬定义
SOFT-1  整卷五型未齐备 → **WARN（不阻断，仅提示）**；
        口径与 `04-章节细纲.md`「卷末三查」②一致（**卷末**看齐备，不是四章）

为什么把「四章内五型齐备」删掉（v1.29.22 缺陷 L1-64）
----------------------------------------------------
`templates/chapter-outline-template.md` 原写「**四章内五型都要出现过一次**」。
在「相邻章不得同型」的约束下，4 个位置最多放 4 种类型，
**放不下 5 种——这条规则数学上不可能满足**；
且与同一文件「卷末三查：五型（A/B/C/D/E）都出现过」**口径互相打架**（四章 vs 整卷）。
本轮定案：**相邻不同型＝硬规则**（可判、存量全过）；**卷内齐备＝软提示**。

输入
----
`02-情绪曲线.md` 的「钩子」节——标题里含"钩子"的 `##` 节。
表头**宽容解析**（存量样本里出现过四种不同表头）：
  · 计划列：`计划钩子类型` / `计划钩子`
  · 实际列：`实际钩子类型` / `实际`（**已回填的以实际为准；未回填回落计划**）
无「实际」列时只用计划列。

用法
----
    python3 check_hook_rotation.py <02-情绪曲线.md> [更多文件…]
    python3 check_hook_rotation.py --all <novels 目录>
    python3 check_hook_rotation.py --selftest        # 污染测试（自证有区分度）

退出码：0 = 无 HARD 违规；1 = 有 HARD 违规；2 = 用法错误／找不到钩子节。
"""

import os
import re
import sys

TYPE_NAMES = {'A': '信息差', 'B': '危机逼近', 'C': '关系转折',
              'D': '规则异常', 'E': '认知颠覆'}
VALID = set(TYPE_NAMES)
# 这些写法表示"尚未确定"，不算违规，只记"未识别"
SOFT_MARKS = ('待写', '待回填', '写作期回填', '未回填', '待定', '结局', '—', '-', '–')
PLAN_KEYS = ('计划钩子类型', '计划钩子')
ACTUAL_KEYS = ('实际钩子类型', '实际')


def find_hook_section(lines):
    """返回标题含「钩子」的 ## 节内容（含标题行）；找不到返回 None。"""
    start = None
    for i, l in enumerate(lines):
        if l.startswith('## ') and '钩子' in l:
            start = i
            break
    if start is None:
        return None
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if lines[j].startswith('## '):
            end = j
            break
    return lines[start:end]


def cells(line):
    return [c.strip() for c in line.strip().strip('|').split('|')]


def is_sep(cs):
    return all(set(c) <= set('-: ') for c in cs if c)


CN_TO_LETTER = {'信息差': 'A', '危机逼近': 'B', '关系转折': 'C',
                '规则异常': 'D', '认知颠覆': 'E'}


def extract_type(cell):
    """从单元格取钩子类型。**先认字母，再认五型中文名**。返回 (字母|None, 写法)。

    认中文名是必要的（v1.29.22 存量普查）：实际样本里出现过
    「信息差钩子」「关系转折钩子」这类只写中文名的做法，
    若只认字母会被整列判成"未识别"，等于漏检。
    """
    if not cell:
        return None, ''
    t = cell.replace('*', '').replace('`', '').strip()
    if not t:
        return None, ''
    m = re.match(r'^([A-E])(?![A-Za-z])', t)
    if not m:
        m = re.search(r'(?<![A-Za-z])([A-E])(?=[\s（(、,，。·/]|$)', t)
    if m:
        return m.group(1), t
    for cn, letter in CN_TO_LETTER.items():
        if cn in t:
            return letter, t
    return None, t


def parse_file(path):
    """返回 (标题, [(章号, 字母|None, 写法, 行号)], 未识别列表) 或 None。"""
    lines = open(path, encoding='utf-8').read().split('\n')
    sec = find_hook_section(lines)
    if sec is None:
        return None
    title = sec[0].strip()
    header, rows = None, []
    for l in sec:
        ls = l.strip()
        if not ls.startswith('|'):
            continue
        cs = cells(ls)
        if is_sep(cs):
            continue
        if header is None:
            header = cs
            continue
        rows.append(cs)
    if header is None:
        return title, [], []

    def col_idx(keys):
        for i, c in enumerate(header):
            if any(k in c for k in keys):
                return i
        return None

    i_plan, i_actual = col_idx(PLAN_KEYS), col_idx(ACTUAL_KEYS)
    i_type = col_idx(('类型',))     # 兜底：有的样本只有一个叫「类型」的列

    seq, unknown = [], []
    for r in rows:
        if not r or not r[0]:
            continue
        m = re.search(r'\d+', r[0])
        if not m:
            continue
        ch = int(m.group())
        letter, raw = None, ''
        if i_actual is not None and i_actual < len(r):
            letter, raw = extract_type(r[i_actual])
        if letter is None and i_plan is not None and i_plan < len(r):
            letter, raw = extract_type(r[i_plan])
        if letter is None and i_type is not None and i_type < len(r):
            letter, raw = extract_type(r[i_type])
        if letter is None:
            # 把该行所有单元格串起来找一次（表头不规范的兜底）
            for c in (r[i_plan] if i_plan is not None and i_plan < len(r) else '',):
                letter, raw = extract_type(c)
            if letter is None and raw and not any(s in raw for s in SOFT_MARKS):
                unknown.append((ch, raw))
        seq.append((ch, letter, raw))
    return title, seq, unknown


def check(seq):
    """返回 (errors, warns)。"""
    errors, warns = [], []
    typed = [(ch, t) for ch, t, _ in seq if t]
    # HARD-2 相邻（章号连续）不得同型
    for (c1, t1), (c2, t2) in zip(typed, typed[1:]):
        if c2 - c1 == 1 and t1 == t2:
            errors.append('第 %d 章与第 %d 章同型（%s %s）——相邻章必须轮换'
                          % (c1, c2, t1, TYPE_NAMES.get(t1, '')))
    # SOFT-1 卷内五型齐备
    used = {t for _, t in typed}
    miss = VALID - used
    if typed and miss:
        warns.append('五型未齐备：缺 %s（%s）——卷末看齐，中间章不必强求'
                     % ('/'.join(sorted(miss)),
                        '、'.join(TYPE_NAMES[m] for m in sorted(miss))))
    return errors, warns


def report(path, title, seq, unknown, errors, warns):
    print('=' * 66)
    print(os.path.basename(os.path.dirname(path)) + ' / ' + os.path.basename(path))
    print('  节标题：%s' % title)
    shown = ' '.join('%d:%s' % (ch, t or '·') for ch, t, _ in seq)
    print('  序列（章:型，·＝未识别）：%s' % (shown or '(空)'))
    if unknown:
        print('  ⚠ 未识别（既不是 A-E，也不在已知的"未填"写法里）：')
        for ch, raw in unknown[:8]:
            print('      第 %d 章 → %r' % (ch, raw[:40]))
    for e in errors:
        print('  [FAIL] ' + e)
    for w in warns:
        print('  [WARN] ' + w)
    if not errors and not warns:
        print('  [PASS] 相邻不同型，五型齐备')
    elif not errors:
        print('  [PASS] 无 HARD 违规（有提示项）')
    return 1 if errors else 0


def run_one(path):
    r = parse_file(path)
    if r is None:
        print('=' * 66)
        print('%s：找不到「钩子」节（标题里含"钩子"的 ## 节）' % path)
        return 2
    title, seq, unknown = r
    errors, warns = check(seq)
    return report(path, title, seq, unknown, errors, warns)


# ── 污染测试：证明本校验器"能放过对、能拦下错" ────────────────────────────
GOOD = """# 02-情绪曲线 · 《样本》

## 3. 章节钩子与伏笔记录

| 章节 | 计划钩子类型 | 具体内容 | 实际钩子类型 |
|---|---|---|---|
| 第1章 | **A 信息差** | 一句 | **A（已回填，与计划一致）** |
| 第2章 | **B 危机逼近** | 一句 | 写作期回填 |
| 第3章 | **C 关系转折** | 一句 | 写作期回填 |
| 第4章 | **D 规则异常** | 一句 | 写作期回填 |
| 第5章 | **E 认知颠覆** | 一句 | 写作期回填 |
"""

SAME_TYPE = GOOD.replace('| 第2章 | **B 危机逼近** |', '| 第2章 | **A 信息差** |')
MISSING = GOOD.replace('**D 规则异常**', '**A 信息差**').replace('**E 认知颠覆**', '**B 危机逼近**')
ODD = GOOD.replace('**A 信息差** | 一句 | **A（已回填，与计划一致）**',
                   '**甲型** | 一句 | **甲型**')
SPARSE = """## 3. 钩子轮换计划

| 章 | 计划钩子 | 实际 | 说明 |
|---|---|---|---|
| 1 | **B 危机逼近** | 待写 | x |
| 6 | **B 危机逼近** | 待写 | x |
| 12 | A 信息差 | 待写 | x |
"""


def selftest():
    import tempfile
    cases = [
        ('合法样本（相邻不同型＋五型齐）', GOOD, 0, False),
        ('改坏①相邻同型', SAME_TYPE, 1, True),
        ('改坏②五型缺（应只 WARN 不 FAIL）', MISSING, 0, False),
        ('改坏③非法写法（应不 FAIL，只列未识别）', ODD, 0, False),
        ('改坏④稀疏章号同型（未连续，不该判相邻）', SPARSE, 0, False),
    ]
    print('=' * 66)
    print('污染测试（自证有区分度）')
    print('=' * 66)
    ok = 0
    d = tempfile.mkdtemp()
    for name, text, want_rc, want_fail in cases:
        p = os.path.join(d, '02-情绪曲线.md')
        open(p, 'w', encoding='utf-8').write(text)
        title, seq, unknown = parse_file(p)
        errors, warns = check(seq)
        rc = 1 if errors else 0
        got_fail = bool(errors)
        good = (rc == want_rc and got_fail == want_fail)
        ok += good
        print('  [%s] %-34s 期望 rc=%d 实际 rc=%d%s'
              % ('OK' if good else '!!', name, want_rc, rc,
                 '' if not errors else '  ← ' + errors[0][:52]))
    print('-' * 66)
    print('结论：%d/%d 通过' % (ok, len(cases)))
    return 0 if ok == len(cases) else 1


def main(argv):
    if len(argv) >= 2 and argv[1] == '--selftest':
        return selftest()
    if len(argv) >= 3 and argv[1] == '--all':
        root = argv[2]
        files = []
        for dp, _, fns in os.walk(root):
            for fn in fns:
                if fn == '02-情绪曲线.md':
                    files.append(os.path.join(dp, fn))
        if not files:
            print('在 %s 下没找到 02-情绪曲线.md' % root)
            return 2
    else:
        files = [a for a in argv[1:] if not a.startswith('-')]
        if not files:
            print(__doc__)
            return 2

    rc, n_fail, n_err = 0, 0, 0
    for f in sorted(files):
        if not os.path.exists(f):
            print('文件不存在：%s' % f)
            n_err += 1
            continue
        r = run_one(f)
        if r == 1:
            n_fail += 1
        elif r == 2:
            n_err += 1
    print('-' * 66)
    print('共 %d 个文件：HARD 违规 %d 个，无法解析 %d 个。' % (len(files), n_fail, n_err))
    if n_fail:
        rc = 1
    print('结论：%s' % ('✅ 相邻章钩子类型均不同型' if not n_fail else '❌ 存在相邻同型，须回细纲重排钩子类型'))
    return rc


if __name__ == '__main__':
    sys.exit(main(sys.argv))
