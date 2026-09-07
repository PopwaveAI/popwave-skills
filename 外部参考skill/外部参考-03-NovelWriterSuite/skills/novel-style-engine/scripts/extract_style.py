#!/usr/bin/env python3
"""
novel-style-engine 客观统计特征提取器。

输入：style/samples/ 目录下的样本 .md 文件
输出：JSON 到 stdout（或 --out 指定的文件）

主观特征不在这里抽取——那是 LLM（skill 主体）的工作。
本脚本只做"机器可计算"的客观统计。

用法：
    python3 extract_style.py --samples style/samples/
    python3 extract_style.py --samples style/samples/ --out style/features.objective.json
"""

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from statistics import mean, stdev


def strip_frontmatter(text: str) -> str:
    """去掉 markdown 顶部的 YAML frontmatter。"""
    if not text.startswith("---"):
        return text
    parts = text.split("\n---\n", 1)
    if len(parts) < 2:
        return text
    rest = parts[1]
    # 也可能是 ---\n...---\n 紧凑写法
    return rest.lstrip("\n")


def chinese_char_count(text: str) -> int:
    """统计汉字数（不含标点、空格）。"""
    return len(re.findall(r"[一-鿿]", text))


def split_sentences(text: str) -> list[str]:
    """中文句子分割。按句号、感叹号、问号、省略号切。"""
    # 把所有中文句末标点统一作为分隔符
    parts = re.split(r"([。！？…]+|\.\.\.|\.{3,})", text)
    sentences: list[str] = []
    buffer = ""
    for p in parts:
        if re.match(r"[。！？…]+|\.\.\.|\.{3,}", p):
            buffer += p
            if buffer.strip():
                sentences.append(buffer.strip())
            buffer = ""
        else:
            buffer += p
    if buffer.strip():
        sentences.append(buffer.strip())
    return [s for s in sentences if chinese_char_count(s) > 0]


def split_paragraphs(text: str) -> list[str]:
    """段落 = 双换行隔开的块。"""
    paragraphs = re.split(r"\n\s*\n", text)
    return [p.strip() for p in paragraphs if p.strip()]


def punctuation_density(text: str) -> dict[str, float]:
    """常见标点的密度（每千字次数）。"""
    total_chars = chinese_char_count(text)
    if total_chars == 0:
        return {}
    counters = {
        "period": len(re.findall(r"[。．]", text)),
        "comma": len(re.findall(r"[，,]", text)),
        "semicolon": len(re.findall(r"[；;]", text)),
        "em_dash": len(re.findall(r"——", text)),
        "ellipsis": len(re.findall(r"…|\.\.\.|\.{3,}", text)),
        "quote": len(re.findall(r"[“”「」『』\"]", text)),
        "exclaim": len(re.findall(r"[！!]", text)),
        "question": len(re.findall(r"[？?]", text)),
    }
    return {k: round(v / total_chars * 1000, 2) for k, v in counters.items()}


def dialogue_ratio(text: str) -> float:
    """对话占比（引号内字数 / 总字数）。"""
    total = chinese_char_count(text)
    if total == 0:
        return 0.0
    # 匹配 "..." 或 「...」 或 直角引号 或 智能引号
    dialogue_chars = 0
    for pattern in [r"“[^”]+”", r"「[^」]+」", r'"[^"]+"']:
        for match in re.findall(pattern, text):
            dialogue_chars += chinese_char_count(match)
    return round(dialogue_chars / total, 3)


def word_frequency(text: str, top_n: int = 30) -> list[tuple[str, int]]:
    """简易词频统计：取 2-gram 出现频率最高的（不分词，用滑动窗口）。

    优点：不依赖外部分词库；中文 2-gram 已能捕捉大量常用词汇/搭配
    缺点：会把"的他""了一"这种连接捕进来——但 top 30 里能看到风格倾向
    """
    chinese = re.findall(r"[一-鿿]+", text)
    grams: list[str] = []
    for run in chinese:
        if len(run) >= 2:
            for i in range(len(run) - 1):
                grams.append(run[i : i + 2])
    counter = Counter(grams)
    return counter.most_common(top_n)


