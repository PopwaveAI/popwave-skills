# Step 1：设计模式 — 创建新 Skill

> **前置条件：** 用户提供了 skill 名称和简要职责。
> **产出：** SKILL.md + skill.json + CHANGELOG.md。

---

## ❌ 质量红线（设计模式）

> **❌D1 是 Popwave Skill 的 top1 红线。所有产出的 skill 都必须在自己的 SKILL.md 中包含此红线。**

| # | 红线 |
|:-:|:-----|
| ❌D1 | **产出 skill 必须包含读取协议红线** — 创建的 skill 的 SKILL.md 第一屏必须写明：`❌ 读取 skill 文件禁止用 Read 工具 — 用 skill_view 或 Get-Content -Encoding UTF8 -Raw`。这是 Popwave 所有 skill 的 top1 红线，不可省略 |
| ❌D2 | frontmatter 超过 4 行 — 只保留 name + description |
| ❌D3 | description 不是触发式 — 必须含"当用户说…时启用"或"Invoke when…" |
| ❌D4 | 质量红线不在第一屏 — ❌/✅ 格式必须第一屏可见 |
| ❌D5 | 红线用定义式 — 改为命令式（"❌ 不准…"而非"P0/P1/P2 分类"） |
| ❌D6 | 无 WRONG 错误示例 — 至少 1 个 ❌ WRONG + ✅ CORRECT 对比 |
| ❌D7 | 正文深层嵌套 — 拍平为 3-6 步扁平框架 |
| ❌D8 | 用第二人称 — "You should…"改为祈使句 |
| ❌D9 | 红线是建议 — "❌ 低于 X 重写"而非"建议≥X" |
| ❌D10 | 速查表缺列 — 必须五列：步骤/操作/读什么/产出什么/门禁 |
| ❌D11 | SOP 步骤缺 I/O — 每步标：读什么/做什么/产出/❌门禁 |
| ❌D12 | 无落盘检查点 — 产文件型 skill 必须列逐条文件路径 |
| ❌D13 | 无越界检测 — 多 step skill 必须有跨步骤违规检测表 |
| ❌D14 | 缺消费关系行 — 有消费者的 skill 必须标注消费关系 |
| ❌D15 | **重要行为无 SOP/模板约束** — skill 中的关键产出环节（搜索、生成选项、质检、推导等）必须有对应的 SOP（references/）或模板（templates/）约束质量。不能只有一句"agent 生成 X"就完事 — 必须告诉 agent "怎么生成好的 X"。SOP 约束过程质量，模板约束产出格式和质量标准 |

---

## Skill 是什么

Skill = SKILL.md（人读指令）+ skill.json（机器元数据）+ 可选 scripts/templates/references。

合格 Skill 回答三个问题：**什么场景用？能产出什么/不能产出什么？Agent 用前做什么准备？**

---

## 双文件结构（强制）

```
my-skill/
├── SKILL.md          ← 人读：全部指令、上下文、方法论
├── skill.json        ← 机读：平台元数据
├── CHANGELOG.md      ← 变更历史
├── steps/            ← 可选：分步执行指令（执行层）
├── references/       ← 可选：知识层 — 读后理解，指导操作（SOP、规范、参考文档）
├── templates/        ← 可选：模板层 — 复制填充，直接产出（空模板、示例模板）
└── examples/         ← 可选：范例数据
```

### references/ vs templates/ 定位区别

| 目录 | 定位 | 使用方式 | 典型文件 |
|:-----|:-----|:---------|:---------|
| `references/` | 知识层 — 读后理解 | 阅读理解，指导操作 | 搜索SOP、调用规范、设计原理、错误清单 |
| `templates/` | 模板层 — 复制填充 | 复制→填充→产出文件 | 空白模板、完整示例、输出格式骨架 |

❌ 不放 README.md。❌ 不另放 docs/ 目录。❌ 模板文件不放 references/（放 templates/）。❌ SOP 文件不放 templates/（放 references/）。

### 文件拆分原则

> 拆分的核心判断：**拆了是否减少 token 浪费 + 注意力损耗**。拆错 = 每次多一次工具调用 + 上下文切换 + 注意力断点。

#### references/templates（知识层/模板层）— 按需拆 ✅

| 拆分信号 | 示例 |
|:---------|:-----|
| 只在特定步骤查阅 | 爽点追问链只在 Phase 2b 用，搜索 SOP 只在 Step 2.1 用 |
| 按条件加载不同内容 | 7 类爽点追问链，每次只查对应的 1-2 个 |
| 内容是独立的知识单元 | 质量标准、调用规范、错误清单各自独立 |

**原则**：references/ 和 templates/ 的文件越细越好 — agent 只在需要时读对应文件，不拆 = 每次全读浪费 token。

#### steps/（执行层）— 按独立阶段拆，不按步骤拆 ⚠️

