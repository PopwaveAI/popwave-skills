# -*- coding: utf-8 -*-
"""信息槽形态探针（I 组）：指标表 ＋ 对照阅读页（并入 H2 散文基线）。"""

import html
import re
import statistics
from pathlib import Path

BASE = Path(__file__).resolve().parent
OUT = BASE / "输出" / "信息槽形态探针"
H_OUT = BASE / "输出" / "两槽位探针"
DEST_MD = OUT / "信息槽形态探针-机器指标.md"
DEST_HTML = BASE / "信息槽形态探针-对照阅读.html"

PREMISE = ("一个人回到十年前的旧居。房子早已空了，房东换过三任。"
           "他在二楼朝北的屋子里找到一只铁盒，里面是当年没寄出的信。"
           "当晚他决定住下，把信一封封重读。")

ROW_DEFS = [
    ("I0", "散文式信息槽（上轮 H2 基线）", H_OUT / "D2__clean.txt", "9/9", True),
    ("I1", "设计文档＋声明", OUT / "I1__clean.txt", "8/9", True),
    ("I2", "设计文档，无声明", OUT / "I2__clean.txt", "9/9", True),
    ("I3", "极简关键词式＋声明", OUT / "I3__clean.txt", "6/9", True),
]

INFO_SLOTS = {
    "I0": "（散文式）这一章要写到：主角姓赵……前六封都只是寻常叮嘱，第七封没有封口，"
          "里面只有半张地图……这一章停在主角把半张地图摊在桌上，又听见院门外有脚步声。"
          "先不要交代来人是谁，也不要解释那半张地图指向哪里。",
    "I1": "以下是本章的内容设计文档，不是正文。不要模仿本文档的格式与句式。\n\n"
          "【人物】主角：姓赵，三十余岁，十年前离开本城；师父：已故三年，院子原主\n"
          "【场景】旧居院子，二楼朝北的屋子\n"
          "【道具】铁盒：内装七封信，收件人均为主角，笔迹为师父\n"
          "【事件链】1 回到旧居 2 翻出铁盒与七封信 3 前六封是寻常叮嘱 "
          "4 第七封未封口，只有半张地图 5 当晚有人敲门，自称师父旧识，说这院子他不能住\n"
          "【落点】停在主角把半张地图摊在桌上，又听见院门外有脚步声\n"
          "【禁令】不交代来人是谁；不解释地图指向哪里",
    "I2": "（同上，但删掉第一句声明）\n\n"
          "【人物】主角：姓赵，三十余岁，十年前离开本城；师父：已故三年，院子原主\n"
          "【场景】旧居院子，二楼朝北的屋子\n"
          "【道具】铁盒：内装七封信，收件人均为主角，笔迹为师父\n"
          "【事件链】1 回到旧居 2 翻出铁盒与七封信 3 前六封是寻常叮嘱 "
          "4 第七封未封口，只有半张地图 5 当晚有人敲门，自称师父旧识，说这院子他不能住\n"
          "【落点】停在主角把半张地图摊在桌上，又听见院门外有脚步声\n"
          "【禁令】不交代来人是谁；不解释地图指向哪里",
    "I3": "以下是本章的内容设计文档，不是正文。不要模仿本文档的格式与句式。\n\n"
          "人物：赵某(30+)／已故师父(院子原主)\n场景：旧居·二楼朝北屋\n"
          "道具：铁盒＝七封信(收件人均为主角·笔迹为师父)\n"
          "事件：归宅→翻出铁盒→读信(前六封寻常叮嘱)→第七封未封口·只有半张地图→"
          "有人敲门(自称师父旧识·说这院子他不能住)\n"
          "落点：地图摊桌上＋院门外脚步声\n禁令：不交代来人身份／不解释地图指向",
}

HAN = re.compile(r"[\u4e00-\u9fff]")
SENT = re.compile(r"[。！？…]+")


