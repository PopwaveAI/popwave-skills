# pop-state-engine 集成指南

> 将 Popwave writer skills 接入 pop-state-engine 的实操指南。覆盖 5 个 skill 的接入模式、双写双读过渡策略、agent 标注验证流程和集成顺序。

## CLI 调用约定

所有命令统一走 `command_executor.py`：

```bash
python scripts/command_executor.py -p {项目路径} -a {动作} -j '{JSON参数}'
```

本文所有示例中 `{P}` 代表项目根目录路径，`{ENGINE}` 代表 `pop-state-engine/scripts` 目录。实际调用时需补全为绝对路径。

## 集成顺序

按以下顺序逐个接入，每个 skill 完成双写双读验证后再进入下一个：

```
1. pop-writer-prose      ← 章末登记不破坏现有流程，风险最低
2. pop-writer-chapter    ← 读上下文需要引擎已有数据（prose 先写入）
3. pop-writer-plot       ← 卷级状态，依赖 chapter 已能正常读引擎
4. pop-writer-world      ← 引擎初始化，L1 设定入库
5. pop-writer-creative  ← 储备卡注册
6. pop-novel         ← 总控 project-status 锚点同步（最后接入）
```

**为什么 prose 先行**：章末登记是纯写入操作（store-chapter / add-node / set-fact / resolve-hook），不改变 chapter 的读取逻辑，即使引擎数据不全也不影响现有写作流程。而 chapter 的 `for-creation` 依赖引擎里已有数据，必须等 prose 跑通后才有意义。

---

## 模式一：pop-writer-prose 章末登记

每章正文写完后，prose 按顺序执行 5 步登记。这是引擎数据的主要来源。

### 步骤 1：store-chapter（设计包入库）

将本章设计包正文存入引擎，建立 FTS5 全文索引。

```bash
python {ENGINE}/command_executor.py -p {P} -a store-chapter -j '{
  "chapter": 15,
  "content": "第十五章正文内容...",
  "characters": "李明,赵雪",
  "tags": "突破,宗门大比",
  "events": "李明突破筑基,赵雪认输"
}'
```

### 步骤 2：Agent 标注新实体和状态变化

agent 阅读本章正文，在设计包中标注：
- **新实体**：本章首次出现的角色、地点、物品、功法
- **状态变化**：已有实体的属性变更（修为提升、关系转变、位置移动等）

这一步由 agent 直接完成，不调用引擎。标注结果作为后续验证的基准。

### 步骤 3：extract-entities（脚本辅助验证）

运行实体提取器，将脚本结果与步骤 2 的 agent 标注做对比：

```bash
python {ENGINE}/command_executor.py -p {P} -a extract-entities -j '{
  "content": "第十五章正文内容..."
}'
```

返回 JSON 包含 `characters` / `locations` / `items` / `events` / `new_entities`，每个实体带 `confidence`（high / medium / low）。对比要点：
- **agent 标注有、脚本没有** → 以 agent 为准（脚本可能漏提）
- **脚本有、agent 没有且 confidence=low** → 丢弃（脚本误匹配）
- **两边都有** → 确认入库

### 步骤 4：Agent 确认后 add-node + set-fact

对验证通过的新实体和状态变化，逐条写入引擎：

```bash
# 新角色入库
python {ENGINE}/command_executor.py -p {P} -a add-node -j '{
  "name": "周长老",
  "type": "character",
  "tags": "宗门长老,筑基期",
  "properties": "{\"role\":\"反派\",\"first_appearance\":15}"
}'

# 状态变化入库（已有实体属性变更）
python {ENGINE}/command_executor.py -p {P} -a set-fact -j '{
  "entity": "李明",
  "attribute": "修为",
  "value": "筑基初期",
  "category": "character",
  "chapter": 15,
  "importance": "chapter-scoped"
}'
```

**importance 三级选择**：
- `permanent` — 世界观级永久事实（身份、出身、核心设定）
- `arc-scoped` — 弧线级事实（持续一个卷/弧线的关系、状态）
- `chapter-scoped` — 章节级临时事实（默认值，会被后续同属性事实替代）

### 步骤 5：list-hooks → resolve-hook（伏笔回收）

检查本章是否回收了任何已种入的伏笔：

