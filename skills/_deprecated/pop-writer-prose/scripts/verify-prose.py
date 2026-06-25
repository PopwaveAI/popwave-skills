#!/usr/bin/env python3
"""
verify-prose.py — Step 3 style & compliance verification for pop-writer-prose.

Usage:
    python verify-prose.py <chapter_md> [--word-count-min <n>] [--word-count-max <n>]
                           [--events <e1,e2,...>] [--json]

Example:
    python verify-prose.py "正文/ch001-正文.md" \\
        --events "灶台,牧师,希斯,索西亚,想好了,打杀,醒了" \\
        --word-count-min 2800 --word-count-max 3200

Checks performed (aligned with pop-writer-prose Step 3):
  1. Chinese word count vs target range ()
  2. AI observation words (他感到/他意识到/他仿佛/他心想)
  3. Explanatory sentences (不是…而是… patterns)
  4. Event coverage — each keyword found in body text
  5. Text pulse density — per-500-char block
  6. 章末 state_update block presence
"""

import re
import sys
import json
import argparse


def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def count_chinese(text):
    return len(re.findall(r'[\u4e00-\u9fff]', text))


def check_ai_words(text):
    WORDS = ['他感到', '他意识到', '他仿佛', '他心想', '他感觉']
    return [w for w in WORDS if w in text]


def check_explanatory_patterns(text):
    patterns = [
        r'不是[\s\S]{0,30}而是',
        r'并非是[\s\S]{0,30}而是',
        r'并不是[\s\S]{0,30}而是',
    ]
    matches = []
    for p in patterns:
        for m in re.finditer(p, text):
            matches.append(m.group(0)[:80])
    return matches


def check_event_coverage(text, events):
    results = {}
    for e in events:
        e = e.strip()
        results[e] = e in text
    return results


def check_pulse_density(text, markers=None, chunk_size=500):
    if markers is None:
        markers = ['雨', '火', '血', '狗', '哭', '抖', '疼', '冷', '饿', '黑暗', '恐惧', '痛']
    chars = re.findall(r'[\u4e00-\u9fff\u3001\u3002\uff01\uff0c]', text)
    chunks = [''.join(chars[i:i+chunk_size]) for i in range(0, len(chars), chunk_size)]
    results = []
    for i, chunk in enumerate(chunks):
        pulse_count = sum(1 for m in markers if m in chunk)
        results.append({'chunk': i + 1, 'size': len(chunk), 'pulses': pulse_count, 'pass': pulse_count >= 2})
    return results


def check_state_update_block(text):
    return 'state_update' in text


def verify(args):
    text = read_file(args.chapter)
    parts = re.split(r'#+\s*_?state_update', text)
    body = parts[0] if parts else text

    report = {'path': args.chapter, 'checks': {}, 'passed': True, 'warnings': []}
    char_count = count_chinese(body)
    wc_min = args.word_count_min or 0
    wc_max = args.word_count_max or float('inf')

    # 1. Word count
    if char_count < wc_min:
        dev = (wc_min - char_count) / wc_min * 100
        if dev > 50:
            report['checks']['word_count'] = {'status': 'FAIL', 'detail': f'{char_count}z ({dev:.1f}% below min {wc_min})'}
            report['passed'] = False
        elif dev > 20:
            report['checks']['word_count'] = {'status': 'WARN', 'detail': f'{char_count}z ({dev:.1f}% below min {wc_min})'}
            report['warnings'].append(f'word count deviation {dev:.1f}% > 20%')
        else:
            report['checks']['word_count'] = {'status': 'OK', 'detail': f'{char_count}z (deviation {dev:.1f}%)'}
    elif char_count > wc_max:
        dev = (char_count - wc_max) / wc_max * 100
        report['checks']['word_count'] = {'status': 'WARN' if dev <= 50 else 'FAIL',
                                          'detail': f'{char_count}z ({dev:.1f}% above max {wc_max})'}
        if dev > 50:
            report['passed'] = False
    else:
        report['checks']['word_count'] = {'status': 'OK', 'detail': f'{char_count}z (in [{wc_min},{wc_max}])'}

    # 2. AI words
    ai_found = check_ai_words(body)
    if ai_found:
        report['checks']['ai_words'] = {'status': 'FAIL', 'detail': f'found: {ai_found}'}
        report['passed'] = False
    else:
        report['checks']['ai_words'] = {'status': 'OK', 'detail': 'clean'}

    # 3. Explanatory patterns
    expl_found = check_explanatory_patterns(body)
    if len(expl_found) >= 2:
        report['checks']['explanatory'] = {'status': 'FAIL', 'detail': f'{len(expl_found)} occurrences'}
        report['passed'] = False
    elif len(expl_found) == 1:
        report['checks']['explanatory'] = {'status': 'WARN', 'detail': f'1 occurrence: {expl_found[0][:60]}'}
        report['warnings'].append('1 explanatory sentence')
    else:
        report['checks']['explanatory'] = {'status': 'OK', 'detail': 'clean'}

    # 4. Event coverage
    if args.events:
        event_list = [e.strip() for e in args.events.split(',')]
        coverage = check_event_coverage(body, event_list)
        missing = [e for e, found in coverage.items() if not found]
        if missing:
            report['checks']['event_coverage'] = {'status': 'WARN', 'detail': f'missing keywords: {missing}'}
            report['warnings'].append(f'events not found by keyword: {missing}')
        else:
            report['checks']['event_coverage'] = {'status': 'OK', 'detail': f'all {len(event_list)} events matched'}

    # 5. Pulse density
    pulses = check_pulse_density(body)
    failed_chunks = [c for c in pulses if not c['pass']]
    if failed_chunks:
        details = [f"chunk{c['chunk']}({c['size']}c):{c['pulses']}p" for c in failed_chunks]
        status = 'WARN' if len(failed_chunks) <= 1 else 'FAIL'
        report['checks']['pulse_density'] = {'status': status, 'detail': '; '.join(details)}
        if status == 'FAIL':
            report['passed'] = False
        else:
            report['warnings'].append(f'{len(failed_chunks)} low-pulse chunk(s)')
    else:
        report['checks']['pulse_density'] = {'status': 'OK', 'detail': f'all {len(pulses)} chunks pass'}

    # 6. State update block
    has_state = check_state_update_block(text)
    report['checks']['state_update'] = {'status': 'OK' if has_state else 'FAIL', 'detail': ''}
    if not has_state:
        report['passed'] = False

    return report


def main():
    parser = argparse.ArgumentParser(description='Verify prose chapter quality')
    parser.add_argument('chapter', help='Path to chapter .md file')
    parser.add_argument('--events', help='Comma-separated event keywords to check')
    parser.add_argument('--word-count-min', type=int, default=0)
    parser.add_argument('--word-count-max', type=int, default=99999)
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    report = verify(args)

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        status = 'PASS' if report['passed'] else 'FAIL'
        print(f"=== Prose Verify: {status} ===")
        print(f"File: {report['path']}")
        print()
        for name, check in report['checks'].items():
            detail = check.get('detail', '')
            icon = {'OK': 'OK', 'WARN': 'WW', 'FAIL': '!!'}[check['status']]
            print(f"  [{icon}] {name}" + (f" — {detail}" if detail else ""))
        if report['warnings']:
            print(f"\n  Warnings ({len(report['warnings'])}):")
            for w in report['warnings']:
                print(f"    WW {w}")

    sys.exit(0 if report['passed'] else 1)


if __name__ == '__main__':
    main()
