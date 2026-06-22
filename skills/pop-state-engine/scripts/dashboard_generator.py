#!/usr/bin/env python3
"""
仪表盘生成器 - 生成自包含 HTML 仪表盘

被 command_executor.py 的 _dump_dashboard() 调用。
查询 9 张 pop_ 前缀表，生成 5 面板 HTML 可视化。
"""

import json
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List


class DashboardGenerator:
    """生成自包含 HTML 仪表盘"""

    # ECharts CDN
    ECHARTS_CDN = "https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"

    # 9 张表
    TABLES = [
        ("pop_scenes_content", "场景内容", ["id", "chapter", "location", "characters"]),
        ("pop_scenes", "FTS5全文索引", ["chapter"]),
        ("pop_embeddings", "语义向量", ["scene_id"]),
        ("pop_summaries", "分层摘要", ["id", "level", "range_desc"]),
        ("pop_facts", "事实表", ["id", "entity", "attribute", "importance"]),
        ("pop_kg_nodes", "知识图谱节点", ["id", "type", "name"]),
        ("pop_kg_edges", "知识图谱边", ["id", "source", "target", "relation"]),
        ("pop_hooks", "伏笔追踪", ["id", "desc", "status", "priority"]),
        ("pop_arcs", "弧线/阶段", ["id", "title", "arc_type", "start_chapter"]),
    ]

    def __init__(self, db_path: str):
        self.db_path = db_path

    def _query(self, sql: str, params: tuple = ()) -> List[Dict]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        try:
            cur.execute(sql, params)
            rows = [dict(r) for r in cur.fetchall()]
        except sqlite3.OperationalError:
            rows = []
        conn.close()
        return rows

    def _query_one(self, sql: str, params: tuple = ()) -> Any:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        try:
            cur.execute(sql, params)
            row = cur.fetchone()
        except sqlite3.OperationalError:
            row = None
        conn.close()
        return dict(row) if row else None

    def _get_table_stats(self) -> List[Dict]:
        stats = []
        for table_name, display_name, preview_cols in self.TABLES:
            count_row = self._query_one(f"SELECT COUNT(*) as cnt FROM {table_name}")
            count = count_row["cnt"] if count_row else 0

            sample = []
            if count > 0:
                col_list = ", ".join(preview_cols)
                sample = self._query(f"SELECT {col_list} FROM {table_name} LIMIT 5")

            stats.append({
                "table": table_name,
                "display": display_name,
                "count": count,
                "sample": sample,
            })
        return stats

    def _get_kg_graph_data(self) -> Dict:
        nodes = self._query("SELECT id, type, name FROM pop_kg_nodes LIMIT 200")
        edges = self._query("SELECT source, target, relation FROM pop_kg_edges LIMIT 300")

        type_colors = {
            "character": "#5470c6",
            "location": "#91cc75",
            "faction": "#fac858",
            "item": "#ee6666",
            "skill": "#73c0de",
            "concept": "#3ba272",
            "event": "#fc8452",
        }

        echarts_nodes = []
        for n in nodes:
            echarts_nodes.append({
                "id": n["id"],
                "name": n["name"],
                "symbolSize": 30,
                "category": n["type"],
                "itemStyle": {"color": type_colors.get(n["type"], "#999")},
            })

        echarts_links = []
        for e in edges:
            echarts_links.append({
                "source": e["source"],
                "target": e["target"],
                "value": e["relation"],
            })

        categories = []
        seen_types = set()
        for n in nodes:
            if n["type"] not in seen_types:
                seen_types.add(n["type"])
                categories.append({"name": n["type"]})

        return {
            "nodes": echarts_nodes,
            "links": echarts_links,
            "categories": categories,
            "total_nodes": len(nodes),
            "total_edges": len(edges),
        }

    def _get_hooks_stats(self) -> Dict:
        status_rows = self._query(
            "SELECT status, COUNT(*) as cnt FROM pop_hooks GROUP BY status ORDER BY cnt DESC"
        )

        overdue = self._query("""
            SELECT id, desc, planted_chapter, expected_resolve, priority
            FROM pop_hooks
            WHERE status='open' AND expected_resolve IS NOT NULL
            AND expected_resolve < (
                SELECT COALESCE(MAX(chapter), 0) FROM pop_scenes_content
            )
            ORDER BY expected_resolve
            LIMIT 20
        """)

        priority_rows = self._query(
            "SELECT priority, COUNT(*) as cnt FROM pop_hooks WHERE status='open' GROUP BY priority ORDER BY cnt DESC"
        )

        return {
            "by_status": status_rows,
            "by_priority": priority_rows,
            "overdue": overdue,
        }

    def _get_facts_stats(self) -> Dict:
        total = self._query_one("SELECT COUNT(*) as cnt FROM pop_facts")
        active = self._query_one("SELECT COUNT(*) as cnt FROM pop_facts WHERE superseded_by IS NULL")
        superseded = self._query_one("SELECT COUNT(*) as cnt FROM pop_facts WHERE superseded_by IS NOT NULL")

        by_importance = self._query(
            "SELECT importance, COUNT(*) as cnt FROM pop_facts WHERE superseded_by IS NULL GROUP BY importance ORDER BY cnt DESC"
        )

        recent = self._query("""
            SELECT entity, attribute, value, chapter, created_at, superseded_by
            FROM pop_facts
            ORDER BY created_at DESC
            LIMIT 10
        """)

        return {
            "total": total["cnt"] if total else 0,
            "active": active["cnt"] if active else 0,
            "superseded": superseded["cnt"] if superseded else 0,
            "by_importance": by_importance,
            "recent": recent,
        }

    def _get_chapter_timeline(self) -> Dict:
        max_ch = self._query_one("SELECT MAX(chapter) as mx FROM pop_scenes_content")
        max_chapter = max_ch["mx"] if max_ch and max_ch["mx"] else 0

        if max_chapter == 0:
            return {"chapters": [], "max_chapter": 0}

        chapters = list(range(1, min(max_chapter + 1, 101)))

        timeline = []
        for ch in chapters:
            scenes = self._query_one(
                "SELECT COUNT(*) as cnt FROM pop_scenes_content WHERE chapter=?", (ch,)
            )
            facts = self._query_one(
                "SELECT COUNT(*) as cnt FROM pop_facts WHERE chapter=?", (ch,)
            )
            hooks = self._query_one(
                "SELECT COUNT(*) as cnt FROM pop_hooks WHERE planted_chapter=?", (ch,)
            )

            timeline.append({
                "chapter": ch,
                "scenes": scenes["cnt"] if scenes else 0,
                "facts": facts["cnt"] if facts else 0,
                "hooks": hooks["cnt"] if hooks else 0,
            })

        return {"chapters": timeline, "max_chapter": max_chapter}

    def generate(self) -> str:
        """生成自包含 HTML 仪表盘"""
        table_stats = self._get_table_stats()
        kg_data = self._get_kg_graph_data()
        hooks_stats = self._get_hooks_stats()
        facts_stats = self._get_facts_stats()
        timeline = self._get_chapter_timeline()

        generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 构建 JSON 数据
        data_json = json.dumps({
            "table_stats": table_stats,
            "kg_data": kg_data,
            "hooks_stats": hooks_stats,
            "facts_stats": facts_stats,
            "timeline": timeline,
        }, ensure_ascii=False, default=str)

        html = self._build_html(data_json, generated_at, table_stats, kg_data, hooks_stats, facts_stats, timeline)
        return html

    def _build_html(self, data_json: str, generated_at: str,
                    table_stats: List, kg_data: Dict, hooks_stats: Dict,
                    facts_stats: Dict, timeline: Dict) -> str:
        # 表概览 HTML
        table_rows = ""
        for t in table_stats:
            sample_html = ""
            if t["sample"]:
                first = t["sample"][0]
                sample_html = " | ".join(f"{k}: {str(v)[:40]}" for k, v in first.items() if v)
            table_rows += f"""
                <tr>
                    <td><code>{t['table']}</code></td>
                    <td>{t['display']}</td>
                    <td class="count-cell">{t['count']}</td>
                    <td class="sample-cell">{sample_html}</td>
                </tr>"""

        # 超期伏笔 HTML
        overdue_html = ""
        if hooks_stats["overdue"]:
            for h in hooks_stats["overdue"][:10]:
                overdue_html += f"""
                    <tr>
                        <td>{h.get('desc', '')[:50]}</td>
                        <td>ch{h.get('planted_chapter', '?')}</td>
                        <td class="overdue">ch{h.get('expected_resolve', '?')}</td>
                        <td>{h.get('priority', '')}</td>
                    </tr>"""
        else:
            overdue_html = '<tr><td colspan="4" class="empty">无超期伏笔</td></tr>'

        # 事实最近变更 HTML
        facts_recent_html = ""
        if facts_stats["recent"]:
            for f in facts_stats["recent"][:10]:
                status = "有效" if f.get("superseded_by") is None else "已替代"
                facts_recent_html += f"""
                    <tr>
                        <td>{f.get('entity', '')}</td>
                        <td>{f.get('attribute', '')}</td>
                        <td class="value-cell">{str(f.get('value', ''))[:40]}</td>
                        <td>ch{f.get('chapter', '?')}</td>
                        <td class="{ 'active-tag' if status == '有效' else 'superseded-tag' }">{status}</td>
                    </tr>"""
        else:
            facts_recent_html = '<tr><td colspan="5" class="empty">无事实记录</td></tr>'

        total_records = sum(t["count"] for t in table_stats)

        return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>pop-state-engine 仪表盘</title>
