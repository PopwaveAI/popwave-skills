# -*- coding: utf-8 -*-
"""
流派词激活力探针（第二轮·V3 深化）

问什么：给一个明显的流派词（武侠／克苏鲁／规则怪谈），是否激活模型内置的该类文体与桥段？
        用一个生造流派词作关键对照——若生造词也产出成体系文体，说明"激活"部分来自听指令即兴编造；
        若生造词明显空洞、无专属词汇体系，则真流派词确实带内置分布。

控制：同一情境（不含任何流派词）、同一句式，只换流派词槽位。每条件 1 稿。
      模型 deepseek-flash，temperature 1.0，top_p 1.0，零 system message。

用法：
    python run_genre_probe.py --dry-run
    python run_genre_probe.py
"""

import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

BASE = Path(__file__).resolve().parent
ENV_PATH = BASE / ".env"
IN_DIR = BASE / "输入" / "流派词探针"
OUT_DIR = BASE / "输出" / "流派词探针"
MANIFEST = OUT_DIR / "manifest.jsonl"

# ---- 固定情境：中性，不含任何流派词 ----
PREMISE = (
    "一个人回到十年前的旧居。房子早已空了，房东换过三任。"
    "他在二楼朝北的屋子里找到一只铁盒，里面是当年没寄出的信。"
    "当晚他决定住下，把信一封封重读。"
)

# (代号, 标签, 提示词前缀, 文件名)
CONDITIONS = [
    ("C0", "无线索词（对照）", "写一段小说第一章。", "C0-无线索词.md"),
    ("C1", "武侠", "写一段武侠小说第一章。", "C1-武侠.md"),
    ("C2", "克苏鲁恐怖", "写一段克苏鲁恐怖小说第一章。", "C2-克苏鲁恐怖.md"),
    ("C3", "规则怪谈", "写一段规则怪谈小说第一章。", "C3-规则怪谈.md"),
    ("C4", "生造流派词：琉璃道（对照）", "写一段“琉璃道”流派小说第一章。", "C4-生造流派词-琉璃道.md"),
]

HAN = __import__("re").compile(r"[\u4e00-\u9fff]")


def build_prompt(prefix: str) -> str:
    return prefix + "\n\n" + PREMISE


def load_env(path: Path) -> dict:
    if not path.exists():
        sys.exit("找不到 .env")
    cfg = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if not s or s.startswith("#") or "=" not in s:
            continue
        k, v = s.split("=", 1)
        cfg[k.strip()] = v.strip()
    return cfg


def call_api(cfg: dict, model: str, prompt: str, timeout: int = 600) -> dict:
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": float(cfg.get("TEMPERATURE", "1.0")),
        "top_p": float(cfg.get("TOP_P", "1.0")),
        "max_tokens": int(cfg.get("MAX_TOKENS", "8000")),
        "stream": False,
    }
    req = urllib.request.Request(
        cfg["BASE_URL"].rstrip("/") + "/chat/completions",
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
        return {"ok": False, "error": "HTTP %s: %s" % (e.code, e.read().decode("utf-8", "replace")[:400]),
                "seconds": round(time.time() - t0, 1)}
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "error": repr(e), "seconds": round(time.time() - t0, 1)}
    msg = (body.get("choices") or [{}])[0].get("message") or {}
    return {
        "ok": True,
        "seconds": round(time.time() - t0, 1),
        "text": msg.get("content") or "",
        "reasoning": msg.get("reasoning_content") or "",
        "finish_reason": (body.get("choices") or [{}])[0].get("finish_reason"),
        "usage": body.get("usage") or {},
    }


def clean_form(text: str) -> str:
    import re
    t = text
    t = re.sub(r"^```[a-zA-Z]*\s*$", "", t, flags=re.M)
    t = t.replace("**", "").replace("__", "")
    t = re.sub(r"^#{1,6}\s*", "", t, flags=re.M)
    t = re.sub(r"^(---|\*\*\*)\s*$", "", t, flags=re.M)
    t = t.replace("...", "\u2026\u2026")
    out, open_q = [], True
    for ch in t:
        if ch == '"':
            out.append("\u201c" if open_q else "\u201d")
            open_q = not open_q
        else:
            out.append(ch)
    t = "".join(out)
    return re.sub(r"\n{3,}", "\n\n", t).strip()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default=None)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-skip", action="store_true")
    args = ap.parse_args()

    cfg = load_env(ENV_PATH)
    model = args.model or (cfg.get("MODELS", "deepseek-flash").split(",")[0].strip())

    IN_DIR.mkdir(parents=True, exist_ok=True)
    for code, label, prefix, fname in CONDITIONS:
        (IN_DIR / fname).write_text(build_prompt(prefix), encoding="utf-8")
    print("输入已归档：%s（%d 份）" % (IN_DIR, len(CONDITIONS)))
    print("模型：%s   温度：%s   零 system message" % (model, cfg.get("TEMPERATURE", "1.0")))
    if args.dry_run:
        print("\n计划：")
        for code, label, prefix, fname in CONDITIONS:
            print("  %s  %-22s %s" % (code, label, prefix))
        return

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ok = fail = 0
    for code, label, prefix, fname in CONDITIONS:
        raw_p = OUT_DIR / ("%s__raw.txt" % code)
        if raw_p.exists() and not args.no_skip:
            print("[skip] %s %s" % (code, label))
            continue
        prompt = build_prompt(prefix)
        res = call_api(cfg, model, prompt)
        rec = {
            "at": time.strftime("%Y-%m-%d %H:%M:%S"), "model": model,
            "code": code, "label": label, "prompt": prompt,
            "temperature": float(cfg.get("TEMPERATURE", "1.0")),
            "max_tokens": int(cfg.get("MAX_TOKENS", "8000")),
        }
        if not res["ok"]:
            rec.update({"status": "fail", "error": res["error"], "seconds": res["seconds"]})
            with MANIFEST.open("a", encoding="utf-8") as f:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            fail += 1
            print("[FAIL] %s %s  %s" % (code, label, res["error"]))
            continue
        text = res["text"]
        raw_p.write_text(text, encoding="utf-8")
        (OUT_DIR / ("%s__clean.txt" % code)).write_text(clean_form(text), encoding="utf-8")
        if res["reasoning"]:
            (OUT_DIR / ("%s__thinking.txt" % code)).write_text(res["reasoning"], encoding="utf-8")
        han = len(HAN.findall(text))
        paras = len([l for l in text.splitlines() if l.strip()])
        rec.update({
            "status": "ok", "seconds": res["seconds"], "finish_reason": res["finish_reason"],
            "usage": res["usage"], "han": han, "paragraphs": paras,
            "avg_para": round(han / paras, 1) if paras else 0,
        })
        with MANIFEST.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        ok += 1
        print("[ok  ] %s %-22s %ss  汉字%d  段%d  平均段长%s  结尾=%s"
              % (code, label, res["seconds"], han, paras, rec["avg_para"], res["finish_reason"]))
    print("\n完成：成功 %d，失败 %d" % (ok, fail))
    print("产出：", OUT_DIR)


if __name__ == "__main__":
    main()
