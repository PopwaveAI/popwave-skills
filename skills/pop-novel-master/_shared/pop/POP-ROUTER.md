# POP-ROUTER.md — pop 编排路由表

> pop 收到需求后，根据用户意图通过编排控制器自动路由。
> 编排器：`glue/orchestrate.py` | 控制器：`_shared/pop/dispatcher.py`
>
> 流程：user_intent → orchestrator → 查路由 → 解析 frontmatter → 前置检查 → 装配上下文 → 分发

---

## 一、路由总表

| 用户意图 | 场景分类 | 路由 skill | 前置条件 | 产出 |
|:---|:---|:---|:---|:---|
| **规格生成 / 审批 / 任何写作任务前先过规格** | **spec → pre-production** | **spec-bridge ★** | **无** | **spec.md + tasks.md + checklist.md** |
| 新书启动 / 开书 / 设计设定 | bootstrap → design | **skill-project-bootstrap** | 无 | L0 ↔ L1 ↔ L2 设定 |
| 设计幕纲 / 剧情架构 | plot → design | **pop-novel-plot** | project.yaml + PRD + L1 设定 | act-XX.yaml |
| 写前三章 / 开篇 | opening | **pop-novel-writer（黄金三章模式）** | L0/L1 设定 | ch001-ch003.md |
| 写第 N 章 / 正文写作 | writing → production | **skill-emergent-writer** | act-XX.yaml + global_summary + **spec.md ★** | chXXX.md |
| 拆书 / 解构 / 分析参考书 | deconstruct → research | **skill-book-deconstructor** | 参考书原文 | scene_fragments.db |
| 审稿 / QA / 质检 | qa → review | **skill-qa-payoff** | 正文 MD + **spec.md（可选）★** | QA 报告 |
| 市场验证 / 审市场 | market → review | **skill-market-test** | 正文 + L1 | 三叠报告 |
| 续写交接 / 已有正文 | continuation | **_continuation** | 已有正文 | bootstrap/plot 输入 |
| 调研 / 研究 / 搜索 | research | **cnovel-research-main** | 调研目标 | 调研报告 |

---

## 二、编排工作流（由 dispatcher.py 自动化）

```
用户需求
      │
      ▼
┌─────────────────────────────────────────────────────────────┐
│ ① pop 声明（自动生成）                                      │
│   glue/orchestrate.py "..." --describe                      │
└──────────────────────┬──────────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ ② dispatcher.py 意图匹配                                    │
│   ROUTING_TABLE × user_intent 关键词打分                    │
│   ★ 如果是写作类意图，检查是否存在 spec.md                   │
│   ★ 如果不存在 → 先路由到 spec-bridge                        │
└──────────────────────┬──────────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ ③ ★ SPEC 闸门（新增）                                      │
│   如果目标 skill 需要 spec 约束（emergent-writer/qa-payoff）│
│   但项目中不存在 .trae/specs/<change-id>/spec.md:           │
│     → 先调 spec-bridge 生成三文件                           │
│     → 等待审批确认                                         │
│     → 审批通过后继续                                       │
└──────────────────────┬──────────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ ④ 解析 SKILL.md frontmatter                                │
│   提取 orchestration 字段:                                  │
│   preflight / dependencies / inject_context                │
└──────────────────────┬──────────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ ⑤ ★ Spec 上下文注入（新增）                                │
│   如果 .trae/specs/<change-id>/spec.md 存在:                │
│     → 执行 spec-bridge/scripts/spec_to_prompt.py --inject   │
│     → 将 spec 约束注入当前 Agent Prompt 头部                │
└──────────────────────┬──────────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ ⑥ 前置检查 ✅                                              │
│   - glue/pre_flight.py（如果编排字段定义）                  │
│   - 检查 dependencies 文件是否存在                          │
│   - ★ 新增: 检查 .trae/specs/<change-id>/ 完整性            │
└──────────────────────┬──────────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ ⑦ 装配上下文 + 生成子Agent Prompt                          │
│   inject_context → 读取文件 → 注入 Prompt                  │
│   ★ 注入 spec.md 的 Goals / Non-Goals / AC 到 Prompt 头部   │
└──────────────────────┬──────────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ ⑧ 交付 JobOrder → pop agent 执行 skill SOP                 │
│   输出：skill_name + context + prompt + preflight_results   │
│   如果 subagent_required → 走子Agent                        │
└─────────────────────────────────────────────────────────────┘
```

