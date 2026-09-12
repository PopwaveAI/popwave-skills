# -*- coding: utf-8 -*-
"""两槽位探针：指标表 ＋ 对照阅读页（并入上一轮 C1 作基线）。"""

import html
import re
import statistics
from pathlib import Path

BASE = Path(__file__).resolve().parent
OUT = BASE / "输出" / "两槽位探针"
GENRE_OUT = BASE / "输出" / "流派词探针"
DEST_MD = OUT / "两槽位探针-机器指标.md"
DEST_HTML = BASE / "两槽位探针-对照阅读.html"

ROWS = [
    ("D0", "武侠，不加信息（基线＝上轮 C1）", GENRE_OUT / "C1__clean.txt",
     "写一段武侠小说第一章。", None, "—"),
    ("D1", "武侠＋信息4条（散文）", OUT / "D1__clean.txt", None,
     "姓赵·师父·十年·七封信·敲门（5 条）", "5/5"),
    ("D2", "武侠＋信息7条（散文）", OUT / "D2__clean.txt", None,
     "5 条 ＋ 叮嘱·地图·不能住·章末脚步声（9 条）", "9/9"),
    ("D3", "武侠＋信息7条（条目式）", OUT / "D3__clean.txt", None, "同 D2，改条目形态", "8/9"),
    ("D4", "无线索词＋信息7条（散文）", OUT / "D4__clean.txt", None, "同 D2，去掉流派词", "7/9"),
]
PREMISE = ("一个人回到十年前的旧居。房子早已空了，房东换过三任。"
           "他在二楼朝北的屋子里找到一只铁盒，里面是当年没寄出的信。"
           "当晚他决定住下，把信一封封重读。")

LEX_WUXIA = r"内力|真气|招式|剑法|刀法|掌法|江湖|门派|师兄|轻功|内功|心法|恩怨|客栈|帮派|秘籍|运功|点穴|暗器|刀光|剑影|剑气|武功|掌门|弟子|兵刃|身法|气劲|侠客|大侠"
BODY = r"(胸口|喉咙|心口|后背|脊背|手心|指尖|头皮|呼吸|心跳)[^。！？]{0,12}(一紧|发凉|发紧|发冷|发热|一沉|收紧|发麻|顿住|停了一拍|沉下去|缩紧|发烫|发僵|一抽)"
HAN = re.compile(r"[\u4e00-\u9fff]")
SENT = re.compile(r"[。！？…]+")


def metrics(p: Path):
    t = p.read_text(encoding="utf-8")
    body = re.sub(r"\s+", "", t)
    han = len(HAN.findall(t))
    paras = [l for l in t.splitlines() if l.strip()]
    sl = [len(HAN.findall(s)) for s in SENT.split(body) if HAN.findall(s)]
    return {
        "han": han, "paras": len(paras), "avg_para": round(han / max(len(paras), 1), 1),
        "sent_avg": round(statistics.mean(sl), 1) if sl else 0,
        "short_pct": round(sum(1 for x in sl if x < 10) / max(len(sl), 1) * 100, 1),
        "wuxia": len(re.findall(LEX_WUXIA, body)),
        "body_emo": len(re.findall(BODY, body)),
        "dash": t.count("\u2014"), "ellipsis": t.count("\u2026"),
        "md": t.count("**"),
    }


data = [(c, lab, metrics(p), prov, rate) for c, lab, p, _, prov, rate in ROWS]

# ---- 指标 md ----
L = ["# 两槽位探针 · 机器指标\n",
     "> 流派词 ＋ 本章要写什么信息。同情境、同流派词（武侠），只动信息槽。"
     "deepseek-flash，温度 1.0，零 system message。基线 D0 复用上一轮 C1 稿。\n",
     "| 条件 | 标签 | 硬事实兑现 | 汉字 | 段数 | 平均段长 | 句长均值 | 短句(<10字)占比 | 武侠词命中 | 破折号 | 省略号 |",
     "|:--|:--|:--|--:|--:|--:|--:|--:|--:|--:|--:|"]
for c, lab, m, prov, rate in data:
    L.append("| %s | %s | %s | %d | %d | %s | %s | %s%% | %d | %d | %d |" % (
        c, lab, rate, m["han"], m["paras"], m["avg_para"], m["sent_avg"],
        m["short_pct"], m["wuxia"], m["dash"], m["ellipsis"]))
L.append("\n注：D1 的信息槽只给了 5 条事实（姓赵、师父、十年、七封信、敲门），"
         "故其分母与 D2/D3/D4 不同；D1 另外自行补了章末脚步声。"
         "D0 无信息槽，兑现率不适用。\n")
L.append("未兑现明细：")
L.append("- D1：半张地图、说了不能住、前六封是叮嘱（三条均未列入信息槽，属正常）")
L.append("- D3：前六封是叮嘱")
L.append("- D4：前六封是叮嘱、**有人敲门**（关键事件漏写）")
DEST_MD.write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L))


def paras_html(text: str) -> str:
    parts = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    if len(parts) <= 1:
        parts = [p.strip() for p in text.splitlines() if p.strip()]
    return "\n".join("<p>%s</p>" % html.escape(p) for p in parts)


