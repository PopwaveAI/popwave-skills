# -*- coding: utf-8 -*-
"""形态与词表计数：**只报数，不下判**。结果进判决书附录，不进排序与分档。"""
import argparse
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
SK = Path(r"d:\popwave-skills\新流程探索\网文编辑")
IN = SK / "scripts" / "输入"
HAN = re.compile(r"[\u4e00-\u9fff]")
SENT = re.compile(r"[。！？…]+")
LEVEL1 = "赋能 闭环 抓手 底座 全链路 打通 拉齐 飞轮 矩阵 沉淀 破局 突围 重构 重塑 王炸 封神 天花板".split()
LEVEL2 = "深耕 聚焦 助力 打造 引领 全方位 多维度 高质量 沉浸式 一站式 底层逻辑 顶层设计 降本增效 提质增效 数智化".split()
TRANS = "此外 另外 值得注意的是 值得一提的是 毫无疑问 不言而喻 众所周知 不可否认 与此同时 事实上 总的来说 综上所述 不难发现 由此可见".split()
PATTERNS = ["不是……而是……", "虽然……但是……", "不仅……而且……"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--round", default="1")
    args = ap.parse_args()
    out_dir = SK / "迭代记录" / ("第%s轮" % args.round)
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = ["# 形态与词表计数（只报数）· 第%s轮\n" % args.round,
            "> 这一栏不是判据。三轮实测的教训：拿统计代替阅读会得出反结论。\n",
            "| 稿 | 汉字 | 段数 | 平均段长 | 句数 | 平均句长 | 短句(<10字)占比 | 破折号 | 半角引号 | markdown残留 | 助手话尾 | 一级词 | 二级词 | 过渡词 | 禁句式 |",
            "|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|"]
    for p in sorted(IN.glob("稿*.md")):
        t = p.read_text(encoding="utf-8")
        paras = [x for x in re.split(r"\n\s*\n", t) if x.strip()]
        sents = [s for s in SENT.split(t) if s.strip()]
        n = len(HAN.findall(t))
        slens = [len(HAN.findall(s)) for s in sents] or [0]
        short = sum(1 for x in slens if x < 10) / len(slens) * 100
        rows.append("| %s | %d | %d | %.1f | %d | %.1f | %.1f%% | %d | %d | %d | %d | %d | %d | %d | %d |" % (
            p.stem, n, len(paras), n / max(len(paras), 1), len(sents), n / max(len(sents), 1), short,
            t.count("—"), len(re.findall(r"[\u4e00-\u9fff]\"", t)),
            len(re.findall(r"^\s*[#*|>`-]", t, re.M)),
            len(re.findall(r"(好的|希望|以上|如需|要不要我|需要我)", t)),
            sum(t.count(w) for w in LEVEL1), sum(t.count(w) for w in LEVEL2),
            sum(t.count(w) for w in TRANS), sum(t.count(w) for w in PATTERNS)))
    (out_dir / "形态计数.md").write_text("\n".join(rows) + "\n", encoding="utf-8")
    print("已写入 %s" % (out_dir / "形态计数.md"))


if __name__ == "__main__":
    main()
