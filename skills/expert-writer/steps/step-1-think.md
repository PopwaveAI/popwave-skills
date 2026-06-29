# Step 1：强制入口意图识别

> Pop 每次都会强制调起 expert-writer。本步只判断用户想做什么，以及项目现在缺什么。

## 1. 读取项目轻状态

优先检查这些文件是否存在：

- `项目总控.md`
- `写作参考/索引.md`
- `活记忆/活记忆.yaml`
- `卷纲/运行/*-运行日志.md`
- `卷纲/运行/*-设定账本.md`
- `卷纲/幕*.md`
- `正文/*.md`

不要全文加载所有大文件。只在 Execute 阶段按目标读取。

## 2. 意图识别

| 用户说 | 意图 | 路由 |
|:-------|:-----|:-----|
| 开新书、启动项目、重建设定 | 初始化/种子设计 | `pop-writer-v3-seed` |
| 设计剧情、幕纲、剧情单元、运行日志 | 剧情单元运行 | `pop-writer-v3-plot` |
| 写第 X 章、继续、下一章 | 正文创作 | `pop-writer-v3-create`（由本 skill 装配材料） |
| 重写、改文风、加强爽点、压缩、扩写 | 按需修订 | `pop-writer-v3-revise` |
| 复盘、弧线校准、查剧情线、设定账本 | 单元事后校准 | `pop-writer-v3-arc` |
| 拆书、分析原文 | 拆书 | `pop-decon` |
| 调研、查资料 | 调研 | `pop-research` |

## 3. 阶段判断

| 项目状态 | 默认下一步 |
|:---------|:-----------|
| 没有 `写作参考/设定/故事DNA.md` | seed |
| 没有 `卷纲/运行/*-运行日志.md` | plot |
| 有运行日志但目标章节正文不存在 | create |
| 用户要求修改已有正文 | revise |
| 当前单元最后一章已写完 | arc |

## 4. 产出

输出一个简短路由决定：

```yaml
route_decision:
  intent: create|seed|plot|revise|arc|research|decon
  target_skill: pop-writer-v3-create
  reason: ""
  required_materials:
    - ""
  missing_materials:
    - ""
```

缺少 create 必需材料时，不要硬写正文，转去 plot/arc 补材料。
