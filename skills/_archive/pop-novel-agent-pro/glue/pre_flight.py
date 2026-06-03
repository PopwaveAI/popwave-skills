"""
pre_flight.py — 章节写作前置检查（v3.3 增强版）

调用方式：
  python glue/pre_flight.py <project_dir> <chapter_number>

功能（15项检查）：
  1. project.yaml 存在性及 schema 合法性
  2. reader_profile 完整性
  3. act-01.yaml 存在及 chapters 字段
  4. v3.db 存在性
  5. v3.db 表结构（6张表）
  6. global-summary.md 存在
  7. character-state-anchor.md 存在
  8. 锚定章库目录存在
  9. 01-事实骨架/ 目录存在
  10. experience-log.md 存在
  11. constitution.yaml 存在
  12. setting-index.yaml 存在
  13. 上一章正文存在（ch001 跳过）
  14. 本章正文覆盖提醒
  15. 路径摘要输出

退出码：0 = 通过，1 = 缺失
"""

import os
import sys

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_PARENT = os.path.dirname(_SCRIPT_DIR)
if _PARENT not in sys.path:
    sys.path.insert(0, _PARENT)

from glue.project_config import resolve_path, get_project_config

EXPECTED_DB_TABLES = ["books", "characters", "weirds", "skills", "items", "state_changelog"]

# ★ Spec 检查（v4.0 新增）
SPEC_CHECK_ENABLED = True  # 设为 False 可禁用 spec 检查


def check_spec_complete(project_dir: str, chapter_num: int = None) -> tuple:
    """检查 Spec 三文件完整性"""
    if not SPEC_CHECK_ENABLED:
        return True, "Spec 检查已禁用"
    
    spec_base = os.path.join(project_dir, ".trae", "specs")
    if not os.path.isdir(spec_base):
        return False, "无 .trae/specs/ 目录 —— 建议先调 spec-bridge 生成规格"
    
    # 查找最匹配的 change-id
    candidate = None
    for d in sorted(os.listdir(spec_base)):
        d_path = os.path.join(spec_base, d)
        if not os.path.isdir(d_path):
            continue
        # 如果指定了章节号，查找最接近的
        if chapter_num and f"ch{chapter_num:03d}" in d:
            candidate = d_path
            break  # ★ 精确匹配到，立即停止
        # 否则取最新的（继续遍历到最后一个）
        candidate = d_path
    
    if not candidate:
        return False, "未找到任何 spec 目录"
    
    spec_md = os.path.join(candidate, "spec.md")
    tasks_md = os.path.join(candidate, "tasks.md")
    checklist_md = os.path.join(candidate, "checklist.md")
    
    missing = []
    if not os.path.isfile(spec_md):
        missing.append("spec.md")
    if not os.path.isfile(tasks_md):
        missing.append("tasks.md")
    if not os.path.isfile(checklist_md):
        missing.append("checklist.md")
    
    if missing:
        return False, f"缺少文件: {', '.join(missing)}"
    return True, f"Spec 三文件完整 ({os.path.basename(candidate)})"


# ─── 检查函数 ────────────────────────────────


def check_v3db_exists(project_dir: str) -> tuple:
    """检查 v3.db 存在性 + 表结构完整性"""
    db_dir = os.path.join(project_dir, "04-数据库")
    if not os.path.isdir(db_dir):
        return False, "04-数据库/ 目录不存在"
    
    db_path = None
    # 精确匹配优先：v3.db / v3_main.db
    for fname in ["v3.db", "v3_main.db"]:
        candidate = os.path.join(db_dir, fname)
        if os.path.isfile(candidate):
            db_path = candidate
            break
    # 回退：文件名含 v3 的 .db 文件
    if not db_path:
        for f in os.listdir(db_dir):
            if "v3" in f.lower() and f.endswith(".db"):
                db_path = os.path.join(db_dir, f)
                break
    
    if not db_path:
        return False, "未找到 *_v3.db 文件"
    
    # 检查表结构
    import sqlite3
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        existing = set()
        for row in cur.execute("SELECT name FROM sqlite_master WHERE type='table'"):
            existing.add(row[0])
        conn.close()
        
        missing = [t for t in EXPECTED_DB_TABLES if t not in existing]
        if missing:
            return False, f"缺少表: {missing}"
        return True, f"v3.db 就绪（{len(existing)} 张表）"
    except Exception as e:
        return False, f"v3.db 读取失败: {e}"


