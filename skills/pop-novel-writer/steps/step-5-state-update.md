# Step 3：状态更新（零 LLM）

> 职责：章末 delta 写入 → 全量快照聚合。零 LLM 调用——纯文件 IO。
> 核心协议：**章末 `# === 状态更新 ===` 块是唯一写入源（delta）。entity-snapshot.yaml 是从所有 delta 聚合的派生视图。**

---

## 协议原则

```
                    ┌──────────┐
                    │ 章末 delta │ ← 唯一写入源（本文 Step 3.2 产出）
                    │ ch00X.md  │   entity_updates + world_updates + event_log
                    └────┬─────┘
                         │
                         │ 聚合（Step 3.3）
                         ▼
              ┌─────────────────────┐
              │ entity-snapshot.yaml │ ← 编译产物（从所有章 delta 重新生成）
              │  全量当前状态快照     │    损坏/丢失？重跑聚合即可恢复
              └─────────────────────┘

章末 delta 存在每章正文文件末尾，永不删除。
entity-snapshot.yaml 每次写完一章后完整重建（覆盖写入，不增量编辑）。
```

---

## 输入

| # | 输入 | 来源 |
|:-:|:-----|:-----|
| 1 | 上一章正文文件的末尾 `# === 状态更新 ===` 块 | `{paths.chapters}/ch{上一章}.md` |
| 2 | project.yaml 的 `paths.chapters` 字段 | `00-总控/project.yaml` |
| 3 | 全部已有章的 `# === 状态更新 ===` 块（用于聚合） | `{paths.chapters}/ch*.md` |

---

## 执行

### 3.1 读取路径注册

从 `project.yaml` 读取章节目录路径：

```yaml
# project.yaml 是路径注册中心
paths:
  chapters: "03-正文/"    # ← 章文件目录
  outline: "02-大纲/"
  settings: "00-原始设定/"
```

不硬编码路径。所有后续文件定位都从 project.yaml 的 paths 字段派生。

### 3.2 确认章末 delta 已写入

渲染器（Step 2）在每章末尾产出了 `# === 状态更新 ===` 块，格式如下：

```
# === 状态更新 ===
chapter: {编号}
summary: "{1-2句核心进展}"
style_report:
  phase1_contract: "{已锚定}"
  phase3_result: "{✅/⚠️}"
  p0_violations: {N}
  deviations: []
entity_updates:
  角色名:
    status: "{新状态}"
    mental: "{心理状态}"
    location: "{位置}"
    key_items: [{物品列表}]
world_updates:
  时间: "{故事内时间}"
  地点: "{场景}"
event_log:
  - "{事件1}"
  - "{事件2}"
```

> 如果章末没有状态更新块 → 记录警告，跳过本章聚合（不编造数据）。

### 3.3 聚合 entity-snapshot.yaml（全量快照）

从 **所有已有章**（ch001 到 ch{当前}）的章末 delta 重建全量快照。

#### 聚合算法

```
输入: project.yaml#paths.chapters 下所有 ch*.md 的状态更新块
输出: entity-snapshot.yaml（覆盖写入）

算法:
1. 初始化空快照 skeleton（见下方 schema）
2. 按章号升序遍历每章的状态更新块:
   a. 遍历 entity_updates 中每个角色:
      - 覆盖 status / mental / location（最新章为准）
      - key_items 做 merge：新章追加，不覆盖旧章列表
      - 角色首次出现 → 创建条目
      - 角色 status=死亡 → 保留在快照，标记 status: 死亡
   b. world_updates: timeline 取最新章的值
   c. event_log: append 到按章组织的 event_log 列表
3. 写入 entity-snapshot.yaml（完整覆盖，不增量编辑）
```

#### 输出格式

路径：`00-总控/entity-snapshot.yaml`

```yaml
# entity-snapshot.yaml — 从所有章末 delta 聚合
# 自动维护，由 Writer Step 3.3 生成（每次写完一章后完整重建）
# 损坏/丢失 → 重跑 Step 3.3 即可恢复

_meta:
  generated_at: "{ISO时间戳}"
  source_chapters: "ch001-ch{当前}"
  total_chapters: {N}

protagonist:
  name: "{主角名}"
  status: "{最新状态}"
  rank: {当前阶位}
  level: "{当前等级描述}"
  mental: "{最新心理状态}"
  location: "{最新位置}"
  key_items: [{合并后的物品列表}]
  money: {铜币/银币/金币}
  achievements: [{成就列表}]

characters:
  {角色名}:
    status: "{健康/受伤/昏迷/死亡}"
    location: "{最新位置}"
    key_items: [{物品列表}]
    first_appearance: "ch{编号}"
    last_update: "ch{编号}"

timeline:
  world_time: "{最新故事内时间}"
  day: {第N天}

flags:
  - "{全局标记1·状态}"
  - "{全局标记2·状态}"

event_log:
  ch001:
    - "{事件}"
  ch002:
    - "{事件}"

style_stats:
  total_p0_violations: {累计P0违规数}
  chapters_with_violations: [{章号列表}]
```

#### 聚合纪律

- 每次写入是完整覆盖，不执行增量 diff — 避免累积偏移
- key_items 合并策略：保留所有章提到过的物品，去重（按名称匹配）
- 角色状态只有最新章说了算，不继承旧状态（除非旧状态是"死亡"且未被新章覆盖）
- entity-snapshot.yaml 第一行为注释 `# 自动维护，由 Writer Step 3.3 生成`

### 3.4 更新 global-summary.md（轻量摘要）

路径：`{项目根}/03-写作资产/global-summary.md`

操作：
1. 更新"已完成章节"行和"最近更新"时间戳
2. 如果 global-summary.md 存在且格式正确 → 将本章 summary 追加到追加记录表
3. global-summary.md 的角色状态表不再独立维护 —— 如需最新角色状态，读 entity-snapshot.yaml

> global-summary.md 降级为"人类可读的叙事摘要"，不再承担状态追踪职能。状态追踪的唯一 canon 是 entity-snapshot.yaml。

---

## 输出文件

| 文件 | 操作 | 说明 |
|:-----|:-----|:-----|
| `{paths.chapters}/ch{编号}.md` | 已由 Step 2 写入 | 章末 delta（唯一写入源） |
| `00-总控/entity-snapshot.yaml` | **覆盖写入** | 从所有章 delta 聚合的全量快照 |
| `03-写作资产/global-summary.md` | 轻量追加 | 叙事摘要（降级） |

---

## 注意事项

- entity-snapshot.yaml 损坏/丢失 → 重跑 Step 3.3 即可完整恢复（因为所有源数据在章文件中）
- 如果某章的 entity_updates 字段缺失 → 对应的角色状态保持不变，不编造数据
- 章节目录路径始终从 project.yaml#paths.chapters 读取，不硬编码
- 全局状态文件的权威来源是 entity-snapshot.yaml，不是 chapter-state.yaml（后者是 bookstrap 的初始快照，写作开始后由 entity-snapshot 取代）
