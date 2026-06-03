"""
glue/orchestrate.py — pop Harness 编排控制器 CLI 入口

调用方式：
    # 直接编排
    python glue/orchestrate.py "写第8章正文" --project "/path/to/project"
    
    # 仅查路由（不动文件）
    python glue/orchestrate.py "HTML化场景卡" --dry-run
    
    # 显示路由表
    python glue/orchestrate.py --list-routes

职责：
    pop agent 的外部 CLI 入口。
    pop 收到需求后 -> 调 orchestrate.py -> 查路由 + 读 frontmatter + 前置检查 -> 返回任务单
"""

import os
import sys
import json

# 确保能找到 pop 模块
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_PARENT = os.path.dirname(_SCRIPT_DIR)  # novel-agent-pro/
if _PARENT not in sys.path:
    sys.path.insert(0, _PARENT)

from skills._shared.pop.dispatcher import Harness, ROUTING_TABLE


# ★ Spec 桥接检查
def check_spec_gate(project_dir: str, skill_name: str) -> bool:
    """
    检查 Spec 闸门：如果目标 skill 需要 spec 约束但不存在 spec.md，返回 False。
    """
    if skill_name not in ("skill-emergent-writer", "skill-qa-payoff"):
        return True  # 不需要 spec 闸门的 skill
    
    spec_base = os.path.join(project_dir, ".trae", "specs")
    if not os.path.isdir(spec_base):
        return False  # 没有任何 spec
    
    # 检查是否存在最新 spec
    spec_dirs = [d for d in os.listdir(spec_base) if os.path.isdir(os.path.join(spec_base, d))]
    if not spec_dirs:
        return False
    
    # 只检查是否有任何 spec 存在（具体到哪个 change-id 由 Agent 判断）
    latest = sorted(spec_dirs)[-1]
    spec_file = os.path.join(spec_base, latest, "spec.md")
    return os.path.isfile(spec_file)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="pop Harness 编排控制器")
    parser.add_argument("user_intent", nargs="?", default="", help="用户需求文本")
    parser.add_argument("--project", "-p", default="", help="项目路径")
    parser.add_argument("--dry-run", action="store_true", help="仅查路由不动文件")
    parser.add_argument("--list-routes", action="store_true", help="显示路由表")
    parser.add_argument("--json", action="store_true", help="JSON 格式输出")
    parser.add_argument("--describe", action="store_true", help="输出 pop 声明文本")
    args = parser.parse_args()
    
    if args.list_routes:
        print("📋 pop Harness 路由表（★ Spec 深度整合 v4.0）")
        print("=" * 60)
        for keywords, category, skill, display in ROUTING_TABLE:
            marker = " ★ " if skill == "spec-bridge" else "   "
            print(f"  {marker}{display:16s} | {category:12s} | {skill}")
            print(f"      ↳ 关键词: {', '.join(keywords[:4])}")
        print()
        print("📋 Spec 闸门规则：")
        print("  写作/质检类任务前，如果不存在 spec.md → 先路由到 spec-bridge")
        return
    
    if not args.user_intent:
        parser.print_help()
        return
    
    harness = Harness(args.project)
    job = harness.route(args.user_intent, args.project, args.dry_run)
    
    if args.json:
        output = {
            "skill_name": job.skill_name,
            "display_name": job.display_name,
            "category": job.category,
            "version": job.version,
            "pass_gate": job.pass_gate,
            "preflight": job.preflight_results,
            "errors": job.errors,
            "prompt_length": len(job.prompt),
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return
    
    if args.describe:
        desc = harness.describe(job)
        # 追加 Spec 闸门信息
        if job.skill_name in ("skill-emergent-writer", "skill-qa-payoff"):
            spec_ok = check_spec_gate(args.project, job.skill_name)
            spec_status = "✅ spec.md 就绪" if spec_ok else "⚠️ 无 spec.md — 建议先调 spec-bridge"
            desc += f"\n  ★ Spec 状态: {spec_status}"
        print(desc)
        return
    
    # 默认输出
    print("=" * 60)
    print(harness.describe(job))
    print("=" * 60)
    
    if not args.dry_run and job.pass_gate:
        print(f"\n📋 任务单已就绪，可调 {job.skill_name} 执行")
        print(f"📦 上下文: {len(job.context)} 项")
    elif not args.dry_run and not job.pass_gate:
        print(f"\n❌ 大门关闭 — 以下前置条件未通过:")
        for e in job.errors:
            print(f"  - {e}")


if __name__ == "__main__":
    main()
