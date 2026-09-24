#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
番茄章节「过审自检」客观指标统计脚本（2026-09-21 新增）

用途：把 `references/audit-checklist.md` 里原本只能"靠感觉"判定的 P0 项，
      跑成可复核的数字——AI 粗制滥造 / 格式混乱 / 空洞水文三组都有可用指标。

统计口径（与 check_chapter_wordcount.py 一致）：只统计 `## 正文` 节，
不含元数据块、章节备注、写后自检清单。

用法：
    python chapter_stats.py <章节文件>
    python chapter_stats.py --all <目录>

输出各项均带 PASS / WARN / FAIL 判定，P0 项出现 FAIL 即不得交付。
退出码：0 = 全部 P0 通过；1 = 有 P0 不通过。

判定主体（v1.22.0 明确）：脚本只自动判定「确定性错误」（格式/标点/重复等），
      并为语义类判据提供**定位材料**。报告中凡出现「确认／复核／四问」字样的项，
      **执行者一律是跑本技能的模型**（逐段回原文取证），**不是用户**。
      「碎／跳」的判定流程见 references/prose-rules-supplement.md **S7.2**；写前机制见 **S7.1**。
"""

import os
import re
import sys
from pathlib import Path

if sys.platform == 'win32':
    import io
    if hasattr(sys.stdout, 'buffer'):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

AI_WORDS = [
    '此外', '然而', '总而言之', '值得注意的是', '综上所述', '凸显', '强调',
    '不禁', '油然而生', '深深地', '毫无疑问', '由此可见',
]
# v1.15.0 修：原先 '最后' / '首先' / '其次' 直接做子串匹配，会误伤正常用法
#   （实测："夏"字的最后一横拖得特别长 / 抄完剩下两页 / 左上最后一把伞）
# 改为**语境判定**：只有充当连接词（句首或另起一句，且后面紧跟逗号/顿号）才算 AI 腔。
AI_WORDS_CTX = {
    '最后': r'(?:^|[。！？；\n])\s*最后[，,、]',
    '首先': r'(?:^|[。！？；\n])\s*首先[，,]',
    '其次': r'(?:^|[。！？；\n])\s*其次[，,]',
}
FULL_QUOTES = ('“', '”')


def extract_body(path: Path) -> tuple:
    """取正文，返回 (文本, 来源标记)。

    来源标记：
      'section'   —— 标准 `## 正文` 节（技能自产章节的正常路径）
      'md-title'  —— 回落：含「章」的一级标题之后
      'txt-cut'   —— 纯 txt：按「第X章」标题只取第一章（v1.22.1 新增）
      'txt-whole' —— 纯 txt 且无章节标题：全篇当正文
    """
    lines = path.read_text(encoding='utf-8').split('\n')
    start = None
    for i, line in enumerate(lines):
        if re.match(r'^#{2,}\s*正文\s*$', line.strip()):
            start = i
            break
    if start is None:
        # 回落：从含「章」的一级标题下一行起
        for i, line in enumerate(lines):
            if line.startswith('#') and '章' in line:
                return '\n'.join(lines[i + 1:]), 'md-title'
        # 纯 txt（用户发来的样本常是这种）：按「第X章」标题切分，只取第一章，
        #   与「一章一文件」的统计口径一致。
        #   v1.22.1 回跑 ch001.txt 暴露：旧版把全篇当正文，`—— 第二章` 这种分隔行
        #   被算成正文破折号（3 处里 1 处是误报），字数也虚高。
        cm = re.compile(r'^[\s\-—–]*第[〇零一二三四五六七八九十百千两0-9]+[章节回]')
        marks = [i for i, l in enumerate(lines) if cm.match(l.strip())]
        if len(marks) >= 2:
            return '\n'.join(lines[marks[0] + 1:marks[1]]), 'txt-cut'
        if len(marks) == 1:
            # 唯一标记要判它在哪一头：贴着文件开头 = 本章标题（正文在其后）；
            #   落在中后部 = 下一章的标题（正文在其前）。
            #   ch001.txt 正是后者：`—— 第二章` 在第 43 行，第 1 章正文在它之前。
            if marks[0] <= 2:
                return '\n'.join(lines[marks[0] + 1:]), 'txt-cut'
            return '\n'.join(lines[:marks[0]]), 'txt-cut'
        return '\n'.join(lines), 'txt-whole'
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if re.match(r'^#{1,6}\s', lines[j].strip()):
            end = j
            break
    return '\n'.join(lines[start + 1:end]), 'section'


def cn_count(text: str) -> int:
    return len(re.findall(r'[\u4e00-\u9fff]', text))


def is_pure_dialogue_line(line: str) -> bool:
    """整行**只有对白**（可含多段引号对白），无引号外的叙述字。

    v1.23.1 修正：此前遮蔽测试用「行内含引号」当判据，会把
    「“今天那句，”他说，“往后别说了。”」这种**对白夹叙述**的行也算成"纯对白"，
    导致遮蔽测试待办段**假阳性**（2026-09-23 武侠仙侠第 1 章实测：报出 1 段，
    遮读后发现该段叙述完整，实际无需处理）。
    正确判据：**去掉全部引号对白段与标点后，若不再剩汉字，才是纯对白行。**
    """
    s = line.strip()
    if not any(q in s for q in FULL_QUOTES):
        return False
    core = re.sub(r'“[^”]*”|「[^」]*」|『[^』]*』', '', s)
    core = re.sub(r'[，。、！？：；…\u2014\s“”「」『』"\'（）()《》]', '', core)
    return cn_count(core) == 0


def analyze(path: Path) -> dict:
    body, body_src = extract_body(path)
    total = cn_count(body)
    raw_lines = body.split('\n')
    lines = [l for l in raw_lines if l.strip()]

    # 正文区末尾的结构分隔符（其后到下一个标题之间全是空行）不算 Markdown 残留
    last_content = len(raw_lines) - 1
    while last_content >= 0 and raw_lines[last_content].strip() == '':
        last_content -= 1
    trailing_sep_ok = last_content >= 0 and raw_lines[last_content].strip() == '---'

    # 对话占比：含全角引号的行的汉字数 / 正文汉字数
    dlg_lines = [l for l in lines if any(q in l for q in FULL_QUOTES)]
    dlg = sum(cn_count(l) for l in dlg_lines)
    dlg_ratio = dlg / total if total else 0

    # 句长与段落
    # v1.21.0 修正：句切分须**至少含 1 个汉字**才算一句。
    # 起因：`“表呢？”` 按 `？` 切会留下一个孤立的 `”`，它汉字数为 0 却被当成"≤6 字的短句"计入碎句链/短句率。
    # 影响实测：《停摆》三章各只有 1 个伪句，碎句链 7/7/15 **完全不变**，短句率变化 <0.5%（35.3→35.0）。
    # 故历史结论不受影响；此处按正确口径修正，避免其他文本上出现偏差。
    sents = [s for s in re.split(r'[。？！]', body) if cn_count(s) > 0]
    avg_sent = total / len(sents) if sents else 0
    para_lens = [cn_count(p) for p in lines]
    same_run = 0
    for i in range(len(para_lens) - 2):
        if para_lens[i] == para_lens[i + 1] == para_lens[i + 2] and para_lens[i] > 0:
            same_run += 1
    longest = max(para_lens) if para_lens else 0

    # AI 词与标点
    ai_hits = [w for w in AI_WORDS if w in body]
    ai_hits += [w for w, pat in AI_WORDS_CTX.items() if re.search(pat, body)]
    ascii_dq = body.count('"')
    ascii_sq = body.count("'")
    # v1.26.0 新增：正文混入 ASCII 字母/数字（2026-09-23 古代言情 L1 实测抓到的门禁缺口——
    # 旧版只查 ASCII 引号，正文里混进拉丁字母/半角数字完全检不出）
    # 口径校准（2026-09-23 同日回跑后拆分，依据「门禁不得误伤正例」）：
    #   · **拉丁字母** = FAIL —— 中文正文里混进英文单词/字母，对读者是明显出戏，无正当理由
    #   · **半角数字** = WARN —— 型号/年代/编号（如「上海牌 7120」）在中文网文里是正常写法，
    #     回跑《停摆》第 1 章时确认：若一并判 FAIL，会误杀已被门禁认可的正例
    ascii_letter_hits = []
    ascii_digit_hits = []
    for _i, _l in enumerate(lines, 1):
        for _m in re.finditer(r'[A-Za-z]+', _l):
            _s = max(0, _m.start() - 6)
            _e = min(len(_l), _m.end() + 6)
            ascii_letter_hits.append((_i, _l[_s:_e].strip()))
        for _m in re.finditer(r'[0-9]+', _l):
            _s = max(0, _m.start() - 6)
            _e = min(len(_l), _m.end() + 6)
            ascii_digit_hits.append((_i, _l[_s:_e].strip()))
    ascii_letter = len(ascii_letter_hits)
    ascii_digit = len(ascii_digit_hits)
    md_residue = len([l for l in lines if l.strip() == '---'])
    if trailing_sep_ok and md_residue:
        md_residue -= 1  # 结构分隔符不计

    # 破折号（v1.15.0 新增：用户 2026-09-22 定为高优先级格式死线——正文零破折号）
    dash_em = body.count('——')
    dash_single = body.count('—') - dash_em * 2
    dash_en = body.count('–')
    dash_total = dash_em + dash_single + dash_en
    dash_lines = [l.strip() for l in lines if ('—' in l or '–' in l)]
    # v1.22.1：定位材料改为「破折号前后各 10 字」。
    #   旧版取行首 26 字——破折号在句中时（如《南味入京》第 1 章「…青苔——那是…」）
    #   提示里根本看不到破折号，等于没定位。回跑实测暴露，见 prd/全类型覆盖测试矩阵.md M7 回跑记录。
    dash_hits = []
    for _i, _l in enumerate(lines, 1):
        for _m in re.finditer(r'——|—|–', _l):
            _s = max(0, _m.start() - 10)
            _e = min(len(_l), _m.end() + 10)
            dash_hits.append((_i, _l[_s:_e].strip()))

    # ---- v1.18.0 新增：文笔层「S3 信息承载 / S5 碎句节奏」机器化指标 ----
    # 背景：用户 2026-09-22 截图批注「信息走对话做成没信息的短句乒乓球」
    #       「一大堆短句，碎句，跳」——原文规则在，却没有可判定的执行层。
    # 全部基于 `## 正文` 节，与原口径一致。

    # 1) 碎句（≤6 汉字的句子）占比与最长连续链
    sent_cn = [cn_count(s) for s in sents]          # 逐句汉字数
    n_sent = len(sent_cn)
    short_n = sum(1 for n in sent_cn if n <= 6)
    short_ratio = short_n / n_sent if n_sent else 0
    s_run = s_best = 0
    for n in sent_cn:
        if n <= 6:
            s_run += 1
            s_best = max(s_best, s_run)
        else:
            s_run = 0
    # 句长总体标准差（体现长短交错程度）
    sent_sd = (sum((n - (sum(sent_cn) / n_sent)) ** 2 for n in sent_cn) / n_sent) ** 0.5 if n_sent else 0

    # 2) 对白行节奏：以「原序相邻的纯对白行」为单位，不跨叙述行统计
    def _inner_cn(line: str) -> int:
        q = re.findall(r'“([^”]*)”', line)
        return cn_count(''.join(q)) if q else cn_count(line)

    is_dlg = [any(q in l for q in FULL_QUOTES) for l in lines]
    # 最长「连续纯对白行」链
    d_run = d_best = 0
    d_start = d_best_start = 0
    for i, d in enumerate(is_dlg):
        if d:
            if d_run == 0:
                d_start = i
            d_run += 1
            if d_run > d_best:
                d_best, d_best_start = d_run, d_start
        else:
            d_run = 0
    # 最长「连续短对白行」链（引号内 ≤10 汉字）——S3.3，治乒乓球
    sd_run = sd_best = 0
    sd_start = sd_best_start = 0
    for i, (l, d) in enumerate(zip(lines, is_dlg)):
        if d and _inner_cn(l) <= 10:
            if sd_run == 0:
                sd_start = i
            sd_run += 1
            if sd_run > sd_best:
                sd_best, sd_best_start = sd_run, sd_start
        else:
            sd_run = 0
    short_dlg_lines = [l for l, d in zip(lines, is_dlg) if d and _inner_cn(l) <= 10]
    # 无信息应答行（引号内 ≤3 汉字，如“够。”“在。”“没有。”）——S3.2 连招侦测
    # 无信息应答行（引号内 ≤3 汉字，如“够。”“在。”“没有。”）
    # 单发不算错——原作者风格本就简省；**连续 ≥3 行**才是 S3.2 说的"连招回避"。
    # 故这里存的是「每条连招的长度」而不是行本身，供 verdict 判最长连招。
    echo_lines = []
    e_run = 0
    for l, d in zip(lines, is_dlg):
        if d and _inner_cn(l) <= 3:
            e_run += 1
        else:
            if e_run:
                echo_lines.append(e_run)
            e_run = 0
    if e_run:
        echo_lines.append(e_run)
    # 遮蔽测试辅助：列出所有「连续 ≥3 行纯对白」段，供 S3.2 遮蔽测试取证（执行者＝模型，见 S7.2）
    # v1.23.1 修正两处：① 判据由「行内含引号」改为 is_pure_dialogue_line（去假阳性）
    #                  ② 区间起点原为 `i - r + 1`，多含了一行非对白行（off-by-one）
    pure_dlg = [is_pure_dialogue_line(l) for l in lines]
    blind_spans = []
    r = 0
    for i, d in enumerate(pure_dlg):
        if d:
            r += 1
        else:
            if r >= 3:
                blind_spans.append((i - r, r))       # 0-based 起点
            r = 0
    if r >= 3:
        blind_spans.append((len(pure_dlg) - r, r))

    # ---- v1.21.0 新增：承接测试的「定位材料」（只把位置摆出来，不判定）----
    # 用户 2026-09-23 把两个词的定义钉死了：
    #   「碎」＝句子短，**且看不出具体要干什么、看不出行为模式和逻辑**（不只是"没新信息"）
    #   「跳」＝情节到情节没有连接。用户原例：
    #          「我躺在床上睁开了眼睛，打湿毛巾把脸好好地擦了一下，终于清醒过来了。」
    #          ——躺着 → 打湿毛巾之间缺「起身／下床／取毛巾／走到水边」这一串中间步骤。
    # 两条都不可「正则化」（形态不可分），但**判定不必由人来做**：脚本负责把「该测的位置」摆出来（防漏），
    # 再由执行本技能的模型按四问逐段判并输出举证表（references/prose-rules-supplement.md S7.2）。
    # 【v1.22.0 更正】v1.21.0 曾写成"只能人工判"——错。用户 2026-09-23 质疑「就是你改不掉？然后只能让人工
    #   给你一条条指出来？」，并给反证：交付的 ch001 系 gemini 3.8 生成、无此类问题。正解＝写前堵（S7.1）＋写后模型自检（S7.2）。
    # A) 最长连续碎句链的原文（可直接拿去做第 1／2 问的取证材料）
    frag_span_txt = []
    _cur = []
    for i, n in enumerate(sent_cn):
        if n <= 6:
            _cur.append(i)
            if s_best and len(_cur) == s_best:
                frag_span_txt = [sents[j].strip().replace('\n', '').strip('“”') for j in _cur]
        else:
            _cur = []
    # B) 【已试并撤除·2026-09-23】「一句内连缀多个无过渡动作」候选检测
    #    做法：一句内 ≥3 个逗号分句、分句均长 ≤13、≥2 个含动作动词、且全句无过渡词
    #          （起身／下床／走过去／拿起…），即列为「疑似动作链断层」。
    #    校准结果（用户原例「我躺在床上睁开了眼睛，打湿毛巾把脸好好地擦了一下，终于清醒过来了」
    #    能被命中，含过渡词的对照句不命中——**检测器本身有效**），但**无区分度**：
    #         8 本正例候选密度中位 2.4 句/千字（区间 1.2–3.0），
    #         《停摆》三章同为 2.4 句/千字；且正例候选句形态相同却完全成立
    #         （如《停摆》「他把目镜推上额头，指腹压住表蒙，往下按了半分」本身是完整动作链）。
    #    → 按本项目纪律「抓不住的就不设门槛，宁可不加也不要加噪声」**撤除**（正则检测器）。
    #    → 「跳」的判定改由**四问自检子流程**执行：判据动作＝「**把这段照着做一遍，中间步骤在不在**」
    #      （用户 2026-09-23 定义），执行者＝跑本技能的模型（references/prose-rules-supplement.md S7.2）。
    #      **不要再造第三个正则检测器**——形态确实不可分；要加的是"生成端约束"（S7.1 动作链），不是又一个正则。

    # ---- v1.20.0 新增：通用硬伤层（唯一保留的门禁；其余风格项一律只报数）----
    # 依据：用户 2026-09-23「病句，碎句，跳，上下句描述错误，这种问题是通用不能有的」
    #       ＋ 8 本异风格正例全量扫描——除本层外，一切节奏/粒度指标都能在正例里找到更极端的反例
    #       （《月光盒子》碎句链 15、短对白链 15，与《停摆》第 3 章同值）。
    # 只扫 `## 正文`；排除标题、引用块 `>`、列表标记，避免把元数据当正文判。
    TITLE_LIKE = re.compile(
        r'^(?:第\s*[0-9０-９一二三四五六七八九十百千零两]+\s*章'
        r'|第\s*(?:[0-9]+|[一二三四五六七八九十百千]+)\s*[节回]'
        r'|Chapter\s*\d+|#{1,6}\s|[*\-_=—]{2,})')
    punct_mismatch, punct_repeat = [], []
    quote_unbalanced, adjacent_dup, dup_char = [], [], []
    half_sent, no_end_punct = [], []
    prev_line = None
    for i, l in enumerate(lines):
        s = l.strip()
        if (TITLE_LIKE.match(s) or s.startswith('>')
                or re.match(r'^[-*+]\s|^\d+[\.、]\s', s)):
            prev_line = s
            continue
        # 标点连用（同种重复：。。 ！！ ？？）
        for m in re.finditer(r'([。！？])\1+', s):
            punct_repeat.append((i, m.group()))
        # 标点错配（不同终止/停顿标点直接相邻：？。 。！ ，。 等）
        if re.search(r'[。！？，][。！？，]', s):
            for m in re.finditer(r'[。！？，][。！？，]', s):
                if m.group()[0] != m.group()[1]:
                    punct_mismatch.append((i, s))
                    break
        # 引号不配对
        if s.count('“') != s.count('”'):
            quote_unbalanced.append((i, s))
        # 相邻行完全重复
        if prev_line is not None and s == prev_line and cn_count(s) > 2:
            adjacent_dup.append((i, s))
        # 叠字错误
        for m in re.finditer(r'(她她|他他|的的|了了|是是|在在|和和|就就|都都|我我|你你)', s):
            dup_char.append((i, m.group()))
        # 半截句（逗号/顿号/分号收尾）与行尾无终止标点
        if re.search(r'[，、；：]$', s) and cn_count(s) > 4:
            half_sent.append((i, s))
        elif cn_count(s) >= 6 and not re.search(r'[。！？…”』」）】]$', s):
            no_end_punct.append((i, s))
        prev_line = s

    # 跨章对白复现检测用：末尾 12 行里的对白行（去标点后比对）
    tail_norm = [re.sub(r'[\s“”‘’"\'。，！？、；：]', '', l)
                 for l in lines[-20:] if any(q in l for q in FULL_QUOTES)]
    tail_dlg = [t for t in tail_norm if cn_count(t) >= 2]

    return {
        'file': str(path),
        'total': total,
        'dlg': dlg,
        'dlg_ratio': dlg_ratio,
        'avg_sent': avg_sent,
        'same_run': same_run,
        'longest_pct': (longest / total * 100) if total else 0,
        'ai_hits': ai_hits,
        'ascii_dq': ascii_dq,
        'ascii_sq': ascii_sq,
        'ascii_letter': ascii_letter,
        'ascii_letter_hits': ascii_letter_hits,
        'ascii_digit': ascii_digit,
        'ascii_digit_hits': ascii_digit_hits,
        'md_residue': md_residue,
        'dash_total': dash_total,
        'dash_lines': dash_lines,
        'dash_hits': dash_hits,
        'body_src': body_src,
        'paras': len(para_lens),
        # --- v1.18.0 ---
        'n_sent': n_sent,
        'short_ratio': short_ratio,
        'sent_sd': sent_sd,
        'short_run': s_best,
        'dlg_run': d_best,
        'dlg_run_lines': lines[d_best_start:d_best_start + d_best],
        'short_dlg_run': sd_best,
        'short_dlg_lines': lines[sd_best_start:sd_best_start + sd_best],
        'short_dlg_total': len(short_dlg_lines),
        'dlg_total_lines': len(dlg_lines),
        'echo_lines': echo_lines,      # 每段「连招」各自的长度
        'blind_spans': blind_spans,
        # --- v1.20.0 通用硬伤层 ---
        'punct_mismatch': punct_mismatch,
        'punct_repeat': punct_repeat,
        'quote_unbalanced': quote_unbalanced,
        'adjacent_dup': adjacent_dup,
        'dup_char': dup_char,
        'half_sent': half_sent,
        'no_end_punct': no_end_punct,
        'tail_dlg': tail_dlg,
        'dlg_line_ratio': (len(dlg_lines) / len(lines)) if lines else 0,
        # --- v1.21.0 承接测试定位材料 ---
        'frag_span_txt': frag_span_txt,
    }


def verdict(r: dict) -> list:
    """返回 (项目, 值, 判定, 说明) 列表；判定取 PASS / WARN / FAIL"""
    rows = []
    rows.append(('正文字数', f"{r['total']}",
                 'PASS' if 2200 <= r['total'] <= 2800 else 'FAIL', '区间 2200-2800'))
    # v1.19.0 废除「对话占比 ≥30%」门槛；v1.20.0 进一步把口径统一为「行占比」，
    # 与 references/benchmark-writing.md 第一节的样本画像同尺（旧口径是汉字占比，两者数值不可比）。
    rows.append(('对白行占比（参考值·不判定）',
                 f"{r['dlg_line_ratio'] * 100:.1f}%（{r['dlg_total_lines']}/{r['paras']} 行）", 'INFO',
                 '正例区间 0–94%（《第365天》18.6%／《昨日书》42.5%／《宠宠欲动》53%，单章最高 92%）。'
                 'v1.19.0 已废除旧的「≥30%」门槛：占比高低不指示质量。'
                 '对白是否合格走 ①遮蔽测试（S3.2）②承接测试第 1 问（每行让局面动一格）'))
    rows.append(('AI 高频词', ('、'.join(r['ai_hits']) if r['ai_hits'] else '无'),
                 'FAIL' if r['ai_hits'] else 'PASS', '命中即 FAIL'))
    rows.append(('连续 3 段等长段落', f"{r['same_run']} 处",
                 'PASS' if r['same_run'] == 0 else 'WARN', '疑似句式雷同，需复核'))
    rows.append(('最长段落占比', f"{r['longest_pct']:.1f}%",
                 'PASS' if r['longest_pct'] <= 40 else 'WARN', '单一场景 ≤40%'))
    rows.append(('正文内 Markdown 残留 ---', f"{r['md_residue']} 根",
                 'PASS' if r['md_residue'] == 0 else 'FAIL', '格式混乱 P0，跑 format_chapter.py'))
    dash_note = ('正文零破折号——用户 2026-09-22 定的高优先级格式死线（v1.15.0）。'
                 '改写句子或换用句号/逗号/冒号，**不要用其他标点简单替换凑数**')
    if r['dash_total']:
        _hd = '；'.join(f"第{i}行「…{t}…」" for i, t in r['dash_hits'][:3])
        dash_note = f"{_hd} → " + dash_note
    rows.append(('破折号 —— / — / –', f"{r['dash_total']} 处",
                 'PASS' if r['dash_total'] == 0 else 'FAIL', dash_note))
    rows.append(('ASCII 直引号残留', f"{r['ascii_dq']} 个",
                 'PASS' if r['ascii_dq'] == 0 else 'FAIL', '标点须全角，跑 format_chapter.py'))
    sq_v = 'PASS' if r['ascii_sq'] == 0 else 'WARN'
    rows.append(('ASCII 单引号残留', f"{r['ascii_sq']} 个", sq_v, '脚本不自动改，需逐处确认'))
    # ---- v1.26.0：正文内含 ASCII 字母/数字（同日回跑后拆成两条）----
    al_note = ('拉丁字母 = FAIL —— 中文正文里混进英文单词/字母，对读者是明显出戏，无正当理由。'
               '一律改为中文写法；若确为英文专名，须在章节备注写明理由')
    if r['ascii_letter']:
        _hl = '；'.join(f"第{i}行「…{t}…」" for i, t in r['ascii_letter_hits'][:3])
        al_note = f"{_hl} → " + al_note
    rows.append(('正文内含拉丁字母', f"{r['ascii_letter']} 处",
                 'PASS' if r['ascii_letter'] == 0 else 'FAIL', al_note))
    ad_note = ('半角数字 = WARN —— 型号/年代/编号（如「上海牌 7120」）在中文网文里是正常写法，'
               '属风格选择不属错误；建议改全角或中文数字，改了更好、不改不判错')
    if r['ascii_digit']:
        _hdg = '；'.join(f"第{i}行「…{t}…」" for i, t in r['ascii_digit_hits'][:3])
        ad_note = f"{_hdg} → " + ad_note
    rows.append(('正文内含半角数字', f"{r['ascii_digit']} 处",
                 'PASS' if r['ascii_digit'] == 0 else 'WARN', ad_note))
    # ---- v1.20.0：全部风格项改「参考值」，不判定 ----
    # 依据：用户交付的 7 本异风格长篇 + 认可的《第365天》实测区间为
    #   对白占比 0–94%／均段长 12–149／均句长 11–95／短句率 0–45%／碎句链 0–15／短对白链 0–15，
    #   而《停摆》逐项落在包络内 → 统计不可分：这些是风格旋钮，不是质量刻度。
    # 用户原话：「也有那种专门写对话文的，不能一刀全割掉，这种不同的方式都可以有的」。
    rows.append(('平均句长（参考值）', f"{r['avg_sent']:.1f} 字", 'INFO',
                 '正例区间 11–95 字（《月光盒子》13.8／《昨日书》26／《宠宠欲动》38）。不判定'))
    ap = (r['total'] / r['paras']) if r['paras'] else 0
    rows.append(('均段长（参考值）', f"{ap:.1f} 字/段（{r['paras']} 段）", 'INFO',
                 '正例区间 12–149（《月光盒子》15.8／《第365天》30.2）。'
                 '不判定——v1.19.0 的「<16 FAIL」已撤销（会误杀用户交付的正例）'))
    sr = r['short_ratio']
    rows.append(('短句率（≤6 字句，参考值）', f"{sr * 100:.1f}%（{r['n_sent']} 句）", 'INFO',
                 '正例区间 0–45%（《月光盒子》31.4%）。不判定——v1.19.0 的 25% 线已撤销'))
    srun = r['short_run']
    rows.append(('最长连续碎句链（参考值）', f"{srun} 句", 'INFO',
                 '正例最高 15（《月光盒子》第 21 章，与《停摆》第 3 章同值）。'
                 '不判定——连发短句是节奏，是否成问题看承接测试四问'))
    if r.get('frag_span_txt'):
        rows.append(('　└ 该链原文（取此段做承接测试第 1／2 问）', f"{len(r['frag_span_txt'])} 句", 'INFO',
                     ' ／ '.join(x[:18] for x in r['frag_span_txt'][:8])
                     + (' …' if len(r['frag_span_txt']) > 8 else '')
                     + '　→ 问：这串短句拼得出"他在干什么、为什么这样干"吗？'))
    rows.append(('「跳」的判据（四问自检 · 执行者＝模型）', '见文档', 'INFO',
                 '**正则检测已试并撤除**（正例 2.4 句/千字 vs 自产 2.4，无区分度）——**但判定不必由人做**：'
                 '按 references/prose-rules-supplement.md S7.2 由模型逐段四问。判据动作只有一条：'
                 '**挑一段动作密集处，照着做一遍——中间步骤在不在？**'
                 '用户 2026-09-23 原例：「我躺在床上睁开了眼睛，打湿毛巾把脸好好地擦了一下，终于清醒过来了」'
                 '——躺着到打湿毛巾之间，缺了起身、下床、取毛巾、走到水边。**根子在写前：S7.1 动作链。**'))
    rows.append(('句长标准差（参考值）', f"{r['sent_sd']:.1f}", 'INFO', '风格画像用，不判定'))
    sdr = r['short_dlg_run']
    note = ('正例最高 15 行（《月光盒子》）／12 行（《宠宠欲动》第 137 章）——不判定。'
            '判据改走承接测试第 1 问：连续短对白中每行是否让局面动一格')
    if sdr >= 3:
        note = '最长链：' + ' ／ '.join(x.strip() for x in r['short_dlg_lines'][:3])[:56] + ' … → ' + note
    rows.append(('最长连续短对白链（参考值）', f"{sdr} 行", 'INFO', note))
    echo_runs = r['echo_lines']
    echo_max = max(echo_runs) if echo_runs else 0
    rows.append(('无信息应答连招（参考值）',
                 f"最长 {echo_max} 行 / 共 {len(echo_runs)} 段（累计 {sum(echo_runs)} 行）", 'INFO',
                 '“够。”“在。”“没有。”单发不算错；连发是否成问题，用承接测试第 1 问逐行举证'))

    # ---- v1.20.0：通用硬伤层（**唯一保留的门禁**）----
    # 用户 2026-09-23：「病句，碎句，跳，上下句描述错误，这种问题是通用不能有的」。
    # 本层只收「确定性语言错误」；承接测试四问（新信息/接得上/指得清/对得上）由模型自检子流程逐段判（S7.2），非人工、非用户。
    def _loc(pairs, n=3):
        return '；'.join(f"第{i}行「{t[:22]}」" for i, t in pairs[:n])

    hm = r['punct_mismatch']
    rows.append(('标点错配（？。 。！ ，。 等）', f"{len(hm)} 处",
                 'PASS' if not hm else 'FAIL',
                 (_loc(hm) if hm else '通用硬伤')))
    hr = r['punct_repeat']
    rows.append(('标点连用（。。 ！！ ？？）', f"{len(hr)} 处",
                 'PASS' if not hr else 'WARN', (_loc(hr) if hr else '通用硬伤')))
    hq = r['quote_unbalanced']
    rows.append(('引号不配对（单行 “≠” ）', f"{len(hq)} 行",
                 'PASS' if not hq else 'FAIL', (_loc(hq) if hq else '通用硬伤')))
    hd = r['adjacent_dup']
    rows.append(('相邻行完全重复', f"{len(hd)} 处",
                 'PASS' if not hd else 'FAIL', (_loc(hd) if hd else '通用硬伤')))
    hc = r['dup_char']
    rows.append(('叠字错误（她她/的的…）', f"{len(hc)} 处",
                 'PASS' if not hc else 'FAIL', (_loc(hc) if hc else '通用硬伤')))
    hs = r['half_sent']
    rows.append(('半截句（逗号/顿号收尾）', f"{len(hs)} 处",
                 'PASS' if not hs else 'WARN',
                 (_loc(hs) + ' → 须确认是否为刻意排版（文书/引文）；非刻意即「碎句」硬伤') if hs
                 else '通用硬伤（v1.20.0 新增）'))
    he = r['no_end_punct']
    rows.append(('行尾无终止标点', f"{len(he)} 处",
                 'PASS' if not he else 'WARN',
                 (_loc(he) + ' → 须逐处确认') if he else '通用硬伤（v1.20.0 新增）'))


    if r['blind_spans']:
        spans = '、'.join(f"第{a + 1}行起×{b}" for a, b in r['blind_spans'][:6])
        more = f"（共 {len(r['blind_spans'])} 段）" if len(r['blind_spans']) > 6 else ''
        rows.append(('遮蔽测试待办段', f"{len(r['blind_spans'])} 段{more}",
                     'WARN',
                     "以下位置有连续 ≥3 行纯对白，须做 S3.2 遮蔽测试（遮住引号行，看剩下的叙述"
                     "能否让读者知道『在哪、谁在场、围绕什么物件、局面变了什么』）：" + spans))
    return rows


def report(raws, files):
    print('\n' + '=' * 68)
    print('番茄章节过审自检 · 客观指标报告（仅统计正文）')
    print('  v1.20.0：风格项（对白占比/均段长/均句长/短句率/碎句链/短对白链）只报数不判定；')
    print('          门禁只剩「通用硬伤层」＋原有的格式/字数/AI 词项。')
    print('  v1.22.0：「碎／跳」的判定走 S7 闭环——写前动作链＋信息增量表（S7.1）→ 写后模型四问自检（S7.2）。')
    print('          本报告只提供「定位材料」；凡「确认／四问」类动作，执行者＝跑本技能的模型，不是用户。')
    print('=' * 68)
    fails = 0
    for path, r in zip(files, raws):
        print(f"\n【{Path(path).name}】")
        _src = r.get('body_src')
        if _src == 'txt-cut':
            print('  [--]  正文提取: 无 `## 正文` 节 → 按纯 txt 处理，已按「第X章」切分'
                  '只取第 1 章（v1.22.1）。若你实际想测的是另一章，请先拆成单章文件。')
        elif _src == 'txt-whole':
            print('  [--]  正文提取: 无 `## 正文` 节、也未找到章节标题 → 全篇当正文统计，'
                  '口径可能与实际不符，结论仅供参考。')
        for name, val, v, note in verdict(r):
            mark = {'PASS': '[OK]  ', 'WARN': '[!]   ', 'FAIL': '[X]   ', 'INFO': '[--]  '}[v]
            print(f"  {mark}{name}: {val}")
            if v != 'PASS' and note:
                print(f"          → {note if len(note) <= 120 else note[:120] + '…'}")
            if v == 'FAIL':
                fails += 1
    # 跨章对白逐字复现（v1.20.0 新增）——《停摆》第 2/3 章末三句曾完全复现
    for a, b in zip(raws, raws[1:]):
        common = [x for x in a['tail_dlg'] if x in set(b['tail_dlg'])]
        if len(common) >= 3:
            print(f"\n【跨章检测】{Path(a['file']).name} 与 {Path(b['file']).name} "
                  f"末尾对白有 {len(common)} 行逐字复现")
            for c in common[:5]:
                print(f"  [X]   「{c}」")
            print('          → 通用硬伤：相邻两章以同一组对白收尾，读者会觉得"又是这一场"。须改其一')
            fails += 1
    print('\n' + '-' * 68)
    if fails:
        print(f"结论: 有 {fails} 项不通过 —— 先修后交（audit-checklist.md 第六组）")
    else:
        print('结论: 门禁全部通过')
    print('-' * 68)
    return fails


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'):
        print('''用法:
  python chapter_stats.py <章节文件>      # 扫单个章节
  python chapter_stats.py --all <目录>    # 扫目录下所有「第*章.md」

判据（v1.20.0 收窄为「确定性错误」）:
  FAIL —— 破折号 / ASCII 直引号 / 标点错配 / 引号不配对 / 相邻行重复 /
          叠字 / 跨章对白逐字复现 / 正文含拉丁字母
  WARN —— 半角数字 / 标点连用 / 半截句 / 行尾无终止标点
  只报数不判定（风格项，不判 PASS/FAIL）:
          对白行占比 / 均段长 / 均句长 / 短句率 / 碎句链 / 短对白链
  须人工核（脚本只定位）:
          S3.2 遮蔽测试待办段 / 承接测试四问（逐句举证，禁止打勾）

退出码: 0 = 无 FAIL；1 = 有 FAIL 或调用错误。''')
        return 0 if len(sys.argv) > 1 else 1
    if len(sys.argv) < 2:
        print('用法: python chapter_stats.py <章节文件>')
        print('      python chapter_stats.py --all <目录>')
        return 0

    if sys.argv[1] == '--all':
        if len(sys.argv) < 3:
            print('错误: --all 需要目录路径')
            return 1
        d = Path(sys.argv[2])
        if not d.exists():
            print(f'目录不存在: {d}')
            return 1
        # v1.18.0 修：原 glob 为 `第*.md`，会把 `第01章_开篇三版样片.md`
        # 这类设计素材一并当章节扫（实测误报 5 项 P0）。收紧为必须以「章.md」结尾。
        files = sorted(str(p) for p in d.glob('第*章.md'))
    else:
        files = [sys.argv[1]]

    if not files:
        print('没有找到章节文件')
        return 1

    raws = [analyze(Path(f)) for f in files]
    return 1 if report(raws, files) else 0


if __name__ == '__main__':
    sys.exit(main())
