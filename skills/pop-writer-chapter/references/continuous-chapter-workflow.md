# 连章工作流 — 持续章节生产的操作顺序

> 适用场景：第一卷已架构完成，需要逐章产出。
> 前置条件：`状态/entity-snapshot.yaml` 已初始化。
> 管线: pop-writer-chapter v2.3

## 一、每章产出顺序

```
读 act-YY.md Canvas → 读 entity-snapshot → 设计事件链 → 写入设计包
→ 更新 entity-snapshot（after 状态）→ 渲染正文(prose) → 供下一章调用
```

> ★ entity-snapshot 由 chapter 维护——prose 不参与状态管理。chapter 从设计包的 after 状态直接更新。

### Step 0：读幕纲 Canvas

从 `剧情设计/幕/vol-XX/act-YY.md` 提取本章信息：

| 从幕纲取 | 用途 |
|:---------|:------|
| 章锚点表的章目标/活跃线/钩子/payoff | 本章约束 |
| Canvas 矩阵各线状态 | 哪些线在动 |
| 篇幅预算 | 本章章数约束 |
| 枪链段 | 本章设伏/回收的枪 |

### Step 1：读 entity-snapshot

从 `状态/entity-snapshot.yaml` 取所有登场角色的 before 状态。这是唯一 canon。

### Step 2：设计事件链

- 事件数 ≥ word_count ÷ 200
- 每事件填写 scene / POV / 关键对白 / 感官锚点
- 标注 ◆小爽点（≥5）和 ★中爽点（≥1）
- 查 `pop-trope-library/套路库/{套路名}.md` 节奏控制段

### Step 3：写入设计包 + 更新状态

- 写入 `章节设计包/chXXX-设计包.md`
- 更新 `状态/entity-snapshot.yaml`（after 状态）
- 同步 `剧情设计/幕/vol-XX/act-YY.md` 枪链段

## 二、跨章节衔接点

| 衔接点 | 处理方式 |
|:-------|:---------|
| 上一章末尾情绪 → 本章开幕 | 读上一章设计包情绪弧线终点 |
| 上一章钩子 → 本章首事件 | 钩子必须被本章第一个事件兑现或承接 |
| 角色状态延续 | entity-snapshot 的 after = 下一章的 before |

## 三、非战斗章的特殊处理

| 章类型 | 事件粒度 | 爽点策略 |
|:-------|:---------|:---------|
| transition | 10-14事件 | ◆小爽点靠物资发现/信息碎片 |
| dialogue | 12-18事件 | ◆小爽点靠干脆表态/情报密度 |
| discovery | 12-18事件 | ◆小爽点靠线索拼接/环境解读 |
| combat | 20-28事件 | ◆小爽点靠每回合干净操作 |
| crisis | 16-22事件 | ◆小爽点靠险中求存的决策 |
