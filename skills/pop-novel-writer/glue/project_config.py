"""
project_config.py — 项目路径解析"""
project_config.py — 项目路径解析层（pop-novel-writer 独立版）

职责：
  所有 SKILL.md 里的硬编码相对路径
  统一经过此层解析。不同项目有不同的目录结构，但逻辑键名一致。

用法：
  from glue.project_config"""
project_config.py — 项目路径解析层（pop-novel-writer 独立版）

职责：
  所有 SKILL.md 里的硬编码相对路径
  统一经过此层解析。不同项目有不同的目录结构，但逻辑键名一致。

用法：
  from glue.project_config import resolve_path, resolve_shared, get_project_config

  # 解析项目内路径
  prd_path = resolve_path("/path/to/project", "prd")
  # → "/path/to/project/00-原始设定"""
project_config.py — 项目路径解析层（pop-novel-writer 独立版）

职责：
  所有 SKILL.md 里的硬编码相对路径
  统一经过此层解析。不同项目有不同的目录结构，但逻辑键名一致。

用法：
  from glue.project_config import resolve_path, resolve_shared, get_project_config

  # 解析项目内路径
  prd_path = resolve_path("/path/to/project", "prd")
  # → "/path/to/project/00-原始设定/L0-产品层/PRD.md"

  # 批量检查（启动模块前调用）
  check_paths(project_dir, ["prd", "constitution", "l1_dir"])
  # → 缺少即报错退出

在 project.yaml 中扩展 paths 段：
  paths:
    prd:"""
project_config.py — 项目路径解析层（pop-novel-writer 独立版）

职责：
  所有 SKILL.md 里的硬编码相对路径
  统一经过此层解析。不同项目有不同的目录结构，但逻辑键名一致。

用法：
  from glue.project_config import resolve_path, resolve_shared, get_project_config

  # 解析项目内路径
  prd_path = resolve_path("/path/to/project", "prd")
  # → "/path/to/project/00-原始设定/L0-产品层/PRD.md"

  # 批量检查（启动模块前调用）
  check_paths(project_dir, ["prd", "constitution", "l1_dir"])
  # → 缺少即报错退出

在 project.yaml 中扩展 paths 段：
  paths:
    prd: "00-原始设定/L0-产品层/PRD.md"
"""

import os
import sys
import yaml


# ─── 项目"""
project_config.py — 项目路径解析层（pop-novel-writer 独立版）

职责：
  所有 SKILL.md 里的硬编码相对路径
  统一经过此层解析。不同项目有不同的目录结构，但逻辑键名一致。

用法：
  from glue.project_config import resolve_path, resolve_shared, get_project_config

  # 解析项目内路径
  prd_path = resolve_path("/path/to/project", "prd")
  # → "/path/to/project/00-原始设定/L0-产品层/PRD.md"

  # 批量检查（启动模块前调用）
  check_paths(project_dir, ["prd", "constitution", "l1_dir"])
  # → 缺少即报错退出

在 project.yaml 中扩展 paths 段：
  paths:
    prd: "00-原始设定/L0-产品层/PRD.md"
"""

import os
import sys
import yaml


# ─── 项目内路径解析 ──────────────────────────────────


def get_project_config(project_dir: str) -> dict:
    """载入项目元数据 + 路径配置"""
    config_path = os.path.join(project_dir, "project.yaml")
    if not os.path.isfile(config_path):
        raise FileNotFoundError(f"[glue] 找不到 project.yaml: {config_path}")
    with"""
project_config.py — 项目路径解析层（pop-novel-writer 独立版）

职责：
  所有 SKILL.md 里的硬编码相对路径
  统一经过此层解析。不同项目有不同的目录结构，但逻辑键名一致。

用法：
  from glue.project_config import resolve_path, resolve_shared, get_project_config

  # 解析项目内路径
  prd_path = resolve_path("/path/to/project", "prd")
  # → "/path/to/project/00-原始设定/L0-产品层/PRD.md"

  # 批量检查（启动模块前调用）
  check_paths(project_dir, ["prd", "constitution", "l1_dir"])
  # → 缺少即报错退出

在 project.yaml 中扩展 paths 段：
  paths:
    prd: "00-原始设定/L0-产品层/PRD.md"
