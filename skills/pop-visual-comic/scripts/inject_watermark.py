#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
品牌水印强制注入脚本（幂等 + 校验）。

背景：2026-08-06 实测 agent 生成长条 HTML 时手写简化版模板（comic-header/comic-footer）
绕过 page-layout-guide.md 模板，导致 popwave 品牌水印 slogan/footer 全部丢失。
本脚本作为工程兜底：无论 HTML 如何生成，强制注入品牌水印三要素并校验存在。

用途（Step 2 生成 HTML 后强制调用）：
    python inject_watermark.py <index.html 路径>

品牌水印三要素（见 page-layout-guide.md §品牌水印）：
    1. 标题区品牌行 slogan：popwave.cn 让创意一键落地
    2. 页脚 footer：未完待续 · popwave.cn 让创意一键落地
    3. 对应 CSS 类（.brand-line / .footer-banner）

脚本幂等：重复运行不重复注入；已含水印则跳过、仅校验。
"""
import io
import re
import sys

SLOGAN = 'popwave.cn 让创意一键落地'
FOOTER = '未完待续 · popwave.cn 让创意一键落地'

# 注入锚点：优先标准模板类名，回退到通用标题/页脚容器
CSS_ANCHOR = '.comic-footer'
CSS_ADD = (
    '.brand-line { margin-top:10px; font-size:12px; color:#8a8274; letter-spacing:3px; }\n'
    '  .footer-banner { text-align:center; padding:36px 24px; font-size:13px; color:#6f6a60; letter-spacing:3px; }\n'
)


def _inject_slogan(html):
    """标题区第三行注入 slogan。定位最后一个 </div> 前的标题容器，尽量贴近 h1/子标题。"""
    if SLOGAN in html:
        return html, True
    # 优先在 .comic-header 或 .title-banner 容器末尾注入
    m = re.search(r'(<div class="(?:comic-header|title-banner)">.*?</div>\s*)(?=<div class="(?:page|container)")', html, re.S)
    if m:
        block = m.group(1)
        anchor = '</div>'
        # 在标题容器最后一个 </div> 前插入 slogan 行
        insert_at = block.rfind(anchor)
        new_block = block[:insert_at] + '\n  <div class="brand-line">' + SLOGAN + '</div>' + block[insert_at:]
        html = html.replace(block, new_block, 1)
        return html, True
    # 兜底：在 <body> 后第一个块前注入一个独立品牌行
    m2 = re.search(r'(<body>\s*)', html)
    if m2:
        html = html.replace(m2.group(1), m2.group(1) +
                            '  <div style="text-align:center;padding:24px;font-size:12px;color:#8a8274;letter-spacing:3px;">' +
                            SLOGAN + '</div>\n', 1)
        return html, True
    return html, False


def _inject_footer(html):
    """页脚注入 footer 品牌行。定位 </body> 前。"""
    if FOOTER in html:
        return html, True
    m = re.search(r'((?:</div>\s*)*)</body>', html)
    if m:
        html = html.replace('</body>', '  <div class="footer-banner">' + FOOTER + '</div>\n</body>', 1)
        return html, True
    return html, False


def _inject_css(html):
    """注入品牌行样式。"""
    if 'brand-line' in html and 'footer-banner' in html and '.brand-line' in html:
        return html  # 样式已存在
    if CSS_ANCHOR in html:
        return html.replace(CSS_ANCHOR, CSS_ANCHOR + '\n  ' + CSS_ADD, 1)
    # 兜底：在 </style> 前注入
    m = re.search(r'</style>', html)
    if m:
        return html.replace('</style>', CSS_ADD + '</style>', 1)
    return html


def inject(html):
    html = _inject_css(html)
    html, ok1 = _inject_slogan(html)
    html, ok2 = _inject_footer(html)
    return html, ok1 and ok2


def verify(html):
    """校验品牌水印三要素是否齐全。"""
    checks = {
        'slogan 标题区品牌行': SLOGAN in html,
        'footer 页脚品牌行': FOOTER in html,
        'brand-line 样式/类': '.brand-line' in html or 'brand-line' in html,
        'footer-banner 样式/类': '.footer-banner' in html or 'footer-banner' in html,
    }
    return checks, all(checks.values())


def main():
    if len(sys.argv) < 2:
        print('用法: python inject_watermark.py <index.html 路径>')
        sys.exit(2)
    path = sys.argv[1]
    with io.open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    html, injected = inject(html)
    if injected:
        with io.open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print('OK: 品牌水印已注入 ->', path)
    else:
        print('WARN: 未能自动注入，请人工检查 HTML 结构')

    checks, ok = verify(html)
    for name, present in checks.items():
        print(('  [%s] %s' % ('PASS' if present else 'FAIL', name)))
    if not ok:
        print('ERROR: 品牌水印校验未通过，禁止发布无品牌水印的漫画')
        sys.exit(1)
    print('验证通过: 品牌水印三要素齐全')


if __name__ == '__main__':
    main()