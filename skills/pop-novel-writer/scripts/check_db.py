"""
check_db.py — DB 就绪检查层

职责：
  在流水线模块启动前，验证 DB 存在且具有预期的表结构。
  解决 "scene_fragments.db 版本不对或不存在" 这类无声断链问题。

用法：
  from glue.check_db import check_scene_fragments, check_novel_db

  # 检查拆书 DB（scene_fragments.db）
  check_scene_fragments("v2")       # 期望 v4.5 后的 schema
  # → 失败则 sys.exit(1)

  # 检查项目 novel.db
  check_novel_db("/path/to/project")
"""

import os
import sqlite3
import sys

# 确保 glue 包可导入（在 project_config.py 中会自动做一次）
_GLUE_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_GLUE_PARENT = os.path.dirname(_GLUE_SCRIPT_DIR)
if _GLUE_PARENT not in sys.path:
    sys.path.insert(0, _GLUE_PARENT)

from glue.project_config import resolve_shared, resolve_path


# ─── Schema 版本定义 ──────────────────────────────────

# v1: 旧版（build_fragments.py 写入，14 个字段）
_SCHEMA_V1 = {
    "scene_fragments": [
        "id", "source_book", "chapter_number", "fragment_number",
        "scene_type", "scene_subtype", "fragment_label",
        "content", "char_start", "char_end",
        "keywords", "tags", "summary", "created_at",
    ],
}

# v2: 新增 v4.5 book-deconstructor 增强字段
_SCHEMA_V2 = {
    "scene_fragments": [
        "id", "source_book", "chapter_number", "fragment_number",
        "scene_type", "scene_subtype", "fragment_label",
        "content", "char_start", "char_end",
        "keywords", "tags", "summary", "created_at",
        # v4.5 新增字段
        "rule", "quality_gate", "dimension", "rule_id",
    ],
    # 可选表
    "beat_sequences": ["id", "book_id", "seq_label", "ch_start", "ch_end",
                       "sequence", "first_payoff_ch", "daily_avg", "notes"],
    "reference_samples": ["id", "source_book", "chapter_number",
                          "scene_type", "scene_subtype", "sample_text", "notes"],
}


# ─── 场景片段 DB (共享) ─────────────────────────────


def check_scene_fragments(expected_version: str = "v2", verbose: bool = True) -> bool:
    """检查 scene_fragments.db 存在且具有预期的表结构"""
    db_path = resolve_shared("scene_fragments_db")
    schema = _SCHEMA_V2 if expected_version == "v2" else _SCHEMA_V1

    if not os.path.isfile(db_path):
        print(f"[glue] ❌ scene_fragments.db 不存在: {db_path}")
        print(f"[glue]    运行 skill-book-deconstructor/fragment-pipeline/scripts/init_db.py")
        return False

    conn = sqlite3.connect(db_path)
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
    actual_tables = {row[0] for row in cursor.fetchall()}

    all_ok = True
    for table, expected_cols in schema.items():
        if table not in actual_tables:
            if verbose:
                print(f"[glue] ❌ 缺少表: {table}")
            all_ok = False
            continue

        cursor = conn.execute(f"PRAGMA table_info({table})")
        actual_cols = {row[1] for row in cursor.fetchall()}
        missing = [c for c in expected_cols if c not in actual_cols]
        if missing:
            if verbose:
                print(f"[glue] ❌ 表 {table} 缺少字段: {missing}")
            all_ok = False

    conn.close()

    if all_ok and verbose:
        print(f"[glue] ✅ scene_fragments.db schema v{expected_version} 就绪")
        print(f"      路径: {db_path}")
    return all_ok


# ─── 项目 novel.db ────────────────────────────────


def check_novel_db(project_dir: str, verbose: bool = True) -> bool:
    """
    检查项目的 novel.db 是否存在且包含核心表。
    核心表: facts, state, sessions

    从 project.yaml 的 paths.database 读取路径，未配置则尝试默认 04-数据库/。
    """
    # 从 project.yaml 获取路径，未配置则尝试默认路径
    try:
        db_dir = resolve_path(project_dir, "database")
    except KeyError:
        db_dir = os.path.join(project_dir, "04-数据库")
        if verbose:
            print(f"[glue] ⚠️  project.yaml 未定义 database 路径，尝试默认 04-数据库/")

    if not os.path.isdir(db_dir):
        if verbose:
            print(f"[glue] ❌ 数据库目录不存在: {db_dir}")
        return False

    db_path = os.path.join(db_dir, "novel.db")
    if not os.path.isfile(db_path):
        if verbose:
            print(f"[glue] ❌ novel.db 不存在: {db_path}")
        return False

    conn = sqlite3.connect(db_path)
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = {row[0] for row in cursor.fetchall()}

    required = {"facts", "state", "sessions"}
    missing = required - tables
    conn.close()

    if missing:
        if verbose:
            print(f"[glue] ❌ novel.db 缺少核心表: {missing}")
        return False

    if verbose:
        print(f"[glue] ✅ novel.db 就绪 ({len(tables)} 张表)")
    return True