<script src="{self.ECHARTS_CDN}"></script>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, "Segoe UI", "Noto Sans CJK SC", sans-serif; background: #f5f5f5; color: #333; }}
.header {{ background: linear-gradient(135deg, #1a1a2e, #16213e); color: #fff; padding: 24px 32px; }}
.header h1 {{ font-size: 22px; font-weight: 600; }}
.header .meta {{ font-size: 13px; color: #8899aa; margin-top: 4px; }}
.header .summary {{ display: flex; gap: 24px; margin-top: 16px; }}
.header .stat {{ text-align: center; }}
.header .stat .num {{ font-size: 24px; font-weight: 700; color: #4fc3f7; }}
.header .stat .label {{ font-size: 12px; color: #8899aa; }}
.container {{ max-width: 1400px; margin: 0 auto; padding: 20px; }}
.panel {{ background: #fff; border-radius: 8px; padding: 20px; margin-bottom: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }}
.panel-title {{ font-size: 16px; font-weight: 600; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #e0e0e0; }}
.grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
.chart {{ width: 100%; height: 350px; }}
table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
th {{ text-align: left; padding: 8px 12px; background: #f8f9fa; border-bottom: 2px solid #e0e0e0; font-weight: 600; color: #555; }}
td {{ padding: 8px 12px; border-bottom: 1px solid #f0f0f0; }}
tr:hover {{ background: #f8f9fa; }}
.count-cell {{ font-weight: 700; color: #1976d2; text-align: center; }}
.sample-cell {{ color: #888; font-size: 12px; max-width: 300px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
.overdue {{ color: #e53935; font-weight: 600; }}
.empty {{ text-align: center; color: #aaa; padding: 20px; }}
.value-cell {{ max-width: 200px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
.active-tag {{ color: #43a047; font-weight: 600; }}
.superseded-tag {{ color: #999; }}
.overdue-list {{ max-height: 300px; overflow-y: auto; }}
@media (max-width: 900px) {{ .grid-2 {{ grid-template-columns: 1fr; }} }}
</style>
</head>
<body>

<div class="header">
    <h1>pop-state-engine 项目仪表盘</h1>
    <div class="meta">生成时间: {generated_at} | 数据库: {self.db_path}</div>
    <div class="summary">
        <div class="stat"><div class="num">{total_records}</div><div class="label">总记录数</div></div>
        <div class="stat"><div class="num">{kg_data['total_nodes']}</div><div class="label">图谱节点</div></div>
        <div class="stat"><div class="num">{kg_data['total_edges']}</div><div class="label">图谱边</div></div>
        <div class="stat"><div class="num">{facts_stats['active']}</div><div class="label">有效事实</div></div>
        <div class="stat"><div class="num">{sum(s['cnt'] for s in hooks_stats['by_status'] if s['status']=='open')}</div><div class="label">未回收伏笔</div></div>
        <div class="stat"><div class="num">{timeline['max_chapter']}</div><div class="label">最新章号</div></div>
    </div>
</div>

<div class="container">

    <!-- 面板1: 表概览 -->
    <div class="panel">
        <div class="panel-title">表概览</div>
        <table>
            <thead><tr><th>表名</th><th>说明</th><th>行数</th><th>样本预览</th></tr></thead>
            <tbody>{table_rows}</tbody>
        </table>
    </div>

    <!-- 面板2: 知识图谱 -->
    <div class="panel">
        <div class="panel-title">知识图谱可视化 ({kg_data['total_nodes']} 节点, {kg_data['total_edges']} 边)</div>
        <div id="chart-kg" class="chart" style="height:450px"></div>
    </div>

    <div class="grid-2">
        <!-- 面板3: 伏笔状态 -->
        <div class="panel">
            <div class="panel-title">伏笔状态分布</div>
            <div id="chart-hooks" class="chart"></div>
            <div class="panel-title" style="margin-top:16px;font-size:14px">超期伏笔</div>
            <div class="overdue-list">
                <table>
                    <thead><tr><th>描述</th><th>种入</th><th>预期回收</th><th>优先级</th></tr></thead>
                    <tbody>{overdue_html}</tbody>
                </table>
            </div>
        </div>

        <!-- 面板4: 事实版本链 -->
        <div class="panel">
            <div class="panel-title">事实版本链统计</div>
            <div id="chart-facts" class="chart"></div>
            <div class="panel-title" style="margin-top:16px;font-size:14px">最近变更</div>
            <table>
                <thead><tr><th>实体</th><th>属性</th><th>值</th><th>章</th><th>状态</th></tr></thead>
                <tbody>{facts_recent_html}</tbody>
            </table>
        </div>
    </div>

    <!-- 面板5: 按章时间线 -->
    <div class="panel">
        <div class="panel-title">按章时间线 (前{min(timeline['max_chapter'], 100)}章)</div>
        <div id="chart-timeline" class="chart" style="height:400px"></div>
    </div>

</div>

<script>
var rawData = {data_json};

// 面板2: 知识图谱
(function() {{
    var kg = rawData.kg_data;
    var chart = echarts.init(document.getElementById('chart-kg'));
    chart.setOption({{
        tooltip: {{}},
        legend: [{{ data: kg.categories.map(function(c) {{ return c.name; }}) }}],
        series: [{{
            type: 'graph',
            layout: 'force',
            data: kg.nodes,
            links: kg.links,
            categories: kg.categories,
            roam: true,
            label: {{ show: true, position: 'right', fontSize: 11 }},
            force: {{ repulsion: 100, edgeLength: 80 }},
            lineStyle: {{ color: '#aaa', curveness: 0.1 }},
            emphasis: {{ focus: 'adjacency', lineStyle: {{ width: 3 }} }}
        }}]
    }});
    window.addEventListener('resize', function() {{ chart.resize(); }});
}})();

// 面板3: 伏笔状态
(function() {{
    var hs = rawData.hooks_stats;
    var chart = echarts.init(document.getElementById('chart-hooks'));
    var statusData = hs.by_status.map(function(s) {{ return {{ name: s.status, value: s.cnt }}; }});
    var statusColors = {{ open: '#ff9800', resolved: '#4caf50', abandoned: '#9e9e9e' }};
    chart.setOption({{
        tooltip: {{ trigger: 'item' }},
        series: [{{
            type: 'pie',
            radius: ['40%', '70%'],
            data: statusData,
            itemStyle: {{ color: function(p) {{ return statusColors[p.name] || '#999'; }} }},
            label: {{ fontSize: 12 }}
        }}]
    }});
    window.addEventListener('resize', function() {{ chart.resize(); }});
}})();

// 面板4: 事实版本链
(function() {{
    var fs = rawData.facts_stats;
    var chart = echarts.init(document.getElementById('chart-facts'));
    chart.setOption({{
        tooltip: {{ trigger: 'axis' }},
        xAxis: {{ type: 'category', data: ['有效', '已替代', '总计'] }},
        yAxis: {{ type: 'value' }},
        series: [{{
            type: 'bar',
            data: [
                {{ value: fs.active, itemStyle: {{ color: '#4caf50' }} }},
                {{ value: fs.superseded, itemStyle: {{ color: '#ff9800' }} }},
                {{ value: fs.total, itemStyle: {{ color: '#2196f3' }} }}
            ],
            barWidth: '40%',
            label: {{ show: true, position: 'top' }}
        }}]
    }});
    window.addEventListener('resize', function() {{ chart.resize(); }});
}})();

// 面板5: 按章时间线
(function() {{
    var tl = rawData.timeline;
    var chart = echarts.init(document.getElementById('chart-timeline'));
    var chapters = tl.chapters.map(function(c) {{ return 'ch' + c.chapter; }});
    chart.setOption({{
        tooltip: {{ trigger: 'axis' }},
        legend: {{ data: ['场景', '事实', '伏笔'] }},
        xAxis: {{ type: 'category', data: chapters, axisLabel: {{ interval: Math.max(0, Math.floor(chapters.length / 20) - 1) }} }},
        yAxis: {{ type: 'value' }},
        series: [
            {{ name: '场景', type: 'bar', stack: 'total', data: tl.chapters.map(function(c) {{ return c.scenes; }}), itemStyle: {{ color: '#5470c6' }} }},
            {{ name: '事实', type: 'bar', stack: 'total', data: tl.chapters.map(function(c) {{ return c.facts; }}), itemStyle: {{ color: '#91cc75' }} }},
            {{ name: '伏笔', type: 'bar', stack: 'total', data: tl.chapters.map(function(c) {{ return c.hooks; }}), itemStyle: {{ color: '#fac858' }} }}
        ]
    }});
    window.addEventListener('resize', function() {{ chart.resize(); }});
}})();
</script>

</body>
</html>"""


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='生成 pop-state-engine HTML 仪表盘')
    parser.add_argument('--db-path', required=True, help='SQLite 数据库路径')
    parser.add_argument('--output', default='dashboard.html', help='输出 HTML 文件路径')
    args = parser.parse_args()

    gen = DashboardGenerator(args.db_path)
    html = gen.generate()
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(html, encoding='utf-8')
    print(f"仪表盘已生成: {args.output} ({len(html)} bytes)")
