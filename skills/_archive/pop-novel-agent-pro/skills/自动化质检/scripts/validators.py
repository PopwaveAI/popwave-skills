"""
validators.py — 内置质量闸门验证器

适用场景：
- 字数范围检查 (word_count)
- 执行超时检查 (timeout)
- 实体覆盖率检查 (entity_coverage)
- 文件存在检查 (file_exists)
- 文件大小检查 (file_size)
- 正则内容匹配 (regex_match)
- 自定义检查 (custom)

所有验证器返回统一格式：
    {"rule": str, "passed": bool, "actual": any, "threshold": dict, "severity": "error"|"warn", ...}
"""

import os
import re
import time


# ── 验证器注册表 ──
VALIDATORS = {}


def register(name):
    """装饰器：注册验证器到 VALIDATORS 字典。"""
    def decorator(func):
        VALIDATORS[name] = func
        return func
    return decorator


# ── 字数检查 ──

@register("word_count")
def validate_word_count(output, rule_config):
    """
    检查输出文本的字数是否在 [min, max] 范围内。
    rule_config: {"type": "word_count", "min": int, "max": int, "severity": "error"|"warn"}
    output: dict, 必须包含 "text" 或 "file_paths" 用于读取文本
    """
    text = _get_output_text(output)
    wc = len(text)
    min_wc = rule_config.get("min", 0)
    max_wc = rule_config.get("max", float("inf"))

    passed = min_wc <= wc <= max_wc
    return {
        "rule": "word_count",
        "passed": passed,
        "actual": wc,
        "threshold": {"min": min_wc, "max": max_wc if max_wc != float("inf") else None},
        "severity": rule_config.get("severity", "error"),
        "message": f"字数 {wc}，要求 [{min_wc}, {max_wc if max_wc != float('inf') else '∞'}]"
    }


# ── 执行超时检查 ──

@register("timeout")
def validate_timeout(output, rule_config):
    """
    检查执行耗时是否在 max_seconds 范围内。
    rule_config: {"type": "timeout", "max_seconds": int, "severity": "error"|"warn"}
    output: dict, 必须包含 "duration_ms"
    """
    duration_ms = output.get("duration_ms", 0)
    max_sec = rule_config.get("max_seconds", 300)
    passed = (duration_ms / 1000) <= max_sec

    return {
        "rule": "timeout",
        "passed": passed,
        "actual": f"{duration_ms/1000:.1f}s",
        "threshold": {"max_seconds": max_sec},
        "severity": rule_config.get("severity", "error"),
        "message": f"耗时 {duration_ms/1000:.1f}s，上限 {max_sec}s"
    }


# ── 实体覆盖率检查 ──

@register("entity_coverage")
def validate_entity_coverage(output, rule_config):
    """
    检查文本中是否包含必需的实体标记。
    rule_config: {"type": "entity_coverage", "required_entities": [str], "min_coverage": float, "severity": "error"|"warn"}
    output: dict, 必须包含 "text"
    """
    text = _get_output_text(output)
    required = rule_config.get("required_entities", [])
    min_cov = rule_config.get("min_coverage", 0.8)

    if not required:
        return {"rule": "entity_coverage", "passed": True, "actual_coverage": 1.0, "message": "无required_entities配置，跳过"}

    matched = [e for e in required if e in text]
    coverage = len(matched) / len(required)
    missing = [e for e in required if e not in text]
    passed = coverage >= min_cov

    return {
        "rule": "entity_coverage",
        "passed": passed,
        "actual_coverage": round(coverage, 2),
        "required_entities": required,
        "matched": matched,
        "missing": missing,
        "severity": rule_config.get("severity", "error"),
        "message": f"覆盖率 {coverage:.0%}，要求 {min_cov:.0%}；缺失: {missing}"
    }


# ── 文件存在检查 ──

@register("file_exists")
def validate_file_exists(output, rule_config):
    """
    检查要求的文件路径是否存在。
    rule_config: {"type": "file_exists", "required_paths": [str], "severity": "error"|"warn"}
    """
    required_paths = rule_config.get("required_paths", [])
    output_paths = set(output.get("file_paths", []))

    missing_paths = [p for p in required_paths if p not in output_paths and not os.path.isfile(p)]
    passed = len(missing_paths) == 0

    return {
        "rule": "file_exists",
        "passed": passed,
        "actual_files_found": len(required_paths) - len(missing_paths),
        "required_paths": required_paths,
        "missing_paths": missing_paths,
        "severity": rule_config.get("severity", "error"),
        "message": f"缺少 {len(missing_paths)} 个文件: {missing_paths}"
    }


