# 创作状态引擎 PRD

> 创建日期：2026-07-07
> 文档性质：技术产品 PRD，面向工程落地
> 上游规划：`prd/10-popwave产品规划/popwave产品规划.md` 第三章

---

## 一、背景与问题

### 1.1 已有的数据层

popwave 的 paopao 运行时已经维护了两层数据：

**runs（per-run 碎片化日志）**：每次对话一个 UUID 目录，含 input.json（完整输入上下文，含 system prompt + 所有 skill SKILL.md 全文，约 50-65KB/次）+ events.jsonl（模型推理事件流，约 90-110KB/次）+ response.md（agent 输出）。为 agent runtime 服务，每次请求需要完整上下文重发。实测 12 个 run 共 2.1MB，其中 89% 是 skill 全文冗余。规模化后（700 章约 1500-2200 个 run）总量约 260-385MB。

**conversations（per-conversation 聚合层）**：一个对话一个 jsonl 文件，每行一条 message（user/assistant），assistant message 内嵌完整 events（含 thinking、tool-call、tool-result）和 file-change 事件（含 action/path/diff）。实测 12 个 run 聚合为 1 个 conversation 文件，1.4MB / 25 行。已有对话上下文、文件变更记录、runId 关联。

### 1.2 已有数据层的局限

conversations 已经聚合了对话和文件变更，但三个局限让它无法直接支撑产品层诉求：

**单行过重**：每条 assistant message 含完整 thinking + tool-result，单行可达 50-100KB。快速扫描"项目全貌"成本高。

**缺产品级事件**：conversations 只记录 agent runtime 的事件。用户在编辑区直接改文件、拖文件进项目、手动调整设定——这些产品级操作不在 conversations 里，agent runtime 不知道。

**操作记录不是状态**：conversations 记录"第 3 轮写了角色储备池.md"，但不记录"张三等级变成了 5"。要查角色当前状态，得回放所有相关文件的变更历史或直接读文件——而文件本身可能不可靠（96.3% 的 agent 跳过 skill 文件读取，状态更新被跳过或降级）。

### 1.3 三条产品诉求

老板提出的实战诉求，定义了 log 要达到的目标：

1. **本项目空间内用户提过什么需求，agent 给了什么反馈**——对话级事实查询
2. **每个角色的状态、剧情事件等**——状态级语义查询
3. **编辑区用户直接改、外部拖文件进来等**——产品级事件捕获

诉求 1 和 3 是事实查询（不需要理解内容含义），诉求 2 是语义查询（需要理解文件内容提取状态）。两类查询的采集方式不同，分两层实现。

### 1.4 解决方案：项目空间 Event Store

建一份项目级的 Event Store——append-only 事件流，按时间轴排序，记录项目空间内发生的所有事件。分两层演进：

- **事实层（第一阶段）**：采集对话、文件变更、产品级事件。不需要 LLM，纯结构化分流，从 conversations + 编辑器埋点采集
- **语义层（第二阶段）**：异步 LLM 从文件内容提取实体变更事件（角色状态变化、设定变更、剧情推进）。不阻塞 runtime，延迟可接受

Event Store 只追加事件，不维护当前状态。消费方需要状态时，从事件流按时间轴 replay 聚合。这是 Event Sourcing 模式——event store 记"发生了什么"，state 是 replay 的结果。

---

## 二、设计目标与非目标

### 2.1 设计目标

1. **项目空间级 Event Store**：一个项目一份事件流，append-only，按时间轴排序，覆盖所有类型的事件
2. **事实层先做**：对话、文件变更、产品级事件不需要 LLM，第一阶段落地
3. **语义层后做**：实体变更事件由 LLM 异步提取，不阻塞 runtime，不定义领域 schema
4. **与 skill 解耦**：Event Store 只观察和记录，不替 skill 做决策，不定义工具语义，不编排流程
5. **时间轴查询**：事件按 ts 排序，时间范围查询是基础能力，后续 UI 可直接渲染时间轴视图
6. **文本友好**：JSON Lines 格式，grep / jq 可查

### 2.2 非目标

- 不替代 runs（runs 是 runtime 刚需，Event Store 是消费方导航）
- 不替代 conversations（conversations 是对话聚合，Event Store 是项目级事件流，数据源部分重叠但定位不同）
- 不定义领域 schema（不定义 Chapter/Setting/Character 的字段结构）
- 不维护当前状态（只追加事件，状态由消费方 replay 聚合）
- 不做矛盾检测 / 校验 / 快照 / 回滚（这些是消费方的事）
- 不编排 skill 流程

