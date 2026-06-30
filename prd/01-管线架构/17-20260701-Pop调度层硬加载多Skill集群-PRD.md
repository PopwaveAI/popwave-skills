# PRD: Pop 调度层硬加载多 Skill 集群

> 创建日期：2026-07-01
> 状态：待确认
> 分类：管线架构
> 关联：expert-writer / pop-writer-v3-seed / world-foundation / plot / create

## 背景

项目 D 在 seed → world → plot → create 的连续运行中暴露出一个架构问题：`expert-writer` 被 Pop 程序层硬加载，但 seed/world/plot/create 等执行 skill 依赖 expert 的 prompt 软路由。结果是 agent 可能知道“应该调用某 skill”，但实际没有加载执行 skill，也仍然能继续写入正式产物。

这不是单个 prompt 写得不够严的问题，而是调度层没有把“路由意图”升级为“硬加载机制”。

## 问题

### P0: 子 skill 软路由导致裸跑

当前链路：

```text
用户请求
  → Pop 硬加载 expert-writer
  → expert-writer 用自然语言要求读取目标 skill
  → agent 自行决定是否读 seed/world/plot/create
  → 即使未读，也可能继续写正式产物
```

风险：

- create 可以不加载 `pop-writer-v3-create` 就写正文。
- world 可以只读部分 world skill，直接补齐 L1 文件。
- expert-writer 会从“调度器”滑成“全能执行器”。
- 产物回报里写“严格来自/按流程执行”，但 run 证据无法支持。

### P1: 文档存在被误判为执行完成

目前许多门禁只检查“产物文件是否存在”，没有检查：

- 目标 skill 是否硬加载。
- step 文件是否完整读取。
- 必要输入是否齐全。
- 产物是 formal / draft / trial 哪种模式。

因此 “文件存在” 会被误判为 “流程完成”。

### P1: 正式产物缺少机器可核验凭证

正文/幕纲/PRD 等产物可以自称“按流程生成”，但缺少统一 `execution` 元数据记录：

```yaml
execution:
  mode:
  loaded_skills:
  loaded_steps:
  required_inputs:
    present:
    missing:
```

这导致后续复盘只能人工翻 runs，而不能由程序快速判定产物可信度。

## 证据链

### 证据 1: create run 只注入 expert-writer

项目 D 的正文 run 中，`input.json` 显示注入的 skill 为：

```text
Skills: /expert-writer
```

未看到 `pop-writer-v3-create` 被 Pop 调度层硬注入。

涉及 run 示例：

```text
C:\Users\AWMPRO\.paopao\projects\6-30-项目d\runs\c76a141a-765b-4e07-ae96-9ca45f31ecea
C:\Users\AWMPRO\.paopao\projects\6-30-项目d\runs\534add32-1db3-496e-a944-7dfc1216c1c7
```

### 证据 2: create 实际未读取 create skill

ch003/ch004 的 `events.jsonl` 显示 agent 直接从幕纲/对话历史中提取章节设计并写正文，没有看到读取：

```text
D:\popwave-skills\skills\pop-writer-v3-create\SKILL.md
D:\popwave-skills\skills\pop-writer-v3-create\steps\step-1-create.md
D:\popwave-skills\skills\pop-writer-v3-create\templates\创作-模板.md
```

但产物仍然落入：

```text
C:\Users\AWMPRO\AppData\Roaming\popwave\paopao-workspace\projects\6-30-项目d\正文\
```

并在回报中被称为正文完成。

### 证据 3: world 阶段只读了 world skill 前段就批量补文件

world run 中存在明确轨迹：

```text
读取 pop-writer-v3-world-foundation/SKILL.md limit=50
agent 思考：虽然只读了前 50 行，但关键信息够了
随后批量写 L1 文件、金手指、文风DNA
```

涉及 run：

```text
C:\Users\AWMPRO\.paopao\projects\6-30-项目d\runs\416f47b6-0dbf-4c3b-ab84-d15902ff598c
```

结果是 `文风DNA.md` 被当作 L1 文件清单中的待补文件，而不是从文风库原件复制继承出来的正式风格资产。

### 证据 4: skill 层红线不足以阻止裸跑

`expert-writer` 已经写明：

```text
不要只凭 expert 自己的概述代替执行 skill
```

但实际 run 仍然发生裸跑。说明仅靠 skill prompt 约束不足以保证执行。

## 目标

