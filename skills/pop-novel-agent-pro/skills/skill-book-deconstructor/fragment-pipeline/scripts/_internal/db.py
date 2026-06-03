"""DB 连接与通用查询。"""

from __future__ import annotations

import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path

# 默认公共库路径（多项目共用）
DEFAULT_DB_PATH = Path("e:/AI小说/_shared/studio/scene_fragments.db")


def get_db_path() -> Path:
    """从环境变量或默认路径获取 DB 路径。"""
    env_path = os.environ.get("SCENE_FRAGMENTS_DB")
    if env_path:
        return Path(env_path).expanduser()
    return DEFAULT_DB_PATH


@contextmanager
def get_conn(db_path: Path | None = None):
    """获取 DB 连接（上下文管理器，自动 commit/close）。"""
    if db_path is None:
        db_path = get_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")   # 允许多读单写，并发性能更好
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


# ---------- 通用查询 ----------

def get_processed_chapters(conn: sqlite3.Connection, book_name: str) -> set[int]:
    """获取某本书已入库的章节号集合（用于 Step2 切割断点续跑）。"""
    rows = conn.execute(
        "SELECT DISTINCT chapter_number FROM scene_fragments WHERE source_book=?",
        (book_name,),
    ).fetchall()
    return {row[0] for row in rows}


def get_tagged_fragment_ids(
    conn: sqlite3.Connection, book_name: str, tag_version: int
) -> set[int]:
    """获取某本书在指定 tag_version 下已打标签的片段 ID 集合（用于 Step3 断点续跑）。"""
    rows = conn.execute(
        """
        SELECT DISTINCT ft.fragment_id FROM fragment_tags ft
        JOIN scene_fragments sf ON ft.fragment_id = sf.id
        WHERE sf.source_book=? AND ft.tag_version=?
        """,
        (book_name, tag_version),
    ).fetchall()
    return {row[0] for row in rows}


def get_max_tag_version(conn: sqlite3.Connection) -> int:
    """获取 fragment_tags 中最大的 tag_version（默认 1）。"""
    row = conn.execute("SELECT MAX(tag_version) FROM fragment_tags").fetchone()
    return row[0] if row and row[0] else 1
