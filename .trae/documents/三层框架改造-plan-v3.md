# 三层框架改造 Plan v3 — 管线重构为 5 步

## 改造总纲

**管线精简为 5 步、3 次 LLM 调用**：

```
Step 1: Director（LLM）
  → 读 act-XX.yaml（emotional_goal + info_release）+ 读者画像
  → 出设计说明 + 信息释放策略（不碰文风DNA）

Step 2: 上下文搜集（零 LLM）
  → 按 Director 指示拿：
    · L1 设定（按 info_release.source_doc 读）
    · 上一章结尾最后 800 字
    · entity-state.yaml
    · global-summary.md
  → 出世界快照（结构化 YAML）

Step 3: 骨架 Agent（LLM）
  → 读 Director 设计说明 + 世界快照
  → 按 事实骨架模板.md 填事件链+设定包+密度标记
  → 骨架层 QC

Step 4: 渲染（LLM）
  → 输入：骨架 + 世界快照 + 设计说明 + 文风DNA（5条原则）
  → Layer 1（骨架）→ 写什么
  → Layer 3（文风DNA）→ 怎么写
  → 输出正文 + 状态更新块（渲染器正文后附带输出）

Step 5: 状态更新（零 LLM）
  → 从渲染器输出的状态更新块解析
  → 追加到 global-summary.md
  → 更新 entity-state.yaml
  → 不需 LLM 调用
```

**关键删除**：
- ❌ ESM before 的 DNA→叙事策略指令生成（Layer 2 砍掉）
- ❌ 锚定章片段注入渲染器（DNA 已蒸馏）
- ❌ Pass1（骨架 Agent 独立文件 `Pass1-chapter-planner.md`）
- ❌ SQLite/DB 引用（未运维，改为文件）
- ❌ experience-log （未运维，暂时冻结）

---

## 涉及文件清单

| # | 文件 | 操作 | 说明 |
|:-:|:----|:----|:------|
| 1 | **NEW** `templates/事实骨架模板.md` | 新建 | 骨架标准化产出格式 |
| 2 | **NEW** `templates/entity-state-schema.md` | 新建 | 世界快照 + 实体状态模板 |
| 3 | **NEW** `templates/everything-bundle-schema.md` | 新建 | Step 4 渲染器的完整输入包格式参考 |
| 4 | `SKILL.md` | **重写** | 管线改为 5 步、全文重写 |
| 5 | `prompt-templates/Director-prompt.md` | 重写 | Step 1 prompt，不含 DNA、不含锚定章处理 |
| 6 | `prompt-templates/Pass1-chapter-planner.md` | **删除** | 被 Step 3 骨架 Agent 取代 |
| 7 | `prompt-templates/Pass2-renderer.md` | **重写** | Step 4 renderer prompt，消费骨架+DNA，需输出状态更新块 |
| 8 | `prompt-templates/global-summary-schema.md` | 更新 | 强化 entity-state 字段、释放优先级 |
| 9 | `prompt-templates/experience-log-schema.md` | 不动 | 保留但管线不再强制消费 |
| 10 | `CHANGELOG.md` | 追加 | v11.0.0 |
| 11 | `skill.json` | 版本号 | 9.7.0 → 11.0.0 |

---

## 模板规范

### 1.1 事实骨架模板.md

```markdown
# ch{XXX} 事实骨架

> 由骨架 Agent（Step 3）产出。供给渲染器（Step 4）直接消费。

---

## 信息释放执行

- 设定{名称}通过{实战展示}嵌入骨架事件{编号}
- 设定{名称}通过{叙事者说明}嵌入骨架插槽【插·设定说明】

---

## 事件节点

### 节点 1：[事件简述]

**事件**：[一句话描述发生了什么事]

**设定包**：
- {key}: {从 L1 提取的具体文本内容}
- {key}: {从 L1 提取的具体文本内容}

**密度标记**：[极高/高/中/低]

**涉及实体**：{实体名}、{实体名}

### 节点 2：[事件简述]
...

---

## 统计数据

- 事件节点总数：{N}
- 唯一实体计数：{N}（要求 ≥ 8）
- 设定包条目数：{N}
- 预估字数：{N}（要求 ≥ 1800）
```

**骨架层 QC 标准**：
```
□ 事件链完整覆盖本章全部不可变事件
□ 每个 info_release 在骨架中有对应的嵌入位置
□ {实体名} 计数 ≥ 8
□ 预估字数 ≥ 1800
□ 无叙事结构决策（"此处应为高潮"）
□ 无叙事者评价（"主角很愤怒"）
□ 设定包内容全部从 L1 提取（非编造）
```

---

### 1.2 entity-state-schema.md（世界快照模板）