def m(p: Path):
    t = p.read_text(encoding="utf-8")
    body = re.sub(r"\s+", "", t)
    han = len(HAN.findall(t))
    paras = [l for l in t.splitlines() if l.strip()]
    sl = [len(HAN.findall(s)) for s in SENT.split(body) if HAN.findall(s)]
    return {"han": han, "paras": len(paras), "avg_para": round(han / max(len(paras), 1), 1),
            "sent_avg": round(statistics.mean(sl), 1) if sl else 0,
            "short_pct": round(sum(1 for x in sl if x < 10) / max(len(sl), 1) * 100, 1)}


rows = [(c, lab, m(p), rate) for c, lab, p, rate, _ in ROW_DEFS]

L = ["# 信息槽形态探针 · 机器指标（I 组）\n",
     "> 同情境、同流派词（武侠）、同七条事实，只改信息槽的载体形态。deepseek-flash，温度 1.0，零 system message。",
     "> I0 复用上一轮 H2 的散文式信息槽稿作基线。\n",
     "| 条件 | 信息槽形态 | 硬事实兑现 | 正文汉字 | 段数 | 平均段长 | 句长均值 | 短句(<10字)占比 |",
     "|:--|:--|:--|--:|--:|--:|--:|--:|"]
for c, lab, mm, rate in rows:
    L.append("| %s | %s | %s | %d | %d | %s | %s | %s%% |" % (
        c, lab, rate, mm["han"], mm["paras"], mm["avg_para"], mm["sent_avg"], mm["short_pct"]))
L.append("")
L.append("## 读法\n")
L.append("1. **控制力：设计文档式确实拉满。** I2（字段式、无声明）拿到 9/9，与散文式基线持平；")
L.append("   且它的短句（不足十字）占比 **23.1% 是四稿最低**——句子层并不碎，只是段落切得更多（55 段对 35 段）。")
L.append("   这与上一轮 H3（七个整句条目）的碎法不同：H3 是句子被切碎（短句占比 41.7%），I2 只是分段变密。")
L.append("2. **声明有害。** 加「这是文档不是正文。不要模仿本文档的格式与句式」的两稿，正文都明显变短")
L.append("   （I1 998 字、I3 1089 字，无声明的 I2 是 1925 字），且更易漏事实（I1 漏「有人敲门」，I3 漏三条）。")
L.append("   声明没起到「隔离形态」的作用，反而让模型转入简写。")
L.append("3. **极简关键词式控制力掉档。** I3 压到 186 字的信息槽，只兑现 6/9，漏「十年前」「前六封是叮嘱」「有人敲门」。")
L.append("   压缩信息槽能省输入，但代价是漏事。")
L.append("4. **一次额度事故要记进方法论。** I1 首跑 finish_reason=length、正文只 315 字，")
L.append("   根因是 8000 输出额度被 2 万字思考吃满（思考 20358 字符）；加额度到 32000 后正常。")
L.append("   凡输入里带「不要模仿格式」这类需要权衡的指令，模型思考量会暴涨，额度要给足。")
DEST_MD.write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L))


def paras_html(text):
    parts = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    if len(parts) <= 1:
        parts = [p.strip() for p in text.splitlines() if p.strip()]
    return "\n".join("<p>%s</p>" % html.escape(p) for p in parts)


tbl = ["<table><tr><th>条件</th><th>信息槽形态</th><th class='n'>硬事实兑现</th><th class='n'>正文汉字</th>"
       "<th class='n'>平均段长</th><th class='n'>句长均值</th><th class='n'>短句占比</th></tr>"]
for c, lab, mm, rate in rows:
    tbl.append("<tr><td>%s</td><td>%s</td><td class='n'>%s</td><td class='n'>%d</td>"
               "<td class='n'>%s</td><td class='n'>%s</td><td class='n'>%s%%</td></tr>"
               % (c, lab, rate, mm["han"], mm["avg_para"], mm["sent_avg"], mm["short_pct"]))
tbl.append("</table>")
tbl = "\n".join(tbl)

secs = []
for c, lab, p, rate, _ in ROW_DEFS:
    secs.append("""
<section id="{c}"><h2>{c} · {lab}</h2>
<div class="prompt"><span class="k">信息槽（正文提示词另含固定情境与「写一段武侠小说第一章。」）</span><code>{slot}</code></div>
<article class="prose">{body}</article></section>""".format(
        c=c, lab=html.escape(lab), slot=html.escape(INFO_SLOTS[c]),
        body=paras_html(p.read_text(encoding="utf-8"))))

