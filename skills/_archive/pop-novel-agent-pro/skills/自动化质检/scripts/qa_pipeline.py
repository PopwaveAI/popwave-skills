"""
qa_pipeline.py — 自动化质检管线主入口

执行一次完整的质检管线流程：
  1. 解析 PipelineConfig
  2. 按步骤序列顺序执行
  3. 每步：执行 → 验证器链 → LLM 验证 → 阻塞判断 → 审计写入
  4. 输出最终 QCReport

使用方式：
    from 自动化质检.scripts.qa_pipeline import run_qc_pipeline

    config = { ... }  # PipelineConfig 字典
    report = run_qc_pipeline(config)
    print(report["overall_status"])
"""

import os
import json
import time
import uuid
from datetime import datetime, timezone

from .validators import run_validators
from .audit_logger import AuditLogger
from .qc_api_check import call_llm_verify


# ── 默认配置 ──
DEFAULT_OUTPUT_DIR = ".qc_reports"
DEFAULT_BLOCK_TIMEOUT = 30  # 分钟
DEFAULT_BLOCK_ACTION = "skip"


# ── 主入口 ──

def run_qc_pipeline(config: dict) -> dict:
    """
    执行一次完整的质检管线。

    参数:
        config: PipelineConfig 字典，结构见 SKILL.md 文档

    返回:
        QCReport 字典
    """
    # ── 初始化 ──
    run_id = config.get("run_id", f"qc_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}")
    global_config = config.get("global_config", {})
    output_dir = global_config.get("output_dir", DEFAULT_OUTPUT_DIR)
    steps_config = config.get("steps", [])

    if not steps_config:
        return {
            "run_id": run_id,
            "overall_status": "FAILED",
            "error": "PipelineConfig.steps 为空"
        }

    # 初始化审计日志
    meta = {
        "run_id": run_id,
        "target_skill": config.get("target_skill", "unknown"),
        "started_at": datetime.now(timezone.utc).isoformat(),
        "total_steps": len(steps_config)
    }
    logger = AuditLogger(run_id, output_dir, meta)

    # ── 统计累加器 ──
    step_records = []
    global_anomalies = []
    blocked_steps = set()

    # ── 步骤循环 ──
    for i, step_cfg in enumerate(steps_config):
        step_id = step_cfg.get("id", f"step_{i+1:02d}")
        step_name = step_cfg.get("name", step_id)

        print(f"\n{'='*50}")
        print(f"▶️ [{step_id}] {step_name}")

        # 检查是否被上一步阻塞
        if step_id in blocked_steps:
            logger.write_step(step_id, {
                "step_name": step_name,
                "status": "BLOCKED",
                "anomalies": [{"message": "被上一步阻塞"}],
                "blocked_by": list(blocked_steps)
            })
            step_records.append({"step_id": step_id, "status": "BLOCKED"})
            continue

        # 开始计时
        step_start = time.time()
        logger.write_event(step_id, "step_started")

        # ── 执行 ──
        executor = step_cfg.get("executor", {})
        executor_type = executor.get("type", "skill")

        output = _execute_step(executor_type, executor, step_id)

        step_elapsed_ms = int((time.time() - step_start) * 1000)
        output["duration_ms"] = step_elapsed_ms

        logger.write_event(step_id, "executor_completed", {
            "executor_type": executor_type,
            "duration_ms": step_elapsed_ms
        })

        # ── 验证器链 ──
        validators_config = step_cfg.get("validators", [])
        validation_results = []

        if validators_config:
            logger.write_event(step_id, "validation_started")
            validation_results, all_passed = run_validators(output, validators_config)
            logger.write_event(step_id, "validation_completed", {
                "rules_total": len(validation_results),
                "rules_passed": sum(1 for r in validation_results if r["passed"]),
                "rules_failed": sum(1 for r in validation_results if not r["passed"])
            })
        else:
            all_passed = True

        # ── LLM 独立验证 ──
        llm_verify_cfg = step_cfg.get("llm_verify", {})
        llm_result = None

        if llm_verify_cfg.get("enabled", False):
            logger.write_event(step_id, "llm_verify_started")
            api_config = global_config.get("api", {})
            template_name = llm_verify_cfg.get("template_name", "content_review")
            dimensions = llm_verify_cfg.get("scoring_dimensions", [])
            text = output.get("text", "")

            llm_start = time.time()
            llm_result = call_llm_verify(api_config, template_name, text, dimensions)
            llm_latency_ms = int((time.time() - llm_start) * 1000)

            if "error" not in llm_result:
                scores = llm_result.get("scores", {})
                avg_score = sum(scores.values()) / len(scores) if scores else 0
                llm_passed = llm_result.get("overall_pass", avg_score >= llm_verify_cfg.get("pass_threshold", 0.6))

                llm_result["api_latency_ms"] = llm_latency_ms
                llm_result["average_score"] = avg_score
                llm_result["passed"] = llm_passed
            else:
                llm_result["passed"] = False
                llm_result["api_latency_ms"] = llm_latency_ms

            logger.write_event(step_id, "llm_verify_completed", {
                "latency_ms": llm_latency_ms,
                "passed": llm_result.get("passed", False),
                "average_score": llm_result.get("average_score", 0)
            })

        # ── 异常收集 ──
        anomalies = []
        for vr in validation_results:
            if not vr["passed"]:
                anomalies.append({
                    "rule": vr["rule"],
                    "severity": vr["severity"],
                    "message": vr.get("message", "")
                })

        if llm_result and "error" in llm_result:
            anomalies.append({
                "rule": "llm_verify",
                "severity": "warn",
                "message": f"LLM验证异常: {llm_result['error']}"
            })

        step_status = "COMPLETED" if not [a for a in anomalies if a["severity"] == "error"] else "FAILED"
        if anomalies:
            step_status = "COMPLETED_WITH_ANOMALIES" if step_status == "COMPLETED" else "FAILED"

        # ── 阻塞判断 ──
        block_on_failure = step_cfg.get("block_on_failure", True)
        should_block = step_status in ("FAILED", "COMPLETED_WITH_ANOMALIES") and block_on_failure

        if should_block:
            timeout_min = global_config.get("block_timeout_minutes", DEFAULT_BLOCK_TIMEOUT)
            logger.write_block(
                step_id=f"step_{i+2:02d}" if i + 1 < len(steps_config) else "__end__",
                blocked_by=step_id,
                reason=f"步骤[{step_name}]异常: {anomalies[0]['message'] if anomalies else '未知'}",
                timeout_minutes=timeout_min
            )
            if i + 1 < len(steps_config):
                blocked_steps.add(steps_config[i + 1].get("id", f"step_{i+2:02d}"))

        # ── 写入审计记录 ──
        step_record = {
            "step_id": step_id,
            "step_name": step_name,
            "status": step_status,
            "timing": {
                "started_at": datetime.fromtimestamp(step_start, tz=timezone.utc).isoformat(),
                "completed_at": datetime.now(timezone.utc).isoformat(),
                "duration_ms": step_elapsed_ms
            },
            "output": {
                "word_count": len(output.get("text", "")),
                "file_paths": output.get("file_paths", [])
            },
            "validation_results": validation_results,
            "llm_verification": llm_result,
            "anomalies": anomalies,
            "blocked_next": should_block,
            "file_access_log": output.get("file_access_log", [])
        }

        logger.write_step(step_id, step_record)
        step_records.append(step_record)

        if step_status.startswith("FAILED"):
            print(f"  ❌ [{step_id}] FAILED — {anomalies[0]['message'] if anomalies else ''}")
            if should_block:
                print(f"  ⛔ 下一步被阻塞")
        else:
            print(f"  ✅ [{step_id}] {step_status}" + (f"  ⚠️ {len(anomalies)}个异常" if anomalies else ""))

    # ── 生成最终报告 ──
    summary = logger.finalize()

    # 汇总状态
    all_failed = all(r.get("status", "").startswith("FAILED") or r.get("status") == "BLOCKED" for r in step_records)
    has_anomalies = any(r.get("anomalies") for r in step_records)
    has_blocked = any(r.get("status") == "BLOCKED" for r in step_records)

    if all_failed:
        overall = "FAILED"
    elif has_anomalies or has_blocked:
        overall = "COMPLETED_WITH_WARNINGS"
        if has_blocked:
            overall = "BLOCKED"
    else:
        overall = "PASSED"

    report = {
        "run_id": run_id,
        "target_skill": config.get("target_skill", "unknown"),
        "started_at": meta["started_at"],
        "completed_at": datetime.now(timezone.utc).isoformat(),
        "overall_status": overall,
        "steps_summary": summary.get("step_summaries", []),
        "global_metrics": {
            "total_steps": len(step_records),
            "passed_steps": sum(1 for r in step_records if r.get("status") in ("COMPLETED",)),
            "failed_steps": sum(1 for r in step_records if r.get("status", "").startswith("FAILED")),
            "blocked_events": sum(1 for r in step_records if r.get("status") == "BLOCKED"),
        },
        "audit_log_path": logger.log_dir
    }

    print(f"\n{'='*50}")
    print(f"📊 QC 报告: {run_id}")
    print(f"    总体状态: {overall}")
    print(f"    步骤: {report['global_metrics']['passed_steps']}通过 / {report['global_metrics']['failed_steps']}失败")
    print(f"    审计日志: {logger.log_dir}")

    return report


