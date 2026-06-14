"""
从 novel.db 生成知识图谱 HTML（力导向图，零外部依赖）
用法: python gen_html_knowledge_graph.py <novel.db 路径> [--out 输出路径]

Phase C 可选工具：基于 core_relationships 表生成 Force-Directed Graph，
节点 = 实体，边 = 关系，支持拖拽/缩放/点击查看详情。
"""
import sqlite3, json, os, sys, argparse, re

def gen_kg(db_path, out_path=None):
    if not os.path.exists(db_path):
        print(f"\u274c 文件不存在: {db_path}")
        sys.exit(1)

    if out_path is None:
        base = os.path.dirname(db_path)
        out_path = os.path.join(base, "知识图谱.html")

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("SELECT name, entity_type, first_ch, desc_text FROM core_entities ORDER BY entity_type")
    nodes_raw = [dict(r) for r in cur.fetchall()]

    cur.execute("SELECT subject, relation, object, ch, detail FROM core_relationships")
    edges_raw = [dict(r) for r in cur.fetchall()]

    conn.close()

    # 节点去重
    seen_names = {}
    nodes = []
    for n in nodes_raw:
        name = n["name"]
        if name not in seen_names:
            seen_names[name] = len(nodes)
            nodes.append({
                "id": name,
                "type": n["entity_type"] or "未知",
                "ch": n["first_ch"] or "",
                "desc": (n["desc_text"] or "")[:120]
            })

    # 边去重
    seen_edges = set()
    edges = []
    for e in edges_raw:
        key = (e["subject"], e["relation"], e["object"])
        if key not in seen_edges:
            seen_edges.add(key)
            edges.append({
                "source": e["subject"],
                "target": e["object"],
                "relation": e["relation"],
                "ch": e["ch"] or "",
                "detail": (e["detail"] or "")[:80]
            })

    COLOR_PALETTE = {
        "人物": "#e74c3c", "势力": "#2ecc71", "地域": "#3498db",
        "器物": "#f39c12", "功法": "#9b59b6", "法术": "#1abc9c",
        "丹药": "#e67e22", "境界": "#34495e", "事件": "#e84393",
        "设定": "#00b894", "生物": "#fd79a8", "果位": "#6c5ce7",
        "天地灵气": "#00cec9", "未知": "#636e72",
    }
    def get_color(t):
        return COLOR_PALETTE.get(t, "#636e72")

    payload = {"nodes": nodes, "edges": edges,
               "colors": {n["id"]: get_color(n["type"]) for n in nodes}}
    payload_json = json.dumps(payload, ensure_ascii=False)

    html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>知识图谱 · 实体关系网络</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,"Noto Sans SC","PingFang SC","Microsoft YaHei",sans-serif;background:#1a1a2e;color:#eee;overflow:hidden}