nav = " · ".join('<a href="#%s">%s</a>' % (r[0], r[0]) for r in ROW_DEFS)
doc = """<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<title>信息槽形态探针 · 对照阅读</title><style>
:root{{--ink:#1b1a18;--dim:#6b6660;--line:#e2ded7;--bg:#faf8f5;--card:#fff;--hi:#8c5a2b}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);
font-family:Georgia,"Songti SC","Source Han Serif SC",SimSun,serif;line-height:1.85}}
header.top{{position:sticky;top:0;z-index:9;background:rgba(250,248,245,.94);backdrop-filter:blur(6px);
border-bottom:1px solid var(--line);padding:12px 24px;display:flex;gap:16px;align-items:baseline;flex-wrap:wrap}}
header.top b{{font-size:15px}}header.top a{{color:var(--hi);text-decoration:none;font-size:13px;
font-family:system-ui,"Microsoft YaHei",sans-serif}}
.wrap{{max-width:940px;margin:0 auto;padding:32px 24px 96px}}h1{{font-size:24px;margin:8px 0 6px}}
.lead{{color:var(--dim);font-size:14px;font-family:system-ui,"Microsoft YaHei",sans-serif;line-height:1.9;margin:0 0 22px}}
.panel{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:18px 20px;margin:0 0 26px}}
.panel h3{{margin:0 0 10px;font-size:14px;font-family:system-ui,"Microsoft YaHei",sans-serif}}
table{{border-collapse:collapse;width:100%;font-size:13px;margin:6px 0 12px;font-family:system-ui,"Microsoft YaHei",sans-serif}}
th,td{{border-bottom:1px solid var(--line);padding:7px 8px;text-align:left}}
th{{color:var(--dim);font-weight:600;background:#f4f1ec}}td.n{{font-variant-numeric:tabular-nums}}
section{{margin:0 0 52px;scroll-margin-top:64px}}h2{{font-size:19px;margin:0 0 14px;padding-bottom:8px;border-bottom:2px solid var(--ink)}}
.prompt{{background:#f2efe9;border-left:3px solid var(--hi);border-radius:0 8px 8px 0;padding:12px 16px;margin:0 0 20px;
font-family:system-ui,"Microsoft YaHei",sans-serif;font-size:13px;color:#4a453f;line-height:1.8}}
.prompt .k{{display:block;color:var(--dim);font-size:12px;margin-bottom:6px}}.prompt code{{white-space:pre-wrap;font-family:inherit}}
.prose p{{margin:0 0 1.05em;text-indent:2em;font-size:16.5px}}.prose p:first-child{{text-indent:0}}
</style></head><body>
<header class="top"><b>信息槽形态探针 · 对照阅读</b><span>{nav}</span></header>
<div class="wrap"><h1>信息槽写成设计文档，质感守不守得住</h1>
<p class="lead">同情境、同流派词（武侠）、同七条事实，只改信息槽的载体形态。
I0 是上一轮的散文式基线；I1／I3 带一句「这是文档不是正文」的声明，I2 不带，用来隔离声明这个变量。<br>
请重点判：①I2 的质感是否可接受——它控制力 9/9，短句占比 23.1% 是四稿最低（句子不碎），
但段落切得密（55 段对散文式的 35 段）；②那句「这是文档不是正文」的声明是不是确实有害；
③极简关键词式（I3）漏三条事实，值不值得为压缩付这个代价。</p>
<div class="panel"><h3>机器指标</h3>{tbl}
<p style="font-size:13px;color:var(--dim);font-family:system-ui,'Microsoft YaHei',sans-serif;margin:0">
注：I1 首跑遇上额度事故（思考吃满 8000 额度、正文只 315 字），此页用的是加额度到 32000 后的重跑稿。</p></div>
{secs}</div></body></html>""".format(nav=nav, tbl=tbl, secs="\n".join(secs))

DEST_HTML.write_text(doc, encoding="utf-8")
print("\n阅读页：", DEST_HTML, DEST_HTML.stat().st_size, "字节")
