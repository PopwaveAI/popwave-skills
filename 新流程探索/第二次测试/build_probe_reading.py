# -*- coding: utf-8 -*-
"""把 5 稿流派词探针产出汇成一页对照阅读页（自包含 HTML）。"""

import html
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent
OUT = BASE / "输出" / "流派词探针"
DEST = BASE / "流派词探针-对照阅读.html"

META = [
    ("C0", "无线索词（对照）", "写一段小说第一章。"),
    ("C1", "武侠", "写一段武侠小说第一章。"),
    ("C2", "克苏鲁恐怖", "写一段克苏鲁小说第一章。"),
    ("C3", "规则怪谈", "写一段规则怪谈小说第一章。"),
    ("C4", "生造流派词：琉璃道（对照）", "写一段“琉璃道”流派小说第一章。"),
]
PREMISE = ("一个人回到十年前的旧居。房子早已空了，房东换过三任。"
           "他在二楼朝北的屋子里找到一只铁盒，里面是当年没寄出的信。"
           "当晚他决定住下，把信一封封重读。")

METRICS_FORM = """| 条件 | 汉字 | 段数 | 平均段长 | 句长均值 | 短句(<10字)占比 | 破折号 | 省略号 |
|:--|--:|--:|--:|--:|--:|--:|--:|
| C0 无线索词 | 2707 | 54 | 50.1 | 18.7 | 29.0% | 22 | 2 |
| C1 武侠 | 1418 | 29 | 48.9 | 20.9 | 22.1% | 12 | 4 |
| C2 克苏鲁 | 1595 | 38 | 42.0 | 13.8 | 54.3% | 5 | 42 |
| C3 规则怪谈 | 2369 | 56 | 42.3 | 20.8 | 22.8% | 16 | 0 |
| C4 生造词 | 1776 | 33 | 53.8 | 20.9 | 21.2% | 18 | 2 |"""

METRICS_LEX = """| 条件 | 武侠词表 | 克苏鲁词表 | 规则怪谈词表 |
|:--|--:|--:|--:|
| C0 无线索词 | 0 | 0 | 0 |
| C1 武侠 | 35.3／万字 (5) 剑法·江湖 | 0 | 0 |
| C2 克苏鲁 | 0 | 12.5／万字 (2) 理智·腐败 | 0 |
| C3 规则怪谈 | 0 | 0 | 12.7／万字 (3) 规则 |
| C4 生造词 | 0 | 0 | 0 |"""


def md_table(md: str) -> str:
    rows = [r for r in md.strip().split("\n") if r.strip()]
    out = ["<table>"]
    for i, r in enumerate(rows):
        cells = [c.strip() for c in r.strip("|").split("|")]
        if i == 1 and set(cells[0]) <= set(":- "):
            continue
        tag = "th" if i == 0 else "td"
        cls = ' class="n"' if i > 0 else ""
        out.append("<tr" + cls + ">" + "".join("<%s>%s</%s>" % (tag, c, tag) for c in cells) + "</tr>")
    out.append("</table>")
    return "\n".join(out)


def paragraphs(text: str) -> str:
    parts = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    if len(parts) <= 1:
        parts = [p.strip() for p in text.splitlines() if p.strip()]
    return "\n".join("<p>%s</p>" % html.escape(p) for p in parts)


nav = " · ".join('<a href="#%s">%s</a>' % (c, c) for c, _, _ in META)
sections = []
for code, label, prefix in META:
    f = OUT / ("%s__clean.txt" % code)
    if not f.exists():
        continue
    body = paragraphs(f.read_text(encoding="utf-8"))
    sections.append("""
<section id="{code}">
  <h2>{code} · {label}</h2>
  <div class="prompt"><span class="k">发出去的提示词</span><code>{prefix}
{premise}</code></div>
  <article class="prose">{body}</article>
</section>""".format(code=code, label=html.escape(label), prefix=html.escape(prefix),
                     premise=html.escape(PREMISE), body=body))