# ── 文件大小检查 ──

@register("file_size")
def validate_file_size(output, rule_config):
    """
    检查输出文件大小是否在范围内。
    rule_config: {"type": "file_size", "min_bytes": int, "max_bytes": int, "severity": "error"|"warn"}
    output: dict, 必须包含 "file_paths"
    """
    file_paths = output.get("file_paths", [])
    min_b = rule_config.get("min_bytes", 0)
    max_b = rule_config.get("max_bytes", float("inf"))

    results = []
    all_passed = True
    for fp in file_paths:
        if os.path.isfile(fp):
            size = os.path.getsize(fp)
            passed = min_b <= size <= max_b
            if not passed:
                all_passed = False
            results.append({"file": fp, "size": size, "passed": passed})
        else:
            results.append({"file": fp, "size": None, "passed": False})
            all_passed = False

    return {
        "rule": "file_size",
        "passed": all_passed,
        "results": results,
        "threshold": {"min_bytes": min_b, "max_bytes": max_b if max_b != float("inf") else None},
        "severity": rule_config.get("severity", "error"),
        "message": f"检查了 {len(results)} 个文件"
    }


# ── 正则匹配检查 ──

@register("regex_match")
def validate_regex_match(output, rule_config):
    """
    检查输出文本是否匹配/不匹配指定正则。
    rule_config: {"type": "regex_match", "pattern": str, "must_match": bool, "severity": "error"|"warn"}
    """
    text = _get_output_text(output)
    pattern = rule_config.get("pattern", "")
    must_match = rule_config.get("must_match", True)

    found = bool(re.search(pattern, text))
    passed = found == must_match

    return {
        "rule": "regex_match",
        "passed": passed,
        "pattern": pattern,
        "must_match": must_match,
        "found": found,
        "severity": rule_config.get("severity", "error"),
        "message": f"模式 '{pattern}' {'需匹配' if must_match else '需不匹配'}，{'找到' if found else '未找到'}"
    }


# ── 自定义检查 ──

@register("custom")
def validate_custom(output, rule_config):
    """
    注册到 CUSTOM_VALIDATORS 中的自定义函数。
    rule_config: {"type": "custom", "function_name": str, "args": dict, "severity": "error"|"warn"}
    """
    func_name = rule_config.get("function_name", "")
    args = rule_config.get("args", {})

    if func_name in CUSTOM_VALIDATORS:
        return CUSTOM_VALIDATORS[func_name](output, args)
    else:
        return {
            "rule": "custom",
            "passed": False,
            "function_name": func_name,
            "severity": rule_config.get("severity", "error"),
            "message": f"自定义函数 '{func_name}' 未注册"
        }


# ── 自定义验证器扩展点 ──

CUSTOM_VALIDATORS = {}


def register_custom(name):
    """注册自定义验证器。"""
    def decorator(func):
        CUSTOM_VALIDATORS[name] = func
        VALIDATORS["custom:" + name] = lambda o, rc: func(o, rc.get("args", {}))
        return func
    return decorator


# ── 辅助函数 ──

def _get_output_text(output):
    """从 output 字典中提取文本内容。"""
    if "text" in output and output["text"]:
        return output["text"]
    # 尝试从文件读取
    for fp in output.get("file_paths", []):
        if os.path.isfile(fp):
            try:
                with open(fp, "r", encoding="utf-8") as f:
                    return f.read()
            except Exception:
                continue
    return ""


# ── 批量验证接口 ──

def run_validators(output, validators_config):
    """
    对 output 运行一系列验证器。
    
    参数:
        output: dict — 步骤产出物
        validators_config: list — 验证器配置列表
    
    返回:
        list[dict] — 验证结果列表
        bool — 是否全部通过（severity=error 的规则全部 passed=True）
    """
    results = []
    all_passed = True

    for vc in validators_config:
        vtype = vc.get("type", "")
        validator = VALIDATORS.get(vtype)

        if not validator:
            results.append({
                "rule": vtype,
                "passed": False,
                "severity": vc.get("severity", "error"),
                "message": f"未找到验证器: {vtype}"
            })
            if vc.get("severity", "error") == "error":
                all_passed = False
            continue

        result = validator(output, vc)
        results.append(result)
        if result["severity"] == "error" and not result["passed"]:
            all_passed = False

    return results, all_passed