---

## 三、架构设计

### 3.1 定位：项目空间 Event Store

```
┌─────────────────────────────────────────────┐
│           Skill 层（现有，不改动）             │
│  读 Event Store 查询事件 / replay 聚合状态     │
├─────────────────────────────────────────────┤
│     Event Store（本 PRD 范围）                │
│                                             │
│  ┌─────────────────────────────────────┐    │
│  │  语义层（第二阶段，LLM 异步提取）      │    │
│  │  实体变更事件（角色/设定/剧情）        │    │
│  └───────────────┬─────────────────────┘    │
│  ┌───────────────┴─────────────────────┐    │
│  │  事实层（第一阶段，不需要 LLM）        │    │
│  │  对话事件 + 文件变更 + 产品事件        │    │
│  └───────────────┬─────────────────────┘    │
│                  │                          │
│  events.jsonl (append-only, 时间轴排序)      │
├─────────────────────────────────────────────┤
│     数据源                                   │
│  conversations (对话+文件变更)                │
│  编辑器埋点 (用户直接改/拖文件)               │
│  文件内容 (语义层LLM提取实体变更)             │
└─────────────────────────────────────────────┘
```

### 3.2 Event Store vs 领域中间件

前版 PRD 试图做领域中间件（定义 Chapter/Setting schema、定义 save_draft/commit_chapter 工具、做校验引擎），被否决因为和 skill 耦合太重。Event Store 的核心区别：

| 维度 | 领域中间件（被否决） | Event Store（当前方案） |
|---|---|---|
| 领域 schema | 引擎定义 Chapter/Setting/Character schema | 不定义 schema，只记事件 |
| 状态维护 | 引擎维护当前状态 | 只追加事件，不维护状态 |
| skill 耦合 | 定义 save_draft/commit_chapter 工具语义 | 不定义工具语义，只观察和记录 |
| LLM 介入 | 校验时同步调 LLM，阻塞流程 | 异步批量提取语义事件，不阻塞 |
| 替 skill 做决策 | 是（校验、快照、编排） | 否（只观察记录） |

### 3.3 Event Store vs conversations

| 维度 | conversations | Event Store |
|---|---|---|
| 组织方式 | per-conversation | per-project（聚合所有对话） |
| 单行大小 | 50-100KB（含完整 thinking + tool-result） | 200-500 字节（只记事实） |
| 产品级事件 | 无（只有 agent runtime 事件） | 有（编辑器埋点） |
| 语义事件 | 无 | 有（第二阶段 LLM 提取） |
| 查询 | 可查但单行太重，快速扫描成本高 | 轻量，grep/jq 高效 |

Event Store 从 conversations 采集事实层事件（对话、文件变更），但不复制 thinking 和 tool-result——只提取消费方需要的字段。

---

## 四、事件格式

### 4.1 存储位置

Event Store 存放在 paopao 的项目元数据目录（`.paopao/projects/{id}/`）下，不在工作区目录里：

```
.paopao/projects/{project_id}/         # 项目元数据目录
  ├── conversations/                    # 对话聚合（数据源）
  ├── runs/                             # per-run 日志（数据源）
  ├── artifacts/                        # 对话消息存储（数据源）
  ├── project.json                      # 项目元数据
  └── .popwave/
      └── events.jsonl                  # Event Store，append-only，时间轴排序

# 工作区目录（实际文件存放位置，由 project.folderPath 决定）：
{folderPath}/                           # 如 C:\Users\...\paopao-workspace\projects\{project_id}\
  ├── 正文/ch001.md
  ├── 设定库.md
  ├── 活记忆/活记忆.yaml
  └── ...
```

关键区分：Event Store 在项目元数据目录（`.paopao/projects/{id}/.popwave/`），实际文件在工作区目录（`project.folderPath`）。file 事件里的 `path` 是相对于工作区的相对路径，`workspace_path` 是工作区绝对路径，两者拼起来路由到物理文件。

### 4.2 通用事件结构

所有事件共享通用字段，`type` 区分事件类型，`data` 承载类型特有字段。

实测产出（6-29-项目a，从 3.3MB conversation 采集为 125KB events.jsonl，118 条事件）：