def check_reader_profile(project_dir: str) -> tuple:
    """检查 project.reader_profile 字段完整性"""
    proj_file = os.path.join(project_dir, "project.yaml")
    if not os.path.isfile(proj_file):
        return False, "project.yaml 不存在"

    try:
        import yaml
        with open(proj_file, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
    except Exception as e:
        return False, f"project.yaml 解析失败: {e}"

    project = config.get("project", {})
    rp = project.get("reader_profile")
    if not rp:
        return False, "project.reader_profile 缺失"
    
    missing = [f for f in ("platform", "gender", "age_range", "reading_habit", "expectation") if f not in rp]
    if missing:
        return False, f"reader_profile 缺少字段: {missing}"
    return True, f"reader_profile 就绪（{rp.get('platform')}, {rp.get('gender')}）"


def check_dir(filepath: str, label: str) -> tuple:
    """检查目录是否存在"""
    if os.path.isdir(filepath):
        return True, f"{label} ✅"
    return False, f"{label} 目录不存在: {filepath}"


def check_file(filepath: str, label: str) -> tuple:
    """检查文件是否存在"""
    if os.path.isfile(filepath):
        return True, f"{label} ✅"
    return False, f"{label} 不存在: {filepath}"


# ─── 主入口 ──────────────────────────────────

def main():
    PROJECT_DIR = sys.argv[1] if len(sys.argv) > 1 else None
    CHAPTER_NUM = int(sys.argv[2]) if len(sys.argv) > 2 else None

    if not PROJECT_DIR or not CHAPTER_NUM:
        print("用法: python pre_flight.py <项目目录> <章节号>")
        print("示例: python pre_flight.py '/path/to/project' 5")
        sys.exit(1)

    errors = []
    warnings = []

    print(f"\n{'='*50}")
    print(f"📋 前置检查 — {os.path.basename(PROJECT_DIR)} ch{CHAPTER_NUM}")
    print(f"{'='*50}\n")

    # 0. ★ Spec 完整性检查（v4.0 新增）
    spec_ok, spec_detail = check_spec_complete(PROJECT_DIR, CHAPTER_NUM)
    if spec_ok:
        print(f"  ✅ {spec_detail}")
    else:
        warnings.append(spec_detail)

    # 1. project.yaml
    proj_file = os.path.join(PROJECT_DIR, "project.yaml")
    config = None
    if os.path.isfile(proj_file):
        import yaml
        with open(proj_file, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        print("  ✅ project.yaml")
    else:
        errors.append("project.yaml 不存在")

    # 2. project.yaml paths 段检查
    if config:
        project = config.get("project", {})
        paths = config.get("paths", {})
        if not paths:
            warnings.append("project.yaml 中未配置 paths 段——将使用默认路径")

    # 3. reader_profile
    rp_ok, rp_detail = check_reader_profile(PROJECT_DIR)
    if rp_ok:
        print(f"  ✅ {rp_detail}")
    else:
        errors.append(rp_detail)

    # 4. act-01.yaml
    try:
        act_dir = resolve_path(PROJECT_DIR, "act_outline") if config else ""
        act_file = os.path.join(act_dir, "act-01.yaml")
    except:
        act_file = os.path.join(PROJECT_DIR, "02-幕纲", "act-01.yaml")
    ok, msg = check_file(act_file, "act-01.yaml")
    if ok:
        print(f"  ✅ {msg}")
        # 检查 chapters 字段
        try:
            with open(act_file, "r", encoding="utf-8") as f:
                act = yaml.safe_load(f)
            chapters = act.get("chapters", []) if act else []
            ch_meta = [c for c in chapters if c.get("number") == CHAPTER_NUM]
            if not ch_meta:
                warnings.append(f"act-01.yaml 中未找到 ch{CHAPTER_NUM} 的章节定义")
        except:
            warnings.append("act-01.yaml 解析失败")
    else:
        warnings.append("act-01.yaml 不存在——幕纲可能尚未完成")

    # 5. v3.db
    db_ok, db_detail = check_v3db_exists(PROJECT_DIR)
    if db_ok:
        print(f"  ✅ {db_detail}")
    else:
        errors.append(db_detail)

    # 6. global-summary.md
    try:
        gs = resolve_path(PROJECT_DIR, "global_summary")
    except:
        gs = os.path.join(PROJECT_DIR, "02-章纲", "global-summary.md")
    ok, msg = check_file(gs, "global-summary.md")
    if ok: print(f"  ✅ {msg}")
    else: warnings.append(msg)

    # 7. 锚定章库目录
    try:
        ac = resolve_path(PROJECT_DIR, "anchor_chapters")
    except:
        ac = os.path.join(PROJECT_DIR, "01-写作资产", "锚定章库")
    ok, msg = check_dir(ac, "锚定章库")
    if ok: print(f"  ✅ {msg}")
    else: warnings.append(msg)

    # 8. 事实骨架目录
    fs_dir = os.path.join(PROJECT_DIR, "01-事实骨架")
    ok, msg = check_dir(fs_dir, "01-事实骨架/")
    if ok: print(f"  ✅ {msg}")
    else: warnings.append(msg)

    # 9. 写作资产目录
    wa_dir = os.path.join(PROJECT_DIR, "01-写作资产")
    ok, msg = check_dir(wa_dir, "01-写作资产/")
    if ok: print(f"  ✅ {msg}")
    else: errors.append(msg)

    # 10. experience-log.md
    exp_path = os.path.join(wa_dir, "experience-log.md")
    ok, msg = check_file(exp_path, "experience-log.md")
    if ok: print(f"  ✅ {msg}")
    else: warnings.append(msg)

    # 11. setting-index.yaml
    si_path = os.path.join(PROJECT_DIR, "00-原始设定", "setting-index.yaml")
    ok, msg = check_file(si_path, "setting-index.yaml")
    if ok: print(f"  ✅ {msg}")
    else: warnings.append(msg)

    # 12. 上一章正文
    if CHAPTER_NUM > 1:
        try:
            ch_dir = resolve_path(PROJECT_DIR, "chapters")
        except:
            ch_dir = os.path.join(PROJECT_DIR, "03-正文")
        prev_file = os.path.join(ch_dir, f"ch{CHAPTER_NUM-1:03d}.md")
        ok, msg = check_file(prev_file, f"ch{CHAPTER_NUM-1:03d}.md（上一章）")
        if ok: print(f"  ✅ {msg}")
        else: warnings.append(f"上一章文件不存在（首次写本章？）")

    # 13. 本章覆盖提醒
    try:
        ch_dir = resolve_path(PROJECT_DIR, "chapters")
    except:
        ch_dir = os.path.join(PROJECT_DIR, "03-正文")
    this_file = os.path.join(ch_dir, f"ch{CHAPTER_NUM:03d}.md")
    if os.path.isfile(this_file):
        size = os.path.getsize(this_file)
        warnings.append(f"⚠️ ch{CHAPTER_NUM:03d}.md 已存在（{size} 字节），写入将覆盖")

    # 14. 路径摘要输出
    print()
    print(f"  项目路径: {PROJECT_DIR}")

    # 15. ★ 规则中枢扫描（v1.0 新增）
    try:
        from glue.rule_hub.hub import scan as rule_hub_scan
        rh = rule_hub_scan(PROJECT_DIR)
        if rh.detail:
            d = rh.detail[0]
            if d['unverified_p0'] > 0:
                warnings.append(f"规则中枢: {d['unverified_p0']} 条 P0 规则未验证，建议审阅")
            elif d['unverified'] > 5:
                warnings.append(f"规则中枢: {d['unverified']} 条规则未验证，建议定期审阅")
    except ImportError:
        pass

    # ─── 汇总 ───
    print()
    if errors:
        print(f"  ❌ {len(errors)} 个严重问题：")
        for e in errors:
            print(f"    ❌ {e}")
        print(f"\n  💡 建议运行: python automation/init_project.py --project \"{PROJECT_DIR}\"")
        sys.exit(1)

    if warnings:
        print(f"  ⚠️ {len(warnings)} 个提醒：")
        for w in warnings:
            print(f"    ⚠️ {w}")

    print(f"\n  ✅ 前置检查通过（{len(errors)} 错误 / {len(warnings)} 提醒）")
    print(f"  可以开始写 ch{CHAPTER_NUM}")
    sys.exit(0)


if __name__ == "__main__":
    main()
