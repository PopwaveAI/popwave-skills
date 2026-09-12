# -*- coding: utf-8 -*-
"""按磁盘重建 素材/manifest.jsonl。素材一动就重建，防 manifest 与实际文件漂移。

单一事实源：本脚本的 SOURCE 表（id + 来源说明由人写）＋ 磁盘实际文件（路径与字数由脚本算）。
重建后必须打印条数对照。

踩过的坑（2026-09-13）：
1. 曾有一版按已废弃的「高/中/低」目录重建，目录不存在就被静默清空，跑一次 manifest 就没了。
2. 曾有一版把档位目录写成「不合格20-30」，而实际目录叫「不合格」，6 份不合格稿被静默丢掉。
3. 曾有一版用文件名当 id，把 flash 那批的 id（J-flash-武侠）换成了文件名（flash-武侠-r01），映射表失配。
所以：档位目录名照磁盘写；id 由 ALIAS 显式指定，不用文件名兜底；每次重建都打印每档份数。
"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
SK = Path(r"d:\popwave-skills\新流程探索\网文编辑")
MAT = SK / "素材"
HAN = re.compile(r"[\u4e00-\u9fff]")
TRACK = "玄幻-东方幻想"
GEARS = ("八十80", "六十60", "四十40", "合格边缘", "不合格")

# 文件名（stem）→ (id, 来源)。id 与文件名不同的只在这里写；其余 id 同 stem。
SOURCE = {
    "A-夜无疆-第1章": "名家原文·夜无疆 第1章（永夜）",
    "A-凡骨-第1章": "小爆款·凡骨 第1章（出瑶池，来自天狩大圣的赐教）",
    "A-不死帝师-第1章": "小爆款·不死帝师 第1章（沉睡十年物是为人）",
    "A-天渊-第1章": "小爆款·天渊 第1章（从天渊禁区归来）",
    "A-系统赋我长生-第1章": "小爆款·系统赋我长生 第1章（长生万古 开始加点）",
    "A-烟雨楼-第1章": "小爆款·烟雨楼 第1章（天资妖孽李子夜）",
    "A-明末从西北再造天下-第1章": "40档·起点历史《明末，从西北再造天下》（小兵王2）第1章；首订 384",
    "A-莫欺老年穷-第1章": "40档·七猫都市《莫欺老年穷，一天增加一个天赋点》（被提线的木偶）第1章；在读 0.7 万",
    "A-普攻永久加生命-第1章": "40档·七猫／书旗游戏《普攻永久加生命，这个弓箭手有亿点肉》（江湖人称老薛）第1章；在读 0.1 万",
    "A-剑烛大荒-第1章": "80档·起点玄幻《剑烛大荒》（爱潜水的乌贼）第1章；首订 114125",
    "A-捞尸人-第1章": "80档·起点都市《捞尸人》（纯洁滴小龙）第1章；首订 2.8 万，均订超 10 万",
    "A-十日终焉-第1章": "80档·番茄悬疑《十日终焉》（杀虫队队员）第1章；在读 186 万至 260 万",
    "A-黜龙-第1章": "60档·起点历史《黜龙》（榴弹怕水）第1章；首订 7920，均订 3.2 万",
    "A-超维度玩家-第1章": "60档·起点游戏《超维度玩家》（诸生浮屠）第1章；首订 6518",
    "A-1984川菜馆-第1章": "60档·起点都市《1984：从破产川菜馆开始》（轻语江湖）第1章；首订 3480",
    "A-全民大航海时代-第1章": "60档·番茄游戏《全民大航海时代》（新买的桃子）第1章；在读 37.1 万",
    "A-网游蓝星online-第1章": "60档·番茄游戏《网游：蓝星online》（吃手）第1章；在读 8.4 万",
    "flash-仙侠修真-r01": "第二轮 flash 直出·仙侠修真 r01",
    "flash-武侠-r01": "第二轮 flash 直出·武侠 r01",
    "flash-西幻玄幻-r01": "第二轮 flash 直出·西幻玄幻 r01",
    "flash-都市异能-r01": "第二轮 flash 直出·都市异能 r01",
    "flash-克苏鲁航海-r01": "第二轮 flash 直出·克苏鲁航海 r01",
    "J-两槽位D2": "第二轮实测·武侠·两槽位 D2",
    "J-稳定S01": "第三轮实测·武侠·稳定 S01",
    "J-稳定S02": "第三轮实测·武侠·稳定 S02",
    "J-稳定S03": "第三轮实测·武侠·稳定 S03",
    "J-稳定S04": "第三轮实测·武侠·稳定 S04",
    "J-稳定S05": "第三轮实测·武侠·稳定 S05",
    "J-辰东L1": "第三轮实测·玄幻·辰东 L1",
    "J-辰东L2": "第三轮实测·玄幻·辰东 L2",
    "X-雨夜收刀": "popagent·9-12-项目1",
    "X-灰烬之主ch001": "popagent·9-10-项目a（带作者逐行判定）",
    "X-灰烬之主ch002": "popagent·9-10-项目a",
    "X-旧海图ch001": "popagent·9-11-项目b",
    "X-旧海图v2": "popagent·9-11-项目b",
    "X-旧海图v3": "popagent·9-11-项目b",
}
ALIAS = {
    "flash-仙侠修真-r01": "J-flash-仙侠修真",
    "flash-武侠-r01": "J-flash-武侠",
    "flash-西幻玄幻-r01": "J-flash-西幻玄幻",
    "flash-都市异能-r01": "J-flash-都市异能",
    "flash-克苏鲁航海-r01": "J-flash-克苏鲁航海",
}

recs = []
for folder in GEARS:
    for p in sorted((MAT / folder).glob("*.md")):
        t = p.read_text(encoding="utf-8")
        recs.append({
            "id": ALIAS.get(p.stem, p.stem), "档位": folder, "赛道": TRACK, "场景": "整章",
            "来源": SOURCE.get(p.stem, "!! 来源未登记，请在 rebuild_manifest.py 的 SOURCE 表补一行"),
            "路径": "素材/%s/%s.md" % (folder, p.stem), "字数": len(HAN.findall(t)),
        })

# 档样库短段（不落盘为素材文件，路径指向 reference）。
# 口径变更 2026-09-13：旧"满分80-90"与"七十70"两档按成绩合并为「八十80」——
# 番茄头部五本的在读是 67 万至 117 万，落在番茄品类榜前两名那一档，按成绩就是 80 档。
for i in range(1, 13):
    recs.append({"id": "F-夜无疆-%02d" % i, "档位": "八十80", "赛道": TRACK,
                 "来源": "名家原文·夜无疆（起点·辰东）", "路径": "references/档样库-玄幻.md#样%02d" % i,
                 "字数": None})
for i in range(1, 13):
    recs.append({"id": "S-番茄头部-%02d" % i, "档位": "八十80", "赛道": TRACK,
                 "来源": "番茄头部五本（凡骨／不死帝师／天渊／系统赋我长生／烟雨楼）",
                 "路径": "references/档样库-七十分.md#样70-%02d" % i, "字数": None})
for i in range(1, 7):
    recs.append({"id": "T-不温不火-%02d" % i, "档位": "四十40", "赛道": TRACK,
                 "来源": "显著不温不火三本（明末／莫欺老年穷／普攻永久加生命）",
                 "路径": "references/档样库-四十分.md#样40-%02d" % i, "字数": None})

(MAT / "manifest.jsonl").write_text(
    "\n".join(json.dumps(r, ensure_ascii=False) for r in recs) + "\n", encoding="utf-8")

print("manifest 重建：共 %d 条" % len(recs))
for g in GEARS:
    print("  %-10s 整章 %2d 份" % (g, len([r for r in recs if r["档位"] == g and not r["路径"].startswith("references/")])))
print("  档样短段 满分 12 ＋ 七十 12")
unregistered = [r["id"] for r in recs if r["来源"].startswith("!!")]
if unregistered:
    print("  !! 来源未登记：%s" % "、".join(unregistered))
for r in recs:
    if not r["路径"].startswith("references/"):
        print("    %-10s %-22s %5s 字  %s" % (r["档位"], r["id"], r["字数"], r["来源"]))