"""

import os
import sys
import yaml


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
    解析"""
project_config.py — 项目路径解析层（pop-novel-writer 独立版）

职责：
  所有 SKILL.md 里的硬编码相对路径
  统一经过此层解析。不同项目有不同的目录结构，但逻辑键名一致。

用法：
  from glue.project_config import resolve_path, resolve_shared, get_project_config

  # 解析项目内路径
  prd_path = resolve_path("/path/to/project", "prd")
  # → "/path/to/project/00-原始设定/L0-产品层/PRD.md"

  # 批量检查（启动模块前调用）
  check_paths(project_dir, ["prd", "constitution", "l1_dir"])
  # → 缺少即报错退出

在 project.yaml 中扩展 paths 段：
  paths:
    prd: "00-原始设定/L0-产品层/PRD.md"
"""

import os
import sys
import yaml


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
    config = get"""
project_config.py — 项目路径解析层（pop-novel-writer 独立版）

职责：
  所有 SKILL.md 里的硬编码相对路径
  统一经过此层解析。不同项目有不同的目录结构，但逻辑键名一致。

用法：
  from glue.project_config import resolve_path, resolve_shared, get_project_config

  # 解析项目内路径
  prd_path = resolve_path("/path/to/project", "prd")
  # → "/path/to/project/00-原始设定/L0-产品层/PRD.md"

  # 批量检查（启动模块前调用）
  check_paths(project_dir, ["prd", "constitution", "l1_dir"])
  # → 缺少即报错退出

在 project.yaml 中扩展 paths 段：
  paths:
    prd: "00-原始设定/L0-产品层/PRD.md"
"""

import os
import sys
import yaml


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
    # 旧版：config[key]（直接写在 project 下"""
project_config.py — 项目路径解析层（pop-novel-writer 独立版）

职责：
  所有 SKILL.md 里的硬编码相对路径
  统一经过此层解析。不同项目有不同的目录结构，但逻辑键名一致。

用法：
  from glue.project_config import resolve_path, resolve_shared, get_project_config

  # 解析项目内路径
  prd_path = resolve_path("/path/to/project", "prd")
  # → "/path/to/project/00-原始设定/L0-产品层/PRD.md"

  # 批量检查（启动模块前调用）
  check_paths(project_dir, ["prd", "constitution", "l1_dir"])
  # → 缺少即报错退出

在 project.yaml 中扩展 paths 段：
  paths:
    prd: "00-原始设定/L0-产品层/PRD.md"
"""

import os
import sys
import yaml


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
"""
project_config.py — 项目路径解析层（pop-novel-writer 独立版）

职责：
  所有 SKILL.md 里的硬编码相对路径
  统一经过此层解析。不同项目有不同的目录结构，但逻辑键名一致。

用法：
  from glue.project_config import resolve_path, resolve_shared, get_project_config

  # 解析项目内路径
  prd_path = resolve_path("/path/to/project", "prd")
  # → "/path/to/project/00-原始设定/L0-产品层/PRD.md"

  # 批量检查（启动模块前调用）
  check_paths(project_dir, ["prd", "constitution", "l1_dir"])
  # → 缺少即报错退出

在 project.yaml 中扩展 paths 段：
  paths:
    prd: "00-原始设定/L0-产品层/PRD.md"
"""

import os
import sys
import yaml


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

    return os.path.normpath(os.path"""
project_config.py — 项目路径解析层（pop-novel-writer 独立版）

职责：
  所有 SKILL.md 里的硬编码相对路径
  统一经过此层解析。不同项目有不同的目录结构，但逻辑键名一致。

用法：
  from glue.project_config import resolve_path, resolve_shared, get_project_config

  # 解析项目内路径
  prd_path = resolve_path("/path/to/project", "prd")
  # → "/path/to/project/00-原始设定/L0-产品层/PRD.md"

  # 批量检查（启动模块前调用）
  check_paths(project_dir, ["prd", "constitution", "l1_dir"])
  # → 缺少即报错退出

在 project.yaml 中扩展 paths 段：
  paths:
    prd: "00-原始设定/L0-产品层/PRD.md"
"""

import os
import sys
import yaml


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


# ─── 共享资源配置（基础降级版，不"""
project_config.py — 项目路径解析层（pop-novel-writer 独立版）

