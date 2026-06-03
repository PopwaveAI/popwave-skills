"""检索：章纲映射 → 分书循环 → 四级回退 → 软去重 → 多样性排序。"""

from __future__ import annotations

import logging
import re
import sqlite3
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

DEFAULT_TOP_N = 3
PER_BOOK_LIMIT = 3             # 每本书独立召回 Top-K
MAX_PER_BOOK_IN_RESULT = 2     # 最终结果中每本书最多 2 条
DEDUP_RECENT_CHAPTERS = 5      # 去重窗口
FTS_MIN_QUERY_LEN = 4          # FTS 查询词最少字数（防 trigram 噪音）


@dataclass
class Candidate:
    id: int
    source_book: str
    chapter_number: int
    fragment_number: int
    content: str
    word_count: int
    quality_score: float
    match_score: float          # sum(confidence * weight)
    matched_tags: str           # 逗号分隔
    match_level: str = ""       # Level1 / Level2 / Level3 / Level4
    note: str = ""              # 重复使用等备注


# ---------- 工具 ----------

def extract_keywords(narrative: str) -> list[str]:
    """
    从章纲叙事功能字段提取关键词。

    目前策略：按常见分隔符（+、、,，空格）切分 + 去空白。
    后续可升级为 jieba 分词或 LLM 抽取。
    """
    parts = re.split(r"[+\s,，、/]+", narrative)
    return [p.strip() for p in parts if p.strip()]


def get_max_tag_version(conn: sqlite3.Connection) -> int:
    row = conn.execute("SELECT MAX(tag_version) FROM fragment_tags").fetchone()
    return row[0] if row and row[0] else 1


def get_recently_used_fragment_ids(
    conn: sqlite3.Connection, project: str, recent_n: int = DEDUP_RECENT_CHAPTERS
) -> set[int]:
    """取最近 N 章用过的片段 ID。"""
    rows = conn.execute(
        """
        SELECT DISTINCT fragment_id FROM usage_log
        WHERE project=?
        ORDER BY used_at DESC
        LIMIT ?
        """,
        (project, recent_n * 5),  # 每章估计 5 片段，留余量
    ).fetchall()
    return {row[0] for row in rows}


# ---------- 标签映射 ----------

def map_narrative_to_tags(
    conn: sqlite3.Connection, keywords: list[str], is_primary: int = 1
) -> dict[str, float]:
    """
    章纲关键词 → 标签 dict（tag → 最大 weight）。
    is_primary=1 走 Level1，0 走 Level2。
    """
    if not keywords:
        return {}

    placeholders = ",".join(["?"] * len(keywords))
    rows = conn.execute(
        f"""
        SELECT tag, MAX(weight) AS w FROM narrative_to_tag
        WHERE narrative_keyword IN ({placeholders}) AND is_primary=?
        GROUP BY tag
        """,
        (*keywords, is_primary),
    ).fetchall()
    return {row["tag"]: row["w"] for row in rows}


# ---------- 分书召回 ----------

def _retrieve_by_tags(
    conn: sqlite3.Connection,
    book: str,
    tag_weights: dict[str, float],
    tag_version: int,
    limit: int,
) -> list[Candidate]:
    """单本书按标签召回 Top-K。"""
    if not tag_weights:
        return []

    tags = list(tag_weights.keys())
    placeholders = ",".join(["?"] * len(tags))
    # 构造 CASE WHEN 来做 weight 加权
    weight_cases = " ".join(
        [f"WHEN t.tag=? THEN ?" for _ in tags]
    )
    weight_case_args: list = []
    for tag in tags:
        weight_case_args.extend([tag, tag_weights[tag]])

    sql = f"""
        SELECT
            f.id, f.source_book, f.chapter_number, f.fragment_number,
            f.content, f.word_count, f.quality_score,
            SUM(t.confidence * (CASE {weight_cases} ELSE 0 END)) AS match_score,
            GROUP_CONCAT(t.tag, ',') AS matched_tags
        FROM scene_fragments f
        JOIN fragment_tags t ON f.id = t.fragment_id
        WHERE f.source_book = ?
          AND t.tag IN ({placeholders})
          AND t.tag_version = ?
          AND f.word_count BETWEEN 500 AND 2000
        GROUP BY f.id
        ORDER BY match_score DESC, f.quality_score DESC, RANDOM()
        LIMIT ?
    """
    params = [*weight_case_args, book, *tags, tag_version, limit]
    rows = conn.execute(sql, params).fetchall()
    return [
        Candidate(
            id=r["id"],
            source_book=r["source_book"],
            chapter_number=r["chapter_number"],
            fragment_number=r["fragment_number"],
            content=r["content"],
            word_count=r["word_count"],
            quality_score=r["quality_score"],
            match_score=r["match_score"] or 0,
            matched_tags=r["matched_tags"] or "",
        )
        for r in rows
    ]


def _retrieve_by_fts(
    conn: sqlite3.Connection,
    book: str,
    query_text: str,
    limit: int,
) -> list[Candidate]:
    """FTS 降级召回（Level 3）。"""
    # FTS 查询词净化：过滤短词（< 4 字）
    terms = [t for t in re.split(r"\s+", query_text) if len(t) >= FTS_MIN_QUERY_LEN]
    if not terms:
        return []
    fts_query = " OR ".join(terms)

    rows = conn.execute(
        """
        SELECT
            f.id, f.source_book, f.chapter_number, f.fragment_number,
            f.content, f.word_count, f.quality_score
        FROM fragment_fts fts
        JOIN scene_fragments f ON fts.rowid = f.id
        WHERE fragment_fts MATCH ? AND f.source_book = ?
          AND f.word_count BETWEEN 500 AND 2000
        ORDER BY rank, f.quality_score DESC
        LIMIT ?
        """,
        (fts_query, book, limit),
    ).fetchall()
    return [
        Candidate(
            id=r["id"],
            source_book=r["source_book"],
            chapter_number=r["chapter_number"],
            fragment_number=r["fragment_number"],
            content=r["content"],
            word_count=r["word_count"],
            quality_score=r["quality_score"],
            match_score=0.0,
            matched_tags="",
            match_level="Level3",
        )
        for r in rows
    ]