| 优先级 | 目标 | 验收标准 |
| --- | --- | --- |
| P0 | Pop 调度层按意图硬加载目标执行 skill | 正文请求的 run input 同时包含 `expert-writer` + `pop-writer-v3-create` |
| P0 | 正式产物必须有执行凭证 | 正文/幕纲/PRD/world 产物包含 `execution.mode: formal` |
| P0 | 非 formal 不得落正式目录 | 未硬加载目标 skill 时，只能输出 trial/draft，不写 `正文/`、正式幕纲、正式 PRD |
| P1 | run metadata 记录硬加载 skill 和必读文件 | run 级 metadata 可查询 `requiredSkills`、`loadedSkills`、`requiredInputs` |
| P1 | 缺输入时自动降级 | 缺章级导演包/文风DNA/案例审计时 create 自动变为 draft |

## 方案

### 方案总览

```text
Skill 层：定义规则、入口门、出口门、execution 模板
Pop 调度层：根据用户意图硬加载 expert + 目标执行 skill
Run 层：记录 loadedSkills / loadedSteps / requiredInputs
写入层：根据 execution.mode 决定能否落正式目录
```

### 1. 意图识别与 requiredSkills

Pop 在构造 run input 前先做轻量意图分类：

| 用户意图 | requiredSkills |
| --- | --- |
| 开书、题材方向、新书PRD | `expert-writer`, `pop-writer-v3-seed` |
| 世界观、力量体系、金手指、文风DNA | `expert-writer`, `pop-writer-v3-world-foundation` |
| 剧情设计、幕纲、剧情单元卡 | `expert-writer`, `pop-writer-v3-plot` |
| 写正文、继续写第 N 章 | `expert-writer`, `pop-writer-v3-create` |
| 修改、审稿、润色、重写 | `expert-writer`, `pop-writer-v3-revise` |
| 单元复盘、记忆压缩、账本更新 | `expert-writer`, `pop-writer-v3-arc` |

run input 中应显式注入：

```yaml
requiredSkills:
  - expert-writer
  - pop-writer-v3-create
hardLoadedSkills:
  - expert-writer
  - pop-writer-v3-create
```

### 2. 子 skill 硬加载内容

硬加载不是只给 skill 名称，而是注入执行 skill 的核心入口：

```text
目标 skill/SKILL.md
目标 skill 声明的必要 step 文件
目标 skill 的输出模板
```

create 示例：

```text
skills/pop-writer-v3-create/SKILL.md
skills/pop-writer-v3-create/steps/step-1-create.md
skills/pop-writer-v3-create/templates/创作-模板.md
```

plot 示例：

```text
skills/pop-writer-v3-plot/SKILL.md
steps/step-0-scale-contract.md
steps/step-1-volume-anchor.md
steps/step-2-case-digest.md
steps/step-3-simulation.md
steps/step-4-judge-compile.md
templates/幕纲-模板.md
```

### 3. 执行模式

Pop 调度层和 skill 层统一使用三种模式：

| mode | 条件 | 允许行为 |
| --- | --- | --- |
| `formal` | requiredSkills 全部硬加载，必需 step 已注入，入口材料齐全 | 可落正式产物 |
| `draft` | skill 已加载，但入口材料缺失 | 可输出草案/缺口报告 |
| `trial` | 目标 skill 未加载，或用户明确快速试写 | 只能试写/对齐，不落正式目录 |

### 4. 写入层门禁

正式目录写入必须检查 `execution.mode`：

| 目录/文件 | 允许 mode | 非 formal 处理 |
| --- | --- | --- |
| `正文/chXXX-*.md` | formal | 写入 `正文/草案/` 或返回试写 |
| `卷纲/幕纲-*.md` | formal | 写入 `卷纲/运行/` 草案 |
| `library/设定账本/新书立项PRD.md` | formal | 写入 `library/设定账本/运行/` 草案 |
| `library/设定账本/L1-*.md` | formal | 写入缺口报告或草案 |
| `library/文风DNA/文风DNA.md` | formal | 缺文风原件时写缺口报告 |

### 5. run metadata

每个 run 应记录：

```yaml
runExecution:
  intent:
  phase:
  mode:
  requiredSkills:
  hardLoadedSkills:
  loadedSkillFiles:
  loadedStepFiles:
  requiredInputs:
    present:
    missing:
  allowedWriteTargets:
  blockedWriteTargets:
```

这些 metadata 不依赖 agent 自述，由 Pop 在构造 prompt 和文件写入前后记录。

### 6. 产物 execution 凭证

正式产物内保留 agent 可读、人可审计的凭证：

