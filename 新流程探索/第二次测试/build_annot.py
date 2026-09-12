# -*- coding: utf-8 -*-
"""
生成"正文标注对照.html"：逐句红黄绿，每一句都有颜色。

    python build_annot.py

红黄绿的定义（老板 2026-09-12 定）：
    红 = 有语病级的问题（读者读到会卡）：指代不明 / 描写与物理冲突 / 搭配错位 / 硬切短句 / 成分缺失
    黄 = 句子平庸：读得顺、不出错，但没亮点
    绿 = 至少 60 分水平：读得顺，而且这一句把场面立起来了（有具体落点或独有说法）

本轮标法：只用 RED / YEL 两张索引表列出红黄，其余默认绿。
    这样脚本不依赖我手数 625 个字符，减少笔误；明细文件逐句可核。
"""

import html
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent
OUT = BASE / "正文标注对照.html"
AUDIT = BASE / "标注明细.txt"
WS = Path(r"C:\Users\AWMPRO\AppData\Roaming\popwave\paopao-workspace\projects")

SPLIT = re.compile(r"[^。！？]*[。！？][”』」]?")
NAME = {"s": "红·有语病", "m": "黄·平庸", "o": "绿·60分以上", "d": "分隔"}

CHAPTERS = [
    ("灰烬之主 ch003", "走 skill（挂了黄金三章规划）", WS / r"9-10-项目a\正文\ch003.txt", None, None),
    ("旧海图 ch001-v3", "走 skill（挂了文风 DNA 夜无疆／辰东）", WS / r"9-11-项目b\正文\ch001-v3.txt", None, None),
    ("雨夜收刀", "零上下文直出（老板偏好的那篇）", WS / r"9-12-项目1\正文\第001章-雨夜收刀.md",
     "雨从黄昏下到子时", "忽然睁开了眼。"),
    ("灰烬之主 ch001", "走 skill（未挂文风 DNA）", WS / r"9-10-项目a\正文\ch001.txt", None, None),
    ("考古 ch001", "走 skill（写作那轮未读文风 DNA）", WS / r"9-11项目c\正文\ch001.txt", None, None),
]

RED = {
"灰烬之主 ch003": [1, 2, 4, 6, 7, 8, 9, 10, 11, 12, 33, 34, 35, 36, 37, 50, 93, 102, 103, 107, 108, 109, 118],
"旧海图 ch001-v3": [8, 15, 38, 53, 68, 100, 123, 125, 126, 127, 141, 142, 144, 161],
"雨夜收刀": [70],
"灰烬之主 ch001": [3, 4, 7, 9, 11, 18, 19, 21, 22, 36, 56, 74],
"考古 ch001": [28],
}

YEL = {
"灰烬之主 ch003": [3, 5, 13, 14, 16, 17, 18, 20, 21, 22, 26, 30, 32, 39, 42, 44, 46, 48, 54, 58, 59,
                   62, 65, 66, 69, 70, 72, 79, 91, 92, 100, 101, 104, 105, 106, 110, 114, 115, 116, 120, 121],
"旧海图 ch001-v3": [2, 5, 11, 17, 22, 25, 32, 33, 42, 43, 46, 50, 51, 52, 56, 60, 64, 65, 67, 69, 70, 71,
                    75, 77, 79, 81, 82, 85, 86, 88, 91, 94, 97, 109, 113, 115, 121, 122, 130, 131, 132, 133,
                    136, 138, 139, 140, 147, 153, 162, 163, 164],
"雨夜收刀": [24, 26, 66, 117, 118],
"灰烬之主 ch001": [4, 20, 21, 24, 33, 40, 44, 46, 50, 58, 66, 69, 73, 78, 83, 92, 95, 102, 105, 109, 110],
"考古 ch001": [17, 25, 29, 80, 106],
}

