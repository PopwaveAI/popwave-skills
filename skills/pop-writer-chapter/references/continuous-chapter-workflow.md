# 连章工作流 — 持续章节生产的操作顺序

> 适用场景：第一卷已架构完成（全书架构/卷设计/幕结构已就绪），需要逐章产出。
> 前置条件：`00-总控/entity-snapshot.yaml` 已初始化，前三章已通过断链修补验证。

---

## 一、每章产出顺序（CH4+ 已验证模式）

```mermaid
flowchart LR
    A[读act-XX.yaml Canvas] --> B[读entity-snapshot\n当前状态]
    B --> C[设计事件链+v3设计包]
    C --> D[写入设计包.md]
    D --> E[渲染正文v3]
    E --> F[核验正文质量]
    F --> G[更新entity-snapshot\n→ CH{N}末状态]
    G --> H[更新event_log+\ntimeline]
    H --> I[供下一章调用]
```

### Step 0：读章级 Canvas

从 `设计/幕/vol-01/act-XX.yaml` 的 `chapters[N]` 块提取：

| 字段 | 用途 |
|:-----|:------|
| title | 章标题 |
| word_count | 字数目标 |
| canvas.设定线 + 设线负载 | 本章需交付的设定信息 |
| canvas.{主线}_payoff | 释放级别，决定★中爽点位置 |
| 登场角色 | 角色池，从 entity-snapshot 取当前状态 |
| emotional_goal | 情绪弧线边界 |
| end_hook.type + drive | 章末钩子方向 |
| chekhov_set / chekhov_fire | 设伏/回收的枪 |

### Step 1：读 entity-snapshot 当前状态

从 `00-总控/entity-snapshot.yaml` 取所有登场角色的 before 状态。这是唯一 canon，不凭记忆。

### Step 2：设计事件链（v3）

- 事件数 ≥ word_count ÷ 200
- 每事件填写 scene / POV / 关键对白/数据 / 感官锚点
- 标注 ◆小爽点（≥5）和 ★中爽点（≥1）
- 升级/面板数据必须在关键对白/数据字段写出精确竖列
- 日记/信件/纸条原文精确写出

### Step 3：写入设计包

写入 `写作资产/设计包/chXXX-设计包.md`，含全部事件。

### Step 4：渲染正文（prose v3 pipeline）

1. 读设计包 → scene 字段定位DNA场景卡
2. 感官锚点开头 → POV限知 → 关键对白/数据精确嵌入
3. 状态流三层（感官输入→身体反应→战术评估→行为输出）
4. 无 AI 观感词（他感到/他仿佛/他心想/他意识到）
5. 无解说员句式（不是...而是...归零）
6. 章末_state_update 块

### Step 5：核验

- 解说员句式 = 0
- AI 观感词 = 0
- 字数在目标±20%范围内
- 所有关键对白/数据已嵌入正文
- 钩子已按 Canvas 方向写

### Step 6：更新 entity-snapshot

用 patch() 更新 `00-总控/entity-snapshot.yaml`：

```yaml
# 需要修改的字段
_meta.total_chapters: +1

entities.江轩:
  level: {新等级}
  position: {新位置}
  hp: {新生命/状态}
  equipment: {装备变化}
  seed_awakening: {新觉醒度}
  status_flags: [...更新...]
  relationships: {...更新...}
  core_desire: {新目标}

entities.{其他角色}: {对应更新}

event_log: [+本行事件摘要]

timeline: [+本行时间节点]
```

---

## 二、连章工作流注意事项

### 2.1 委托模式（Hermes 专属）

当批量生产章节时，使用并行 delegate_task 提升效率：

```
Phase 1 — 设计包升级（一次性修补已有章节）
  委托: CH1 设计包 → subagent A
  委托: CH2 设计包 → subagent B
  委托: CH3 设计包 → subagent C
  ← 三个并行完成后合入

Phase 2 — 正文重写（一次性修补已有章节）
  委托: CH1 正文 → subagent A
  委托: CH2 正文 → subagent B
  委托: CH3 正文 → subagent C
  ← 三个并行完成后合入

Phase 3 — 新章生产（逐章线性）
  每个新章：设计包 + 正文 = 一个 subagent 任务
  → parent 在 subagent 完成后读取 state_update 块，更新 entity-snapshot
```

### 2.2 跨章节衔接点

| 衔接点 | 处理方式 |
|:-------|:---------|
| 上一章末尾情绪 → 本章开幕 | 读上一章正文最后3-5段，确保情绪过渡自然 |
| 上一章钩子 → 本章首事件 | CH{N}的end_hook必须被CH{N+1}的第一个事件兑现或承接 |
| 角色状态延续 | 从 entity-snapshot 取 before 状态，设计包中的 after 状态=下一章的 before |
| 未解决的事件/伏笔 | 检查上一章设计包的 chekhov_set，那些设伏在本章是否 chekhov_fire |

### 2.3 非战斗章的特殊处理

| 章类型 | 事件粒度 | 爽点策略 | 关键对白/数据侧重 |
|:-------|:---------|:---------|:-----------------|
| transition（过渡） | 10-14事件 | ◆小爽点靠物资发现/信息碎片/配合默契 | 对话中的信息碎片 |
| dialogue（对话） | 12-18事件 | ◆小爽点靠干脆表态/情报密度 | 精确台词·面部微表情 |
| discovery（探索） | 12-18事件 | ◆小爽点靠线索拼接/环境解读 | 环境描述中的信息精确度 |
| combat（战斗） | 20-28事件 | ◆小爽点靠每回合干净操作·★中爽点靠升级/面板 | 升级数据·法术描述 |
| crisis（危机） | 16-22事件 | ◆小爽点靠险中求存的决策 | 时间压力·生理数据 |

### 2.4 变化追踪

每章结束后以下内容一定有变化：
- 江轩的 level / position / equipment / seed_awakening / core_desire
- 登场配角的状态（可能还有关系变化）
- 本章击杀/消耗的敌方实体
- 主线1-3的推进进度
- event_log 和 timeline

不建议直接在 entity-snapshot 中保存"无变化"的实体（如萝丝在卷1中期前）——只更新活跃实体即可。