| 该拆 ✅ | 不该拆 ❌ |
|:--------|:----------|
| 有用户确认断点（天然分水岭） | 连贯推导链中间硬切 |
| 两个阶段彼此独立（输入/产出不依赖） | 两个阶段必须顺序执行且共享上下文 |
| 一个阶段可以反复执行（如研究阶段可多轮） | 一次性线性流程 |

**行数约束**：
- references/templates：无硬上限，按知识单元自然拆分
- steps/：目标 50-150 行/文件。超 150 行时检查是否能按用户断点拆分。**不设硬上限** — 连贯推导链拆碎反而有害（每次工具调用 = token 开销 + 注意力断点）

**拆分决策流程**：
```
step 文件 > 150 行？
  ├─ 否 → 不拆
  └─ 是 → 内部有用户确认断点？
       ├─ 是 → 按断点拆（断点前一个文件，断点后一个文件）
       └─ 否 → 有可下沉到 references/ 的知识层内容？
            ├─ 是 → 下沉，step 文件保留执行流程
            └─ 否 → 不拆（连贯推导链保持一个文件）
```

**反面案例**：
- ❌ 把 9 步推导链拆成 9 个文件 → agent 走 9 步读 9 个文件 = 9 次工具调用 + 9 次上下文切换
- ❌ 把 7 类追问链留在 step 文件里 → 每次走 step 都全读 7 个，但实际只用 1-2 个
- ✅ 把 7 类追问链下沉到 references/ → 只在 Phase 2b 时查对应的 1-2 个
- ✅ 把 9 步推导链按 Step 3 用户断点拆成 2 个文件 → research（Step 1-2）+ derive（Step 3-9），agent 走完 research 自然暂停等用户

---

## skill.json 规格

| 字段 | 必填 | 说明 |
|------|------|------|
| `id` | ✅ | 唯一标识，与目录名一致 |
| `version` | ✅ | 语义化版本号 |
| `displayName` | ✅ | 中文显示名 |
| `description` | ✅ | 触发条件式描述 |
| `entry` | ✅ | 固定 `"SKILL.md"` |
| `activation.slashCommands` | ✅ | 触发命令数组 |
| `permissions` | ✅ | 权限声明 |

### skill.json 示例

```json
{
  "id": "my-skill",
  "version": "1.0.0",
  "displayName": "我的技能",
  "description": "当用户说'做X/做Y'时启用。产出来物供给下游管线。",
  "entry": "SKILL.md",
  "activation": {
    "slashCommands": ["my-skill", "做X"]
  },
  "permissions": {
    "readProjectFiles": true,
    "writeProjectFiles": true
  }
}
```

---

## frontmatter 规范

SKILL.md 开头 YAML frontmatter **不超过 4 行**：

```yaml
---
name: my-skill
description: "当用户说'做X/做Y'时启用。产出来物供给下游管线。"
---
```

❌ 不在 frontmatter 放 version/tags/category/orchestration/dependencies/produces/display_name。全部移入 skill.json 或正文。

---

## description 写法

```
❌ 差：description: "用户调研工具"
❌ 差：description: "五模式设计：模式A→B→C→D→E"
✅ 好：description: "网文作者社区用户调研。Invoke when user needs to research opinions across Chinese web novel communities."
```

---

## SKILL.md 内容组织（推荐顺序）

```
# 标题
> 一句话摘要

## ❌ 质量红线              ← 第一屏必须出现，第一条必须是读取协议
## 什么时候使用 / Triggers
## 前置条件（可选）
## 速查表（全文件目录引导）
## 核心流程（3-6步，扁平）
## ❌ 错误示例（WRONG 区块）
## 验收清单
## 异常与边界条件
## 版本（指向 CHANGELOG.md）
```

### 质量红线第一屏模板

产出的 skill 的红线区块**必须以读取协议开头**：

```markdown
## ❌ 质量红线

| # | 红线 |
|:-:|:-----|
| ❌1 | **读取 skill 文件禁止用 Read 工具** — 用 `skill_view` 或 `Get-Content -Encoding UTF8 -Raw`，Read 有行数限制会截断 |
| ❌2 | {该 skill 的业务红线} |
| ... | ... |
```

### 速查表 = 全文件目录引导

产出的 skill 的速查表**不只是模式路由**，而是整个 skill 文件夹的文件索引。让 agent 一看速查表就知道每个文件什么时候读：

```markdown
## 速查表（文件目录引导）

| 我要 | 读什么文件 | 什么时候读 | 产出 |
|:-----|:----------|:----------|:-----|
| {操作A} | `steps/step-1-xxx.md` | {触发条件} | {产出物} |
| {操作B} | `steps/step-2-xxx.md` | {触发条件} | {产出物} |
| {查规范} | `references/xxx.md` | {触发条件} | — |
| {填模板} | `templates/xxx.md` | {触发条件} | {产出文件} |
```

