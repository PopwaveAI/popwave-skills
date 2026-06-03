"""
post_write.py — 章节写作后置处理

调用方式：
  python glue/post_write.py <project_dir> <chapter_number>

功能：
  1. 更新 project-status.html（将本章标记为已完成）
  2. 汇总已写章节的字数统计
  3. 提示更新 global-summary.md 和 character-state-anchor.md

变更（2026-05-20）：
  - 路径解析改为 resolve_path()，不再硬编码 02-大纲/ 03-正文/
"""

import os
import sys
import re

# 确保 glue/ 包可导入
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_PARENT = os.path.dirname(_SCRIPT_DIR)
if _PARENT not in sys.path:
    sys.path.insert(0, _PARENT)

from glue.project_config import resolve_path, get_project_config

PROJECT_DIR = sys.argv[1] if len(sys.argv) > 1 else None
CHAPTER_NUM = int(sys.argv[2]) if len(sys.argv) > 2 else None

if not PROJECT_DIR or not CHAPTER_NUM:
    print("用法: python post_write.py <项目目录> <章节号>")
    sys.exit(1)


def resolve_chapter_dir():
    """解析正文目录，优雅降级到 03-正文"""
    try:
        return resolve_path(PROJECT_DIR, "chapters")
    except KeyError:
        return os.path.join(PROJECT_DIR, "03-正文")


def resolve_global_summary():
    """解析全局摘要路径"""
    try:
        return resolve_path(PROJECT_DIR, "global_summary")
    except KeyError:
        return os.path.join(PROJECT_DIR, "02-大纲", "global-summary.md")


def resolve_character_state():
    """解析角色状态路径"""
    try:
        return resolve_path(PROJECT_DIR, "character_state")
    except KeyError:
        return os.path.join(PROJECT_DIR, "02-大纲", "character-state-anchor.md")


def resolve_project_status():
    """解析 project-status.html 路径"""
    # 优先：project.yaml 中配置
    try:
        config = get_project_config(PROJECT_DIR)
        paths = config.get("paths", {})
        if p := paths.get("project_status"):
            candidate = os.path.join(PROJECT_DIR, p)
            if os.path.isfile(candidate):
                return candidate
    except Exception:
        pass
    # 降级：项目根目录
    candidate = os.path.join(PROJECT_DIR, "project-status.html")
    if os.path.isfile(candidate):
        return candidate
    return None


# ─── 更新 project-status.html ─────────────────────────

status_file = resolve_project_status()

if status_file is None:
    print(f"[glue] ⚠️ 找不到 project-status.html，跳过")
else:
    with open(status_file, "r", encoding="utf-8") as f:
        html = f.read()

    ch_dir = resolve_chapter_dir()
    chapter_path_in_status = os.path.join("03-正文", f"ch{CHAPTER_NUM:03d}.md")

    # 检查是否已有该行
    if re.search(re.escape(chapter_path_in_status), html):
        old_line_match = re.search(
            r'<li>.*?' + re.escape(chapter_path_in_status) + r'.*?</li>',
            html, re.DOTALL
        )
        if old_line_match:
            old = old_line_match.group(0)
            if 'badge-todo' in old or '⬜' in old:
                new = old.replace('badge-todo', 'badge-done').replace('⬜', '✅')
                if '（已写）' not in new:
                    new = new.replace('</span>', '</span> <span style="color:#8b8fa3;font-size:0.75rem;">（已写）</span>', 1)
                html = html.replace(old, new)
                print(f"[glue] ✅ project-status.html 更新：ch{CHAPTER_NUM:03d}.md → ✅")
    else:
        insert_point = html.find('<!-- 正文章节 -->')
        if insert_point == -1:
            insert_point = html.find('<li><span class="badge badge-todo">⬜</span> 02-大纲/章纲/')
        if insert_point != -1:
            new_line = f'  <li><span class="badge badge-done">✅</span> 03-正文/ch{CHAPTER_NUM:03d}.md <span style="color:#8b8fa3;font-size:0.75rem;">（新增）</span></li>\n'
            html = html[:insert_point] + new_line + html[insert_point:]
            print(f"[glue] ✅ project-status.html 新增行：ch{CHAPTER_NUM:03d}.md")
        else:
            print(f"[glue] ⚠️ 找不到插入点，请手动更新 project-status.html")

    with open(status_file, "w", encoding="utf-8") as f:
        f.write(html)

# ─── 字数统计 ──────────────────────────────────

ch_dir = resolve_chapter_dir()
chapter_file = os.path.join(ch_dir, f"ch{CHAPTER_NUM:03d}.md")

if os.path.isfile(chapter_file):
    with open(chapter_file, "r", encoding="utf-8") as f:
        content = f.read()
    text = re.sub(r'^# .*?\n', '', content)
    text = re.sub(r'^>.*?\n', '', text, flags=re.MULTILINE)
    text = re.sub(r'^---.*?---', '', text, flags=re.DOTALL)
    char_count = len(text.replace('\n', '').replace(' ', ''))
    print(f"[glue] 📊 ch{CHAPTER_NUM:03d}.md 正文约 {char_count} 字")

    total = 0
    for i in range(1, CHAPTER_NUM + 1):
        fpath = os.path.join(ch_dir, f"ch{i:03d}.md")
        if os.path.isfile(fpath):
            with open(fpath, "r", encoding="utf-8") as f:
                tc = f.read()
            tc_clean = re.sub(r'^# .*?\n', '', tc)
            tc_clean = re.sub(r'^>.*?\n', '', tc_clean, flags=re.MULTILINE)
            tc_clean = re.sub(r'^---.*?---', '', tc_clean, flags=re.DOTALL)
            total += len(tc_clean.replace('\n', '').replace(' ', ''))
    print(f"[glue] 📊 卷一累计：约 {total} 字（ch001-ch{CHAPTER_NUM:03d}）")

# ─── 提醒 ──────────────────────────────────

# 规则中枢扫描
try:
    from glue.rule_hub.hub import scan as rule_hub_scan
    rh_report = rule_hub_scan(PROJECT_DIR)
    if rh_report.warnings:
        for w in rh_report.warnings:
            print(f"[rule-hub] ⚠️ {w}")
    if rh_report.detail:
        d = rh_report.detail[0]
        print(f"[rule-hub] 📊 规则状态: {d['active_rules']} active / {d['unverified']} 未验证 ({d['unverified_p0']} P0)")
except ImportError:
    pass

print()
print("[glue] 📋 写后待办：")
print(f"  1. ✅ 更新 global-summary.md —— ch{CHAPTER_NUM} 摘要追加")
print(f"  2. ✅ 更新 character-state-anchor.md —— 角色状态刷新")
print(f"  3. ✅ project-status.html 已更新")
print(f"  4. ⬜ 自检完成了吗？")
print()

print(f"[glue] ✅ 后置处理完成 — ch{CHAPTER_NUM}")
sys.exit(0)