# ── 辅助：步骤执行器 ──

def _execute_step(executor_type: str, executor: dict, step_id: str) -> dict:
    """
    执行一个步骤，返回 output 字典。

    返回值格式:
        {
            "text": str,           # 步骤产出的文本内容
            "file_paths": [str],   # 产出文件路径列表
            "duration_ms": int,    # 执行耗时（毫秒）
            "file_access_log": []  # 文件访问记录
        }
    """
    output = {
        "text": "",
        "file_paths": [],
        "file_access_log": []
    }

    if executor_type == "command":
        import subprocess
        command = executor.get("command", "")
        cwd = executor.get("cwd")
        if command:
            try:
                result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True, timeout=300)
                output["text"] = result.stdout
                if result.returncode != 0:
                    output["text"] += f"\nSTDERR:\n{result.stderr}"
            except subprocess.TimeoutExpired:
                output["text"] = "[ERROR: 命令执行超时]"

    elif executor_type == "function":
        func_name = executor.get("function_name", "")
        args = executor.get("args", {})
        # 尝试从外部传入的注册表调用
        if func_name in _FUNCTION_REGISTRY:
            try:
                result = _FUNCTION_REGISTRY[func_name](**args)
                if isinstance(result, dict):
                    output.update(result)
                elif isinstance(result, str):
                    output["text"] = result
            except Exception as e:
                output["text"] = f"[ERROR: 函数执行异常] {str(e)}"
        else:
            output["text"] = f"[ERROR: 未注册函数] {func_name}"

    elif executor_type == "skill":
        # skill 模式：由调用方负责执行，这里只记录
        output["text"] = executor.get("params", {}).get("expected_output", "")
        output["note"] = "skill模式：由外部执行，此处为占位"

    return output


