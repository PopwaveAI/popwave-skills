# typical-paths.md — 典型路径速查

> 加载时机：Think 初次路由时，对照确认当前环节上下游。
> 加载方式：`Get-Content -Encoding UTF8 -Raw`，不用 Read 工具。

---

## v3.5 管线全路径

```
种子设计(pop-writer-v3-seed) → 幕纲设计(pop-writer-v3-plot) → 涌现写作环(expert-writer 5步循环) ↔ 弧线校准(pop-writer-v3-arc)
                                                                ↑ 按需：pop-research
```

> emerge 已废弃：5步循环由 expert-writer 主会话直接执行。

---

## 典型路径

### 路径1：新书启动

```
用户："开新书"
→ step-0-init.md（项目初始化）
→ pop-writer-v3-seed（种子设计）
  → 产出：卷纲/卷N-方向锚.md + 写作参考/设定/* + 写作资产/文风库/{书名}.md + 活记忆/活记忆.yaml(baseline)
→ pop-writer-v3-plot（幕纲设计）
  → 产出：卷纲/幕NNN-名称.md（含结构分析表+物理坐标段+设定引用指针）
→ expert-writer 5步循环（涌现写作环）
```

### 路径2：继续写作（每章）

```
用户："继续"/"下一步"/"写第X章"
→ step-1-think.md（状态感知+意图识别）
  → 判断：幕纲存在？ → 是
  → 前置校验：活记忆+文风DNA+写作参考索引
→ step-2-execute.md（5步循环执行）
  → Step0 导演意图提取（主会话）
    → 读幕纲结构分析表 → 组装导演意图 → 【CHECK 1】用户确认
  → Step1 状态快照投影（主会话）
    → 读活记忆+幕纲物理坐标 → 投影状态快照
  → Step2 信息获取（主会话）
    → 设定指针强制读取 → library查询 → pop-research(如需)
  → Step3 子agent创作（调度子agent）
    → create：context manifest→涌现写作→初稿+receipt
    → revise：初稿+文风DNA→重写稿+receipt → 【CHECK 2】用户验收
  → Step4 receipt检查（主会话）
    → 6项检查 → 通过/修复/降级
  → Step5 活记忆更新+落盘（主会话）
    → 活记忆追加 → 正文落盘 → 项目总控更新 → 弧线触发检查
→ step-3-reflect.md（审视+引导）
```

### 路径3：L2单元完成 → 弧线校准

```
L2单元最后一章 Step5 完成
→ 弧线触发检查：是最后一章 → 触发arc
→ pop-writer-v3-arc（弧线校准）
  → 检查L2单元结构完整性
  → 校准L3剧情线
  → 压缩活记忆
  → 修剪失效要素（归档到写作参考/已废弃/）
  → 更新幕纲
→ arc完成 → expert-writer 5步循环（下一L2单元）
```

### 路径4：按需调研

```
Step2 信息获取中判断需要外部调研
→ pop-research（按需调用，尚未创建则WebSearch替代）
  → 调研结果沉淀到 写作参考/知识沉淀/
  → 更新 写作参考/索引.md
→ 回到 Step2 继续信息获取
```

### 路径5：回滚

```
用户："回滚到第N章"
→ step-2-execute.md §3.2
→ 删除 正文/chNNN.md 及之后
→ 回退活记忆
→ 更新项目总控
→ 从第N章 Step0 重新开始
```

### 路径6：拆书

```
用户："拆这本书"
→ pop-decon（拆书分析）
→ 产出拆书报告
```

---

## 文件产出/消费关系

| 阶段 | 产出 | 消费 |
|:-----|:-----|:-----|
| seed | 卷纲/卷N方向锚 + 写作参考/设定/* + 文风库 + 活记忆(baseline) | — |
| plot | 卷纲/幕NNN-{名称}.md | 卷N方向锚 + 设定 |
| emerge Step0 | 导演意图 | 幕纲结构分析表 |
| emerge Step1 | 状态快照 | 活记忆 + 幕纲物理坐标 |
| emerge Step2 | info_acquired | 导演意图settings_ref + 写作参考/索引 + library |
| emerge Step3 | 初稿(create) + 重写稿(revise) + 2个receipt | context manifest |
| emerge Step4 | receipt检查结果 | manifest + receipt |
| emerge Step5 | 活记忆追加 + 正文落盘 + 项目总控更新 | 本章正文 + 导演意图 + 状态快照 |
| arc | 弧线校准报告 + 幕纲更新 + L3卡 + 活记忆压缩 | 正文 + 活记忆 + 幕纲 |

---

## 关键文件路径速查

| 文件 | 路径 | 加载方式 |
|:-----|:-----|:---------|
| 幕纲 | `卷纲/幕NNN-名称.md` | Get-Content -Raw |
| 活记忆 | `活记忆/活记忆.yaml` | Get-Content -Raw |
| 文风DNA | `写作资产/文风库/{书名}.md` | Get-Content -Raw |
| 写作参考索引 | `写作参考/索引.md` | Get-Content -Raw |
| 设定文件 | `写作参考/设定/*.md` | Get-Content -Raw（强制） |
| 正文 | `正文/chXXX.md` | Get-Content -Raw |
| 项目总控 | `项目总控.md` | Get-Content -Raw |
| 管线合同 | `references/pipeline/manifest.md` | Get-Content -Raw |