职责：
  所有 SKILL.md 里的硬编码相对路径
  统一经过此层解析。不同项目有不同的目录结构，但逻辑键名一致。

用法：
  from glue.project_config import resolve_path, resolve_shared, get_project_config

  # 解析项目内路径
  prd_path = resolve_path("/path/to/project", "prd")
  # → "/path/to/project/00-原始设定/L0-产品层/PRD.md"

  # 批量检查（启动模块前调用）
  check_paths(project_dir, ["prd", "constitution", "l1_dir"])
  # → 缺少即报错退出

在 project.yaml 中扩展 paths 段：
  paths:
    prd: "00-原始设定/L0-产品层/PRD.md"
"""

import os
import sys
import yaml


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


# ─── 共享资源配置（基础降级版，不依赖外部路径）───────────────

_SHARED_PATHS = {
    "scene_fragments_db": "_shared/studio/scene_fragments.db",
    "study_materials": "_shared/study_materials/",
    "plot_library_db": "_shared/"""
project_config.py — 项目路径解析层（pop-novel-writer 独立版）

职责：
  所有 SKILL.md 里的硬编码相对路径
  统一经过此层解析。不同项目有不同的目录结构，但逻辑键名一致。

用法：
  from glue.project_config import resolve_path, resolve_shared, get_project_config

  # 解析项目内路径
  prd_path = resolve_path("/path/to/project", "prd")
  # → "/path/to/project/00-原始设定/L0-产品层/PRD.md"

  # 批量检查（启动模块前调用）
  check_paths(project_dir, ["prd", "constitution", "l1_dir"])
  # → 缺少即报错退出

在 project.yaml 中扩展 paths 段：
  paths:
    prd: "00-原始设定/L0-产品层/PRD.md"
"""

import os
import sys
import yaml


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


# ─── 共享资源配置（基础降级版，不依赖外部路径）───────────────

_SHARED_PATHS = {
    "scene_fragments_db": "_shared/studio/scene_fragments.db",
    "study_materials": "_shared/study_materials/",
    "plot_library_db": "_shared/studio/plot_library.db",
}

# 共享资源的基准目录 = 本脚本所在目录"""
project_config.py — 项目路径解析层（pop-novel-writer 独立版）

职责：
  所有 SKILL.md 里的硬编码相对路径
  统一经过此层解析。不同项目有不同的目录结构，但逻辑键名一致。

用法：
  from glue.project_config import resolve_path, resolve_shared, get_project_config

  # 解析项目内路径
  prd_path = resolve_path("/path/to/project", "prd")
  # → "/path/to/project/00-原始设定/L0-产品层/PRD.md"

  # 批量检查（启动模块前调用）
  check_paths(project_dir, ["prd", "constitution", "l1_dir"])
  # → 缺少即报错退出

在 project.yaml 中扩展 paths 段：
  paths:
    prd: "00-原始设定/L0-产品层/PRD.md"
"""

import os
import sys
import yaml


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


# ─── 共享资源配置（基础降级版，不依赖外部路径）───────────────

_SHARED_PATHS = {
    "scene_fragments_db": "_shared/studio/scene_fragments.db",
    "study_materials": "_shared/study_materials/",
    "plot_library_db": "_shared/studio/plot_library.db",
}

# 共享资源的基准目录 = 本脚本所在目录的上级的上级（popwave-skills/ 或用户项目父目录）
_GLUE_DIR = os.path.dirname(os.path.abspath(__file__))
_SKILL_ROOT ="""
project_config.py — 项目路径解析层（pop-novel-writer 独立版）

职责：
  所有 SKILL.md 里的硬编码相对路径
  统一经过此层解析。不同项目有不同的目录结构，但逻辑键名一致。

用法：
  from glue.project_config import resolve_path, resolve_shared, get_project_config

  # 解析项目内路径
  prd_path = resolve_path("/path/to/project", "prd")
  # → "/path/to/project/00-原始设定/L0-产品层/PRD.md"

  # 批量检查（启动模块前调用）
  check_paths(project_dir, ["prd", "constitution", "l1_dir"])
  # → 缺少即报错退出

在 project.yaml 中扩展 paths 段：
  paths:
    prd: "00-原始设定/L0-产品层/PRD.md"