```markdown
# 世界快照 · ch{当前章号}

> 由 Step 2 上下文搜集产出。供给骨架 Agent 和渲染器使用。

---

## 当前时间

- 日期/时间点：[故事内时间]
- 经过时间：[自上一章过去了多少时间]

---

## 角色状态

{角色名}:
  status: [{健康/受伤/昏迷/死亡/...}]
  location: [{位置}]
  key_items: [{关键物品清单}]
  recent_memory: [{最近1-2句发生的核心事件回忆}]

{角色名}:
  ...

---

## 全局环境

- 地点：[当前主要场景位置]
- 天气/环境：[天气、光照等环境条件]
- 当前威胁：[当前正在进行的危险/冲突，如有]

---

## 未收伏笔（TOP 5）

- {伏笔名} — {当前状态}
- {伏笔名} — {当前状态}
```

---

### 1.3 everything-bundle-schema.md（渲染器输入包模板）

```markdown
# 渲染器输入包 · ch{XXX}

> 由 Step 4 渲染器接收的完整输入结构。

---

## 输入项

| # | 项目 | 说明 |
|:-:|:----|:------|
| 1 | 读者画像 | 谁在读 |
| 2 | 事实骨架 | Step 3 产出的事件链+设定包+密度标记 |
| 3 | 世界快照 | Step 2 产出的实体状态+全局环境 |
| 4 | 文风DNA | 5条叙事哲学原则 |
| 5 | 宪法红线 | 写作禁止清单 |
| 6 | 全局摘要 | 全书进展 1500 字以内 |
| 7 | 上一章结尾 | 原文最后 800 字 |
| 8 | 导演设计说明 | Step 1 产出 + 信息释放策略 |
| 9 | 经验日志 | （如有）|
| 10 | 知识注入 K1-K4 | 网文理论参考 |
```

---

## Step 1 → Step 5 管线改动

### 2.1 重写 SKILL.md

当前 130 行的管线描述（第 80-210 行）全部替换。

**新 SKILL.md 管线段**：

```markdown
## 六阶段管线（5步驱动）

先判断是否启用黄金三章模式：

```
用户的章节？
  ├─ CH1–CH3 → 黄金三章模式
  └─ CH4+ → 正常管线
```

### 正常管线（CH4+）

#### Step 1：Director（LLM）

**输入**：
- act-XX.yaml 当前章切片（含 emotional_goal + info_release + plotlines_active）
- 读者画像（project.yaml reader_profile）
- L1 元设定层

**输出**：设计说明 + 信息释放策略

**设计说明**包含：
- 本章核心目的（一句话）
- 场景权重分配 + 字数目标
- 爽点触发方式
- 描写密度指南

**信息释放策略**（关键产出）：
- 本章释放哪些设定信息（从 info_release 读取）
- 每项信息的释放方式（实战展示/角色对话/叙事者说明/探索发现）
- 信息密度控制（本章新概念 ≤ N 个）

**☆ Director 不读文风DNA** — DNA 由渲染器直接消费。

→ 大纲层 QC 通过才进 Step 2。

---

#### Step 2：上下文搜集（零 LLM）

按 Director 的信息释放策略，从文件系统读取：

1. **L1 设定** — 按 info_release 中的 source_doc 路径读取
2. **上一章结尾** — 读取上一章正文最后 800 字
3. **entity-state.yaml** — 读取当前实体状态
4. **global-summary.md** — 读取全书进展摘要

**输出**：世界快照（结构化 YAML，格式参考 `templates/entity-state-schema.md`）

→ 进 Step 3。

---

#### Step 3：骨架 Agent（LLM）

**输入**：Step 1 设计说明 + Step 2 世界快照

**输出**：事实骨架（格式参考 `templates/事实骨架模板.md`）

**执行**：
1. 按信息释放策略中的 release_method 确定事件节点嵌入方式
2. 按 density 确定展开程度
3. 按模板格式组织事件链 + 设定包 + 密度标记
4. 填充统计数据

**骨架层 QC**：
```
□ 事件链完整覆盖本章全部不可变事件
□ 每个 info_release 在骨架中有对应嵌入位置
□ {实体名} 计数 ≥ 8
□ 预估字数 ≥ 1800
□ 无叙事结构决策
□ 无叙事者评价
□ 设定包内容全部从 L1 提取
```
不通过 → 退回修改。通过 → 进 Step 4。

---

#### Step 4：渲染（LLM）

**输入**（Everything Bundle）：
| # | 项目 |
|:-:|:-----|
| 1 | 事实骨架（Step 3 产出）|
| 2 | 世界快照（Step 2 产出）|
| 3 | 设计说明 + 信息释放策略（Step 1 产出）|
| 4 | 文风DNA（5条叙事哲学原则，来自文风锚定包）|
| 5 | 宪法红线 |
| 6 | 全局摘要 |
| 7 | 上一章结尾原文 |

**三层框架消费**：
- **Layer 1（骨架）** → 写什么
- **Layer 3（文风DNA）** → 怎么写
- 没有 Layer 2 中间层

**输出**：
1. **成品正文** — 本章完整正文
2. **状态更新块** — 正文后追加以下结构：

```yaml
# === 状态更新 ===
chapter: {编号}
summary: "一句话总结本章核心进展"
entity_updates:
  {角色名}:
    status: {新状态}
    location: {新位置}
    key_items: [{关键物品变更}]
  {角色名}:
    ...