# ---------- 多样性 + 软去重 ----------

def apply_diversity_and_dedup(
    candidates: list[Candidate],
    used_recently: set[int],
    top_n: int,
) -> list[Candidate]:
    """
    软去重策略（v3.3）：
    - 候选 >= 3*top_n 时硬过滤
    - 候选 >= top_n 时软降权
    - 候选 < top_n 时重复使用并标注
    同时应用"每本书最多 2 条"的多样性约束。
    """
    needed = top_n

    if not candidates:
        return []

    # 1. 去重处理
    if len(candidates) >= 3 * needed:
        # 硬过滤
        filtered = [c for c in candidates if c.id not in used_recently]
    elif len(candidates) >= needed:
        # 软降权
        filtered = list(candidates)
        for c in filtered:
            if c.id in used_recently:
                c.quality_score *= 0.5
                c.note = "已降权（近期用过）"
    else:
        # 不足：重复使用并标注
        filtered = list(candidates)
        for c in filtered:
            if c.id in used_recently:
                c.note = "⚠️ 重复使用（候选不足）"

    # 2. 按 (match_score, quality_score) 排序
    filtered.sort(key=lambda x: (-x.match_score, -x.quality_score))

    # 3. 多样性：每本书最多 MAX_PER_BOOK_IN_RESULT 条
    result: list[Candidate] = []
    per_book: dict[str, int] = {}
    for c in filtered:
        if per_book.get(c.source_book, 0) >= MAX_PER_BOOK_IN_RESULT:
            continue
        result.append(c)
        per_book[c.source_book] = per_book.get(c.source_book, 0) + 1
        if len(result) >= needed:
            break

    # 如果因多样性导致不足，补齐
    if len(result) < needed:
        for c in filtered:
            if c not in result:
                result.append(c)
                if len(result) >= needed:
                    break

    return result


# ---------- 主入口 ----------

def retrieve(
    conn: sqlite3.Connection,
    narrative: str,
    *,
    project: str = "default",
    top_n: int = DEFAULT_TOP_N,
    books: list[str] | None = None,
) -> list[Candidate]:
    """
    四级回退检索主入口。

    Args:
        narrative: 章纲叙事功能字段原文（如 "势均力敌战 + 营救"）
        project:   项目名（用于 usage_log 去重）
        top_n:     返回片段数
        books:     书列表（为 None 时自动从 DB 查所有书）
    """
    keywords = extract_keywords(narrative)
    logger.info("提取关键词: %s", keywords)

    if not books:
        rows = conn.execute(
            "SELECT DISTINCT source_book FROM scene_fragments"
        ).fetchall()
        books = [r[0] for r in rows]
    logger.info("检索范围: %s", books)

    tag_version = get_max_tag_version(conn)
    used = get_recently_used_fragment_ids(conn, project)

    # ---- Level 1: 精准标签匹配（分书循环）----
    primary_tags = map_narrative_to_tags(conn, keywords, is_primary=1)
    logger.info("Level1 精准标签: %s", primary_tags)
    if primary_tags:
        all_candidates: list[Candidate] = []
        for book in books:
            candidates = _retrieve_by_tags(
                conn, book, primary_tags, tag_version, PER_BOOK_LIMIT
            )
            for c in candidates:
                c.match_level = "Level1"
            all_candidates.extend(candidates)
        result = apply_diversity_and_dedup(all_candidates, used, top_n)
        if result:
            return result
        logger.info("Level1 未命中，回退 Level2")

    # ---- Level 2: 近似标签匹配 ----
    secondary_tags = map_narrative_to_tags(conn, keywords, is_primary=0)
    logger.info("Level2 近似标签: %s", secondary_tags)
    if secondary_tags:
        all_candidates = []
        for book in books:
            candidates = _retrieve_by_tags(
                conn, book, secondary_tags, tag_version, PER_BOOK_LIMIT
            )
            for c in candidates:
                c.match_level = "Level2"
            all_candidates.extend(candidates)
        result = apply_diversity_and_dedup(all_candidates, used, top_n)
        if result:
            return result
        logger.info("Level2 未命中，回退 Level3")

    # ---- Level 3: FTS 降级 ----
    long_keywords = [k for k in keywords if len(k) >= FTS_MIN_QUERY_LEN]
    if long_keywords:
        fts_query = " ".join(long_keywords)
        logger.info("Level3 FTS 查询: %s", fts_query)
        all_candidates = []
        for book in books:
            candidates = _retrieve_by_fts(conn, book, fts_query, PER_BOOK_LIMIT)
            all_candidates.extend(candidates)
        result = apply_diversity_and_dedup(all_candidates, used, top_n)
        if result:
            return result

    # ---- Level 4: 兜底 ----
    logger.warning("所有层级均未命中，返回空")
    return []


def log_usage(
    conn: sqlite3.Connection,
    project: str,
    chapter: str,
    candidates: list[Candidate],
) -> None:
    """写入 usage_log 供下次去重。"""
    for c in candidates:
        conn.execute(
            """
            INSERT INTO usage_log (project, chapter, fragment_id, recall_reason)
            VALUES (?, ?, ?, ?)
            """,
            (project, chapter, c.id, f"{c.match_level}:{c.matched_tags}"),
        )
