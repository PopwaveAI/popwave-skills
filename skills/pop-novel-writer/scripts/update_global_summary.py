#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
update_global_summary.py — 全局摘要 & 角色状态锚 自动化更新

调用时机：每章 QC 质检通过后，手动或 CI 触发。
功能：
  1. 读上一章完成的正文
  2. 读旧的全局摘要（如果存在）
  3. LLM 产出增量更新的全局摘要（≤300 字）
  4. 从摘要中提取角色状态锚（每个活跃角色一行）
  5. 写入 02-章纲/ 目录
  6. 更新 _pipeline_state.json 进度

用法：
  python scripts/update_global_summary.py ^
      --project-dir "E:\project\your-novel" ^
      --chapter 10 ^
      --chapter-file "03-正文\ch010.md"

依赖：
  pip install openai python-dotenv
  .env 文件中配置 DEEPSEEK_API_KEY / DEEPSEEK_MODEL
"""

import argparse
import json
import logging
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# 日志
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("update_global_summary")

# ---------------------------------------------------------------------------
# Prompt 模板（不放在单独文件，便于脚本独立运转）
# ---------------------------------------------------------------------------

SUMMARY_UPDATE_SYSTEM = """你是一位资深网文编辑，负责维护小说的"全书进展摘要"。

你的任务：
- 基于已完成的章节正文，更新全书摘要
- 保留既有重要信息，同时融入新章节的核心推进
- 用简洁、连贯的语言描述全书进展
- 保留关键感官细节（视觉/触觉/听觉的异常）和未解释的诡异现象
- 每个章节的摘要 ≤ 300 字
- 只写最重要的 2-3 个进展，不逐段罗列

输出格式（严格 JSON）：
{
  "chapter_deliverables": ["一句话说明本章推进了什么事件", "一句话说明读者认知发生了什么变化"],
  "unresolved_threads": ["仍悬而未决的谜题（如无则写'无'）"],
  "global_summary": "≤200 字描述全书进展到哪了。保留氛围信息，不删感官细节。"
}"""

SUMMARY_UPDATE_PROMPT = """## 已完成的章节正文

{chapter_text}

## 旧的全局摘要（不存在则为空）

{old_summary}

---

基于以上内容，输出增量更新的全局摘要 JSON。"""

# ---------------------------------------------------------------------------

CHARACTER_STATE_SYSTEM = """你是一位小说角色分析师，负责从全局摘要中提取"角色状态锚"。

角色状态锚的规则：
- 每个角色一行，格式：[角色名]：[2-3个感知级状态词·用·分隔]
- 感知级 = 读者能"感觉到"的状态，不是剧情摘要
- 示例：
  ✅ 陈默：心跳加速·手指在抖·强行稳住呼吸
  ✅ 苏晚：界面层冷静·但手心在出汗
  ❌ 陈默：发现了纸人巷的秘密（这是剧情，不是状态）
  ❌ 苏晚：联系了玩家（这是行动，不是状态）
- 只保留当前章节活跃的角色（≤3 行）
- 如果角色不在当前章节出现，不写

输出格式（严格 JSON）：
{
  "character_anchors": [
    {"name": "陈默", "anchor": "心跳加速·手指在抖·强行稳住呼吸"},
    {"name": "苏晚", "anchor": "界面层冷静·但手心在出汗"}
  ]
}"""

CHARACTER_STATE_PROMPT = """## 当前全局摘要

{global_summary}

---

