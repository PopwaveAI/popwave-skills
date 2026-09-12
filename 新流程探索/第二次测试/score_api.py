# -*- coding: utf-8 -*-
"""
把正文匿名送 API 做零上下文的人类读者审美打分。

    python score_api.py --dry-run        # 看样本池，不花钱
    python score_api.py                  # 打分（已打过的自动跳过）
    python score_api.py --report         # 只看汇总
    python score_api.py --no-skip        # 全部重打

匿名机制：样本先打乱再编号（S001...），编号不按来源排。
          真身映射写在 评分/mapping.json，只留在本地，不随正文发出去。
每次调用互相隔离：一份正文一次调用，不给别的样本作参照，避免互相锚定。
"""

import argparse
import hashlib
import json
import random
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
SCORE_DIR = BASE / "评分"
MAPPING = SCORE_DIR / "mapping.json"
MANIFEST = SCORE_DIR / "manifest.jsonl"

# 走 skill 链路的正文来源（真身，只在本文件里用）
SKILL_DIRS = [
    ("skill-灰烬之主", Path(r"C:\Users\AWMPRO\AppData\Roaming\popwave\paopao-workspace\projects\9-10-项目a\正文")),
    ("skill-旧海图", Path(r"C:\Users\AWMPRO\AppData\Roaming\popwave\paopao-workspace\projects\9-11-项目b\正文")),
]

DIMS = ["句子质感", "节奏呼吸", "人物活度", "画面具象", "情绪落点", "开局抓人", "自然度", "综合"]

PROMPT = """你是网文读者，不是编辑，也不是评审。下面是一篇中文小说第一章的正文，请你只凭阅读感受打分。

打分维度，每项 1 到 10 分。参照：6 分＝能读下去但不惊艳，7 到 8 分＝明显好于一般网文，9 到 10 分＝少见的好，5 分以下＝读不下去。
不要因为篇幅长短加减分。

1. 句子质感：语言是否准确、具体、不套路，有没有让你停下来重读的句子
2. 节奏呼吸：长短句和段落推进是否舒服，读起来有没有喘不上气或拖沓
3. 人物活度：人物有没有自己的欲望和性格，台词像不像人会说的话
4. 画面具象：能不能看见画面，有没有用抽象词代替具体描写
5. 情绪落点：读完留下什么，结尾有没有把气留在空中
6. 开局抓人：前三段能不能抓住你
7. 自然度：像不像一个人在讲故事，有没有 AI 腔、翻译腔、套路腔
8. 综合：作为一章正文，你愿不愿意接着读第二章

只输出 JSON，不要任何别的文字，格式：
{"句子质感": 0, "节奏呼吸": 0, "人物活度": 0, "画面具象": 0, "情绪落点": 0, "开局抓人": 0, "自然度": 0, "综合": 0, "一句总评": ""}

以下是正文：

"""


def load_env():
    cfg = {}
    for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if not s or s.startswith("#") or "=" not in s:
            continue
        k, v = s.split("=", 1)
        cfg[k.strip()] = v.strip()
    return cfg


def body_from_md(text: str) -> str:
    """从合并 md 里抠出每稿的正文（含模型自己写的简介块，不含我加的表头和思考）。"""
    parts = re.split(r"\n## 第 \d+ 稿\s*\n", text)
    out = []
    for p in parts[1:]:
        p = p.split("<details>")[0]
        p = p.strip().strip("-").strip()
        if p:
            out.append(p)
    return out


def build_samples(direct_model: str):
    samples = []

    # 直出稿：只收指定模型（默认 flash），别的模型不进池
    for mdir in sorted(p for p in OUT_DIR.iterdir() if p.is_dir()):
        if direct_model and mdir.name != direct_model:
            continue
        for gdir in sorted(p for p in mdir.iterdir() if p.is_dir()):
            md = gdir / (gdir.name + ".md")
            if not md.exists():
                continue
            for i, body in enumerate(body_from_md(md.read_text(encoding="utf-8")), 1):
                samples.append({
                    "group": "直出·" + mdir.name,
                    "name": "%s r%02d" % (gdir.name, i),
                    "text": body,
                })

    # 走 skill 链路的正文
    for label, d in SKILL_DIRS:
        if not d.exists():
            continue
        for f in sorted(d.glob("*.txt")):
            t = f.read_text(encoding="utf-8").strip()
            if t:
                samples.append({"group": label, "name": f.stem, "text": t})

    # 打乱 + 匿名编号（编号不按来源排）
    random.Random(20260912).shuffle(samples)
    for i, s in enumerate(samples, 1):
        s["id"] = "S%03d" % i
    return samples


