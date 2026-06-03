"""
validate.py — Schema 校验层

职责：
  跨模块传递的 YAML 数据文件（act-XX.yaml、chXXX.yaml 等），
  在消费方读取前做字段存在性校验。

  不依赖 jsonschema 库，用纯 Python + yaml 做轻量 required 检查。
  需要更严格的类型/格式校验时，可升级为 pydantic 或 fastjsonschema。

用法：
  from glue.validate import validate_yaml, validate_schema

  # 校验单个文件
  ok = validate_yaml("/path/to/act-01.yaml", "act-XX")

  # 校验目录下所有匹配文件
  ok = validate_schema("/path/to/02-幕纲/", "*.yaml", "act-XX")
"""

import os
import glob
import sys
import yaml

# 确保 glue 包可导入
_GLUE_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_GLUE_PARENT = os.path.dirname(_GLUE_SCRIPT_DIR)
if _GLUE_PARENT not in sys.path:
    sys.path.insert(0, _GLUE_PARENT)

# ─── 内置 Schema 定义 ──────────────────────────────
# 每个 schema 定义 required 字段集合（不含全量校验）
# 扩展方式：加一个条目即可

_SCHEMAS = {}

def _register(name, required_fields):
    _SCHEMAS[name] = {
        "required": required_fields,
        "description": ""
    }

# act-XX.yaml（剧情架构 v2.0 输出 → 章纲生成消费）
_register("act-XX", {
    "act": [
        "number", "title", "chapter_range",
        "payoff_distribution", "emotional_arc", "chapters"
    ],
})

# chXXX.yaml（已废弃——v7.8 上下文组装器直接从幕纲读取数据）
_register("chXXX", {
    "chapter": [
        "number", "payoff_plan", "reader_emotion_path",
        "emotion_anchors", "end_hook", "scenes"
    ],
    "_deprecated": True,
    "_deprecated_at": "2026-05-19",
    "_replaced_by": "幕纲数据直读（act-XX.yaml 的 chapter[N]）",
})

# writer 元数据 12 字段（已废弃——v7.8 已改为6块素材直出）
_register("writer-metadata", {
    "chapter_metadata": [
        "chapter_number", "chapter_position", "pace_type",
        "suspense_operation", "foreshadowing",
        "twist_level", "info_density",
        "summary", "key_characters",
        "emotional_anchor", "next_chapter_hint",
        "scene_type_tags"
    ],
    "_deprecated": True,
    "_deprecated_at": "2026-05-19",
    "_replaced_by": "v7.8 6块素材（全局摘要/本章爽点兑现/角色状态/风格种子/本章设计/下一章钩子）",
})

# project.yaml（扩展：含 reader_profile + paths 检查）
_register("project", {
    "project": ["name", "reader_profile", "paths"],
})


def get_schema(name: str) -> dict:
    """按名字获取 Schema。不存在的名字会报 KeyError"""
    if name not in _SCHEMAS:
        raise KeyError(
            f"[glue] 未知 Schema: '{name}'，可用: {list(_SCHEMAS.keys())}"
        )
    return _SCHEMAS[name]


def check_fun_level_distribution(data: dict, verbose: bool = True) -> bool:
    """
    检查 act-01.yaml 的 chapters 中 fun_level 字段的分布。
    规则：
      1. fun_level 不能连续 2 章为"零"
      2. fun_level 必须每章都有（不能空缺）
    """
    chapters = data.get("act", {}).get("chapters", [])
    if not chapters:
        return True

    all_ok = True
    last_zero = False
    for i, ch in enumerate(chapters):
        fl = ch.get("fun_level")
        if fl is None:
            if verbose:
                print(f"[glue] ❌ ch{ch.get('number', i+1)}: 缺少 fun_level 字段")
            all_ok = False
            continue
        if fl not in ("微", "中", "大", "零"):
            if verbose:
                print(f"[glue] ❌ ch{ch.get('number', i+1)}: fun_level='{fl}' 非法，允许: 微/中/大/零")
            all_ok = False
            continue
        if fl == "零":
            if last_zero:
                if verbose:
                    print(f"[glue] ❌ ch{ch.get('number', i+1)}: fun_level='零'，上一章也是 '零'，连续2章零爽点")
                all_ok = False
            last_zero = True
        else:
            last_zero = False

    return all_ok


