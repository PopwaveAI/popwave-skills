# -*- coding: utf-8 -*-
"""
流派词探针分析：三类特征词交叉命中矩阵 + 形态与通病指标。

判读逻辑：若流派词真激活了内置文体，矩阵应呈对角优势——
C1 只在武侠词表高，C2 只在克苏鲁词表高，C3 只在规则怪谈词表高。
生造词条件 C4 若也自成体系，说明"激活"部分来自听指令即兴编造。
"""

import re
import statistics
from pathlib import Path

BASE = Path(__file__).resolve().parent
OUT = BASE / "输出" / "流派词探针"
REPORT = OUT / "流派词探针-机器指标.md"

LEX = {
    "武侠": r"内力|真气|招式|剑法|刀法|掌法|江湖|门派|师父|师兄|师叔|轻功|内功|心法|恩怨|客栈|帮派|秘籍|运功|点穴|暗器|刀光|剑影|剑气|武功|掌门|弟子|兵刃|身法|气劲|侠客|大侠|武人|练家子",
    "克苏鲁": r"理智|疯狂|不可名状|古神|旧日|触须|触手|深渊|呓语|图腾|邪神|异神|献祭|亵渎|认知|崩坏|低语|蠕动|畸变|凝视|非欧|异形|呢喃|黏液|腐败|不洁净|不可直视|无面",
    "规则怪谈": r"规则|守则|违反|违规|禁止|务必|须知|值班|日志|管理员|通报|异常|条例|按要求|照做|遵守|后果自负|请注意|不要相信|不可回头|切记",
}

# 规则条文形态
RULE_FORM = [
    ("编号条文", r"^第[一二三四五六七八九十百]+条"),
    ("阿拉伯条款", r"^\s*\d+[.、]\s*\S"),
    ("方头括号", r"【[^】]{2,20}】"),
    ("圆括号提示", r"^[（(][^）)]{4,40}[）)]\s*$"),
]

BI_AI = [
    ("比喻词", r"像|仿佛|宛如|如同|似的|犹如"),
    ("身体反应写情绪", r"(胸口|喉咙|心口|胃|后背|脊背|手心|指尖|头皮|呼吸|心跳)[^。！？]{0,12}(一紧|发凉|发紧|发冷|发热|一沉|收紧|发麻|发起|顿住|停了一拍|沉下去|缩紧|发烫|发僵|一抽)"),
    ("不是而是", r"不是[^，。]{2,20}，?而是"),
    ("总结腔", r"他知道|她明白|他意识到|某种|仿佛在诉说|诉说着一|见证了|承载着"),
]

HAN = re.compile(r"[\u4e00-\u9fff]")
SENT_SPLIT = re.compile(r"[。！？…]+")


def sent_lens(text: str):
    body = re.sub(r"\s+", "", text)
    return [len(HAN.findall(s)) for s in SENT_SPLIT.split(body) if len(HAN.findall(s)) >= 1]


rows = []
for p in sorted(OUT.glob("C*__clean.txt")):
    code = p.name.split("__")[0]
    t = p.read_text(encoding="utf-8")
    body = re.sub(r"\s+", "", t)
    han = len(HAN.findall(t))
    paras = [l for l in t.splitlines() if l.strip()]
    sl = sent_lens(t)
    lex = {}
    for name, pat in LEX.items():
        hits = re.findall(pat, body)
        lex[name] = (len(hits), round(len(hits) / max(han, 1) * 10000, 1))  # 每万字
    rf = {}
    for name, pat in RULE_FORM:
        rf[name] = len(re.findall(pat, t, flags=re.M))
    bi = {}
    for name, pat in BI_AI:
        bi[name] = len(re.findall(pat, body))
    rows.append({
        "code": code, "han": han, "paras": len(paras),
        "avg_para": round(han / max(len(paras), 1), 1),
        "sent_avg": round(statistics.mean(sl), 1) if sl else 0,
        "sent_sd": round(statistics.pstdev(sl), 1) if len(sl) > 1 else 0,
        "short_pct": round(sum(1 for x in sl if x < 10) / max(len(sl), 1) * 100, 1),
        "sents": len(sl), "lex": lex, "rule_form": rf, "ai": bi,
        "dash": t.count("\u2014"), "ellipsis": t.count("\u2026"),
        "half_quote": t.count('"'), "md": t.count("**") + len([l for l in t.splitlines() if l.lstrip().startswith("#")]),
    })

L = []
L.append("# 流派词探针 · 机器指标\n")
L.append("> 输入：同一情境、同一句式，只换流派词槽位。每条件 1 稿。deepseek-flash，温度 1.0，零 system message。\n")

L.append("## 一、形态表\n")
L.append("| 条件 | 汉字 | 段数 | 平均段长 | 句数 | 句长均值 | 句长标准差 | 短句(<10字)占比 | 破折号 | 省略号 |")
L.append("|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|")
for r in rows:
    L.append("| %s | %d | %d | %s | %d | %s | %s | %s%% | %d | %d |" % (
        r["code"], r["han"], r["paras"], r["avg_para"], r["sents"], r["sent_avg"],
        r["sent_sd"], r["short_pct"], r["dash"], r["ellipsis"]))

L.append("\n## 二、流派特征词交叉矩阵（每万字命中数，对角线优势＝激活）\n")
L.append("| 条件 | 武侠词表 | 克苏鲁词表 | 规则怪谈词表 |")
L.append("|:--|--:|--:|--:|")
for r in rows:
    L.append("| %s | %s (%d) | %s (%d) | %s (%d) |" % (
        r["code"], r["lex"]["武侠"][1], r["lex"]["武侠"][0],
        r["lex"]["克苏鲁"][1], r["lex"]["克苏鲁"][0],
        r["lex"]["规则怪谈"][1], r["lex"]["规则怪谈"][0]))

L.append("\n## 三、规则条文形态（规则怪谈的体式特征）\n")
L.append("| 条件 | 编号条文 | 阿拉伯条款 | 方头括号 | 圆括号提示 |")
L.append("|:--|--:|--:|--:|--:|")
for r in rows:
    rf = r["rule_form"]
    L.append("| %s | %d | %d | %d | %d |" % (r["code"], rf["编号条文"], rf["阿拉伯条款"], rf["方头括号"], rf["圆括号提示"]))

L.append("\n## 四、AI 通病机器可判项\n")
L.append("| 条件 | 比喻词 | 身体反应写情绪 | 不是而是 | 总结腔 |")
L.append("|:--|--:|--:|--:|--:|")
for r in rows:
    bi = r["ai"]
    L.append("| %s | %d | %d | %d | %d |" % (r["code"], bi["比喻词"], bi["身体反应写情绪"], bi["不是而是"], bi["总结腔"]))

L.append("\n## 五、形态污染\n")
L.append("| 条件 | 半角引号 | markdown 标记 |")
L.append("|:--|--:|--:|")
for r in rows:
    L.append("| %s | %d | %d |" % (r["code"], r["half_quote"], r["md"]))

REPORT.write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L))
print("\n报告：", REPORT)
