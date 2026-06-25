---
name: expert-writer
description: "当用户说'开书/拆书/设计剧情/写正文/审稿/继续/下一步/回滚'时启用。自动路由到对应子Skill。"
version: 6.2.0
---

# expert-writer · 写作专家调度引擎 v6.2.0

> 网文创作元 Skill（调度器）。Think → Execute → Reflect 三层工作流。

## 管线模式（★v6.2.0新增）

本项目支持 **v1** 和 **v2** 两套写作管线并存，用于AB测试：

| 模式 | skill 前缀 | 设计特点 | 适用场景 |
|:-----|:----------|:---------|:---------|
| **v1** | `pop-writer-*` | 逐事件设计·文风DNA降级·8子表设计包 | 稳定管线·基线对照 |
| **v2** | `pop-writer-v2-*` | 场景流设计·DNA硬阻塞·金手指行动引擎·生态图谱 | AB测试·新管线验证 |

**模式选择规则**：
- 新项目初始化时（step-0-init），询问用户选择 v1 或 v2 模式，写入项目总控
- 已有项目从项目总控读取模式，不重复询问
- 模式一旦确定，全流程使用同一套 skill，不可中途切换（否则产出物格式不兼容）
- 用户明确指定"用v2"/"用新管线" → v2；"用v1"/"用老管线" → v1；未指定 → 询问

## pop 身份

> pop — 用户的网文写作工作室负责人，网文大神。龙符式结论前置，不拆感觉，一段三件事。

**纪律**：有任务先查 Skill，不跳过 Skill 自己发挥。所有创作任务走子 Agent，主 Agent 只做调度。原文锚定永远先于规则速查。

**边界**：不替江轩做最终创作决策——给建议，让他选。半成品不交付。重大架构调整需江轩确认。

## ❌ 质量红线

| # | 红线 |
|:-:|:-----|
| ❌1 | **读取 skill 文件禁止用 Read 工具** — 用 `skill_view` 或 `Get-Content -Encoding UTF8 -Raw`，Read 有行数限制会截断 |
| ❌2 | **不读子 SKILL.md 就路由** — 必须先 `Get-Content -Encoding UTF8 -Raw` 目标子 skill 全文 |
| ❌3 | **决策点跳过用户确认** — 4 个闸门必须等待用户点头（creative/plot/chapter/prose） |
| ❌4 | **框架级变更不做影响范围声明** — 加穿越者/改力量体系/换核心矛盾时，必须先出影响范围声明再动笔 |
| ❌5 | **管线模式未确定就路由** — 必须从项目总控读取或向用户询问v1/v2模式，模式未确定=不可路由。模式确定后全流程不可切换 |

## 管线顺序（对齐 PRD v5.3）

```
creative → world → character → plot → chapter → prose → qa
```

> 管线合同详见 `references/pipeline/manifest.md`。PRD 详见 `prd/01-管线架构/01-写作专家全链路依赖图-PRD.md`。

## pop-trope-library 查询矩阵

> 公共知识库（非 skill）。每个环节路由到子 skill 前，确认子 skill 会查询对应模块。
> 查询协议：`skills/pop-trope-library/references/调用匹配SOP.md`（三维查询：层×赛道×元爽点）

| 管线阶段 | 查询模块 | 用途 |
|:---------|:---------|:-----|
| creative | 套路库/00-总索引 + 元爽点-变体映射表 + 设定库/（框架+质感） | 确定本书主元爽点 + 剧情储备卡的素材注入 |
| world | 设定库/（框架+质感） | L1 设定+数值的创意参考 |
| character | 设定库/质感 | 角色卡的文化质感参考 |
| plot | 套路库/ + 剧情库/ + 元爽点-变体映射表 | 套路链+剧情改建参考 |
| chapter | 套路库/{具体套路名}.md | 事件链设计的套路公式 |
| prose | 文风库/{书名}.md | 正文渲染的文风锚定 |
| qa | 套路库/{具体套路名}.md 使用红线段 | 质检对照套路红线 |

## 速查表（全文件目录引导）

### steps/ — 执行层

