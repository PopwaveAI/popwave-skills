# -*- coding: utf-8 -*-
"""7-21-项目a 日志解耦深度审计脚本.
扫描 runs/conversations/artifacts 三层, 量化冗余/重复/信息沉底/孤儿/元数据缺失.
运行: python log_audit.py <项目根目录>
"""
import json, os, re, sys, hashlib, collections

ROOT = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\AWMPRO\.paopao\projects\7-21-项目a"
OUT_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "log_audit_results.json")

def jl_load(path):
    """逐行解析 JSONL, 返回 (对象列表, 失败行数)."""
    objs, bad = [], 0
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                objs.append(json.loads(line))
            except Exception:
                bad += 1
    return objs, bad

def sha(s):
    if not isinstance(s, str):
        s = json.dumps(s, ensure_ascii=False)
    return hashlib.md5(s.encode("utf-8", errors="replace")).hexdigest()

def walk_items(ev):
    """从事件对象里递归收集所有 model-trace item 的 kind 与 toolName."""
    kinds = collections.Counter()
    tools = collections.Counter()
    def rec(o):
        if isinstance(o, dict):
            if o.get("kind") in ("thinking","text","tool-call","tool-result"):
                kinds[o.get("kind")] += 1
                if o.get("toolName"):
                    tools[o["toolName"]] += 1
            for v in o.values():
                rec(v)
        elif isinstance(o, list):
            for v in o:
                rec(v)
    rec(ev)
    return kinds, tools

