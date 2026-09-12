# -*- coding: utf-8 -*-
"""匿名化：读 素材/manifest.jsonl → 固定种子打乱 → 输出纯正文匿名稿 + 封存映射表"""
import argparse
import json
import random
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
SK = Path(r"d:\popwave-skills\新流程探索\网文编辑")
MAT = SK / "素材"
OUT = SK / "跑批" / "输入"
SEED = 20260913
CN = "一二三四五六七八九十"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--round", default=1)
    ap.add_argument("--n", type=int, default=6, help="本批取几稿")
    ap.add_argument("--plan", default="", help='分层抽样，例："满分80-90:1,七十70:1,合格边缘:2,不合格20-30:2"')
    ap.add_argument("--ids", default="", help="指定稿号（逗号分隔），用于控制变量批；给了它就不用 --plan")
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)

    recs = []
    for line in (MAT / "manifest.jsonl").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        if r["路径"].startswith("references/"):
            continue                      # 档样库里的短段不入匿名稿批，避免与整章不可比
        r["真身路径"] = MAT.parent / r["路径"]
        if not r["真身路径"].exists():
            print("!! 真身缺失，跳过：%s" % r["路径"])
            continue
        recs.append(r)

    rnd = random.Random(SEED + int(args.round))
    if args.ids:
        # 控制变量批：稿号由调用者指定，仍按同一种子打乱先后，避免默认顺序带偏
        want = [s.strip() for s in args.ids.split(",") if s.strip()]
        byid = {r["id"]: r for r in recs}
        missing = [i for i in want if i not in byid]
        if missing:
            print("!! 指定稿号不存在：%s" % "、".join(missing))
            sys.exit(1)
        picked = [byid[i] for i in want]
        rnd.shuffle(picked)
    elif args.plan:
        # 分层抽样：保证四档都进批，这是跨档排序能测出来的前提
        picked = []
        for item in args.plan.split(","):
            gear, _, k = item.partition(":")
            pool = [r for r in recs if r["档位"] == gear]
            rnd.shuffle(pool)
            picked.extend(pool[: int(k)])
    else:
        rnd.shuffle(recs)
        picked = recs[: args.n]

    mapping = {"轮次": args.round, "种子": SEED + int(args.round), "对应": {}}
    for i, r in enumerate(picked, 1):
        code = "稿%s" % (CN[i - 1] if i <= 10 else str(i))
        text = r["真身路径"].read_text(encoding="utf-8").strip()
        (OUT / ("%s.md" % code)).write_text(text, encoding="utf-8")
        mapping["对应"][code] = {"id": r["id"], "档位": r["档位"], "来源": r["来源"], "路径": r["路径"]}
        print("  %s  ←  %s（%s｜%s）" % (code, r["id"], r["档位"], r["来源"]))
    (SK / "跑批" / "映射表-封存.json").write_text(
        json.dumps(mapping, ensure_ascii=False, indent=2), encoding="utf-8")
    print("\n匿名稿 %d 份 → %s" % (len(picked), OUT))
    print("映射表已封存：跑批/映射表-封存.json（判完才开）")


if __name__ == "__main__":
    main()