def validate_project_config(filepath: str, verbose: bool = True) -> dict:
    """
    project.yaml 专项校验，返回详细检查报告。

    检查项：
      1. 文件存在性
      2. YAML 可解析
      3. project.name 必填
      4. project.reader_profile 存在且含 platform, gender
      5. project.paths.prd 存在
      6. project.paths.database 存在

    返回:
        dict: {
            "valid": bool,
            "checks": [
                {"name": str, "passed": bool, "detail": str},
                ...
            ],
            "errors": [str]
        }
    """
    report = {"valid": True, "checks": [], "errors": []}

    def _check(name: str, passed: bool, detail: str = ""):
        report["checks"].append({"name": name, "passed": passed, "detail": detail})
        if not passed:
            report["valid"] = False
            report["errors"].append(detail if detail else f"{name}: 未通过")

    # 1. 文件存在性
    exists = os.path.isfile(filepath)
    _check("文件存在性", exists,
           f"project.yaml {'存在' if exists else '不存在'}: {filepath}")
    if not exists:
        return report

    # 2. YAML 可解析
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        _check("YAML 解析", data is not None,
               "project.yaml 为空文件" if data is None else "YAML 解析成功")
    except Exception as e:
        _check("YAML 解析", False, f"YAML 解析失败: {e}")
        return report

    if data is None:
        return report

    # 3. project.name 必填
    project = data.get("project", {})
    name = project.get("name")
    _check("project.name", bool(name),
           f"project.name={'✅' if name else '❌ 缺失'}")

    # 4. project.reader_profile 存在且含 platform, gender
    rp = project.get("reader_profile")
    if rp and isinstance(rp, dict):
        rp_ok = bool(rp.get("platform")) and bool(rp.get("gender"))
        rp_detail = (f"platform={rp.get('platform')}, gender={rp.get('gender')}"
                     if rp_ok else f"缺少必要字段（当前: {dict(rp)}）")
        _check("project.reader_profile", rp_ok, rp_detail)
    else:
        _check("project.reader_profile", False,
               "reader_profile 缺失或非字典类型")

    # 5. project.paths.prd 存在
    paths = data.get("paths", {})
    prd = paths.get("prd")
    _check("project.paths.prd", bool(prd),
           f"paths.prd={'✅ ' + str(prd) if prd else '❌ 缺失'}")

    # 6. project.paths.database 存在
    db = paths.get("database")
    _check("project.paths.database", bool(db),
           f"paths.database={'✅ ' + str(db) if db else '❌ 缺失'}")

    return report


def validate_yaml(data_path: str, schema_name: str, verbose: bool = True) -> bool:
    """
    校验单个 YAML 文件的必填字段。

    参数:
      data_path:   YAML 文件路径
      schema_name: Schema 名称（act-XX / chXXX / writer-metadata / project）

    返回:
      True  = 校验通过
      False = 字段缺失（打印缺失列表）
    """
    if not os.path.isfile(data_path):
        if verbose:
            print(f"[glue] ❌ 文件不存在: {data_path}")
        return False

    schema = get_schema(schema_name)

    with open(data_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if data is None:
        if verbose:
            print(f"[glue] ❌ {os.path.basename(data_path)} 为空文件")
        return False

    all_ok = True
    for parent_key, required_children in schema["required"].items():
        parent = data.get(parent_key)
        if parent is None:
            if verbose:
                print(f"[glue] ❌ {os.path.basename(data_path)}: 缺少顶层字段 '{parent_key}'")
            all_ok = False
            continue

        missing = [k for k in required_children if k not in parent]
        if missing:
            if verbose:
                print(f"[glue] ❌ {os.path.basename(data_path)}: {parent_key} 缺少: {missing}")
            all_ok = False

    if all_ok and verbose:
        print(f"[glue] ✅ {os.path.basename(data_path)} schema '{schema_name}' 校验通过")
    return all_ok


def validate_directory(dir_path: str, glob_pattern: str, schema_name: str,
                      verbose: bool = True) -> bool:
    """
    校验目录下所有匹配的文件。

    用法:
      validate_directory("02-幕纲/", "*.yaml", "act-XX")
      validate_directory("03-章纲/", "ch*.yaml", "chXXX")
    """
    if not os.path.isdir(dir_path):
        if verbose:
            print(f"[glue] ❌ 目录不存在: {dir_path}")
        return False

    files = sorted(glob.glob(os.path.join(dir_path, glob_pattern)))
    if not files:
        if verbose:
            print(f"[glue] ⚠️  {dir_path} 下无匹配 {glob_pattern} 的文件，跳过")
        return True  # 没有文件不算失败

    all_ok = True
    passes = 0
    fails = 0
    for fpath in files:
        ok = validate_yaml(fpath, schema_name, verbose=False)
        if ok:
            passes += 1
        else:
            fails += 1
            all_ok = False
            # 失败时再输出详细信息
            validate_yaml(fpath, schema_name, verbose=True)

    if verbose:
        print(f"[glue]   {dir_path}: {passes} 通过, {fails} 失败")
    return all_ok


# ─── CLI ─────────────────────────────────────────


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="YAML Schema 校验器")
    parser.add_argument("target", help="文件路径 或 目录路径")
    parser.add_argument("--schema", required=True,
                        choices=list(_SCHEMAS.keys()),
                        help="Schema 名称")
    parser.add_argument("--pattern", default="*.yaml",
                        help="目录模式下的 glob 匹配（默认: *.yaml）")
    parser.add_argument("--list-schemas", action="store_true",
                        help="列出所有可用 Schema")

    args = parser.parse_args()

    if args.list_schemas:
        print("可用 Schema:")
        for name in _SCHEMAS:
            req = _SCHEMAS[name]["required"]
            print(f"  {name:20s} required: {req}")
        sys.exit(0)

    if os.path.isdir(args.target):
        ok = validate_directory(args.target, args.pattern, args.schema)
    else:
        ok = validate_yaml(args.target, args.schema)

    import sys
    sys.exit(0 if ok else 1)
