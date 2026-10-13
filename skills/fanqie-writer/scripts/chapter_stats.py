#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
章节客观指标统计脚本（确定性错误 ＋ 风格画像）（2026-09-21 新增）

用途：把**技能自检清单**里原本只能"靠感觉"判定的 P0 项，
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

import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from word_range import resolve as resolve_range  # noqa: E402

if sys.platform == 'win32':
    import io
    if hasattr(sys.stdout, 'buffer'):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# ── AI 化表达禁用清单 · 唯一真源（v1.29.23 改制）──────────────────────────────
# 改制起因（2026-10-08 全盘体检）：同一份清单在本技能里有四份副本，表长 15 / 35 / 7 / 4，
#   四份交集只有 3 个词；而机检用的恰恰是最短那份——**写得最全的 35 项里 27 项从不进机检**
#   （微微一笑／嘴角勾起／眸光一暗／瞳孔骤缩／心中一凛／五味杂陈……全在文档里躺着）。
# 现统一为：词表只在本 JSON 里存在一份，本脚本与三处 md 一律引用，不再各自维护。
_LEXICON_PATH = Path(__file__).with_name('ai-flavor-lexicon.json')


def load_lexicon(path=None) -> dict:
    """读清单真源。**找不到就报错停下**——不静默回落成空表（空表＝全 PASS，等于门禁消失）。"""
    p = Path(path) if path else _LEXICON_PATH
    if not p.exists():
        raise SystemExit('❌ 找不到 AI 化表达清单真源：%s\n'
                         '   本脚本不再自带词表，必须随包提供该文件。' % p)
    with open(p, encoding='utf-8') as f:
        return json.load(f)


LEXICON = load_lexicon()
AI_WORDS = [x['word'] for x in LEXICON['tier1_words']]
# tier2：裸词匹配会误伤正常用法（"夏"字的最后一横／抄完剩下两页／左上最后一把伞，v1.15.0 实测），
#   故这一档一律走**语境判定**：只有充当连接词（句首或另起一句，且后面紧跟逗号/顿号）才算 AI 腔。
AI_WORDS_CTX = {x['word']: x['regex'] for x in LEXICON['tier2_context']}
# tier3：句式模板（判 FAIL）
AI_PATTERNS = [(x['id'], x['name'], x['regex']) for x in LEXICON['tier3_patterns']]
# tier3_advisory：句式但会误伤正例，只判 WARN（如"认知直述"——有物象承载就是合格的）
AI_ADVISORY = [(x['id'], x['name'], x['regex']) for x in LEXICON['tier3_advisory']]
# 比喻：只画像不判定（比喻本身不是病，无效比喻和堆砌才是；样本不足以定阈值）
FIG_MARKERS = LEXICON['figurative']['markers']