```jsonl
{"ts":"2026-06-29T08:13:07.828Z","type":"user_message","data":{"conversation_id":"b922d319","run_id":"7279ccb2","content":"从library库里下载 深渊主宰 世界观设定+ 第一幕的单元剧情卡 + 文风dna"}}
{"ts":"2026-06-29T08:15:37.404Z","type":"assistant_message","data":{"conversation_id":"b922d319","run_id":"7279ccb2","content_head":"全部拉取完成！文件已下载到 `6-29-项目a/library/` 下...","content_size":946}}
{"ts":"2026-06-29T08:15:37.444Z","type":"file_created","data":{"path":"library/单元剧情卡/深渊主宰-v1-001-贫民区开篇.md","workspace_path":"C:\\Users\\AWMPRO\\AppData\\Roaming\\popwave\\paopao-workspace\\projects\\6-29-项目a","source":"agent","run_id":"7279ccb2","conversation_id":"b922d319","change_id":"f7849f48-c4a8-4cea-ad6f-f509e1ceb27b","content_head":"# L2-001 · 贫民区开篇（ch001-ch005）\n\n> **范围**: ch001-ch005..."}}
{"ts":"2026-07-07T14:20:00Z","type":"file_modified","data":{"path":"设定库.md","workspace_path":"...","source":"editor","content_head":"## L1-02 力量体系..."}}
{"ts":"2026-07-07T04:30:00Z","type":"entity_state_change","data":{"entity_type":"character","entity_id":"char:索伦","field":"等级","old_value":"1","new_value":"3","source_file":"正文/ch047.md","extracted_by":"llm"}}
```

通用字段：

| 字段 | 说明 |
|---|---|
| `ts` | 事件时间戳（ISO 8601），时间轴坐标 |
| `type` | 事件类型（见 §4.3 / §4.4） |
| `data` | 事件特有字段 |

### 4.3 事实层事件类型（第一阶段，不需要 LLM）

**对话事件**——从 conversations 采集：

| type | data 字段 | 说明 |
|---|---|---|
| `user_message` | conversation_id, run_id, content | 用户指令全文 |
| `assistant_message` | conversation_id, run_id, content_head（前 200 字符）, content_size | agent 输出速览 |

**文件变更事件**——从 conversations 的 file-change + 编辑器埋点采集：

| type | data 字段 | 说明 |
|---|---|---|
| `file_created` | path, workspace_path, source, run_id, conversation_id, change_id, content_head | 文件创建 |
| `file_modified` | path, workspace_path, source, run_id, conversation_id, change_id, content_head | 文件修改 |
| `file_deleted` | path, workspace_path, source, run_id, conversation_id | 文件删除（无 content_head，文件已不存在） |
| `file_imported` | path, workspace_path, source(editor), content_head | 用户拖文件进项目 |

file 事件的路由字段（核心设计——不存内容，但给到清晰准确的查询地址）：

| 字段 | 说明 | 路由目标 |
|---|---|---|
| `path` | 相对于工作区的文件路径（如 `正文/ch047.md`） | 拼接 workspace_path → 物理文件 |
| `workspace_path` | 工作区绝对路径（来自 input.json 的 `project.folderPath`） | path 的根 |
| `change_id` | file-change 事件的 UUID | 回溯到 conversation 里的原始 diff |
| `conversation_id` | 所属对话 ID | 定位 conversation 文件 |
| `run_id` | 所属 run ID | 定位 runs 目录 |
| `content_head` | 文件内容前 500 字符（已清洗 diff 标记） | 快速预览，不打开文件 |
| `source` | `agent` 或 `editor` | 区分 agent 操作和用户操作 |

消费方读文件的完整路由链：

```
events.jsonl 一条 file_created 事件
  → data.path = "正文/ch047.md"
  → data.workspace_path = "C:\Users\...\paopao-workspace\projects\6-29-项目a"
  → 物理文件 = workspace_path + "/" + path
  → cat 物理文件 → 完整内容

需要回溯 diff 时：
  → data.change_id = "f7849f48-..."
  → data.conversation_id = "b922d319-..."
  → 在 conversations/{conversation_id}.jsonl 里找 change_id 对应的 file-change 事件
  → diff 字段 → 变更详情
```

实测验证（6-29-项目a）：从 events.jsonl 取第一条 file_created 事件，path=`library/单元剧情卡/深渊主宰-v1-001-贫民区开篇.md`，拼 workspace_path 后 `Test-Path` 确认物理文件存在。60 个 file 事件的 path 全部能路由到物理文件。

**产品事件**——编辑器埋点采集：

| type | data 字段 | 说明 |
|---|---|---|
| `project_opened` | - | 用户打开项目 |
| `project_closed` | - | 用户关闭项目 |

