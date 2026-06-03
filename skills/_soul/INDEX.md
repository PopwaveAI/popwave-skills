# PopWave — 全局知识库

> 存放位置：`skills/_soul/`
> 职责：PopWave 的顶层定义 + 全局知识资产沉淀
> 形式：纯 Markdown。不依赖数据库、API、引擎。人和 Agent 的认知起点。

---

# 第一部分：PopWave 是什么

## 一句话

> **PopWave 是一个面向 Gen 4 涌现式协作的 AI Creative IDE。**
>
> 我们构建的不仅是一个工具，而是一个**多人多 AI 在共享空间中自组织创作的协奏平台**。

## 代际框架

PopWave 的定位基于一个清晰的代际判断——AI 产品的演化按**协作关系**划分，而非技术能力：

| 代际 | 协作模式 | 本质 | 代表 |
|:----|:---------|:-----|:-----|
| **Gen 1** | 人 → AI | 大模型套壳，单向请求 | SeaArt、AI 写作网站 |
| **Gen 2** | 人 → AI → 交付物 | 云端 agent，端到端外包 | Manus、Lovable |
| **Gen 3** | 人 ⟷ AI | 本地 agent + IDE，双向实时 | Cursor、Codex、Cline |
| **Gen 4 🎯** | **人 ⟷ AI ⟷ AI ⟷ 人** | **多节点协作网络** | **PopWave（定义中）** |
| **Gen 5** | AI = OS | AI 即操作系统 | 远期概念 |

**PopWave 的起点就是 Gen 4。** 不做 Gen 1-3 的追赶者，而是重新定义创意协作的产品范式。

> 深度阅读：[PopWave 世界观](vision/popwave-worldview.md) | [Creative IDE 战略储备方案](vision/popwave-ai-creative-ide.md)

## 两个核心变量

驱动 Gen 4 必然发生的两个底层变量：

| 变量 | 趋势 | 结果 |
|:-----|:-----|:-----|
| **内容复杂度** | 持续暴涨，从单线剧情→多层嵌套宇宙→跨作品联动 | 中心化管理成本 → ∞ |
| **Agent 能力** | 半年一迭代，从单轮到自主编排 | 强管控抑制 Agent 自主性的价值 |

**交汇的唯一解：从"指令驱动"向"涌现驱动"迁移。**

## 涌现式协作的四条规则

PopWave 不提供钉钉式的管理后台，而是让涌现发生的简单规则：

```
规则 1：自主权 — 每个 agent 有权拒绝/提议任务
规则 2：局部共识 — 共享设定的修改必须相关方同意
规则 3：完全可观测 — 所有决策对所有人可见
规则 4：自由进出 — 随时退出，自动移交知识
```

---

# 第二部分：PopWave 的产品蓝图

PopWave 的产品体系由四大核心模块构成，当前处于 **Gen 3 → Gen 4 的过渡期**：

```
PopWave Creative IDE（愿景）
├── Goal Model（编排引擎）      — 长任务自主执行的架构核心
├── 知识库系统（知识资产层）     — 人+Agent 共享的结构化知识
├── 浏览器插件（知识获取器）     — 一键采集高价值内容
└── 多 Skill 生态（能力单元）    — 当前处于此层
```

## Goal Model — 编排架构

> 核心问题：**人不在回路的情况下，系统能稳定地、可预期地、可审计地完成多步骤复杂任务。**

三 Tier 架构：

| 层 | 角色 | 形态 | 生命周期 |
|:---|:-----|:-----|:---------|
| **Tier 1** | 编排层（项目经理） | LLM Agent，持有目标，决策下一步 | 长期存活 |
| **Tier 2** | 执行层（干活的人） | LLM Agent 实例，收到 Message 执行并返回 | 每次新建，用完销毁 |
| **共享状态层** | 进度/基线/日志/经验 | 文件系统 / DB | 持久化 |

**核心创新：**
- Tier 2 每次独立上下文窗口 → 不累积膨胀
- Message 结构化契约（模板池只读 / 质量基线只读 / 审计强制写）
- 经验库跨任务注入 → "下次不犯同样的错"

> 深度阅读：[Goal Model PRD](vision/goal-model-prd.md)

## 知识库系统

> 知识不在 prompt 里，在知识库里。知识是人积累的、Agent 自动查询的、团队共享的。

| 层次 | 形态 | 消费方式 |
|:-----|:-----|:---------|
| **全局知识库** | `skills/_soul/`（本文） | 人读 + Agent 查阅 |
| **规则中枢** | `rule-hub/`（各 skill 内） | 管线自动注入 |
| **项目设定集** | 结构化 YAML/Markdown | Agent 确定性读取 |