# 只给红档写理由（黄档理由基本就是"平庸"两个字，不逐条注）
WHY = {
"灰烬之主 ch003": {
    1: "成分缺失：一头扎进芦苇，缺「丛里」，芦苇当处所站不住",
    2: "搭配错位＋无施动无结果：叶子比人高；割在脸上（谁割、割成什么样没说）",
    4: "抽象感受当实体，还量化成「半里地」；且复述了 ch002 已用具体写法给过的同一个恐怖",
    6: "主语错位：把路走慢的是「他」，不是「看」",
    7: "动作被名词化成「那一下」再做判断，施动关系丢了，句式绕",
    8: "两个疑问碎片并列当主语，读者拿到的是碎块",
    9: "指代不明：「那地方」指哪儿没说清",
    10: "「跟」没有落点，跟向哪里没说",
    11: "「割」用错位：割是刀的动作或草割人",
    12: "「立着」带两个宾语，第二个（土屋）不搭",
    33: "指代不明：那东西是什么没交代，读者一头雾水。老板给的绿标准是这里该配外貌／形容描写把压迫力立起来",
    34: "描写与物理冲突：四条腿是交替的，不可能「一起一落」",
    35: "搭配错位：「侧里」不成词",
    36: "硬切短句：该和后面连成一句，被句号切开",
    37: "搭配错位：衣服和皮是两种东西，共用一个「开」",
    50: "成分不全：硬的、烫的——是什么没交代",
    93: "「脑子里」和「记忆里」两个「里」叠加，句子绊",
    102: "只交代没发生什么（没睡），不给处境。老板示范改法：靠墙坐着，始终睡不着",
    103: "动词悬空：翻没有对象、没有结果、没有目的",
    107: "并置碎片：与前后句说不出「因为／所以／然后／但是」",
    108: "同上，三句并置的第二句",
    109: "宾语后置当强调，「钥匙」甩到句末，揭示没带来新理解",
    118: "成分缺失：灯后头「牵着」一长串，谁牵的、牵什么，都没说",
},
"旧海图 ch001-v3": {
    8: "成分缺失＋硬切：擦得不快——擦什么不快、快慢的参照是什么，都没有",
    15: "「盯着自己」语义空转：前两样是物件，第三样突然变成「自己」",
    38: "语义空：「这条船就不认得自己了」读者拿不到具体感觉；且与后文「船开始重复自己」同义",
    53: "语法断：说他刚才看见一个人，背影，穿着他的衣服——名词块插进句中断开",
    68: "句式绕：「V 的是……」，且把读者自己能看出的意思直接点破",
    100: "句子不完整：数出来的是名字，缺「都」或「全是」",
    123: "硬切：他开口，一句话，甲板静了——三个节点硬切",
    125: "搭配错位：雾是弥散的，不会「穿过」人脸",
    126: "喻体与本体不同类：话不会落在板上，和缆绳用一个「一样响」并起来",
    127: "悬空：后半句到章末也没兑现，是为留白而留白",
    141: "语法断裂：「是什么」和「一样会要命的东西」之间缺连接词",
    142: "搭配生硬：「话落下」和「半盏茶」两个刻意的古味叠在一起",
    144: "指代重复加主语乱：「它」和「整条船」重复，贴到眼前的主语不清楚",
    161: "量词错位：凉用「一遍」计量不对",
},
"雨夜收刀": {
    70: "形容词错位：「平」不用于形容人说话，汉语里成立的是「声音平稳」「声音平静」",
},
"灰烬之主 ch001": {
    3: "搭配不当：喉咙里全是「烟」——烟是实体，喉咙里该是烟气／烟味",
    4: "赘余：「天是红的，红得发暗」和句末「把天烤成一片暗红」同一信息说了两遍",
    7: "结构混乱：一句里主语跳了两次。「七八岁的女孩」是名词短语（无谓语），接着换成「脸」做主语，再换成「一双眼睛」，中间没有交代",
    9: "表意不明：「它们来了」——是什么来了没说。前文没有任何东西出场，补不出唯一答案",
    11: "结构混乱：「想说自己昨天下班」和「钥匙还插在门锁上」被并到一起，后半句没有统领它的谓语",
    18: "表意不明：「胸口被什么顶了一下」——被什么？认出妹妹、记忆翻涌、还是别的，读者只能猜",
    19: "赘余：「腥，甜」已经在说味道，句末又「像血放久了发出来的味」，同一信息两遍",
    21: "表意不明：「一团东西」是什么没说清（悬念式先行指代，第 22 句才落实）",
    22: "表意不明：「比人高出一截」的主语是四条腿还是整团东西，有歧义",
    36: "不合逻辑：「那东西的哼声跟在后头，闷闷的，贴着地皮走」——声音不会贴着地皮走，能贴地皮走的是那个东西。施动张冠李戴",
    56: "成分残缺：「手里一盏快烧尽的油灯」缺谓语（手里提着／有）",
    74: "表意不明：「心口那块空着的地方」——前文没建立「心口空着一块」这个意象，读者不知道空的是什么",
},
"考古 ch001": {
    28: "省略过度：「两回手」该是「两回手笔」，简称到读着拗",
},
}


