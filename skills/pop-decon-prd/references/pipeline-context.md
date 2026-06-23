# pop-decon-prd · 管线上下文

## 在拆书管线中的位置

```
Phase 1          Phase 2           Phase 3           Phase 4          Phase 5
事实提取  ──→  聚类卷幕  ──→  归纳世界观   ──→ 归纳故事引擎 ──→  立项PRD
pop-decon-extract                pop-decon-setting     pop-decon-trace  pop-decon-prd
                                                         ↑                  ↑
                                                    upstream         you are here ← 终点
```

## 消费说明

| 产出 | 谁消费 | 消费目的 |
|:-----|:-------|:---------|
| 全书立项PRD.md | 写作端（pop-novel-bookstrap 等） | 立项参考：赛道/卖点/结构/读者定位 |
| 全书立项PRD.md | pop-trope-library/立项库/ | 归档存储，供后续写书项目检索 |

## 消费的上游产出

| 上游产出 | 来源 Phase | 消费目的 |
|:---------|:-----------|:---------|
| 设计包v3/ | Phase 1 | 章节数/字数/套路统计 |
| L2单元卡 | Phase 2 | 可迁移要点/卖点提炼 |
| L3剧情线 | Phase 3 | 结构/主角驱动提炼 |
| L4全书事件 | Phase 2 | 核心假说/结构提炼 |
| L1六件套+世界宪法+数值体系 | Phase 3 | 赛道判定/结构提炼 |
| 起点/终点快照 | Phase 3 | 主角驱动提炼 |
| 创意溯源 | Phase 4 | 赛道判定/创意版图提炼 |
| 文风DNA | 共享 | 目标读者提炼 |
| 套路库 | pop-trope-library | 可复用资产清单 |

## 级别映射

| 级别 | 覆盖步骤 | 产出范围 |
|:-----|:---------|:---------|
| 前N章 | Step 1-2 | 全书立项PRD.md（标注拆解窗口百分比） |
| 全书 | Step 1-2 | 全书立项PRD.md（完整版） |

## 入库

产出后入 `pop-trope-library/立项库/{书名}-立项PRD.md`