"""

import os
import sys
import yaml


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


# ─── 共享资源配置（基础降级版，不依赖外部路径）───────────────

_SHARED_PATHS = {
    "scene_fragments_db": "_shared/studio/scene_fragments.db",
    "study_materials": "_shared/study_materials/",
    "plot_library_db": "_shared/studio/plot_library.db",
}

# 共享资源的基准目录 = 本脚本所在目录的上级的上级（popwave-skills/ 或用户项目父目录）
_GLUE_DIR = os.path.dirname(os.path.abspath(__file__))
_SKILL_ROOT = os.path.dirname(_GLUE_DIR)            # pop-novel-writer/
_SHARED_BASE = os.path.normpath(os.path.join(_SKILL_ROOT, "..", """"
project_config.py — 项目路径解析层（pop-novel-writer 独立版）

职责：
  所有 SKILL.md 里的硬编码相对路径
  统一经过此层解析。不同项目有不同的目录结构，但逻辑键名一致。

用法：
  from glue.project_config import resolve_path, resolve_shared, get_project_config

  # 解析项目内路径
  prd_path = resolve_path("/path/to/project", "prd")
  # → "/path/to/project/00-原始设定/L0-产品层/PRD.md"

  # 批量检查（启动模块前调用）
  check_paths(project_dir, ["prd", "constitution", "l1_dir"])
  # → 缺少即报错退出

在 project.yaml 中扩展 paths 段：
  paths:
    prd: "00-原始设定/L0-产品层/PRD.md"
"""

import os
import sys
import yaml


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


# ─── 共享资源配置（基础降级版，不依赖外部路径）───────────────

_SHARED_PATHS = {
    "scene_fragments_db": "_shared/studio/scene_fragments.db",
    "study_materials": "_shared/study_materials/",
    "plot_library_db": "_shared/studio/plot_library.db",
}

# 共享资源的基准目录 = 本脚本所在目录的上级的上级（popwave-skills/ 或用户项目父目录）
_GLUE_DIR = os.path.dirname(os.path.abspath(__file__))
_SKILL_ROOT = os.path.dirname(_GLUE_DIR)            # pop-novel-writer/
_SHARED_BASE = os.path.normpath(os.path.join(_SKILL_ROOT, "..", ".."))  # popwave-skills/


def resolve_shared(key: str) -> str:
    """解析共享资源路径（不依赖具体项目）"""
    if key not in _"""
project_config.py — 项目路径解析层（pop-novel-writer 独立版）

职责：
  所有 SKILL.md 里的硬编码相对路径
  统一经过此层解析。不同项目有不同的目录结构，但逻辑键名一致。

用法：
  from glue.project_config import resolve_path, resolve_shared, get_project_config

  # 解析项目内路径
  prd_path = resolve_path("/path/to/project", "prd")
  # → "/path/to/project/00-原始设定/L0-产品层/PRD.md"

  # 批量检查（启动模块前调用）
  check_paths(project_dir, ["prd", "constitution", "l1_dir"])
  # → 缺少即报错退出

在 project.yaml 中扩展 paths 段：
  paths:
    prd: "00-原始设定/L0-产品层/PRD.md"
"""

import os
import sys
import yaml


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


# ─── 共享资源配置（基础降级版，不依赖外部路径）───────────────

_SHARED_PATHS = {
    "scene_fragments_db": "_shared/studio/scene_fragments.db",
    "study_materials": "_shared/study_materials/",
    "plot_library_db": "_shared/studio/plot_library.db",
}

# 共享资源的基准目录 = 本脚本所在目录的上级的上级（popwave-skills/ 或用户项目父目录）
_GLUE_DIR = os.path.dirname(os.path.abspath(__file__))
_SKILL_ROOT = os.path.dirname(_GLUE_DIR)            # pop-novel-writer/
_SHARED_BASE = os.path.normpath(os.path.join(_SKILL_ROOT, "..", ".."))  # popwave-skills/


def resolve_shared(key: str) -> str:
    """解析共享资源路径（不依赖具体项目）"""
    if key not in _SHARED_PATHS:
        raise KeyError(f"[glue] 未知共享资源键: {key}，可用: {list(_SHARED_PATHS.keys())}")
"""
project_config.py — 项目路径解析层（pop-novel-writer 独立版）

