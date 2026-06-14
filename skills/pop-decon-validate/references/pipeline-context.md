# pop-decon-validate · 管线上下文

## 在拆书管线中的位置

```
Phase 1          Phase 2           Phase 3           Phase 4          Phase 5
事实提取  ──→  聚类卷幕  ──→  归纳世界观   ──→ 归纳故事引擎 ──→  验证打包
pop-decon-extract    pop-decon-cluster    pop-decon-world    pop-decon-engine    pop-decon-validate
                                                                       ↑
                                                                 you are here (终 Phase)
```

## 消费说明

| 产出 | 谁消费 | 消费目的 |
|:-----|:-------|:---------|
| Phase5-产出索引.md | 用户 / 写作端 | 告知全部拆解产出位置及消费关系 |
| 矛盾报告（context 中） | 当前对话 | P0 矛盾退回对应 Phase 修正 |

## 级别映射

| 级别 | 覆盖步骤 | 输入来源 |
|:-----|:---------|:---------|
| Lv1 | Step 1-3 | Phase 1 产出（角色卡+龙套池+ETL 数据） |
| Lv2 | Step 1-3 | Phase 1→2→3 产出 |
| Lv3 | Step 1-3 | Phase 1→2→3→4 全部产出 |