# ── 函数注册表（扩展点） ──

_FUNCTION_REGISTRY = {}


def register_function(name):
    """注册一个可被 executor_type="function" 调用的函数。"""
    def decorator(func):
        _FUNCTION_REGISTRY[name] = func
        return func
    return decorator


# ── 阻塞确认/状态查询接口 ──

def confirm_step(run_id: str, step_id: str, output_dir: str = DEFAULT_OUTPUT_DIR) -> bool:
    """
    人工确认解除步骤阻塞。

    参数:
        run_id: 运行 ID
        step_id: 被阻塞的步骤 ID
        output_dir: 审计日志根目录

    返回:
        bool — 确认是否成功
    """
    from .audit_logger import AuditLogger
    log_dir = os.path.join(output_dir, run_id)
    if not os.path.isdir(log_dir):
        return False

    # 追加一条确认事件
    trail_path = os.path.join(log_dir, "audit_trail.jsonl")
    record = {
        "run_id": run_id,
        "step_id": step_id,
        "event": "manual_confirm",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "action": "confirmed"
    }
    try:
        with open(trail_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
        return True
    except IOError:
        return False


def get_pipeline_status(run_id: str, output_dir: str = DEFAULT_OUTPUT_DIR) -> dict:
    """
    查询管线执行状态。

    参数:
        run_id: 运行 ID
        output_dir: 审计日志根目录

    返回:
        {"summary": dict, "steps": list, "last_events": list} 或 {"error": str}
    """
    run_dir = os.path.join(output_dir, run_id)
    if not os.path.isdir(run_dir):
        return {"error": f"未找到运行记录: {run_id}"}

    result = {}
    summary_path = os.path.join(run_dir, "summary.json")
    if os.path.isfile(summary_path):
        with open(summary_path, "r", encoding="utf-8") as f:
            result["summary"] = json.load(f)

    steps_dir = os.path.join(run_dir, "steps")
    if os.path.isdir(steps_dir):
        steps = []
        for fn in sorted(os.listdir(steps_dir)):
            if fn.endswith(".json"):
                with open(os.path.join(steps_dir, fn), "r", encoding="utf-8") as f:
                    steps.append(json.load(f))
        result["steps"] = steps

    # 最后10条事件
    trail_path = os.path.join(run_dir, "audit_trail.jsonl")
    if os.path.isfile(trail_path):
        events = []
        with open(trail_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    events.append(json.loads(line))
        result["last_events"] = events[-10:]

    return result


# ── CLI 入口 ──

def main():
    """命令行调用入口。"""
    import argparse

    parser = argparse.ArgumentParser(description="自动化质检管线")
    parser.add_argument("--config", required=True, help="PipelineConfig JSON 文件路径")
    parser.add_argument("--output", help="输出目录（覆盖 global_config.output_dir）")
    parser.add_argument("--status", help="查询指定 run_id 的状态")

    args = parser.parse_args()

    if args.status:
        result = get_pipeline_status(args.status, args.output or DEFAULT_OUTPUT_DIR)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    with open(args.config, "r", encoding="utf-8") as f:
        config = json.load(f)

    if args.output:
        config.setdefault("global_config", {})["output_dir"] = args.output

    report = run_qc_pipeline(config)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
