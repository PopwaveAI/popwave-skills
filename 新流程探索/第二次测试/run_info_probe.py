# -*- coding: utf-8 -*-
"""
两槽位范式探针：流派词 ＋ 本章要写什么信息

问什么：这两个槽位是否构成有效组合——流派词管文体与语料（C 组已证），信息槽管控制力。

四个条件（同情境、同流派词）：
  D1 武侠 ＋ 本章信息（4 条事实，散文）
  D2 武侠 ＋ 本章信息（7 条事实，散文）
  D3 武侠 ＋ 本章信息（7 条事实，条目式）← 与 D2 只差输入形态，验 P4
  D4 无线索词 ＋ 本章信息（同 D2 的散文）← 关键对照：拿掉流派词，看信息槽能否独立撑住

基线 D0 = C1（武侠，不加信息），上一轮已有，不重跑。

用法：
    python run_info_probe.py --dry-run
    python run_info_probe.py
"""

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

BASE = Path(__file__).resolve().parent
ENV_PATH = BASE / ".env"
IN_DIR = BASE / "输入" / "两槽位探针"
OUT_DIR = BASE / "输出" / "两槽位探针"
MANIFEST = OUT_DIR / "manifest.jsonl"

PREMISE = (
    "一个人回到十年前的旧居。房子早已空了，房东换过三任。"
    "他在二楼朝北的屋子里找到一只铁盒，里面是当年没寄出的信。"
    "当晚他决定住下，把信一封封重读。"
)

# 七条本章内容事实（不含答案，不含反转解释）
FACTS = [
    "主角姓赵，十年前离开这座城，回来时已经过了三十",
    "院子是师父留下的，师父三年前过世，房子空了三年",
    "铁盒里是七封信，信封上的收件人写的都是他自己，笔迹却是师父的",
    "前六封都只是寻常叮嘱",
    "第七封没有封口，里面只有半张地图",
    "当晚有人敲门，来人自称是师父生前的旧识，说这院子他不能住",
    "这一章停在主角把半张地图摊在桌上，又听见院门外有脚步声",
]
INFO_PROSE_4 = (
    "这一章要写到：主角姓赵，十年前离开这座城，回来时已经过了三十；"
    "院子是师父留下的，师父三年前过世；"
    "铁盒里是七封信，信封上的收件人写的都是他自己，笔迹却是师父的；"
    "当晚有人来敲门。写到有人敲门为止，先不要交代来人是谁。"
)
INFO_PROSE_7 = (
    "这一章要写到：主角姓赵，十年前离开这座城，回来时已经过了三十；"
    "院子是师父留下的，师父三年前过世，房子空了三年；"
    "铁盒里是七封信，信封上的收件人写的都是他自己，笔迹却是师父的；"
    "前六封都只是寻常叮嘱，第七封没有封口，里面只有半张地图；"
    "当晚有人敲门，来人自称是师父生前的旧识，说这院子他不能住；"
    "这一章停在主角把半张地图摊在桌上，又听见院门外有脚步声。"
    "先不要交代来人是谁，也不要解释那半张地图指向哪里。"
)
INFO_ITEM_7 = (
    "这一章要写的硬事实：\n"
    "- 主角姓赵，十年前离开这座城，回来时已经过了三十\n"
    "- 院子是师父留下的，师父三年前过世，房子空了三年\n"
    "- 铁盒里是七封信，收件人写的都是他自己，笔迹却是师父的\n"
    "- 前六封都只是寻常叮嘱\n"
    "- 第七封没有封口，里面只有半张地图\n"
    "- 当晚有人敲门，来人自称是师父生前的旧识，说这院子他不能住\n"
    "- 停在主角把半张地图摊在桌上，又听见院门外有脚步声\n"
    "先不要交代来人是谁，也不要解释那半张地图指向哪里。"
)

CONDITIONS = [
    ("D1", "武侠＋信息4条（散文）", "武侠", INFO_PROSE_4),
    ("D2", "武侠＋信息7条（散文）", "武侠", INFO_PROSE_7),
    ("D3", "武侠＋信息7条（条目式）", "武侠", INFO_ITEM_7),
    ("D4", "无线索词＋信息7条（散文）", None, INFO_PROSE_7),
]