### 三层架构原则

| 层级 | 职责 | 文件 | 行数目标 |
|:-----|:-----|:-----|:---------|
| 路由层 | 告诉 agent "走哪条路" | SKILL.md | ≤60 行 |
| 执行层 | 该模式的完整操作指令 | steps/step-N.md | 50-150 行/文件 |
| 知识层 | 方法论、规范参考（读后理解） | references/ | 按需加载 |
| 模板层 | 空模板、示例（复制填充产出） | templates/ | 按需加载 |

**SKILL.md 只做路由。** 红线/错误/边界条件/方法论全部下沉到 steps/ 或 references/。模板文件放 templates/。

---

## 速查表（强制五列）

| 步骤 | 操作 | 读什么 | 产出什么 | ❌门禁 |
|:-----|:-----|:-------|:---------|:-------|
| 1 | 读取配置 | `config.yaml` | 配置对象 | 文件不存在 → 终止 |
| 2 | 执行分析 | 上一步产出 | 分析报告 | — |

「读什么」列必须是文件路径。

---

## SOP 步骤标注（强制 I/O）

每步必须标：

```markdown
### 步骤 N：{步骤名}

**读什么：** {文件路径或上一步产出}
**做什么：** {操作描述}
**产出：** {产出物}
**❌ 门禁：** {不满足条件时的处理}
```

---

## 落盘检查点

| 确认项 | 状态 |
|:-------|:----:|
| `{skill-id}/SKILL.md` 已写入 | [ ] |
| `{skill-id}/skill.json` 已写入 | [ ] |
| `{skill-id}/CHANGELOG.md` 已写入 | [ ] |
| `{skill-id}/steps/` 目录存在（多步骤 skill） | [ ] |
| `{skill-id}/references/` 存在（需方法论支撑） | [ ] |
| `{skill-id}/templates/` 存在（需模板文件） | [ ] |

---

## 异常与边界条件

| 场景 | 触发条件 | 处理动作 |
|:-----|:---------|:---------|
| 文件/依赖缺失 | 路径无效 | 告知用户，**不准编造数据** |
| 外部工具不可用 | 工具未安装 | 降级方案 |
| 用户中途改变需求 | 用户改变指令 | 暂停当前流程，确认后继续 |
| 子 agent 启动失败 | 子进程错误 | 手动执行 + 红线自检 |
| skill.json 缺失 | 新建时未创建 | 必须补建，不能只有 SKILL.md |

---

## ❌ WRONG 示例

```
❌ WRONG: 创建 skill 时只写 SKILL.md 不写 skill.json → 平台无法注册机器元数据
✅ CORRECT: 双文件结构强制：SKILL.md + skill.json 同时创建

❌ WRONG: description 写成"用户调研工具"（只说做什么，不说何时触发）
✅ CORRECT: "当用户说'调研/社区/什么火'时启用。产出调研报告供给下游管线。"

❌ WRONG: SKILL.md 塞了红线+错误示例+边界条件+方法论+版本历史，200+行
✅ CORRECT: SKILL.md ≤60行只做路由，执行细节下沉到 steps/，知识下沉到 references/

❌ WRONG: 产出的 skill 红线第一条是"frontmatter 不超过4行" → agent 用 Read 工具读文件被截断
✅ CORRECT: 产出的 skill 红线第一条必须是"禁止用 Read 工具读取 skill 文件"，用 skill_view / Get-Content -Raw

❌ WRONG: 速查表只列了模式路由（A/B/C/D），没列 references/ 文件 → agent 不知道什么时候该查参考
✅ CORRECT: 速查表是全文件目录引导，steps/ 和 references/ 和 templates/ 的每个文件都列出读取时机

❌ WRONG: 把空模板文件放在 references/ 里 → agent 误以为是阅读理解的规范文档
✅ CORRECT: 模板文件放 templates/（复制填充产出），SOP/规范放 references/（读后理解指导操作）
```

---

## 创建流程

1. 向用户确认 skill 名称和职责（Q&A 流程，不准跳过）
2. 创建目录 `{skill-name}/`
3. 创建 `SKILL.md`（按内容组织顺序，≤60 行）
   - **红线第一条必须是读取协议**：`❌ 读取 skill 文件禁止用 Read 工具 — 用 skill_view 或 Get-Content -Encoding UTF8 -Raw`
   - **速查表必须是全文件目录引导**：列出 steps/ 和 references/ 的每个文件及读取时机
4. 创建 `skill.json`（按规格）
5. 创建 `CHANGELOG.md`（初始 v1.0.0）
6. 如有 steps/references 需求，创建对应目录
7. 对照落盘检查点逐项验证
8. **验证读取协议**：确认产出的 SKILL.md 第一屏红线第一条是读取协议
9. 输出创建完成报告（文件路径列表）