def table_html() -> str:
    out = ["<table><tr><th>条件</th><th>标签</th><th class='n'>硬事实兑现</th><th class='n'>汉字</th>"
           "<th class='n'>平均段长</th><th class='n'>句长均值</th><th class='n'>短句占比</th>"
           "<th class='n'>武侠词</th></tr>"]
    for c, lab, m, prov, rate in data:
        out.append("<tr><td>%s</td><td>%s</td><td class='n'>%s</td><td class='n'>%d</td>"
                   "<td class='n'>%s</td><td class='n'>%s</td><td class='n'>%s%%</td>"
                   "<td class='n'>%d</td></tr>" % (c, lab, rate, m["han"], m["avg_para"],
                                                   m["sent_avg"], m["short_pct"], m["wuxia"]))
    out.append("</table>")
    return "\n".join(out)


sections = []
for c, lab, m, prov, rate in data:
    src = dict((x[0], x[2]) for x in ROWS)[c]
    text = src.read_text(encoding="utf-8")
    body = paras_html(text)
    if c == "D0":
        pinfo = "（不加信息槽）"
    else:
        pinfo = dict((x[0], x[4]) for x in ROWS)[c]
    sections.append("""
<section id="{c}">
  <h2>{c} · {lab}</h2>
  <div class="prompt"><span class="k">提示词</span><code>{head}

{premise}

{pinfo}</code></div>
  <article class="prose">{body}</article>
</section>""".format(c=c, lab=html.escape(lab), head=html.escape(
        "写一段武侠小说第一章。" if c != "D4" else "写一段小说第一章。"),
        premise=html.escape(PREMISE), pinfo=html.escape(pinfo), body=body))

nav = " · ".join('<a href="#%s">%s</a>' % (row[0], row[0]) for row in ROWS)
doc = """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<title>两槽位探针 · 对照阅读</title>
<style>
  :root{{--ink:#1b1a18;--dim:#6b6660;--line:#e2ded7;--bg:#faf8f5;--card:#fff;--hi:#8c5a2b}}
  *{{box-sizing:border-box}}
  body{{margin:0;background:var(--bg);color:var(--ink);
    font-family:Georgia,"Songti SC","Source Han Serif SC",SimSun,serif;line-height:1.85}}
  header.top{{position:sticky;top:0;z-index:9;background:rgba(250,248,245,.94);
    backdrop-filter:blur(6px);border-bottom:1px solid var(--line);padding:12px 24px;
    display:flex;gap:16px;align-items:baseline;flex-wrap:wrap}}
  header.top b{{font-size:15px}}
  header.top a{{color:var(--hi);text-decoration:none;font-size:13px;
    font-family:system-ui,"Microsoft YaHei",sans-serif}}
  .wrap{{max-width:940px;margin:0 auto;padding:32px 24px 96px}}
  h1{{font-size:24px;margin:8px 0 6px}}
  .lead{{color:var(--dim);font-size:14px;font-family:system-ui,"Microsoft YaHei",sans-serif;
    line-height:1.9;margin:0 0 22px}}
  .panel{{background:var(--card);border:1px solid var(--line);border-radius:10px;
    padding:18px 20px;margin:0 0 26px}}
  .panel h3{{margin:0 0 10px;font-size:14px;font-family:system-ui,"Microsoft YaHei",sans-serif}}
  table{{border-collapse:collapse;width:100%;font-size:13px;margin:6px 0 12px;
    font-family:system-ui,"Microsoft YaHei",sans-serif}}
  th,td{{border-bottom:1px solid var(--line);padding:7px 8px;text-align:left}}
  th{{color:var(--dim);font-weight:600;background:#f4f1ec}}
  td.n{{font-variant-numeric:tabular-nums}}
  section{{margin:0 0 52px;scroll-margin-top:64px}}
  h2{{font-size:19px;margin:0 0 14px;padding-bottom:8px;border-bottom:2px solid var(--ink)}}
  .prompt{{background:#f2efe9;border-left:3px solid var(--hi);border-radius:0 8px 8px 0;
    padding:12px 16px;margin:0 0 20px;font-family:system-ui,"Microsoft YaHei",sans-serif;
    font-size:13px;color:#4a453f;line-height:1.85}}
  .prompt .k{{display:block;color:var(--dim);font-size:12px;margin-bottom:6px}}
  .prompt code{{white-space:pre-wrap;font-family:inherit}}
  .prose p{{margin:0 0 1.05em;text-indent:2em;font-size:16.5px}}
  .prose p:first-child{{text-indent:0}}
</style></head><body>
<header class="top"><b>两槽位探针 · 对照阅读</b><span>{nav}</span></header>
<div class="wrap">
<h1>流派词 ＋ 本章要写什么信息</h1>
<p class="lead">四个条件同情境、同流派词（武侠），只动「本章要写什么信息」这个槽位；
D4 拿掉流派词做关键对照，D0 复用上一轮 C1（有流派词、不加信息）作基线。<br>
判读要点：①信息槽写散文时硬事实是否全兑现；②改条目式后段长是否变碎（P4 复现）；
③拿掉流派词后，同一个信息槽的兑现率与文体是否一起掉。</p>
<div class="panel"><h3>机器指标</h3>{table}
<p style="font-size:13px;color:var(--dim);font-family:system-ui,'Microsoft YaHei',sans-serif;margin:0">
D1 的信息槽只列了 5 条事实，分母与其余不同；它另外自行补了章末脚步声。
「身体反应写情绪」五稿均为 0。</p></div>
{sections}
</div></body></html>""".format(nav=nav, table=table_html(), sections="\n".join(sections))

DEST_HTML.write_text(doc, encoding="utf-8")
print("\n阅读页：", DEST_HTML, DEST_HTML.stat().st_size, "字节")
