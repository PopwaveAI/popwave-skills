"""
project_config.py — 项目路径解析层

职责：
  所有 SKILL.md 里的硬编码相对路径统一经过此层解析。
"""

import os
import sys
import yaml


def resolve_shared(key: str) -> str:
    """解析共享资源路径"""
    _SHARED_PATHS = {
        "scene_fragments_db": "_shared/studio/scene_fragments.db",
        "plot_library_db": "_shared/studio/plot_library.db",
    }
    if key not in _SHARED_PATHS:
        raise KeyError(f"未知共享资源键: {key}")
    return _SHARED_PATHS[key]


def get_project_config(project_dir: str) -> dict:
    """载入项目元数据 + 路径配置"""
    config_path = os.path.join(project_dir, "project.yaml")
    if not os.path.isfile(config_path):
        raise FileNotFoundError(f"找不到 project.yaml: {config_path}")
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def resolve_path(project_dir: str, key: str) -> str:
    """解析项目内逻辑路径"""
    config = get_project_config(project_dir)
    paths = config.get("paths", config)
    raw = paths.get(key)
    if raw is None:
        raise KeyError(f"project.yaml 中找不到 '{key}' 路径定义")
    return os.path.normpath(os.path.join(project_dir, raw))


def check_paths(project_dir: str, keys: list[str]) -> None:
    """批量检查关键路径是否存在"""
    missing = []
    for key in keys:
        try:
            path = resolve_path(project_dir, key)
            if not os.path.exists(path):
                missing.append((key, path))
        except KeyError:
            missing.append((key, f"<project.yaml 中未定义 '{key}'>"))
    if missing:
        for key, path in missing:
            print(f"  {key:20s} → {path}")
        sys.exit(1)