def analyze_sample(text: str) -> dict:
    """对单个样本做统计。"""
    text_body = strip_frontmatter(text)
    sentences = split_sentences(text_body)
    paragraphs = split_paragraphs(text_body)

    sentence_lengths = [chinese_char_count(s) for s in sentences]
    paragraph_sentence_counts = [len(split_sentences(p)) for p in paragraphs]

    result = {
        "total_chinese_chars": chinese_char_count(text_body),
        "sentence_count": len(sentences),
        "paragraph_count": len(paragraphs),
        "avg_sentence_length": round(mean(sentence_lengths), 1) if sentence_lengths else 0.0,
        "sentence_length_std": round(stdev(sentence_lengths), 1) if len(sentence_lengths) >= 2 else 0.0,
        "avg_paragraph_sentences": round(mean(paragraph_sentence_counts), 1) if paragraph_sentence_counts else 0.0,
        "paragraph_sentence_std": round(stdev(paragraph_sentence_counts), 1) if len(paragraph_sentence_counts) >= 2 else 0.0,
        "punctuation_density_per_1000": punctuation_density(text_body),
        "dialogue_ratio": dialogue_ratio(text_body),
        "top_bigrams": word_frequency(text_body, top_n=30),
    }
    return result


def aggregate(samples: list[dict]) -> dict:
    """聚合多个样本的统计（加权平均）。"""
    if not samples:
        return {}
    total_chars = sum(s["total_chinese_chars"] for s in samples)
    if total_chars == 0:
        return {}

    # 加权（按字数）合并
    def weighted_mean(field: str) -> float:
        return round(sum(s[field] * s["total_chinese_chars"] for s in samples) / total_chars, 1)

    agg = {
        "sample_count": len(samples),
        "total_chinese_chars": total_chars,
        "avg_sentence_length": weighted_mean("avg_sentence_length"),
        "sentence_length_std": weighted_mean("sentence_length_std"),
        "avg_paragraph_sentences": weighted_mean("avg_paragraph_sentences"),
        "paragraph_sentence_std": weighted_mean("paragraph_sentence_std"),
        "dialogue_ratio": round(sum(s["dialogue_ratio"] * s["total_chinese_chars"] for s in samples) / total_chars, 3),
    }

    # 标点密度聚合
    punct_keys = samples[0]["punctuation_density_per_1000"].keys() if samples[0]["punctuation_density_per_1000"] else []
    agg["punctuation_density_per_1000"] = {
        k: round(
            sum(s["punctuation_density_per_1000"].get(k, 0) * s["total_chinese_chars"] for s in samples) / total_chars,
            2,
        )
        for k in punct_keys
    }

    # bigram 聚合：合并所有 sample 的 bigram counter，取 top 30
    all_bigrams: Counter = Counter()
    for s in samples:
        for bg, c in s["top_bigrams"]:
            all_bigrams[bg] += c
    agg["top_bigrams_combined"] = all_bigrams.most_common(30)

    return agg


def main() -> int:
    parser = argparse.ArgumentParser(description="novel-style-engine 客观特征统计")
    parser.add_argument("--samples", type=Path, required=True, help="样本目录路径")
    parser.add_argument("--out", type=Path, help="输出 JSON 文件路径，省略则打印到 stdout")
    args = parser.parse_args()

    samples_dir: Path = args.samples.resolve()
    if not samples_dir.is_dir():
        print(f"❌ 样本目录不存在：{samples_dir}", file=sys.stderr)
        return 1

    md_files = sorted(samples_dir.glob("*.md"))
    if not md_files:
        print(f"⚠️  样本目录为空：{samples_dir}", file=sys.stderr)
        return 1

    per_sample: list[dict] = []
    for path in md_files:
        text = path.read_text(encoding="utf-8")
        stats = analyze_sample(text)
        stats["file"] = path.name
        per_sample.append(stats)

    aggregated = aggregate(per_sample)

    result = {
        "samples": per_sample,
        "aggregated": aggregated,
    }

    output_text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(output_text, encoding="utf-8")
        print(f"✅ 客观统计输出到：{args.out}")
        print(f"   样本数：{len(per_sample)}, 总字数：{aggregated.get('total_chinese_chars', 0)}")
    else:
        print(output_text)

    return 0


if __name__ == "__main__":
    sys.exit(main())
