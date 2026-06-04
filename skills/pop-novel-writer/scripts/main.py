"""
ESM / main.py — CLI 入口（v1.0）

用法：
  # 写前加载：构建完整12项输入包
  python main.py before 389 --project /path/to/project --scene "威廉,丹彼尔" --output bundle.md

  # 写后更新 + 全局摘要
  python main.py after 389 --skeleton skeleton.md --project /path/to/project

  # 一致性校验
  python main.py validate 003 --skeleton skeleton.md --project ... 

  # 列出所有实体
  python main.py list --project ...

  # 全量引用检查
  python main.py check-refs --project ...
"""

import os
import sys
import argparse
import re
import yaml

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)

from loader import EntityLoader
from updater import EntityUpdater
from validator import EntityValidator

# ── 路径桥接注入 —— 动态 resolve 取代硬编码目录名 ─────
try:
    _GLUE_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "glue"))
    if _GLUE_DIR not in sys.path:
        sys.path.insert(0, os.path.dirname(_GLUE_DIR))  # pop-novel-writer/
    from glue.project_config import resolve_path as _resolve_glue_path
    _HAS_GLUE = True
except ImportError:
    _HAS_GLUE = False

# 路径别名表（key → project.yaml paths key，未配置时回退到硬编码）
_PATH_ALIASES = {
    "anchor_chapters":    ("anchor_chapters",    "01-写作资产/锚定章库"),
    "writing_assets":     ("writing_assets",     "01-写作资产"),
    "fact_skeletons":     ("fact_skeletons",     "01-事实骨架"),
    "global_summary":     ("global_summary",     "02-章纲/global-summary.md"),
    "experience_log":     ("experience_log",     "01-写作资产/experience-log.md"),
    "act_outline":        ("act_outline",        "02-幕纲"),
    "chapters":           ("chapters",           "03-正文"),
    "database":           ("database",           "04-数据库"),
    "l1_settings":        ("l1_dir",             "00-原始设定/L1-元设定层"),
    "l0_product":         ("prd",                "00-原始设定/L0-产品层"),
    "original_settings":  ("_no_glue_fallback",  "00-原始设定"),
}

def _resolve(project_root: str, key: str) -> str:
    """统一的路径解析：先尝试 resolve_path 再回退到 project_root + 默认路径"""
    if _HAS_GLUE and key in _PATH_ALIASES:
        glue_key, default_rel = _PATH_ALIASES[key]
        try:
            return _resolve_glue_path(project_root, glue_key)
        except (KeyError, FileNotFoundError):
            pass
        return os.path.join(project_root, default_rel)
    return project_root  # fallback

# ── v3.3 新增：读取辅助函数 ──────────────────────

