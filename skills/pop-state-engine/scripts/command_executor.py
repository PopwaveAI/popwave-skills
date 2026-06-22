#!/usr/bin/env python3
"""
命令执行器 - pop-state-engine 统一命令入口
架构: 直接调用Python函数，无subprocess/param_map映射层
引擎实例缓存复用，消除进程启动开销和参数名映射bug

改编自 OnKos 项目，删除流程层命令（角色/质量/连续性/风格/情节），
新增 catalog / dump-dashboard / project-status 三个聚合命令。
"""

import sys
import os
import json
import sqlite3
import importlib
from pathlib import Path
from typing import Dict, Any

# 确保 vendor 的 jieba 可被 import（引擎自包含，不依赖外部 pip install）
_SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)


class CommandExecutor:
    """命令执行器 - 统一命令入口"""

    SCRIPTS_DIR = Path(__file__).parent

    # 英文别名 / 中文别名 → COMMAND_MAP 中的正式命令名
    ALIAS_MAP = {
        # 英文别名
        "help": "help", "write": "store-chapter", "store": "store-scene",
        "search": "search", "progress": "arc-progress",
        "suggest": "suggest-next", "status": "status",
        "fact": "get-fact", "stats": "mem-stats",
        "continue": "for-creation",
        "catalog": "catalog", "dashboard": "dump-dashboard",
        # 中文别名
        "帮助": "help", "指令列表": "help", "命令列表": "help",
        "写": "store-chapter", "续写": "for-creation",
        "存储": "store-scene", "搜索": "search",
        "查事实": "get-fact",
        "进度": "arc-progress",
        "建议": "suggest-next", "统计": "mem-stats",
        "状态": "status", "创建项目": "init",
        "创建阶段": "create-phase", "创建弧线": "create-arc-am",
        "提取实体": "extract-entities", "录入事实": "set-fact",
        "种伏笔": "plant-hook", "回收伏笔": "resolve-hook",
        "放弃伏笔": "abandon-hook", "更新摘要": "store-summary",
        "完成章节": "chapter-complete", "完成弧线": "complete-arc",
        "列出伏笔": "list-hooks", "列出弧线": "list-arcs",
        "列出节点": "list-nodes",
        "添加节点": "add-node", "添加关系": "add-edge",
        "查节点": "find-node", "查路径": "find-path", "查邻居": "get-neighbors",
        "相关事实": "relevant-facts", "伏笔统计": "hook-stats",
        "伏笔": "overdue-hooks", "矛盾": "detect-contradictions",
        "覆盖检查": "context-hierarchy", "预算": "budget-report",
        "获取上下文": "for-creation",
        "更新事实": "set-fact", "归档事实": "archive-facts",
        "查所有事实": "list-all-facts", "图谱统计": "kg-stats",
        "指令详情": "help",
        "目录": "catalog", "仪表盘": "dump-dashboard",
        "项目状态": "project-status",
        # 特殊符号
        "?": "help",
    }

    # 命令 → 模块/类/动作 映射
    COMMAND_MAP = {
        # 系统
        "help": {"module": "_builtin", "action": "help"},
        "catalog": {"module": "_builtin", "action": "catalog"},
        "dump-dashboard": {"module": "_builtin", "action": "dump-dashboard"},
        "project-status": {"module": "_builtin", "action": "project-status"},

        # 项目管理
        "init": {"module": "project_initializer", "class": "ProjectInitializer", "action": "init"},
        "status": {"module": "project_initializer", "class": "ProjectInitializer", "action": "status"},

        # 记忆引擎
        "store-chapter": {"module": "memory_engine", "class": "MemoryEngine", "action": "store-chapter"},
        "store-scene": {"module": "memory_engine", "class": "MemoryEngine", "action": "store-scene"},
        "delete-chapter-scenes": {"module": "memory_engine", "class": "MemoryEngine", "action": "delete-chapter-scenes"},
        "search": {"module": "memory_engine", "class": "MemoryEngine", "action": "search"},
        "store-summary": {"module": "memory_engine", "class": "MemoryEngine", "action": "store-summary"},
        "mem-stats": {"module": "memory_engine", "class": "MemoryEngine", "action": "stats"},
        "create-arc": {"module": "memory_engine", "class": "MemoryEngine", "action": "create-arc"},
        "list-arcs": {"module": "memory_engine", "class": "MemoryEngine", "action": "list-arcs"},
        "chapter-complete": {"module": "memory_engine", "class": "MemoryEngine", "action": "chapter-complete"},

        # 事实引擎
        "set-fact": {"module": "fact_engine", "class": "FactEngine", "action": "set-fact"},
        "get-fact": {"module": "fact_engine", "class": "FactEngine", "action": "get-fact"},
        "get-facts": {"module": "fact_engine", "class": "FactEngine", "action": "get-facts"},
        "relevant-facts": {"module": "fact_engine", "class": "FactEngine", "action": "relevant-facts"},
        "list-all-facts": {"module": "fact_engine", "class": "FactEngine", "action": "get-facts"},
        "get-relevant-facts": {"module": "fact_engine", "class": "FactEngine", "action": "relevant-facts"},
        "archive-facts": {"module": "fact_engine", "class": "FactEngine", "action": "archive-facts"},
        "supersede-chapter-facts": {"module": "fact_engine", "class": "FactEngine", "action": "supersede-chapter-facts"},
        "detect-contradictions": {"module": "fact_engine", "class": "FactEngine", "action": "detect-contradictions"},
        "fact-history": {"module": "fact_engine", "class": "FactEngine", "action": "fact-history"},

        # 知识图谱
        "add-node": {"module": "knowledge_graph", "class": "KnowledgeGraph", "action": "add-node"},
        "add-edge": {"module": "knowledge_graph", "class": "KnowledgeGraph", "action": "add-edge"},
        "find-node": {"module": "knowledge_graph", "class": "KnowledgeGraph", "action": "find-node"},
        "get-neighbors": {"module": "knowledge_graph", "class": "KnowledgeGraph", "action": "get-neighbors"},
        "find-path": {"module": "knowledge_graph", "class": "KnowledgeGraph", "action": "find-path"},
        "list-nodes": {"module": "knowledge_graph", "class": "KnowledgeGraph", "action": "list-nodes"},
        "kg-stats": {"module": "knowledge_graph", "class": "KnowledgeGraph", "action": "stats"},

        # 伏笔追踪
        "plant-hook": {"module": "hook_tracker", "class": "HookTracker", "action": "plant"},
        "resolve-hook": {"module": "hook_tracker", "class": "HookTracker", "action": "resolve"},
        "abandon-hook": {"module": "hook_tracker", "class": "HookTracker", "action": "abandon"},
        "abandon-chapter-hooks": {"module": "hook_tracker", "class": "HookTracker", "action": "abandon-chapter"},
        "list-hooks": {"module": "hook_tracker", "class": "HookTracker", "action": "list-open"},
        "overdue-hooks": {"module": "hook_tracker", "class": "HookTracker", "action": "overdue"},
        "forgotten-hooks": {"module": "hook_tracker", "class": "HookTracker", "action": "forgotten"},
        "hook-stats": {"module": "hook_tracker", "class": "HookTracker", "action": "stats"},

        # 弧线管理
        "create-phase": {"module": "arc_manager", "class": "ArcManager", "action": "create-phase"},
        "create-arc-am": {"module": "arc_manager", "class": "ArcManager", "action": "create-arc"},
        "complete-arc": {"module": "arc_manager", "class": "ArcManager", "action": "complete-arc"},
        "arc-progress": {"module": "arc_manager", "class": "ArcManager", "action": "progress"},
        "suggest-next": {"module": "arc_manager", "class": "ArcManager", "action": "suggest-next"},

        # 实体提取
        "extract-entities": {"module": "entity_extractor", "class": "EntityExtractor", "action": "extract"},

        # 上下文检索
        "for-creation": {"module": "context_retriever", "class": "ContextRetriever", "action": "for-creation"},
        "context-hierarchy": {"module": "context_retriever", "class": "ContextRetriever", "action": "hierarchy"},
        "budget-report": {"module": "context_retriever", "class": "ContextRetriever", "action": "budget-report"},

        # 内置命令
        "clear-chapter": {"module": "_builtin", "action": "clear-chapter"},
    }

    # 命令级参数重映射
    PARAM_MAP = {
        "extract-entities": {"content": "text"},
        "resolve-hook": {"how": "resolution", "id": "hook_id"},
        "plant-hook": {"desc": "description", "id": "hook_id"},
        "abandon-hook": {"id": "hook_id"},
        "abandon-chapter-hooks": {},
        "get-relevant-facts": {"chapter": "chapter"},
    }

    # 引擎构造参数：不同模块的初始化参数不同
    ENGINE_INIT_PARAMS = {
        "project_initializer": {"key": "project_path", "class": "ProjectInitializer"},
        "memory_engine": {"key": "db_path", "class": "MemoryEngine", "extra": {"project_path": "{project_path}"}},
        "fact_engine": {"key": "db_path", "class": "FactEngine", "extra": {"project_path": "{project_path}"}},
        "knowledge_graph": {"key": "db_path", "class": "KnowledgeGraph"},
        "hook_tracker": {"key": "db_path", "class": "HookTracker"},
        "arc_manager": {"key": "db_path", "class": "ArcManager", "extra": {"project_path": "{project_path}"}},
        "entity_extractor": {"key": "project_path", "class": "EntityExtractor"},
        "context_retriever": {"key": "db_path", "class": "ContextRetriever", "extra": {"project_path": "{project_path}"}},
    }

    # catalog: 表描述信息
    TABLE_DESCRIPTIONS = {
        "pop_scenes_content": {"desc": "场景内容（设计包入库）", "query_dims": ["chapter", "tags", "characters", "location"]},
        "pop_scenes": {"desc": "FTS5全文索引（自动同步）", "query_dims": ["content", "chapter", "characters"]},
        "pop_embeddings": {"desc": "ONNX语义向量（可选）", "query_dims": ["scene_id"]},
        "pop_summaries": {"desc": "6级分层摘要", "query_dims": ["level", "range_desc"]},
        "pop_facts": {"desc": "事实表（3级重要性+版本链）", "query_dims": ["entity", "attribute", "category", "importance", "chapter"]},
        "pop_kg_nodes": {"desc": "知识图谱节点", "query_dims": ["type", "name", "tags"]},
        "pop_kg_edges": {"desc": "知识图谱边", "query_dims": ["source", "target", "relation"]},
        "pop_hooks": {"desc": "伏笔追踪", "query_dims": ["status", "priority", "planted_chapter"]},
        "pop_arcs": {"desc": "弧线/阶段", "query_dims": ["arc_type", "phase_id", "start_chapter"]},
    }

    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self._engine_cache = {}
        self._module_cache = {}

    def _get_db_path(self) -> str:
        return str(self.project_path / "data" / "novel_memory.db")

    def _resolve_extra_kwargs(self, extra: dict) -> dict:
        resolved = {}
        for k, v in extra.items():
            if isinstance(v, str) and v == "{project_path}":
                resolved[k] = str(self.project_path)
            else:
                resolved[k] = v
        return resolved

    def _get_engine(self, module_name: str):
        if module_name in self._engine_cache:
            return self._engine_cache[module_name]

        if module_name not in self._module_cache:
            self._module_cache[module_name] = importlib.import_module(module_name)
        module = self._module_cache[module_name]

        class_name = self.ENGINE_INIT_PARAMS[module_name].get("class")
        if not class_name:
            import typing
            typing_attrs = set(dir(typing))
            for attr_name in dir(module):
                obj = getattr(module, attr_name)
                if (isinstance(obj, type) and not attr_name.startswith('_')
                        and attr_name not in typing_attrs
                        and hasattr(obj, '__module__')
                        and obj.__module__ != 'typing'):
                    class_name = attr_name
                    break
        cls = getattr(module, class_name)

        init_config = self.ENGINE_INIT_PARAMS[module_name]
        init_key = init_config["key"]
        init_kwargs = self._resolve_extra_kwargs(init_config.get("extra", {}))

        if init_key == "db_path":
            instance = cls(self._get_db_path(), **init_kwargs)
        elif init_key == "project_path":
            instance = cls(str(self.project_path), **init_kwargs)
        else:
            instance = cls(**init_kwargs)

        self._engine_cache[module_name] = instance
        return instance

    def _infer_chapter(self) -> int:
        try:
            engine = self._get_engine("fact_engine")
            chapter = engine.get_latest_chapter()
            return chapter if chapter > 0 else 1
        except Exception:
            return 1

    def execute(self, command: str, args: Dict[str, Any] = None) -> Dict[str, Any]:
        if command.startswith("/"):
            command = command[1:]
        command = self.ALIAS_MAP.get(command, command)

        cmd_info = self.COMMAND_MAP.get(command)
        if not cmd_info:
            return {"error": f"未知命令: {command}", "available": list(self.COMMAND_MAP.keys())}

        if cmd_info["module"] == "_builtin":
            action = cmd_info["action"]
            if action == "help":
                return self._help_output(args)
            if action == "clear-chapter":
                return self._clear_chapter(args)
            if action == "catalog":
                return self._catalog()
            if action == "dump-dashboard":
                return self._dump_dashboard(args)
            if action == "project-status":
                return self._project_status()
            return {"error": f"未知内置命令: {command}"}

        args = args or {}
        module_name = cmd_info["module"]
        action = cmd_info["action"]

        if command in self.PARAM_MAP:
            for from_key, to_key in self.PARAM_MAP[command].items():
                if from_key in args and to_key not in args:
                    args[to_key] = args.pop(from_key)

        try:
            engine = self._get_engine(module_name)
        except Exception as e:
            return {"error": f"引擎初始化失败: {str(e)}", "module": module_name}

        try:
            result = engine.execute_action(action, args)
            return result
        except ValueError as e:
            return {"error": str(e), "command": command}
        except TypeError as e:
            return {"error": f"参数错误: {str(e)}", "command": command}
        except Exception as e:
            return {"error": f"执行失败: {str(e)}", "command": command}

    def close(self):
        for engine in self._engine_cache.values():
            if hasattr(engine, 'close'):
                try:
                    engine.close()
                except Exception:
                    pass
        self._engine_cache.clear()

    def list_commands(self) -> Dict[str, str]:
        return {cmd: info.get("action", "") for cmd, info in self.COMMAND_MAP.items()}

    def _clear_chapter(self, args: Dict[str, Any] = None) -> Dict[str, Any]:
        args = args or {}
        chapter = args.get("chapter")
        if chapter is None:
            return {"error": "缺少 chapter 参数"}

        result = {"chapter": chapter}
        try:
            me = self._get_engine("memory_engine")
            deleted_scenes = me.delete_chapter_scenes(int(chapter))
            result["deleted_scenes"] = deleted_scenes
        except Exception as e:
            result["deleted_scenes"] = f"错误: {e}"

        try:
            fe = self._get_engine("fact_engine")
            superseded_facts = fe.supersede_chapter_facts(int(chapter))
            result["superseded_facts"] = superseded_facts
        except Exception as e:
            result["superseded_facts"] = f"错误: {e}"

        try:
            ht = self._get_engine("hook_tracker")
            abandoned_hooks = ht.abandon_chapter_hooks(int(chapter))
            result["abandoned_hooks"] = abandoned_hooks
        except Exception as e:
            result["abandoned_hooks"] = f"错误: {e}"

        return result

    def _help_output(self, args: Dict[str, Any] = None) -> Dict[str, Any]:
        detail_name = (args or {}).get("name", "")
        if detail_name:
            resolved = self.ALIAS_MAP.get(detail_name, detail_name)
            if resolved in self.COMMAND_MAP:
                info = self.COMMAND_MAP[resolved]
                return {"command": resolved, "action": info.get("action", ""),
                        "module": info.get("module", "")}
            return {"error": f"未找到指令: {detail_name}"}

        topic = (args or {}).get("topic", "")
        categories = {
            "系统": ["help", "catalog", "dump-dashboard", "project-status", "status", "clear-chapter"],
            "初始化": ["init", "add-node", "add-edge", "create-phase", "create-arc-am"],
            "存储": ["store-chapter", "store-scene", "store-summary", "chapter-complete", "delete-chapter-scenes"],
            "查询": ["get-fact", "get-facts", "search", "relevant-facts", "list-hooks", "list-arcs", "list-nodes", "find-node", "find-path", "get-neighbors", "fact-history"],
            "事实管理": ["set-fact", "archive-facts", "supersede-chapter-facts", "detect-contradictions"],
            "伏笔追踪": ["plant-hook", "resolve-hook", "abandon-hook", "abandon-chapter-hooks", "overdue-hooks", "forgotten-hooks", "hook-stats"],
            "弧线管理": ["arc-progress", "suggest-next", "complete-arc", "mem-stats", "kg-stats"],
            "上下文": ["for-creation", "context-hierarchy", "budget-report", "extract-entities"],
        }

        if topic and topic in categories:
            return {"topic": topic, "commands": categories[topic]}

        return {"type": "help", "categories": categories, "total_commands": len(self.COMMAND_MAP)}

    def _catalog(self) -> Dict[str, Any]:
        """运行时自描述：从 DB 实时生成表目录"""
        db_path = self._get_db_path()
        if not Path(db_path).exists():
            return {"error": "数据库不存在，请先执行 init", "db_path": db_path}

        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        tables = {}
        for table_name, desc_info in self.TABLE_DESCRIPTIONS.items():
            try:
                cur.execute(f"SELECT COUNT(*) as cnt FROM {table_name}")
                count = cur.fetchone()["cnt"]
            except sqlite3.OperationalError:
                count = 0

            sample = []
            if count > 0:
                try:
                    cur.execute(f"SELECT * FROM {table_name} LIMIT 3")
                    for row in cur.fetchall():
                        sample.append(dict(row))
                except sqlite3.OperationalError:
                    pass

            tables[table_name] = {
                "description": desc_info["desc"],
                "row_count": count,
                "queryable_dimensions": desc_info["query_dims"],
                "sample_data": sample,
            }

        # 分组统计
        group_stats = {}
        try:
            cur.execute("SELECT type, COUNT(*) as cnt FROM pop_kg_nodes GROUP BY type ORDER BY cnt DESC")
            group_stats["kg_nodes_by_type"] = [dict(r) for r in cur.fetchall()]
        except sqlite3.OperationalError:
            group_stats["kg_nodes_by_type"] = []

        try:
            cur.execute("SELECT importance, COUNT(*) as cnt FROM pop_facts WHERE superseded_by IS NULL GROUP BY importance ORDER BY cnt DESC")
            group_stats["facts_by_importance"] = [dict(r) for r in cur.fetchall()]
        except sqlite3.OperationalError:
            group_stats["facts_by_importance"] = []

        try:
            cur.execute("SELECT status, COUNT(*) as cnt FROM pop_hooks GROUP BY status ORDER BY cnt DESC")
            group_stats["hooks_by_status"] = [dict(r) for r in cur.fetchall()]
        except sqlite3.OperationalError:
            group_stats["hooks_by_status"] = []

        try:
            cur.execute("SELECT level, COUNT(*) as cnt FROM pop_summaries GROUP BY level ORDER BY cnt DESC")
            group_stats["summaries_by_level"] = [dict(r) for r in cur.fetchall()]
        except sqlite3.OperationalError:
            group_stats["summaries_by_level"] = []

        conn.close()

        quick_queries = [
            {"desc": "获取第N章创作上下文", "command": "for-creation", "params": {"chapter": "N"}},
            {"desc": "查找实体", "command": "find-node", "params": {"name": "实体名"}},
            {"desc": "查询实体属性", "command": "get-fact", "params": {"entity": "实体名", "attribute": "属性名"}},
            {"desc": "列出未回收伏笔", "command": "list-hooks", "params": {}},
            {"desc": "查看弧线进度", "command": "arc-progress", "params": {}},
            {"desc": "搜索场景", "command": "search", "params": {"query": "关键词"}},
            {"desc": "项目状态总览", "command": "project-status", "params": {}},
        ]

        return {
            "type": "catalog",
            "tables": tables,
            "group_stats": group_stats,
            "quick_queries": quick_queries,
            "total_tables": len(tables),
        }

    def _dump_dashboard(self, args: Dict[str, Any] = None) -> Dict[str, Any]:
        """生成自包含 HTML 仪表盘"""
        args = args or {}
        output_path = args.get("output", str(self.project_path / "data" / "dashboard.html"))

        try:
            from dashboard_generator import DashboardGenerator
            gen = DashboardGenerator(self._get_db_path())
            html = gen.generate()
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            Path(output_path).write_text(html, encoding="utf-8")
            return {"success": True, "output": output_path, "size_bytes": len(html.encode("utf-8"))}
        except ImportError:
            return {"error": "dashboard_generator 模块未找到"}
        except Exception as e:
            return {"error": f"生成仪表盘失败: {str(e)}"}

    def _project_status(self) -> Dict[str, Any]:
        """聚合查询：一次返回总控需要的所有数据"""
        db_path = self._get_db_path()
        if not Path(db_path).exists():
            return {"error": "数据库不存在，请先执行 init", "db_path": db_path}

        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        result = {}

        # 总章数/场景数
        try:
            cur.execute("SELECT MAX(chapter) as max_ch, COUNT(*) as cnt FROM pop_scenes_content")
            row = cur.fetchone()
            result["total_chapters"] = row["max_ch"] or 0
            result["total_scenes"] = row["cnt"]
        except sqlite3.OperationalError:
            result["total_chapters"] = 0
            result["total_scenes"] = 0

        # 下一章
        result["next_chapter"] = result["total_chapters"] + 1

        # 当前弧线
        try:
            cur.execute("""
                SELECT * FROM pop_arcs
                WHERE arc_type = 'arc' AND start_chapter <= ?
                AND (end_chapter IS NULL OR end_chapter >= ?)
                ORDER BY start_chapter DESC LIMIT 1
            """, (result["total_chapters"], result["total_chapters"]))
            row = cur.fetchone()
            result["current_arc"] = dict(row) if row else None
        except sqlite3.OperationalError:
            result["current_arc"] = None

        # 当前阶段
        try:
            cur.execute("""
                SELECT * FROM pop_arcs
                WHERE arc_type = 'phase' AND start_chapter <= ?
                AND (end_chapter IS NULL OR end_chapter >= ?)
                ORDER BY start_chapter DESC LIMIT 1
            """, (result["total_chapters"], result["total_chapters"]))
            row = cur.fetchone()
            result["active_phase"] = dict(row) if row else None
        except sqlite3.OperationalError:
            result["active_phase"] = None

        # 当前卷
        try:
            cur.execute("SELECT value FROM pop_facts WHERE entity='_meta' AND attribute='current_volume' AND superseded_by IS NULL")
            row = cur.fetchone()
            result["current_volume"] = int(row["value"]) if row else 1
        except (sqlite3.OperationalError, TypeError, ValueError):
            result["current_volume"] = 1

        # 主角状态
        try:
            cur.execute("SELECT value FROM pop_facts WHERE entity='_meta' AND attribute='protagonist_state' AND superseded_by IS NULL")
            row = cur.fetchone()
            result["protagonist_state"] = row["value"] if row else ""
        except sqlite3.OperationalError:
            result["protagonist_state"] = ""

        # 关键伏笔
        try:
            cur.execute("""
                SELECT desc, planted_chapter, expected_resolve, priority
                FROM pop_hooks WHERE status='open' AND priority='critical'
                ORDER BY planted_chapter LIMIT 5
            """)
            result["critical_hooks"] = [dict(r) for r in cur.fetchall()]
        except sqlite3.OperationalError:
            result["critical_hooks"] = []

        # 伏笔统计
        try:
            cur.execute("SELECT COUNT(*) as cnt FROM pop_hooks WHERE status='open'")
            result["open_hooks_count"] = cur.fetchone()["cnt"]
        except sqlite3.OperationalError:
            result["open_hooks_count"] = 0

        try:
            cur.execute("""
                SELECT COUNT(*) as cnt FROM pop_hooks
                WHERE status='open' AND expected_resolve IS NOT NULL
                AND expected_resolve < ?
            """, (result["total_chapters"],))
            result["overdue_hooks_count"] = cur.fetchone()["cnt"]
        except sqlite3.OperationalError:
            result["overdue_hooks_count"] = 0

        # 节点/事实计数
        try:
            cur.execute("SELECT COUNT(*) as cnt FROM pop_kg_nodes")
            result["kg_node_count"] = cur.fetchone()["cnt"]
        except sqlite3.OperationalError:
            result["kg_node_count"] = 0

        try:
            cur.execute("SELECT COUNT(*) as cnt FROM pop_facts WHERE superseded_by IS NULL")
            result["fact_count"] = cur.fetchone()["cnt"]
        except sqlite3.OperationalError:
            result["fact_count"] = 0

        conn.close()
        return {"type": "project-status", **result}


def main():
    import argparse
    parser = argparse.ArgumentParser(description="pop-state-engine 命令执行器")
    parser.add_argument("--project-path", "-p", required=True, help="项目根目录路径")
    parser.add_argument("--action", "-a", required=True, help="要执行的命令")
    parser.add_argument("--params", "-j", default="{}", help="命令参数 (JSON 字符串)")
    parser.add_argument("--output", "-o", default=None, help="输出文件路径 (仅 dump-dashboard)")

    args = parser.parse_args()

    try:
        params = json.loads(args.params) if args.params else {}
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"参数JSON解析失败: {e}"}, ensure_ascii=False))
        sys.exit(1)

    if args.output:
        params["output"] = args.output

    # 确保 scripts 目录在 sys.path 中
    scripts_dir = str(Path(__file__).parent)
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)

    executor = CommandExecutor(args.project_path)
    try:
        result = executor.execute(args.action, params)
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    finally:
        executor.close()


if __name__ == "__main__":
    main()
