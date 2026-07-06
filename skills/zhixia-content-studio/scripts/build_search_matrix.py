#!/usr/bin/env python3
"""Generate a reusable Chinese search matrix for Zhixia content research."""

from __future__ import annotations

import argparse
import json


def build(topic: str, platform: str | None, claim: str | None) -> dict[str, list[str]]:
    matrix = {
        "核心概念": [
            f"{topic} 类型 分类",
            f"{topic} 设定 素材",
        ],
        "写作方法": [
            f"{topic} 怎么写 写法",
            f"{topic} 误区 避坑",
            f"{topic} 例子 名场面",
        ],
        "用户痛点": [
            f"{topic} 卡文 不会写",
            f"{topic} 太悬浮 同质化",
        ],
        "平台表达": [
            f"{topic} 小红书 网文作者",
            f"{topic} 知乎 写作",
        ],
        "反面与争议": [
            f"{topic} 反例 为什么不好用",
            f"{topic} 争议 不推荐",
        ],
    }
    if platform:
        matrix["平台表达"].insert(0, f"{topic} {platform}")
    if claim:
        matrix["事实核验"] = [
            f"{claim} 官方 原始来源",
            f"{claim} 报告 数据",
            f"{claim} 反例 争议",
        ]
    return matrix


def main() -> None:
    parser = argparse.ArgumentParser(description="生成知夏内容研究的搜索矩阵")
    parser.add_argument("topic", help="研究主题，例如：校园纯爱CP")
    parser.add_argument("--platform", help="重点平台，例如：小红书")
    parser.add_argument("--claim", help="需要核验的具体说法")
    parser.add_argument("--json", action="store_true", help="输出JSON")
    args = parser.parse_args()

    matrix = build(args.topic.strip(), args.platform, args.claim)
    if args.json:
        print(json.dumps(matrix, ensure_ascii=False, indent=2))
        return

    print(f"# 搜索矩阵：{args.topic.strip()}\n")
    for section, queries in matrix.items():
        print(f"## {section}")
        for query in queries:
            print(f"- {query}")
        print()


if __name__ == "__main__":
    main()
