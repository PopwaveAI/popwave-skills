# -*- coding: utf-8 -*-
"""
update_project_status.py — novel-agent-pro 项目状态自动感知 + 引导看板生成

用法：
  python scripts/update_project_status.py --project-dir "/path/to/project"

功能：
  1. 自动扫描项目目录，检测文件存在/缺失
  2. 推断当前所处的写作阶段（T1-T8 → 正文写作循环）
  3. 给出"下一步该做什么"的具体指引
  4. 生成 project-status.html（自包含，无需外部依赖）

依赖：
  - Python 3.10+
  - 项目目录遵循 novel-agent-pro v2.0 规范
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path


# ============================================================
# 阶段定义
# ============================================================

PHASES = [
    {
        "id": "T1",
        "name": "开书启动",
        "desc": "从模板创建项目结构，生成 project.yaml，建立目录骨架。",
        "guide": "执行 pop-novel-bootstrap → 或手动创建 project.yaml + 目录骨架",
        "skill": "pop-novel-bootstrap",
        "check_files": ["project.yaml"],
        "outputs": ["project.yaml"],
    },
    {
        "id": "T2",
        "name": "L0灵魂层-核心卖点",
        "desc": "确定一句话卖点、核心爽点链条、对标标杆、目标读者。这一步是全书基因。",
        "guide": "确认 PRD.md 存在且包含 核心卖点/爽点链/对标标准/目标读者。运行 bootstrap Phase 0。",
        "skill": "pop-novel-bootstrap Phase 0",
        "check_files": ["00-原始设定/L0-产品层/PRD.md"],
        "outputs": ["00-原始设定/L0-产品层/PRD.md"],
    },
    {
        "id": "T3",
        "name": "L1元设定-世界观铁律",
        "desc": "五类元设定：世界底座 / 对抗模型 / 成长体系 / 势力底层 / 主角契约。",
        "guide": "手动创建或运行 bootstrap Phase 1 → 执行 01-世界底座.md ~ 05-主角契约.md",
        "skill": "pop-novel-bootstrap Phase 1",
        "check_files": [
            "00-原始设定/L1-元设定层/01-世界底座.md",
            "00-原始设定/L1-元设定层/02-对抗模型.md",
            "00-原始设定/L1-元设定层/03-成长体系.md",
            "00-原始设定/L1-元设定层/04-势力底层.md",
            "00-原始设定/L1-元设定层/05-主角契约.md",
        ],
        "outputs": ["00-原始设定/L1-元设定层/01~05.md"],
    },
    {
        "id": "T4",
        "name": "素材采集 + 参考库",
        "desc": "参考书拆解、场景卡资产、民俗/诡异素材库。可选但强烈推荐。",
        "guide": "运行 skill-book-deconstructor 拆解参考书 → 手动创建场景卡资产（可选）",
        "skill": "skill-book-deconstructor",
        "check_files": [],
        "outputs": ["01-写作资产/场景卡/（可选）"],
    },
    {
        "id": "T5",
        "name": "宪法 + 对标标杆",
        "desc": "constitution.yaml：核心爽点链 + 双线对标标准 + 文风铁则 + 20条世界观铁律。",
        "guide": "确保 constitution.yaml 包含 soul/tonal_benchmarks/tone_law/world_rules 四个节。",
        "skill": "手动编写",
        "check_files": ["00-总控/constitution.yaml"],
        "outputs": ["00-总控/constitution.yaml"],
    },
    {
        "id": "T6",
        "name": "世界稳定性检验",
        "desc": "双宇宙测试：移除主角推演世界 vs 叠加上主角推演。找出设定层逻辑裂缝。",
        "guide": "手动执行稳定性检验 → 产出 stability-check-result.md → 如有 P0 缺陷则退回 T3",
        "skill": "手动（无专用skill）",
        "check_files": [],
        "outputs": ["stability-check-result.md"],
    },
    {
        "id": "T7",
        "name": "宪法完整性验证",
        "desc": "验证 constitution.yaml 的 WR 列表完整、milestones.yaml 幕规划已就绪。",
        "guide": "检查 constitution.yaml 的 world_rules ≥ 5 条 → 检查 milestones.yaml 存在",
        "skill": "手动检查",
        "check_files": ["00-总控/milestones.yaml"],
        "outputs": ["00-总控/milestones.yaml"],
    },
    {
        "id": "T8",
        "name": "🎬 卷纲设计",
        "desc": "剧情架构（战略层）：全书→卷→幕设计。情感曲线锚定+功能标签。",
        "guide": "运行 pop-novel-plot → 产出 02-章纲/volume-1-outline.yaml",
        "skill": "pop-novel-plot",
        "check_files": [],
        "outputs": ["02-章纲/volume-1-outline.yaml"],
    },
]

WRITING_PHASES = [
    {
        "id": "W0",
        "name": "章纲生成",
        "desc": "从幕纲展开章级细节。产出导演层输入格式的章纲（事实链+骨架+Payload）。",
        "guide": "运行 pop-novel-continuation → 产出 02-章纲/chXXX.yaml",
        "skill": "pop-novel-continuation",
        "check_files": [],
        "outputs": ["02-章纲/chXXX.yaml"],
    },
    {
        "id": "W1",
        "name": "正文写作",
        "desc": "emergent-writer v7.7：导演层→碎片写作→桥接→QC双向质检→产出正文。",
        "guide": "对着 chXXX.yaml 运行 emergent-writer → 产出 03-正文/chXXX.md",
        "skill": "pop-novel-writer director→write→qc",
        "check_files": [],
        "outputs": ["03-正文/chXXX.md", "01-写作资产/director/*.md", "05-质检/*.md"],
    },
    {
        "id": "W2",
        "name": "全局摘要更新",
        "desc": "每章 QC 通过后，自动更新 global-summary.md + character-state-anchor.md。",
        "guide": "python scripts/update_global_summary.py --project-dir \"{dir}\" --chapter N --chapter-file \"03-正文/chN.md\"",
        "skill": "update_global_summary.py",
        "check_files": [],
        "outputs": ["02-章纲/global-summary.md", "02-章纲/character-state-anchor.md"],
    },
    {
        "id": "W3",
        "name": "审稿复盘",
        "desc": "读者视角审稿：SOP-R单章审稿 → SOP-S存档 → SOP-C还原度校验 → SOP-P复盘。",
        "guide": "运行 pop-novel-qa SOP-R → 产出 06-复盘/*.md",
        "skill": "pop-novel-qa",
        "check_files": [],
        "outputs": ["06-复盘/*.md"],
    },
]

# 阶段检查项（文件列表）
STAGE_FILE_CHECKS = {
    "设计层": [
        ("00-原始设定/L0-产品层/PRD.md", "L0 产品需求文档"),
        ("00-原始设定/L1-元设定层/01-世界底座.md", "L1 世界底座"),
        ("00-原始设定/L1-元设定层/02-对抗模型.md", "L1 对抗模型"),
        ("00-原始设定/L1-元设定层/03-成长体系.md", "L1 成长体系"),
        ("00-原始设定/L1-元设定层/04-势力底层.md", "L1 势力底层"),
        ("00-原始设定/L1-元设定层/05-主角契约.md", "L1 主角契约"),
    ],
    "运行时层": [
        ("00-总控/constitution.yaml", "宪法（铁律+红线+对标）"),
        ("00-总控/milestones.yaml", "幕规划"),
        ("00-总控/payload_pool.yaml", "Payload池（可选）"),
    ],
    "写作层": [
        ("02-章纲/", "章纲目录（有文件即 ✅）"),
        ("03-正文/", "正文目录（有文件即 ✅）"),
        ("02-章纲/global-summary.md", "全局摘要（运行时生成）"),
        ("02-章纲/character-state-anchor.md", "角色状态锚（运行时生成）"),
    ],
    "资产层": [
        ("01-写作资产/场景卡/", "场景卡资产（可选）"),
        ("01-写作资产/director/", "导演指令卡（写作时生成）"),
    ],
    "元数据": [
        ("project.yaml", "项目元数据"),
        ("_pipeline_state.json", "管线进度（运行时生成）"),
        ("project-status.html", "项目总控台（本文件）"),
    ],
}


def infer_current_phase(project_dir: Path, file_status: dict) -> tuple:
    """推断当前阶段。返回 (phase_id, phase_index)"""
    # 如果 02-章纲目录下已有 *.yaml → 已进入写作循环
    ch_outline_dir = project_dir / "02-章纲"
    if ch_outline_dir.exists():
        yamls = list(ch_outline_dir.glob("*.yaml")) + list(ch_outline_dir.glob("ch*.yaml"))
        if yamls:
            return ("W0", -1)  # 章纲存在 → 章纲阶段

    ch_body_dir = project_dir / "03-正文"
    if ch_body_dir.exists():
        chapters = list(ch_body_dir.glob("ch*.md")) + list(ch_body_dir.glob("chapter-*.md"))
        if chapters:
            return ("W1", -1)

    # 正文 → 按 T1-T8 自上而下找第一个未完成的
    for i, phase in enumerate(PHASES):
        phase_done = all(
            file_status.get(p, False)
            for p in phase["check_files"]
        )
        if not phase_done:
            return (phase["id"], i)
    
    # 全部 T1-T8 完成 → T8
    return ("T8", len(PHASES) - 1)


def build_file_md(project_dir: Path) -> list:
    """构建章节附件 MD 文件扫描"""
    ch_dir = project_dir / "03-正文"
    chapters = []
    if ch_dir.exists():
        files = sorted(
            ch_dir.glob("*.md"),
            key=lambda f: int(re.search(r'(\d+)', f.stem).group(1)) if re.search(r'(\d+)', f.stem) else 0
        )
        for f in files:
            chapters.append({
                "name": f.stem,
                "path": str(f.relative_to(project_dir)).replace("\\", "/"),
                "words": 0,
            })
    return chapters


def build_guide(phase_id: str, project_path: str, phase_count: int, file_status: dict) -> str:
    """构造下一步指引 HTML"""
    if phase_id.startswith("T"):
        # 找当前阶段
        current = None
        for p in PHASES:
            if p["id"] == phase_id:
                current = p
                break
        if not current:
            return ""
        guide = current["guide"].replace("{dir}", project_path)
        return f"""
        <div style="background: rgba(96, 165, 250, 0.1);border:1px solid #60a5fa;border-radius:0.6rem;padding:1rem 1.2rem;">
          <div style="font-size:0.85rem;font-weight:600;color:#60a5fa;margin-bottom:0.4rem;">🔥 下一步操作</div>
          <div style="font-size:0.9rem;line-height:1.6;">
            <strong>{current['id']} · {current['name']}</strong><br>
            <span style="color:var(--text-dim);font-size:0.8rem;">{current['desc']}</span><br><br>
            <code style="background:#2a2d3a;padding:0.2rem 0.5rem;border-radius:0.3rem;font-size:0.8rem;">{guide}</code>
          </div>
          <div style="margin-top:0.6rem;font-size:0.8rem;color:var(--text-dim);">
            预期产出：{' → '.join(current['outputs'])}
          </div>
        </div>"""
    else:
        # 写作阶段
        guides = {
            "W0": f"执行 <code style='background:#2a2d3a;padding:0.1rem 0.4rem;border-radius:0.3rem;font-size:0.8rem;'>pop-novel-continuation</code> → 产出当前幕的章纲",
            "W1": f"执行 <code style='background:#2a2d3a;padding:0.1rem 0.4rem;border-radius:0.3rem;font-size:0.8rem;'>pop-novel-writer</code> → 导演层 → 碎片写作 → QC",
            "W2": f"执行 <code style='background:#2a2d3a;padding:0.1rem 0.4rem;border-radius:0.3rem;font-size:0.8rem;'>python scripts/update_global_summary.py --project-dir &quot;{project_path}&quot; --chapter N --chapter-file &quot;03-正文/chN.md&quot;</code>",
            "W3": f"执行 <code style='background:#2a2d3a;padding:0.1rem 0.4rem;border-radius:0.3rem;font-size:0.8rem;'>pop-novel-qa SOP-R</code> → 审稿 → 存档 → 复盘",
        }
        guide_text = guides.get(phase_id, "")
        phase_names = {"W0": "章纲生成", "W1": "正文写作", "W2": "全局摘要", "W3": "审稿复盘"}
        return f"""
        <div style="background: rgba(96, 165, 250, 0.1);border:1px solid #60a5fa;border-radius:0.6rem;padding:1rem 1.2rem;">
          <div style="font-size:0.85rem;font-weight:600;color:#60a5fa;margin-bottom:0.4rem;">🔥 下一步操作</div>
          <div style="font-size:0.9rem;line-height:1.6;">
            <strong>{phase_id} · {phase_names.get(phase_id, '写作循环')}</strong><br><br>
            {guide_text}
          </div>
        </div>"""


def build_novel_agent_chapters(chapters: list, project_path: str) -> str:
    """生成章节进度 HTML"""
    if not chapters:
        return '<div style="text-align:center;padding:2rem;color:var(--text-dim);font-size:0.9rem;">📄 暂无正文。完成 T1-T8 后开始写作。</div>'
    
    rows = []
    for i, ch in enumerate(chapters):
        status = "✅" if i < len(chapters) - 1 else "⏳"
        rows.append(f"""
        <a href="computer://{project_path}/{ch['path']}" style="text-decoration:none;">
          <div style="display:flex;align-items:center;gap:0.5rem;background:var(--card);border:1px solid var(--border);border-radius:0.4rem;padding:0.5rem 0.8rem;">
            <span>{status}</span>
            <span style="flex:1;font-size:0.85rem;">{ch['name']}</span>
          </div>
        </a>""")
    return '\n'.join(rows)


def build_phase_bar(phase_id: str) -> str:
    """生成 T1-T8 阶段条 HTML"""
    items = []
    for p in PHASES:
        p_id = p["id"]
        if p_id == phase_id:
            cls = "now"
            icon = "⏳"
        elif all(ph["id"] != phase_id for ph in PHASES) and p_id in ["T1","T2","T3","T4","T5","T6","T7","T8"]:
            # All T phases done
            cls = "done"
            icon = "✅"
        else:
            done = False
            for pp in PHASES:
                if pp["id"] == p_id:
                    done = p_id < phase_id
            cls = "done" if done else "wait"
            icon = "✅" if done else "○"
        
        items.append(f'<span class="phase-step {cls}">{icon} {p["name"]}</span>')
    
    return ' <span class="phase-arrow">→</span> '.join(items)


def check_chapter_count(project_dir: Path) -> (int, int):
    """获取章节数和总字数"""
    ch_dir = project_dir / "03-正文"
    if not ch_dir.exists():
        return 0, 0
    mds = list(ch_dir.glob("*.md"))
    total_words = 0
    for f in mds:
        try:
            text = f.read_text(encoding="utf-8")
            # 中文 + 英文单词计数
            words = len(re.findall(r'[\u4e00-\u9fff]', text)) + len(text.split())
            total_words += words
        except:
            pass
    return len(mds), total_words


def build_file_section(project_dir: Path, category: str, checks: list, file_status: dict) -> str:
    """生成文件检查表格 HTML"""
    rows = []
    for rel_path, desc in checks:
        if rel_path.endswith("/"):
            # 目录检查
            dir_path = project_dir / rel_path
            exists = dir_path.exists() and any(dir_path.iterdir())
        else:
            exists = file_status.get(rel_path, False)
        
        status_icon = "✅" if exists else "❌"
        status_text = "就绪" if exists else "缺失"
        status_color = "var(--green)" if exists else "var(--red)"
        
        rows.append(f"""
        <tr>
          <td style="padding:0.35rem;border-bottom:1px solid var(--border);color:var(--text-dim);font-size:0.75rem;">{desc}</td>
          <td style="padding:0.35rem;border-bottom:1px solid var(--border);"><code style="background:#2a2d3a;padding:0.1rem 0.4rem;border-radius:0.2rem;font-size:0.7rem;">{rel_path}</code></td>
          <td style="padding:0.35rem;border-bottom:1px solid var(--border);"><span style="color:{status_color};">{status_icon} {status_text}</span></td>
        </tr>""")
    
    if not rows:
        return ""
    
    return f"""
    <div style="margin-bottom:1rem;">
      <div style="font-size:0.8rem;font-weight:600;margin-bottom:0.3rem;">{category}</div>
      <table style="width:100%;border-collapse:collapse;font-size:0.8rem;">{''.join(rows)}</table>
    </div>"""


def generate_html(project_dir: Path) -> str:
    """生成 project-status.html"""
    project_path = str(project_dir).replace("\\", "/")
    
    # 读取 project.yaml
    project_name = os.path.basename(project_dir)
    genre = "—"
    pj_file = project_dir / "project.yaml"
    if pj_file.exists():
        try:
            text = pj_file.read_text(encoding="utf-8")
            m = re.search(r'name:\s*(.+?)$', text, re.MULTILINE)
            if m: project_name = m.group(1).strip().strip("'\"")
            m = re.search(r'genre:\s*(.+?)$', text, re.MULTILINE)
            if m: genre = m.group(1).strip().strip("'\"")
        except:
            pass

    # 扫描文件状态
    all_checks = {}
    for _, checks in STAGE_FILE_CHECKS.items():
        for rel_path, desc in checks:
            fp = project_dir / rel_path
            exists = fp.exists()
            if rel_path.endswith("/"):
                exists = fp.exists() and any(fp.iterdir())
            all_checks[rel_path] = exists
    
    # 推断阶段
    phase_id, phase_idx = infer_current_phase(project_dir, all_checks)
    
    # 章节统计
    ch_count, word_count = check_chapter_count(project_dir)
    
    # 计算 T1-T8 进度
    t_done = sum(1 for i, p in enumerate(PHASES) if i < phase_idx)
    t_total = len(PHASES)
    t_progress = int(t_done / t_total * 100) if t_total else 0
    
    # 构建 HTML
    gen_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    phase_bar_html = build_phase_bar(phase_id)
    guide_html = build_guide(phase_id, project_path, phase_idx, all_checks)
    chapters_html = build_novel_agent_chapters(build_file_md(project_dir), project_path)
    
    file_secs = ""
    for category, checks in STAGE_FILE_CHECKS.items():
        file_secs += build_file_section(project_dir, category, checks, all_checks)
    
    # 阶段名称
    phase_name = "设计阶段"
    for p in PHASES:
        if p["id"] == phase_id:
            phase_name = f"{p['id']} · {p['name']}"
    if phase_id.startswith("W"):
        wn = {"W0": "章纲", "W1": "正文", "W2": "摘要", "W3": "审稿"}
        phase_name = f"写作循环 · {wn.get(phase_id, phase_id)}"
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{project_name} — 项目总控台</title>
<style>
  :root {{
    --bg: #0f1117; --card: #1a1d27; --border: #2a2d3a;
    --text: #e4e6f0; --text-dim: #8b8fa3;
    --green: #34d399; --yellow: #fbbf24; --red: #f87171; --blue: #60a5fa;
    --accent: #a78bfa;
  }}
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; padding: 1.5rem; }}
  .container {{ max-width: 920px; margin: 0 auto; }}

  .header {{ text-align: center; margin-bottom: 2rem; border-bottom: 1px solid var(--border); padding-bottom: 1.5rem; }}
  .header h1 {{ font-size: 1.6rem; font-weight: 700; color: #fff; }}
  .header .desc {{ color: var(--text-dim); font-size: 0.9rem; margin-top: 0.3rem; }}
  .badge {{ display: inline-block; padding: 0.2rem 0.6rem; border-radius: 999px; font-size: 0.75rem; font-weight: 600; margin: 0.3rem 0.15rem; }}
  .badge-phase {{ background: var(--blue); color: #fff; }}
  .badge-tag {{ background: #2a2d3a; color: var(--text-dim); }}
  .badge-done {{ background: var(--green); color: #1a1d27; }}
  .badge-now {{ background: var(--blue); color: #fff; }}
  .badge-wait {{ background: #2a2d3a; color: var(--text-dim); }}

  .section {{ margin-bottom: 1.5rem; }}
  .section-title {{ font-size: 1.1rem; font-weight: 700; margin-bottom: 0.8rem; padding-bottom: 0.4rem; border-bottom: 1px solid var(--border); display: flex; align-items: center; gap: 0.5rem; }}
  .section-sub {{ font-size: 0.85rem; color: var(--text-dim); margin-bottom: 0.6rem; }}

  .task-list {{ display: flex; flex-direction: column; gap: 0.4rem; }}
  .task-item {{ background: var(--card); border: 1px solid var(--border); border-radius: 0.6rem; padding: 0.8rem 1rem; display: flex; align-items: flex-start; gap: 0.8rem; }}
  .task-icon {{ flex-shrink: 0; width: 1.8rem; height: 1.8rem; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.85rem; font-weight: 700; margin-top: 0.1rem; }}
  .task-icon.done {{ background: var(--green); color: #1a1d27; }}
  .task-icon.current {{ background: var(--blue); color: #fff; }}
  .task-icon.pending {{ background: #2a2d3a; color: var(--text-dim); }}
  .task-body {{ flex: 1; }}
  .task-body h3 {{ font-size: 0.9rem; font-weight: 600; }}
  .task-body .meta {{ font-size: 0.78rem; color: var(--text-dim); margin-top: 0.15rem; }}
  .task-body .files {{ margin-top: 0.4rem; display: flex; flex-wrap: wrap; gap: 0.3rem; }}

  .phase-bar {{ display: flex; align-items: center; justify-content: center; gap: 0.3rem; margin-bottom: 1.5rem; flex-wrap: wrap; }}
  .phase-step {{ display: flex; align-items: center; gap: 0.3rem; padding: 0.3rem 0.5rem; border-radius: 0.4rem; font-size: 0.72rem; white-space: nowrap; }}
  .phase-step.done {{ background: rgba(52,211,153,0.12); color: var(--green); }}
  .phase-step.now {{ background: rgba(96,165,250,0.12); color: var(--blue); border: 1px solid var(--blue); }}
  .phase-step.wait {{ color: var(--text-dim); }}
  .phase-arrow {{ color: var(--border); font-size: 0.7rem; }}

  .info-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 0.6rem; margin-bottom: 1.5rem; }}
  .info-card {{ background: var(--card); border: 1px solid var(--border); border-radius: 0.5rem; padding: 0.8rem 1rem; }}
  .info-card .label {{ font-size: 0.7rem; color: var(--text-dim); }}
  .info-card .value {{ font-size: 1rem; font-weight: 600; margin-top: 0.15rem; }}

  .progress-bar {{ height: 0.35rem; background: #2a2d3a; border-radius: 999px; overflow: hidden; margin: 0.4rem 0; }}
  .progress-fill {{ height: 100%; border-radius: 999px; }}
  .progress-fill.green {{ background: var(--green); }}
  .progress-fill.yellow {{ background: var(--yellow); }}
  .progress-fill.blue {{ background: var(--blue); }}

  .ch-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 0.4rem; }}

  .footer {{ text-align: center; color: var(--text-dim); font-size: 0.75rem; margin-top: 2rem; padding-top: 1rem; border-top: 1px solid var(--border); }}
  @media (max-width: 640px) {{ body {{ padding: 0.8rem; }} }}
</style>
</head>
<body>
<div class="container">

<!-- ===================== HEADER ===================== -->
<div class="header">
  <h1>📖 {project_name}</h1>
  <p class="desc">{genre} · 引擎 novel-agent-pro v2.0 · emergent-writer v7.7</p>
  <div>
    <span class="badge badge-phase">📌 当前阶段：{phase_name}</span>
    <span class="badge badge-tag">生成于 {gen_time}</span>
  </div>
</div>

<!-- ===================== PHASE BAR ===================== -->
<div class="phase-bar">
  {phase_bar_html}
</div>

<!-- ===================== QUICK STATS ===================== -->
<div class="info-grid">
  <div class="info-card">
    <div class="label">T1-T8 进度</div>
    <div class="value" style="color: var(--yellow);">{t_progress}%</div>
    <div class="progress-bar"><div class="progress-fill yellow" style="width:{t_progress}%"></div></div>
    <div style="font-size:0.7rem;color:var(--text-dim);">{t_done}/{t_total} 阶段完成</div>
  </div>
  <div class="info-card">
    <div class="label">正文</div>
    <div class="value" style="font-size:1rem;">{ch_count} 章</div>
    <div style="font-size:0.7rem;color:var(--text-dim);">约 {word_count:,} 字</div>
  </div>
  <div class="info-card">
    <div class="label">运行环境</div>
    <div class="value" style="font-size:0.9rem;">Python 3</div>
    <div style="font-size:0.7rem;color:var(--text-dim);">novel-agent-pro v2.0</div>
  </div>
  <div class="info-card">
    <div class="label">项目路径</div>
    <div class="value" style="font-size:0.7rem;word-break:break-all;">{project_path}</div>
  </div>
</div>

<!-- ===================== NEXT STEP GUIDE ===================== -->
{guide_html}

<br>

<!-- ===================== TASK LIST ===================== -->
<div class="section">
  <div class="section-title">🎯 T1-T8 · 设计阶段</div>
  <div class="section-sub">按顺序推进。未完成的阶段前面是蓝色标记。通过 T8 后进入写作循环。</div>
  <div class="task-list">"""

    for i, p in enumerate(PHASES):
        done = all(all_checks.get(fp, False) for fp in p["check_files"]) if p["check_files"] else i < phase_idx
        if p["id"] == phase_id:
            icon_class = "current"
            icon_char = "⏳"
            border = "var(--blue)"
        elif done or i < phase_idx:
            icon_class = "done"
            icon_char = "✅"
            border = "var(--green)"
        else:
            icon_class = "pending"
            icon_char = "○"
            border = "var(--border)"
        
        file_tags = ""
        for fp in p["check_files"]:
            exists = all_checks.get(fp, False)
            tag_class = "exists" if exists else "missing"
            tag_text = "就绪" if exists else "缺失"
            short = os.path.basename(fp) if "/" in fp else fp
            file_tags += f'<span class="file-tag {tag_class}">{short} {tag_text}</span>'
        
        html += f"""
    <div class="task-item" style="border-color: {border};">
      <div class="task-icon {icon_class}">{icon_char}</div>
      <div class="task-body">
        <h3>{p['id']} · {p['name']}</h3>
        <div class="meta">{p['desc']}</div>
        <div class="files">{file_tags}</div>
      </div>
    </div>"""

    html += """
  </div>
</div>

<!-- ===================== WRITING CYCLE ===================== -->
<div class="section">
  <div class="section-title">✍️ 写作循环</div>
  <div class="section-sub">每章执行一轮：章纲 → 正文 → 全局摘要 → 审稿。</div>
  <div class="ch-grid">"""
  
    html += chapters_html

    html += """
  </div>
</div>

<!-- ===================== FILE STATUS ===================== -->
<div class="section">
  <div class="section-title">📁 文件状态（自动检测）</div>
  <div class="section-sub">✅ 就绪 / ❌ 缺失 / ⚠️ 可选。缺失的文件是下一步需要创建的。</div>"""
  
    html += file_secs

    html += """
</div>

<!-- ===================== USAGE ===================== -->
<div class="section" style="background: var(--card); border: 1px solid var(--border); border-radius: 0.5rem; padding: 0.8rem 1rem;">
  <div style="font-size: 0.8rem; color: var(--text-dim);">
    <strong style="color: var(--text);">🤖 Agent 使用说明</strong><br>
    此文件由 <code style="background:#2a2d3a;padding:0.1rem 0.3rem;border-radius:0.2rem;">scripts/update_project_status.py</code> 自动生成。<br><br>
    <strong>启动对话时的标准操作：</strong><br>
    1. 先读此文件，了解项目当前阶段<br>
    2. 看"🔥 下一步操作"框中的指引<br>
    3. 按指引执行对应的 skill<br>
    4. 完成后运行脚本刷新此文件<br><br>
    <strong>手动刷新：</strong><br>
    <code style="background:#2a2d3a;padding:0.1rem 0.3rem;border-radius:0.2rem;">python scripts/update_project_status.py --project-dir "{project_path}"</code>
  </div>
</div>

<div class="footer">
  此文件自动生成 · novel-agent-pro v2.0 · update_project_status.py · {gen_time}
</div>

</div>
</body>
</html>"""
    return html


def main():
    parser = argparse.ArgumentParser(description="novel-agent-pro 项目状态自动生成器")
    parser.add_argument("--project-dir", required=True, help="项目根目录路径")
    args = parser.parse_args()

    project_dir = Path(args.project_dir).resolve()
    if not project_dir.exists():
        print(f"❌ 项目目录不存在: {project_dir}")
        sys.exit(1)

    print(f"🔍 扫描: {project_dir}")
    html = generate_html(project_dir)
    
    output_path = project_dir / "project-status.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ 生成: {output_path}")

    # 从生成的 HTML 提取阶段摘要
    phase_match = re.search(r'当前阶段：(\S+)', html)
    phase_label = phase_match.group(1) if phase_match else "—"
    ch_count, word_count = check_chapter_count(project_dir)
    print(f"📊 阶段: {phase_label} | 章节: {ch_count} | 字数: {word_count:,}")


if __name__ == "__main__":
    main()