```bash
# 列出当前未回收伏笔
python {ENGINE}/command_executor.py -p {P} -a list-hooks -j '{
  "current_chapter": 15
}'
```

如果返回的 hooks 中有本章已回收的，逐条标记回收：

```bash
python {ENGINE}/command_executor.py -p {P} -a resolve-hook -j '{
  "hook_id": "hook_003",
  "resolved_chapter": 15,
  "how": "李明用周长老赠予的破阵符破解了禁制"
}'
```

### 章末登记完整流程图

```
store-chapter → agent标注 → extract-entities对比 → add-node+set-fact → list-hooks→resolve-hook
     ↓              ↓              ↓                      ↓                      ↓
  正文入库       人工基准       脚本验证              实体/事实入库          伏笔回收
```

---

## 模式二：pop-writer-chapter 上下文加载

用引擎的 `for-creation` 替代全量文件加载，按章节自动裁剪上下文。

### 替代方案

**改造前**：chapter 每次加载全部设定文件 + entity-snapshot.yaml + 历史章节，token 浪费严重。

**改造后**：

```bash
python {ENGINE}/command_executor.py -p {P} -a for-creation -j '{
  "chapter": 16
}'
```

返回自动组装的上下文包（裁剪到 ~5-8KB），包含：
- `book_summary` → 全书摘要
- `volume_summary` → 当前卷摘要
- `arc_summary` → 当前弧线摘要
- `recent_summaries` → 近几章摘要
- `active_entities` → 活跃实体
- `active_facts` → 当前有效事实
- `open_hooks` → 未回收伏笔
- `continuity_notes` → 连续性提示

### entity-snapshot.yaml 作为降级兜底

引擎返回空（如项目刚初始化、数据未灌入）时，回退到读取 `entity-snapshot.yaml`：

```
if for-creation 返回空 or active_facts 为空:
    读取 entity-snapshot.yaml（现有逻辑不变）
else:
    使用引擎返回的上下文包
```

### CH1 初始化分支不变

第 1 章是项目起点，引擎尚无历史数据，`for-creation` 自然返回空。CH1 的初始化逻辑（读取 world L1 设定、建立初始状态）保持现有实现不变，不接入引擎读取。

---

## 模式三：pop-writer-plot 卷级状态

plot 产出卷级策略后，将弧线和伏笔种入引擎。

### 卷策略输出后：create-arc + store-summary

```bash
# 创建卷弧线
python {ENGINE}/command_executor.py -p {P} -a create-arc -j '{
  "arc_id": "vol2_arc",
  "title": "第二卷：宗门大比",
  "arc_type": "arc",
  "start_chapter": 31,
  "end_chapter": 60,
  "description": "李明参加宗门大比，从外门弟子崛起至内门"
}'

# 存储卷摘要
python {ENGINE}/command_executor.py -p {P} -a store-summary -j '{
  "level": "volume",
  "range_desc": "2",
  "content": "第二卷核心冲突：宗门大比中的阶级对抗..."
}'
```

**arc_type 说明**：
- `arc` — 弧线（对应一卷的主线）
- `phase` — 阶段（卷内更细的阶段划分，通过 `phase_id` 关联到 arc）

### 剧情线输出后：plant-hook + add-edge

每条剧情线可能种入伏笔或建立实体关系：

```bash
# 种入伏笔
python {ENGINE}/command_executor.py -p {P} -a plant-hook -j '{
  "desc": "周长老赠予的破阵符来历不明，符上刻有上古铭文",
  "planted_chapter": 31,
  "expected_resolve": 45,
  "priority": "high",
  "characters": "周长老,李明"
}'

# 建立实体关系
python {ENGINE}/command_executor.py -p {P} -a add-edge -j '{
  "source": "周长老",
  "target": "李明",
  "relation": "暗中扶持",
  "properties": "{\"since_chapter\":31,\"motive\":\"偿还旧恩\"}"
}'
```

**priority 三级**：`critical`（主线必收）/ `high`（重要支线）/ `medium`（点缀性伏笔）。

---

## 模式四：pop-writer-world 引擎初始化

world 产出 L1 设定后，将世界观实体和事实批量灌入引擎。这是引擎数据的初始来源。

