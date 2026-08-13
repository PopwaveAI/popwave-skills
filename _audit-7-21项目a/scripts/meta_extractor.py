# -*- coding: utf-8 -*-
"""7-21项目a runs 层 meta.json 抽取器.
对每个 run 生成结构化元数据, 并汇总 index.json.
输入: 源项目根 (只读)  输出: 目标目录/_logmeta/{runId}.json + index.json
运行: python meta_extractor.py <源项目根> <输出目录>
"""
import json, os, re, sys, collections

SRC = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\AWMPRO\.paopao\projects\7-21-项目a"
OUT = sys.argv[2] if len(sys.argv) > 2 else r"d:\popwave-skills\_audit-7-21项目a\_logmeta"

KV = re.compile(r'([a-zA-Z]+)[^0-9]*?:\s*(-?\d+)')
TS = re.compile(r'\\?"at\\?"\s*:\s*\\?"([0-9TZ:\-\.]+)\\?"')

def usage_from_text(text):
    """从文本提取 usage 对象(3层转义, 平衡括号)."""
    out = []
    for m in re.finditer('usage', text):
        i = text.find('{', m.end())
        if i < 0: continue
        depth = 0; j = i
        while j < len(text):
            c = text[j]
            if c == '{': depth += 1
            elif c == '}':
                depth -= 1
                if depth == 0: break
            j += 1
        d = dict((k, int(v)) for k, v in KV.findall(text[i+1:j]))
        if 'input' in d: out.append(d)
    return out

def text_scan(text):
    """从文本扫描提取 usage/model/contextTokens/runtime/exitCode/durationMs."""
    meta = {}
    us = usage_from_text(text)
    if us: meta['usage'] = us[0]
    for pat, key in [(r'\\?"model\\?"\s*:\s*\\?"([^\\"]+)\\?"', 'model'),
                     (r'\\?"runtimeVersion\\?"\s*:\s*\\?"([^\\"]+)\\?"', 'runtime'),
                     (r'\\?"contextTokens\\?"\s*:\s*(\d+)', 'contextTokens')]:
        m = re.search(pat, text)
        if m:
            meta[key] = int(m.group(1)) if key == 'contextTokens' else m.group(1)
    return meta

def extract_run(runid):
    rdir = os.path.join(SRC, 'runs', runid)
    ep = os.path.join(rdir, 'events.jsonl')
    meta = {
        'runId': runid,
        'eventCounts': collections.Counter(),
        'toolsTop': collections.Counter(),
        'errors': [],
        'timestamps': [],
        'hasResponseMd': os.path.exists(os.path.join(rdir, 'response.md')),
        'responseSizeBytes': os.path.getsize(os.path.join(rdir, 'response.md')) if os.path.exists(os.path.join(rdir, 'response.md')) else 0,
        'inputJsonSizeBytes': os.path.getsize(os.path.join(rdir, 'input.json')) if os.path.exists(os.path.join(rdir, 'input.json')) else 0,
    }
    if os.path.isdir(os.path.join(rdir, 'subagents')):
        meta['subagents'] = sorted(os.listdir(os.path.join(rdir, 'subagents')))
    else:
        meta['subagents'] = []
    if not os.path.exists(ep):
        return meta

    raw = open(ep, encoding='utf-8', errors='replace').read()
    # 文本级: usage / model / contextTokens / 时间
    for k, v in text_scan(raw).items():
        meta[k] = v
    for m in TS.finditer(raw):
        meta['timestamps'].append(m.group(1))

    # 行级: 事件类型 / 工具 / error / exitCode / durationMs
    for line in raw.splitlines():
        line = line.strip()
        if not line: continue
        try:
            o = json.loads(line)
        except Exception:
            continue
        t = o.get('type', '?')
        meta['eventCounts'][t] += 1
        if t == 'error':
            meta['errors'].append(str(o.get('summary', o))[:200])
        elif t == 'tool':
            meta['toolsTop'][o.get('name', '?')] += 1
        elif t == 'model-trace':
            for it in o.get('items', []):
                if isinstance(it, dict) and it.get('toolName'):
                    meta['toolsTop'][it['toolName']] += 1
        if t == 'tool' and o.get('name') == 'Popwave Agent':
            try:
                osj = json.loads(o.get('outputSummary', '') or '{}')
                if isinstance(osj, dict):
                    if 'exitCode' in osj: meta['exitCode'] = osj['exitCode']
                    if 'durationMs' in osj: meta['durationMs'] = osj['durationMs']
            except Exception:
                pass
    return meta