> 深度阅读：[知识库 PRD](vision/popwave-knowledge-base-prd.md)

## Skill 生态

每个 pop-* skill 是 PopWave 生态中的一个**能力单元**。Skill = Agent 的"技能包"。

| skill 类型 | 作用 | 代表 |
|:----------|:-----|:-----|
| **内容创作** | 写小说/做海报/生成游戏 | novel-agent / html-anything / book-promo |
| **调研采集** | 搜舆情/下文章/抓数据 | cnovel-research / knowledge-downloader |
| **基础设施** | SEO/飞书/PRD/联网 | seo-anything / feishu-docs / prd-builder |

> 完整图谱见 [`references/skills-overview.md`](references/skills-overview.md)

---

# 第三部分：全局知识库导航

```
_soul/
├── INDEX.md              ← ★ 本文件：PopWave 顶层定义 + 知识库导航
│
├── vision/               ← PopWave 的顶层设计文档
│   ├── popwave-worldview.md           — 底层认知框架
│   ├── popwave-ai-creative-ide.md     — Gen 4 产品蓝图
│   ├── goal-model-prd.md              — 编排引擎架构
│   ├── popwave-knowledge-base-prd.md  — 知识资产层设计
│   └── popwave-browser-extension.md   — 浏览器插件方案
│
├── pop/                  ← 我是谁（身份认知）
│   ├── SOUL.md           — 四层认知操作系统
│   ├── IDENTITY.md       — 身份声明
│   ├── POP-ROUTER.md     — 路由表 + 编排规则
│   └── POP-CALL.md       — 声明模板
│
├── spec-bridge/          ← 我怎么思考（方法论）
│   ├── templates/        — 宏观 Spec / 微观 Spec / Tasks / Checklist
│   └── prompts/          — Spec 生成 / 注入 / QC 的 Prompt
│
├── knowledge/            ← 我知道什么（整合知识，79 份→6 份精华）
│   ├── 01-网文创作底层原理.md  — 三大引擎、代际框架、读者心理学、编辑审稿标准
│   ├── 02-写作质量基线.md     — 10 条内容创作质量标准（章末钩子/否定式/爽点密度/对话占比等）
│   ├── 03-爽点工程设计.md     — 四级分类、六步设计法、铺垫释放比、101 个爽点实证数据
│   ├── 04-开篇与钩子系统.md   — 四类开局公式、黄金三章设计、六种钩子类型
│   ├── 05-角色人设与代入感.md — 主角铁律、辨识度系统、代入感工程、修复方案
│   ├── 06-写作技法精要.md     — 否定式/留白/五感/节奏/对话/视角/52 个技巧速查
│   └── 07-管线踩坑与教训沉淀.md — 18 条 P0-P1 踩坑经验+10 个复盘核心发现
│
└── references/           ← 导航和能力图谱
    ├── skills-overview.md     — 14 个 skill 能力图谱 + 协作边界
    ├── cross-skill-lessons.md — 15 条跨 skill 通用经验
    └── learning-map.md        — 学习资料导航 + 推荐路径
```

## vision/ — PopWave 顶层设计文档

PopWave 整套产品的架构蓝本，从认知框架到产品实现的完整链路：

| 文档 | 核心内容 |
|:-----|:---------|
| [PopWave 世界观](vision/popwave-worldview.md) | AI 两条主线、代际框架、涌现式协作、OPC、PopWave 生态位 |
| [AI Creative IDE](vision/popwave-ai-creative-ide.md) | Agent 角色系统、协作拓扑、产品架构蓝图、演进路线图 |
| [Goal Model PRD](vision/goal-model-prd.md) | 三 Tier 编排架构、Message 契约、质量基线、经验库 |
| [知识库系统 PRD](vision/popwave-knowledge-base-prd.md) | 条目引擎、Schema 模板、权限模型、Agent 消费接口 |
| [浏览器知识获取插件](vision/popwave-browser-extension.md) | 一键内容采集 → 后端拆解管线 |

---

# 第四部分：使用原则

1. **`_soul/` 是认知起点** — 任何人/Agent 打开这里，应该能回答"PopWave 是什么、信什么、能做什么"
2. **不搬文件，只建索引和精华** — 各 skill 内部的复盘/学习资料保留在原位
3. **渐进沉淀** — 经验先在 skill 内部验证，成熟后提炼到全局
4. **旧位保留** — 迁移时保留源文件，存量引用不中断

---

> **PopWave 的第一性原理：创作不是一个人的孤独旅程，也不是一个 AI 的全能表演。创作是一群人 + 一群 AI 在一个共享空间里的协奏。**

*最后更新：2026-06-02 · PopWave v0.1*