### L1 输出后：add-node × N + set-fact × N + store-summary

```bash
# 世界观实体入库（角色、地点、势力、物品、功法...）
python {ENGINE}/command_executor.py -p {P} -a add-node -j '{
  "name": "玄天宗",
  "type": "faction",
  "tags": "正道,顶级宗门",
  "properties": "{\"location\":\"玄天峰\",\"leader\":\"天玄子\"}"
}'

python {ENGINE}/command_executor.py -p {P} -a add-node -j '{
  "name": "李明",
  "type": "character",
  "tags": "主角,外门弟子",
  "properties": "{\"background\":\"没落家族\",\"talent\":\"隐藏灵根\"}"
}'

# 世界观事实入库（永久设定，importance=permanent）
python {ENGINE}/command_executor.py -p {P} -a set-fact -j '{
  "entity": "玄天宗",
  "attribute": "定位",
  "value": "正道顶级宗门，坐落于玄天峰",
  "category": "world",
  "chapter": 0,
  "importance": "permanent"
}'

python {ENGINE}/command_executor.py -p {P} -a set-fact -j '{
  "entity": "李明",
  "attribute": "身份",
  "value": "玄天宗外门弟子，没落家族出身",
  "category": "character",
  "chapter": 0,
  "importance": "permanent"
}'

# 全书摘要入库
python {ENGINE}/command_executor.py -p {P} -a store-summary -j '{
  "level": "book",
  "range_desc": "book",
  "content": "《xxx》是一部讲述没落家族子弟李明在修仙世界中..."
}'
```

**chapter=0 约定**：世界观级事实使用 `chapter=0` 表示"开篇前确立的设定"，区别于正文中产生的事实。

### L1 文档不再每章加载

改造前：chapter 每章都读取全部 L1 设定文档（世界蓝图、力量体系、势力格局等），token 消耗大。

改造后：L1 文档只在 world Phase 2 执行时读取一次并灌入引擎。后续 chapter 通过 `for-creation` 获取引擎中已结构化的设定事实，不再重复加载原始文档。

---

## 模式五：pop-writer-creative 储备卡注册

creative 产出储备卡（预备角色、预备场景、预备道具等）后，注册到引擎知识图谱。

### 储备卡输出后：add-node + set-fact

```bash
# 储备卡实体入库（properties 标注来源）
python {ENGINE}/command_executor.py -p {P} -a add-node -j '{
  "name": "神秘黑衣人",
  "type": "character",
  "tags": "储备,未登场",
  "properties": "{\"source\":\"储备卡-伏笔角色-01\",\"intended_role\":\"后期反派\",\"trigger\":\"李明突破金丹后登场\"}"
}'

# 储备卡事实入库（importance=permanent，长期保留）
python {ENGINE}/command_executor.py -p {P} -a set-fact -j '{
  "entity": "神秘黑衣人",
  "attribute": "设定",
  "value": "身份未定，与李明家族没落有关，持有上古残卷",
  "category": "character",
  "chapter": 0,
  "importance": "permanent"
}'
```

**关键约定**：
- `properties.source` 标注储备卡名称，便于追溯来源
- `importance=permanent` 确保储备卡设定长期保留，不会被章节级事实替代
- 储备卡实体 `tags` 含"储备"标记，`for-creation` 默认不将其推入活跃上下文，直到正式登场

---

## 双写双读过渡策略

entity-snapshot.yaml（旧）和引擎（新）在过渡期并行运行，分三阶段切换：

### 阶段 1：双写（引擎写入 + yaml 写入）

skill 同时向引擎和 entity-snapshot.yaml 写入数据。此阶段引擎数据逐步积累，yaml 保持现有逻辑不变。

```
prose 章末 → store-chapter + add-node + set-fact（引擎写入）
           → 同时更新 entity-snapshot.yaml（yaml 写入，现有逻辑）
```

### 阶段 2：双读（引擎读取 + yaml 读取）

chapter 同时从引擎和 yaml 读取上下文，对比两者一致性：

```
chapter → for-creation（引擎读取）
       → 同时读取 entity-snapshot.yaml（yaml 读取）
       → 对比两者，记录差异
```

确认稳定标准：连续 N 章（建议 5-10 章）引擎与 yaml 数据一致，无遗漏实体或事实。