# reaction_cliches：生理反应套话（密度判据，v1.29.24 新增——词表见 ai-flavor-lexicon.json 同名节）
REACTION_PATTERNS = LEXICON.get('reaction_cliches', {}).get('patterns', [])
RC_WINDOW = LEXICON.get('reaction_cliches', {}).get('window_chars', 800)
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
    # 影响实测：某悬疑样本三章各只有 1 个伪句，碎句链 7/7/15 **完全不变**，短句率变化 <0.5%（35.3→35.0）。
    # 故历史结论不受影响；此处按正确口径修正，避免其他文本上出现偏差。
    sents = [s for s in re.split(r'[。？！]', body) if cn_count(s) > 0]
    avg_sent = total / len(sents) if sents else 0
    para_lens = [cn_count(p) for p in lines]
    # --- v1.29.35：叙述段／对白段分开算 ---
    # 为什么：均段长把两种段混在一起算，**对白段天生短（「嗯。」＝2 字）会把它拉低**，
    # 于是"叙述被拆成一句一段"这种病**在均段长上看不出来**。
    # 实测（同一本书、同一个门禁全过的三版稿，**本脚本口径**：含全角引号的行＝对白行）：
    #   全章均段长   叙述段均长   对白段均长
    #   第 1 章        14.9        18.8         9.8
    #   第 2 章旧稿     9.3        10.2         6.5   ← 叙述段腰斩，读者判「全是短句子」
    #   第 2 章重写    17.6        21.6        10.4
    #   → **重点：叙述段 18.8 → 10.2 是病；对白段 9.8 → 6.5 → 10.4 一直在 10 上下，本来就这样。**
    #   **均段长把两段混算，会被天生短的对白段拉低 → 叙述碎在均段长上看不出来。这一格才看得到。**
    _nar_lens = [cn_count(l) for l in lines if not any(q in l for q in FULL_QUOTES)]
    _dia_lens = [cn_count(l) for l in lines if any(q in l for q in FULL_QUOTES)]
    nar_paras, dia_paras = len(_nar_lens), len(_dia_lens)
    nar_avg = (sum(_nar_lens) / nar_paras) if nar_paras else 0
    dia_avg = (sum(_dia_lens) / dia_paras) if dia_paras else 0
    same_run = 0
    for i in range(len(para_lens) - 2):
        if para_lens[i] == para_lens[i + 1] == para_lens[i + 2] and para_lens[i] > 0:
            same_run += 1
    longest = max(para_lens) if para_lens else 0

    # AI 词与标点
    ai_hits = [w for w in AI_WORDS if w in body]
    ai_hits += [w for w, pat in AI_WORDS_CTX.items() if re.search(pat, body)]

    # v1.29.23 新增（清单真源 tier3 / tier3_advisory / figurative）：
    def _ctx(text, m, pad=16):
        a = max(0, m.start() - pad)
        e = min(len(text), m.end() + pad)
        return text[a:e].replace('\n', '')

    ai_pat_hits = []       # 句式模板（判 FAIL）：(模板名, 命中片段, 上下文)
    for _pid, _pname, _prx in AI_PATTERNS:
        for _m in re.finditer(_prx, body):
            ai_pat_hits.append((_pname, _m.group(0)[:26], _ctx(body, _m)))
    advisory_hits = []     # 认知直述等（判 WARN）：(项名, 命中片段, 上下文)
    for _pid, _pname, _prx in AI_ADVISORY:
        for _m in re.finditer(_prx, body):
            advisory_hits.append((_pname, _m.group(0)[:26], _ctx(body, _m)))

    # 比喻画像（只报数、不判定——比喻本身不是病）
    fig_marker_count = {}
    fig_total = 0
    for _w in FIG_MARKERS:
        _c = len(re.findall(_w, body))
        if _c:
            fig_marker_count[_w] = _c
            fig_total += _c
    fig_para_over = []     # 同一段 ≥2 个比喻引导词（WARN，交承接测试四问）
    for _i, _l in enumerate(lines, 1):
        _c = sum(len(re.findall(_w, _l)) for _w in FIG_MARKERS)
        if _c >= 2:
            fig_para_over.append((_i, _c, _l.strip()[:60]))
    fig_per_w = (fig_total / (total / 10000)) if total else 0

    ascii_dq = body.count('"')
    ascii_sq = body.count("'")
    # v1.26.0 新增：正文混入 ASCII 字母/数字（2026-09-23 古代言情 L1 实测抓到的门禁缺口——
    # 旧版只查 ASCII 引号，正文里混进拉丁字母/半角数字完全检不出）
    # 口径校准（2026-09-23 同日回跑后拆分，依据「门禁不得误伤正例」）：
    #   · **拉丁字母** = FAIL —— 中文正文里混进英文单词/字母，对读者是明显出戏，无正当理由
    #   · **半角数字** = WARN —— 型号/年代/编号（如「上海牌 7120」）在中文网文里是正常写法，
    #     回跑该悬疑样本第 1 章时确认：若一并判 FAIL，会误杀已被门禁认可的正例
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
    #   旧版取行首 26 字——破折号在句中时（如某样本第 1 章「…青苔——那是…」）
    #   提示里根本看不到破折号，等于没定位。回跑实测暴露，见 prd/全类型覆盖测试矩阵.md M7 回跑记录。
    dash_hits = []
    for _i, _l in enumerate(lines, 1):
        for _m in re.finditer(r'——|—|–', _l):
            _s = max(0, _m.start() - 10)
            _e = min(len(_l), _m.end() + 10)
            dash_hits.append((_i, _l[_s:_e].strip()))

    # ---- v2.2.0 新增：正文内「」括号（S6.4③）----
    # 背景：2026-10-09 用户质疑「为什么会出现这个符号」。复核发现基准样本（短章文艺向）
    #   用「」包人名（17 处全部是人名、无一处做引号用途），而
    #   references/prose-rules-supplement.md S6.4③ 早已写明：
    #   「样本中有书用「」括人名／对白 → 来源排版格式，**输出统一用 “”**」。
    #   规则在、机器不检 → 续写时把它当成了"该书独特排版"照抄，还写进视角锚。
    #   故把 S6.4③ 从"文档里的一句话"变成"会报警的机制"（缺维病：不在检查面上的那一维）。
    lq_hits = [(i, l.strip()[:30]) for i, l in enumerate(lines, 1) if '「' in l or '」' in l]
    lq_total = len(lq_hits)

    # ---- v2.3.0 新增：生理反应套话堆叠（reaction_cliches 密度判据）----
    # 背景：2026-10-09 用户在接续稿上红框「脚步猛地顿住／心脏莫名漏跳了半拍／呼吸凝滞了」
    #   三句——全部出自基准样本（短章文艺向）第 1 章。此前机器不检、前文体检清单也没这一类，
    #   套话被原样保留进交付章。取证：这 5 类套话在 8 本真人书（约 800 万字）里密度
    #   0~0.1 次/万字、且从不堆叠；该书却在 176 字内堆了 2 个（约 60 倍差距）。
    #   判据：单章内两处命中相距 <800 字＝堆叠（FAIL）；孤立 1 处＝WARN；0 处＝PASS。
    #   校准：1776 章分章回跑＝真人书 0 误伤，唯一 FAIL 正是用户红框章。
    rc_hits = []                   # (body 内位置, 套话名, 上下文)
    for _rc in REACTION_PATTERNS:
        for _m in re.finditer(_rc['regex'], body):
            rc_hits.append((_m.start(), _rc['name'], _ctx(body, _m)))
    rc_hits.sort(key=lambda x: x[0])
    rc_stacks = [(rc_hits[i], rc_hits[i + 1]) for i in range(len(rc_hits) - 1)
                 if rc_hits[i + 1][0] - rc_hits[i][0] < RC_WINDOW]
    rc_total = len(rc_hits)

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
    #         悬疑样本三章同为 2.4 句/千字；且正例候选句形态相同却完全成立
    #         （如「他把目镜推上额头，指腹压住表蒙，往下按了半分」本身是完整动作链）。
    #    → 按本项目纪律「抓不住的就不设门槛，宁可不加也不要加噪声」**撤除**（正则检测器）。
    #    → 「跳」的判定改由**四问自检子流程**执行：判据动作＝「**把这段照着做一遍，中间步骤在不在**」
    #      （用户 2026-09-23 定义），执行者＝跑本技能的模型（references/prose-rules-supplement.md S7.2）。
    #      **不要再造第三个正则检测器**——形态确实不可分；要加的是"生成端约束"（S7.1 动作链），不是又一个正则。

    # ---- v1.20.0 新增：通用硬伤层（唯一保留的门禁；其余风格项一律只报数）----
    # 依据：用户 2026-09-23「病句，碎句，跳，上下句描述错误，这种问题是通用不能有的」
    #       ＋ 8 本异风格正例全量扫描——除本层外，一切节奏/粒度指标都能在正例里找到更极端的反例
    #       （《月光盒子》碎句链 15、短对白链 15，与悬疑样本第 3 章同值）。
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
        'ai_pat_hits': ai_pat_hits,
        'advisory_hits': advisory_hits,
        'fig_total': fig_total,
        'fig_marker_count': fig_marker_count,
        'fig_para_over': fig_para_over,
        'fig_per_w': fig_per_w,
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
        'lq_total': lq_total,
        'lq_hits': lq_hits,
        # --- v2.3.0 反应套话 ---
        'rc_total': rc_total,
        'rc_hits': rc_hits,
        'rc_stacks': rc_stacks,
        'body_src': body_src,
        'paras': len(para_lens),
        # --- v1.29.35：叙述段／对白段分开 ---
        'nar_paras': nar_paras,
        'nar_avg': nar_avg,
        'dia_paras': dia_paras,
        'dia_avg': dia_avg,
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