def _read_reader_profile(project_root: str) -> str:
    """从 project.yaml 读取 reader_profile，返回格式化文本"""
    yaml_path = os.path.join(project_root, "project.yaml")
    if not os.path.isfile(yaml_path):
        return "（未配置 reader_profile）"
    try:
        with open(yaml_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        rp = data.get("project", {}).get("reader_profile", {})
        if not rp:
            return "（reader_profile 未配置）"
        lines = [
            f"平台: {rp.get('platform', '未知')}",
            f"读者: {rp.get('gender', '')} {rp.get('age_range', '')}",
            f"习惯: {rp.get('reading_habit', '')}",
            f"期望: {rp.get('expectation', '')}",
        ]
        return "\n".join(lines)
    except Exception as e:
        return f"（reader_profile 读取失败: {e}）"


def _load_anchor_chapter(project_root: str, skeleton_path: str) -> str:
    """从骨架或 Director 输出中提取锚定章引用，从锚定章库加载全文。
    
    支持三种格式:
      1. 骨架: 锚定章《filename》
      2. Director: ### 锚定章引用\n**主锚定**：`filename`
      3. 旧格式: 锚定章引用: filename
    """
    if not skeleton_path or not os.path.isfile(skeleton_path):
        return ""
    with open(skeleton_path, "r", encoding="utf-8") as f:
        text = f.read()

    anchor_file = None

    # 模式1: 骨架格式 `锚定章《filename》` 或 `锚定章 filename`
    m = re.search(r'锚定章[《\s]*([^《》\n]+?)(?:\.md)?[》\n]', text)
    if m:
        anchor_file = m.group(1).strip()

    # 模式2: Director 格式 `### 锚定章引用\n**主锚定**：filename`
    if not anchor_file:
        m = re.search(r'主锚定[：:]\s*[`"\']?([^`"\'\n]+?)(?:\.md)?[`"\']?', text)
        if m:
            anchor_file = m.group(1).strip()

    # 模式3: 旧格式 `锚定章引用: filename`
    if not anchor_file:
        m = re.search(r'锚定章引用[：:]\s*["\']?([^"\'\n]+?)(?:\.md)?["\']?', text)
        if m:
            anchor_file = m.group(1).strip()

    if not anchor_file:
        return ""

    anchor_dir = _resolve(project_root, "anchor_chapters")
    if not os.path.isdir(anchor_dir):
        return f"（锚定章库目录不存在: {anchor_dir}）"

    for fname in os.listdir(anchor_dir):
        # 模糊匹配：去除空格、书引号、扩展名后比对
        clean_fname = re.sub(r'[\s《》""\']', '', fname).replace('.md', '')
        clean_anchor = re.sub(r'[\s《》""\']', '', anchor_file).replace('.md', '')
        if clean_anchor in clean_fname or clean_fname in clean_anchor:
            path = os.path.join(anchor_dir, fname)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            # 只取前 2000 字锚定片段
            return content[:2000] if len(content) > 2000 else content

    return f"（锚定章文件未找到: {anchor_file}）"


def _post_render_auto_check(chapter_path: str, act_yaml_path: str = "") -> dict:
    """正文字数/否定句/钩子自动检查脚本"""
    result = {"passed": True, "checks": []}

    if not os.path.isfile(chapter_path):
        result["passed"] = False
        result["checks"].append({"name": "文件存在", "status": "❌", "detail": "文件不存在"})
        return result

    with open(chapter_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 字数检查
    word_count = len(content.replace("\n", "").replace(" ", ""))
    wc_check = {"name": "字数检查", "detail": f"{word_count} 字"}
    if word_count < 1800:
        wc_check["status"] = "❌"
        result["passed"] = False
    elif word_count > 2800:
        wc_check["status"] = "⚠️"
    else:
        wc_check["status"] = "✅"
    result["checks"].append(wc_check)

    # 否定句检查（5变体 — Phase 0 修复）
    neg_patterns = [
        # 变体1: "不是A而是B"
        r'不是[^，。\n]{1,30}而是',
        # 变体2: "不是A不是B是一种C"
        r'不是[^，。\n]+不是[^，。\n]+是[一|种|某种]',
        # 变体3: "说不清(楚)的(颜色|感觉|味道|声音)"
        r'说不清[楚的]{0,2}(?:的)?\s*(?:颜色|感觉|味道|声音|情绪|恐惧)',
        # 变体4: "是某种/一种说不清的"
        r'是(?:某种|一种)\s*说不清[的楚楚]{0,4}',
        # 变体5: "直觉告诉" / "没有问"
        r'直觉告诉',
        r'他没有问',
        r'她没有问',
    ]
    neg_count = 0
    for pat in neg_patterns:
        neg_count += len(re.findall(pat, content))
    neg_check = {"name": "否定句检查", "detail": f"{neg_count} 处"}
    neg_check["status"] = "❌" if neg_count > 0 else "✅"
    if neg_count > 0:
        result["passed"] = False
    result["checks"].append(neg_check)

    # 章末钩子检查
    last_3_lines = "\n".join(content.strip().split("\n")[-3:])
    hook_indicators = ["?", "！", "但", "然而", "不知道", "还没", "没结束", "不是"]
    has_hook = any(ind in last_3_lines for ind in hook_indicators)
    hook_check = {"name": "章末钩子", "detail": "有钩子" if has_hook else "无钩子"}
    hook_check["status"] = "❌" if not has_hook else "✅"
    if not has_hook:
        result["passed"] = False
    result["checks"].append(hook_check)

    return result

def _read_global_summary(project_root: str) -> str:
    """读取全局摘要（≤1500字），不存在则返回空占位"""
    gs_path = _resolve(project_root, "global_summary")
    if os.path.isfile(gs_path):
        with open(gs_path, "r", encoding="utf-8") as f:
            text = f.read()
        if len(text) > 2000:
            text = text[-1500:]
        return text
    return "（尚无全局摘要）"


def _read_original_settings(project_root: str) -> str:
    """读取 00-原始设定/ 下的所有关键设定文件，拼接注入 bundle"""
    l0_dir = _resolve(project_root, "l0_product")
    settings_dir = _resolve(project_root, "original_settings")

    key_files = [
        (os.path.join(l0_dir, "角色行为锚定.md"), 1200),
        (os.path.join(l0_dir, "金手指设计.md"), 1000),
        (os.path.join(l0_dir, "PRD.md"), 800),
        (os.path.join(l1_dir, "01-世界底座.md"), 1000),
        (os.path.join(l1_dir, "02-对抗模型.md"), 1000),
        (os.path.join(l1_dir, "03-成长体系.md"), 1000),
        (os.path.join(l1_dir, "05-主角契约.md"), 1500),
        (os.path.join(l1_dir, "06-力量体系.md"), 1000),
        (os.path.join(l1_dir, "数值体系.md"), 1500),
        (os.path.join(l1_dir, "诡异行为性格.md"), 2000),
    ]

    sections = []
    for full_path, max_len in key_files:
        if os.path.isfile(full_path):
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()
            if len(content) > max_len:
                content = content[:max_len] + "\n...(已截断)"
            sections.append(f"### {os.path.basename(full_path)}\n{content}")
        else:
            sections.append(f"### {os.path.basename(full_path)}\n（文件缺失）")

    return "\n\n".join(sections)


def _read_prev_chapter(project_root: str, chapter: int) -> str:
    """读取上一章正文的最后800字"""
    prev = chapter - 1
    if prev < 1:
        return "（第一章，无上一章）"
    chapters_dir = _resolve(project_root, "chapters")
    for ext in [".md", ".txt"]:
        path = os.path.join(chapters_dir, f"ch{prev:03d}{ext}")
        if os.path.isfile(path):
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
            return text[-800:]
    # 尝试 v2 的 _chapters 格式（兼容旧项目）
    path = os.path.join(project_root, "..", os.path.basename(project_root.rstrip('/\\').rstrip('v3').rstrip('V3')), "_chapters", f"ch_{prev:04d}.txt")
    if os.path.isfile(path):
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        return text[-800:]
    return "（上一章正文未找到）"


def _read_experience_log(project_root: str, max_entries: int = 5) -> str:
    """读取经验日志中最近N条 active 记录"""
    log_path = _resolve(project_root, "experience_log")
    if not os.path.isfile(log_path):
        return "（尚无经验日志）"
    with open(log_path, "r", encoding="utf-8") as f:
        text = f.read()
    # 按 --- 分隔提取条目，只保留 active 的
    entries = text.split("\n---\n")
    active_entries = []
    for e in entries:
        if "status: active" in e or "状态: active" in e:
            active_entries.append(e.strip())
    if not active_entries:
        return "（无 active 经验记录）"
    return "\n---\n".join(active_entries[-max_entries:])


def _detect_scene_types(skeleton_path: str) -> list:
    """从骨架头部提取场景类型列表"""
    if not skeleton_path or not os.path.isfile(skeleton_path):
        return ["通用"]
    with open(skeleton_path, "r", encoding="utf-8") as f:
        head = f.read(2000)
    # 匹配场景权重块
    types = re.findall(r'（([^）]+场景)）', head)
    if not types:
        types = re.findall(r'场景类型[：:](.+)', head)
    return types if types else ["通用"]


def _build_pass2_input(project_root: str, db_path: str, chapter: int, scene_keywords: list,
                        skeleton_path: str = "", output_path: str = "") -> str:
    """构建 Pass 2 的 14 项完整输入包（v3.3 升级版：+reader_profile+锚定章）"""
    lines = []
    lines.append(f"# 第 {chapter} 章 · 完整写作上下文（ESM v2.0 · SQLite={'是' if db_path else '否'}）\n")

    # 第0项 · 读者画像（v3.3 新增——全管线共享）
    rp = _read_reader_profile(project_root)
    lines.append("## 第0项 · 读者画像\n")
    lines.append(rp)
    lines.append("")

    # ① 事实骨架（文件引用或内容）
    if skeleton_path and os.path.isfile(skeleton_path):
        with open(skeleton_path, "r", encoding="utf-8") as f:
            skeleton_text = f.read()
        lines.append("## ① 事实骨架\n")
        lines.append(skeleton_text)
        lines.append("")

    # ② context-bundle（实体状态——自动从骨架{实体}提取并查DB）
    # DB schema: characters(角色) / weirds(诡异) / items(道具) / skills(技能) / state_changelog(状态变更)
    loader = EntityLoader(project_root, db_path=db_path if db_path else None)
    
    # 自动从骨架文本提取 {实体名} 引用，按需查DB
    refs_to_query = []
    if skeleton_path and os.path.isfile(skeleton_path):
        with open(skeleton_path, "r", encoding="utf-8") as f:
            skel = f.read()
        refs_to_query = EntityLoader.extract_entity_references(skel)
    if not refs_to_query:
        refs_to_query = scene_keywords  # fallback
    if not refs_to_query:
        refs_to_query = []  # 什么都不提供时也确保不报错
    
    bundle = loader.build_context_bundle(refs_to_query)
    lines.append("## ② context-bundle（实体状态)\n")
    lines.append(f"> 自动从骨架提取 {len(refs_to_query)} 个实体引用 | DB: characters/weirds/items/skills\n")
    if bundle:
        lines.append(bundle)
    else:
        lines.append("（骨架中无实体引用，未查询DB）\n")
    lines.append("")

    # ③ 全局摘要
    gs = _read_global_summary(project_root)
    lines.append("## ③ 全局摘要\n")
    lines.append(gs)
    lines.append("")

    # ④ 上一章结尾
    prev = _read_prev_chapter(project_root, chapter)
    lines.append("## ④ 上一章结尾原文（最后800字）\n")
    lines.append(prev)
    lines.append("")

    # ⑤ 经验日志
    exp = _read_experience_log(project_root)
    lines.append("## ⑤ 经验日志（最近active记录）\n")
    lines.append(exp)
    lines.append("")

    # ⑥ 场景模板约束（按类型）
    scene_types = _detect_scene_types(skeleton_path)
    template_dir = os.path.join(os.path.dirname(_SCRIPT_DIR), "template-pools")
    template_map = {
        "战斗": "战斗对抗.md", "对抗": "战斗对抗.md",
        "谈判": "对话博弈.md", "博弈": "对话博弈.md", "对话": "对话博弈.md",
        "悬疑": "悬疑揭示.md", "揭示": "悬疑揭示.md",
        "过渡": "过渡推进.md", "推进": "过渡推进.md",
        "压抑": "压抑蓄力.md", "蓄力": "压抑蓄力.md",
        "轻松": "轻松调剂.md", "调剂": "轻松调剂.md",
        "爽点": "爽点释放.md", "释放": "爽点释放.md",
    }
    matched_templates = set()
    for st in scene_types:
        for kw, tmpl in template_map.items():
            if kw in st:
                matched_templates.add(tmpl)
    lines.append("## ⑥ 场景模板约束\n")
    if matched_templates:
        for tmpl_name in sorted(matched_templates):
            tmpl_path = os.path.join(template_dir, tmpl_name)
            if os.path.isfile(tmpl_path):
                with open(tmpl_path, "r", encoding="utf-8") as f:
                    tmpl_content = f.read()
                lines.append(f"### {tmpl_name} 参考\n")
                lines.append(tmpl_content[:500])  # 只取前500字约束
                lines.append("")
    else:
        lines.append("（无对应场景模板，使用通用写作约束）\n")

    # ⑦ 知识注入 K1-K4
    kb_dir = os.path.join(os.path.dirname(_SCRIPT_DIR),
                          "knowledge-base")
    lines.append("## ⑦ 知识注入 K1-K4\n")
    for kb_file in ["K1-core-theory.md", "K2-platform-profile.md",
                     "K3-quantitative-baseline.md", "K4-genre-perception.md"]:
        kb_path = os.path.join(kb_dir, kb_file)
        if os.path.isfile(kb_path):
            with open(kb_path, "r", encoding="utf-8") as f:
                lines.append(f"### {kb_file}\n")
                lines.append(f.read())
                lines.append("")
    lines.append("")

    # ⑧ 锚定章片段（v3.3 新增——从 Director 引用加载）
    anchor = _load_anchor_chapter(project_root, skeleton_path)
    lines.append("## ⑧ 锚定章片段\n")
    lines.append(anchor if anchor else "（无锚定章引用，使用通用写作约束）\n")
    lines.append("")

    # ⑨ 导演决策日志（Phase 1 修复——从 Director 文件中直接读取）
    writing_assets = _resolve(project_root, "writing_assets")
    director_path = os.path.join(writing_assets, f"ch{chapter:03d}-director.md")
    lines.append("## ⑨ 导演决策日志\n")
    if os.path.isfile(director_path):
        with open(director_path, "r", encoding="utf-8") as f:
            lines.append(f.read())
    else:
        lines.append("（无 Director 文件）\n")
    lines.append("")

    # ⑩ 原始设定约束包（Phase 1 新增——将原始设定注入正文写作）
    original_settings = _read_original_settings(project_root)
    lines.append("## ⑩ 原始设定约束包\n")
    lines.append(original_settings)
    lines.append("")

    # ⑩+ 设定纲索引（结构化版本——管线可直接查询）
    setting_index_path = os.path.join(_resolve(project_root, "original_settings"), "setting-index.yaml")
    lines.append("## ⑩+ 设定纲索引（结构化）\n")
    if os.path.isfile(setting_index_path):
        with open(setting_index_path, "r", encoding="utf-8") as f:
            lines.append(f.read())
    else:
        lines.append("（setting-index.yaml 不存在）\n")
    lines.append("")

    # ⑪ 上一轮 QC 反馈（Phase 1 新增）
    writing_assets = _resolve(project_root, "writing_assets")
    qc_path = os.path.join(writing_assets, f"ch{chapter:03d}-qc-text.md")
    lines.append("## ⑪ 上一轮 QC 反馈\n")
    if os.path.isfile(qc_path):
        with open(qc_path, "r", encoding="utf-8") as f:
            lines.append(f.read()[:800])
    else:
        lines.append("（无QC反馈）\n")
    lines.append("")

    # ⑫ 上一章全文（Phase 1 新增——增加完整上下文而非仅结尾800字）
    if chapter > 1:
        prev_full = os.path.join(_resolve(project_root, "chapters"), f"ch{chapter-1:03d}.md")
        lines.append("## ⑫ 上一章全文\n")
        if os.path.isfile(prev_full):
            with open(prev_full, "r", encoding="utf-8") as f:
                lines.append(f.read())
        else:
            lines.append("（上一章文件缺失）\n")
    lines.append("")

    # ⑬ 下一章钩子预告（Phase 1 新增——从 act-01.yaml 读取）
    lines.append("## ⑬ 下一章钩子预告\n")
    act_yaml_path = os.path.join(_resolve(project_root, "act_outline"), "act-01.yaml")
    if os.path.isfile(act_yaml_path) and chapter < 30:
        with open(act_yaml_path, "r", encoding="utf-8") as f:
            act = yaml.safe_load(f)
        act_chapters = act.get("chapters", [])
        # act-01.yaml chapters 是 1-indexed 的列表
        next_ch = None
        for ac in act_chapters:
            if ac.get("number") == chapter + 1:
                next_ch = ac
                break
        if next_ch:
            lines.append(f"下一章标题: {next_ch.get('title', '未知')}")
            lines.append(f"情感目标: {next_ch.get('emotional_goal', '未知')}")
            hook = next_ch.get("end_hook", {}).get("content", "")
            if hook:
                lines.append(f"本章钩子指向: {hook}")
            fun_level = next_ch.get("fun_level", "")
            if fun_level:
                lines.append(f"爽点等级: {fun_level}")
        else:
            lines.append("（下一章信息未找到）\n")
    else:
        lines.append("（无法读取下一章信息）\n")
    lines.append("")

    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="ESM v2.0 — 实体状态管理器 + 上下文组装（SQLite 优先）")
    parser.add_argument("action", choices=["before", "after", "validate", "list", "check-refs", "autocheck"],
                        help="操作类型")
    parser.add_argument("chapter", nargs="?", type=int, default=None,
                        help="章节号")
    parser.add_argument("--project", "-p", required=True)
    parser.add_argument("--db-path", "-d", default="",
                        help="v3.db 路径（提供则走 SQLite 模式，否则降级到 YAML）")
    parser.add_argument("--scene", "-s", default="",
                        help="scene_keywords 逗号分隔（before 使用）")
    parser.add_argument("--skeleton", "-k", default="",
                        help="事实骨架文件路径（after/validate/before使用）")
    parser.add_argument("--output", "-o", default="",
                        help="输出文件路径（before的输入包输出）")
    parser.add_argument("--chapter-path", "-c", default="",
                        help="正文章节路径（autocheck 使用）")
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    project_root = os.path.abspath(args.project)
    if not os.path.isdir(project_root):
        print(f"[ESM] ❌ 项目目录不存在: {project_root}")
        sys.exit(1)
    db_path = os.path.abspath(args.db_path) if args.db_path else ""
    if db_path and not os.path.isfile(db_path):
        print(f"[ESM] ⚠️ db_path 文件不存在: {db_path}，降级到 YAML 模式")
        db_path = ""

    try:
        if args.action == "before":
            cmd_before(project_root, db_path, args)
        elif args.action == "after":
            cmd_after(project_root, db_path, args)
        elif args.action == "validate":
            cmd_validate(project_root, db_path, args)
        elif args.action == "list":
            cmd_list(project_root, db_path)
        elif args.action == "check-refs":
            cmd_check_refs(project_root, db_path)
        elif args.action == "autocheck":
            cmd_autocheck(project_root, args)
    except Exception as e:
        import traceback; traceback.print_exc()
        print(f"[ESM] ❌ 执行失败: {e}")
        sys.exit(1)


def cmd_before(project_root: str, db_path: str, args):
    """写前加载：构建12项完整输入包"""
    if not args.chapter:
        print("[ESM] ❌ before 操作需要章节号")
        sys.exit(1)
    keywords = [k.strip() for k in args.scene.split(",")] if args.scene else []
    skeleton = os.path.abspath(args.skeleton) if args.skeleton else ""
    input_pkg = _build_pass2_input(project_root, db_path, args.chapter, keywords, skeleton)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(input_pkg)
        print(f"[ESM] ✅ v2.0 输入包已写入: {args.output} (db={'是' if db_path else '否'})")
    else:
        print(input_pkg)


def cmd_after(project_root: str, db_path: str, args):
    """写后更新 + 全局摘要追加"""
    if not args.skeleton or not args.chapter:
        print("[ESM] ❌ after 需要 --skeleton 和章节号")
        sys.exit(1)
    skeleton_path = os.path.abspath(args.skeleton)
    if not os.path.isfile(skeleton_path):
        print(f"[ESM] ❌ 骨架文件不存在: {skeleton_path}")
        sys.exit(1)

    # Step 1: 更新实体状态
    updater = EntityUpdater(project_root, db_path=db_path if db_path else None)
    count = updater.apply_changes_from_skeleton(skeleton_path, args.chapter)
    print(f"[ESM] ✅ 实体状态更新完成: {count} 个 (db={'是' if db_path else '否'})")

    # Step 2: 更新全局摘要
    _append_to_global_summary(project_root, args.chapter, skeleton_path)
    print(f"[ESM] ✅ 全局摘要已更新（第 {args.chapter} 章）")


def _append_to_global_summary(project_root: str, chapter: int, skeleton_path: str):
    """从骨架提取核心进展→追加到全局摘要"""
    gs_dir = _resolve(project_root, "writing_assets")
    os.makedirs(gs_dir, exist_ok=True)
    gs_path = os.path.join(gs_dir, "global-summary.md")

    # 从骨架头部提取核心目的
    core_purpose = "（无标注）"
    with open(skeleton_path, "r", encoding="utf-8") as f:
        text = f.read()
    m = re.search(r'核心目的[：:]\s*([^\n]+)', text)
    if m:
        core_purpose = m.group(1).strip()

    # 从骨架尾部提取下一章钩子
    next_hook = "（无标注）"
    m = re.search(r'下一章钩子[：:]\s*([^\n]+)', text)
    if m:
        next_hook = m.group(1).strip()

    append_line = f"| ch{chapter:03d} | {core_purpose} | 下一章: {next_hook} |\n"

    if os.path.isfile(gs_path):
        with open(gs_path, "r", encoding="utf-8") as f:
            existing = f.read()
        # 追加到表中
        if "| ch" in existing:
            existing = existing.rstrip("\n") + "\n" + append_line
        else:
            existing += "\n## 追加记录\n| 章号 | 核心进展 |\n|:----:|:--------|\n" + append_line
        with open(gs_path, "w", encoding="utf-8") as f:
            f.write(existing)
    else:
        with open(gs_path, "w", encoding="utf-8") as f:
            f.write(f"# 全局摘要 · ch{chapter} 结束时\n\n## 追加记录\n| 章号 | 核心进展 |\n|:----:|:--------|\n{append_line}\n")


def cmd_validate(project_root: str, db_path: str, args):
    """一致性校验"""
    if not args.skeleton or not args.chapter:
        print("[ESM] ❌ validate 需要 --skeleton 和章节号")
        sys.exit(1)
    skeleton_path = os.path.abspath(args.skeleton)
    validator = EntityValidator(project_root, db_path=db_path if db_path else None)
    report = validator.check_consistency(args.chapter, skeleton_path)
    print(f"\n[ESM] 📋 校验报告 — 第 {args.chapter} 章")
    print(f"  检查项: {report['total_checks']} | 通过: {report['passed']} | 未通过: {report['failed']}")
    for item in report["items"]:
        print(f"  {item['status']} {item['check']}: {item['detail']}")


def cmd_list(project_root: str, db_path: str):
    loader = EntityLoader(project_root, db_path=db_path if db_path else None)
    all_entities = loader.list_all_entities()
    print(f"[ESM] 📋 实体清单 (db={'是' if db_path else '否'})")
    total = 0
    for entity_type, names in all_entities.items():
        print(f"\n  {entity_type}/ ({len(names)} 个)")
        for name in names:
            print(f"    - {name}")
        total += len(names)
    print(f"\n  总计: {total} 个实体")


def cmd_check_refs(project_root: str, db_path: str):
    validator = EntityValidator(project_root, db_path=db_path if db_path else None)
    report = validator.check_reference_coverage()
    print(f"[ESM] 📋 引用覆盖率检查")
    print(f"  实体总数: {report['total_entities']}")
    print(f"  状态: {report['status']}")
    print(f"  详情: {report['detail']}")


def cmd_autocheck(project_root: str, args):
    """写后自动检查：字数/否定句/钩子"""
    chapter_path = args.chapter_path if args.chapter_path else ""
    if not chapter_path and args.chapter:
        chapter_path = os.path.join(_resolve(project_root, "chapters"), f"ch{args.chapter:03d}.md")
    if not chapter_path or not os.path.isfile(chapter_path):
        print(f"[ESM] ❌ autocheck 需要 --chapter-path 或 --chapter（自动构造路径）")
        sys.exit(1)

    act_path = os.path.join(_resolve(project_root, "act_outline"), "act-01.yaml")
    if not os.path.isfile(act_path):
        act_path = ""

    result = _post_render_auto_check(chapter_path, act_path)
    print(f"\n[ESM] 📋 写后自动检查 — {os.path.basename(chapter_path)}")
    for c in result["checks"]:
        print(f"  {c['status']} {c['name']}: {c['detail']}")
    print(f"\n  总体: {'✅ 通过' if result['passed'] else '❌ 未通过，请修正后重试'}")


if __name__ == "__main__":
    main()