### 阶段 3：退役 yaml

确认稳定后，移除 yaml 读写逻辑，引擎成为唯一数据源：

```
prose 章末 → 仅引擎写入
chapter    → 仅 for-creation 读取
```

**每个 skill 独立走完三阶段**，不要求全局同步切换。prose 先完成双写验证，chapter 再完成双读验证，依次推进。

---

## Agent 标注 → 脚本验证 → 确认 → 入库流程

这是 prose 章末登记步骤 2-4 的核心机制，也适用于其他需要实体入库的场景。

### 流程详解

```
┌─────────────┐     ┌──────────────────┐     ┌──────────┐     ┌────────────────┐
│ Agent 标注  │ →   │ extract-entities │ →   │ Agent    │ →   │ add-node       │
│ (设计包内)  │     │ (脚本辅助验证)   │     │ 确认     │     │ + set-fact     │
└─────────────┘     └──────────────────┘     └──────────┘     └────────────────┘
```

**第一步：Agent 标注**

agent 阅读正文，在设计包中直接标注新实体和状态变化。这是人工基准，agent 理解叙事语境，能识别脚本无法捕捉的隐含信息（如暗示性出场、关系暗线）。

**第二步：extract-entities 脚本验证**

`extract-entities` 作为脚本辅助验证工具运行，不是唯一来源。它基于 jieba 分词 + 称谓模式 + 题材自适应关键词，提供机器视角的实体清单。将脚本结果与 agent 标注对比：

| 情况 | 处理 |
|------|------|
| agent 有、脚本有 | 确认入库（双重验证通过） |
| agent 有、脚本没有 | 以 agent 为准入库（脚本漏提，常见于隐含实体） |
| 脚本有、agent 没有 + confidence=high | agent 复核，确认后入库（agent 可能漏看） |
| 脚本有、agent 没有 + confidence=low | 丢弃（脚本误匹配） |

**第三步：Agent 确认**

agent 综合两份清单，产出最终入库清单。确认标准：
- 实体名准确（非误匹配的动词/虚词组合）
- 实体类型正确（character / location / item / faction）
- 状态变化有正文依据

**第四步：add-node + set-fact 入库**

对确认后的实体逐条调用 `add-node`（新实体）和 `set-fact`（状态变化），写入引擎。

### 为什么不直接用 extract-entities 入库

`extract-entities` 基于规则匹配，存在误匹配（如将"来到玄天峰"中的"玄天峰"误判为角色）和漏提（如未用称谓后缀的隐含角色）。agent 标注提供语境理解，脚本提供覆盖率验证，两者交叉确认才能保证入库质量。脚本的角色是"辅助验证"而非"自动入库"。

---

## 附：命令速查

| 场景 | 命令 | 关键参数 |
|------|------|---------|
| 正文入库 | `store-chapter` | chapter, content, characters, tags, events |
| 章节摘要 | `store-summary` | level=chapter, range_desc=章号, content |
| 卷摘要 | `store-summary` | level=volume, range_desc=卷号, content |
| 全书摘要 | `store-summary` | level=book, range_desc=book, content |
| 创建弧线 | `create-arc` | arc_id, title, arc_type, start_chapter, end_chapter |
| 新实体入库 | `add-node` | name, type, tags, properties(JSON) |
| 实体关系 | `add-edge` | source, target, relation, properties(JSON) |
| 事实入库 | `set-fact` | entity, attribute, value, category, chapter, importance |
| 种入伏笔 | `plant-hook` | desc, planted_chapter, expected_resolve, priority |
| 回收伏笔 | `resolve-hook` | hook_id, resolved_chapter, how |
| 列出伏笔 | `list-hooks` | current_chapter, priority |
| 实体提取 | `extract-entities` | content, types |
| 上下文组装 | `for-creation` | chapter |
| 项目状态 | `project-status` | （无参数） |

**importance 三级**：`permanent`（永久）/ `arc-scoped`（弧线级）/ `chapter-scoped`（章节级，默认）

**summary level 六级**：`book` / `phase` / `arc` / `volume` / `chapter` / `scene`

**arc_type 两类**：`arc`（弧线）/ `phase`（阶段）