### 4.4 语义层事件类型（第二阶段，LLM 异步提取）

**实体变更事件**——LLM 从文件内容提取：

| type | data 字段 | 说明 |
|---|---|---|
| `entity_state_change` | entity_type(character/setting/plotline), entity_id, field, old_value, new_value, source_file, extracted_by(llm) | 实体状态变更 |
| `entity_introduced` | entity_type, entity_id, source_file, description, extracted_by | 新实体出现 |
| `entity_removed` | entity_type, entity_id, source_file, extracted_by | 实体消失（角色死亡等） |

语义层不定义实体 schema——`field` 是自由文本（"等级""位置""心理状态"），不约束字段结构。LLM 从文件内容里提取什么就记什么，消费方自己决定怎么解析。

### 4.5 量级估算

| 维度 | 事实层 | 语义层 |
|---|---|---|
| 单次事件大小 | 200-500 字节 | 300-600 字节 |
| 每章事件数 | 约 10-20 条（5-8 个工具调用 + 对话） | 约 5-10 条（角色/设定/剧情变更） |
| 700 章总量 | 约 10-14 万条，5-10MB | 约 3-5 万条，2-3MB |
| 合计 | 7-13MB | |

对比 runs 的 260-385MB，Event Store 降两个数量级，grep/jq 可直接处理。

### 4.6 日志管理

- **append-only**：只追加不修改，任何历史记录不可变
- **时间轴排序**：事件按 ts 排序，写入序即时间序
- **轮转**：events.jsonl 超过 10MB 时轮转为 `events-{YYYYMMDD}.jsonl`，新事件继续写主文件
- **不压缩**：事件是原始事实，保留完整
- **不删数据**：即使项目回滚，事件也保留

---

## 五、时间轴查询

时间轴是 Event Store 的天然索引——append-only 日志按时间排序，`ts` 字段就是坐标。所有查询的基础都是时间范围过滤。

### 5.1 基础查询

```bash
# 项目全貌：按时间顺序看所有事件
cat .popwave/events.jsonl | jq -r '.ts + " " + .type + " " + (.data.content_head // .data.path // .data.entity_id // "")'

# 某时间段发生了什么
cat .popwave/events.jsonl | jq -c 'select(.ts >= "2026-07-07T12:00" and .ts < "2026-07-07T18:00")'

# 诉求1：用户提过什么需求
cat .popwave/events.jsonl | jq -r 'select(.type=="user_message") | .ts + " " + .data.content'

# 诉求3：编辑区改了哪些文件
cat .popwave/events.jsonl | jq -r 'select(.type | startswith("file_") and .data.source=="editor") | .ts + " " + .type + " " + .data.path'
```

### 5.2 状态查询（诉求2）

语义层落地后，按实体过滤 + 时间范围 replay：

```bash
# 张三的所有状态变更事件
cat .popwave/events.jsonl | jq -c 'select(.type=="entity_state_change" and .data.entity_id=="char:张三")'

# 张三在第47章时的状态（replay到该时间点）
cat .popwave/events.jsonl | jq -c 'select(.type=="entity_state_change" and .data.entity_id=="char:张三" and .ts <= "2026-07-07T16:00")'
```

语义层未落地时，fallback 到直接读文件——Event Store 帮定位"哪轮碰了角色相关文件"，再读文件内容。

### 5.3 时间轴视图（后续 UI）

事件流按 ts 排序，后续 UI 可直接渲染为时间轴视图——项目从立项到当前，一条时间线串起所有事件。这是产品层甜点功能（时间轴回溯）的数据基础。

---

## 六、采集机制

### 6.1 事实层采集（第一阶段）

**从 conversations 采集对话事件和 agent 文件变更**：

conversations 已有 user_message / assistant_message / file-change 事件。采集脚本读取 conversation jsonl，提取需要的字段（content / path / action / content_head），转换为 Event Store 格式写入 events.jsonl。

采集时机：
- **方式 A（实时）**：paopao 运行时在写 conversation 后同步触发采集脚本（推荐）
- **方式 B（增量）**：下次 run 启动时，脚本扫描 conversation 文件的新增行，增量采集（兜底）

**从编辑器埋点采集产品事件和编辑区文件变更**：

用户在编辑区直接改文件、拖文件进来时，编辑器触发埋点回调，写入 events.jsonl。这是 conversations 覆盖不到的区域——agent runtime 不知道用户在编辑区做了什么。

