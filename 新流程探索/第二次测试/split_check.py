# -*- coding: utf-8 -*-
"""把每篇拆成逐句清单并编号，用来做逐句过检、防漏标。

    python split_check.py            # 全部
    python split_check.py 灰烬之主    # 只按标题关键字过滤
"""
import re
import sys
from pathlib import Path

WS = Path(r"C:\Users\AWMPRO\AppData\Roaming\popwave\paopao-workspace\projects")

CHAPTERS = [
    ("灰烬之主 ch003", WS / r"9-10-项目a\正文\ch003.txt", None, None),
    ("旧海图 ch001-v3", WS / r"9-11-项目b\正文\ch001-v3.txt", None, None),
    ("雨夜收刀", WS / r"9-12-项目1\正文\第001章-雨夜收刀.md",
     "雨从黄昏下到子时", "忽然睁开了眼。"),
    ("灰烬之主 ch001", WS / r"9-10-项目a\正文\ch001.txt", None, None),
    ("考古 ch001", WS / r"9-11项目c\正文\ch001.txt", None, None),
]

SPLIT = re.compile(r"[^。！？]*[。！？][”』」]?")


def sentences(text: str):
    out = []
    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue
        parts = SPLIT.findall(line)
        tail = SPLIT.sub("", line).strip()
        out.extend(p.strip() for p in parts if p.strip())
        if tail:
            out.append(tail)
    return out


def main():
    key = sys.argv[1] if len(sys.argv) > 1 else None
    for title, path, s_mark, e_mark in CHAPTERS:
        if key and key not in title:
            continue
        if not path.exists():
            print("[缺文件]", path)
            continue
        t = path.read_text(encoding="utf-8-sig")
        if s_mark:
            t = t[t.index(s_mark):]
        if e_mark:
            t = t[:t.index(e_mark) + len(e_mark)]
        ss = sentences(t)
        print("=" * 70)
        print("%s   共 %d 句" % (title, len(ss)))
        print("=" * 70)
        for i, s in enumerate(ss, 1):
            print("%3d %s" % (i, s))
        print()


if __name__ == "__main__":
    main()