职责：
  所有 SKILL.md 里的硬编码相对路径
  统一经过此层解析。不同项目有不同的目录结构，但逻辑键名一致。

用法：
  from glue.project_config import resolve_path, resolve_shared, get_project_config

  # 解析项目内路径
  prd_path = resolve_path("/path/to/project", "prd")
  # → "/path/to/project/00-原始设定/L0-产品层/PRD.md"

  # 批量检查（启动模块前调用）
  check_paths(project_dir, ["prd", "constitution", "l1_dir"])
  # → 缺少即报错退出

在 project.yaml 中扩展 paths 段：
  paths:
    prd: "00-原始设定/L0-产品层/PRD.md"
"""

import os
import sys
import yaml


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


# ─── 共享资源配置（基础降级版，不依赖外部路径）───────────────

_SHARED_PATHS = {
    "scene_fragments_db": "_shared/studio/scene_fragments.db",
    "study_materials": "_shared/study_materials/",
    "plot_library_db": "_shared/studio/plot_library.db",
}

# 共享资源的基准目录 = 本脚本所在目录的上级的上级（popwave-skills/ 或用户项目父目录）
_GLUE_DIR = os.path.dirname(os.path.abspath(__file__))
_SKILL_ROOT = os.path.dirname(_GLUE_DIR)            # pop-novel-writer/
_SHARED_BASE = os.path.normpath(os.path.join(_SKILL_ROOT, "..", ".."))  # popwave-skills/


def resolve_shared(key: str) -> str:
    """解析共享资源路径（不依赖具体项目）"""
    if key not in _SHARED_PATHS:
        raise KeyError(f"[glue] 未知共享资源键: {key}，可用: {list(_SHARED_PATHS.keys())}")
    return os.path.normpath(os.path.join(_SHARED_BASE, _SHARED_PATHS[key]))


# ─── 路径键名说明文档 ─────────────────────────────────

PATH_KEYS = """
project.yaml paths 段支持的逻辑键名：

  prd"""
project_config.py — 项目路径解析层（pop-novel-writer 独立版）

职责：
  所有 SKILL.md 里的硬编码相对路径
  统一经过此层解析。不同项目有不同的目录结构，但逻辑键名一致。

用法：
  from glue.project_config import resolve_path, resolve_shared, get_project_config

  # 解析项目内路径
  prd_path = resolve_path("/path/to/project", "prd")
  # → "/path/to/project/00-原始设定/L0-产品层/PRD.md"

  # 批量检查（启动模块前调用）
  check_paths(project_dir, ["prd", "constitution", "l1_dir"])
  # → 缺少即报错退出

在 project.yaml 中扩展 paths 段：
  paths:
    prd: "00-原始设定/L0-产品层/PRD.md"
"""

import os
import sys
import yaml


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


# ─── 共享资源配置（基础降级版，不依赖外部路径）───────────────

_SHARED_PATHS = {
    "scene_fragments_db": "_shared/studio/scene_fragments.db",
    "study_materials": "_shared/study_materials/",
    "plot_library_db": "_shared/studio/plot_library.db",
}

# 共享资源的基准目录 = 本脚本所在目录的上级的上级（popwave-skills/ 或用户项目父目录）
_GLUE_DIR = os.path.dirname(os.path.abspath(__file__))
_SKILL_ROOT = os.path.dirname(_GLUE_DIR)            # pop-novel-writer/
_SHARED_BASE = os.path.normpath(os.path.join(_SKILL_ROOT, "..", ".."))  # popwave-skills/


def resolve_shared(key: str) -> str:
    """解析共享资源路径（不依赖具体项目）"""
    if key not in _SHARED_PATHS:
        raise KeyError(f"[glue] 未知共享资源键: {key}，可用: {list(_SHARED_PATHS.keys())}")
    return os.path.normpath(os.path.join(_SHARED_BASE, _SHARED_PATHS[key]))


# ─── 路径键名说明文档 ─────────────────────────────────

PATH_KEYS = """
project.yaml paths 段支持的逻辑键名：

  prd               PRD.md
  constitution      constitution.yaml
  l1_dir            L1-元设定层/  目录
  l2_dir            L2-展开层/    目录
