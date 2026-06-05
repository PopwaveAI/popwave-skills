"""
project_config.py — 项目路径解析层

职责：
  所有 SKILL.md 里的硬编码相对路径（"00-原始设定/L0-产品层/PRD.md"）
  统一经过此层解析。不同项目有不同的目录结构，但逻辑键名一致。

用法：
  from glue.project_config import resolve_path, resolve_shared, get_project_config

  # 解析项目内路径
  prd_path = resolve_path("/E/AI小说/灰骑士之主正在杀穿多元宇宙", "prd")
  # → "/E/AI小说/灰骑士之主正在杀穿多元宇宙/v10/00-原始设定/L0-产品层/PRD.md"

  # 解析共享资源路径
  db_path = resolve_shared("scene_fragments_db")
  # → "/E/AI小说/_shared/studio/scene_fragments.db"

  # 批量检查（启动模块前调用）
  check_paths(project_dir, ["prd", "constitution", "l1_dir"])
  # → 缺少即报错退出

在 project.yaml 中扩展 paths 段：
  paths:
    prd: "00-总控/PRD.md"               # 示例（旧项目）
    # 或
    prd: "v10/00-原始设定/L0-产品层/PRD.md"  # 灰骑士
"""

import os
import sys
import yaml

# ─── 胶水自身配置路径 ─────────────────────────────────

_GLUE_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.dirname(_GLUE_DIR)  # novel-agent-pro/


# ─── 共享资源配置 ──────────────────────────────────

_SHARED_PATHS = {
    # key: 相对路径（相对于 novel-agent-pro/ 上一级，即 E:\AI小说\）
    "scene_fragments_db": "_shared/studio/scene_fragments.db",
    "study_materials": "novel-agent-pro/学习资料/",
    "plot_library_db": "_shared/studio/plot_library.db",
}

# 共享资源的基准目录 = novel-agent-pro/ 的上一级
# 例如：E:\AI小说\novel-agent-pro\ → 基准 = E:\AI小说\
_SHARED_BASE = os.path.normpath(os.path.join(_PROJECT_ROOT, ".."))


def resolve_shared(key: str) -> str:
    """解析共享资源路径（不依赖具体项目）"""
    if key not in _SHARED_PATHS:
        raise KeyError(f"[glue] 未知共享资源键: {key}，可用: {list(_SHARED_PATHS.keys())}")
    return os.path.normpath(os.path.join(_SHARED_BASE, _SHARED_PATHS[key]))


# ─── 项目内路径解析 ──────────────────────────────────


def get_project_config(project_dir: str) -> dict:
    """载入项目元数据 + 路径配置"""
    config_path = os.path.join(project_dir, "project.yaml")
    if not os.path.isfile(config_path):
        raise FileNotFoundError(f"[glue] 找不到 project.yaml: {config_path}")
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config


def resolve_path(project_dir: str, key: str) -> str:
    """
    解析项目内逻辑路径。

    参数:
      project_dir: project.yaml 所在目录的绝对路径
      key:         逻辑键名（见下方 PATH_KEYS）

    返回:
      解析后的绝对路径（文件或目录），不检查存在性
    """
    config = get_project_config(project_dir)

    # 兼容两种格式：
    # 新版：config["paths"][key]
    # 旧版：config[key]（直接写在 project 下）
    paths = config.get("paths", config)
    raw = paths.get(key)
    if raw is None:
        raise KeyError(
            f"[glue] project.yaml 中找不到 '{key}' 路径定义。\n"
            f"  可用路径键: {list(paths.keys())}\n"
            f"  项目: {config.get('project', {}).get('name', project_dir)}"
        )

    return os.path.normpath(os.path.join(project_dir, raw))


# ─── 路径键名说明文档 ─────────────────────────────────

PATH_KEYS = """
project.yaml paths 段支持的逻辑键名：

  prd               PRD.md
  constitution      constitution.yaml
  l1_dir            L1-元设定层/  目录
  l2_dir            L2-展开层/    目录
  l3_dir            L3-角色层/    目录
  reference_analysis  _参考书分析/  目录
  act_outline       幕纲/         目录（如 02-幕纲/）
  chapter_outline   章纲/         目录（如 02-章纲/）
  chapters          正文/         目录（如 03-正文/）
  database          数据库/       目录（如 04-数据库/）
  global_summary    global-summary.md
  character_state   character-state-anchor.md
  l1_settings       l1-settings.yaml
"""


# ─── 批量检查 ──────────────────────────────────


def check_paths(project_dir: str, keys: list[str]) -> None:
    """
    批量检查关键路径是否存在。
    任何一个缺失 → 打印错误并 sys.exit(1)
    """
    missing = []
    for key in keys:
        try:
            path = resolve_path(project_dir, key)
            if not os.path.exists(path):
                missing.append((key, path))
        except KeyError as e:
            print(f"[glue] {e}")
            missing.append((key, f"<project.yaml 中未定义 '{key}'>"))

    if missing:
        print(f"\n[glue] ❌ 以下路径缺失（共 {len(missing)} 项）：")
        for key, path in missing:
            print(f"  {key:20s} → {path}")
        print(f"\n[glue] 项目: {project_dir}")
        sys.exit(1)
    else:
        print(f"[glue] ✅ 全部 {len(keys)} 项路径就绪")


# ─── CLI 入口：快速检查单个项目 ──────────────────


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="检查项目路径配置")
    parser.add_argument("project_dir", help="项目根目录（包含 project.yaml）")
    parser.add_argument("--keys", nargs="+", default=["prd", "constitution"],
                        help="要检查的路径键（默认: prd constitution）")
    parser.add_argument("--show", action="store_true", help="显示所有已配置的路径")
    args = parser.parse_args()

    if args.show:
        config = get_project_config(args.project_dir)
        paths = config.get("paths", {})
        print(f"\n项目: {config.get('project', {}).get('name', '?')}")
        print(f"已配置 {len(paths)} 条路径：")
        for k, v in paths.items():
            abspath = os.path.normpath(os.path.join(args.project_dir, v))
            exists = "✅" if os.path.exists(abspath) else "❌"
            print(f"  {k:20s} → {v}  {exists}")

    if args.keys:
        check_paths(args.project_dir, args.keys)