埋点事件：
- 文件保存（用户在编辑区修改并保存）→ `file_modified`，source=editor
- 文件拖入 → `file_imported`，source=editor
- 文件删除 → `file_deleted`，source=editor
- 项目打开/关闭 → `project_opened` / `project_closed`

### 6.2 语义层采集（第二阶段）

**LLM 异步提取实体变更事件**：

每隔 N 轮（或每章完成时），批量提取任务读取最近变更的文件内容，调 LLM 提取实体变更事件，追加到 events.jsonl。

提取逻辑：
- 输入：最近变更的文件内容（正文、设定库、人物库等）
- LLM prompt：从文本中提取角色状态变化、设定变更、剧情推进事件，输出结构化 JSON
- 输出：`entity_state_change` / `entity_introduced` / `entity_removed` 事件
- 不定义实体 schema：field 是自由文本，LLM 提取什么就记什么

不阻塞 runtime，延迟可接受（用户不需要实时看到语义事件）。用轻量模型（如 gpt-4o-mini）降低成本。

---

## 七、与现有数据层的关系

### 7.1 不替代，复用 + 补充

| 数据层 | 定位 | 与 Event Store 的关系 |
|---|---|---|
| runs | agent runtime 完整上下文 | 不动。Event Store 不从 runs 采集（冗余太大），从 conversations 采集 |
| conversations | 对话级聚合 | 事实层数据源。Event Store 从 conversations 提取轻量字段，不复制 thinking/tool-result |
| 项目文件 | 创作产物 | 语义层数据源。LLM 从文件内容提取实体变更事件 |

### 7.2 数据流

```
paopao 运行时
    │
    ├──→ runs/{uuid}/              （runtime 完整上下文，不动）
    ├──→ conversations/{id}.jsonl   （对话聚合，不动）
    │         │
    │         └──→ 采集脚本 ──→ events.jsonl（事实层：对话+文件变更）
    │
    └──→ 编辑器埋点 ──→ events.jsonl（事实层：产品事件+编辑区文件变更）

文件内容 ──→ LLM 异步提取 ──→ events.jsonl（语义层：实体变更）
```

---

## 八、实现路径

### 8.1 阶段一：事实层 Event Store

**目标**：项目空间内所有事实级事件可查，时间轴可浏览。

**交付物**：

1. events.jsonl 写入逻辑（append-only，时间轴排序）
2. conversations 采集脚本：从 conversation jsonl 提取对话事件和文件变更事件
3. 编辑器埋点接口：文件保存/拖入/删除/项目打开关闭
4. `.popwave/` 目录初始化逻辑
5. 日志轮转逻辑（超过 10MB 轮转）
6. 从现有 conversations 补建 events.jsonl 的迁移脚本

**验证标准**：

- 现有 7-7-项目a 的 conversation 补建 events.jsonl，包含 12 组对话事件 + 47 条文件变更事件
- 新 run 结束后，对话事件和文件变更事件自动追加
- 用户在编辑区改文件、拖文件后，对应事件出现在 events.jsonl
- `cat events.jsonl | jq -r 'select(.type=="user_message") | .data.content'` 输出所有用户指令
- `cat events.jsonl | jq -r 'select(.data.source=="editor") | .ts + " " + .type + " " + .data.path'` 输出所有编辑区操作
- 采集脚本出错时不影响 agent 正常工作

### 8.2 阶段二：语义层扩展

**目标**：实体变更事件可查，支持状态查询。

**交付物**：

1. LLM 异步提取任务：批量读取变更文件，提取实体变更事件
2. 提取触发机制：每 N 轮或每章完成时触发
3. 实体变更事件写入 events.jsonl
4. 状态 replay 查询示例

**验证标准**：

- 写完第 47 章后，LLM 提取出"张三等级从 3 变成 5"事件
- `cat events.jsonl | jq -c 'select(.type=="entity_state_change" and .data.entity_id=="char:张三")'` 输出张三的所有状态变更
- replay 到某时间点的事件，聚合出该时间点的角色状态
- 语义提取不阻塞 runtime，延迟 <5 分钟

### 8.3 后续（不在本 PRD 范围）

- 基于 Event Store 的时间轴 UI 视图
- 基于 Event Store 的状态重建 skill
- 基于 Event Store 的矛盾检测 skill
- 跨项目 Event Store 聚合

---

## 九、风险与对策

