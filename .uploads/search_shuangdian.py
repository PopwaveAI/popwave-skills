# -*- coding: utf-8 -*-
import re, sys

files_enc = [
    (r'E:\AI小说\参考小说txt\龙符.txt', 'utf-8', '龙符'),
    (r'E:\AI小说\参考小说txt\圣王.txt', 'utf-8', '圣王'),
    (r'E:\AI小说\参考小说txt\海贼法典.txt', 'utf-8', '海贼法典'),
    (r'E:\AI小说\参考小说txt\铸星者（完整版）.txt', 'gbk', '铸星者'),
]

for path, enc, name in files_enc:
    print('===== %s =====' % name)
    with open(path, 'r', encoding=enc) as f:
        lines = f.readlines()
    
    best_patterns = [
        (r'头颅.{0,3}(?:飞起|滚落|落地|斩下)', 'zhan_mo-head'),
        (r'(?:一剑|一刀|一拳|一掌|一爪|一脚|一指).{0,15}(?:贯穿|洞穿|刺穿|穿透|斩断|斩下|劈开|切成|轰碎|炸开|打爆|捏碎)', 'yi_ji_zhan'),
        (r'(?:咔嚓|扑哧).*?(?:头颅|鲜血|倒地|斩杀|杀死)', 'gan_jing_zhan'),
        (r'(?:终于|成功|瞬息|瞬间).{0,10}(?:突破|晋升).{0,10}(?:到|为|至).{0,10}(?:境界|层次)', 'sheng_ji'),
        (r'(?:啪).{0,30}(?:耳光|巴掌)', 'da_lian'),
        (r'(?:一耳光|一巴掌).{0,30}(?:抽|扇|甩|打)', 'da_lian2'),
        (r'(?:随手|反手|一伸手).{0,15}(?:镇压|封印|擒拿|制服|抓住|按住|拿下)', 'zhi_fu'),
    ]
    
    found = []
    for pat, desc in best_patterns:
        count = 0
        for i, line in enumerate(lines):
            m = re.search(pat, line)
            if m:
                stripped = line.strip()
                if len(stripped) < 10:
                    continue
                dialog_chars = sum(1 for c in stripped if c in '\u201c\u201d"')
                if dialog_chars > 4:
                    continue
                start = max(0, i-3)
                end = min(len(lines), i+4)
                context = [(j+1, lines[j].rstrip()) for j in range(start, end)]
                total_chars = sum(len(c[1]) for c in context)
                if total_chars < 500:
                    found.append((i+1, desc, context, total_chars))
                    count += 1
                    if count >= 3:
                        break
    
    print('  Found %d candidates' % len(found))
    for ln, desc, ctx, chars in found:
        print('')
        print('  --- L%d [%s] (%d chars) ---' % (ln, desc, chars))
        for cln, ct in ctx:
            print('    L%d: %s' % (cln, ct[:150]))
    print('')
