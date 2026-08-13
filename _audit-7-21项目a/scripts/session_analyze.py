# -*- coding: utf-8 -*-
"""7-21项目a 会话链条分析. 读 index.json + subagents, 输出分析数据."""
import json, os, collections

META = r"d:\popwave-skills\_audit-7-21项目a\_logmeta"
SRC = r"C:\Users\AWMPRO\.paopao\projects\7-21-项目a"
OUT = r"c:\Users\AWMPRO\.trae-cn\work\6a7cc05fef4ef00c46f73d82\session_analysis.json"

rows = json.load(open(os.path.join(META, "index.json"), encoding="utf-8"))

# 会话分组
sessions = collections.OrderedDict()  # title -> list[run]
for r in rows:
    t = r.get("conversationTitle") or "(未关联)"
    sessions.setdefault(t, []).append(r)

# 子 agent 数据
subagents = []
for d in os.listdir(os.path.join(SRC, "runs")):
    sd = os.path.join(SRC, "runs", d, "subagents")
    if not os.path.isdir(sd):
        continue
    for sa in os.listdir(sd):
        p = os.path.join(sd, sa, "result.json")
        if not os.path.exists(p):
            continue
        j = json.load(open(p, encoding="utf-8"))
        subagents.append({
            "parentRun": d[:8], "subRun": j.get("runId", sa)[:8],
            "title": j.get("title"), "purpose": j.get("purpose"),
            "status": j.get("status"), "summaryLen": len(str(j.get("summary", ""))),
            "detailsLen": len(str(j.get("details", ""))),
            "error": str(j.get("error"))[:200] if j.get("error") else None,
        })

result = {"sessions": {}, "subagents": subagents}

for title, runs in sessions.items():
    runs.sort(key=lambda r: r.get("startedAt") or "")
    tokens = [(r.get("inputTokens")) for r in runs]
    tokenized = [t for t in tokens if t is not None]
    tot_in = sum(tokenized)
    tot_cache = sum(r.get("cacheRead") or 0 for r in runs)
    tot_dur = sum(r.get("durationMs") or 0 for r in runs)
    n_ok = sum(1 for r in runs if r["status"] == "success")
    n_fail = sum(1 for r in runs if r["status"] == "fail")
    n_part = sum(1 for r in runs if r["status"] == "partial")
    result["sessions"][title] = {
        "kind": runs[0].get("kind"), "purpose": runs[0].get("purpose"),
        "runCount": len(runs), "nSuccess": n_ok, "nFail": n_fail, "nPartial": n_part,
        "inputTokensSum": tot_in, "tokenizedCount": len(tokenized),
        "cacheReadSum": tot_cache, "durationMsSum": tot_dur,
        "inputFirst": tokenized[0] if tokenized else None,
        "inputLast": tokenized[-1] if tokenized else None,
        "inputMax": max(tokenized) if tokenized else None,
        "runs": [{"runId": r["runId"][:8], "status": r["status"], "startedAt": r["startedAt"],
                  "input": r["inputTokens"], "cacheRead": r["cacheRead"], "durMs": r["durationMs"],
                  "error": (r["errors"][0] if r["errors"] else None)} for r in runs],
    }

json.dump(result, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

# 打印概览
print(f"{'会话':<22}{'run数':>5}{'成功':>5}{'失败':>5}{'残缺':>5}{'input累计':>10}{'token采样':>8}{'input首→末':>16}{'耗时累计s':>10}")
for t, s in result["sessions"].items():
    f = f"{s['inputFirst']}→{s['inputLast']}" if s['inputFirst'] is not None else "—"
    print(f"{t[:22]:<22}{s['runCount']:>5}{s['nSuccess']:>5}{s['nFail']:>5}{s['nPartial']:>5}"
          f"{s['inputTokensSum']:>10,}{s['tokenizedCount']:>8}{f:>16}{s['durationMsSum']/1000:>10.1f}")
print("\n--- 子agent ---")
for sa in subagents:
    print(f"  {sa['title'][:20]:<20} status={sa['status']} purpose={sa['purpose']} summary={sa['summaryLen']}ch details={sa['detailsLen']}ch")