基于以上内容，提取当前章节活跃角色的状态锚 JSON。"""


# ---------------------------------------------------------------------------
# LLM 调用（轻量，直接复用 _llm.py 的设计模式）
# ---------------------------------------------------------------------------

def _load_env():
    """从 .env 加载 API 配置（从脚本所在目录向上找）"""
    script_dir = Path(__file__).resolve().parent
    # 向上找 .env：scripts/ → pop-novel-writer/ → skills/
    for p in [script_dir, script_dir.parent, script_dir.parent.parent,
              script_dir.parent.parent.parent]:
        env_file = p / ".env"
        if env_file.exists():
            load_dotenv(env_file)
            logger.info("Loaded .env from %s", env_file)
            return
    # 最后尝试项目根
    load_dotenv()
    logger.info("Loaded .env from default location")


def _llm_call(system: str, prompt: str, temperature: float = 0.3,
              max_tokens: int = 2000) -> dict | None:
    """
    通用 LLM JSON 调用。
    复用 _llm.py 的 client 设计，但直接内联避免跨文件耦合。
    """
    try:
        from openai import OpenAI
    except ImportError:
        logger.error("缺少 openai 库，请执行: pip install openai")
        return None

    api_key = os.environ.get("DEEPSEEK_API_KEY")
    base_url = os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
    model = os.environ.get("DEEPSEEK_MODEL", "deepseek-v4-flash")

    if not api_key:
        logger.error("DEEPSEEK_API_KEY 未配置。请检查 .env 文件。")
        return None

    client = OpenAI(api_key=api_key, base_url=base_url)

    for attempt in range(3):
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": prompt},
                ],
                temperature=temperature,
                max_tokens=max_tokens,
                response_format={"type": "json_object"},
            )
            text = resp.choices[0].message.content or ""
            result = json.loads(text)
            logger.info("LLM 调用成功: %s tokens", resp.usage.total_tokens if resp.usage else "?")
            return result
        except Exception as e:
            logger.warning("LLM 调用失败 (attempt %d): %s", attempt + 1, e)
            time.sleep(2 ** attempt)

    logger.error("LLM 调用最终失败")
    return None


# ---------------------------------------------------------------------------
# 文件读写
# ---------------------------------------------------------------------------

def read_file_safe(path: Path) -> str:
    """安全读取文件，不存在则返回空字符串"""
    if not path.exists():
        return ""
    try:
        return path.read_text(encoding="utf-8").strip()
    except Exception as e:
        logger.warning("读取文件失败 %s: %s", path, e)
        return ""


def write_file_safe(path: Path, content: str):
    """安全写入文件，自动创建父目录"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")
    logger.info("写入 %s (%d 字符)", path, len(content))


# ---------------------------------------------------------------------------
# 核心逻辑
# ---------------------------------------------------------------------------

def load_chapter_text(project_dir: Path, chapter_file: str) -> str:
    """加载本章正文"""
    path = project_dir / chapter_file if not Path(chapter_file).is_absolute() else Path(chapter_file)
    text = read_file_safe(path)
    if not text:
        logger.warning("章节文件为空或不存在: %s", path)
        return "（正文内容为空）"
    # 限制最大长度（避免超 token）
    if len(text) > 8000:
        text = text[:8000] + "\n\n...（截断）"
    return text


def load_old_summary(project_dir: Path) -> str:
    """加载旧的全局摘要"""
    path = project_dir / "02-章纲" / "global-summary.md"
    return read_file_safe(path)