def call(cfg, text):
    url = cfg["BASE_URL"].rstrip("/") + "/chat/completions"
    payload = {
        "model": cfg.get("SCORE_MODEL") or cfg["MODELS"].split(",")[0].strip(),
        "messages": [{"role": "user", "content": PROMPT + text}],
        "temperature": 0,
        # 评委是带思考的模型，思考量和 JSON 共用这份额度，给小了会把 JSON 截断
        "max_tokens": int(cfg.get("SCORE_MAX_TOKENS", "8000")),
        "stream": False,
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + cfg["DEEPSEEK_API_KEY"]},
        method="POST",
    )
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            body = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return {"ok": False, "error": "HTTP %s %s" % (e.code, e.read().decode("utf-8", "replace")[:200])}
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "error": repr(e)}

    raw = ((body.get("choices") or [{}])[0].get("message") or {}).get("content") or ""
    data = None
    m = re.search(r"\{.*\}", raw, re.S)
    if m:
        try:
            data = json.loads(m.group(0))
        except Exception:  # noqa: BLE001
            data = None
    if data is None:
        # 兜底：就算 JSON 被截断，也把已吐出来的维度抠出来
        data = {}
        for d in DIMS:
            mm = re.search('"%s"\\s*:\\s*(\\d+)' % d, raw)
            if mm:
                data[d] = int(mm.group(1))
    missed = [d for d in DIMS if not isinstance(data.get(d), (int, float))]
    if missed:
        return {"ok": False, "error": "缺维度 %s，原始输出前 120 字：%s" % (",".join(missed), raw[:120])}
    data.setdefault("一句总评", re.search(r"一句总评\"?\s*:\s*\"([^\"]{0,120})", raw).group(1)
                    if re.search(r"一句总评\"?\s*:\s*\"([^\"]{0,120})", raw) else "")
    return {"ok": True, "data": data, "seconds": round(time.time() - t0, 1)}


def one(cfg, s, idx, skip):
    p = SCORE_DIR / (s["id"] + "__p%d.json" % idx)
    if skip and p.exists():
        return {"status": "skip", "id": s["id"]}
    res = call(cfg, s["text"])
    rec = {"at": time.strftime("%Y-%m-%d %H:%M:%S"), "id": s["id"], "pass": idx,
           "chars": len(s["text"]), "group": s["group"], "name": s["name"]}
    if res["ok"]:
        p.write_text(json.dumps(res["data"], ensure_ascii=False, indent=1), encoding="utf-8")
        rec["status"] = "ok"
        rec["seconds"] = res.get("seconds")
        rec["scores"] = {d: res["data"][d] for d in DIMS}
        rec["comment"] = str(res["data"].get("一句总评", ""))[:200]
    else:
        rec["status"] = "fail"
        rec["error"] = res["error"]
    return rec


