# -*- coding: utf-8 -*-
"""
validate_l2.py — L2 轻量校验脚本（v1.0）
供 pop-ai-reduce / pop-ai-reduce-lite 共用。禁止 agent 运行时自写脚本，统一用本脚本。

用法:
  python validate_l2.py <文件路径> <期望字节数> [期望首行前20字] [期望末行后20字]

期望值缺省时不校验对应项（传 '-' 跳过）。

输出:
  每行一个文件校验结果：PASS / FAIL（附实际值），结尾 FAIL 时 exit code 1。
"""
import os
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def check(path, exp_size, exp_first, exp_last):
    name = os.path.basename(path)
    size = os.path.getsize(path) if os.path.exists(path) else -1
    first = last = None
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            lines = f.read().split("\n")
        nz = [l for l in lines if l.strip()]
        first = nz[0][:20] if nz else ""
        last = nz[-1][-20:] if nz else ""
    ok = True
    issues = []
    if exp_size is not None and exp_size != "-":
        if size != int(exp_size):
            ok = False
            issues.append(f"size={size} 期望={exp_size}")
    if exp_first and exp_first != "-":
        if exp_first not in (first or ""):
            ok = False
            issues.append(f"首行不含期望片段")
    if exp_last and exp_last != "-":
        if exp_last not in (last or ""):
            ok = False
            issues.append(f"末行不含期望片段")
    status = "PASS" if ok else "FAIL"
    print(f"{status} {name}: size={size} first='{first}' last='{last}'" + (f" | {'; '.join(issues)}" if issues else ""))
    return ok


if __name__ == "__main__":
    if len(sys.argv) < 2 or (len(sys.argv) - 1) % 4 != 0:
        print("用法: python validate_l2.py <路径> <期望字节数> [首行20字] [末行20字] [更多文件...]",
              file=sys.stderr)
        sys.exit(2)
    args = sys.argv[1:]
    all_ok = True
    for i in range(0, len(args), 4):
        path, exp_size, exp_first, exp_last = args[i], args[i + 1], args[i + 2], args[i + 3]
        if not check(path, exp_size, exp_first, exp_last):
            all_ok = False
    sys.exit(0 if all_ok else 1)
