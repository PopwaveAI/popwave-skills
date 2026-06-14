# Step 2：识别幕边界（卷内）

> **方向**：从卷内 chapter-index 标签的密度变化中识别幕边界。
> **级别覆盖**：Lv2(ch1-100) / Lv3(全书)

---

## 数据来源

`_temp/chapter-index.json` → 卷内章节的 `tags[]` 密度分布

## 幕类型与标签特征

| 幕类型 | 标签特征 |
|:-------|:---------|
| 开局幕 | worldbuilding 标签密集 → 设定介绍 |
| 推进幕 | battle + worldbuilding 交替 → 冒险探索 |
| 高潮幕 | battle 标签连续密集 → 连续战斗 |
| 收尾幕 | economy 标签增多 + 章节字数降低 → 交易/整理/过渡 |

## Canvas 矩阵反推规则

每个幕的 canvas，逐章反推：

```
主线1（世界危机）：worldbuilding 标签密集章 → 标记为世界线推进章
主线2（主角成长）：battle 标签章且字数上升 → 标记为成长线推进章
主线3（主角行动）：首句中的主动动词（"索伦决定/前去/潜入"）
设线负载：连续 non-battle 章中新设定披露次数
```

> **ch 级 Canvas 字段**（act-*.yaml）：每章填写 payoff_summary / 设定线 / 设线负载 / 主线1/2/3推进 / 支线1/2推进 / emotional_goal / end_hook
> 推进内容来自 Phase 1 事实骨架的事件摘要

---

## 产出

| 文件 | 格式 | 内容 |
|:-----|:-----|:-----|
| `设计/幕/vol-01/act-01.yaml` | YAML | 按 `templates/act-skeleton.tpl.yaml` 完整 Canvas 矩阵 |
| `设计/幕/vol-01/act-02.yaml` | YAML | ...（本卷内全部幕） |
| `设计/幕/vol-02/act-*.yaml` | YAML | ...（Lv3 覆盖全部卷） |

---

## 落盘检查

- [ ] 每幕边界有标签密度变化证据
- [ ] Canvas 矩阵无空白列（每章至少一条主线推进。如有空白 → 标注「过渡章无主线推进」）
- [ ] 节奏自检通过（单条线无连续 4 章以上留白）
- [ ] `设计/幕/vol-01/act-*.yaml` 已创建
