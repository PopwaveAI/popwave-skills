# -*- coding: utf-8 -*-
"""素材归一：跑批前必做。把每份稿洗成"纯正文"。

三道洗法，只动首尾与杂质，绝不删正文：
1. 砍模型思考块：从含 `<details>` 或 `<summary>` 的行起到文末全砍（第二轮 flash 直出稿尾巴带过 5 份）。
2. 剥开篇标题行：匹配章号（第X章/回/节）开头，或长度 ≤12 且无句读的短行 → 剥。
   为什么必须剥：G18（正文夹带工作标记）是文笔质感的硬门槛，标题行只出现在部分稿上，
   会不对称地触发 G18，把合格边缘档压进红线组，制造成假倒挂。
3. 砍尾部的站点导航与推荐块：命中导航词即从该行砍到文末（不死帝师曾带进 7 行零点小说导航）。
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
MAT = Path(r"d:\popwave-skills\新流程探索\网文编辑\素材")

CH = re.compile(r"^第\s*[0-9一二三四五六七八九十百千]+\s*[章回节]")
PUNCT = re.compile(r"[。！？，、；：”“‘’…—\-·？！”\"'()（）]")
BLOCK = re.compile(r"<details|<summary|</details>")
NAV = re.compile(
    r"零点小说|^书架|最新网址|亲[,，]?\s*(双击|点击)|本站所有|返回目录|^上一篇|^下一篇|"
    r"为您推荐|排行榜|推荐榜|加入书签|手机版|天才一秒|请记住本书|www\.|https?://|"
    r"如果侵犯|立场无关|自动滚动"
)
# 作者感言与求票（2026-09-13 踩过：《超维度玩家》第1章正文里夹着一行「【PS：开新书了。求个追读。就这么多。】」，
# 编辑评委据此打 G18，把 60 档稿压到文笔末位。这类行不是正文，必须砍。）
AUTHOR_NOTE = re.compile(
    r"^【?\s*PS\s*[：:】]|求个?\s*追读|求\s*(月票|推荐票|收藏|追读)|^作者的话|^ps[：:]|开新书了"
)


def clean(lines):
    notes = []
    # 1. 砍思考块（含标签行及其后全部内容）
    for i, raw in enumerate(lines):
        if BLOCK.search(raw):
            lines = lines[:i]
            notes.append("砍思考块（原第 %d 行起）" % (i + 1))
            break
    # 3. 砍尾部导航块与作者感言
    for i, raw in enumerate(lines):
        s = raw.strip()
        if (NAV.search(s) or AUTHOR_NOTE.search(s)) and i > 0:
            lines = lines[:i]
            notes.append("砍尾部杂质（原第 %d 行「%s」）" % (i + 1, s[:18]))
            break
    # 2. 剥开篇标题行
    for i, raw in enumerate(lines):
        s = raw.strip()
        if not s:
            continue
        if CH.match(s) or (len(s) <= 12 and not PUNCT.search(s)):
            lines = lines[i + 1:]
            notes.append("剥首行标题「%s」" % s[:18])
        break
    while lines and not lines[0].strip():
        lines = lines[1:]
    return lines, notes


changed = 0
for p in sorted(MAT.rglob("*.md")):
    if p.name in ("README.md", "映射表-封存.md"):
        continue
    before = p.read_text(encoding="utf-8")
    lines, notes = clean(before.splitlines())
    after = "\n".join(lines).strip() + "\n"
    if notes:
        p.write_text(after, encoding="utf-8")
        changed += 1
        print("  %-26s %s" % (p.name, "；".join(notes)))
    else:
        print("  %-26s 干净" % p.name)
print("\n共洗 %d 份" % changed)
