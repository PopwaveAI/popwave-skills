#!/usr/bin/env python3
"""初始化 scene_fragments.db：建表、索引、narrative_to_tag 初始数据。

用法：
    python scripts/init_db.py                       # 建库（已存在则跳过）
    python scripts/init_db.py --reset               # 删库重建（危险）
    python scripts/init_db.py --cleanup-old-tag-versions  # 清理旧版标签
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent / ".env")  # 加载 fragment-pipeline/.env

sys.path.insert(0, str(Path(__file__).parent))

from _internal.db import get_conn, get_db_path, get_max_tag_version  # noqa: E402

# ---------- DDL ----------

DDL = [
    # 片段主表（v3.6：新增 scene_type / narrative_desc）
    """
    CREATE TABLE IF NOT EXISTS scene_fragments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_book TEXT NOT NULL,
        chapter_number INTEGER NOT NULL,
        fragment_number INTEGER NOT NULL,
        content TEXT NOT NULL,
        word_count INTEGER,
        quality_score REAL DEFAULT 0,
        scene_type TEXT,
        narrative_desc TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(source_book, chapter_number, fragment_number)
    )
    """,
    # 标签关联表（v3.3：主键加入 tag_version 支持双缓冲）
    """
    CREATE TABLE IF NOT EXISTS fragment_tags (
        fragment_id INTEGER NOT NULL,
        tag TEXT NOT NULL,
        confidence REAL DEFAULT 1.0,
        tag_version INTEGER NOT NULL DEFAULT 1,
        PRIMARY KEY (fragment_id, tag, tag_version),
        FOREIGN KEY (fragment_id) REFERENCES scene_fragments(id) ON DELETE CASCADE
    )
    """,
    # 章纲叙事功能 → 标签映射表（v3.3 补回）
    """
    CREATE TABLE IF NOT EXISTS narrative_to_tag (
        narrative_keyword TEXT NOT NULL,
        tag TEXT NOT NULL,
        weight REAL NOT NULL DEFAULT 1.0,
        is_primary INTEGER NOT NULL DEFAULT 1,
        PRIMARY KEY (narrative_keyword, tag)
    )
    """,
    # 全文检索（trigram 支持中文）
    """
    CREATE VIRTUAL TABLE IF NOT EXISTS fragment_fts USING fts5(
        content,
        content_rowid=id,
        tokenize='trigram'
    )
    """,
    # 使用记录
    """
    CREATE TABLE IF NOT EXISTS usage_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project TEXT NOT NULL,
        chapter TEXT NOT NULL,
        fragment_id INTEGER NOT NULL,
        recall_reason TEXT,
        used_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (fragment_id) REFERENCES scene_fragments(id)
    )
    """,
    # 索引
    "CREATE INDEX IF NOT EXISTS idx_book ON scene_fragments(source_book)",
    "CREATE INDEX IF NOT EXISTS idx_book_chap ON scene_fragments(source_book, chapter_number)",
    "CREATE INDEX IF NOT EXISTS idx_tag ON fragment_tags(tag, tag_version)",
    "CREATE INDEX IF NOT EXISTS idx_nm_keyword ON narrative_to_tag(narrative_keyword)",
    "CREATE INDEX IF NOT EXISTS idx_usage_frag ON usage_log(fragment_id, used_at)",
]

# 迁移语句：为已有 DB 补充新列（SQLite 不支持 IF NOT EXISTS，用 try/except 忽略已存在错误）
MIGRATIONS = [
    "ALTER TABLE scene_fragments ADD COLUMN scene_type TEXT",
    "ALTER TABLE scene_fragments ADD COLUMN narrative_desc TEXT",
    "CREATE INDEX IF NOT EXISTS idx_scene_type ON scene_fragments(source_book, scene_type)",
]

    # narrative_to_tag 初始数据（章纲叙事功能词 → 10类 scene_type + 权重）
INITIAL_NARRATIVE_MAP = [
    # (narrative_keyword, scene_type, weight, is_primary)
    # 战斗
    ("割草", "战斗", 2.0, 1),
    ("清剿", "战斗", 2.0, 1),
    ("清扫", "战斗", 1.5, 1),
    ("对战", "战斗", 2.0, 1),
    ("Boss", "战斗", 2.0, 1),
    ("处决", "战斗", 2.0, 1),
    ("行刑", "战斗", 2.0, 1),
    ("撤退", "战斗", 1.5, 0),
    ("突入", "战斗", 1.5, 1),
    ("营救", "战斗", 1.5, 0),
    # 成长
    ("修炼", "成长", 2.0, 1),
    ("练级", "成长", 2.0, 1),
    ("突破", "成长", 2.0, 1),
    ("顿悟", "成长", 2.0, 1),
    ("淬炼", "成长", 1.5, 1),
    ("习得", "成长", 1.5, 1),
    ("升级", "成长", 2.0, 1),
    ("面板", "成长", 2.0, 1),
    # 获取
    ("战利品", "获取", 2.0, 1),
    ("功法", "获取", 2.0, 1),
    ("装备", "获取", 1.5, 1),
    ("奖励", "获取", 1.5, 1),
    ("招募", "获取", 1.5, 0),
    # 立威
    ("示威", "立威", 2.0, 1),
    ("挑衅", "立威", 2.0, 1),
    ("震慑", "立威", 2.0, 1),
    ("立威", "立威", 2.0, 1),
    ("宣示", "立威", 1.5, 1),
    # 探索
    ("侦察", "探索", 2.0, 1),
    ("探索", "探索", 2.0, 1),
    ("行军", "探索", 1.5, 1),
    ("调查", "探索", 2.0, 1),
    ("新地点", "探索", 2.0, 1),
    ("追踪", "探索", 1.5, 1),
    # 仪式
    ("仪式", "仪式", 2.0, 1),
    ("植入", "仪式", 2.0, 1),
    ("改造", "仪式", 2.0, 1),
    ("觉醒", "仪式", 2.0, 1),
    ("融合", "仪式", 1.5, 1),
    ("转化", "仪式", 1.5, 1),
    # 对话
    ("对话", "对话", 2.0, 1),
    ("对质", "对话", 2.0, 1),
    ("谈判", "对话", 2.0, 1),
    ("交谈", "对话", 1.5, 1),
    # 情感
    ("日常", "情感", 2.0, 1),
    ("营地", "情感", 1.5, 1),
    ("情感", "情感", 2.0, 1),
    ("休整", "情感", 1.5, 1),
    ("牺牲", "情感", 1.5, 0),
    # 建设
    ("种田", "建设", 2.0, 1),
    ("扩张", "建设", 2.0, 1),
    ("建设", "建设", 2.0, 1),
    ("积累", "建设", 1.5, 1),
    ("培养", "建设", 1.5, 1),
]


def create_schema(reset: bool = False) -> None:
    db_path = get_db_path()
    if reset and db_path.exists():
        confirm = input(f"⚠️  确认删除 {db_path}? [y/N] ")
        if confirm.lower() != "y":
            print("已取消")
            return
        db_path.unlink()
        print(f"✓ 已删除 {db_path}")

    with get_conn() as conn:
        for stmt in DDL:
            conn.execute(stmt)
        # 迁移：为已有 DB 补充 v3.6 新列（忽略"column already exists"错误）
        for stmt in MIGRATIONS:
            try:
                conn.execute(stmt)
            except Exception:
                pass
        # 插入初始映射数据（INSERT OR IGNORE 保证幂等）
        conn.executemany(
            """
            INSERT OR IGNORE INTO narrative_to_tag
              (narrative_keyword, tag, weight, is_primary)
            VALUES (?, ?, ?, ?)
            """,
            INITIAL_NARRATIVE_MAP,
        )
    print(f"✓ DB 初始化完成: {db_path}")
    print(f"  - scene_fragments 表新增 scene_type / narrative_desc 字段（v3.6）")
    print(f"  - {len(INITIAL_NARRATIVE_MAP)} 条 narrative_to_tag 初始数据（10 类 scene_type）")


def cleanup_old_tag_versions() -> None:
    """清理旧版本的 fragment_tags（仅保留最大版本）。"""
    with get_conn() as conn:
        max_v = get_max_tag_version(conn)
        if max_v <= 1:
            print(f"当前最大 tag_version={max_v}，无需清理")
            return
        cnt = conn.execute(
            "SELECT COUNT(*) FROM fragment_tags WHERE tag_version < ?", (max_v,)
        ).fetchone()[0]
        confirm = input(
            f"⚠️  即将删除 {cnt} 条 tag_version < {max_v} 的旧标签，确认? [y/N] "
        )
        if confirm.lower() != "y":
            print("已取消")
            return
        conn.execute("DELETE FROM fragment_tags WHERE tag_version < ?", (max_v,))
        print(f"✓ 已清理 {cnt} 条旧版本标签，当前保留 tag_version={max_v}")


def main() -> None:
    ap = argparse.ArgumentParser(description="初始化 scene_fragments.db")
    ap.add_argument("--reset", action="store_true", help="删库重建（危险）")
    ap.add_argument(
        "--cleanup-old-tag-versions",
        action="store_true",
        help="清理 fragment_tags 中所有旧版本，仅保留最大版本",
    )
    args = ap.parse_args()

    if args.cleanup_old_tag_versions:
        cleanup_old_tag_versions()
    else:
        create_schema(reset=args.reset)


if __name__ == "__main__":
    main()