doc = """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<title>流派词激活力探针 · 对照阅读</title>
<style>
  :root{{--ink:#1b1a18;--dim:#6b6660;--line:#e2ded7;--bg:#faf8f5;--card:#fff;--hi:#8c5a2b}}
  *{{box-sizing:border-box}}
  body{{margin:0;background:var(--bg);color:var(--ink);
    font-family:Georgia,"Songti SC","Source Han Serif SC",SimSun,serif;
    line-height:1.85;-webkit-font-smoothing:antialiased}}
  header.top{{position:sticky;top:0;z-index:9;background:rgba(250,248,245,.94);
    backdrop-filter:blur(6px);border-bottom:1px solid var(--line);padding:12px 24px;
    display:flex;gap:16px;align-items:baseline;flex-wrap:wrap}}
  header.top b{{font-size:15px;letter-spacing:.02em}}
  header.top a{{color:var(--hi);text-decoration:none;font-size:13px;
    font-family:system-ui,"Microsoft YaHei",sans-serif}}
  header.top a:hover{{text-decoration:underline}}
  .wrap{{max-width:940px;margin:0 auto;padding:32px 24px 96px}}
  h1{{font-size:24px;margin:8px 0 6px}}
  .lead{{color:var(--dim);font-size:14px;font-family:system-ui,"Microsoft YaHei",sans-serif;
    line-height:1.9;margin:0 0 22px}}
  .panel{{background:var(--card);border:1px solid var(--line);border-radius:10px;
    padding:18px 20px;margin:0 0 26px}}
  .panel h3{{margin:0 0 10px;font-size:14px;
    font-family:system-ui,"Microsoft YaHei",sans-serif}}
  table{{border-collapse:collapse;width:100%;font-size:13px;margin:6px 0 18px;
    font-family:system-ui,"Microsoft YaHei",sans-serif}}
  th,td{{border-bottom:1px solid var(--line);padding:7px 9px;text-align:left}}
  th{{color:var(--dim);font-weight:600;background:#f4f1ec}}
  td.n{{font-variant-numeric:tabular-nums}}
  section{{margin:0 0 52px;scroll-margin-top:64px}}
  h2{{font-size:19px;margin:0 0 14px;padding-bottom:8px;border-bottom:2px solid var(--ink)}}
  .prompt{{background:#f2efe9;border-left:3px solid var(--hi);border-radius:0 8px 8px 0;
    padding:12px 16px;margin:0 0 20px;
    font-family:system-ui,"Microsoft YaHei",sans-serif;font-size:13px;
    color:#4a453f;line-height:1.85}}
  .prompt .k{{display:block;color:var(--dim);font-size:12px;margin-bottom:6px}}
  .prompt code{{white-space:pre-wrap;font-family:inherit}}
  .prose p{{margin:0 0 1.05em;text-indent:2em;font-size:16.5px}}
  .prose p:first-child{{text-indent:0}}
</style></head><body>
<header class="top"><b>流派词激活力探针 · 对照阅读</b><span>{nav}</span></header>
<div class="wrap">
<h1>同一情境，只换一个流派词</h1>
<p class="lead">
固定情境（不含任何流派词）：{premise}<br>
五个条件只改提示词里的流派词槽位，其余一字不动：模型 deepseek-flash，temperature 1.0，
top_p 1.0，零 system message，每条件 1 稿。<br>
判读要点：①真流派词有没有带出该类的文体与专属词汇（看下方矩阵，理想是对角优势）；
②生造词条件 C4 是否也自成体系——若它只是普通文笔、没有专属词汇，说明真流派词确实调动了内置分布；
③克苏鲁条件 C2 的短句与省略号形态是否与其余四稿明显分叉。
</p>

<div class="panel">
<h3>形态指标</h3>
{form}
<h3>流派特征词交叉命中（每万字）</h3>
{lex}
<p style="font-size:13px;color:var(--dim);font-family:system-ui,'Microsoft YaHei',sans-serif;margin:0">
补充：规则条文体式（编号条文／阿拉伯条款／方头括号）在五稿里均为 0——C3 用了「规则」类词汇，
但没有生成「第X条」那种条文版式。AI 通病机器可判项里，「身体反应写情绪」在五稿均为 0，
比喻词 C4 最多（17）。
</p>
</div>
{sections}
</div></body></html>""".format(nav=nav, premise=html.escape(PREMISE),
                                form=md_table(METRICS_FORM),
                                lex=md_table(METRICS_LEX),
                                sections="\n".join(sections))

DEST.write_text(doc, encoding="utf-8")
print("已生成：", DEST, "  %d 字节" % DEST.stat().st_size)