# ─── v3.db (项目设定数据库) ──────────────────────


def check_v3db(project_dir: str, verbose: bool = True) -> dict:
    """
    检查 v3.db 存在且包含核心表。

    核心表: characters, weirds, state_changelog

    返回:
        dict: {status, tables_found, errors}
    """
    result = {"status": False, "tables_found": [], "errors": []}

    # 从 project.yaml 的 paths.database 读取 v3.db 路径
    try:
        db_dir = resolve_path(project_dir, "database")
    except KeyError:
        # 如果没定义，拼接 04-数据库/ 下找 *v3*.db
        db_dir = os.path.join(project_dir, "04-数据库")

    if not os.path.isdir(db_dir):
        result["errors"].append(f"数据库目录不存在: {db_dir}")
        return result

    # 在目录中查找 *v3*.db 文件
    db_path = None
    # 精确匹配优先：v3.db / v3_main.db
    for fname in ["v3.db", "v3_main.db"]:
        candidate = os.path.join(db_dir, fname)
        if os.path.isfile(candidate):
            db_path = candidate
            break
    # 回退：文件名含 v3 的 .db 文件
    if not db_path:
        for f in os.listdir(db_dir):
            if "v3" in f.lower() and f.endswith(".db"):
                db_path = os.path.join(db_dir, f)
                break

    if not db_path or not os.path.isfile(db_path):
        result["errors"].append(f"v3.db 未找到（搜索目录: {db_dir}）")
        return result

    if verbose:
        print(f"[glue]    v3.db 路径: {db_path}")

    # 连接并检查核心表
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = {row[0] for row in cursor.fetchall()}
        conn.close()
    except Exception as e:
        result["errors"].append(f"无法连接 v3.db: {e}")
        return result

    result["tables_found"] = sorted(tables)
    required = {"characters", "weirds", "state_changelog"}
    missing = required - tables

    if missing:
        result["errors"].append(f"v3.db 缺少核心表: {missing}")
        if verbose:
            print(f"[glue] ❌ v3.db 缺少核心表: {missing}（现有: {sorted(tables)}）")
    else:
        result["status"] = True
        if verbose:
            print(f"[glue] ✅ v3.db 就绪（{len(tables)} 张表: {sorted(tables)}）")

    return result


# ─── 总检查 ──────────────────────────────────────


def check_all(project_dir: str, verbose: bool = True) -> bool:
    """跑所有 DB 检查"""
    ok = True

    # scene_fragments.db (P0 — 核心流水线依赖)
    if not check_scene_fragments(verbose=verbose):
        ok = False

    # novel.db (可选 — 不影响核心写作)
    if not check_novel_db(project_dir, verbose=verbose):
        ok = False

    # v3.db (P1 — 项目设定依赖)
    v3_result = check_v3db(project_dir, verbose=verbose)
    if not v3_result["status"]:
        ok = False

    return ok


# ─── CLI ─────────────────────────────────────────


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="检查数据库就绪状态")
    parser.add_argument("--project-dir", help="项目根目录（检查 novel.db / v3.db 时需要）")
    parser.add_argument("--check", choices=["scene_fragments", "novel", "v3", "all"],
                        default="all", help="检查目标")
    parser.add_argument("--schema-version", choices=["v1", "v2"], default="v2",
                        help="期望的 scene_fragments.db schema 版本")

    args = parser.parse_args()

    if args.check in ("scene_fragments", "all"):
        ok_sf = check_scene_fragments(args.schema_version)
        if not ok_sf:
            sys.exit(1)

    if args.check in ("novel", "all") and args.project_dir:
        ok_novel = check_novel_db(args.project_dir)
        if not ok_novel:
            sys.exit(1)

    if args.check in ("v3", "all"):
        if not args.project_dir:
            print("[glue] ❌ 检查 v3.db 需要 --project-dir 参数")
            sys.exit(1)
        v3_result = check_v3db(args.project_dir)
        if not v3_result["status"]:
            print(f"[glue] ❌ v3.db 检查不通过:")
            for e in v3_result["errors"]:
                print(f"       {e}")
            sys.exit(1)

    print(f"\n[glue] ✅ DB 检查全部通过")
