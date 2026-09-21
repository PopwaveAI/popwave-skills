#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
deai_gate.py —— 标点规范化与残留检查 v4.0.0

两件事：
  1. --fix ：机械修复（零风险替换，不碰语义）。标点与字形归位的唯一执行处。
  2. --json：精简清单（位置 + 命中 + 建议），交给 agent 自查自改。

用法:
  python deai_gate.py <文件>            出报告（不改文件）
  python deai_gate.py <文件> --fix      先机械修，改后文本写回原文件，再出报告
  python deai_gate.py <文件> --json     JSON 输出（agent 消费）

退出码: 0=无命中  1=有命中  2=参数或文件错误

检查面（只留与新 SKILL.md 三条语感规则和明显残留对得上的项）:
  1. 长句串动作     long_action       一句里三个以上动作
  2. 同义短语重复   repeat_phrase     同一 5 字以上片段反复出现
  3. 情绪直说       emotion_direct    心里一紧/身上发凉/感到一阵 这类直接报情绪
  4. 抽象对偶比喻   abstract_parallel 不是…而是/不仅…而且 ＋ 仿佛/宛如＋抽象名词
  5. 生成器残留     ai_meta           已思考/嗯，用户/（96字）/客服口吻等显式残留
  6. 英文残留行     en_line           整行英文（无汉字）