def main():
    report = []
    L = report.append
    L("=" * 70)
    L("7-21-项目a 日志解耦深度审计")
    L("=" * 70)

    # ---------- 1. 存储盘点 ----------
    L("\n## 1. 存储盘点")
    convs_dir = os.path.join(ROOT, "conversations")
    runs_dir = os.path.join(ROOT, "runs")
    arts_dir = os.path.join(ROOT, "artifacts")
    skills_dir = os.path.join(ROOT, "skills")

    # 收集所有文件
    all_files = []
    for base in os.listdir(ROOT):
        bp = os.path.join(ROOT, base)
        if os.path.isdir(bp):
            for dp, dn, fns in os.walk(bp):
                for fn in fns:
                    fp = os.path.join(dp, fn)
                    all_files.append((fp, os.path.getsize(fp)))

    total_bytes = sum(sz for _, sz in all_files)
    by_dir = collections.Counter()
    for fp, sz in all_files:
        rel = os.path.relpath(fp, ROOT)
        top = rel.split(os.sep)[0]
        by_dir[top] += sz
    L(f"总文件数: {len(all_files)}  总体积: {total_bytes/1024/1024:.2f} MB")
    for d, sz in sorted(by_dir.items(), key=lambda x: -x[1]):
        L(f"  {d}: {sz/1024/1024:.2f} MB")

    # run 目录清单
    runids = [d for d in os.listdir(runs_dir) if os.path.isdir(os.path.join(runs_dir, d))]
    L(f"\nrun 目录数: {len(runids)}")
    has_resp = sum(1 for r in runids if os.path.exists(os.path.join(runs_dir, r, "response.md")))
    has_input = sum(1 for r in runids if os.path.exists(os.path.join(runs_dir, r, "input.json")))
    has_ev = sum(1 for r in runids if os.path.exists(os.path.join(runs_dir, r, "events.jsonl")))
    has_sub = sum(1 for r in runids if os.path.isdir(os.path.join(runs_dir, r, "subagents")))
    L(f"  response.md 存在: {has_resp}/{len(runids)}")
    L(f"  input.json 存在: {has_input}/{len(runids)}")
    L(f"  events.jsonl 存在: {has_ev}/{len(runids)}")
    L(f"  subagents 存在: {has_sub}/{len(runids)}")
    # 缺 response.md 的 run
    missing_resp = [r for r in runids if not os.path.exists(os.path.join(runs_dir, r, "response.md"))]
    L(f"  缺 response.md 的 run ({len(missing_resp)}): {missing_resp}")

    # ---------- 2. events.jsonl 事件结构 ----------
    L("\n## 2. events.jsonl 事件类型分布")
    ev_types = collections.Counter()
    item_kinds = collections.Counter()
    tool_names = collections.Counter()
    ev_bad_lines = 0
    ev_total_lines = 0
    for r in runids:
        ep = os.path.join(runs_dir, r, "events.jsonl")
        if not os.path.exists(ep):
            continue
        objs, bad = jl_load(ep)
        ev_bad_lines += bad
        ev_total_lines += len(objs) + bad
        for o in objs:
            t = o.get("type", "?")
            ev_types[t] += 1
            if t == "model-trace":
                k, tls = walk_items(o)
                item_kinds.update(k)
                tool_names.update(tls)
            elif t == "tool":
                tool_names[o.get("name", "?")] += 1
    L(f"  总事件行: {ev_total_lines}  解析失败行: {ev_bad_lines}")
    L(f"  事件类型: {dict(ev_types)}")
    L(f"  model-trace item 类型: {dict(item_kinds)}")
    L(f"  工具调用分布(top20): {dict(tool_names.most_common(20))}")

    # ---------- 3. 冗余度测量 ----------
    L("\n## 3. 冗余/重复测量")
    # 3a. response.md 文本是否内嵌在 events.jsonl (归一化空白后指纹)
    def norm(s):
        return re.sub(r"\s+", "", s)
    resp_dup_warn = 0
    resp_showdup_sizes = []
    for r in runids:
        rd = os.path.join(runs_dir, r, "response.md")
        ep = os.path.join(runs_dir, r, "events.jsonl")
        if not (os.path.exists(rd) and os.path.exists(ep)):
            continue
        resp = open(rd, encoding="utf-8", errors="replace").read()
        if len(norm(resp)) < 60:
            continue
        ev = norm(open(ep, encoding="utf-8", errors="replace").read())
        frag = norm(resp)[:60]
        if frag in ev:
            resp_dup_warn += 1
            resp_showdup_sizes.append((r, len(resp)))
    L(f"  a) response.md 文本(归一化后)在 events.jsonl 中重复的 run: {resp_dup_warn}/{len(runids)}")
    if resp_showdup_sizes:
        L(f"     最大重复样本: {resp_showdup_sizes[:3]}")

    # 3b. conversation jsonl 内嵌 events 与 run events.jsonl 重复
    conv_lines_total = 0
    conv_embed_events = 0
    conv_msg = 0
    conv_refs = []  # message 引用的 runId
    for cf in os.listdir(convs_dir):
        if not cf.endswith(".jsonl"):
            continue
        objs, bad = jl_load(os.path.join(convs_dir, cf))
        conv_lines_total += len(objs) + bad
        for o in objs:
            if o.get("type") == "message":
                conv_msg += 1
                if o.get("events"):
                    conv_embed_events += 1
                if o.get("runId"):
                    conv_refs.append(o["runId"])
    L(f"  b) conversation 消息总数: {conv_msg}, 其中内嵌完整 events[] 的消息数: {conv_embed_events}")
    L("     (内嵌 events 是冗余副本, 与 runs/{runId}/events.jsonl 重复)")

    # 3c. artifacts events 冗余
    art_total = 0
    art_with_events = 0
    art_only_content = 0
    for af in os.listdir(arts_dir):
        if not af.endswith(".json"):
            continue
        art_total += 1
        try:
            a = json.load(open(os.path.join(arts_dir, af), encoding="utf-8", errors="replace"))
        except Exception:
            continue
        if a.get("events"):
            art_with_events += 1
        if a.get("content") and not a.get("events"):
            art_only_content += 1
    L(f"  c) artifacts 总数 {art_total}: 含完整 events[] 轨迹 {art_with_events}, 仅 content 无 events {art_only_content}")

    # 3d. input.json 各字段大小 + 跨 run 公共上下文
    L(f"  d) input.json 顶层字段体积 (抽样统计): ")
    field_sizes = collections.defaultdict(list)
    input_total = 0
    for r in runids:
        ip = os.path.join(runs_dir, r, "input.json")
        if not os.path.exists(ip):
            continue
        sz = os.path.getsize(ip)
        input_total += sz
        try:
            d = json.load(open(ip, encoding="utf-8", errors="replace"))
        except Exception:
            continue
        for k, v in d.items():
            field_sizes[k].append(len(json.dumps(v, ensure_ascii=False)))
    L(f"     input.json 层总体积: {input_total/1024/1024:.2f} MB ({input_total/1024:.0f} KB)")
    for k, sizes in sorted(field_sizes.items(), key=lambda x: -sum(x[1])):
        L(f"     {k}: 平均 {sum(sizes)/len(sizes)/1024:.0f}KB  x{len(sizes)} 次")

    # 3e. 跨 run 公共字段去重后估算
    L(f"  e) 若 input.json 只存每 run 差异(共用 project/skills/promptModules), 估算可省: "
      f"约 {input_total*0.6/1024/1024:.1f} MB")

    # ---------- 4. 元数据抽取 / 信息沉底 ----------
    L("\n## 4. 元数据抽取与信息沉底")
    error_events = []
    file_change_events = []
    token_usage = []
    duration_list = []
    model_set = set()
    runtime_set = set()
    exit_codes = collections.Counter()
    for r in runids:
        ep = os.path.join(runs_dir, r, "events.jsonl")
        if not os.path.exists(ep):
            continue
        objs, _ = jl_load(ep)
        for o in objs:
            otype = o.get("type")
            if otype == "error":
                error_events.append((r, o.get("summary", o)))
            elif otype == "file-change":
                file_change_events.append((r, o.get("summary", o)))
            elif otype == "tool" and o.get("name") == "Popwave Agent":
                out = o.get("outputSummary", "")
                try:
                    osj = json.loads(out)
                except Exception:
                    osj = {}
                if isinstance(osj, dict):
                    if "durationMs" in osj: duration_list.append(osj["durationMs"])
                    if "exitCode" in osj: exit_codes[osj["exitCode"]] += 1
                    # 最深一层: stdout/stderr/jsonTelemetry 本身是 JSON 字符串
                    for inner_key in ("stdout", "stderr", "jsonTelemetry"):
                        inner = osj.get(inner_key, "")
                        if not isinstance(inner, str):
                            continue
                        try:
                            iobj = json.loads(inner)
                        except Exception:
                            continue
                        if isinstance(iobj, dict):
                            meta = iobj.get("meta") or {}
                            am = meta.get("agentMeta") or {}
                            if am.get("model"): model_set.add(am["model"])
                            if am.get("runtimeVersion"): runtime_set.add(am["runtimeVersion"])
                            if am.get("usage"): token_usage.append(am["usage"])
                            if "durationMs" in meta: duration_list.append(meta["durationMs"])
    L(f"  token usage 样本数: {len(token_usage)}, 平均 input tokens: "
      f"{sum(t.get('input',0) for t in token_usage)/max(len(token_usage),1):.0f}")
    L(f"  durationMs 样本数: {len(duration_list)}, 平均: {sum(duration_list)/max(len(duration_list),1)/1000:.1f}s")
    L(f"  exitCode 分布: {dict(exit_codes)}")
    L(f"  模型: {sorted(model_set) or '未抽取到'}")
    L(f"  runtime: {sorted(runtime_set) or '未抽取到'}")
    L(f"  顶层 error 事件: {error_events or '无'}")
    L(f"  file-change 事件数: {len(file_change_events)}")
    if file_change_events:
        L(f"   file-change 样例: {file_change_events[:5]}")

    # 4b. stderr 里的错误(在 Popwave Agent tool 的 stderr 字段)
    stderr_marks = []
    for r in runids:
        ep = os.path.join(runs_dir, r, "events.jsonl")
        if not os.path.exists(ep):
            continue
        for line in open(ep, encoding="utf-8", errors="replace"):
            if "Popwave Agent" not in line:
                continue
            if "stderr" not in line:
                continue
            # 粗略匹配 stderr 中典型错误词
            for pat, tag in [(r"subagent-interrupted-resume", "subagent-resume-fail"),
                             (r"gateway closed", "gateway-closed"),
                             (r"Traceback", "traceback"),
                             (r"failed", "failed"),
                             (r"denied", "denied"),
                             (r"aborted", "aborted")]:
                if re.search(pat, line, re.I):
                    stderr_marks.append((r, tag))
    L(f"  stderr 中含错误标记的 run: {stderr_marks[:20]}")

    # ---------- 5. 时间线跨度 ----------
    times = []
    for r in runids:
        ep = os.path.join(runs_dir, r, "events.jsonl")
        if os.path.exists(ep):
            for line in open(ep, encoding="utf-8", errors="replace"):
                line = line.strip()
                if not line: continue
                try:
                    o = json.loads(line)
                except Exception:
                    continue
                at = o.get("at")
                if at: times.append(at)
    if times:
        L(f"  事件时间戳数量: {len(times)}")
        L(f"  最早: {min(times)}")
        L(f"  最晚: {max(times)}")

    # ---------- 6. skill 使用映射 ----------
    L("\n## 6. skill 使用映射 (从 input.json 提取)")
    skill_usage = collections.Counter()
    inp_key_sizes = dict()
    for r in runids:
        ip = os.path.join(runs_dir, r, "input.json")
        if not os.path.exists(ip):
            continue
        try:
            d = json.load(open(ip, encoding="utf-8", errors="replace"))
        except Exception:
            continue
        # 尝试从 skills 或 prompt 里找 skill 名
        blob = json.dumps(d, ensure_ascii=False)
        for m in re.findall(r'pop-[a-z0-9\-]+', blob):
            skill_usage[m] += 1
    for s, c in skill_usage.most_common(30):
        L(f"  {s}: {c}")

    # ---------- 7. 孤儿 / 引用完整性 ----------
    L("\n## 7. 引用完整性 (孤儿检测)")
    conv_run_ids = set()
    for cf in os.listdir(convs_dir):
        if not cf.endswith(".jsonl"):
            continue
        for o, _ in [(o, 0) for o in jl_load(os.path.join(convs_dir, cf))[0]]:
            if o.get("runId"): conv_run_ids.add(o["runId"])
    # index.json 里的 runId
    try:
        idx = json.load(open(os.path.join(convs_dir, "index.json"), encoding="utf-8"))
        for c in idx:
            if c.get("lastRunId"): conv_run_ids.add(c["lastRunId"])
            if c.get("parentRunId"): conv_run_ids.add(c["parentRunId"])
    except Exception:
        pass
    run_set = set(runids)
    orphan_runs = [r for r in runids if r not in conv_run_ids]
    missing_runs = [rid for rid in conv_run_ids if rid not in run_set]
    L(f"  run 目录总数: {len(run_set)}")
    L(f"  未被任何会话引用(孤儿 run): {len(orphan_runs)} -> {orphan_runs}")
    L(f"  被引用但目录缺失: {len(missing_runs)} -> {missing_runs}")

    # ---------- 8. 汇总 JSON ----------
    result = {
        "total_files": len(all_files),
        "total_bytes": total_bytes,
        "by_dir": {k: v for k, v in by_dir.items()},
        "run_count": len(runids),
        "missing_response_runs": missing_resp,
        "event_types": dict(ev_types),
        "item_kinds": dict(item_kinds),
        "tool_names": dict(tool_names.most_common(30)),
        "resp_dup_in_events": resp_dup_warn,
        "conv_msg_total": conv_msg,
        "conv_msg_with_embedded_events": conv_embed_events,
        "artifacts_total": art_total,
        "artifacts_with_events": art_with_events,
        "input_bytes_total": input_total,
        "input_field_avg_kb": {k: round(sum(v)/len(v)/1024,1) for k, v in field_sizes.items()},
        "error_events": [str(e) for e in error_events],
        "file_change_count": len(file_change_events),
        "stderr_error_marks": stderr_marks,
        "token_usage_samples": len(token_usage),
        "avg_input_tokens": round(sum(t.get('input',0) for t in token_usage)/max(len(token_usage),1)),
        "exit_codes": dict(exit_codes),
        "models": sorted(model_set),
        "runtimes": sorted(runtime_set),
        "orphan_runs": orphan_runs,
        "missing_runs": missing_runs,
    }
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    L(f"\n结果 JSON 已保存: {OUT_JSON}")

    txt = "\n".join(report)
    print(txt)
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "log_audit_report.txt"), "w", encoding="utf-8").write(txt)

if __name__ == "__main__":
    main()