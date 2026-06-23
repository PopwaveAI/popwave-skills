# 连章工作流 — 持续章节生产的操作顺序

> 适用场景：第一卷已架构完成，需要逐章产出。
> 前置条件：`状态/state-log.yaml` 已初始化。
> 管线: pop-writer-chapter v2.3

## 一、每章产出顺序

```
读 L2-{编号}.md Canvas → 读 state-log.yaml → 设计事件链 → 写入设计包
→ 渲染正文(prose) → prose 章末追加 event 到 state-log.yaml → 供下一章调用
```

> ★ state-log.yaml 是 append-only 叙事日志。chapter 只读不写——prose 章末追加 event。当日志过长时执行 compaction（将旧 event 合并为新 baseline），不再使用 history 快照。

### Step 0：读L2幕纲 Canvas

从 `剧情设计/幕/vol-XX/act-YY.md` 提取本章信息：

| 从L2幕纲取 | 用途 |
|:---------|:------|
| 章锚点表的章目标/活跃线/钩子/payoff | 本章约束 |
| Canvas 矩阵各线状态 | 哪些线在动 |
| 篇幅预算 | 本章章数约束 |
| 枪链段 | 本章设伏/回收的枪（从 state-log.yaml 读 open 伏笔列表） |

### Step 1：读 state-log.yaml

从 `状态/state-log.yaml` 读最后 baseline + event，取所有登场角色的 before 状态。这是唯一 canon。

### Step 2：设计事件链

- 事件数 ≥ word_count ÷ 200
- 每事件填写 scene / POV / 关键对白 / 感官锚点
- 标注 ◆小爽点（≥5）和 ★中爽点（≥1）
- 查 `pop-trope-library/套路库/{套路名}.md` 节奏控制段

### Step 3：写入设计包

- 写入 `章节设计包/chXXX-设计包.md`
- 设计包 after 段标注伏笔预判（设伏/回收）
- state-log.yaml 由 prose 章末追加 event 维护，chapter 不写

## 二、跨章节衔接点

| 衔接点 | 处理方式 |
|:-------|:---------|
| 上一章末尾情绪 → 本章开幕 | 读上一章设计包情绪弧线终点 |
| 上一章钩子 → 本章首事件 | 钩子必须被本章第一个事件兑现或承接 |
| 角色状态延续 | state-log.yaml 最后 event 的 after = 下一章的 before |

## 三、非战斗章的特殊处理

| 章类型 | 事件粒度 | 爽点策略 |
|:-------|:---------|:---------|
| transition | 10-14事件 | ◆小爽点靠物资发现/信息碎片 |
| dialogue | 12-18事件 | ◆小爽点靠干脆表态/情报密度 |
| discovery | 12-18事件 | ◆小爽点靠线索拼接/环境解读 |
| combat | 20-28事件 | ◆小爽点靠每回合干净操作 |
| crisis | 16-22事件 | ◆小爽点靠险中求存的决策 |
