# -*- coding: utf-8 -*-
"""
把每个赛道文件夹里的多份 txt 合成一个 md，方便直接读。

    python merge_md.py                # 全部模型、全部赛道
    python merge_md.py --model deepseek-flash
    python merge_md.py --no-thinking  # 不把思考过程放进 md（文件会小很多）

产出：输出/{模型}/{赛道}/{赛道}.md
      结构 = 总览表 + 逐稿正文（正文用 clean 版，更好读）+ 折叠的思考过程
      txt 原件不动，留着做原始存档。
"""

import argparse
import json
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent
OUT = BASE / "输出"
MANIFEST = OUT / "manifest.jsonl"


def load_manifest():
    idx = {}
    if not MANIFEST.exists():
        return idx
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        r = json.loads(line)
        if r.get("status") == "ok":
            idx[(r["model"], r["genre"], r["run"])] = r
    return idx


def read(p: Path) -> str:
    if not p.exists():
        return ""
    return p.read_text(encoding="utf-8").strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model")
    ap.add_argument("--no-thinking", action="store_true")
    ap.add_argument("--clean-txt", action="store_true",
                    help="md 写好后删掉该文件夹里的 txt（只删合并成功的）")
    a = ap.parse_args()

    if not OUT.exists():
        raise SystemExit("还没有 输出 目录，先跑 run_test.py")

    man = load_manifest()
    made = []

    for mdir in sorted(p for p in OUT.iterdir() if p.is_dir()):
        if a.model and mdir.name != a.model:
            continue
        for gdir in sorted(p for p in mdir.iterdir() if p.is_dir()):
            runs = []
            for raw in sorted(gdir.glob("*__raw.txt")):
                mm = re.search(r"__r(\d+)__raw\.txt$", raw.name)
                if not mm:
                    continue
                n = int(mm.group(1))
                stem = raw.name.replace("__raw.txt", "")
                body = read(gdir / (stem + "__clean.txt")) or read(raw)
                thinking = "" if a.no_thinking else read(gdir / (stem + "__thinking.txt"))
                runs.append({"n": n, "body": body, "thinking": thinking,
                             "meta": man.get((mdir.name, gdir.name, n), {})})
            if not runs:
                continue
            runs.sort(key=lambda x: x["n"])

            L = []
            L.append("# %s · %s" % (mdir.name, gdir.name))
            L.append("")
            L.append("> 一键直出测试稿，零上下文。每稿都是同一个 prompt："
                     "「没有任何前提，为我写一段%s小说第一章」" % gdir.name)
            L.append("")
            L.append("## 总览")
            L.append("")
            L.append("| 稿 | 汉字 | 耗时 | 破折号 | markdown | 半角引号 | 助手话尾 |")
            L.append("|:--|--:|--:|--:|--:|--:|:--|")
            for r in runs:
                f = r["meta"].get("form", {})
                md = (f.get("md_bold", 0) + f.get("md_heading", 0)
                      + f.get("md_hr", 0) + f.get("md_list", 0))
                L.append("| r%02d | %d | %ss | %d | %d | %d | %s |" % (
                    r["n"], f.get("han", 0), r["meta"].get("seconds", "-"),
                    f.get("em_dash", 0), md, f.get("half_width_quote", 0),
                    "是" if r["meta"].get("tail_chatter") else ""))
            L.append("")

            for r in runs:
                L.append("---")
                L.append("")
                L.append("## 第 %02d 稿" % r["n"])
                L.append("")
                if r["body"]:
                    L.append(r["body"])
                else:
                    L.append("（本次调用没有返回正文，原因见 manifest.jsonl）")
                L.append("")
                if r["thinking"]:
                    L.append("<details>")
                    L.append("<summary>思考过程</summary>")
                    L.append("")
                    L.append(r["thinking"])
                    L.append("")
                    L.append("</details>")
                    L.append("")

            target = gdir / (gdir.name + ".md")
            target.write_text("\n".join(L) + "\n", encoding="utf-8")

            # 只有 md 确实写出来了、稿数对得上，才允许删原件
            txts = sorted(gdir.glob("*.txt"))
            removed = 0
            if a.clean_txt and target.exists() and target.stat().st_size > 0:
                headings = target.read_text(encoding="utf-8").count("\n## 第 ")
                if headings == len(runs):
                    for t in txts:
                        t.unlink()
                        removed += 1
                else:
                    print("!! 跳过清理 %s：md 里只有 %d 个稿标题，txt 有 %d 个"
                          % (gdir.name, headings, len(txts)))
            made.append((target, len(runs), removed))

    for t, n, removed in made:
        extra = "，清理 txt %d 个" % removed if removed else ""
        print("生成 %s  （%d 稿%s）" % (t.relative_to(BASE), n, extra))
    print("\n共 %d 个文件" % len(made))


if __name__ == "__main__":
    main()