def format_summary_to_markdown(data: dict, chapter: int) -> str:
    """将 LLM 返回的 JSON 格式化为可读的 markdown"""
    lines = []
    lines.append(f"## CH{chapter:02d} 全局摘要更新")
    lines.append(f"> 更新于 {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("")

    lines.append("### 本章关键交付")
    for item in data.get("chapter_deliverables", []):
        lines.append(f"- {item}")
    lines.append("")

    lines.append("### 未收束伏笔")
    for item in data.get("unresolved_threads", []):
        lines.append(f"- {item}")
    lines.append("")

    lines.append("### 当前全书状态")
    lines.append(data.get("global_summary", "（摘要生成失败）"))
    lines.append("")

    # 分隔线
    lines.append("---")
    lines.append("")

    return "\n".join(lines)


def update_pipeline_state(project_dir: Path, chapter: int):
    """更新 _pipeline_state.json"""
    state_file = project_dir / "_pipeline_state.json"
    if state_file.exists():
        try:
            state = json.loads(state_file.read_text(encoding="utf-8"))
        except Exception:
            state = {}
    else:
        state = {}

    state["last_summary_update"] = {
        "chapter": chapter,
        "timestamp": datetime.now().isoformat(),
    }
    state["status"] = "summary_done"
    write_file_safe(state_file, json.dumps(state, ensure_ascii=False, indent=2))
    logger.info("管线状态已更新: chapter=%d, status=summary_done", chapter)


# ---------------------------------------------------------------------------
# 主入口
# ---------------------------------------------------------------------------

def _discover_chapter_files(project_dir: Path, chapters_dir: str, max_chapter: int) -> list[tuple[int, str]]:
    """
    批量初始化模式下自动发现章节文件。
    支持命名格式: ch001.md, chapter_1.txt, 01-标题.md, ch006-片段A-名称.md 等。
    多个碎片文件按相同章节号合并。
    返回 [(编号, 合并后的正文内容), ...] 按编号正序。
    """
    scan_dir = project_dir / chapters_dir if not Path(chapters_dir).is_absolute() else Path(chapters_dir)
    if not scan_dir.exists():
        logger.error("章节目录不存在: %s", scan_dir)
        return []

    # 收集所有可能的章节文件
    import re
    from collections import defaultdict

    chapter_files = defaultdict(list)  # {chapter_num: [file1, file2, ...]}

    for f in scan_dir.iterdir():
        if not f.is_file():
            continue
        m = re.search(r'(?:ch|chapter[_\s]?|第)?0*(\d+)', f.stem)
        if m:
            num = int(m.group(1))
            if num <= max_chapter:
                chapter_files[num].append(f)

    # 排序并合并碎片
    result = []
    for num in sorted(chapter_files.keys()):
        files = sorted(chapter_files[num], key=lambda x: x.name)  # 按文件名排序保持碎片顺序
        # 合并所有碎片内容
        combined_text = ""
        for f in files:
            try:
                combined_text += f.read_text(encoding="utf-8").strip() + "\n\n"
            except Exception as e:
                logger.warning("读取文件失败 %s: %s", f, e)
        if combined_text.strip():
            # 截断过长文本
            if len(combined_text) > 6000:
                combined_text = combined_text[:6000] + "\n\n...（截断）"
            result.append((num, combined_text))

    logger.info("批量初始化: 发现 %d 个有效章节 (~%d)", len(result), max_chapter)
    for num, text in result:
        logger.info("  CH%02d (%d 字符)", num, len(text))
    return result


def _run_batch_init(project_dir: Path, chapters_dir: str, max_chapter: int):
    """
    批量初始化流程：顺序处理 1..N 章，累积生成全局摘要。
    """
    _load_env()
    chapters = _discover_chapter_files(project_dir, chapters_dir, max_chapter)
    if not chapters:
        logger.error("未找到任何章节文件，批量初始化终止。")
        sys.exit(1)

    # 确保旧摘要清空（批量初始化应从空白开始）
    summary_path = project_dir / "02-章纲" / "global-summary.md"
    anchor_path = project_dir / "02-章纲" / "character-state-anchor.md"
    if summary_path.exists():
        logger.warning("存在旧摘要文件，将在批处理前清空。")
        summary_path.write_text("", encoding="utf-8")

    old_summary = ""

    for chapter_num, chapter_content in chapters:
        logger.info("")
        logger.info("── 处理 CH%02d ──", chapter_num)

        # 正文已由 _discover_chapter_files 读取并合并碎片
        chapter_text = chapter_content[:6000]  # 已有截断

        # 调 LLM 生成增量摘要
        summary_result = _llm_call(
            system=SUMMARY_UPDATE_SYSTEM,
            prompt=SUMMARY_UPDATE_PROMPT.format(
                chapter_text=chapter_text,
                old_summary=old_summary or "（无旧摘要，首次生成）",
            ),
        )
        if not summary_result:
            logger.error("CH%02d 摘要生成失败，中断批量初始化", chapter_num)
            sys.exit(1)

        summary_md = format_summary_to_markdown(summary_result, chapter_num)
        old_summary = (old_summary + "\n" + summary_md) if old_summary else summary_md

        # 写入累积摘要
        write_file_safe(summary_path, old_summary)
        logger.info("CH%02d 已写入累积摘要", chapter_num)

    # 全部处理完成后，从最终全局摘要提取角色状态锚
    final_summary = read_file_safe(summary_path)
    last_global = "（批量初始化完成）"
    # 尝试取最后一个 CH 的 global_summary 字段
    # 直接再调一次 LLM 提取
    character_result = _llm_call(
        system=CHARACTER_STATE_SYSTEM,
        prompt=CHARACTER_STATE_PROMPT.format(
            global_summary="全书已完成" + str(max_chapter) + "章。当前状态：" +
                           final_summary[-500:] if len(final_summary) > 500 else final_summary,
        ),
        temperature=0.2,
    )
    if character_result:
        anchors = character_result.get("character_anchors", [])
        anchor_lines = [
            "# 角色状态锚（自动提取）\n",
            f"> 批量初始化基于 CH01-CH{max_chapter:02d} 正文自动生成\n",
        ]
        for a in anchors:
            anchor_lines.append(f"{a['name']}：{a['anchor']}")
        anchor_lines.append("")
        write_file_safe(anchor_path, "\n".join(anchor_lines))
        logger.info("角色状态锚已写入: %d 个角色", len(anchors))

    # 更新管线状态
    update_pipeline_state(project_dir, max_chapter)
    logger.info("批量初始化完成: CH01~CH%02d", max_chapter)


def main():
    parser = argparse.ArgumentParser(
        description="全局摘要 & 角色状态锚 自动化更新",
    )
    parser.add_argument(
        "--project-dir", "-p",
        required=True,
        help="项目根目录，例如 E:\\AI小说\\这诡异游戏也太真实了",
    )

    # 两种模式：单章更新 或 批量初始化
    mode_group = parser.add_argument_group("模式选择（二选一）")
    mode_group.add_argument(
        "--chapter", "-c",
        type=int,
        default=None,
        help="单章模式：当前完成的章节号（如 10）",
    )
    mode_group.add_argument(
        "--chapter-file", "-f",
        default=None,
        help="单章模式：章节正文文件路径",
    )
    mode_group.add_argument(
        "--batch-init", action="store_true",
        help="批量初始化模式：处理已有章节文件，累积生成全局摘要",
    )
    mode_group.add_argument(
        "--chapters-dir", default="03-正文",
        help="批量初始化：章节文件所在的目录（相对 project-dir），默认 03-正文",
    )
    mode_group.add_argument(
        "--max-chapter", type=int, default=10,
        help="批量初始化：最大章节号，默认 10",
    )

    parser.add_argument(
        "--skip-llm", action="store_true",
        help="跳过 LLM 调用，只创建空模板文件（调试用）",
    )
    args = parser.parse_args()

    project_dir = Path(args.project_dir).resolve()

    # ── 模式分发 ─────────────────────────────────
    if args.batch_init:
        _run_batch_init(project_dir, args.chapters_dir, args.max_chapter)
        return

    # 单章模式（原有逻辑）
    if not args.chapter or not args.chapter_file:
        parser.error("单章模式需要 --chapter 和 --chapter-file 参数。批量初始化请用 --batch-init。")

    chapter = args.chapter
    chapter_file = args.chapter_file

    logger.info("=" * 50)
    logger.info("全局摘要更新开始")
    logger.info("项目目录: %s", project_dir)
    logger.info("章节: CH%02d", chapter)
    logger.info("章节文件: %s", chapter_file)
    logger.info("=" * 50)

    # ── Step 1: 加载正文 & 旧摘要 ─────────────────
    chapter_text = load_chapter_text(project_dir, chapter_file)
    old_summary = load_old_summary(project_dir)

    logger.info("章节正文长度: %d 字符", len(chapter_text))
    logger.info("旧摘要长度: %d 字符", len(old_summary))

    # ── Step 2: LLM 生成新摘要 ──────────────────
    if not args.skip_llm:
        _load_env()
        summary_result = _llm_call(
            system=SUMMARY_UPDATE_SYSTEM,
            prompt=SUMMARY_UPDATE_PROMPT.format(
                chapter_text=chapter_text,
                old_summary=old_summary or "（无旧摘要，首次生成）",
            ),
        )
        if summary_result:
            summary_md = format_summary_to_markdown(summary_result, chapter)

            # 将新摘要追加到旧摘要下方（保留历史）
            if old_summary:
                # 找到全局摘要的位置：追加在文件末尾
                combined = old_summary + "\n" + summary_md
            else:
                combined = summary_md

            # 写入 02-章纲/global-summary.md
            summary_path = project_dir / "02-章纲" / "global-summary.md"
            write_file_safe(summary_path, combined)
            logger.info("全局摘要已更新")

            # ── Step 3: 提取角色状态锚 ──────────
            global_summary_text = summary_result.get("global_summary", "")
            character_result = _llm_call(
                system=CHARACTER_STATE_SYSTEM,
                prompt=CHARACTER_STATE_PROMPT.format(
                    global_summary=global_summary_text,
                ),
                temperature=0.2,  # 状态提取用更低温度，更稳定
            )
            if character_result:
                anchors = character_result.get("character_anchors", [])
                anchor_lines = ["# 角色状态锚（自动提取）\n",
                                f"> 基于 CH{chapter:02d} 正文自动生成\n"]
                for a in anchors:
                    anchor_lines.append(f"{a['name']}：{a['anchor']}")
                anchor_lines.append("")  # 末尾空行

                anchor_path = project_dir / "02-章纲" / "character-state-anchor.md"
                write_file_safe(anchor_path, "\n".join(anchor_lines))
                logger.info("角色状态锚已更新: %d 个角色", len(anchors))

            # ── Step 4: 更新管线状态 ────────────
            update_pipeline_state(project_dir, chapter)

        else:
            logger.error("全局摘要生成失败，请检查 LLM 配置和网络连接。")
            sys.exit(1)
    else:
        # 调试模式：写模板
        logger.info("跳过 LLM 调用（--skip-llm），创建空模板...")
        placeholder = (
            f"## CH{chapter:02d} 全局摘要更新\n"
            f"> 更新于 {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
            f"### 本章关键交付\n"
            f"- [待 LLM 生成：本章推进了什么事件]\n"
            f"- [待 LLM 生成：读者认知发生了什么变化]\n\n"
            f"### 当前全书状态\n"
            f"[待 LLM 生成]\n"
        )
        summary_path = project_dir / "02-章纲" / "global-summary.md"
        if old_summary:
            combined = old_summary + "\n" + placeholder
        else:
            combined = "# 全局摘要累积记录\n\n" + placeholder
        write_file_safe(summary_path, combined)

        anchor_placeholder = (
            "# 角色状态锚（自动提取）\n\n"
            f"> 基于 CH{chapter:02d} 正文自动生成\n\n"
            "陈默：[待 LLM 提取]\n"
            "苏晚：[待 LLM 提取]\n"
        )
        anchor_path = project_dir / "02-章纲" / "character-state-anchor.md"
        write_file_safe(anchor_path, anchor_placeholder)

        update_pipeline_state(project_dir, chapter)

    logger.info("=" * 50)
    logger.info("完成！")
    logger.info("全局摘要: %s", project_dir / "02-章纲" / "global-summary.md")
    logger.info("角色状态锚: %s", project_dir / "02-章纲" / "character-state-anchor.md")
    logger.info("=" * 50)


if __name__ == "__main__":
    main()
