"""quality_score 计算（v3.3 显式公式）。"""

from __future__ import annotations

# 句末标点
SENTENCE_END = "。！？.!?"
# 不应作为开头的标点
BAD_START = "，。！？、；：\")】」』]"
# 句末标点（含中英文引号收尾）
GOOD_END = "。！？\")】」』.!?"


def calc_quality_score(content: str) -> float:
    """
    返回 0-1 分数，用于检索排序。

    四个维度（加权和）：
    1. 字数适中（800-1500 最优）   权重 0.3
    2. 段落完整（首尾完整句）       权重 0.2
    3. 叙事多样性（对话占比适度）   权重 0.3
    4. 信息密度（句号密度）         权重 0.2
    """
    wc = len(content)
    if wc == 0:
        return 0.0

    # 1. 字数得分
    if 800 <= wc <= 1500:
        wc_score = 1.0
    elif 500 <= wc < 800:
        wc_score = 0.5 + (wc - 500) / 600  # 0.5 ~ 1.0
    elif 1500 < wc <= 2000:
        wc_score = 1.0 - (wc - 1500) / 1000  # 1.0 ~ 0.5
    else:
        wc_score = 0.3

    # 2. 完整性
    starts_well = content[0] not in BAD_START
    ends_well = content[-1] in GOOD_END
    completeness = (int(starts_well) + int(ends_well)) / 2

    # 3. 多样性（对话占比作为代理）
    # 「」 是中文对话引号，"" 是英文（部分网文也用）
    dialog_count = content.count("「") + content.count("\u201c")
    dialog_density = dialog_count / max(wc, 1) * 50
    diversity = min(dialog_density, 1.0)
    # 完全无对话时也不该 0 分（叙事/动作场景同样重要）
    diversity = max(diversity, 0.3)

    # 4. 信息密度（句号密度作为节奏代理）
    sentence_count = sum(content.count(p) for p in "。！？")
    expected = max(wc / 50, 1)
    density = min(sentence_count / expected, 1.0)

    score = (
        0.3 * wc_score
        + 0.2 * completeness
        + 0.3 * diversity
        + 0.2 * density
    )
    return round(score, 3)
