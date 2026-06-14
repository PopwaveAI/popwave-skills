# 管线上下文 — pop-decon-design-pack

## 拆书管线全景

```
拆书链路 (bottom-up, 倒雪花)
────────────────────────────
正文 ──→ 章节清洗 ──→ 章节设计包 ──→ 聚类卷幕 ──→ 归纳世界观 ──→ 归纳故事引擎
        Phase 1       Phase 2         Phase 3      Phase 4          Phase 5
  "写了什么"  清洗+结构化   逆向设计包    什么结构     什么世界观      "所以这书是什么"
```

## 技能依赖关系

| 技能 | 职责 | 上下游 |
|:-----|:-----|:-------|
| `pop-decon-clean` | Phase 1：章节清洗 → 逐章 JSON | → pop-decon-design-pack |
| **`pop-decon-design-pack`** | **Phase 2：从逐章 JSON 逆向产出设计包** | ← pop-decon-clean → pop-decon-volume |
| `pop-decon-volume` | Phase 3：卷幕聚类 | ← pop-decon-design-pack |

## Phase 2 在管线中的位置

**Phase 2 是拆书管线的结构化入口**：
- Phase 1 回答「原文长什么样」（清洗 — 去噪）
- Phase 2 回答「每章有什么事件」（结构化 — 事件链 + 角色）
- Phase 3 回答「什么结构」（聚类 — 卷/幕）

没有 Phase 2 的事件链提取，Phase 3 的卷幕聚类无从建立事件级别的素材库。

## 产出对齐关系

| 拆书端产出（pop-decon-design-pack） | 写作端对应（pop-writer-chapter） | 差异 |
|:-----------------------------------|:--------------------------------|:-----|
| 基础信息（章号/标题/字数/类型） | 完整基础信息 + 幕/爽点/字数 | 拆书端不标注爽点等级 |
| 登场人物表（出场状态/有对话/证据） | 登场人物（含 before/after/角色卡引用） | 拆书端不关联角色卡和 entity-snapshot |
| 事件链（内容/类型/证据） | 事件链（含情绪目标/冲突层次/信息释放/字数） | 拆书端不写情绪/信息/冲突——这些需要设计，不能从原文提取 |
| 事件类型分布 | 无（写作端不标注类型标签） | 拆书端独有字段，便于 Phase 3 聚类 |

## 输入输出摘要

```
输入: _temp/chapter-data/ch001.json ... chNNN.json
      (来自 pop-decon-clean Phase 1)

输出: 写作资产/设计包/ch001-设计包.md ... chNNN-设计包.md
      (供 pop-decon-volume Phase 3 消费)
```
