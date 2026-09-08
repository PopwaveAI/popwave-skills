# 12-创作工具管理 vs snow（skill 规范 / 管线编排）

> 镜界「12-创作工具管理」vs snow 的工具/能力管理微观对比。snow 侧：pop-shared-skill-create（skill 设计规范：单文件自包含/资源分层/懒加载）+ pop-snow-pipeline（管线状态机与能力编排）。镜界这是一份**"工具管理总入口"**——本质是呈现"按任务路由到对应操作指南，只读需要、不预读全部"的懒加载模式 + 管理 AgentRules/AgentSkill/Workflow/Subagent 的入口表。镜界没有"工具如何写"（那是单独的 skill-design），这里只管"怎么查/用已装工具"。

---

## 一、镜界该 skill 有哪些提示词（全拆）

**核心逻辑**：`先按任务选择附件，只读取本次需要的操作指南`。

| 任务 | Reference |
|---|---|
| 保存长期写作偏好/禁忌，管理 AgentRules | `references/agent-rules.md` |
| AgentSkill 查找/安装/日常管理 | `references/agent-skills.md` |
| 从模糊需求设计新 AgentSkill（触发边界/提示词/附件结构） | `references/skill-design.md` |
| 管理智能体（职责与 system prompt） | `references/subagents.md` |
| 编排多步骤 Workflow 节点图 | `references/workflows.md` |

**执行纪律**：复制 `<skill_resources>` 的 `reference-list` 调用列出附件，再 `reference-get` 读选中文件；已读且在上下文的附件无需重读，**不预读全部附件**。

**一条关键边界**：`小说角色、功法、世界观规则和故事流程属于故事资料，不按 AI 工具配置处理`——即"工具配置"与"故事资料"严格分流（配套 11 的载体分流理念）。

---

## 二、snow 对应环节定位

- pop-shared-skill-create：skill 设计规范（对应镜界的 skill-design reference + AgentSkill 管理的思想层）。
- pop-snow-pipeline + pop-snow-research/pipeline：能力编排（对应 Workflow 编排）。

---

## 三、值得深挖的学习点（snow 可吸收）

### 🟢 A 级
| # | 镜界提示词 | 为什么值得学 | snow 现状 / 吸收方式 |
|:-:|:--|:--|:--|
| A1 | **懒加载路由：先按任务选附件，只读本次需要的，不预读全部** | snow 的 pop-shared-skill-create 已写"references 越细越好、agent 只在需要时读对应文件"，此处是**产品级印证**——工具管理第一原则就是别把全部操作指南塞进上下文 | 已是 snow 规范，无需新增；可作为 skill 文档"速查表"设计依据（每外部文件标"什么时候读/执行"） |
| A2 | **工具管理 = 路由入口，不承载"怎么写"** | 镜界把"管理工具"和"设计工具"分离两个附件（agent-rules/skill-design 分开）。对应 snow 的"skill 规范"应是独立文档、管理入口只做路由 | 呼应 pop-shared-skill-create"每个 skill 只有一个核心职责"，无新增 |
| A3 | **故事资料 vs AI 工具配置严格分流** | "角色/功法/世界观是故事资料，不按工具配置处理" = 与 11 的载体分流一致，是一条**防串层的红线** | snow 无此显式声明；可进 pop-shared-skill-create 红线：skills 不得储存/改写具体小说的故事事实 |

### 🟡 B 级
| # | 学习点 | 吸收方式 |
|:-:|:--|:--|
| B1 | 附件"name 用「创作工具管理」、path 用目录返回值"的引用协议 | 对应 snow skill 的 resource 引用规范，无新增 |
| B2 | 已读附件无需重读（上下文内省） | 已是 snow 通用原则 |

---

## 四、snow 反补镜界 / 交汇点

- snow 的**自包含单文件 + 资源分层 + 懒加载**是镜界"附件懒加载"的落地实现；镜界的**故事资料 vs 工具配置分流**可反补 snow 的红线。
- 无冲突，本档含金量主要是一次**理念印证**，而非新方法论。

---

## 五、结论 / 吸收建议

本档无重大新增；两点呼应：①懒加载路由已是 snow 「references 拆分」的落地示例；②「故事资料 ≠ AI 工具配置」可进 pop-shared-skill-create 红线，防止 skill 越界存储/改写项目故事事实。