def verdict(r: dict, rng: dict = None) -> list:
    """返回 (项目, 值, 判定, 说明) 列表；判定取 PASS / WARN / FAIL

    字数区间由 scripts/word_range.py 解析（命令行 ＞ 本书 .learnings/立项参数.json
    ＞ 分档表 ＞ 内置默认），**不再硬编码 2200-2800**。v1.29.17 修——v1.29.16 只让
    check_chapter_wordcount.py 与 plan_word_quota.py 走了解析入口，**本脚本漏网**
    （若立项按悬疑定 3000 字，本脚本会把达标的章误判 FAIL）。

    v1.29.30 再补一维：**「字数区间来源」单独成行放在最前**——区间没落到本书口径时，
    下面那条字数判定按定义不作数；只做末尾脚注＝不在检查面上（缺维病）。
    """
    if rng is None:
        rng = {'min': 2200, 'max': 2800, 'label': '⚠️ 内置默认（未接区间解析）'}
    rows = []
    # ── v1.29.30：**先报「区间来源」，再报「正文字数判定」** ──────────────
    # 为什么必须放在第一行：区间来源未确定时，下面那条字数判定**按定义就不作数**
    #（不是"可能不准"，是"没有可比对象"）。2026-10-09 全量回跑实测：7 本存量样本没有
    # `.learnings/立项参数.json`，一律按内置默认 2200-2800 判的；其中 3 本按今天的
    # 题材档回算**结论会翻**（武侠仙侠／玄幻修真 各 1 章、悬疑推理 3 章被判"短"）。
    # 判 WARN 而不判 FAIL：接续已有项目时用户手上的项目可能本来就没有这个文件，硬拦住＝误伤；
    # 但**必须出现在判定表里**——只做末尾脚注等于"不在检查面上"（缺维病）。
    _und = str(rng.get('label', '')).startswith('⚠️')
    rows.append(('字数区间来源',
                 ('未确定' if _und else '已确定'),
                 'WARN' if _und else 'PASS',
                 (('⚠️ 下面「正文字数」那条判定**不作数**——没有已知区间可比。两处按顺序查：'
                   '① **命令没指到本书目录**（查找起点＝命令行 `--min/--max` ＞ 章节文件 ＞ '
                   '**当前目录**，逐级向上找；v1.29.30 修的就是这一半）；'
                   '② **本书确实没落盘** `.learnings/立项参数.json`'
                   '（接续已有项目时常见——按已有正文口径补落盘，工具 `scripts/set_word_range.py`）。')
                  if _und else
                  ('区间 %s-%s｜来源: %s' % (rng['min'], rng['max'], rng['label'])))))
    rows.append(('正文字数', f"{r['total']}",
                 'PASS' if rng['min'] <= r['total'] <= rng['max'] else 'FAIL',
                 '区间 %s-%s｜来源: %s' % (rng['min'], rng['max'], rng['label'])))
    # v1.19.0 废除「对话占比 ≥30%」门槛；v1.20.0 进一步把口径统一为「行占比」，
    # 与 references/benchmark-writing.md 第一节的样本画像同尺（旧口径是汉字占比，两者数值不可比）。
    rows.append(('对白行占比（参考值·不判定）',
                 f"{r['dlg_line_ratio'] * 100:.1f}%（{r['dlg_total_lines']}/{r['paras']} 行）", 'INFO',
                 '正例区间 0–94%（基准样本 18.6%／《昨日书》42.5%／《宠宠欲动》53%，单章最高 92%）。'
                 'v1.19.0 已废除旧的「≥30%」门槛：占比高低不指示质量。'
                 '对白是否合格走 ①遮蔽测试（S3.2）②承接测试第 1 问（每行让局面动一格）'))
    rows.append(('AI 高频词', ('、'.join(r['ai_hits']) if r['ai_hits'] else '无'),
                 'FAIL' if r['ai_hits'] else 'PASS',
                 '命中即 FAIL（清单真源 scripts/ai-flavor-lexicon.json 的 tier1，共 %d 词）' % len(AI_WORDS)))
    # v1.29.23 新增：句式模板（FAIL）／认知直述（WARN）／比喻画像（WARN 或 INFO）
    _pat = r.get('ai_pat_hits') or []
    if _pat:
        _pn = '；'.join('%s「%s」→ …%s…' % (n, s, c) for n, s, c in _pat[:3])
        _pat_note = _pn + '   ← 逐处回原文改：把模板句式换成具体写法，**不是换同义词**'
    else:
        _pat_note = '未出现 AI 模板句式（不是A而是B／，带着…／他不知道的是…／仿佛…一般）'
    rows.append(('AI 句式模板', ('%d 处' % len(_pat)) if _pat else '无',
                 'FAIL' if _pat else 'PASS', _pat_note))
    _adv = r.get('advisory_hits') or []
    if _adv:
        _an = '；'.join('%s「%s」→ …%s…' % (n, s, c) for n, s, c in _adv[:3])
        _adv_note = _an + '   ← 提示项：看命中处**有没有具体物象承载**。有＝保留，没有＝补一个（**不是一律删**）'
    else:
        _adv_note = '未出现认知直述句式'
    rows.append(('认知直述（提示项）', ('%d 处' % len(_adv)) if _adv else '无',
                 'WARN' if _adv else 'PASS', _adv_note))
    _fo = r.get('fig_para_over') or []
    _fig_head = ('；'.join('第%d行 %d个「%s」' % (i, c, t) for i, c, t in _fo[:3]) + '  →  ') if _fo else ''
    _fig_note = (_fig_head + '密度 %.1f 处/万字（%s）——**只画像不判定**：比喻本身不是病，'
                 '无效比喻与堆砌才是病；本仓样本量不足以定阈值'
                 % (r.get('fig_per_w', 0),
                    '、'.join('%s×%d' % (k, v) for k, v in
                              sorted((r.get('fig_marker_count') or {}).items(), key=lambda x: -x[1])[:5]) or '无'))
    # v1.29.23 校准：本项**恒为 INFO，不判 WARN**。
    #   原设计「同一段 ≥2 个比喻引导词 → WARN」，回跑存量后**当场误伤全仓最好的两段**：
    #     一部武侠样本 3 处「像」并列、一部现实题材样本 4 处层层递进的比喻（详见真源 figurative.gates）
    #   病在「堆砌」不在「数量」——正则分不出「密集且递进」与「密集且空洞」，
    #   而这两处的差别正是承接测试四问的活。按门禁校准通则「无区分度／误伤即拆级」，降为只列位置。
    rows.append(('比喻画像', '%.1f 处/万字' % r.get('fig_per_w', 0),
                 'INFO', _fig_note))
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
    # ---- v2.2.0：正文内「」（S6.4③ 机器化）----
    lq_note = ('正文内「」= WARN —— 样本里的「」是**来源排版格式**（有样本用它包人名／对白），'
               '**输出统一用 “”**（prose-rules-supplement.md S6.4③）。'
               '规划文档用「」引术语不受限；本项只扫 `## 正文` 节')
    if r.get('lq_total'):
        _hlq = '；'.join(f"第{i}行「…{t}…」" for i, t in r['lq_hits'][:3])
        lq_note = f"{_hlq} → " + lq_note
    rows.append(('正文内「」（含包人名）', f"{r.get('lq_total', 0)} 处",
                 'PASS' if not r.get('lq_total') else 'WARN', lq_note))

    # ---- v2.3.0：生理反应套话堆叠（reaction_cliches 密度判据）----
    _rcstack = r.get('rc_stacks', [])
    if _rcstack:
        _rcdet = '；'.join(f"{a[1]}＋{b[1]}（相距 {b[0] - a[0]} 字）" for a, b in _rcstack[:2])
        _rcnote = (f"反应堆叠：{_rcdet}。{RC_WINDOW} 字内两处生理套话＝拿模板当反应的全部，读者会认出来。"
                   "删掉套话，用「动作停在哪／行为延迟了什么／看见哪个具体物件」承载"
                   "（真人正例摘句：references/reaction-beats.md）")
        _rcv = 'FAIL'
    elif r.get('rc_total'):
        _rcnote = ('单章出现生理反应套话 1 处（真人书也用但密度极低、从不堆叠）——'
                   '承接测试问一句：它承载了不可替代的信息吗？能换成具体动作就换')
        _rcv = 'WARN'
    else:
        _rcnote = '生理反应套话 0 处（词表：ai-flavor-lexicon.json reaction_cliches 节）'
        _rcv = 'PASS'
    rows.append(('生理反应套话堆叠',
                 f"{r.get('rc_total', 0)} 处" + (f"（堆叠 {len(_rcstack)} 对）" if _rcstack else ''),
                 _rcv, _rcnote))
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
    # 依据：用户交付的 7 本异风格长篇 + 认可的基准样本实测区间为
    #   对白占比 0–94%／均段长 12–149／均句长 11–95／短句率 0–45%／碎句链 0–15／短对白链 0–15，
    #   而悬疑样本逐项落在包络内 → 统计不可分：这些是风格旋钮，不是质量刻度。
    # 用户原话：「也有那种专门写对话文的，不能一刀全割掉，这种不同的方式都可以有的」。
    rows.append(('平均句长（参考值）', f"{r['avg_sent']:.1f} 字", 'INFO',
                 '正例区间 11–95 字（《月光盒子》13.8／《昨日书》26／《宠宠欲动》38）。不判定'))
    ap = (r['total'] / r['paras']) if r['paras'] else 0
    rows.append(('均段长（参考值）', f"{ap:.1f} 字/段（{r['paras']} 段）", 'INFO',
                 '正例区间 12–149（《月光盒子》15.8／基准样本 30.2）。'
                 '不判定——v1.19.0 的「<16 FAIL」已撤销（会误杀用户交付的正例）'))
    # v1.29.35：把均段长拆开成叙述段／对白段。**这一格才是能定位"叙述被拆成一句一段"的那一格**：
    # 对白段天生短，混算会把均段长拉低，于是"叙述碎"在均段长上看不出来（详见 analyze() 里的实测注）。
    rows.append(('　└ 其中：叙述段／对白段（参考值）',
                 f"叙述 {r['nar_avg']:.1f} 字/段（{r['nar_paras']} 段）｜对白 {r['dia_avg']:.1f} 字/段（{r['dia_paras']} 段）",
                 'INFO',
                 '**分开看才是判据**：叙述段均长掉到 15 以下 ＝ 叙述被拆成了碎片（对白段短是正常的）。'
                 '实测同一本书三版：第 1 章 叙述 18.8／对白 9.8｜第 2 章**旧稿** 叙述 10.2／对白 6.5｜'
                 '第 2 章重写 叙述 21.6／对白 10.4。'
                 '**看出来的差别全在叙述段（18.8 → 10.2 → 21.6），对白段一直在 10 上下。'
                 '病在叙述段，不在对白段。**不判定，只报数'))
    sr = r['short_ratio']
    rows.append(('短句率（≤6 字句，参考值）', f"{sr * 100:.1f}%（{r['n_sent']} 句）", 'INFO',
                 '正例区间 0–45%（《月光盒子》31.4%）。不判定——v1.19.0 的 25% 线已撤销'))
    srun = r['short_run']
    rows.append(('最长连续碎句链（参考值）', f"{srun} 句", 'INFO',
                 '正例最高 15（《月光盒子》第 21 章，与悬疑样本第 3 章同值）。'
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


def report(raws, files, ranges=None):
    print('\n' + '=' * 68)
    print('章节客观指标报告（仅统计正文）')
    print('  v1.20.0：风格项（对白占比/均段长/均句长/短句率/碎句链/短对白链）只报数不判定；')
    print('          门禁只剩「通用硬伤层」＋原有的格式/字数/AI 词项。')
    print('  v1.22.0：「碎／跳」的判定走 S7 闭环——写前动作链＋信息增量表（S7.1）→ 写后模型四问自检（S7.2）。')
    print('          本报告只提供「定位材料」；凡「确认／四问」类动作，执行者＝跑本技能的模型，不是用户。')
    print('=' * 68)
    fails = 0
    if ranges is None:
        ranges = [None] * len(files)
    for path, r, rng in zip(files, raws, ranges):
        print(f"\n【{Path(path).name}】")
        _src = r.get('body_src')
        if _src == 'txt-cut':
            print('  [--]  正文提取: 无 `## 正文` 节 → 按纯 txt 处理，已按「第X章」切分'
                  '只取第 1 章（v1.22.1）。若你实际想测的是另一章，请先拆成单章文件。')
        elif _src == 'txt-whole':
            print('  [--]  正文提取: 无 `## 正文` 节、也未找到章节标题 → 全篇当正文统计，'
                  '口径可能与实际不符，结论仅供参考。')
        for name, val, v, note in verdict(r, rng):
            mark = {'PASS': '[OK]  ', 'WARN': '[!]   ', 'FAIL': '[X]   ', 'INFO': '[--]  '}[v]
            print(f"  {mark}{name}: {val}")
            if v != 'PASS' and note:
                print(f"          → {note if len(note) <= 120 else note[:120] + '…'}")
            if v == 'FAIL':
                fails += 1
    # 跨章对白逐字复现（v1.20.0 新增）——悬疑样本第 2/3 章末三句曾完全复现
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

    degraded = [Path(f).name for f, rng in zip(files, ranges)
                if rng and str(rng.get('label', '')).startswith('⚠️')]
    if degraded:
        print('WARN: 有 %d 章**没解析到本书字数口径**（%s）——判定表首行「字数区间来源」'
              '已标「未确定」，**那几章的字数判定不作数**。' % (len(degraded), '、'.join(degraded[:5])))
        print('   两处按顺序查：① **命令没指到本书目录**（查找起点＝命令行 ＞ 章节文件 ＞ 当前目录）；'
              '② **本书确实没落盘** `.learnings/立项参数.json`（生成方式见 SKILL.md，'
              '工具 `scripts/set_word_range.py`）。')
    return fails


USAGE = '''用法:
  python chapter_stats.py <章节文件>      # 扫单个章节
  python chapter_stats.py --all <目录>    # 扫目录下所有「第*章.md」
  python chapter_stats.py --lexicon       # 打印 AI 化表达禁用清单（与机检同一份真源）

可选参数（一般不用给——脚本会自己找本书立项参数）:
  --min <n> / --max <n>          显式指定区间（优先级最高）
  --genre <题材名>               配合 --range-config 用
  --range-config <json>          分档表（各技能自带的字数分档 json）
  -h / --help                    看这段

区间解析顺序: 命令行 ＞ 本书 .learnings/立项参数.json ＞ 分档表 ＞ 内置默认 2200-2800。
              报告里逐章打印「来源」——降级到默认档会显式告警。

判据（v1.20.0 收窄为「确定性错误」；v1.29.23 补 AI 句式模板与比喻画像；v2.2.0 补正文「」；v2.3.0 补生理反应套话堆叠）:
  FAIL —— AI 高频词 / AI 句式模板（不是A而是B 等）/ 破折号 / ASCII 直引号 / 标点错配 /
          引号不配对 / 相邻行重复 / 叠字 / 跨章对白逐字复现 / 正文含拉丁字母 / 字数落在本书区间外 / 生理反应套话堆叠（800 字内 2 处，v2.3.0）
  WARN —— 认知直述（看有无物象承载）/ 半角数字 / 标点连用 / 半截句 / 行尾无终止标点 / 正文内「」（v2.2.0：样本的排版格式，**输出统一用 “”**，见 S6.4③） / 生理反应套话孤立 1 处（v2.3.0）
  只报数不判定（风格项，不判 PASS/FAIL）:
          **比喻密度与同段密集位置**（比喻本身不是病，无效比喻与堆砌才是；
          实测最密的两处恰是全仓最好的句子，故不设判定）/
          对白行占比 / 均段长 / 均句长 / 短句率 / 碎句链 / 短对白链
  须人工核（脚本只定位）:
          S3.2 遮蔽测试待办段 / 承接测试四问（逐句举证，禁止打勾）

AI 化表达清单真源: scripts/ai-flavor-lexicon.json（本脚本与三处文档共用一份，不再各自维护）。

退出码: 0 = 无 FAIL；1 = 有 FAIL 或调用错误。'''


def print_lexicon() -> int:
    """打印清单真源（供文档与模板引用时取同一份内容，避免复制出第二份词表）。"""
    print('# AI 化表达禁用清单（真源：scripts/ai-flavor-lexicon.json v%s）'
          % LEXICON['_meta']['version'])
    print()
    print('## 第一档 · 命中即 FAIL 的 AI 词（%d 个）' % len(AI_WORDS))
    cur = None
    for x in LEXICON['tier1_words']:
        if x['group'] != cur:
            cur = x['group']
            print()
            print('### %s' % cur)
        print('- `%s` —— %s → %s' % (x['word'], x['why'], x['fix']))
    print()
    print('## 第二档 · 语境判定（仅作连接词时算 AI 腔，%d 个）' % len(AI_WORDS_CTX))
    for x in LEXICON['tier2_context']:
        print('- `%s` —— %s' % (x['word'], x['why']))
    print()
    print('## 第三档 · 句式模板（命中即 FAIL，%d 条）' % len(AI_PATTERNS))
    for x in LEXICON['tier3_patterns']:
        print('- **%s** —— %s' % (x['name'], x['why']))
        print('  改法：%s' % x['fix'])
        if x.get('realfix'):
            print('  %s' % x['realfix'])
    print()
    print('## 第三档附 · 提示项（判 WARN，%d 条）' % len(AI_ADVISORY))
    for x in LEXICON['tier3_advisory']:
        print('- **%s** —— %s' % (x['name'], x['why']))
        print('  %s' % x['why_advisory'])
    _rcsec = LEXICON.get('reaction_cliches')
    if _rcsec:
        print()
        print('## 生理反应套话（密度判据，%d 类）' % len(_rcsec['patterns']))
        print('  判据：%s' % _rcsec['_meta']['gate'])
        for x in _rcsec['patterns']:
            print('  - %-8s %s' % (x['name'], x['regex']))
            if x.get('real_books'):
                print('    真人书出现率：%s' % x['real_books'])
        print('  背景：%s' % _rcsec['_meta']['background'])
        print('  校准：%s' % _rcsec['_meta']['calibration'])
        print('  不进表的（交承接测试）：+%s' % _rcsec['_meta']['why_not_gated'])
        print('  改法：%s' % _rcsec['fix'])
    print()
    print('## 比喻：只画像不判定')
    print('- 引导词：%s' % '、'.join(FIG_MARKERS))
    print('- %s' % LEXICON['figurative']['why'])
    print()
    print('## 编辑须知')
    for n in LEXICON['notes_for_editors']:
        print('- %s' % n)
    return 0


def _take_flag(argv, name):
    '''从 argv 里摘掉 `--name value`，返回 (值, 剩余列表)'''
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
        return 0 if argv else 1

    if argv[0] == '--lexicon':
        return print_lexicon()

    min_words, rest = _take_flag(argv, '--min')
    max_words, rest = _take_flag(rest, '--max')
    range_config, rest = _take_flag(rest, '--range-config')
    genre, rest = _take_flag(rest, '--genre')
    min_words = int(min_words) if min_words else None
    max_words = int(max_words) if max_words else None

    if not rest:
        print(USAGE)
        return 1

    if rest[0] == '--all':
        if len(rest) < 2:
            print('错误: --all 需要目录路径')
            return 1
        d = Path(rest[1])
        if not d.exists():
            print(f'目录不存在: {d}')
            return 1
        # v1.18.0 修：原 glob 为 `第*.md`，会把 `第01章_开篇三版样片.md`
        # 这类设计素材一并当章节扫（实测误报 5 项 P0）。收紧为必须以「章.md」结尾。
        files = sorted(str(p) for p in d.glob('第*章.md'))
    else:
        files = [rest[0]]

    if not files:
        print('没有找到章节文件')
        return 1

    # 逐章解析区间（本书参数与黄金三章递减结构要按章号判，不能整批用同一个数）
    ranges = [resolve_range(min_words=min_words, max_words=max_words,
                            range_config=range_config, genre=genre,
                            chapter_path=f) for f in files]
    raws = [analyze(Path(f)) for f in files]
    return 1 if report(raws, files, ranges) else 0


if __name__ == '__main__':
    sys.exit(main())
