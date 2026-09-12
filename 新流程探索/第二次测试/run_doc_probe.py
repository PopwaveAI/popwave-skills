# -*- coding: utf-8 -*-
"""
信息槽载体形态探针（I 组）

问什么：老板假设——流派词已能保证质感，信息槽就该写成设计文档式，把控制力拉满。
        对手证据：上一轮 H3 用武侠＋条目式，质感仍碎（段长 34.5，短句占比 41.7%）。
        所以本轮要分清：是「条目」本身导致碎，还是「模型把信息槽当正文来模仿」导致碎。

三个条件（同情境、同流派词武侠、同七条事实）：
  I1 设计文档（字段式）＋ 显式声明「这是文档不是正文，不要模仿格式与句式」
  I2 设计文档（字段式）＋ 不加声明      ← 与 I1 只差一句声明，隔离「声明」这个变量
  I3 极简关键词式 ＋ 显式声明           ← 信息槽能压到多干
基线 I0 = 上一轮 H2（武侠＋同七条事实，散文式，9/9 兑现且落点精准），不重跑。

用法：
    python run_doc_probe.py --dry-run
    python run_doc_probe.py
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
IN_DIR = BASE / "输入" / "信息槽形态探针"
OUT_DIR = BASE / "输出" / "信息槽形态探针"
MANIFEST = OUT_DIR / "manifest.jsonl"

PREMISE = (
    "一个人回到十年前的旧居。房子早已空了，房东换过三任。"
    "他在二楼朝北的屋子里找到一只铁盒，里面是当年没寄出的信。"
    "当晚他决定住下，把信一封封重读。"
)

DECL = "以下是本章的内容设计文档，不是正文。不要模仿本文档的格式与句式。"

DOC_FIELD = """【人物】
- 主角：姓赵，三十余岁，十年前离开本城
- 师父：已故三年，院子原主

【场景】
- 旧居院子，二楼朝北的屋子

【道具】
- 铁盒：内装七封信，收件人均为主角，笔迹为师父

【事件链】
1. 主角回到旧居
2. 翻出铁盒与七封信
3. 前六封都是寻常叮嘱
4. 第七封未封口，里面只有半张地图
5. 当晚有人敲门，自称师父生前的旧识，说这院子他不能住

【落点】
- 停在主角把半张地图摊在桌上，又听见院门外有脚步声

【禁令】
- 不交代来人是谁
- 不解释地图指向哪里"""

DOC_MIN = """人物：赵某(30+)／已故师父(院子原主)
场景：旧居·二楼朝北屋
道具：铁盒＝七封信(收件人均为主角·笔迹为师父)
事件：归宅→翻出铁盒→读信(前六封寻常叮嘱)→第七封未封口·只有半张地图→有人敲门(自称师父旧识·说这院子他不能住)
落点：地图摊桌上＋院门外脚步声
禁令：不交代来人身份／不解释地图指向"""

CONDITIONS = [
    ("I1", "设计文档（字段式）＋声明", DECL + "\n\n" + DOC_FIELD),
    ("I2", "设计文档（字段式）无声明", DOC_FIELD),
    ("I3", "极简关键词式＋声明", DECL + "\n\n" + DOC_MIN),
]

FACT_KEYS = [
    (["赵"], "姓赵"),
    (["师父"], "师父"),
    (["十年"], "十年前"),
    (["七封", "7封", "七封信"], "七封信"),
    (["叮嘱"], "前六封是叮嘱"),
    (["地图"], "半张地图"),
    (["敲门", "叩门"], "有人敲门"),
    (["不能住", "别住", "搬走", "住不得"], "说了不能住"),
    (["脚步声"], "章末脚步声"),
]
HAN = re.compile(r"[\u4e00-\u9fff]")


def build_prompt(info):
    return "写一段武侠小说第一章。\n\n" + PREMISE + "\n\n" + info


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


def call_api(cfg, model, prompt, timeout=600, max_tokens=None):
    payload = {"model": model, "messages": [{"role": "user", "content": prompt}],
               "temperature": float(cfg.get("TEMPERATURE", "1.0")),
               "top_p": float(cfg.get("TOP_P", "1.0")),
               "max_tokens": int(max_tokens or cfg.get("MAX_TOKENS", "8000")), "stream": False}
    req = urllib.request.Request(
        cfg["BASE_URL"].rstrip("/") + "/chat/completions",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + cfg["DEEPSEEK_API_KEY"]}, method="POST")
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
    return {"ok": True, "seconds": round(time.time() - t0, 1), "text": msg.get("content") or "",
            "reasoning": msg.get("reasoning_content") or "",
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
            out.append("\u201c" if open_q else "\u201d"); open_q = not open_q
        else:
            out.append(ch)
    return re.sub(r"\n{3,}", "\n\n", "".join(out)).strip()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default=None)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-skip", action="store_true")
    ap.add_argument("--max-tokens", type=int, default=None, help="覆盖 .env 的输出额度")
    ap.add_argument("--only", default=None, help="只跑指定条件，如 I1")
    args = ap.parse_args()
    cfg = load_env(ENV_PATH)
    model = args.model or (cfg.get("MODELS", "deepseek-flash").split(",")[0].strip())

    IN_DIR.mkdir(parents=True, exist_ok=True)
    for code, label, info in CONDITIONS:
        (IN_DIR / ("%s-%s.md" % (code, label))).write_text(build_prompt(info), encoding="utf-8")
    print("输入已归档：%s（%d 份）" % (IN_DIR, len(CONDITIONS)))
    print("模型：%s  温度：%s  零 system message" % (model, cfg.get("TEMPERATURE", "1.0")))
    if args.dry_run:
        for code, label, info in CONDITIONS:
            print("  %s  %-24s 信息槽 %d 字，含声明=%s" % (code, label, len(info), info.startswith("以下")))
        return

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ok = fail = 0
    for code, label, info in CONDITIONS:
        if args.only and code != args.only:
            continue
        raw_p = OUT_DIR / ("%s__raw.txt" % code)
        if raw_p.exists() and not args.no_skip:
            print("[skip] %s %s" % (code, label)); continue
        prompt = build_prompt(info)
        res = call_api(cfg, model, prompt, max_tokens=args.max_tokens)
        rec = {"at": time.strftime("%Y-%m-%d %H:%M:%S"), "model": model, "code": code,
               "label": label, "prompt": prompt, "info_slot": info,
               "has_decl": info.startswith("以下"),
               "max_tokens": int(args.max_tokens or cfg.get("MAX_TOKENS", "8000")),
               "temperature": float(cfg.get("TEMPERATURE", "1.0"))}
        if not res["ok"]:
            rec.update({"status": "fail", "error": res["error"], "seconds": res["seconds"]})
            with MANIFEST.open("a", encoding="utf-8") as f:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            fail += 1; print("[FAIL] %s %s  %s" % (code, label, res["error"])); continue
        text = res["text"]
        body = re.sub(r"\s+", "", text)
        hit = [(n, any(k in body for k in keys)) for keys, n in FACT_KEYS]
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
                    "landing_hit": hit[-1][1]})
        with MANIFEST.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        ok += 1
        print("[ok  ] %s %-24s %ss  汉字%d 段%d 均段%s  硬事实%s  落点=%s"
              % (code, label, res["seconds"], han, paras, rec["avg_para"], rec["facts_rate"], hit[-1][1]))
        if rec["facts_miss"]:
            print("        未兑现：", "、".join(rec["facts_miss"]))
    print("\n完成：成功 %d，失败 %d" % (ok, fail))
    print("产出：", OUT_DIR)


if __name__ == "__main__":
    main()
