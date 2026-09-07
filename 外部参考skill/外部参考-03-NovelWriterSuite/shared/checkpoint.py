#!/usr/bin/env python3
"""
novel-suite checkpoint manager — 创建快照、回滚、列出、删除。

借鉴 novel-writer/scripts/checkpoint.py 设计，全部独立重写：
- vault 路径作为参数传入（不硬编码 ~/Documents）
- 自动扫描 vault 关键文件（不硬编码文件列表）
- JSON 序列化文件内容做快照
- 检查点存放在 vault/.memory/checkpoints/<name>.checkpoint

用法：
    python3 checkpoint.py create --vault /path/to/vault --name step_3_complete
    python3 checkpoint.py rollback --vault /path/to/vault --name step_3_complete
    python3 checkpoint.py list --vault /path/to/vault
    python3 checkpoint.py delete --vault /path/to/vault --name step_3_complete
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

# vault 中需要被快照的关键文件（按 DESIGN.md 第 3 节）
SNAPSHOT_PATTERNS = [
    "story.md",
    "status.md",
    "style/_index.md",
    "style/features.md",
    "style/anti-ai.md",
    "style/compiled/*.md",
    "characters/_index.md",
    "characters/*.md",
    "worldbuilding/_index.md",
    "worldbuilding/locations/*.md",
    "worldbuilding/systems/*.md",
    "plot/_index.md",
    "plot/timeline.md",
    "plot/foreshadowing.md",
    "plot/arcs/*.md",
    "chapters/_index.md",
    "chapters/*.md",
    ".memory/*.md",
]


def collect_files(vault: Path) -> list[Path]:
    """扫描 vault，返回所有需要快照的文件的绝对路径。"""
    files: list[Path] = []
    for pattern in SNAPSHOT_PATTERNS:
        for path in vault.glob(pattern):
            if path.is_file():
                files.append(path)
    # 去重保序
    seen = set()
    unique: list[Path] = []
    for path in files:
        if path not in seen:
            seen.add(path)
            unique.append(path)
    return unique


def checkpoint_dir(vault: Path) -> Path:
    d = vault / ".memory" / "checkpoints"
    d.mkdir(parents=True, exist_ok=True)
    return d


def cmd_create(vault: Path, name: str) -> int:
    if not vault.exists():
        print(f"❌ vault 不存在：{vault}", file=sys.stderr)
        return 1

    files = collect_files(vault)
    if not files:
        print(f"⚠️  vault 中没有发现可快照的文件：{vault}", file=sys.stderr)
        return 1

    payload = {
        "name": name,
        "vault": str(vault.resolve()),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "files": {},
    }

    for path in files:
        rel = path.relative_to(vault)
        try:
            payload["files"][str(rel)] = path.read_text(encoding="utf-8")
        except Exception as exc:
            print(f"⚠ 跳过 {rel}：{exc}", file=sys.stderr)

    target = checkpoint_dir(vault) / f"{name}.checkpoint"
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"✅ 检查点已创建：{name}")
    print(f"   路径：{target}")
    print(f"   文件数：{len(payload['files'])}")
    print(f"   时间：{payload['created_at']}")
    return 0


def cmd_rollback(vault: Path, name: str, force: bool) -> int:
    target = checkpoint_dir(vault) / f"{name}.checkpoint"
    if not target.exists():
        print(f"❌ 检查点不存在：{name}", file=sys.stderr)
        cmd_list(vault)
        return 1

    payload = json.loads(target.read_text(encoding="utf-8"))
    files = payload.get("files", {})

    print(f"⚠️  即将回滚到检查点：{name}")
    print(f"   创建时间：{payload.get('created_at', '?')}")
    print(f"   将覆盖 {len(files)} 个文件：")
    for rel in sorted(files.keys()):
        print(f"     - {rel}")

    if not force:
        try:
            answer = input("\n确认回滚？输入 yes 继续：").strip().lower()
        except EOFError:
            answer = ""
        if answer != "yes":
            print("已取消")
            return 1

    restored = 0
    for rel, content in files.items():
        path = vault / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            path.write_text(content, encoding="utf-8")
            restored += 1
        except Exception as exc:
            print(f"❌ 恢复失败 {rel}：{exc}", file=sys.stderr)

    print(f"\n✅ 回滚完成，恢复 {restored} 个文件")
    return 0


def cmd_list(vault: Path) -> int:
    cps = sorted(checkpoint_dir(vault).glob("*.checkpoint"))
    if not cps:
        print("📭 没有检查点")
        return 0

    print(f"\n📋 检查点（{len(cps)} 个）\n")
    print(f"{'名称':<40} {'创建时间':<22} {'文件':>5}")
    print("-" * 70)
    for path in cps:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            name = data.get("name", path.stem)
            created = data.get("created_at", "?")[:19]
            count = len(data.get("files", {}))
            print(f"{name:<40} {created:<22} {count:>5}")
        except Exception as exc:
            print(f"{path.stem:<40} {'(读取失败)':<22} {'?':>5}  # {exc}")
    return 0


def cmd_delete(vault: Path, name: str) -> int:
    target = checkpoint_dir(vault) / f"{name}.checkpoint"
    if not target.exists():
        print(f"❌ 检查点不存在：{name}", file=sys.stderr)
        return 1
    target.unlink()
    print(f"✅ 已删除：{name}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="novel-suite checkpoint manager")
    parser.add_argument("action", choices=["create", "rollback", "list", "delete"])
    parser.add_argument("--vault", type=Path, required=True, help="vault 目录的绝对路径")
    parser.add_argument("--name", type=str, help="检查点名称（create/rollback/delete 必填）")
    parser.add_argument("--force", action="store_true", help="rollback 时跳过确认")
    args = parser.parse_args()

    vault: Path = args.vault.resolve()

    if args.action in ("create", "rollback", "delete") and not args.name:
        parser.error(f"{args.action} 需要 --name 参数")

    if args.action == "create":
        return cmd_create(vault, args.name)
    if args.action == "rollback":
        return cmd_rollback(vault, args.name, args.force)
    if args.action == "list":
        return cmd_list(vault)
    if args.action == "delete":
        return cmd_delete(vault, args.name)
    return 1


if __name__ == "__main__":
    sys.exit(main())