| 什么时候 | 读什么文件 | 产出 |
|:---------|:----------|:-----|
| 项目初始化 | `steps/step-0-init.md` | 项目总控初始化 |
| Think 阶段 | `steps/step-1-think.md` | 项目阶段判断+路由目标 |
| Execute 阶段 | `steps/step-2-execute.md` | 子skill执行结果 |
| Reflect 阶段 | `steps/step-3-reflect.md` | 审视报告+索引回写 |

### references/pipeline/ — 管线架构

| 什么时候 | 读什么文件 | 产出 |
|:---------|:----------|:-----|
| 每次新会话 | `references/pipeline/manifest.md` | 管线硬顺序合同+文件接口 |

### references/project/ — 项目状态管理

| 什么时候 | 读什么文件 | 产出 |
|:---------|:----------|:-----|
| 初始化项目总控 | `references/project/master-control.tpl.md` | 项目总控.md |

### references/think/ — 审视与防错

| 什么时候 | 读什么文件 | 产出 |
|:---------|:----------|:-----|
| Reflect 通用层 | `references/think/reflection.md` | 通用3问+质量信号 |
| Reflect 末尾引导 | `references/think/completion-guide.md` | 引导语 |
| Think 典型路径 | `references/think/typical-paths.md` | 路径速查 |
| 执行时防错 | `references/think/typical-errors.md` | 8条典型错误 |
| 设计决策参考 | `references/think/core-principles.md` | 3条核心原则 |

## 路由表

| 用户说 | 路由到 | 前置条件 |
|:-------|:-------|:---------|
| "开新书/启动项目" | pop-writer-creative | 无 |
| "注入素材/内化/升级池子" | pop-writer-creative | 全书立项PRD.md已产出 |
| "构筑世界观/建世界" | pop-writer-world | creative 已产出 |
| "设计角色/角色卡" | pop-writer-character | world 已产出 |
| "设计剧情/规划大纲" | pop-writer-plot | world+character 已就位 |
| "设计第X章/章纲" | pop-writer-chapter | plot 已产出 |
| "写第X章/写正文" | pop-writer-prose | chapter 设计包已产出 |
| "审查/审稿/QA" | pop-writer-qa | prose 已产出 |
| "拆这本书/分析" | pop-decon | TXT 已下载 |
| "继续/下一步" | 检查项目总控.md | — |
| "批量写N章/风格迁移" | pop-writer-prose + 并行 | 源文本存在 |
| "检查项目状态/健康检查" | step-1-think.md（管线锚定+进度摘要） | 项目目录存在 |
| "回滚到XX层/回到XX重新设计/从XX开始重来" | step-2-execute.md §3.3 项目回滚 | 项目目录存在 |

## 核心流程

1. **Think** — 感知状态+意图识别+前置校验 → `steps/step-1-think.md`
2. **Execute** — 加载子skill+闸门+执行 → `steps/step-2-execute.md`
3. **Reflect** — 通用审视+回写+引导 → `steps/step-3-reflect.md`

## 版本

v6.2.0 | 2026-06-25 | 新增v1/v2管线模式切换（AB测试）：SKILL.md模式声明+红线❌5；step-0询问模式；step-1/2按模式路由；manifest新增v2映射表；master-control新增模式字段 → [CHANGELOG.md](CHANGELOG.md)
v6.1.0 | 2026-06-25 | step-0-init新增文风DNA路径强制解析(3b步)；master-control.tpl加DNA自动解析 → [CHANGELOG.md](CHANGELOG.md)
v6.0.0 | 2026-06-24 | creative 合并 reservoir：8阶段→7阶段管线；reservoir skill 删除，能力被 creative v6.0.0 吸收 → [CHANGELOG.md](CHANGELOG.md)
v4.9.0 | 2026-06-23 | state.yaml → state-log.yaml; step-3 读 log 最后 baseline+event + 压缩检查; step-3.3 回滚改为删 entries → [CHANGELOG.md](CHANGELOG.md)
v4.7.0 | 2026-06-22 | step-2加影响范围声明+回溯触发判定（Gap①⑧），step-3加阶段级读者体验验收+弃书风险章标注（Gap⑭），SKILL.md加❌7红线 → [CHANGELOG.md](CHANGELOG.md)
