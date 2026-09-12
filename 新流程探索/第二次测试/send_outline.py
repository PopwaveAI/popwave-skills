# -*- coding: utf-8 -*-
"""
把一份章纲原样发给 API，不加任何指令、不发 system prompt，看返回什么。

用法：
    python send_outline.py                # 默认发 输入/ch001-章纲-黄金重构版.md，跑 3 稿
    python send_outline.py --runs 5
    python send_outline.py --file 输入/别的章纲.md
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.request
from pathlib import Path

BASE = Path(__file__).resolve().parent
ENV = BASE / ".env"


def load_env(path: Path) -> dict:
    cfg = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        cfg[k.strip()] = v.strip()
    return cfg


def call(cfg, content, timeout=300):
    payload = {
        "model": cfg.get("MODELS", "deepseek-flash").split(",")[0].strip(),
        "messages": [{"role": "user", "content": content}],
        "temperature": float(cfg.get("TEMPERATURE", 1.0)),
        "max_tokens": int(cfg.get("MAX_TOKENS", 8000)),
        "top_p": float(cfg.get("TOP_P", 1.0)),
    }
    req = urllib.request.Request(
        cfg["BASE_URL"].rstrip("/") + "/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + cfg["DEEPSEEK_API_KEY"],
        },
        method="POST",
    )
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=timeout) as r:
        body = json.loads(r.read().decode("utf-8"))
    return body, time.time() - t0


def split_think(text):
    """把  thinking...<｜end▁of▁thinking｜> 或独立思考字段剥出来。"""
    m = re.search(r"<think(?:ing)?>(.*?)</think(?:ing)?>", text, re.S)
    if m:
        return (text[: m.start()] + text[m.end():]).strip(), m.group(1).strip()
    return text.strip(), ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", default="输入/ch001-章纲-黄金重构版.md")
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--outdir", default="输出/章纲直出")
    args = ap.parse_args()

    cfg = load_env(ENV)
    src = BASE / args.file
    content = src.read_text(encoding="utf-8")
    outdir = BASE / args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("章纲原样直发 · 零指令 · 零 system prompt")
    print("模型:", cfg.get("MODELS"))
    print("输入:", args.file, f"({len(content)} 字符)")
    print("=" * 60)

    stem = src.stem
    rows = []
    for i in range(1, args.runs + 1):
        print(f"\n--- 第 {i:02d} 稿 ---")
        try:
            body, dt = call(cfg, content)
        except Exception as e:
            print("失败:", e)
            rows.append({"run": i, "error": str(e)})
            continue

        msg = body["choices"][0]["message"]
        text = msg.get("content") or ""
        thinking = msg.get("reasoning_content") or ""
        text, inline = split_think(text)
        thinking = thinking or inline
        finish = body["choices"][0].get("finish_reason")
        u = body.get("usage", {})

        han = len(re.findall(r"[\u4e00-\u9fff]", text))
        para = len([p for p in text.split("\n") if p.strip()])
        print(f"耗时 {dt:.1f}s | finish={finish} | 汉字 {han} | 段 {para}")
        print(f"tokens: completion={u.get('completion_tokens')} "
              f"reasoning={u.get('completion_tokens_details', {}).get('reasoning_tokens')}")

        base = outdir / f"{stem}__r{i:02d}"
        (base.parent / (base.name + "__raw.txt")).write_text(text, encoding="utf-8")
        if thinking:
            (base.parent / (base.name + "__thinking.txt")).write_text(thinking, encoding="utf-8")
        rows.append({
            "run": i, "file": str(src), "elapsed": round(dt, 1), "finish": finish,
            "han": han, "paras": para, "usage": u,
        })

    with (outdir / "manifest.jsonl").open("a", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print("\n" + "=" * 60)
    ok = [r for r in rows if "error" not in r]
    if ok:
        print("完成", len(ok), "稿 | 平均", round(sum(r["elapsed"] for r in ok) / len(ok), 1), "s")
        print("汉字:", [r["han"] for r in ok])
    print("输出目录:", outdir)


if __name__ == "__main__":
    sys.exit(main())
