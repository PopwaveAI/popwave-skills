"""
audit_logger.py — 审计追溯日志系统

核心功能：
1. 按 run_id 组织审计日志目录
2. 每一步写入一条结构化 JSON 审计记录
3. 追加式 audit_trail.jsonl 事件流水（不可变）
4. 最终生成 summary.json 汇总报告

使用方式：
    logger = AuditLogger(run_id, output_dir)
    logger.write_step(step_id, step_data)
    logger.write_event(step_id, event_type, extra_data)
    summary = logger.finalize()
"""

import os
import json
import time
from datetime import datetime, timezone


class AuditLogger:
    """审计追溯日志记录器。"""

    def __init__(self, run_id: str, output_dir: str, meta: dict = None):
        """
        初始化审计日志记录器。

        参数:
            run_id: 运行 ID，如 "qc_20260526_001"
            output_dir: 输出根目录，如 ".qc_reports"
            meta: 可选的元信息，如 {"target_skill": "...", "started_at": "..."}
        """
        self.run_id = run_id
        self.log_dir = os.path.join(output_dir, run_id)
        self.steps_dir = os.path.join(self.log_dir, "steps")
        self.trail_path = os.path.join(self.log_dir, "audit_trail.jsonl")
        self.summary_path = os.path.join(self.log_dir, "summary.json")
        self.meta_path = os.path.join(self.log_dir, "meta.json")

        # 确保目录存在
        os.makedirs(self.steps_dir, exist_ok=True)

        # 写入 meta.json
        if meta is None:
            meta = {}
        meta.setdefault("run_id", run_id)
        meta.setdefault("created_at", datetime.now(timezone.utc).isoformat())
        with open(self.meta_path, "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)

        # 初始化汇总数据累加器
        self._step_records = []
        self._event_count = 0

        # 写入启动事件
        self.write_event("__pipeline__", "pipeline_started", meta)

    def write_event(self, step_id: str, event: str, extra: dict = None):
        """
        写入一条事件到 audit_trail.jsonl（追加式，不可变）。

        参数:
            step_id: 步骤 ID
            event: 事件类型（step_started, executor_invoked, validation_started, ...）
            extra: 额外数据（可选）
        """
        record = {
            "run_id": self.run_id,
            "step_id": step_id,
            "event": event,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        if extra:
            record.update(extra)

        try:
            with open(self.trail_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
            self._event_count += 1
        except IOError as e:
            # 降级：输出警告
            print(f"[AuditLogger] ⚠️ 事件写入失败: {e}")

    def write_step(self, step_id: str, step_data: dict):
        """
        写入一个步骤的完整审计记录。

        参数:
            step_id: 步骤 ID
            step_data: 步骤审计数据字典（包含 timing/output/validation/llm/anomalies 等）
        """
        path = os.path.join(self.steps_dir, f"{step_id}.json")
        record = {
            "run_id": self.run_id,
            "step_id": step_id,
            "recorded_at": datetime.now(timezone.utc).isoformat(),
            **step_data
        }

        with open(path, "w", encoding="utf-8") as f:
            json.dump(record, f, ensure_ascii=False, indent=2)

        self._step_records.append(record)

        # 写入完成事件
        status = step_data.get("status", "UNKNOWN")
        self.write_event(step_id, f"step_{status.lower()}", {
            "duration_ms": step_data.get("timing", {}).get("duration_ms"),
            "anomalies_count": len(step_data.get("anomalies", []))
        })

    def write_block(self, step_id: str, blocked_by: str, reason: str, timeout_minutes: int = 30):
        """
        记录一个阻塞事件。

        参数:
            step_id: 被阻塞的步骤 ID
            blocked_by: 导致阻塞的步骤 ID
            reason: 阻塞原因
            timeout_minutes: 超时时间（分钟）
        """
        block_data = {
            "blocked_step_id": step_id,
            "blocked_by_step_id": blocked_by,
            "blocked_at": datetime.now(timezone.utc).isoformat(),
            "reason": reason,
            "status": "BLOCKED",
            "timeout_at": datetime.fromtimestamp(
                time.time() + timeout_minutes * 60, tz=timezone.utc
            ).isoformat(),
            "auto_action_on_timeout": "skip",
            "resolved_at": None
        }
        self.write_event("__block__", "step_blocked", block_data)

    def write_resolve(self, step_id: str, action: str = "confirmed"):
        """记录阻塞解除。"""
        self.write_event("__block__", "block_resolved", {
            "step_id": step_id,
            "action": action,
            "resolved_at": datetime.now(timezone.utc).isoformat()
        })

    def get_trail_path(self) -> str:
        """返回 audit_trail.jsonl 的路径。"""
        return self.trail_path

    def finalize(self) -> dict:
        """
        完成审计，生成 summary.json。
        
        返回:
            summary dict
        """
        passed = sum(1 for r in self._step_records if r.get("status") == "COMPLETED" and not r.get("anomalies"))
        failed = sum(1 for r in self._step_records if r.get("status") == "FAILED")
        blocked = sum(1 for r in self._step_records if r.get("status") == "BLOCKED")
        warned = sum(1 for r in self._step_records if r.get("anomalies"))

        summary = {
            "run_id": self.run_id,
            "completed_at": datetime.now(timezone.utc).isoformat(),
            "total_steps": len(self._step_records),
            "passed_steps": passed,
            "failed_steps": failed,
            "blocked_steps": blocked,
            "warned_steps": warned,
            "total_events_logged": self._event_count,
            "step_summaries": [
                {
                    "step_id": r.get("step_id"),
                    "step_name": r.get("step_name"),
                    "status": r.get("status"),
                    "duration_ms": r.get("timing", {}).get("duration_ms"),
                    "anomalies_count": len(r.get("anomalies", [])),
                    "llm_passed": r.get("llm_verification", {}).get("passed") if r.get("llm_verification") else None
                }
                for r in self._step_records
            ]
        }

        with open(self.summary_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)

        self.write_event("__pipeline__", "pipeline_completed", {
            "total_steps": summary["total_steps"],
            "passed": passed,
            "failed": failed,
            "blocked": blocked
        })

        return summary