def build_index():
    os.makedirs(OUT, exist_ok=True)
    # run -> conversation 映射 (所有 runId 都关联到其所属会话的 title)
    idx = json.load(open(os.path.join(SRC, 'conversations', 'index.json'), encoding='utf-8'))
    conv_meta = {c.get('id'): {'title': c.get('title'), 'kind': c.get('kind'),
                               'purpose': c.get('branchPurpose')} for c in idx}
    conv_map = {}
    for c in idx:
        if c.get('parentRunId'): conv_map[c['parentRunId']] = conv_meta.get(c.get('id'), {})
    for cf in os.listdir(os.path.join(SRC, 'conversations')):
        if not cf.endswith('.jsonl'): continue
        cm = conv_meta.get(cf[:-6], {})
        for line in open(os.path.join(SRC, 'conversations', cf), encoding='utf-8', errors='replace'):
            line = line.strip()
            if not line: continue
            try:
                m = json.loads(line)
            except Exception:
                continue
            if m.get('type') == 'message' and m.get('runId'):
                conv_map[m['runId']] = cm

    rows = []
    for runid in sorted(os.listdir(os.path.join(SRC, 'runs'))):
        if not os.path.isdir(os.path.join(SRC, 'runs', runid)):
            continue
        meta = extract_run(runid)
        # 关联会话
        cm = conv_map.get(runid, {})
        meta['conversationTitle'] = cm.get('title')
        meta['conversationKind'] = cm.get('kind')
        meta['branchPurpose'] = cm.get('purpose')
        # 时间
        if meta.get('timestamps'):
            meta['startedAt'] = min(meta['timestamps'])
            meta['endedAt'] = max(meta['timestamps'])
        meta.pop('timestamps', None)
        # 状态推断
        ec = meta.get('exitCode')
        if meta.get('errors') or ec == 1:
            meta['status'] = 'fail'
        elif not meta.get('hasResponseMd'):
            meta['status'] = 'partial'
        elif ec == 0:
            meta['status'] = 'success'
        else:
            meta['status'] = 'unknown'
        # 清理 Counter -> dict
        meta['eventCounts'] = dict(meta['eventCounts'])
        meta['toolsTop'] = dict(meta['toolsTop'].most_common(10))
        with open(os.path.join(OUT, runid + '.json'), 'w', encoding='utf-8') as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)
        # 摘要行
        rows.append({
            'runId': runid,
            'conversationTitle': meta.get('conversationTitle'),
            'kind': meta.get('conversationKind'),
            'purpose': meta.get('branchPurpose'),
            'status': meta.get('status'),
            'startedAt': meta.get('startedAt'),
            'endedAt': meta.get('endedAt'),
            'durationMs': meta.get('durationMs'),
            'exitCode': meta.get('exitCode'),
            'inputTokens': (meta.get('usage') or {}).get('input'),
            'cacheRead': (meta.get('usage') or {}).get('cacheRead'),
            'model': meta.get('model'),
            'hasResponseMd': meta.get('hasResponseMd'),
            'errors': meta.get('errors'),
        })
    rows.sort(key=lambda r: r.get('startedAt') or '')
    with open(os.path.join(OUT, 'index.json'), 'w', encoding='utf-8') as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)

    # 汇报
    from collections import Counter as C
    status = C(r['status'] for r in rows)
    print(f"生成 {len(rows)} 个 run 的 meta.json 到 {OUT}")
    print(f"状态分布: {dict(status)}")
    print(f"提取到 usage 的 run: {sum(1 for r in rows if r['inputTokens'] is not None)}/{len(rows)}")
    print("失败/部分 run:")
    for r in rows:
        if r['status'] in ('fail', 'partial'):
            print(f"  {r['runId'][:8]} {r['status']}  title={r['conversationTitle']}  err={r['errors']}")

if __name__ == '__main__':
    build_index()