#canvas{display:block;width:100vw;height:100vh}
.sidebar{position:fixed;top:16px;left:16px;background:rgba(26,26,46,.92);border:1px solid rgba(255,255,255,.1);border-radius:12px;padding:16px;max-width:280px;z-index:100;backdrop-filter:blur(8px)}
.sidebar h2{font-size:13px;font-weight:400;letter-spacing:.06em;color:#888;margin-bottom:8px}
.sidebar .stats{font-size:11px;color:#666;margin-bottom:10px}
.legend{display:flex;flex-wrap:wrap;gap:4px 10px}
.legend-item{display:flex;align-items:center;gap:4px;font-size:11px;color:#aaa}
.legend-dot{width:8px;height:8px;border-radius:50%;display:inline-block}
.tooltip{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:rgba(26,26,46,.95);border:1px solid rgba(255,255,255,.15);border-radius:10px;padding:12px 20px;font-size:13px;z-index:100;text-align:center;max-width:500px;backdrop-filter:blur(8px);display:none;pointer-events:none}
.tooltip strong{color:#fff;font-weight:500}
.tooltip .meta{color:#888;font-size:11px;margin-top:2px}
.search-bar{position:fixed;top:16px;right:16px;z-index:100}
.search-bar input{padding:8px 14px;border:1px solid rgba(255,255,255,.15);border-radius:8px;background:rgba(26,26,46,.92);color:#eee;font-size:13px;outline:none;width:160px;backdrop-filter:blur(8px);font-family:inherit}
.search-bar input:focus{border-color:#6c5ce7}
.search-bar input::placeholder{color:#555}
.controls{position:fixed;bottom:24px;right:24px;z-index:100;display:flex;gap:6px}
.controls button{padding:6px 12px;border:1px solid rgba(255,255,255,.15);border-radius:6px;background:rgba(26,26,46,.92);color:#aaa;font-size:11px;cursor:pointer;backdrop-filter:blur(8px);font-family:inherit}
.controls button:hover{background:rgba(108,92,231,.3);color:#fff;border-color:#6c5ce7}
</style>
</head>
<body>
<div class="sidebar">
  <h2>\u{1f4ca} 知识图谱</h2>
  <div class="stats" id="stats">节点: 0 · 关系: 0</div>
  <div class="legend" id="legend"></div>
</div>
<div class="search-bar"><input id="searchBox" placeholder="搜索实体..." oninput="searchNode(this.value)"></div>
<div class="tooltip" id="tooltip"></div>
<div class="controls">
  <button onclick="resetZoom()">重置</button>
  <button onclick="toggleLabels()">标签</button>
</div>
<canvas id="canvas"></canvas>
<script>
const DATA = """ + payload_json + r""";
const COLORS = DATA.colors;
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
let width, height;
function resize() { width = canvas.width = window.innerWidth; height = canvas.height = window.innerHeight; }
resize();
window.addEventListener('resize', resize);

const neighbors = {};
DATA.edges.forEach(e => {
  (neighbors[e.source] = neighbors[e.source] || []).push(e);
  (neighbors[e.target] = neighbors[e.target] || []).push(e);
});

const ALPHA = 0.8, REPULSION = 8000, ATTRACTION = 0.005, DAMPING = 0.9, MIN_SPEED = 0.5;
const idMap = {};
const simNodes = DATA.nodes.map((n, i) => {
  const node = {
    id: n.id, type: n.type, ch: n.ch, desc: n.desc,
    x: Math.random() * width, y: Math.random() * height,
    vx: 0, vy: 0,
    radius: n.type === '人物' ? 8 : n.type === '势力' ? 10 : 6,
    color: COLORS[n.id] || '#636e72',
    fixed: false
  };
  idMap[n.id] = node;
  return node;
});
const nodeMap = {};
simNodes.forEach(n => nodeMap[n.id] = n);
const simEdges = DATA.edges.map(e => ({
  source: nodeMap[e.source], target: nodeMap[e.target],
  relation: e.relation, ch: e.ch, detail: e.detail
})).filter(e => e.source && e.target);

function center() {
  let cx = 0, cy = 0;
  simNodes.forEach(n => { cx += n.x; cy += n.y; });
  return { x: cx / simNodes.length, y: cy / simNodes.length };
}

let tick = 0;
function simulate() {
  const n = simNodes.length;
  if (n === 0) return false;
  for (let i = 0; i < n; i++) {
    for (let j = i + 1; j < n; j++) {
      let dx = simNodes[i].x - simNodes[j].x;
      let dy = simNodes[i].y - simNodes[j].y;
      let dist = Math.sqrt(dx * dx + dy * dy) || 1;
      let force = REPULSION / (dist * dist);
      let fx = (dx / dist) * force, fy = (dy / dist) * force;
      if (!simNodes[i].fixed) { simNodes[i].vx += fx; simNodes[i].vy += fy; }
      if (!simNodes[j].fixed) { simNodes[j].vx -= fx; simNodes[j].vy -= fy; }
    }
  }
  simEdges.forEach(e => {
    let dx = e.target.x - e.source.x, dy = e.target.y - e.source.y;
    let dist = Math.sqrt(dx * dx + dy * dy) || 1;
    let force = dist * ATTRACTION;
    let fx = (dx / dist) * force, fy = (dy / dist) * force;
    if (!e.source.fixed) { e.source.vx += fx; e.source.vy += fy; }
    if (!e.target.fixed) { e.target.vx -= fx; e.target.vy -= fy; }
  });
  const c = center();
  simNodes.forEach(node => {
    if (!node.fixed) { node.vx += (c.x - node.x) * 0.001; node.vy += (c.y - node.y) * 0.001; }
  });
  let maxSpeed = 0;
  simNodes.forEach(node => {
    if (!node.fixed) {
      node.vx *= DAMPING; node.vy *= DAMPING;
      let speed = Math.sqrt(node.vx * node.vx + node.vy * node.vy);
      if (speed > maxSpeed) maxSpeed = speed;
      node.x += node.vx; node.y += node.vy;
      node.x = Math.max(20, Math.min(width - 20, node.x));
      node.y = Math.max(20, Math.min(height - 20, node.y));
    }
  });
  tick++;
  return maxSpeed > MIN_SPEED;
}

let dragNode = null, hoverNode = null, showLabels = true, searchTerm = '';
let highlighted = new Set();

canvas.addEventListener('mousedown', e => {
  const node = findNode(e);
  if (node) { dragNode = node; node.fixed = true; }
});
canvas.addEventListener('mousemove', e => {
  const node = findNode(e);
  hoverNode = node;
  canvas.style.cursor = node ? 'pointer' : 'default';
  if (dragNode) { const r = canvas.getBoundingClientRect(); dragNode.x = e.clientX - r.left; dragNode.y = e.clientY - r.top; }
  updateTooltip(e);
});
canvas.addEventListener('mouseup', () => { dragNode = null; });
canvas.addEventListener('dblclick', e => { const node = findNode(e); if (node) node.fixed = false; });

function findNode(e) {
  const r = canvas.getBoundingClientRect();
  const mx = e.clientX - r.left, my = e.clientY - r.top;
  for (let i = simNodes.length - 1; i >= 0; i--) {
    const n = simNodes[i];
    const dx = mx - n.x, dy = my - n.y;
    if (dx * dx + dy * dy < (n.radius + 6) * (n.radius + 6)) return n;
  }
  return null;
}

function updateTooltip(e) {
  const tip = document.getElementById('tooltip');
  if (hoverNode && !dragNode) {
    const n = hoverNode;
    const rels = neighbors[n.id] || [];
    let relText = rels.slice(0, 6).map(r => r.source === n.id ? r.relation + ' \u2192 ' + r.target : r.source + ' \u2192 ' + r.relation).join(' \u00b7 ');
    if (rels.length > 6) relText += ' (+' + (rels.length - 6) + ')';
    tip.innerHTML = '<strong>' + n.id + '</strong> <span style="color:' + n.color + '">\u25cf</span> ' + n.type + (n.ch ? ' <span class="meta">' + n.ch + '</span>' : '') + (n.desc ? '<div style="color:#999;font-size:11px;margin-top:2px">' + n.desc + '</div>' : '') + (relText ? '<div style="color:#666;font-size:10px;margin-top:4px">' + relText + '</div>' : '');
    tip.style.display = 'block';
  } else { tip.style.display = 'none'; }
}

function searchNode(q) {
  searchTerm = q.toLowerCase().trim();
  highlighted.clear();
  if (searchTerm) DATA.nodes.forEach(n => { if (n.id.toLowerCase().includes(searchTerm)) highlighted.add(n.id); });
}
function resetZoom() { const c = center(); simNodes.forEach(n => { n.x += width/2 - c.x; n.y += height/2 - c.y; }); }
function toggleLabels() { showLabels = !showLabels; }

function render() {
  ctx.clearRect(0, 0, width, height);
  simEdges.forEach(e => { ctx.strokeStyle = 'rgba(255,255,255,0.06)'; ctx.beginPath(); ctx.moveTo(e.source.x, e.source.y); ctx.lineTo(e.target.x, e.target.y); ctx.stroke(); });
  simNodes.forEach(n => {
    const hi = highlighted.has(n.id);
    const r = hi ? n.radius + 4 : n.radius;
    if (hi) { ctx.shadowColor = n.color; ctx.shadowBlur = 16; }
    ctx.beginPath(); ctx.arc(n.x, n.y, r, 0, Math.PI * 2);
    ctx.fillStyle = n.color; ctx.globalAlpha = hi ? 1 : 0.85; ctx.fill(); ctx.globalAlpha = 1;
    ctx.strokeStyle = 'rgba(255,255,255,0.2)'; ctx.lineWidth = 1; ctx.stroke();
    ctx.shadowBlur = 0;
    if (showLabels && (hi || !searchTerm)) {
      ctx.fillStyle = 'rgba(255,255,255,0.7)'; ctx.font = '11px -apple-system, "Noto Sans SC", sans-serif';
      ctx.textAlign = 'center'; ctx.fillText(n.id, n.x, n.y + r + 14);
    }
  });
}

const typeCount = {};
DATA.nodes.forEach(n => { typeCount[n.type] = (typeCount[n.type] || 0) + 1; });
document.getElementById('stats').textContent = '节点: ' + DATA.nodes.length + ' · 关系: ' + DATA.edges.length;
const TYPE_COLORS = {"人物":"#e74c3c","势力":"#2ecc71","地域":"#3498db","器物":"#f39c12","功法":"#9b59b6","法术":"#1abc9c","丹药":"#e67e22","境界":"#34495e","事件":"#e84393","设定":"#00b894","生物":"#fd79a8","果位":"#6c5ce7","天地灵气":"#00cec9","未知":"#636e72"};
const legendEl = document.getElementById('legend');
Object.entries(typeCount).sort((a,b) => b[1] - a[1]).forEach(([t, c]) => {
  const div = document.createElement('div'); div.className = 'legend-item';
  div.innerHTML = '<span class="legend-dot" style="background:' + (TYPE_COLORS[t]||'#636e72') + '"></span>' + t + ' ' + c;
  legendEl.appendChild(div);
});

function loop() {
  const running = simulate();
  render();
  if (running || tick < 200) requestAnimationFrame(loop);
  else { function idle() { render(); requestAnimationFrame(idle); } idle(); }
}
loop();
setTimeout(resetZoom, 100);
</script>
</body>
</html>"""

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)

    print("=== 验证 ===")
    with open(out_path, "rb") as f:
        raw = f.read()
    text = raw.decode("utf-8")
    refs = re.findall(r'(?:src|href)=["\'](https?://[^"\']+)', text)
    print(f"  外部引用: {len(refs)} {'\u26a0\ufe0f' if refs else '\u2705'}")
    print(f"  </html>结尾: {'\u2705' if text.strip().endswith('</html>') else '\u274c'}")
    print(f"  双击可用: {'\u2705' if 'fetch(' not in text and 'require(' not in text else '\u274c'}")
    print(f"  大小: {len(text)//1024} KB | 节点: {len(nodes)} | 边: {len(edges)}")
    print(f"\n\u2705 {out_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="从 novel.db 生成知识图谱 HTML")
    parser.add_argument("db_path", help="novel.db 的路径")
    parser.add_argument("--out", default="", help="输出 HTML 路径")
    args = parser.parse_args()
    gen_kg(args.db_path, args.out or None)
