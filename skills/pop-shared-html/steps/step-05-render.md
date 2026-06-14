# Step 5：注入内容 + 渲染

**读什么：** 以上所有步骤的产出 + 原始素材内容。

**数据映射规则：**
| 内容元素 | 映射目标 | 组件 |
|:---------|:---------|:-----|
| 标题/名称 | 页面标题/Hero H1 | — |
| 描述/摘要 | Hero 副标题/About 段落 | — |
| 数字指标 | Stats/Metric 卡片 | `.metric` |
| 条目列表 | 数据表格/卡片网格 | `table` / `.card` |
| 状态字段 | Tag 标签 | `.tag` |
| 多 Tab 内容 | Tab 切换 | `.tabs` |
| `volume_stats`（YAML） | 顶部指标卡片+概览区 | `.metric` + Stats |
| `chapters[].tone`（YAML） | 时间线颜色编码 | 按情绪定色 |
| `entity_cooccurrence`（YAML） | 关系网络图 | Canvas 力导向图 |

**产出：** 完整 HTML 文件。
