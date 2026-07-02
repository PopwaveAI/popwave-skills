# 管线上下文 — pop-decon-volume

## 拆书管线全景

```
写作链路 (top-down, 雪花法)
────────────────────────────
creative ──→ world ──→ plot ──→ pop-writer-chapter ──→ pop-writer-prose
故事引擎      L1设定     卷/幕      设计包                正文
 "想写什么"                                            "写了什么"

拆书链路 (bottom-up, 倒雪花)
────────────────────────────
正文 ──→ 事实提取 ──→ 聚类卷幕 ──→ 归纳世界观 ──→ 归纳故事引擎
        Phase 1       Phase 2      Phase 3           Phase 4
  "写了什么" 提取什么      什么结构       什么世界观     "所以这书是什么"
```

## 技能依赖关系

| 技能 | 职责 | 上下游 |
|:-----|:-----|:-------|
| `pop-decon-design-pack` | Phase 1：事实提取 → 产出 `_temp/` 三个 JSON | → pop-decon-volume |
| **`pop-decon-volume`** | **Phase 2：聚类卷幕** | ← pop-decon-design-pack → pop-decon-setting |
| `pop-decon-setting` | Phase 3：归纳世界观 → 产出 L1 六件套 + 宪法 | ← pop-decon-volume → pop-decon-prd |
| `pop-decon-prd` | Phase 4：归纳故事引擎（仅 Lv3） | ← pop-decon-setting |
| `pop-decon` | 元 Skill：编排整个管线 | orchestrator |

## 三级分级说明

| 级别 | 范围 | 覆盖 Phase | 产出文件 | 适用场景 |
|:-----|:-----|:---------|:--------|:---------|
| **Lv1** | ch1-20 | Phase 1 | 角色卡 + 龙套池 + ETL 数据 | "快速看榜" |
| **Lv2** | ch1-100 | Phase 1 → 2 → 3 | Lv1 + 卷幕 + L1 六件套 + 宪法 + 数值 | "深度对标" |
| **Lv3** | 全书 | Phase 1 → 2 → 3 → 4 | Lv2 + 故事引擎 + 全书卷幕 + 文风档案 | "完整模板工厂" |

> **Lv1 不做归纳**：前 20 章不产出故事引擎、不产出 L1 设定、不产出卷/幕。只提取事实。
> **Lv2 不归纳故事引擎**：前 100 章不足以回答"这书是什么"。但可以归纳 L1 六件套和卷幕结构。
> **只有 Lv3 产出故事引擎**：全书走完后，从全部数据中归纳。

## Phase 2 在管线中的位置

**Phase 2 是拆书管线的转折点**：
- Phase 1 回答「写了什么」（事实提取 — 原子化）
- Phase 2 回答「什么结构」（聚类 — 结构化）
- Phase 3 回答「什么世界观」（归纳 — 抽象化）
- Phase 4 回答「所以这书是什么」（引擎化 — 仅 Lv3）

没有 Phase 2 的聚类，Phase 3 无从归纳世界观。卷/幕是世界观的上层容器。