```yaml
execution:
  mode: formal
  loaded_skills:
    - expert-writer
    - pop-writer-v3-create
  loaded_steps:
    - pop-writer-v3-create/SKILL.md
    - pop-writer-v3-create/steps/step-1-create.md
    - pop-writer-v3-create/templates/创作-模板.md
  required_inputs:
    present:
      - 当前章级导演包
      - 当前章节运行日志
      - 案例消化摘要
      - 爽文审计结果
      - 当前状态快照
      - 设定账本
      - 文风DNA
      - 上章末尾
    missing: []
```

注意：产物内凭证是审计辅助，不是唯一真相。真正可信来源是 run metadata。

## 实施计划

### Phase 1: 调度层硬加载

- 增加意图 → requiredSkills 映射。
- run input 同时注入 expert + 目标执行 skill。
- 目标 skill 注入范围包括 `SKILL.md`、必要 step、模板。

验收：

```text
写正文 run input 中可看到 expert-writer + pop-writer-v3-create。
```

### Phase 2: 模式判定与写入门禁

- run 构建时根据 requiredSkills 和 requiredInputs 判定 `mode`。
- 文件写入前检查 `mode` 和目标路径。
- 非 formal 阻止写入正式目录，或强制落到草案目录。

验收：

```text
缺 create skill 时，正文请求不能写入 正文/chXXX-*.md。
```

### Phase 3: run metadata

- 在 `input.json` 或相邻 metadata 文件中写入 `runExecution`。
- 在 response/report 中显示本次 mode。
- 后续审计工具可扫描 runs，统计 formal/draft/trial 占比。

验收：

```text
runs/*/input.json 或 metadata 中可查询 requiredSkills/hardLoadedSkills/mode。
```

### Phase 4: 产物模板统一

- create 模板已加入 `execution`。
- seed/world/plot/revise/arc 的正式产物模板逐步加入 `execution`。
- world 文风DNA模板必须记录原件来源和复制范围。

验收：

```text
正式正文、正式幕纲、正式 PRD 均可看到 execution 块。
```

## 边界

### 本 PRD 不解决

- 子 agent gateway 断裂、虚假 accepted、completion 丢失等 OpenClaw 框架问题。
- 模型 reasoning_effort 参数透传。
- 文风库内容质量本身。
- plot 审计逻辑是否足够细。

### 本 PRD 解决

- expert-writer 软路由导致目标 skill 未加载。
- 未加载目标 skill 仍落正式产物。
- 正式产物缺 execution 凭证。
- run 复盘必须人工翻 events 才知道是否裸跑。

## 风险

| 风险 | 影响 | 缓解 |
| --- | --- | --- |
| 硬加载多个 skill 增加 prompt token | 成本上升 | 只硬加载 expert + 当前目标 skill，不加载全链路 |
| 意图识别误判 | 加载错 skill | 用户意图表只做第一判定，expert-writer 仍可二次纠偏并返回缺口 |
| 非 formal 阻止写入影响快速试写 | 用户觉得慢 | 增加 trial 输出路径或明确“快速试写不会污染正式目录” |
| agent 伪造 execution | 产物自述不可信 | run metadata 由 Pop 记录，作为真正验收依据 |

## 验收标准

| 验收项 | 标准 |
| --- | --- |
| create 硬加载 | 写正文 run input 同时包含 `expert-writer` 和 `pop-writer-v3-create` |
| world 硬加载 | 世界观/文风DNA请求 run input 同时包含 `expert-writer` 和 `pop-writer-v3-world-foundation` |
| plot 硬加载 | 幕纲请求 run input 同时包含 `expert-writer` 和 `pop-writer-v3-plot` |
| formal 判定 | 入口材料齐全时产物写 `execution.mode: formal` |
| draft 判定 | 缺章级导演包时 create 自动 `mode: draft` |
| trial 阻断 | 未加载 create skill 时不得写入 `正文/chXXX-*.md` |
| run metadata | 每个 run 可查 `requiredSkills/hardLoadedSkills/mode/requiredInputs` |
| 审计效率 | 不读 events 全文，也能判断一次 run 是否裸跑 |

## 推荐最小实现

先实现最小闭环：

```text
1. 意图识别得到 requiredSkills
2. run input 硬注入 expert + target skill
3. runExecution.mode 写入 input/metadata
4. 正式目录写入前检查 mode=formal
5. create 产物写 execution 块
```

只要这五步完成，项目 D 中出现的 “create 没按 skill 执行但仍落正式正文” 问题即可被阻断。
