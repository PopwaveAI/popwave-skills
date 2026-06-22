# Step 1：建立基线

> 管线: pop-writer-chapter v2.2
> 模板: `templates/baseline.tpl.md`
> 产出: 本章设计基线（内存，不落盘）
> 下游: Step 2 全程消费此基线

## 目的

读完本章的容器约束 + 角色快照 + 剧情线上下文，建立一份结构化基线。基线回答：**这一章在什么位置、受什么约束、当前角色什么状态、活跃线在做什么**。

Step 2 不再回头翻源文件——所有决策从基线出发。

## 读什么

### 优先路径：pop-state-engine 上下文组装

```bash
python {engine_scripts}/command_executor.py -p {项目路径} -a for-creation -j '{"chapter": {N}}'
```

引擎返回 JSON 包含：book_summary → volume_summary → arc_summary → recent_summaries → active_entities → active_facts → open_hooks → continuity_notes。自动裁剪到 ~5-8KB，替代全量加载 act-YY.md + entity-snapshot.yaml。

**fallback 条件**：引擎返回为空（`active_entities` 为空且 `recent_summaries` 为空）时，退回文件加载路径。

### Fallback 路径：文件全量加载

| # | 文件 | 读什么 | 为什么 |
|:-:|:-----|:-------|:-------|
| 1 | `剧情设计/幕/vol-XX/act-YY.md` | **全文** | 理解整段剧情全貌：幕功能/幕级门槛/章锚点/Canvas 矩阵/枪链。不是只看本章切片 |
| 2 | `状态/entity-snapshot.yaml` | 全部角色当前状态 | 本章登场角色的 before 状态唯一 canon |
| 3 | `剧情设计/剧情线/{线名}.md` | **仅本章 Canvas 中活跃的线** | 活跃线的驱动力/套路链/枪链/阶段位置。非活跃线不读 |

> 双读过渡期：引擎和 entity-snapshot.yaml 并行。引擎有数据时优先用引擎（数据更新、裁剪更精准），引擎无数据时退回文件加载。

## 不读什么

- ❌ 不读非活跃剧情线（本章 Canvas 中空白的线）
- ❌ 不读角色卡（Step 2 按需读）
- ❌ 不读套路库（Step 2 按需读）
- ❌ 不读 PRD（chapter 不消费）

## 做什么

按 `templates/baseline.tpl.md` 组装基线，全部字段从上述 3 个文件提取——不编造。

---

## 门禁

| 检查项 | 失败动作 |
|:-------|:---------|
| 幕纲不存在 | ❌ 终止，提示先完成 plot |
| entity-snapshot 不存在 | CH1 → 执行初始化；非 CH1 → ❌ 终止 |
| Canvas 中本章无任何活跃线 | ⚠️ 警告，继续（可能是纯过渡章） |
| 剧情线文档缺失（活跃线对应的） | ❌ 终止 |

### 上游时效性检查（在存在性检查后执行）

| 检查项 | 失败动作 |
|:-------|:---------|
| 幕纲 `lastUpdatedAt` 早于项目总控的框架级变更时间 | ⚠️ 标注「幕纲可能过期，建议先回 plot 更新」 |
| entity-snapshot 最后更新章号 vs 当前目标章号差距 > 3 章 | ⚠️ 标注「entity-snapshot 过期」 |
| 卷纲 `lastUpdatedAt` 早于项目总控的框架级变更时间 | ⚠️ 标注「卷纲可能过期」 |

## 产出

基线写入**内存**（不落盘）。Step 2 从基线出发设计，不再回头翻源文件。

---
⛔ 下一 step：`steps/step-2-event-chain.md` — 加载后才能继续（`Get-Content -Encoding UTF8 -Raw steps/step-2-event-chain.md`）
