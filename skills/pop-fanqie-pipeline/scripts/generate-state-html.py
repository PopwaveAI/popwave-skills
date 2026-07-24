#!/usr/bin/env python3
"""
generate-state-html.py
从project-state.md解析字段，替换HTML模板占位符，生成project-state.html

用法：python generate-state-html.py <project-state.md路径>
输出：同目录下生成project-state.html
"""

import sys
import os
import re
from datetime import datetime

def parse_state_md(md_path):
    """解析project-state.md，提取字段"""
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    state = {}

    # 项目名
    m = re.search(r'# 项目：(.+)', content)
    state['project_name'] = m.group(1).strip() if m else '未命名项目'

    # 创建/更新时间
    m = re.search(r'创建：(\S+ \S+)', content)
    state['created_at'] = m.group(1).strip() if m else ''
    m = re.search(r'更新：(\S+ \S+)', content)
    state['updated_at'] = m.group(1).strip() if m else ''

    # phase
    m = re.search(r'phase:\s*(\S+)', content)
    state['phase'] = m.group(1).strip() if m else 'init'

    # mode
    m = re.search(r'mode:\s*(\S+)', content)
    state['mode'] = m.group(1).strip() if m else 'fresh'

    # current_chapter
    m = re.search(r'current_chapter:\s*(\S+)', content)
    state['current_chapter'] = m.group(1).strip() if m else 'ch000'

    # 阶段完成情况
    phases = []
    phase_labels = {
        'Phase 0': '用户意图',
        'Phase 1': 'Seed',
        'Phase 2': 'World',
        'Phase 3': 'Plot',
        'Phase 3.5': 'Character',
        'Phase 4': 'Write',
        'Phase 5': 'Review',
    }
    phase_keys = ['Phase 0', 'Phase 1', 'Phase 2', 'Phase 3', 'Phase 3.5', 'Phase 4', 'Phase 5']
    for pk in phase_keys:
        pattern = r'- \[([ x])\] ' + re.escape(pk) + r':'
        m = re.search(pattern, content)
        done = bool(m and m.group(1) == 'x')
        phases.append({'key': pk, 'label': phase_labels[pk], 'done': done})

    # 底牌就绪
    decks = []
    deck_patterns = [
        ('用户意图', r'用户意图：.*?(✅|❌)'),
        ('赛道调研', r'赛道调研：.*?(✅|❌)'),
        ('参考书下载', r'参考书下载：.*?(done|skipped|✅|❌)'),
        ('笔触DNA', r'笔触DNA：.*?(✅|❌)'),
        ('decon-lite', r'decon-lite：.*?(✅|❌)'),
    ]
    for name, pattern in deck_patterns:
        m = re.search(pattern, content)
        if m:
            status = m.group(1)
            if status in ('✅', 'done'):
                status_class = 'ready'
                status_text = '✓ 就绪'
            elif status == 'skipped':
                status_class = 'skipped'
                status_text = '跳过'
            else:
                status_class = 'not-ready'
                status_text = '✗ 未就绪'
        else:
            status_class = 'not-ready'
            status_text = '✗ 未就绪'
        decks.append({'name': name, 'status_class': status_class, 'status_text': status_text})

    # 创意摘要
    m = re.search(r'书名\(暂\)：(.+)', content)
    state['book_name'] = m.group(1).strip() if m else '待seed产出'
    m = re.search(r'一句话：(.+)', content)
    state['one_line'] = m.group(1).strip() if m else '待seed产出'

    # 最近产出
    outputs = []
    output_section = re.search(r'## 最近产出\s*\n\|.*?\n\|.*?\n(.*?)(?:\n\n|\Z)', content, re.DOTALL)
    if output_section:
        for line in output_section.group(1).strip().split('\n'):
            line = line.strip()
            if line and line.startswith('|'):
                cols = [c.strip() for c in line.split('|')[1:-1]]
                if len(cols) >= 3:
                    outputs.append({'phase': cols[0], 'file': cols[1], 'time': cols[2]})

    # 下一步操作
    next_step_map = {
        'init': 'Phase 0: 用户意图深问',
        'phase0': 'Phase 1: Seed创意+首章',
        'phase1': 'Phase 2: World世界构筑',
        'phase2': 'Phase 3: Plot剧情白描',
        'phase3': 'Phase 3.5: Character角色库建设',
        'phase3.5': 'Phase 4: Write正文渲染 (ch002)',
        'phase4': f'Phase 5: Review审核 ({state["current_chapter"]})',
        'phase5': f'Phase 4: Write下一章 / 重写本章',
    }
    state['next_step'] = next_step_map.get(state['phase'], '未知')

    return state, phases, decks, outputs