# 硬事实关键词（每条一组，命中任一算兑现）
FACT_KEYS = [
    (["赵"], "姓赵"),
    (["师父"], "师父"),
    (["十年"], "十年前"),
    (["七封", "7封", "七封信"], "七封信"),
    (["叮嘱"], "前六封是叮嘱"),
    (["地图"], "半张地图"),
    (["敲门", "叩门"], "有人敲门"),
    (["不能住", "别住", "搬走", "住不得", "住不"], "说了不能住"),
    (["脚步声"], "章末脚步声"),
]

HAN = re.compile(r"[\u4e00-\u9fff]")


def build_prompt(genre, info):
    head = "写一段%s小说第一章。" % genre if genre else "写一段小说第一章。"
    return head + "\n\n" + PREMISE + "\n\n" + info


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


def call_api(cfg, model, prompt, timeout=600):
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
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + cfg["DEEPSEEK_API_KEY"]},
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
    return {"ok": True, "seconds": round(time.time() - t0, 1),
            "text": msg.get("content") or "", "reasoning": msg.get("reasoning_content") or "",
            "finish_reason": (body.get("choices") or [{}])[0].get("finish_reason"),
            "usage": body.get("usage") or {}}


def clean_form(text: str) -> str:
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
    return re.sub(r"\n{3,}", "\n\n", "".join(out)).strip()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default=None)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-skip", action="store_true")
    args = ap.parse_args()

    cfg = load_env(ENV_PATH)
    model = args.model or (cfg.get("MODELS", "deepseek-flash").split(",")[0].strip())

    IN_DIR.mkdir(parents=True, exist_ok=True)
    for code, label, genre, info in CONDITIONS:
        (IN_DIR / ("%s-%s.md" % (code, label))).write_text(build_prompt(genre, info), encoding="utf-8")
    print("输入已归档：%s（%d 份）" % (IN_DIR, len(CONDITIONS)))
    print("模型：%s  温度：%s  零 system message" % (model, cfg.get("TEMPERATURE", "1.0")))
    if args.dry_run:
        for code, label, genre, info in CONDITIONS:
            print("  %s  %-24s 流派词=%-6s 信息=%d 字" % (code, label, genre or "无", len(info)))
        return

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ok = fail = 0
    for code, label, genre, info in CONDITIONS:
        raw_p = OUT_DIR / ("%s__raw.txt" % code)
        if raw_p.exists() and not args.no_skip:
            print("[skip] %s %s" % (code, label)); continue
        prompt = build_prompt(genre, info)
        res = call_api(cfg, model, prompt)
        rec = {"at": time.strftime("%Y-%m-%d %H:%M:%S"), "model": model, "code": code,
               "label": label, "genre_word": genre, "prompt": prompt,
               "temperature": float(cfg.get("TEMPERATURE", "1.0"))}
        if not res["ok"]:
            rec.update({"status": "fail", "error": res["error"], "seconds": res["seconds"]})
            with MANIFEST.open("a", encoding="utf-8") as f:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            fail += 1; print("[FAIL] %s %s  %s" % (code, label, res["error"])); continue
        text = res["text"]
        body = re.sub(r"\s+", "", text)
        hit = [(n, any(k in body for k in keys)) for keys, n in FACT_KEYS]
        landed = hit[-1][1]
        han = len(HAN.findall(text))
        paras = len([l for l in text.splitlines() if l.strip()])
        raw_p.write_text(text, encoding="utf-8")
        (OUT_DIR / ("%s__clean.txt" % code)).write_text(clean_form(text), encoding="utf-8")
        if res["reasoning"]:
            (OUT_DIR / ("%s__thinking.txt" % code)).write_text(res["reasoning"], encoding="utf-8")
        rec.update({"status": "ok", "seconds": res["seconds"], "finish_reason": res["finish_reason"],
                    "usage": res["usage"], "han": han, "paragraphs": paras,
                    "avg_para": round(han / paras, 1) if paras else 0,
                    "facts_hit": [n for n, b in hit if b], "facts_miss": [n for n, b in hit if not b],
                    "facts_rate": "%d/%d" % (sum(1 for _, b in hit if b), len(hit)),
                    "landing_hit": landed})
        with MANIFEST.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        ok += 1
        print("[ok  ] %s %-24s %ss  汉字%d 段%d 均段%s  硬事实%s  落点命中=%s"
              % (code, label, res["seconds"], han, paras, rec["avg_para"], rec["facts_rate"], landed))
        if rec["facts_miss"]:
            print("        未兑现：", "、".join(rec["facts_miss"]))
    print("\n完成：成功 %d，失败 %d" % (ok, fail))
    print("产出：", OUT_DIR)


if __name__ == "__main__":
    main()
