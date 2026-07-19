#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
字数自检脚本 (wordcount_check.py)
write skill执行完后调用，检查实际字数是否达标，如超标则调用API裁剪

用法:
  python wordcount_check.py <chapter_file.md>
  python wordcount_check.py <chapter_file.md> --auto  # 自动裁剪不询问

流程:
  1. 解析chXXX.md，分离正文和交付面板
  2. 统计实际中文字符数（不含标点/空格/换行/markdown标记）
  3. 对比交付面板自报字数
  4. 如超标(>2500字)，调用API裁剪
  5. 输出裁剪后的正文+更新交付面板字数
"""

import os
import sys
import re
import requests
import argparse

# ============ API配置 ============
DS_API_KEY = "sk-5a3654e4aa2e4eefa08abe3d0e0231f5"
DS_BASE_URL = "https://api.deepseek.com/v1"
DS_MODEL = "deepseek-v4-flash"

TEMPERATURE = 0.3  # 裁剪用低temperature保持稳定
TIMEOUT = 600

# 字数硬限制
TARGET_MIN = 2000
TARGET_MAX = 2500
HARD_LIMIT = 2500  # 超过这个就裁剪


def count_chinese_chars(text):
    """统计实际中文字符数（不含标点/空格/换行/markdown标记）"""
    # 去除markdown标记
    text = re.sub(r'^#+\s.*$', '', text, flags=re.MULTILINE)  # 标题
    text = re.sub(r'^\|.*\|$', '', text, flags=re.MULTILINE)  # 表格
    text = re.sub(r'^---$', '', text, flags=re.MULTILINE)  # 分隔线
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)  # 代码块
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # 粗体
    text = re.sub(r'\*([^*]+)\*', r'\1', text)  # 斜体

    # 统计中文字符 + 字母数字（系统面板里的）
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    # 英文单词也算字数（每个单词算1字）
    english_words = len(re.findall(r'[a-zA-Z]+', text))
    # 数字也算
    numbers = len(re.findall(r'[0-9]+', text))

    return chinese_chars + english_words + numbers


def parse_chapter(content):
    """分离正文和交付面板"""
    # 交付面板通常以"## 交付面板"或"---\n\n## 交付面板"开始
    panel_pattern = re.compile(r'\n---\s*\n\s*##\s*交付面板', re.IGNORECASE)
    match = panel_pattern.search(content)

    if match:
        body = content[:match.start()].strip()
        panel = content[match.start():].strip()
    else:
        # 尝试其他格式
        panel_pattern2 = re.compile(r'\n##\s*交付面板', re.IGNORECASE)
        match2 = panel_pattern2.search(content)
        if match2:
            body = content[:match2.start()].strip()
            panel = content[match2.start():].strip()
        else:
            body = content.strip()
            panel = ""

    return body, panel


def extract_reported_count(panel):
    """从交付面板提取自报字数"""
    if not panel:
        return None
    match = re.search(r'\|\s*字数\s*\|\s*(\d+)\s*字?\s*\|', panel)
    if match:
        return int(match.group(1))
    return None


def call_ds_for_trim(body, actual_count, target_max=HARD_LIMIT):
    """调用API裁剪正文"""
    system_prompt = """你是网文裁剪专家。你的任务是裁剪正文到指定字数，保留核心内容。

裁剪规则：
1. 目标字数：2000-2500字（中文字符数）
2. 裁剪优先级（从先删到后删）：
   - 环境描写（不是物象的环境描写）
   - 人物外貌描写
   - 内心独白
   - 铺垫段
   - 对话（最后删，对话是番茄读者最爱看的）
3. 禁止裁剪：
   - 剧情推进点
   - 爽感爆发段
   - 系统面板（【】格式）
   - 章末钩子
4. 保持段落结构完整，不要出现半句话

直接输出裁剪后的正文，不要输出任何说明。"""

    user_prompt = f"""当前正文字数：{actual_count}字（超标，目标≤2500字）

请裁剪以下正文到2000-2500字：

---

{body}"""

    url = f"{DS_BASE_URL}/chat/completions"
    headers = {"Authorization": f"Bearer {DS_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": DS_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": TEMPERATURE,
        "max_tokens": 6000,
        "stream": False
    }

    response = requests.post(url, headers=headers, json=payload, timeout=TIMEOUT)
    response.raise_for_status()
    result = response.json()
    return result["choices"][0]["message"]["content"]


def update_panel_wordcount(panel, new_count):
    """更新交付面板的字数"""
    if not panel:
        return panel
    return re.sub(
        r'(\|\s*字数\s*\|\s*)\d+(\s*字?\s*\|)',
        rf'\g<1>{new_count}\g<2>',
        panel
    )


def process_chapter(file_path, auto=False):
    """处理单个章节"""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    body, panel = parse_chapter(content)
    actual_count = count_chinese_chars(body)
    reported_count = extract_reported_count(panel)

    print(f"\n{'='*60}")
    print(f"文件: {os.path.basename(file_path)}")
    print(f"{'='*60}")
    print(f"自报字数: {reported_count if reported_count else 'N/A'}")
    print(f"实际字数: {actual_count}")
    print(f"虚报差值: {actual_count - reported_count if reported_count else 'N/A'}")

    if actual_count <= TARGET_MAX:
        print(f"状态: ✅ 达标（{actual_count} ≤ {TARGET_MAX}）")
        return True
    elif actual_count <= 3000:
        print(f"状态: ⚠️ 超标（{actual_count} > {TARGET_MAX}），需要裁剪")
    else:
        print(f"状态: ❌ 严重超标（{actual_count} > 3000），需要重写裁剪")

    if not auto:
        answer = input(f"\n是否调用API裁剪到{TARGET_MIN}-{TARGET_MAX}字？(y/n): ")
        if answer.lower() != 'y':
            print("跳过裁剪")
            return False

    print(f"\n调用API裁剪中...")
    try:
        trimmed_body = call_ds_for_trim(body, actual_count)
        new_count = count_chinese_chars(trimmed_body)

        print(f"裁剪后字数: {new_count}")

        if new_count > TARGET_MAX:
            print(f"⚠️ 一次裁剪未达标，进行第二次裁剪...")
            trimmed_body = call_ds_for_trim(trimmed_body, new_count)
            new_count = count_chinese_chars(trimmed_body)
            print(f"第二次裁剪后字数: {new_count}")

        # 更新交付面板
        if panel:
            new_panel = update_panel_wordcount(panel, new_count)
        else:
            new_panel = ""

        # 写回文件
        new_content = trimmed_body.strip()
        if new_panel:
            new_content += "\n\n---\n\n" + new_panel

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)

        print(f"✅ 裁剪完成！已写回 {file_path}")
        print(f"   原始: {actual_count}字 → 裁剪后: {new_count}字")
        return True

    except Exception as e:
        print(f"❌ 裁剪失败: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="字数自检脚本")
    parser.add_argument("file", help="章节文件路径")
    parser.add_argument("--auto", action="store_true", help="自动裁剪不询问")
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"文件不存在: {args.file}")
        sys.exit(1)

    success = process_chapter(args.file, auto=args.auto)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