def build_phase_checklist_html(phases, current_phase):
    """构建Phase进度条HTML"""
    phase_order = ['phase0', 'phase1', 'phase2', 'phase3', 'phase3.5', 'phase4', 'phase5']
    current_idx = phase_order.index(current_phase) if current_phase in phase_order else -1

    html = ''
    for i, p in enumerate(phases):
        phase_key = phase_order[i] if i < len(phase_order) else ''
        if p['done']:
            circle_class = 'done'
            icon = '&#10003;'
        elif phase_key == current_phase:
            circle_class = 'current'
            icon = '&#8635;'
        else:
            circle_class = 'pending'
            icon = '&#9675;'

        label_class = 'active' if phase_key == current_phase else ''
        html += f'''        <div class="phase-item">
          <div class="phase-circle {circle_class}">{icon}</div>
          <div class="phase-label {label_class}">{p['key']}<br>{p['label']}</div>
        </div>
'''
        if i < len(phases) - 1:
            line_class = 'done' if p['done'] else ''
            html += f'        <div class="phase-line {line_class}"></div>\n'

    return html

def build_deck_cards_html(decks):
    """构建底牌就绪卡片HTML"""
    icons = {'用户意图': '&#128203;', '赛道调研': '&#128269;', '参考书下载': '&#128218;', '笔触DNA': '&#9999;&#65039;', 'decon-lite': '&#128295;'}
    html = ''
    for d in decks:
        icon = icons.get(d['name'], '&#9678;')
        html += f'''      <div class="deck-item">
        <div class="name">{icon} {d['name']}</div>
        <span class="deck-status {d['status_class']}">{d['status_text']}</span>
      </div>
'''
    return html

def build_creative_summary_html(state):
    """构建创意摘要卡片HTML"""
    return f'''      <div class="summary-item">
        <div class="label">书名</div>
        <div class="value">{state['book_name']}</div>
      </div>
      <div class="summary-item">
        <div class="label">一句话</div>
        <div class="value">{state['one_line']}</div>
      </div>'''

def build_recent_outputs_html(outputs):
    """构建最近产出表格HTML"""
    if not outputs:
        return '      <tr><td colspan="3">暂无产出</td></tr>'
    html = ''
    for o in outputs:
        html += f'        <tr><td>{o["phase"]}</td><td class="file-path">{o["file"]}</td><td>{o["time"]}</td></tr>\n'
    return html

def main():
    if len(sys.argv) < 2:
        print("用法: python generate-state-html.py <project-state.md路径>")
        sys.exit(1)

    md_path = sys.argv[1]
    if not os.path.exists(md_path):
        print(f"错误: 文件不存在: {md_path}")
        sys.exit(1)

    # 解析state.md
    state, phases, decks, outputs = parse_state_md(md_path)

    # 读取模板
    script_dir = os.path.dirname(os.path.abspath(__file__))
    tpl_path = os.path.join(script_dir, '..', 'templates', 'project-state.html.tpl')
    with open(tpl_path, 'r', encoding='utf-8') as f:
        template = f.read()

    # 替换占位符
    replacements = {
        '{{PROJECT_NAME}}': state['project_name'],
        '{{CREATED_AT}}': state['created_at'],
        '{{UPDATED_AT}}': state['updated_at'],
        '{{PHASE}}': state['phase'],
        '{{MODE}}': state['mode'],
        '{{CURRENT_CHAPTER}}': state['current_chapter'],
        '{{PHASE_CHECKLIST}}': build_phase_checklist_html(phases, state['phase']),
        '{{DECK_CARDS}}': build_deck_cards_html(decks),
        '{{CREATIVE_SUMMARY}}': build_creative_summary_html(state),
        '{{RECENT_OUTPUTS}}': build_recent_outputs_html(outputs),
        '{{NEXT_STEP}}': state['next_step'],
    }

    html = template
    for placeholder, value in replacements.items():
        html = html.replace(placeholder, value)

    # 落盘
    html_path = os.path.join(os.path.dirname(md_path), 'project-state.html')
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✅ 已生成: {html_path}")

if __name__ == '__main__':
    main()
