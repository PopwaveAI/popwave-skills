#!/usr/bin/env python3
"""清洗 + LLM 合并切割打标 + 入库（v3.7 单阶段并发版）。

用法：
    # 全量构建（默认 10 并发）
    python scripts/build_fragments.py --book "深渊主宰"

    # 试点（仅前 50 章）
    python scripts/build_fragments.py --book "深渊主宰" --chapter-range 1-50

    # 调整并发数（保守=5，激进=20）
    python scripts/build_fragments.py --book "深渊主宰" --workers 5

    # 仅重打标签（Prompt 迭代后，双缓冲不影响线上）
    python scripts/build_fragments.py --book "深渊主宰" --retag-only --tag-version 2

    # 断点续跑：直接重新执行同一命令，已完成章节自动跳过

并发架构（v3.7）：
    单阶段：asyncio.Semaphore(workers) 并发调用合并 Prompt
            每章完成后立即写入 DB（asyncio.Lock 串行化 SQLite 写操作）
            较 v3.6 减少 ~75% API 调用次数，无两阶段等待开销
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import sqlite3
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).parent))

from _internal.cleaner import load_and_split  # noqa: E402
from _internal.combined import CombinedFragment, split_and_tag_async  # noqa: E402
from _internal.db import get_conn, get_db_path, get_processed_chapters, get_tagged_fragment_ids  # noqa: E402
from _internal.llm_client import LLMClient  # noqa: E402
from _internal.quality import calc_quality_score  # noqa: E402
from _internal.tagger import tag_batch_async  # noqa: E402

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("build_fragments")

CONFIG_PATH = Path(__file__).parent.parent / "config" / "books.yaml"

BATCH_SIZE = 4   # --retag-only 时每批片段数
COMMIT_EVERY = 50


# ── 配置 ─────────────────────────────────────────────────────────────────────

def load_book_config(book_name: str) -> dict:
    cfg = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))
    for book in cfg["books"]:
        if book["name"] == book_name:
            return book
    raise ValueError(f"未在 config/books.yaml 中找到书 '{book_name}'")


def parse_chapter_range(s: str | None) -> tuple[int, int] | None:
    if not s:
        return None
    parts = s.split("-")
    if len(parts) != 2:
        raise ValueError(f"--chapter-range 格式错误，应为 'N-M'，收到 '{s}'")
    return int(parts[0]), int(parts[1])


# ── DB 写入（串行，每章 commit）────────────────────────────────────────────────

def _write_chapter(
    conn: sqlite3.Connection,
    book_name: str,
    chapter_number: int,
    fragments: list[CombinedFragment],
    tag_version: int,
) -> int:
    """将一章的切割+打标结果原子写入 DB，返回写入片段数。"""
    written = 0
    for idx, frag in enumerate(fragments, start=1):
        wc = len(frag.content)
        score = calc_quality_score(frag.content)

        # UPSERT：保留已有行的 id（避免 DELETE+INSERT 导致 FK 失效）
        conn.execute(
            """
            INSERT INTO scene_fragments
              (source_book, chapter_number, fragment_number,
               content, word_count, quality_score,
               scene_type, narrative_desc, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(source_book, chapter_number, fragment_number) DO UPDATE SET
              content        = excluded.content,
              word_count     = excluded.word_count,
              quality_score  = excluded.quality_score,
              scene_type     = excluded.scene_type,
              narrative_desc = excluded.narrative_desc,
              updated_at     = CURRENT_TIMESTAMP
            """,
            (book_name, chapter_number, idx,
             frag.content, wc, score,
             frag.scene_type, frag.narrative_desc),
        )

        row = conn.execute(
            "SELECT id FROM scene_fragments WHERE source_book=? AND chapter_number=? AND fragment_number=?",
            (book_name, chapter_number, idx),
        ).fetchone()
        if not row:
            logger.error("写入后查不到 fragment(%s, %d, %d)", book_name, chapter_number, idx)
            continue
        frag_id = row[0]

        for kw in frag.tags:
            conn.execute(
                """
                INSERT OR REPLACE INTO fragment_tags
                  (fragment_id, tag, confidence, tag_version)
                VALUES (?, ?, 1.0, ?)
                """,
                (frag_id, kw, tag_version),
            )

        tr = frag.to_tag_result()
        fts_text = tr.fts_text(frag.content)
        conn.execute(
            "INSERT OR REPLACE INTO fragment_fts(rowid, content) VALUES (?, ?)",
            (frag_id, fts_text),
        )
        written += 1

    conn.commit()
    return written


# ── 重打标签（--retag-only 专用）────────────────────────────────────────────

def _write_retag(
    conn: sqlite3.Connection,
    fragment_id: int,
    fragment_content: str,
    tag_result,
    tag_version: int,
) -> None:
    from _internal.tagger import TagResult  # noqa: F401
    conn.execute(
        "UPDATE scene_fragments SET scene_type=?, narrative_desc=?, updated_at=CURRENT_TIMESTAMP WHERE id=?",
        (tag_result.scene_type, tag_result.narrative_desc, fragment_id),
    )
    for kw in tag_result.tags:
        conn.execute(
            "INSERT OR REPLACE INTO fragment_tags (fragment_id, tag, confidence, tag_version) VALUES (?, ?, 1.0, ?)",
            (fragment_id, kw, tag_version),
        )
    fts_text = tag_result.fts_text(fragment_content)
    conn.execute(
        "INSERT OR REPLACE INTO fragment_fts(rowid, content) VALUES (?, ?)",
        (fragment_id, fts_text),
    )


# ── 主流程（单阶段并发）──────────────────────────────────────────────────────

async def _run_build_async(
    book_name: str,
    chapters: list[tuple[int, str, str]],
    llm: LLMClient,
    tag_version: int,
    workers: int,
) -> None:
    db_path = get_db_path()
    logger.info("DB: %s", db_path)

    with get_conn(db_path) as conn:
        processed = get_processed_chapters(conn, book_name)
        logger.info("[断点续跑] 已完成章节: %d", len(processed))

    pending = [(n, t, tx) for n, t, tx in chapters if n not in processed]
    if not pending:
        logger.info("所有章节已处理完毕")
        return
    logger.info("待处理章节: %d（并发=%d）", len(pending), workers)

    sem = asyncio.Semaphore(workers)
    db_lock = asyncio.Lock()
    done_count = 0
    total = len(pending)
    total_frags = 0

    async def process_chapter(ch_num: int, ch_title: str, ch_text: str) -> None:
        nonlocal done_count, total_frags
        async with sem:
            logger.info("  ✂ 第 %d 章「%s」(%d字)", ch_num, ch_title, len(ch_text))
            frags = await split_and_tag_async(ch_text, llm)

        if not frags:
            logger.warning("  第 %d 章切割结果为空，跳过", ch_num)
        else:
            async with db_lock:
                with get_conn(db_path) as conn:
                    n = _write_chapter(conn, book_name, ch_num, frags, tag_version)
                    total_frags += n

        done_count += 1
        if done_count % 10 == 0 or done_count == total:
            logger.info("  进度 %d/%d，累计写入片段 %d", done_count, total, total_frags)

    tasks = [process_chapter(n, t, tx) for n, t, tx in pending]
    await asyncio.gather(*tasks, return_exceptions=True)

    logger.info("✓ [%s] 构建完成，共写入 %d 片段", book_name, total_frags)


# ── 重打标签流程 ──────────────────────────────────────────────────────────────

async def _run_retag_async(
    book_name: str,
    chapter_range: tuple[int, int] | None,
    llm: LLMClient,
    tag_version: int,
    workers: int,
) -> None:
    db_path = get_db_path()
    logger.info("[重打标签] book=%s, tag_version=%d", book_name, tag_version)

    with get_conn(db_path) as conn:
        if chapter_range:
            lo, hi = chapter_range
            rows = conn.execute(
                "SELECT id, content FROM scene_fragments WHERE source_book=? AND chapter_number BETWEEN ? AND ?",
                (book_name, lo, hi),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT id, content FROM scene_fragments WHERE source_book=?",
                (book_name,),
            ).fetchall()
        already = get_tagged_fragment_ids(conn, book_name, tag_version)

    frag_jobs = [(r[0], r[1]) for r in rows if r[0] not in already]
    logger.info("待重打: %d（已完成: %d）", len(frag_jobs), len(already))
    if not frag_jobs:
        logger.info("无待处理片段")
        return

    batches = [frag_jobs[i: i + BATCH_SIZE] for i in range(0, len(frag_jobs), BATCH_SIZE)]
    sem = asyncio.Semaphore(workers)
    db_lock = asyncio.Lock()
    done_count = 0

    async def tag_batch(batch: list[tuple[int, str]]) -> None:
        nonlocal done_count
        async with sem:
            contents = [c for _, c in batch]
            tag_results = await tag_batch_async(contents, llm)

        async with db_lock:
            with get_conn(db_path) as conn:
                for (frag_id, content), tr in zip(batch, tag_results):
                    if tr is None:
                        logger.warning("  片段 #%d 打标失败", frag_id)
                        continue
                    _write_retag(conn, frag_id, content, tr, tag_version)
                conn.commit()

        done_count += 1
        if done_count % COMMIT_EVERY == 0 or done_count == len(batches):
            logger.info("  [重打标签] 进度 %d/%d 批", done_count, len(batches))

    await asyncio.gather(*[tag_batch(b) for b in batches], return_exceptions=True)
    logger.info("✓ [%s] 重打标签完成", book_name)


# ── CLI ───────────────────────────────────────────────────────────────────────

def main() -> None:
    ap = argparse.ArgumentParser(description="构建 scene_fragments 库（v3.7 单阶段并发）")
    ap.add_argument("--book", required=True, help="参考书名（与 books.yaml 匹配）")
    ap.add_argument("--chapter-range", help="章节范围，如 '1-50'。不指定则全量")
    ap.add_argument(
        "--workers",
        type=int,
        default=10,
        help="并发 API 请求数（默认 10；免费额度建议 5，高配额可设 20）",
    )
    ap.add_argument(
        "--retag-only",
        action="store_true",
        help="仅重打标签，不重切片段（双缓冲，旧版本保留）",
    )
    ap.add_argument(
        "--tag-version",
        type=int,
        default=1,
        help="标签版本号（与 LLM Prompt 版本对应，重打时递增）",
    )
    args = ap.parse_args()

    rng = parse_chapter_range(args.chapter_range)
    book = load_book_config(args.book)
    llm = LLMClient()

    if args.retag_only:
        asyncio.run(_run_retag_async(args.book, rng, llm, args.tag_version, args.workers))
    else:
        txt_path = Path(book["txt_path"]).expanduser()
        if not txt_path.exists():
            raise FileNotFoundError(f"参考书 txt 不存在: {txt_path}")
        logger.info("开始处理 [%s] @ %s", args.book, txt_path)
        chapters = load_and_split(txt_path, encoding=book.get("encoding", "gbk"))
        if rng:
            lo, hi = rng
            chapters = [c for c in chapters if lo <= c[0] <= hi]
            logger.info("章节范围 %d-%d，共 %d 章", lo, hi, len(chapters))
        asyncio.run(_run_build_async(args.book, chapters, llm, args.tag_version, args.workers))


if __name__ == "__main__":
    main()