---

## 三、意图关键词 → 分类映射

| 用户输入包含 | 场景分类 | 路由 skill |
|:---|:---|:---|
| 规格 / spec / 审批 / 生成规格 | spec | **spec-bridge ★** | 无 | spec.md + tasks.md + checklist.md |
| 开书 / 启动 / 设计设定 / 开新书 | bootstrap | skill-project-bootstrap |
| 幕纲 / 大纲 / 剧情 / 幕设计 | plot | pop-novel-plot |
| 前三章 / 开篇 / 黄金三章 | opening | pop-novel-writer（黄金三章模式） |
| 写 ch / 写作 / 正文 / 第N章 | writing | skill-emergent-writer |
| 拆书 / 解构 / 分析 / 对标 | deconstruct | skill-book-deconstructor |
| 审稿 / QA / 审一下 / 质检 | qa | skill-qa-payoff |
| 市场 / 验证 / 审市场 | market | skill-market-test |
| 续写 / 交接 / 已有正文 | continuation | _continuation |
| 调研 / 搜索 / 研究 | research | **cnovel-research** | 调研目标 | 跨平台调研报告 |
| HTML化 / 发布 / 渲染 / 做成HTML | htmlify → publish | **html-renderer** | 任意文档（.md/.yaml） | 可视化HTML文件 |
| 舆情 / 网文舆情 / 查一下 / 书评 | research → opinion | **book-opinion-tracker** | 书名 | 标准化舆情报告 |

> 关键词匹配优先级：精确匹配 > 部分匹配 > tags 匹配。
> 如果多个 skill 匹配 → 选 `recommended` 值最小的（1=最高优先级）。

---

## 四、编排器声明格式

pop 收到需求后，调 `glue/orchestrate.py` 自动生成声明：

```bash
# pop 内部等价操作：
python glue/orchestrate.py "写第8章" --project "..." --describe
```

输出：
```
🖋️ **pop 收到老板指示**

任务理解：正文写作引擎 v8.0。导演Agent思考+判断...
场景判断：writing → production
路由技能：正文写作 v8.0（推荐排序 1）
前置条件：project.yaml → ✅ / act-XX.yaml → ✅
大门状态：✅ 门全开
```

---

## 五、编排规则

1. **有 skill 不走自由发挥** → 任何创作任务必须先路由到对应 skill
2. **不跳过 HARD-GATE** → 每个 SKILL.md 的 HARD-GATE 是最高级前置信令
3. **Spec 优先** → 写作/质检类任务前，必须先检查是否存在对应 spec.md；不存在则先路由到 spec-bridge
4. **审批闸门** → spec.md 必须经过人工审批才能进入实现阶段；审批未通过不执行
5. **子Agent 隔离** → 正文/审稿走独立子Agent，不继承主对话历史
6. **glue 层介入** → 写作前必须跑 pre_flight，写作后必须跑 post_write
7. **Spec 贯穿** → 每个子Agent 的 Prompt 头部注入 spec.md 的 Goals / Non-Goals / AC 约束
8. **Checklist 验证** → 所有任务完成后，必须对照 checklist.md 逐项验证才能声称完成
9. **一步一公示** → 每一步的输出路径都要告诉用户

---

> 此文件为 pop 编排调度基准。变更时同步更新 skill-mapping.yaml 和 VERSION.md。
