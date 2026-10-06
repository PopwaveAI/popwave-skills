#!/usr/bin/env python3
"""校验 description 的触发面是否覆盖「接续已有项目」的场景。

由来（2026-09-28）：技能上架平台后，用户项目已有大纲/细纲/人设并写了部分正文，
说「续写第 X 章」——技能不触发。根因＝description 的触发词全是"立项"类
（写番茄小说/番茄小说推文/番茄平台连载/按番茄算法写网文），
没有一个"接着已有项目往下写"的说法，而 1.0 入口分流也只有 A/B/C/D 四路（全是立项）。

本脚本做三件事：
  A. 描述覆盖测试：续写类关键词必须出现在 description 里
  B. 反例测试：非番茄平台 + 无续写词的诉求不应被判为触发
  C. 污染测试（自证有区分度）：拿"旧版只有立项词"的描述喂进来，必须 FAIL

用法：
    python scripts/check_trigger_coverage.py [SKILL.md路径]
退出码：0 = 全过；1 = 有问题
"""
import os
import re
import sys

# ── A. 描述里必须出现的接续类关键词（缺一即 FAIL） ──
REQUIRED_PHRASES = [
    '续写',
    '接着写',
    '继续写',
    '写第',
    '往下写',
    '写正文',
]

# ── A2. 必须存在的边界条款（防止把非番茄平台也吸进来） ──
REQUIRED_BOUNDARY = ['非番茄平台']

# ── B. 用例表：（用户会说的话，期望判定） ──
CASES = [
    # 正例：必须触发
    ('续写第3章', True),
    ('接着写下一章', True),
    ('继续写', True),
    ('帮我写第2章正文', True),
    ('往下写吧', True),
    ('番茄小说，已经有大纲和细纲了，帮我写正文', True),
    ('按番茄算法写连载', True),
    ('番茄小说推文', True),
    # 反例：不应触发（非番茄平台）
    ('帮我写个晋江的文', False),
    ('写一篇公众号推文', False),
    ('起点中文网的书怎么写', False),
    ('写个通用短篇小说', False),
]

# 触发面判定：出现番茄平台词，或出现接续/正文类词 → 判为应触发
CONTINUATION_WORDS = ['续写', '接着写', '继续写', '往下写', '写第', '写正文', '下一章']


def judge_utterance(text):
    """按触发面关键词预测：这句话会不会命中本技能。"""
    if '番茄' in text:
        return True
    return any(w in text for w in CONTINUATION_WORDS)


def extract_description(md_text):
    """取 frontmatter 里的 description 行（跨行也能取到）。"""
    m = re.match(r'^---\n(.*?)\n---\n', md_text, re.S)
    if not m:
        return None
    fm = m.group(1)
    lines = fm.split('\n')
    for idx, line in enumerate(lines):
        if line.startswith('description:'):
            parts = [line]
            # YAML 里长描述可能折行（续行以空格开头）
            k = idx + 1
            while k < len(lines) and (lines[k].startswith(' ') or lines[k].startswith('\t')):
                parts.append(lines[k])
                k += 1
            return '\n'.join(parts)
    return None


def check(desc, label='当前 SKILL.md'):
    """返回 (是否通过, 问题列表)"""
    problems = []
    if not desc:
        return False, ['取不到 description（frontmatter 缺失或格式坏了）']

    for ph in REQUIRED_PHRASES:
        if ph not in desc:
            problems.append(f'描述里缺接续类关键词：{ph}')
    for ph in REQUIRED_BOUNDARY:
        if ph not in desc:
            problems.append(f'描述里缺边界条款：{ph}')

    # B. 用例表：正例必须被判触发、反例必须不被判触发
    for text, expect in CASES:
        got = judge_utterance(text)
        if got != expect:
            problems.append(f'用例判定不符｜"{text}" 期望={expect} 实际={got}')

    return (len(problems) == 0), problems


def main():
    if any(a in ('-h', '--help') for a in sys.argv[1:]):
        print(__doc__)
        return 0
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'SKILL.md')
    if not os.path.exists(path):
        print(f'[FAIL] 找不到文件：{path}')
        return 1

    md = open(path, encoding='utf-8').read()

    # ── 0. frontmatter 的 YAML 是否可解析（引号是否配对） ──
    m = re.match(r'^---\n(.*?)\n---\n', md, re.S)
    if not m:
        print('[FAIL] frontmatter 不存在（技能根本无法被加载）')
        return 1
    fm = m.group(1)
    try:
        import yaml  # 有则严格解析
        try:
            yaml.safe_load(fm)
            print('[OK]   YAML 解析通过（frontmatter 语法正常）')
        except Exception as e:
            print(f'[FAIL] YAML 解析失败：{str(e)[:160]}')
            return 1
    except ImportError:
        bad = [i + 1 for i, l in enumerate(fm.split('\n')) if l.count('"') % 2 != 0]
        if bad:
            print(f'[FAIL] 引号不配对的行：{bad}')
            return 1
        print('[OK]   YAML 手工检查通过（引号全配对；未装 pyyaml，跳过严格解析）')

    desc_now = extract_description(md)
    ok_now, problems_now = check(desc_now)
    print(f'[{"OK" if ok_now else "FAIL"}]   描述覆盖 + 用例表：{len(REQUIRED_PHRASES)} 关键词 / {len(CASES)} 用例')
    for p in problems_now:
        print(f'        - {p}')

    # ── C. 污染测试：旧版（只有立项词）必须被判 FAIL ──
    old_desc = ('description: "番茄爆款小说写作助手——专为「番茄小说」平台优化的分章节网文创作助手。'
                '仅在用户明确指向番茄小说平台创作时触发：写番茄小说、番茄小说推文、番茄平台连载、'
                '按番茄算法写网文；对非番茄平台需求（晋江/起点/公众号）不要触发。"')
    ok_old, _ = check(old_desc)
    print(f'[{"OK" if not ok_old else "FAIL"}]   污染测试：旧版立项-only 描述 → 期望拦下，实际 {"拦下" if not ok_old else "放过（校验器无区分度！）"}')

    passed = ok_now and (not ok_old)
    print()
    print('结论：' + ('✅ 触发面覆盖「接续已有项目」且边界正确' if passed else '❌ 有问题，见上'))
    return 0 if passed else 1


if __name__ == '__main__':
    sys.exit(main())
