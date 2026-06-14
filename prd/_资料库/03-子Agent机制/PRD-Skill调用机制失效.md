# PRD-Skill调用机制失效

> 来源：飞书文档 | [原文链接](https://n0mqbh938qa.feishu.cn/wiki/BYPwwxC8HilzWGkeKrWcoGucntc)
> 同步时间：2026-06-14 | doc_id: Q2N4dGearonNeexqHBtctflAn7d | rev: 9

# PRD：Paopao Skill 加载机制审计与修复方案

> 版本：v4.0 | 2026-06-09  
> 来源：6-9测试项目全量 47 次 run 的 input.json + events.jsonl 全量分析 + thinking 链深度审计  
> 状态：待执行

---

## 一、问题简述

线管纪律问题（ch011-015 跳过 Design 文件、bookstrap 跳过多个 phase）经过四轮迭代审计，根因逐步收敛。

**v3.0 结论是 "steps/\*.md 不在 system prompt 里"——对但不完整。** v4.0 通过 events.jsonl 的 thinking 链 + tool_calls 全量分析，发现了两层更深的根因：

1. **Manual Read 不是 "50% 执行"——是 50% 截断。** Read 工具输出的子 skill 文件只拿到 \~50% 内容。Agent 拿到的是一份残缺的指令。
2. **长会话惰性侵蚀。** ch011-014 五轮连续零次 Read 子 skill 文件。Agent 切换到 "全凭记忆写" 模式。
3. **ch015 即使 writer 在 system prompt 里，design 文件仍缺失。** 因为输出路径指令在 step-1-design.md 里，不在 SKILL.md 主文件里——System prompt 注入也不够。

---

## 二、证据链

### 证据 1：Paopao 的 Skill 架构（来自 input.json）

```
input.json 结构:
  ├── skills: [{name, path}]        ← 本轮注入的 skill 列表
  ├── prompt: (完整文本)            ← 组裝后发给 DeepSeek 的最终 prompt
  ├── input: {instruction, skillNames, ...}
  ├── project: {id, name, folderPath, ...}
  ├── injectedHistoryTurns: {N}     ← 注入的历史轮数
  └── outputPath / openClawSessionId

prompt 内部结构（以 ch015 为例，26,870 字符）:
  char 0-882:      Paopao 基础指令
  char 882-1273:   对话历史（16 轮注入）
  char 1273-1300:  "Local Skill instructions:" 分隔符
  char 1300-4858:  pop-novel-writer SKILL.md 全文（3,558 chars · 完整注入）
  char 4858-26870: expert-writer SKILL.md 全文（22,012 chars · 完整注入）
  末尾:            User instruction: "/pop-novel-writer 写ch15"
```

**Paopao 没有 `Skill()` 工具——Skill 通过 system prompt 注入。注入是完整展开的，不存在 "只挂名称" 的情况。**

### 证据 2：47 次 run 的 skill 注入分布

| 阶段 | run 次数 | 注入的 skill | 触发方式 |
|-|-|-|-|
| 开书 | 2 | [bookstrap, expert-writer] | 用户 `/pop-novel-bookstrap` |
| 全部中间流程 | 44 | [expert-writer] | "继续下一章" / "补全文档" |
| ch015 演示 | 1 | [writer, expert-writer] | 用户手动 `/pop-novel-writer` |

**writer 的 SKILL.md 只有 2/47 次通过 system prompt 注入。其余 44 次靠 agent 手动 Read。**

### 证据 3：expert-writer 自身加载——8/8 满分

8 次随机抽样覆盖全部类型（开书/补全/ch产出/继续/gap分析），满分通过：

```
expert-writer SKILL.md 完整性: 5/5 × 8 轮
  ✅ 纪律与异常协议（§0）
  ✅ 路由表（3.1 Think · 意图识别）
  ✅ Think 层（需求审视 + 进度读取）
  ✅ Reflect 层（四层递进审视）
  ✅ 决策点闸门（3.2 Execute）
```

### 证据 4：Read 工具输出严重截断——只拿到 \~50%

子 skill 文件通过 Read 工具读取后的实际输出 vs 源文件大小：

```
文件                       源文件大小    Read 输出    完整度
─────────────────────────────────────────────────────────
writer SKILL.md             5,915 chars → 2,829 chars   48%
step-1-design.md           13,561 chars → 6,734 chars   50%
step-2-render.md            8,791 chars → 4,546 chars   52%
step-5-state-update.md      6,398 chars →   940 chars   15%
step-3-state-update.md      (文件不存在) → 215 (error)   —
```

**System prompt 注入的 expert-writer（22,012 chars）100% 完整。Manual Read 的子 skill 文件平均只拿到 \~50%。Agent 在残缺的指令下执行。**

### 证据 5：ch001-009 正常 vs ch011-014 惰性——分水岭在 thinking 链

**正常轮次（如 ch001-009）**：每轮读取 writer SKILL.md + step-1/2/5 → Design 文件正确产出。

**惰性轮次（ch011-014）**——来自 events.jsonl thinking 链的完整记录：

```
ch010 (51d5192c) thinking:
  "用户说继续下一章...但他们在做gap分析..."
  "我先检查ch010有什么——有design文件！"        ← 关键转折
  → Read(ch010-design.md) + Read(act-01.yaml)
  → Write(ch010.md)
  → 全程没有 Read(writer/SKILL.md)

ch011 (36126d85) thinking:
  "用户要ch011...有没有design文件？"
  "没有design文件"                              ← 但已经形成了跳过惯性
  → Read(act-01.yaml)  ← 只读了幕纲
  → Write(ch011.md)
  → 全程没有 Read(writer/SKILL.md)

ch012-014 (42b94539, a51cb898, a50f8086):        ← 三连零读取
  全部: Read(act-01.yaml) → Write(chXX.md)
  全部: 零次 Read(writer/SKILL.md) 或任何 step 文件
```

**根因链**：ch010 有一个预存的 design 文件（beae49b2 开书阶段顺手产的）→ agent 断定 "不需要走 Design 流程" → 跳过整个 writer 管线 → 形成惯性 → ch011-014 连续五轮不读 writer 的任何规范文件。

### 证据 6：ch015 即使 writer 在 system prompt 里——design 仍缺失

ch015 你手动 `/pop-novel-writer` 触发，writer SKILL.md **在 system prompt 里**（完整 3,558 chars）。但产出结果：

```
✅ 03-正文/ch015.md 已创建
✅ 章末状态更新块完整（style_report + entity_updates + event_log）
❌ 03-写作资产/ch015-design.md 未创建
```

**即使 system prompt 里有 writer SKILL.md，质量红线#3 写着 "Design 必须输出事件链"，agent 仍然跳过了 Design 文件持久化。** 因为输出路径 `03-写作资产/chXXX-design.md` 不在 SKILL.md 主文件的任何一行——它在 step-1-design.md 的最后一行。System prompt 注入只覆盖了 SKILL.md 主文件，不覆盖 steps/ 子文件。

---

## 三、真实根因（v4.0 收敛）

### 三个根因，两层修复

**根因一：Manual Read 输出截断——指令是残缺的**

Read 工具对子 skill 文件的输出被截断到 \~50%。Agent 拿到的不是 "完整的执行规范"，是 "执行规范的前一半"。聚合算法、输出路径、硬性约束可能全在后一半。

**根因二：长会话惰性侵蚀——agent 不再路由到子 skill**

Expert-writer 的 Think 框架在长会话中被压缩成 "检查文件是否存在" 而非 "检查应该用什么管线执行"。当 ch010 已有 design 文件 → agent 以为不用走 writer → 接下来连续五轮不读 writer 的 SKILL.md。Think→Execute→Reflect 变成了 Think(文件在吗?)→直接写。

**根因三：System prompt 注入也不够——关键输出指令在 step 子文件里**

即使 writer SKILL.md 完整在 system prompt 里（ch015），关键输出路径仍在孙文件层。SKILL.md 说 "详细指令 → steps/step-1-design.md"，但那个文件的内容不在 prompt 里。Agent 看到了引用但不一定去追。

**Summary**：

```
System prompt 注入 = 100% 完整 + 每轮必在 + 无自主跳过权
Manual Read        = ~50% 截断 + 可选(ch011-014直接跳过) + 长会话惰性侵蚀
System prompt       = 100% 完整 + 但只覆盖主文件(steps/不在内)
```

---

## 四、解决方案

### 4.1 P0：关键输出路径从 step 子文件提升到 SKILL.md 主文件

**原则**：SKILL.md 主文件里的内容会被 system prompt 注入。每个 step 的**输出文件路径**和**硬性产出约束**必须在主文件可见——不管 agent 以后是通过 system prompt 还是 Manual Read 拿到的，都能看到。

**此方案的增量修复（2026-06-10）：expert-writer 层面已落地。** 见下文 §4.6。

**影响文件**：

| Skill | 改动 |
|-|-|
| `pop-novel-writer/SKILL.md` | Step 1 增加输出路径 + Step 2 增加输出路径 + Step 3 增加输出路径 |
| `pop-novel-bookstrap/SKILL.md` | Phase 产出清单（主文件可见） |
| `pop-novel-plot/SKILL.md` | Step 产出清单（主文件可见） |

**Writer SKILL.md 改动示例**：

```markdown
## 管线（3步驱动）

Step 1 — Design（LLM · 产出八块 chXXX-design.md）
  ★ 输出文件: 03-写作资产/chXXX-design.md（必须持久化到磁盘，不可只口头汇报）
  每章必须产出独立的 design 文件，不得复用上一章的 design
  详细指令 → steps/step-1-design.md

Step 2 — Render（LLM / 三阶段）
  ★ 输出文件: 03-正文/chXXX.md
  ★ 章末必须附带 # === 状态更新 === 块（entity_updates + world_updates + event_log + style_report）
  详细指令 → steps/step-2-render.md

Step 3 — State Update（零 LLM）
  ★ 输出文件: 00-总控/entity-snapshot.yaml（覆盖写入·从所有章 delta 聚合）
  详细指令 → steps/step-5-state-update.md
```

### 4.2 P0：质量红线增加持久化检查

```markdown
| ❌10 | **Design 文件已写入磁盘** — 03-写作资产/chXXX-design.md 存在且非空 | [ ] |
| ❌11 | **Entity-snapshot 已更新** — 00-总控/entity-snapshot.yaml 被覆盖写入 | [ ] |
```

### 4.3 P1：expert-writer Think 层增加任务类型切换硬性规则

**问题**：agent 从非创作类（诊断/修订）切换到创作类（写正文）时，Think 被压缩为 "检查文件是否存在" 而非 "检查应该用什么管线执行"。

**改动文件**：`expert-writer/SKILL.md` §3.1 Think

```markdown
**第三步：任务类型切换检查（v2.3 新增）**

当本轮 tasks 类型与上一轮不同（诊断→写作 / 修订→写作 / 补全→写作），强制执行：
  □ 重新进入完整 Think 流程——不得因 "已有相似产出" 跳过
  □ 重新 Read 目标子 skill 的 SKILL.md + 全部 steps/*.md
  □ 重新验证前置条件（管线前置校验 §3.1.6）
  □ 理由：任务类型切换意味着管线上下文完全不同。上一轮的捷径
    （如 "design文件已存在，直接写"）在本轮不适用。

检测方式：
  上一轮 tasks = "诊断·gap分析"
  本轮 tasks = "继续下一章" → 类型不匹配 → 强制完整路由
```

### 4.4 P1：expert-writer §0 增加 Skill 加载完整性协议

**改动文件**：`expert-writer/SKILL.md` §0

```markdown
| 0.8 | **路由到子 skill 后 steps 加载不完整** | agent 在 Read 子 skill 的 SKILL.md 后，必须再 Read 该 skill 的全部 steps/*.md。不得只读主文件。若 Read 工具输出被截断 → 用 offset 参数续读，直到全部内容加载完毕。 |
```

**2026-06-10 增量升级为 §0.8\~0.10**：见下文 §4.6。

### 4.5 P2：Paopao 注入 skill 时附带 steps/ 文件内容

当前 system prompt 注入：

```
--- skill: /pop-novel-writer ---
(SKILL.md 正文结束)
--- skill: /写作专家 ---
```

目标：skill 注入时追加 steps/ 清单和关键内容摘要：

```
--- skill: /pop-novel-writer ---
(SKILL.md 正文结束)

This skill requires reading these step files:
  steps/step-1-design.md (13,561 chars) — 八块 Design 模板 + 输出路径
  steps/step-2-render.md (8,791 chars) — 风格锚定三阶段
  steps/step-5-state-update.md (6,398 chars) — 聚合算法 + entity-snapshot 格式

Critical output paths (must be persisted to disk):
  03-写作资产/chXXX-design.md ← Step 1
  03-正文/chXXX.md            ← Step 2
  00-总控/entity-snapshot.yaml ← Step 3
--- skill: /写作专家 ---
```

### 4.6 ★ 2026-06-10 增量修复：expert-writer 三层强制读完整

> 原方案(4.1\~4.4)倾向于在 Paopao 应用层/各子 Skill 层修复。本次仅从 expert-writer 元 Skill 层面修复，改动最小。

**改动文件**：`d:\popwave-skills\skills\expert-writer\SKILL.md`

#### 改动一：§0.8→§0.9 合并为通用规则

**旧版（§0.8+§0.9+§0.10）→ 新版（§0.8+§0.9）**。

旧版区分了三类文件（steps/\*.md、SKILL.md 主文件、路由前验证），每类各自写一条。新版合并为一条通用规则：

| # | 场景 | 强制行为 |
|-|-|-|
| **0.8** | Skill 目录中的文档文件被截断 | 技能目录中所有文档型文件（SKILL.md、steps/*.md、phases/*.md、templates/*.md、references/*.md、README.md 等），只要 Read 了就必须读完整 |
| **0.9** | 路由前未验证完整性 | Execute 阶段第①步后，确认已读所有文档型文件完整 |

**合并理由**：

- 审计证据表明截断是系统性的（bookstrap SKILL.md 22.8%、模板 6-17%、94B README 42.6%），不是某类文件的特例
- "区分指令文件和参考文档"在实践中难以操作，agent 不知道边界在哪
- 一条通用规则比三条分类规则更容易被 agent 理解和执行

**检测与续读方法（通用，不变）**：

1. Read 返回后检查最后一行行号
2. 如果行号为 \~250（接近 Read 工具的行数上限），说明可能被截断
3. 必须用 `Read(path, offset=200)` 发起第二轮确认
4. 如果第二轮返回内容从行号 200+ 开始且有内容 → 确认被截断，继续 `offset=400/600` 分段读取直到返回为空
5. 仅当返回为空时才确认文件已全部读完

#### 改动二：§3.2 Execute — 路由校验步骤②更新语言

旧版：

```
② 前置文件完整性验证（NEW — 见 §0.10）
   → 检查当前 context 中该子 skill 的 SKILL.md 是否完整（未被截断）
   → 检查其所有指令子文件（steps/*.md / phases/*.md 等）是否已全部 Read 完毕
```

新版（2026-06-10 v2）：

```
② 子 skill 文件完整性验证（NEW — 见 §0.9）
   → 检查 context 中该子 skill 的 SKILL.md + 其他已 Read 的文档型文件是否完整
   → 不完整 → 退回重新 Read 续读
```

#### 改动三：§3.1.6 管道前置校验 — 步骤③更新语言

旧版区分"SKILL.md"和"指令子文件"，新版合并为一句话："已 Read 当前路由目标子 skill 的完整 SKILL.md + 全部文档型文件（未被截断）"

#### 改动四：§3.1 Think 任务类型切换检查

旧版写"全部指令子文件"，新版改为"全部文档型文件（steps/*.md、phases/*.md、templates/\*.md 等）"

#### 方案评价

- **一条规则代替三条**：不再区分"主文件 vs 步骤文件 vs 指令文件 vs 参考文档"——凡是 skill 目录里的文档文件，读了就必须读完
- **覆盖审计发现的所有截断场景**：SKILL.md 主文件（22.8%）、模板文件（6-17%）、README.md（42.6%）都归 §0.8 保护

### 4.7 ★ 2026-06-10 增量修复：「继续任务」意图识别补全

**问题**：路由表"继续前进"行的典型说法中没有「继续任务」这4个字。Agent 无法匹配到"继续前进"意图 → 落入"不属于创作范畴"分支 → 自由回复，不唤起任何 Skill。

同时，"继续前进"固定使用 `think-正文写作.md` 审视框架——但说"继续任务"时可能发生在管线任意阶段（拆书/开书/写作），写正文的审视框架对非写作阶段不可用。

**改动**：`expert-writer/SKILL.md` §3.1 意图识别表

```
旧:
| 继续前进 | 「继续」「下一章」「往下写」「接受目前的方案」「可以」 | think-正文写作.md | 项目状态扫描 → 路由 |

新:
| 继续前进 | 「继续」「继续任务」「继续写」「下一章」「往下写」「接受目前的方案」「可以」 | —（无固定审视框架，直接读 progress 判定路由） | 读 progress → last_completed_skill + next_skill 路由 → 无数据则回退项目状态扫描 |
```

**核心变化**：

1. 新增「继续任务」「继续写」到典型说法
2. 审视框架从固定的 `think-正文写作.md` 改为无固定框架——"继续任务"不需要审视框架，直接读进度表判定路由
3. 执行路径从"项目状态扫描"改为优先读 workspace-index.yaml#progress 的 last_completed_skill / next_skill / checkpoints（这条数据本来就在 Think step 1 读入了，只是路由表之前没引用）

**why not 开书设定**：审视框架选 `think-开书设定.md` 也覆盖不全。正确的做法是"有进度读进度，无进度回退扫描"——避免任何固定审视框架对"继续任务"场景的误匹配。

---

## 五、排查技巧沉淀

### 5.1 项目产出物在哪里

```
{项目}/00-原始设定/     ← L1 六件套 + 深度展开 + 稳定性检验
{项目}/00-总控/         ← project.yaml / constitution.yaml / 数值体系 / entity-snapshot
{项目}/02-大纲/设计/    ← Plot Canvas（里程碑/情节线/人物/地图/势力/装备）
{项目}/02-大纲/设计/幕/ ← act-01.yaml + Canvas 子文件
{项目}/03-写作资产/      ← chXXX-design.md（八块设计包）
{项目}/03-正文/         ← chXXX.md（正文 + 章末状态更新块）
{项目}/_参考书分析/     ← 对标分析结果
```

### 5.2 输入/输出原始信息在哪里（完整度最高）

**runs 目录**——信息最完整：

```
{项目}/.paopao/projects/{项目名}/runs/{run_id}/
├── input.json     ← ★ 完整 prompt（发给 DeepSeek 的最终文本）
│    ├── prompt:        system + skill + history + 用户指令（全部组裝好的文本）
│    ├── skills:        本轮注入的 skill 列表及路径
│    ├── input:         用户指令元数据（instruction, skillNames, model 等）
│    ├── project:       项目信息
│    └── injectedHistoryTurns: 注入的历史轮数
│
├── response.md    ← DeepSeek 返回的最终 assistant 可见文本
│
└── events.jsonl   ← 流式事件
     ├── thinking delta:   agent 的思考过程（完整思维链）
     ├── tool-call:        工具调用（Read/Write/Exec 的 input）
     ├── tool-result:      工具返回（Read 的输出内容 + 截断标记）
     └── file-change:      文件变更记录（create/update + diff）
```

**排查顺序**：

1. `input.json#prompt` → 本轮 system prompt 的完整内容（skill 有没有、版本对不对）
2. `input.json#skills` → 本轮注入的 skill 列表及版本路径
3. `events.jsonl` → agent 的完整 thinking 链 + 所有 tool calls + Read 输出大小（判断截断）
4. `response.md` → 最终输出
5. `input.json#prompt` 对比 `D:\popwave-skills\` 源码 → 确认注入的版本是否是最新的

**Conversations 目录**（对话摘要·适合快速浏览·缺 system prompt）：

```
{项目}/.paopao/projects/{项目名}/conversations/{conv_id}.jsonl
每行一条消息：user + assistant(content + events摘要)
```

### 5.3 Skill 定义在哪里

| 位置 | 内容 | 何时更新 |
|-|-|-|
| `D:\popwave-skills\skills\{skill-id}\` | 源码（你手动编辑） | 你手动改 |
| `C:\Users\AWMPRO\AppData\Roaming\paopao\remote-skills\{skill-id}\{version}\` | 缓存（Paopao 实际加载） | Paopao 自动同步 |

**排查技巧**：

- `input.json#skills[].path` → 确认本轮从哪个路径加载、哪个版本
- 对比源码 `D:\popwave-skills\` 和缓存 `remote-skills\` 内容是否一致
- 改了源码但缓存没更新 → Paopao 用的还是旧版

### 5.4 如何判断 Read 工具是否截断了子文件

```python
# 从 events.jsonl 提取
tool-call: {toolName: "read", input: {path: ".../SKILL.md"}}
tool-result: {toolName: "read", output: "..."}

# 对比
实际文件大小 vs Read output 长度 → 48-52% = 被截断
100% = 完整读取
output 中包含 "(truncated)" = 显式截断标记
```

---

## 六、修复文件定位

| # | 优先 | 文件 | 改动 |
|-|-|-|-|
| 1 | P0 | `pop-novel-writer/SKILL.md` | 每个 Step 描述增加 ★ 输出文件路径 + 质量红线#10/#11 |
| 2 | P0 | `pop-novel-bookstrap/SKILL.md` | Phase 产出清单路径在主文件可见 |
| 3 | P0 | `pop-novel-plot/SKILL.md` | Step 产出清单路径在主文件可见 |
| 4 | P1 | `expert-writer/SKILL.md` §3.1 | 任务类型切换检查——诊断→写作时强制完整路由 |
| 5 | P1 | `expert-writer/SKILL.md` §0 | 增加 §0.8：子 skill steps 文件加载完整性协议 |
| 6 | P2 | Paopao 应用层 | skill 注入时在 SKILL.md 正文后追加 steps 路径清单 + 输出路径摘要 |