world_updates:
  时间: {新时间点}
  地点: {新地点}
  状态: {全局状态变化}
event_log:
  - {核心事件1}
  - {核心事件2}
```

**写后自评**：
- "战斗场景和文风DNA中信息释放哲学一致吗？"
- "这一章我给了读者几个节点去回味？"
- "字数差了多少？差的篇幅应该写什么？"
- "对照 info_release 确认每条设定信息是否在正文中出现"

---

#### Step 5：状态更新（零 LLM）

从渲染器产出的状态更新块中解析，写入文件：

1. **追加到 global-summary.md**
   - 在"追加记录"表中新增一行
   - 更新"全书进展"顶层字段（主角状态、最新事件）

2. **更新 entity-state.yaml**
   - 按 entity_updates 逐条更新角色状态
   - 按 world_updates 更新时间/地点

3. **更新伏笔状态**（如有）

**输出文件**：
- `design/global-summary.md` — 追加后
- `design/entity-state.yaml` — 更新后
```

---

### 2.2 重写 Director-prompt.md

当前文件的 v4.0 版本做了过多的事。新版本精简：

**输入**：
- act-XX.yaml 当前章切片（含 info_release）
- 读者画像
- L1 设定

**输出**：设计说明 + 信息释放策略

**前置检查**：
```
□ 读者画像已读入
□ 爽点等级已确认
□ info_release 已确认（本章释放哪些设定信息）
□ 字数目标已定
```

**不要包含**：
- ❌ 文风DNA读取
- ❌ 锚定章引用（不需要了，信息释放策略已确定设定释放方式）
- ❌ 锚定章选择

---

### 2.3 重写 Pass2-renderer.md

当前 v4.0 文件重写。新版本：

**输入项（精简为 10 项）**：
```
 1 读者画像
 2 事实骨架（事件链+设定包+密度标记）
 3 世界快照（实体状态+全局环境）
 4 文风DNA（5条叙事哲学原则）
 5 宪法红线 + 写作禁止清单
 6 全局摘要（全书进展 ≤1500字）
 7 上一章结尾原文（最后800字）
 8 导演设计说明 + 信息释放策略
 9 经验日志（如有）
10 知识注入 K1-K4
```

**三层框架消费**：
```
【Layer 1：事实骨架】
  优先级最高。骨架中的每一个事件节点必须在正文中出现。
  - 有设定包的节点：对应设定必须在正文中释放，方式遵守 release_method
  - 密度标记：极高/高→充分展开，中/低→点到为止

【Layer 3：文风DNA（5条叙事哲学原则）】
  控制句子质感、情感表达方式、对话策略。
  - DNA 原则是信念层——"为什么要这么写"
  - 直接应用，不需要中间翻译层
```

**输出格式**：
正文 + 状态更新块（yaml 代码块）

**写后自评**：
```
① "这一章的信息释放按骨架执行了吗？"
   → 对照骨架中的设定包和密度标记
② "这一章我给了读者几个'停下来'的时刻？"
   → 标记至少 1 处"读者可能滑过去"的位置
③ "字数差了多少？差的篇幅本来应该写什么？"
   → 字数不足 → 补一个被压缩的场景
④ "文风DNA的原则我遵守了吗？"
   → 检查叙事者姿态/情感表达/对话策略是否偏离
```

---

### 2.4 删除 Pass1-chapter-planner.md

整个文件删除。

---

### 2.5 更新 global-summary-schema.md

强化 entity-state 字段：
```
- 新增：**entity_state** — 当前各角色状态快照（供 Step 2 直接读取）
- 新增：**世界快照导出** — 明确每次更新后自动导出到 entity-state.yaml
```

---

## 实施顺序

```
Phase 1: 新建 3 个模板（事实骨架模板.md / entity-state-schema.md / everything-bundle-schema.md）
Phase 2: 重写 SKILL.md 管线部分
Phase 3: 重写 Director-prompt.md
Phase 4: 删除 Pass1-chapter-planner.md
Phase 5: 重写 Pass2-renderer.md
Phase 6: 更新 global-summary-schema.md
Phase 7: CHANGELOG + skill.json 版本号更新
Phase 8: git add + commit + push
```

## 兼容性

- 旧版 `act-XX.yaml`（无 info_release）→ Director 检测后不输出信息释放策略，Step 2 直接 skip
- `entity-state.yaml` 不存在 → Step 2 跳过该文件，只读 global-summary
- Pass1-chapter-planner.md 删除 → 旧管线不会自动调用
