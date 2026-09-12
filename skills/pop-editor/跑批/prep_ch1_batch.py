# -*- coding: utf-8 -*-
"""批量抽整章素材（新增书用）。取代老的 extract_ch1.py 与 prep_material_v2.py 的取章部分。

切法：在头部区域找**最后一个**匹配「第1章」的标题行，从它之后开始收正文；
     正文里按导航词过滤，遇到「第2章」标题即停；碰到正文中的导航行也直接停（说明进了尾部推荐块）。

用法：改下方 JOBS 后直接跑，跑完用 rebuild_manifest.py 重建 manifest。
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
REPO = Path(r"d:\popwave-skills")
MAT = REPO / "新流程探索" / "网文编辑" / "素材"
HAN = re.compile(r"[\u4e00-\u9fff]")
CH_TITLE = re.compile(r"^#?\s*(?:第\s*[0-9一二三四五六七八九十百千]+\s*卷[\s\u3000]*)?(?:正文\s*)?第\s*([0-9一二三四五六七八九十百千]+)\s*[章回节][\s\u3000]*(.*)$")
CN_DIGIT = {"一": 1, "二": 2, "两": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9,
            "十": 10, "百": 100, "千": 1000, "零": 0}


def cn2int(s):
    """把章号（阿拉伯或中文数字）转成整数。中文只处理到千位，够章节号用。

    2026-09-13 踩过：起点那批 txt 的标题写「第一章」，旧正则只认 `第(\\d+)章`，
    于是剑烛大荒／捞尸人／黜龙／超维度玩家四本全被判"找不到第1章标题"。
    """
    if s.isdigit():
        return int(s)
    total, section, num = 0, 0, 0
    for ch in s:
        v = CN_DIGIT.get(ch)
        if v is None:
            return None
        if v >= 10:
            section += (num or 1) * v
            num = 0
        else:
            num = v
    return total + section + num
NAV = re.compile(
    r"零点小说|^书架|最新网址|亲[,，]?\s*(双击|点击)|本站所有|返回目录|^上一篇|^下一篇|"
    r"为您推荐|排行榜|推荐榜|加入书签|手机版|天才一秒|请记住本书|www\.|https?://|"
    r"如果侵犯|立场无关|自动滚动|打满分的|书友|请假|更新(时间|放到)"
)
CAT = {"玄幻", "仙侠", "言情", "历史", "网游", "科幻", "恐怖", "其他", "榜单", "总排行榜"}

# (档位目录, id, 相对 参考小说txt 的路径)
JOBS_DEFAULT = [
    ("四十40", "A-明末从西北再造天下-第1章", r"起点\历史\明末，从西北再造天下-小兵王2.txt"),
    ("四十40", "A-莫欺老年穷-第1章", r"番茄\都市\莫欺老年穷，一天增加一个天赋点-被提线的木偶.txt"),
    ("四十40", "A-普攻永久加生命-第1章", r"番茄\科幻游戏\普攻永久加生命，这个弓箭手有亿点肉-江湖人称老薛.txt"),
]

# 命令行传参优先（免去反复改本文件）：
#   python prep_ch1_batch.py --job "八十80|A-剑烛大荒-第1章|起点\玄幻仙侠\剑烛大荒-爱潜水的乌贼.txt"
# 可传多个 --job；不传则跑 JOBS_DEFAULT。
JOBS = JOBS_DEFAULT
if "--job" in sys.argv:
    JOBS = []
    for i, a in enumerate(sys.argv):
        if a == "--job" and i + 1 < len(sys.argv):
            gear, rid, rel = sys.argv[i + 1].split("|", 2)
            JOBS.append((gear, rid, rel))

for gear, rid, rel in JOBS:
    src = REPO / "参考小说txt" / rel
    if not src.exists():
        print("!! 缺 %s" % rel)
        continue
    (MAT / gear).mkdir(parents=True, exist_ok=True)
    lines = src.read_bytes()[: 8 * 1024 * 1024].decode("utf-8", "ignore").splitlines()
    head = lines[:100]
    starts = []
    for i, r in enumerate(head):
        m = CH_TITLE.match(r.strip())
        if m and cn2int(m.group(1)) == 1:
            starts.append(i)
    if not starts:
        print("!! 找不到第1章标题 %s" % rel)
        continue
    begin = starts[-1] + 1
    ch_title = CH_TITLE.match(head[starts[-1]].strip()).group(2)
    body, dropped, stop = [], 0, "读到第2章标题"
    for raw in lines[begin:]:
        s = raw.strip()
        if not s:
            continue
        m = CH_TITLE.match(s)
        if m and cn2int(m.group(1)) >= 2:
            break
        if s in CAT or NAV.search(s):
            dropped += 1
            if body:
                stop = "正文中遇导航行「%s」" % s[:16]
                break
            continue
        body.append(s)
    else:
        stop = "读到文件尾（前 8MB）"
    text = "\n\n".join(body)
    out = MAT / gear / ("%s.md" % rid)
    out.write_text(text, encoding="utf-8")
    print("  %-28s 段 %4d  过滤 %2d  字 %5d  章题「%s」  停因：%s"
          % (rid, len(body), dropped, len(HAN.findall(text)), ch_title, stop))