def report():
    if not SCORE_DIR.exists():
        sys.exit("还没有评分结果")
    pertask = {}
    for p in sorted(SCORE_DIR.glob("S*__p*.json")):
        sid = p.name.split("__")[0]
        pertask.setdefault(sid, []).append(json.loads(p.read_text(encoding="utf-8")))
    if not pertask:
        sys.exit("还没有评分结果")
    mapping = json.loads(MAPPING.read_text(encoding="utf-8")) if MAPPING.exists() else {}

    # 每份稿先把多轮平均掉，让一份稿只算一票，再进分组
    samples = {}
    for sid, runs in pertask.items():
        samples[sid] = {d: sum(r[d] for r in runs) / len(runs) for d in DIMS}

    bygroup = {}
    for sid, d in samples.items():
        g = mapping.get(sid, {}).get("group", "?")
        bygroup.setdefault(g, []).append(d)

    def line(label, ds):
        m = [sum(x[d] for x in ds) / len(ds) for d in DIMS]
        return "%-24s %5d %7.2f %7.2f %7.2f %7.2f %7.2f %7.2f %7.2f %7.2f" % (label, len(ds), *m)

    head = "%-24s %5s %7s %7s %7s %7s %7s %7s %7s %7s" % ("组", "稿数", *DIMS)
    print("=" * 108)
    print("人类读者审美评分 · 分组均值（每份稿多轮先平均，一份稿一票）")
    print("=" * 108)
    print(head)
    for g in sorted(bygroup, key=lambda x: -sum(sum(v[d] for d in DIMS) for v in bygroup[x])):
        print(line(g, bygroup[g]))

    direct = [g for g in bygroup if g.startswith("直出")]
    if direct:
        print()
        print("=" * 108)
        print("直出组按赛道（看清均分是不是被多赛道稀释了）")
        print("=" * 108)
        print(head)
        buckets = {}
        for sid, d in samples.items():
            if not mapping.get(sid, {}).get("group", "").startswith("直出"):
                continue
            genre = mapping[sid]["name"].split(" r")[0]
            buckets.setdefault(genre, []).append(d)
        for g in sorted(buckets, key=lambda x: -sum(sum(v[d] for d in DIMS) for v in buckets[x])):
            print(line(g, buckets[g]))

    print()
    print("=" * 108)
    print("逐稿（两轮均分）")
    print("=" * 108)
    for sid in sorted(samples, key=lambda s: -samples[s]["综合"]):
        d = samples[sid]
        mm = mapping.get(sid, {})
        print("%s  综合%.1f  句质%.1f 节奏%.1f 人物%.1f 画面%.1f 情绪%.1f 开局%.1f 自然%.1f  [%s] %s"
              % (sid, d["综合"], d["句子质感"], d["节奏呼吸"], d["人物活度"], d["画面具象"],
                 d["情绪落点"], d["开局抓人"], d["自然度"], mm.get("group", "?"), mm.get("name", "")))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--passes", type=int, default=2, help="每份打几轮（取均值可降噪，默认 2）")
    ap.add_argument("--concurrency", type=int, default=4)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--no-skip", action="store_true")
    a = ap.parse_args()

    if a.report:
        report()
        return

    cfg = load_env()
    samples = build_samples(cfg.get("SCORE_DIRECT_MODEL", "deepseek-flash"))
    SCORE_DIR.mkdir(exist_ok=True)

    if not MAPPING.exists() or a.no_skip:
        MAPPING.write_text(json.dumps(
            {s["id"]: {"group": s["group"], "name": s["name"], "chars": len(s["text"])}
             for s in samples}, ensure_ascii=False, indent=1), encoding="utf-8")

    cnt = {}
    for s in samples:
        cnt[s["group"]] = cnt.get(s["group"], 0) + 1
    print("样本池 %d 份，每份 %d 轮，共 %d 次调用" % (len(samples), a.passes, len(samples) * a.passes))
    for g in sorted(cnt):
        print("   %s：%d 份" % (g, cnt[g]))
    print("评分模型：", cfg.get("SCORE_MODEL") or cfg["MODELS"].split(",")[0].strip())
    if a.dry_run:
        return

    tasks = [(s, i) for s in samples for i in range(1, a.passes + 1)]
    ok = fail = skipped = 0
    with ThreadPoolExecutor(max_workers=a.concurrency) as ex:
        futs = [ex.submit(one, cfg, s, i, not a.no_skip) for s, i in tasks]
        for f in as_completed(futs):
            rec = f.result()
            if rec.get("status") == "skip":
                skipped += 1
                continue
            with MANIFEST.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
            if rec["status"] == "ok":
                ok += 1
                print("[ok  ] %s p%d 综合%2d  %s" % (rec["id"], rec["pass"], rec["scores"]["综合"], rec["comment"][:40]))
            else:
                fail += 1
                print("[FAIL] %s p%d %s" % (rec["id"], rec["pass"], rec["error"]))

    print("\n成功 %d，失败 %d，跳过 %d\n" % (ok, fail, skipped))
    report()


if __name__ == "__main__":
    main()