"""
import argparse
import json
import os
import re
import sys
from collections import Counter

CJK = r'\u4e00-\u9fff'
# 汉字 + 常用中文标点（判断"英文标点是否长在中文语境里"的邻接集）
CJKX = (r'\u4e00-\u9fff\u3001\u3002\uff0c\uff01\uff1f\uff1b\uff1a\uff08\uff09'
        r'\u201c\u201d\u2018\u2019\u2026\u2014\uff5e\u300a\u300b\u3010\u3011')

# ---------------- 零风险修复 ----------------

HTML_ENTITIES = {
    '&nbsp;': ' ', '&amp;': '&', '&lt;': '<', '&gt;': '>', '&quot;': '"',
    '&#39;': "'", '&mdash;': '——', '&ndash;': '—', '&hellip;': '……',
    '&ldquo;': '“', '&rdquo;': '”', '&lsquo;': '‘', '&rsquo;': '’', '&middot;': '·',
}


def fix_fullwidth_ascii(t):
    """全角英文字母数字转半角（ＡＢＣ１２３→ABC123），不碰全角标点。"""
    table = {}
    table.update({i: chr(i - 0xFEE0) for i in range(0xFF10, 0xFF1A)})  # ０-９
    table.update({i: chr(i - 0xFEE0) for i in range(0xFF21, 0xFF3B)})  # Ａ-Ｚ
    table.update({i: chr(i - 0xFEE0) for i in range(0xFF41, 0xFF5B)})  # ａ-ｚ
    return t.translate(table)


def _adj_sub(t, punct, repl):
    """英文标点两侧任一侧是中文（含中文标点）时转全角。"""
    pat = re.compile(r'(?<=[%s])%s|%s(?=[%s])' % (CJKX, re.escape(punct), re.escape(punct), CJKX))
    return pat.sub(repl, t)


# ---------------- 标点规范化（破折号／冒号／括号）----------------
# 三条规则各自写死边界：改哪一处、留哪一处。宁可少改，不改出语病。

DASH = '——'
# 引号开口：冒号后紧跟引号开口，才算对话提示语
QUOTE_OPEN = ('「', '『', '“', '‘', '"', "'")
# 对话提示语动词：冒号紧跟在这些字后（说：/道：/问：/答： 等）才改
SPEECH_VERB = set('说道问答应喊叫嚷骂吼哼念唱叹喝唤嘱诉')

# 成对插入语：X——插入语——Y
PAT_DASH_PAIR = re.compile(
    r'(?<=[\u4e00-\u9fff」』])——([^—\n]{2,20})——(?=[\u4e00-\u9fff「『])')


def _is_han(ch):
    return bool(ch) and '\u4e00' <= ch <= '\u9fff'


def _dash_pair_inner_ok(inner):
    """插入语内部不开新句、不带停顿与引号，才敢整对换成逗号。"""
    return not re.search(r'[。！？…，、；：（）()「」『』“”]', inner)


def _dash_single_to_comma(prev, rest, before):
    """单用破折号改逗号的判据。
    改：后接完整分句的解释说明。
    留：声音延长（前字重复、后接引号或句末）、被打断（行尾截断）、列举与总结前。"""
    if not _is_han(prev):
        return False
    if not _is_han(rest[:1]) or rest[0] == prev:
        return False
    seg = re.split(r'[。！？…]', rest)[0]
    if '—' in seg or '、' in seg or len(seg) < 6:
        return False
    if seg[0] in '，、；：':
        return False
    pre = re.split(r'[。！？…]', before)[-1].strip('，')
    if '、' in pre:
        return False
    if re.search(r'(如下|以下|下列|下面|三种|两样|三样|几样|几点)$', pre):
        return False
    head = re.split(r'[。！？…，、；：「『“”"\n]', before)[-1]
    if len(head) <= 2:
        return False                      # 呼语后拉长音：你——、妈——，保留
    return True


def _paren_comment_ok(inner):
    """短注释与名词性同位语的判据：2-8 字、无句末标点。
    含逗号顿号、纯数字序号、含引号的放行不改，避免改坏内部停顿；
    单字括号（笑）（哭）（停）这类演出提示也放行不改。"""
    if not 2 <= len(inner) <= 8:
        return False
    if re.search(r'[。！？…；，、：]', inner):
        return False
    if re.search(r'[（）()「」『』“”]', inner):
        return False
    return bool(re.search(r'[\u4e00-\u9fff]', inner))


def _clean_inserted_comma(s):
    """局部收尾：新插入的逗号可能跟前后的逗号、句读撞车。"""
    s = re.sub(r'，{2,}', '，', s)
    return re.sub(r'，(?=[。！？；、」』])', '', s)


def fix_punct_norm(t):
    """标点规范化：破折号→逗号、对话提示冒号→逗号、括号短注释→逗号。
    返回 (新文本, {修复名: 处数})。放最后跑：此时引号已归位成「」、全角括号已就位。"""
    counts = {}

    # 1) 破折号：成对插入语前后、单用解释说明 → 逗号；声音延长／打断／列举总结前保留
    n_pair = n_single = 0
    d_lines = []
    for ln in t.split('\n'):
        if DASH not in ln:
            d_lines.append(ln)
            continue

        def _pair(m):
            nonlocal n_pair
            if not _dash_pair_inner_ok(m.group(1)):
                return m.group(0)
            n_pair += 1
            return '，' + m.group(1) + '，'

        new = PAT_DASH_PAIR.sub(_pair, ln)
        res = []
        i = 0
        while i < len(new):
            if new.startswith(DASH, i):
                prev = new[i - 1] if i > 0 else ''
                if _dash_single_to_comma(prev, new[i + 2:], new[:i]):
                    res.append('，')
                    n_single += 1
                else:
                    res.append(DASH)
                i += 2
                continue
            res.append(new[i])
            i += 1
        s = ''.join(res)
        d_lines.append(_clean_inserted_comma(s) if s != ln else s)
    t = '\n'.join(d_lines)
    if n_pair:
        counts['成对破折号改逗号'] = n_pair
    if n_single:
        counts['解释破折号改逗号'] = n_single

    # 2) 冒号：只改对话提示语（说：/道：/问：/答：＋引号）；引号内、列举、总说冒号不动
    n_colon = 0
    c_lines = []
    for ln in t.split('\n'):
        if '：' not in ln:
            c_lines.append(ln)
            continue
        chars = list(ln)
        depth = 0
        for i, ch in enumerate(chars):
            if ch in '「『':
                depth += 1
                continue
            if ch in '」』':
                depth = max(0, depth - 1)
                continue
            if (ch == '：' and depth == 0 and i > 0
                    and chars[i - 1] in SPEECH_VERB
                    and i + 1 < len(chars) and chars[i + 1] in QUOTE_OPEN):
                chars[i] = '，'
                n_colon += 1
        c_lines.append(''.join(chars))
    t = '\n'.join(c_lines)
    if n_colon:
        counts['提示冒号改逗号'] = n_colon

    # 3) 括号：只改短注释与名词性同位语（2-8 字、无句末标点、前后都是汉字）
    n_paren = 0
    p_lines = []
    for ln in t.split('\n'):
        if '（' not in ln:
            p_lines.append(ln)
            continue
        res = []
        i = 0
        changed = False
        while i < len(ln):
            if ln[i] == '（':
                j = ln.find('）', i + 1)
                if j > i:
                    inner = ln[i + 1:j]
                    prev = ln[i - 1] if i > 0 else ''
                    nxt = ln[j + 1] if j + 1 < len(ln) else ''
                    # 前面已是逗号就不再加，后面接句读时多出来的逗号由 _clean_inserted_comma 收掉
                    prev_ok = _is_han(prev) or prev == '，'
                    nxt_ok = _is_han(nxt) or nxt in '，。！？；、」』'
                    if _paren_comment_ok(inner) and prev_ok and nxt_ok:
                        if prev != '，':
                            res.append('，')
                        res.append(inner + '，')
                        n_paren += 1
                        changed = True
                        i = j + 1
                        continue
            res.append(ln[i])
            i += 1
        s = ''.join(res)
        p_lines.append(_clean_inserted_comma(s) if changed else s)
    t = '\n'.join(p_lines)
    if n_paren:
        counts['括号注释改逗号'] = n_paren

    return t, counts


def fix_zero_risk(text):
    """机械修复，不改任何语义。返回 (新文本, {修复名: 处数})。"""
    counts = {}
    t = text

    def bump(name, n):
        if n:
            counts[name] = counts.get(name, 0) + n

    # 0a. 隐形字符清理（复制粘贴常见，肉眼不可见）
    new, n = re.subn(r'[\u200b\u200c\u200d\u2060\ufeff\u00ad]', '', t)
    bump('零宽字符清理', n)
    t = new
    new, n = re.subn('\u00a0', ' ', t)
    bump('不间断空格转普通', n)
    t = new

    # 0a-2. HTML实体解码（AI复制粘贴残留）
    ent_n = 0
    for k, v in HTML_ENTITIES.items():
        if k in t:
            ent_n += t.count(k)
            t = t.replace(k, v)
    bump('HTML实体解码', ent_n)

    # 0a-3. HTML标签剥离（<br>/<p>/<div>等）
    new, n = re.subn(r'</?(?:br|p|div|span|em|strong|b|i|section|article|h[1-6]|blockquote)[^>]*>', '', t)
    bump('HTML标签剥离', n)
    t = new

    # 0a-4. emoji清理（正文不该有emoji；保留★☆→等常用符号）
    new, n = re.subn(r'[\U0001F000-\U0001FAFF\u2600-\u2604\u2607-\u26FF\u2700-\u27BF'
                    r'\u2B50\u2B55\uFE0F]', '', t)
    bump('emoji清理', n)
    t = new

    # 0a-5. 生成器思考/响应残留行整行删除（精确模式，正常正文不可能出现）
    think_line = re.compile(r'^\s*(已思考.*|已深度思考.*|思考中.*|嗯，用户.*|好的，用户.*|'
                            r'（?\s*Response formatting.*|\d+\s*秒\s*)$')
    lines0 = t.split('\n')
    kept = [ln for ln in lines0 if not think_line.match(ln)]
    bump('思考残留行删除', len(lines0) - len(kept))
    t = '\n'.join(kept)

    # 0a-6. tab清理（正文\t一律为AI/排版残留）
    tab_n = t.count('\t')
    if tab_n:
        t = t.replace('\t', '')
    bump('tab清理', tab_n)

    # 0b. markdown残留清理（AI输出正文常带md符号；正文纯文本不应有）
    new, n = re.subn(r'\*\*|__|##|``', '', t)
    bump('markdown符号清理', n)
    t = new
    # markdown斜体（内容含中文）: *X* → X
    def _de_italic(m):
        return m.group(1) if re.search(r'[%s]' % CJK, m.group(1)) else m.group(0)
    new = re.sub(r'\*([^*\n]{1,60})\*', _de_italic, t)
    bump('markdown斜体清理', _diff_count(t, new))
    t = new
    # 删除线 ~~X~~ → X
    new, n = re.subn(r'~~([^~\n]{1,60})~~', r'\1', t)
    bump('markdown删除线清理', n)
    t = new
    lines = t.split('\n')
    md_list = sum(1 for ln in lines if re.match(r'^\s*[-*]\s+\S|^\s*\d+\.\s+\S', ln))
    if md_list:
        lines = [re.sub(r'^(\s*)([-*]\s+|\d+\.\s+)', r'\1', ln) for ln in lines]
        t = '\n'.join(lines)
    bump('markdown列表符清理', md_list)
    # markdown标题符（行首#+空格）与引用符（行首>）
    new, n1 = re.subn(r'^#{1,6}[ \t]+', '', t, flags=re.M)
    new, n2 = re.subn(r'^[ \t]*>[ \t]?', '', new, flags=re.M)
    bump('markdown标题引用符清理', n1 + n2)
    t = new

    # 0c. 破折号变体统一：单—、──、— —、—— —等 → 标准——
    new, n = re.subn(r'—(?:[ \t]?—)+|(?<!)—(?!—)', '——', t)
    n = sum(1 for a, b in zip(t, new) if a != b)
    bump('破折号变体统一', n)
    t = new

    # 0d. 重复标点压缩：，，、、、、；；；：：：→单个
    #     （连续中文句号"。。。"是网文省略号习惯写法，留给后面省略号归一规则；
    #       ？？！！！保留——网文情绪表达合法）
    new, n = re.subn(r'，{2,}|、{2,}|；{2,}|：{2,}',
                     lambda m: m.group(0)[0], t)
    bump('重复标点压缩', n)
    t = new

    # 0e. 相邻句读修正：，。→。 等
    swap = {'，。': '。', '、。': '。', '，、': '，', '、，': '、', '，；': '；', '；，': '；'}
    new, n = re.subn(r'，。|、。|，、|、，|，；|；，',
                     lambda m: swap.get(m.group(0), m.group(0)), t)
    bump('相邻句读修正', n)
    t = new

    # 0f. 行首缩进删除（网文txt惯例顶格）
    lines = t.split('\n')
    indent_n = sum(1 for ln in lines if re.match(r'^[ \t\u3000]+\S', ln))
    if indent_n:
        lines = [re.sub(r'^[ \t\u3000]+(?=\S)', '', ln) for ln in lines]
        t = '\n'.join(lines)
    bump('行首缩进删除', indent_n)

    # 0f-2. 行首标点上移（AI断行错误：逗号句号挂在段首，归位到上一行末尾）
    lines = t.split('\n')
    out_lines = []
    moved = 0
    for ln in lines:
        if out_lines and out_lines[-1].strip() and re.match(r'^[，。、；：]', ln):
            out_lines[-1] = out_lines[-1] + ln[0]
            ln = ln[1:]
            moved += 1
        out_lines.append(ln)
    if moved:
        t = '\n'.join(out_lines)
    bump('行首标点归位', moved)

    # 0g. 中文与数字之间空格删除（"第 3 章"→"第3章"，AI/翻译腔空格）
    new, n = re.subn(r'(?<=[%s])[ \t]+(?=\d)|(?<=\d)[ \t]+(?=[%s])' % (CJKX, CJKX), '', t)
    bump('中数间空格删除', n)
    t = new

    # 1. 全角字母数字 → 半角
    new = fix_fullwidth_ascii(t)
    bump('全角字母数字转半角', sum(1 for a, b in zip(t, new) if a != b))
    t = new

    # 2. 省略号归一：非双字符的…连续串 → 标准双字符……；'… …'→'……'
    def _norm_ellipsis(m):
        return '……' if len(m.group(0)) != 2 else m.group(0)
    new, n = re.subn(r'…+', _norm_ellipsis, t)
    n = sum(1 for a, b in zip(t, new) if a != b)
    bump('单省略号补双', n)
    t = new
    new, n = re.subn(r'…[ \t]+…', '……', t)
    bump('省略号间空格清理', n)
    t = new

    # 3. 半角点串（2个以上）中文邻接 → ……
    new, n = re.subn(r'(?<=[%s])\.{2,}|\.{2,}(?=[%s])' % (CJKX, CJKX), '……', t)
    bump('英文省略号转……', n)
    t = new

    # 4. 连续中文句号（打字式省略号 。。。）→ ……
    new, n = re.subn(r'。{2,}', '……', t)
    bump('连续句号转省略号', n)
    t = new

    # 5. 句读后紧跟句号（！。→！、……。→……）
    new, n1 = re.subn(r'([！？；：，、])。+', r'\1', t)
    new, n2 = re.subn(r'……。+', '……', new)
    bump('重复句读清理', n1 + n2)
    t = new

    # 6. 中文邻接的英文逗号/冒号/分号/问叹号 → 全角
    for punct, repl, name in ((',', '，', '英文逗号'), (':', '：', '英文冒号'),
                              (';', '；', '英文分号'), ('?', '？', '英文问号'),
                              ('!', '！', '英文叹号')):
        new = _adj_sub(t, punct, repl)
        bump(name, _diff_count(t, new))
        t = new

    # 7. 中文后的英文句点 → 。（避开小数/缩写/文件名）
    new, n = re.subn(r'(?<=[%s])\.(?![0-9A-Za-z])' % CJKX, '。', t)
    bump('英文句点转句号', n)
    t = new

    # 8. 括号中文邻接 → 全角
    new, n1 = re.subn(r'\((?=[%s])' % CJKX, '（', t)
    new, n2 = re.subn(r'(?<=[%s])\)' % CJKX, '）', new)
    bump('英文括号转全角', n1 + n2)
    t = new

    # 9. 中文后波浪号 → ～
    #     半角 --／--- 一律不动：不再由脚本生成破折号，破折号只保留原文已有的。
    new, n = re.subn(r'(?<=[%s])~' % CJKX, '～', t)
    bump('半角波浪号转～', n)
    t = new

    # 10. 中文之间的空格不修（"沈念 收"这类收件人/名单格式是有意空格，
    #     误删会改语义）

    # 11. 标点前的空格删除（中 ，→ 中，）
    new, n = re.subn(r'[ \t\u3000]+(?=[，。！？；：、”）])', '', t)
    bump('标点前空格清理', n)
    t = new

    # 11b. 引号内边缘空格（“ 你好 ”→“你好”）
    new, n1 = re.subn(r'“[ \t]+', '“', t)
    new, n2 = re.subn(r'[ \t]+”', '”', new)
    bump('引号内边缘空格清理', n1 + n2)
    t = new

    # 12. 行尾空白 + 3连以上空行压成1空行
    lines = t.split('\n')
    lines = [ln.rstrip(' \t\u3000') for ln in lines]
    bump('行尾空白清理', sum(1 for a, b in zip(t.split('\n'), lines) if a != b))
    t = '\n'.join(lines)
    new, n = re.subn(r'\n{3,}', '\n\n', t)
    bump('多余空行压缩', n)
    t = new

    # 13. 英文双引号配对 → 中文引号（逐行状态机；网文引号不跨行）
    fixed_lines = []
    pair_count = 0
    for ln in t.split('\n'):
        out = []
        inside = False
        for ch in ln:
            if ch == '"':
                out.append('“' if not inside else '”')
                inside = not inside
                pair_count += 1
            else:
                if ch == '“':
                    inside = True
                elif ch == '”':
                    inside = False
                out.append(ch)
        fixed_lines.append(''.join(out))
    t = '\n'.join(fixed_lines)
    bump('英文引号转中文引号', pair_count)

    # 14. 英文单引号：中文邻接且非英文单词内部 → ‘’（逐行配对）
    fixed_lines = []
    sq_count = 0
    for ln in t.split('\n'):
        out = []
        inside = False
        for i, ch in enumerate(ln):
            if ch == "'":
                prev = ln[i - 1] if i > 0 else ''
                nxt = ln[i + 1] if i + 1 < len(ln) else ''
                cjk_adj = _is_cjkx(prev) or _is_cjkx(nxt)
                word_inner = prev.isascii() and prev.isalnum() and nxt.isascii() and nxt.isalnum()
                if cjk_adj and not word_inner:
                    out.append('‘' if not inside else '’')
                    inside = not inside
                    sq_count += 1
                    continue
            out.append(ch)
        fixed_lines.append(''.join(out))
    t = '\n'.join(fixed_lines)
    bump('英文单引号转中文引号', sq_count)

    # 14b. 引号字形统一：弯引号 → 直角引号（逐行状态机；网文引号不跨行）。
    #      两层及以上用直角单引号，符合直角引号体系的嵌套规范。
    #      独立的单弯引号（术语引用、内心独白惯例，正文惯例合法）不动。
    q_lines = []
    q_fix = 0
    for ln in t.split('\n'):
        out = []
        depth = 0
        for ch in ln:
            if ch == '“':
                out.append('「' if depth == 0 else '『')
                depth += 1
                q_fix += 1
                continue
            if ch == '”':
                depth = max(0, depth - 1)
                out.append('」' if depth == 0 else '』')
                q_fix += 1
                continue
            if ch == '「':
                depth += 1
                out.append(ch)
                continue
            if ch == '」':
                depth = max(0, depth - 1)
                out.append(ch)
                continue
            if ch in ('『', '』'):
                out.append(ch)
                continue
            if depth > 0 and ch in ('‘', '’'):
                out.append('『' if ch == '‘' else '』')
                q_fix += 1
                continue
            out.append(ch)
        q_lines.append(''.join(out))
    t = '\n'.join(q_lines)
    bump('标点字形统一', q_fix)

    # 15. 连续ASCII空格压缩（2+→1；中文间空格不修）
    new, n = re.subn(r' {2,}', ' ', t)
    bump('连续空格压缩', n)
    t = new

    # 16. 标点规范化（破折号／对话提示冒号／括号短注释 → 逗号）
    #     放最后跑：引号已归位成「」，全角括号已就位，判定最准。
    new, punct = fix_punct_norm(t)
    for _name, _cnt in punct.items():
        bump(_name, _cnt)
    t = new

    return t, counts


def _is_cjkx(ch):
    return bool(ch) and re.match(r'^[%s]$' % CJKX, ch)


def _diff_count(old, new):
    return sum(1 for a, b in zip(old, new) if a != b)


# ---------------- 检查项（位置 + 命中 + 建议） ----------------

# (id, 名称, 建议)
CHECKS = [
    ('long_action', '长句串动作',
     '一句里三个以上动作的，按动作拆开；最重的那句单独收尾'),
    ('repeat_phrase', '同义短语重复',
     '同一片段反复出现，只留一处，其余换说法或删'),
    ('emotion_direct', '情绪直说',
     '报情绪的词换成身体反应、动作或细节（心里一紧→手停了）'),
    ('abstract_parallel', '抽象对偶比喻',
     '对偶句式拆成两个独立短句；抽象比喻换成看得见的画面'),
    ('ai_meta', '生成器残留',
     '生成器残留（已思考/嗯，用户/（96字）/客服口吻）——整行删除'),
    ('en_line', '英文残留行',
     '整行英文——生成器残留，删除或重写'),
]
CHECK_IDS = {c[0] for c in CHECKS}

# 长句串动作：动作词（三个以上不同动作 + 长句 + 多停顿才算串）
PAT_ACTION = re.compile(
    r'走过|走去|走进|走出|走向|跑|站起|站起身来|起身|坐下|转身|回头|抬头|低头|'
    r'点头|摇头|伸手|抬手|抓起|抓住|握住|握紧|推开|拉开|扯住|拽|扔下|递过去|'
    r'扶着|抱住|拍了拍|按|掀开|翻开|睁眼|闭眼|皱眉|咬牙|看了一眼|看了|望|瞥|盯|'
    r'停住|停下|后退|跨|蹲|跪|靠在|贴上|说|道|问|答|喊|笑|哭|冲|迈')

# 情绪直说：直接报情绪（不给身体反应、不给动作）
PAT_EMOTION = re.compile(
    r'(心里|心中|心头|心底)一[紧沉痛酸暖震凛颤悸喜惊凉]|心里咯噔|'
    r'身上(一)?(发凉|发冷)|脊背(一)?(发凉|发冷)|后背发凉|'
    r'胸口一[紧闷堵]|鼻子一酸|眼眶(一热|泛红)|'
    r'感到|感受到|感觉到|涌上心头|涌上心间|心底泛起|泛起(一丝|一阵|阵阵)')

# 抽象对偶比喻：对偶关联词 + 抽象比喻
PAT_PARALLEL = [
    r'不是[^。！？\n"]{0,12}而是',
    r'不仅[^。！？\n]{0,15}(?:而且|更是|还是|也)',
    r'不只是[^。！？\n]{0,12}(?:还是|更是)',
    r'既[^。！？\n]{0,10}又[^。！？\n]{0,10}(?!而)',
    r'一方面[^。！？\n]{0,15}另一方面',
]
PAT_ABSTRACT_SIMILE = re.compile(
    r'(仿佛|宛如|犹如|如同|像)[^。！？\n]{0,12}'
    r'(潮水|深渊|枷锁|牢笼|漩涡|涟漪|迷雾|寒气|热浪|利刃|刀锋|冰窖|死水|泥潭|巨浪|洪流|风暴)')

# 生成器残留（显式痕迹，正常正文不可能出现）
PAT_AI_META = (r'已思考|已深度思考|思考中|思考残留|用时\d+秒|嗯，用户|好的，用户|'
               r'（\d+字）|\(\d+字\)|Response formatting|作为一个?AI|需要我帮|'
               r'以下是[^，。]{0,6}(分析|回答|介绍|总结|清单|章)|如果你想(即刻)?动笔|'
               r'本章节?[:：]|章节标题[:：]|希望这(段|章|篇)|祝(你|您)(阅读|愉快)|'
               r'希望以上内容|希望对(您|你)有帮助|感谢(您|你)的阅读|'
               r'以上(就是|便是)[^。！？]{0,10}(?:全部|内容|要点|总结|清单|分析|介绍|文件|结果)|如需进一步|欢迎随时(提问|联系)|如有任何问题|'
               r'oaicite|turn0search|turn0image|contentReference|utm_source=chatgpt|'
               r'utm_source=openai|\[citation|\[cite|'
               r'知识截止|我的知识(?:库|范围)|(?:最后|之前)的?训练(?:数据|更新)|'
               r'好问题[！!]|您说得(?:完全)?正确|这是一个很好的?(?:问题|观点)|'
               r'针对您的问题|根据您的需求|非常感谢您的提问|很高兴能帮到您|'
               r'如有疑问[^。！？]{0,8}(?:咨询|联系)|以上供参考|不当之处[^。！？]{0,6}指正')

# 英文残留行（整行无汉字 + 两个 3 字母以上英文词）
PAT_EN_LINE = r'[A-Za-z]{3,}[\s,.;:!?\'\"]+[A-Za-z]{3,}'


def check_text(text):
    """在（已修复的）文本上跑检查。返回 (items, 正文字数)。
    items: [{id, name, total_hits, hits:[{line, snippet}], advice}]"""
    lines = text.split('\n')
    nonblank = [(i, ln) for i, ln in enumerate(lines, 1) if ln.strip()]
    body = ''.join(ln for _i, ln in nonblank)
    n = max(len(body), 1)
    hits = {cid: [] for cid, _name, _advice in CHECKS}
    # 逐字符记行号 + 汉字在 body 中的位置，供重复片段回算行号
    char_line = []
    for i, ln in nonblank:
        char_line.extend([i] * len(ln))
    han_pos = [j for j, ch in enumerate(body) if '\u4e00' <= ch <= '\u9fff']
    HAN = ''.join(body[j] for j in han_pos)

    # 1. 长句串动作
    for i, ln in enumerate(lines, 1):
        if not ln.strip():
            continue
        for s in re.split(r'[。！？…]', ln):
            s2 = s.strip().strip('“”‘’「」')
            if len(s2) < 30 or s2.count('，') < 2:
                continue
            if len(set(PAT_ACTION.findall(s2))) >= 3:
                hits['long_action'].append({'line': i, 'snippet': s2[:60]})

    # 2. 同义短语重复（同一5字片段出现≥3次，位置取首次出现行）
    if len(HAN) >= 300:
        g5 = Counter()
        first = {}
        for k in range(len(HAN) - 4):
            g = HAN[k:k + 5]
            g5[g] += 1
            if g not in first:
                first[g] = k
        for g, c in g5.items():
            if c >= 3:
                hits['repeat_phrase'].append(
                    {'line': char_line[han_pos[first[g]]], 'snippet': '%s ×%d' % (g, c)})
        hits['repeat_phrase'].sort(key=lambda h: -int(h['snippet'].split('×')[1]))

    # 3. 情绪直说
    for i, ln in enumerate(lines, 1):
        for m in PAT_EMOTION.finditer(ln):
            ctx = ln[max(0, m.start() - 6):min(len(ln), m.end() + 6)]
            hits['emotion_direct'].append({'line': i, 'snippet': ctx})

    # 4. 抽象对偶比喻
    for i, ln in enumerate(lines, 1):
        for pat in PAT_PARALLEL:
            for m in re.finditer(pat, ln):
                hits['abstract_parallel'].append({'line': i, 'snippet': m.group(0)[:42]})
        for m in PAT_ABSTRACT_SIMILE.finditer(ln):
            hits['abstract_parallel'].append({'line': i, 'snippet': m.group(0)[:42]})

    # 5. 生成器残留
    for i, ln in enumerate(lines, 1):
        for m in re.finditer(PAT_AI_META, ln):
            ctx = ln[max(0, m.start() - 6):min(len(ln), m.end() + 6)]
            hits['ai_meta'].append({'line': i, 'snippet': ctx})

    # 6. 英文残留行
    for i, ln in enumerate(lines, 1):
        if ln.strip() and not re.search(r'[%s]' % CJK, ln) and re.search(PAT_EN_LINE, ln):
            hits['en_line'].append({'line': i, 'snippet': ln.strip()[:40]})

    items = []
    for cid, name, advice in CHECKS:
        hs = hits.get(cid, [])
        items.append({'id': cid, 'name': name, 'total_hits': len(hs),
                      'hits': hs[:8], 'advice': advice})
    return items, n


# ---------------- 报告（位置 + 命中 + 建议） ----------------

def render_report(path, n_chars, fixes, items, json_out=False, do_fix=False):
    if json_out:
        return {
            'file': path,
            'chars': n_chars,
            'fixes': fixes,
            'checks': items,
            'need_review': [it['id'] for it in items if it['total_hits']],
        }

    out = []
    out.append('=' * 56)
    out.append('正文去AI味检查  %s  (%d字)' % (os.path.basename(path), n_chars))
    out.append('=' * 56)
    if fixes:
        out.append('—— 零风险自动修复（已执行）——')
        for name, cnt in sorted(fixes.items(), key=lambda x: -x[1]):
            out.append('  %-14s %d 处' % (name, cnt))
    elif do_fix:
        out.append('—— 零风险自动修复：已执行，本次无可修复项 ——')
    else:
        out.append('—— 零风险自动修复：未执行（加 --fix 启用）——')
    out.append('')
    out.append('—— 命中项（位置 + 命中 + 建议）——')
    hit_items = [it for it in items if it['total_hits']]
    if not hit_items:
        out.append('  无命中')
    for it in hit_items:
        out.append('  [%s] %d 处' % (it['name'], it['total_hits']))
        out.append('      建议：%s' % it['advice'])
        for h in it['hits']:
            out.append('      L%-4d %s' % (h['line'], h['snippet']))
        if it['total_hits'] > len(it['hits']):
            out.append('      …另有 %d 处' % (it['total_hits'] - len(it['hits'])))
    out.append('')
    if hit_items:
        out.append('结论: %d项命中 —— 按上行定位改写' % len(hit_items))
    else:
        out.append('结论: 全部通过')
    return '\n'.join(out)


def process_file(path, do_fix, json_out):
    raw = open(path, 'rb').read()
    if raw.startswith(b'\xef\xbb\xbf'):
        text, eol = raw.decode('utf-8-sig'), ('\r\n' if b'\r\n' in raw else '\n')
    else:
        try:
            text, eol = raw.decode('utf-8'), ('\r\n' if b'\r\n' in raw else '\n')
        except UnicodeDecodeError:
            text, eol = raw.decode('gb18030'), ('\r\n' if b'\r\n' in raw else '\n')
    text = text.replace('\r\n', '\n')

    if do_fix:
        fixed, fixes = fix_zero_risk(text)
    else:
        fixed, fixes = text, {}
    items, n_chars = check_text(fixed)

    if do_fix and fixed != text:
        out = fixed.replace('\n', eol)
        open(path, 'wb').write(out.encode('utf-8'))
    payload = render_report(path, n_chars, fixes, items, json_out, do_fix)
    has_issue = any(it['total_hits'] for it in items)
    if isinstance(payload, dict):
        return json.dumps(payload, ensure_ascii=False, indent=2), has_issue
    return payload, has_issue


def main():
    ap = argparse.ArgumentParser(description='去AI味：标点与字形规范化（--fix）＋残留检查（--json）')
    ap.add_argument('input', help='正文文件（单文件）')
    ap.add_argument('--fix', action='store_true',
                    help='执行零风险机械修复，改后文本写回原文件')
    ap.add_argument('--json', action='store_true', help='JSON 输出（agent 消费）')
    args = ap.parse_args()

    if not os.path.isfile(args.input):
        print('错误: 找不到文件 %s（本脚本只处理单文件）。用法: python deai_gate.py <正文文件> [--fix] [--json]，详见 --help' % os.path.abspath(args.input), file=sys.stderr)
        sys.exit(2)

    report, any_issue = process_file(args.input, args.fix, args.json)
    print(report)
    sys.exit(1 if any_issue else 0)


if __name__ == '__main__':
    main()
