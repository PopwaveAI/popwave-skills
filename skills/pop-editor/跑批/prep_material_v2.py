# -*- coding: utf-8 -*-
"""素材重建（v2）：档位由产源决定，不由读后印象决定。

80-90  名家原文（夜无疆）→ references 档样库-玄幻.md
70     小爆款（凡骨、不死帝师）→ references 档样库-七十分.md
合格边缘 deepseek-flash 直出（第二轮十赛道 r01 + 第三轮实测稿）→ 素材/合格边缘/
20-30  popagent 产出（9-12-项目1、9-10-项目a、9-11-项目b 正文）→ 素材/不合格/
"""
import json
import re
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
REPO = Path(r"d:\popwave-skills")
SK = REPO / "新流程探索" / "网文编辑"
MAT = SK / "素材"
P2 = REPO / "新流程探索" / "第二次测试"
P3 = REPO / "新流程探索" / "第三次测试"
PROJ = Path(r"C:\Users\AWMPRO\AppData\Roaming\popwave\paopao-workspace\projects")
HAN = re.compile(r"[\u4e00-\u9fff]")
TRACK = "玄幻-东方幻想"

# 清掉旧的三档目录（旧口径已废）
for old in ("高", "中", "低"):
    p = MAT / old
    if p.exists():
        shutil.rmtree(p)
        print("删旧档目录：素材/%s（口径已废）" % old)
for new in ("合格边缘", "不合格"):
    (MAT / new).mkdir(parents=True, exist_ok=True)

records = []
for i in range(1, 13):
    records.append({"id": "F-夜无疆-%02d" % i, "档位": "满分80-90", "赛道": TRACK,
                    "来源": "名家原文·夜无疆", "路径": "references/档样库-玄幻.md#样%02d" % i, "字数": None})
for i in range(1, 7):
    records.append({"id": "S-小爆款-%02d" % i, "档位": "七十70", "赛道": TRACK,
                    "来源": "小爆款·凡骨/不死帝师", "路径": "references/档样库-七十分.md#样70-0%d" % i, "字数": None})


def strip_flash(md_text, want="01"):
    m = re.search(r"##\s*第\s*%s\s*稿(.*?)(?=\n##\s*第|\Z)" % want, md_text, re.S)
    if not m:
        return None
    keep = [l.strip() for l in m.group(1).splitlines()
            if l.strip() and not l.strip().startswith((">", "|", "#"))]
    return "\n\n".join(keep).strip()


# ---- 合格边缘：flash 直出 ----
for t in ("仙侠修真", "武侠", "西幻玄幻", "都市异能", "克苏鲁航海"):
    f = P2 / "输出" / "deepseek-flash" / t / ("%s.md" % t)
    if f.exists():
        body = strip_flash(f.read_text(encoding="utf-8"), "01")
        if body:
            out = MAT / "合格边缘" / ("flash-%s-r01.md" % t)
            out.write_text(body, encoding="utf-8")
            records.append({"id": "J-flash-%s" % t, "档位": "合格边缘", "赛道": TRACK,
                            "来源": "flash 直出·%s r01" % t, "路径": "素材/合格边缘/%s" % out.name,
                            "字数": len(HAN.findall(body))})

for rid, src, note in [
    ("J-稳定S01", P3 / "06-稳定性5稿" / "输出" / "S01__clean.txt", "第三轮 flash·武侠"),
    ("J-稳定S02", P3 / "06-稳定性5稿" / "输出" / "S02__clean.txt", "第三轮 flash·武侠"),
    ("J-稳定S03", P3 / "06-稳定性5稿" / "输出" / "S03__clean.txt", "第三轮 flash·武侠"),
    ("J-稳定S04", P3 / "06-稳定性5稿" / "输出" / "S04__clean.txt", "第三轮 flash·武侠"),
    ("J-稳定S05", P3 / "06-稳定性5稿" / "输出" / "S05__clean.txt", "第三轮 flash·武侠"),
    ("J-辰东L1", P3 / "02-辰东文风四级" / "输出" / "L1__clean.txt", "第三轮 flash·玄幻"),
    ("J-辰东L2", P3 / "02-辰东文风四级" / "输出" / "L2__clean.txt", "第三轮 flash·玄幻"),
    ("J-两槽位D2", P2 / "输出" / "两槽位探针" / "D2__clean.txt", "第二轮 flash·武侠"),
]:
    if src.exists():
        t = src.read_text(encoding="utf-8")
        out = MAT / "合格边缘" / ("%s.md" % rid)
        out.write_text(t, encoding="utf-8")
        records.append({"id": rid, "档位": "合格边缘", "赛道": TRACK, "来源": note,
                        "路径": "素材/合格边缘/%s.md" % rid, "字数": len(HAN.findall(t))})
    else:
        print("!! 缺 %s" % src)

# ---- 不合格：popagent 产出 ----
for rid, src, note in [
    ("X-雨夜收刀", PROJ / "9-12-项目1" / "正文" / "第001章-雨夜收刀.md", "popagent·9-12-项目1"),
    ("X-灰烬之主ch001", PROJ / "9-10-项目a" / "正文" / "ch001.txt", "popagent·9-10-项目a（带作者逐行判定）"),
    ("X-灰烬之主ch002", PROJ / "9-10-项目a" / "正文" / "ch002.txt", "popagent·9-10-项目a"),
    ("X-旧海图ch001", PROJ / "9-11-项目b" / "正文" / "ch001.txt", "popagent·9-11-项目b"),
    ("X-旧海图v2", PROJ / "9-11-项目b" / "正文" / "ch001-v2.txt", "popagent·9-11-项目b"),
    ("X-旧海图v3", PROJ / "9-11-项目b" / "正文" / "ch001-v3.txt", "popagent·9-11-项目b"),
]:
    if src.exists():
        t = src.read_text(encoding="utf-8")
        out = MAT / "不合格" / ("%s.md" % rid)
        out.write_text(t, encoding="utf-8")
        records.append({"id": rid, "档位": "不合格20-30", "赛道": TRACK, "来源": note,
                        "路径": "素材/不合格/%s.md" % rid, "字数": len(HAN.findall(t))})
    else:
        print("!! 缺 %s" % src)

(MAT / "manifest.jsonl").write_text(
    "\n".join(json.dumps(r, ensure_ascii=False) for r in records) + "\n", encoding="utf-8")

print("\n=== 重建结果 ===")
from collections import Counter
c = Counter(r["档位"] for r in records)
for k, v in c.items():
    print("  %-12s %d 条" % (k, v))
print("  manifest 共 %d 条" % len(records))
for r in records:
    if r["档位"] != "满分80-90":
        print("    %-14s %-16s %s 字" % (r["档位"], r["id"], r["字数"]))