| 风险 | 概率 | 影响 | 对策 |
|---|---|---|---|
| conversations 格式变化导致采集失败 | 中 | 中 | 采集脚本做防御性解析，字段缺失时跳过；记录 parse_error |
| 编辑器埋点遗漏事件 | 中 | 中 | 埋点是补充源，遗漏不影响 agent 事件采集；定期比对文件系统与事件流做一致性检查 |
| 语义层 LLM 提取不准 | 中 | 中 | 语义事件标注 extracted_by: llm 和置信度；消费方可选择不信任 LLM 提取结果，fallback 到读文件 |
| 语义层 LLM 成本 | 中 | 低 | 用轻量模型；批量提取而非逐文件；只在文件变更时触发 |
| events.jsonl 膨胀 | 低 | 低 | 10MB 轮转；700 章预估 7-13MB，单文件可承载 |
| 采集脚本影响 runtime | 低 | 高 | 采集是 fire-and-forget，失败静默丢弃，不阻塞 runtime |

---

## 九.五、缺口检查（实测发现）

用 6-29-项目a 实测采集时发现并修复的缺口：

| 缺口 | 状态 | 说明 |
|---|---|---|
| path 无法路由到物理文件 | 已修复 | file 事件缺少 workspace_path，消费方不知道工作区根路径。已从 input.json 的 `project.folderPath` 提取，加入 file 事件 |
| 缺少 change_id | 已修复 | file 事件无法回溯到 conversation 原始 diff。已从 file-change 事件的 `id` 字段提取，加入 file 事件 |
| content_head 含 diff 噪音 | 已修复 | create 操作的 diff 含 `--- before\n+++ after\n` 标记。已加清洗逻辑，去掉 diff header 和 `+`/`-` 前缀 |
| 多 conversation 未处理 | 已修复 | 采集脚本只处理一个 conversation 文件。已改为扫描 conversations 目录下所有 .jsonl 文件 |
| file_deleted 无法路由 | 已知局限 | 删除的文件物理上已不存在，path 无法路由到文件。这是固有局限，file_deleted 事件不记 content_head |
| 路径分隔符不一致 | 已处理 | conversation 的 path 用 `/`（如 `正文/ch001.md`），Windows 文件系统用 `\`。消费方拼路径时需转换 |
| 编辑器埋点未实现 | 待实现 | source=editor 的事件还没有采集机制，需要编辑器支持埋点回调。PRD 第一阶段交付物 |
| 增量采集未实现 | 待优化 | 当前脚本是全量重跑，未做增量同步。后续优化为只采集 conversation 的新增行 |

---

## 十、验收标准

### 10.1 功能验收

1. 事实层采集：对话事件、文件变更事件、编辑器事件均正确写入 events.jsonl
2. 时间轴查询：按 ts 时间范围过滤，正确返回事件子集
3. 诉求 1 验证：`jq` 查询 user_message 事件，输出项目内所有用户指令
4. 诉求 3 验证：`jq` 查询 source=editor 的文件事件，输出所有编辑区操作
5. 语义层采集（阶段二）：LLM 提取的实体变更事件正确写入 events.jsonl
6. 诉求 2 验证（阶段二）：`jq` 查询 entity_state_change 事件，replay 出角色当前状态
7. 迁移补建：现有 conversations 一键补建 events.jsonl
8. 容错：采集脚本出错不影响 agent 正常工作

### 10.2 非功能验收

1. 单条事件写入 <1ms（append-only）
2. 事实层单条事件 <500 字节
3. 700 章项目 events.jsonl <15MB（轮转前）
4. 采集不阻塞 runtime 主流程
5. 日志格式符合 JSON Lines 规范，`jq` 可正常解析

---

## 十一、与产品规划的关系

本 PRD 实现的是产品规划（`popwave产品规划.md`）第三章"创作状态引擎"的**第一阶段：可观测性 + 可查询性基础**。

产品规划的原始诉求是"第 87 章不能让第 12 章死掉的角色复活"——这是状态一致性诉求。本 PRD 的 Event Store 解决的是可观测性（"能查到怎么崩的"）和可查询性基础（"能查到角色状态变更历史"），不直接解决状态一致性（"保证不写崩"）。

但 Event Store 是状态一致性的数据基础：先让创作过程的所有事件可查、可 replay，后续 skill 才能基于事件流做状态重建、矛盾检测、一致性校验。语义层的实体变更事件直接支撑了状态查询（诉求 2），为冲突雷达和角色关系网可视化提供数据底座。

Event Store 的定位是**项目空间的观察者**——只记录，不干预；只追加事件，不维护状态；不替 skill 做决策，不定义领域 schema。skill 怎么消费事件流是 skill 自己的事。