def units_of(line):
    parts = SPLIT.findall(line)
    tail = SPLIT.sub("", line).strip()
    us = [p.strip() for p in parts if p.strip()]
    if tail:
        us.append(tail)
    return us


def main():
    audit, blocks = [], []
    rows = []

    for title, sub, path, s_mark, e_mark in CHAPTERS:
        raw = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
        if s_mark:
            raw = raw[raw.index(s_mark):]
        if e_mark:
            raw = raw[:raw.index(e_mark) + len(e_mark)]
        head = ""
        lines = raw.split("\n")
        if lines and re.match(r"^第.+章\s", lines[0].strip()):
            head, lines = lines[0].strip(), lines[1:]
        raw = "\n".join(lines)

        red, yel = set(RED[title]), set(YEL[title])
        idx = n_o = n_m = n_s = n_d = 0
        body = []
        audit.append("=" * 68)
        audit.append("%s" % title)
        audit.append("=" * 68)

        for line in raw.split("\n"):
            st = line.strip()
            if not st:
                continue
            us = units_of(st)
            if len(us) == 1 and us[0] == "***":
                idx += 1
                n_d += 1
                body.append("<hr>")
                continue
            out = []
            for u in us:
                idx += 1
                lv = "s" if idx in red else ("m" if idx in yel else "o")
                if lv == "s":
                    n_s += 1
                elif lv == "m":
                    n_m += 1
                else:
                    n_o += 1
                why = WHY.get(title, {}).get(idx, "")
                tip = ' title="【%s】%s"' % (NAME[lv], html.escape(why)) if why \
                    else ' title="【%s】"' % NAME[lv]
                out.append('<span class="%s"%s>%s</span>' % (lv, tip, html.escape(u)))
                audit.append("%3d [%s] %s%s" % (idx, NAME[lv], u, ("　← " + why) if why else ""))
            body.append("<p>%s</p>" % "".join(out))

        h = '<h3>%s</h3>' % html.escape(head) if head else ""
        blocks.append('<section><h2>%s</h2><div class="sub">%s　共 %d 句：红 %d · 黄 %d · 绿 %d</div>%s%s</section>'
                      % (html.escape(title), html.escape(sub), idx, n_s, n_m, n_o, h, "".join(body)))
        rows.append((title, idx, n_s, n_m, n_o))
        audit.append("")

    t_s = sum(r[2] for r in rows)
    t_m = sum(r[3] for r in rows)
    t_o = sum(r[4] for r in rows)
    t_n = sum(r[1] for r in rows)

    tbl = "".join("<tr><td>%s</td><td>%d</td><td class='c2'>%d</td><td class='c3'>%d</td>"
                  "<td class='c1'>%d</td><td>%s</td></tr>"
                  % (t, n, s, m, o, ("%.0f%%" % (100.0 * s / n))) for t, n, s, m, o in rows)
    tbl += "<tr class='sum'><td>合计</td><td>%d</td><td class='c2'>%d</td><td class='c3'>%d</td><td class='c1'>%d</td><td></td></tr>" \
           % (t_n, t_s, t_m, t_o)

    doc = """<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<title>正文标注对照 · 逐句红黄绿</title>
<style>
:root{--s:#ffdede;--m:#fff4cf;--o:#eef8f0;--sb:#e5484d;--mb:#e2b100;--ob:#8fc79c;
--ink:#222;--dim:#6b6b6b;--line:#e6e6e6;}
*{box-sizing:border-box}
body{margin:0;background:#faf9f7;color:var(--ink);line-height:2.0;font-size:17px;
font-family:"Noto Sans CJK SC","WenQuanYi Micro Hei","Microsoft YaHei",system-ui,sans-serif;}
header{position:sticky;top:0;background:#fff;border-bottom:1px solid var(--line);padding:14px 28px;z-index:9}
h1{font-size:19px;margin:0 0 8px}
.legend{display:flex;gap:14px;flex-wrap:wrap;font-size:13.5px;color:var(--dim);align-items:center}
.chip{padding:2px 10px;border-radius:4px;border-left:3px solid}
.chip.s{background:var(--s);border-color:var(--sb)}
.chip.m{background:var(--m);border-color:var(--mb)}
.chip.o{background:var(--o);border-color:var(--ob)}
.wrap{max-width:900px;margin:0 auto;padding:22px 28px 80px}
table{width:100%%;border-collapse:collapse;font-size:14px;margin:0 0 26px;background:#fff}
th,td{border:1px solid var(--line);padding:6px 10px;text-align:left}
th{background:#f4f4f2;font-weight:600}
td.c1{background:var(--o)}td.c2{background:var(--s)}td.c3{background:var(--m)}
tr.sum td{font-weight:600;background:#f4f4f2}
section{margin:0 0 48px;background:#fff;border:1px solid var(--line);border-radius:10px;padding:22px 30px}
h2{font-size:19px;margin:0 0 4px}
h3{font-size:17px;margin:16px 0 12px;color:#444}
.sub{font-size:13px;color:var(--dim);margin-bottom:16px;padding-bottom:12px;border-bottom:1px dashed var(--line)}
p{margin:0 0 1.0em}
span.s,span.m,span.o{padding:1px 2px;border-radius:3px}
span.s{background:var(--s);box-shadow:inset 3px 0 0 var(--sb)}
span.m{background:var(--m);box-shadow:inset 3px 0 0 var(--mb)}
span.o{background:var(--o);box-shadow:inset 3px 0 0 var(--ob)}
hr{border:0;border-top:1px dashed var(--line);margin:22px 0}
footer{max-width:900px;margin:0 auto;padding:0 28px 60px;font-size:13px;color:var(--dim);line-height:1.9}
</style></head><body>
<header>
  <h1>正文标注对照 · 逐句红黄绿</h1>
  <div class="legend">
    <span class="chip s">红 有语病（读者读到会卡）</span>
    <span class="chip m">黄 平庸</span>
    <span class="chip o">绿 60 分以上</span>
    <span>鼠标停在句上看理由</span>
  </div>
</header>
<div class="wrap">
<table><tr><th>篇</th><th>句数</th><th>红</th><th>黄</th><th>绿</th><th>红占比</th></tr>%s</table>
%s
</div>
<footer>红＝指代不明／描写与物理冲突／搭配错位／硬切短句／成分缺失，读者读到会卡。<br>
黄＝读得顺但没亮点。绿＝读得顺，而且这一句把场面立起来了。<br>
每一句都过检，明细逐句另存 标注明细.txt。</footer>
</body></html>""" % (tbl, "\n".join(blocks))

    OUT.write_text(doc, encoding="utf-8")
    AUDIT.write_text("\n".join(audit), encoding="utf-8")
    print("生成 %s（%.1f KB）" % (OUT.name, OUT.stat().st_size / 1024))
    print("生成 %s" % AUDIT.name)
    for t, n, s, m, o in rows:
        print("  %-16s 共%3d  红%3d  黄%3d  绿%3d  红占比%2.0f%%" % (t, n, s, m, o, 100.0 * s / n))
    print("  合计            共%3d  红%3d  黄%3d  绿%3d" % (t_n, t_s, t_m, t_o))


if __name__ == "__main__":
    main()
