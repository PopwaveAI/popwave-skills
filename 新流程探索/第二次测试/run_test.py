# -*- coding: utf-8 -*-
"""
第二次测试 · 多赛道零上下文直出

测什么：不给任何项目上下文，只发一句 prompt，让模型直接写某个赛道的小说第一章。
         目的是量出模型"裸直出"的文笔自然度水位，以及各赛道之间的差异。

怎么跑：
    python run_test.py --smoke          # 先冒烟：1 次最便宜的调用，确认 key 和模型可用
    python run_test.py --dry-run        # 只看计划，不花钱
    python run_test.py                  # 按 .env 跑全部赛道
    python run_test.py --genres 武侠,克苏鲁航海 --runs 5   # 临时覆盖

产出：
    输出/manifest.jsonl                 每次调用的参数、耗时、token 用量、文本形态指标
    输出/{模型}/{赛道}/{赛道}__r{n}__raw.txt    原始输出，一字未改
    输出/{模型}/{赛道}/{赛道}__r{n}__clean.txt  只做机械形态清理，不动内容

形态指标为什么重要：上一轮测试里，一份直出稿混进了 64 个半角引号和 8 处 markdown 加粗，
                    这种形态污染会把"文笔"的判断带偏。所以每稿都自动量一遍，评之前先筛。
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

BASE = Path(__file__).resolve().parent
ENV_PATH = BASE / ".env"
OUT_DIR = BASE / "输出"
MANIFEST = OUT_DIR / "manifest.jsonl"


# ---------------------------------------------------------------- 配置

def load_env(path: Path) -> dict:
    if not path.exists():
        sys.exit("找不到 .env，先把 .env.example 复制成 .env 并填好 key")
    cfg = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if not s or s.startswith("#") or "=" not in s:
            continue
        k, v = s.split("=", 1)
        cfg[k.strip()] = v.strip()
    return cfg


def as_list(cfg: dict, key: str, default: str = "") -> list:
    raw = cfg.get(key, default)
    return [x.strip() for x in raw.split(",") if x.strip()]


# ---------------------------------------------------------------- 文本形态指标

HAN = re.compile(r"[\u4e00-\u9fff]")


def form_metrics(text: str) -> dict:
    return {
        "chars": len(text),
        "han": len(HAN.findall(text)),
        "half_width_quote": text.count('"'),
        "full_width_quote": text.count("\u201c"),
        "em_dash": text.count("\u2014"),
        "ellipsis_raw": text.count("..."),
        "md_bold": text.count("**"),
        "md_heading": len([l for l in text.splitlines() if l.lstrip().startswith("#")]),
        "md_hr": len([l for l in text.splitlines() if l.strip() in ("---", "***")]),
        "md_list": len([l for l in text.splitlines() if l.lstrip()[:2] in ("- ", "* ")]),
        "paragraphs": len([l for l in text.splitlines() if l.strip()]),
    }


def tail_looks_like_chatter(text: str) -> bool:
    """结尾像不像模型的助手话术（要接着往下写吗 / 这一章给你开个头 之类）。"""
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    if not lines:
        return False
    last = lines[-1]
    if re.fullmatch(r"[（(].{0,20}[)）]", last):      # （第一章 完）这类是收束标记，不算话术
        return False
    if len(last) > 150:
        return False
    return ("。" not in last) or bool(re.search(r"(可以|建议|要不要|接着|继续|告诉我|随时|希望)", last))


# ---------------------------------------------------------------- 机械形态清理

def clean_form(text: str) -> str:
    """只清形态，不动内容。留着 raw 版做对照，这版用于阅读和评分。"""
    t = text
    t = re.sub(r"^```[a-zA-Z]*\s*$", "", t, flags=re.M)          # 代码围栏
    t = t.replace("**", "").replace("__", "")                     # 加粗
    t = re.sub(r"^#{1,6}\s*", "", t, flags=re.M)                  # 标题井号
    t = re.sub(r"^(---|\*\*\*)\s*$", "", t, flags=re.M)           # 分割线
    t = t.replace("...", "\u2026\u2026")                          # 省略号归一
    # 半角引号成对转全角
    out, open_q = [], True
    for ch in t:
        if ch == '"':
            out.append("\u201c" if open_q else "\u201d")
            open_q = not open_q
        else:
            out.append(ch)
    t = "".join(out)
    t = re.sub(r"\n{3,}", "\n\n", t).strip()
    return t


# ---------------------------------------------------------------- 调用

def build_messages(cfg: dict, genre: str) -> list:
    tpl = cfg.get("USER_PROMPT_TEMPLATE", "没有任何前提，为我写一段{genre}小说第一章")
    msgs = []
    if cfg.get("SEND_SYSTEM_PROMPT", "0") == "1":
        sp = cfg.get("SYSTEM_PROMPT", "").strip()
        if sp:
            msgs.append({"role": "system", "content": sp})
    msgs.append({"role": "user", "content": tpl.replace("{genre}", genre)})
    return msgs


def call_api(cfg: dict, model: str, messages: list, timeout: int = 600) -> dict:
    url = cfg["BASE_URL"].rstrip("/") + "/chat/completions"
    payload = {
        "model": model,
        "messages": messages,
        "temperature": float(cfg.get("TEMPERATURE", "1.0")),
        "top_p": float(cfg.get("TOP_P", "1.0")),
        "max_tokens": int(cfg.get("MAX_TOKENS", "8000")),
        "stream": False,
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + cfg["DEEPSEEK_API_KEY"],
        },
        method="POST",
    )
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:500]
        return {"ok": False, "error": "HTTP %s: %s" % (e.code, detail), "seconds": time.time() - t0}
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "error": repr(e), "seconds": time.time() - t0}

    msg = (body.get("choices") or [{}])[0].get("message") or {}
    return {
        "ok": True,
        "seconds": round(time.time() - t0, 1),
        "text": msg.get("content") or "",
        "reasoning": msg.get("reasoning_content") or "",
        "finish_reason": (body.get("choices") or [{}])[0].get("finish_reason"),
        "usage": body.get("usage") or {},
        "model_returned": body.get("model"),
    }


# ---------------------------------------------------------------- 主流程

def one_task(cfg: dict, model: str, genre: str, idx: int, runs: int, skip: bool) -> dict:
    gdir = OUT_DIR / model / genre
    stem = "%s__r%02d" % (genre, idx)
    raw_p = gdir / (stem + "__raw.txt")
    if skip and raw_p.exists():
        return {"status": "skip", "genre": genre, "model": model, "idx": idx}

    messages = build_messages(cfg, genre)
    res = call_api(cfg, model, messages)
    rec = {
        "at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "model": model,
        "genre": genre,
        "run": idx,
        "prompt": messages[-1]["content"],
        "system_prompt_sent": cfg.get("SEND_SYSTEM_PROMPT", "0") == "1",
        "temperature": float(cfg.get("TEMPERATURE", "1.0")),
        "top_p": float(cfg.get("TOP_P", "1.0")),
        "max_tokens": int(cfg.get("MAX_TOKENS", "8000")),
    }
    if not res["ok"]:
        rec["status"] = "fail"
        rec["error"] = res["error"]
        rec["seconds"] = res["seconds"]
        return rec

    text = res["text"]
    gdir.mkdir(parents=True, exist_ok=True)
    raw_p.write_text(text, encoding="utf-8")
    (gdir / (stem + "__clean.txt")).write_text(clean_form(text), encoding="utf-8")
    if res["reasoning"]:
        (gdir / (stem + "__thinking.txt")).write_text(res["reasoning"], encoding="utf-8")

    rec.update({
        "status": "ok",
        "seconds": res["seconds"],
        "finish_reason": res["finish_reason"],
        "usage": res["usage"],
        "form": form_metrics(text),
        "tail_chatter": tail_looks_like_chatter(text),
        "has_thinking": bool(res["reasoning"]),
        "file": str(raw_p.relative_to(BASE)),
    })
    return rec


def append_manifest(rec: dict) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with MANIFEST.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--genres", help="覆盖 .env 里的赛道清单，逗号分隔")
    ap.add_argument("--models", help="覆盖 .env 里的模型清单，逗号分隔")
    ap.add_argument("--runs", type=int, help="覆盖每赛道稿数")
    ap.add_argument("--concurrency", type=int, default=2)
    ap.add_argument("--dry-run", action="store_true", help="只打印计划，不调用")
    ap.add_argument("--smoke", action="store_true", help="只跑 1 次最便宜的调用")
    ap.add_argument("--no-skip", action="store_true", help="忽略已有文件，全部重跑")
    args = ap.parse_args()

    cfg = load_env(ENV_PATH)
    models = [args.models] if args.models else as_list(cfg, "MODELS", "deepseek-chat")
    genres = [args.genres] if args.genres else as_list(cfg, "GENRES")
    runs = args.runs or int(cfg.get("RUNS_PER_GENRE", "1"))
    skip = (cfg.get("SKIP_EXISTING", "1") == "1") and not args.no_skip

    if args.smoke:
        models, genres, runs = models[:1], ["武侠"], 1

    if not models or not genres:
        sys.exit("MODELS 或 GENRES 是空的，检查 .env")

    total = len(models) * len(genres) * runs
    print("模型  :", ", ".join(models))
    print("赛道  :", ", ".join(genres), "(共 %d 个)" % len(genres))
    print("每赛道:", runs, "稿")
    print("计划  :", total, "次调用")
    print("system:", "发送 SYSTEM_PROMPT" if cfg.get("SEND_SYSTEM_PROMPT") == "1" else "不发送（零上下文）")
    print("输出  :", OUT_DIR)
    if args.dry_run:
        return

    tasks = [(m, g, i) for m in models for g in genres for i in range(1, runs + 1)]
    ok = fail = skipped = 0
    with ThreadPoolExecutor(max_workers=max(1, args.concurrency)) as ex:
        futs = [ex.submit(one_task, cfg, m, g, i, runs, skip) for (m, g, i) in tasks]
        for f in as_completed(futs):
            rec = f.result()
            if rec.get("status") == "skip":
                skipped += 1
                print("[skip] %s / %s r%02d" % (rec["model"], rec["genre"], rec["idx"]))
                continue
            append_manifest(rec)
            if rec.get("status") == "ok":
                ok += 1
                fm = rec["form"]
                print("[ok  ] %s / %s r%02d  %ss  汉字%d  半角引号%d  markdown%d%s"
                      % (rec["model"], rec["genre"], rec["run"], rec["seconds"],
                         fm["han"], fm["half_width_quote"], fm["md_bold"] + fm["md_heading"] + fm["md_hr"],
                         "  结尾像助手话术" if rec["tail_chatter"] else ""))
            else:
                fail += 1
                print("[FAIL] %s / %s r%02d  %s" % (rec["model"], rec["genre"], rec["run"], rec["error"]))

    print("\n完成：成功 %d，失败 %d，跳过 %d" % (ok, fail, skipped))
    print("清单：", MANIFEST)


if __name__ == "__main__":
    main()
