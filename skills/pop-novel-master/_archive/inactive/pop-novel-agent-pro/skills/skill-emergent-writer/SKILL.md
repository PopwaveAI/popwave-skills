---
name: emergent-writer
display_name: "正文写作引擎"
category: writing
scenario: production
mode: chapter
recommended: 4
tags: ["正文", "写作", "六阶段", "ESM"]
fidelity: production
description: "正文写作引擎 v9.3（v3.3）。六阶段管线：Director（设计说明+决策日志）→ Pass 1（事实骨架）→ ESM before（14项完整输入包）→ Pass 2（渲染+自评）→ QC（三层介入）→ ESM after（状态变更）。v3.3核心升级：Hard闸门+否定句5变体全覆盖+锚定章3格式正则+原始设定10文件注入bundle+DB state_changelog写入。"
version: v9.3.0
novel_agent_version: v3.3
orchestration:
  preflight: ["check_project_dir", "check_act_exists", "check_v3db", "check_reader_profile"]
  dependencies: ["project.yaml", "02-幕纲/act-XX.yaml"]
  inject_context:
    - "project.yaml#reader_profile"
    - "02-幕纲/act-XX.yaml"
    - "02-章纲/global-summary.md"
    - "00-原始设定/L1-元设定层/"       # Phase 1: 新增——诡异行为/数值/成长体系注入
    - "00-原始设定/L0-产品层/"         # Phase 1: 新增——角色行为锚定/金手指设计注入
    - "01-写作资产/锚定章库/"           # Phase 1: 显式列出锚定章路径
    - "01-写作资产/"
    - "01-事实骨架/"
  subagent_required: true
directory: skill-emergent-writer

produces:
  - 设计说明 + 决策日志（Phase 1）
  - 大纲层QC报告（Phase 1-Gate）
  - 01-事实骨架/chXXX-事实骨架.md（Phase 2）
  - 骨架层QC报告（Phase 2-Gate）
  - 01-写作资产/chXXX-bundle.md（Phase 3 — 14项输入包）
  - 03-正文/chXXX.md + 写后自评（Phase 4）
  - 正文层QC报告（Phase 5）
  - v3.db state_changelog + global-summary.md（Phase 6）
---

# Emergent Writer — v3.3 · 六阶段管线

> 版本：**9.3.0** · 2026-05-25
>
> v3.3 核心变化：
> - **中控升级**：从"规划者"到"导演"——输出决策日志、锚定章引用
> - **QC 三层介入**：大纲层（事前）→ 骨架层（渲染前）→ 正文层（成品）
> - **读者画像穿透**：reader_profile 作为第0项注入全管线
> - **写后自评**：Agent 自己先看一遍再给 QC
> - **锚定章注入**：手动片段池 + Director 核心特征提炼
> - **经验日志结构化**：scene_type 自动匹配同类场景

<pop-category>writing</pop-category>
<pop-position>4</pop-position>

---

## 什么时候使用

- 用户要求写第N章正文
- 用户要求续写当前章节
- 用户要求修改已写章节

## HARD-GATE

在开始写任何章节正文之前，必须确认以下前提：
1. 当前幕的幕纲（act-XX.yaml）已完成设计并通过节奏自检
2. v3.db 已就绪（04-数据库/xxx_v3.db）
3. 01-事实骨架/ 和 01-写作资产/ 目录已创建
4. 全局摘要和经验日志已就绪
5. **project.yaml 包含 reader_profile 字段**（v3.3 新增）
6. **★ spec.md 已审批就绪**（v4.0 新增 — 规格文档必须在正文写作前通过审批）

如果以上任意一项不满足：
→ 无 act-XX.yaml → 先调 skill-plot-architecture 设计幕纲
→ 无 v3.db → 确认项目已通过 bootstrap Phase 3 骨架创建
→ 无 reader_profile → 执行 bootstrap Phase 4 嵌入
→ ★ 无 spec.md → 先调 spec-bridge 生成规格文档，审批通过后再进入正文写作
→ 提示用户缺失依赖，不进入正文写作

---

## v3.3 六阶段管线

```
Phase 0 · 提前完成的设定（开书阶段）：
  ├── ★ spec.md 已审批（v4.0 新增 — 规格闸门）
  ├── Boss设计（数值体系联合完成）
  ├── 数值体系（含敌我段位表+幕级升级时间表）
  ├── 锚定章片段库（手动提取 3-5 个片段）
  └── 角色行为锚定

Phase 1 · Director Agent ⭐ 升级：
  读 act-XX.yaml + 读者画像 + 经验日志
  → 输出设计说明 + 决策日志

  设计说明：
    ├── 本章核心目的（一句话）
    ├── 场景权重分配 + 字数目标
    ├── 锚定章引用（从库中选同类型片段）
    ├── 爽点触发方式（视觉冲击/信息反转/代价展示/碾压释放/情绪积累释放）
    └── 描写密度指南（哪个场景用短句、哪个场景用感官细节）

  决策日志（新增——让推理路径可审视）：
    ├── 锚定章选择: "战斗-XXX-YYY"
    │   ├── 原因: "本章节奏和XXX一致"
    │   └── 核心特征提炼: ...
    ├── 字数决策: "目标2300-2500"
    │   └── 原因: ...
    └── 爽点触发方式: "视觉冲击型"
        └── 原因: ...

  → ⭐ 大纲层 QC（qa-payoff Phase 0）通过才能进入下一步

Phase 2 · Pass 1 · 骨架 Agent：
  遵循导演约束 → 输出事实骨架 + 预估字数
  → 骨架 {实体名} 计数 ≥ 8 → 通过
  → 预估字数 < 1800 → 退回加场景或合并章节
  → ⭐ 骨架层 QC（qa-payoff Phase 1）通过才能渲染

Phase 3 · ESM before（零LLM，v3.3 升级 / v4.0 spec 注入）：
  ├── 第0项 · 读者画像（全管线共享）
  ├── 第1-5项 · 固定SQL
  ├── 第6-8项 · 骨架推断 + 文件读取
  ├── 第9项 · 锚定章片段（按Director引用的片段加载）
  ├── 第10项 · 经验日志自动匹配（按 scene_type 匹配）
  ├── 第11-13项 · K1-K4 知识注入 + 场景模板 + 上轮 QC 反馈
  └── ★ 第14项 · spec.md（v4.0 新增——规格约束注入 Pass2）
  → 输出 15 项输入包（14+1，含 spec.md）

Phase 4 · Pass 2 · 渲染 Agent：
  接收 14 项（含锚定章片段+读者画像+经验日志匹配）
  → 渲染正文
  → ⭐ 写后自评（新增——自问三段）：
      "我写的战斗场景和{锚定章}的画面密度差距在哪里？"
      "这一章我给了读者几个'停下来'的时刻？"
      "字数差了多少？差的篇幅本来应该写什么？"
  → 自评不通过 → 补一段最核心的缺失（不重写整章）

Phase 5 · QC Agent ⭐（qa-payoff v3.3）：
  ├── 正文层 QC → 纯感受报告
  ├── 红线标记: "想跳过"≥2 或 "会弃书"
  └── → 不通过 → 退回 Pass 2 重写

Phase 6 · ESM after（零LLM）：
  ├── SQLite: INSERT state_changelog + UPDATE 字段
  └── 文件: 追加 global-summary.md
  └── 如 QC 有红线 → 追加经验日志条目（自动归档）
```

## 读者画像（v3.3 新增穿透机制）

reader_profile 定义在 `project.yaml` 中，作为**第0项**注入每一个 bundle：

```yaml
reader_profile:
  platform: "番茄"
  gender: "男频"
  age_range: "22-28"
  reading_habit: "日刷30-50章，每章停留≤40秒，连续2章无爽点即弃"
  expectation: "每章至少一个微爽点，每3章一个中爽点"
```

全管线共享同一个读者画像：
- Directors Agent: "我追的这个人会想看这段吗？"
- Pass 1 Agent: "这段能让他停下来吗？不能就别写那么长"
- Pass 2 Agent: "这一段他会不会滑过去？"
- QC Agent: 以这个读者的身份输出感受报告

## 锚定章系统（v3.3 新增注入）

```
01-写作资产/锚定章库/
  ├── 战斗-XXX-YYY.md         ← 战斗场景画面节奏参考
  ├── 对话-XXX-YYY.md         ← 对话场景信息释放参考
  └── 悬疑-XXX-YYY.md         ← 悬疑场景气氛构建参考

使用方式：
  1. Director 写设计说明时选中锚定章引用 + 提炼核心特征
  2. ESM before 读到引用 → 从 01-写作资产/锚定章库/ 加载片段
  3. 锚定片段 + Director 提炼的核心特征 → 一并注入 Pass 2 的"风格种子"区域
```

## 经验日志结构化匹配（v3.3 新增）

每条经验包含结构化字段，ESM before 自动匹配：

```yaml
- id: 1
  scene_type: "章节规划"
  problem: "有效信息量不足却独立成章 → 字数1200"
  root_cause: "骨架时没意识到'3件事只够2章'"
  fix_action: "核心事件数<3个时 → 不做独立章，合并"
  status: "active"
```

ESM before 加载时：扫描 status="active" 的条目 → 匹配当前 chapter 的场景类型 → 将 fix_action 追加到 Director prompt 中。

## ESM before 加载的 14 项输入包

| # | 来源 | 内容 |
|:-:|:----|:------|
| 0 | project.yaml | **读者画像 reader_profile**（v3.3 新增）|
| 1-5 | SQLite | 主角/skills/weirds/items/state_changelog |
| 6-8 | 骨架+文件 | 骨架推断 + global-summary + 上一章结尾 |
| 9 | 设计说明 | Director 决策日志（含锚定引用）|
| 10 | 锚定章库 | **按 Director 引用加载的片段**（v3.3 新增）|
| 11 | 场景模板 | 按场景类型匹配的模板 |
| 12 | K1-K4 | 知识注入 |
| 13 | 经验日志 | **自动匹配的经验教训**（v3.3 新增）|
| 14 | QC反馈 | 上一轮 QC 报告（如有）|

## 输出

| 步骤 | 产出 | 位置 |
|:----|:----|:----|
| Phase 1 | 设计说明 + 决策日志 | 传递给 Pass 1 |
| Phase 1-Gate | 大纲层 QC 报告 | 决定是否进入 Pass 1 |
| Phase 2 | 事实骨架 | 01-事实骨架/chXXX-事实骨架.md |
| Phase 2-Gate | 骨架层 QC 报告 | 决定是否进入 Phase 3 |
| Phase 3 | 14 项输入包 | 01-写作资产/chXXX-bundle.md |
| Phase 4 | 正文章节 + 自评 | 03-正文/chXXX.md |
| Phase 5 | 正文层 QC 报告 | QC 报告 |
| Phase 6 | 状态变更 | v3.db + global-summary.md |

## 质量标准

- Director 必须输出决策日志（含"为什么"）
- 每章骨架 {实体名} 计数 ≥ 8
- 预估字数 ≥ 1800（不够则合并章节）
- 写后自评必须执行（补充不重写）
- 5 项轻量自检（来自 v7.8）
- 否定句红线：3 变体正则匹配 + K4 注入双拦截
- QC 红线触发 → 退回 Pass 2 重写

## 版本历史

### v9.3 — 2026-05-25（v3.3）
- 六阶段管线重构
- Director 升级：决策日志 + 锚定章引用 + 字数目标
- ESM before 14 项：+reader_profile + 锚定章 + 经验日志匹配
- Pass 2：+写后自评 + 锚定章风格种子
- QC 升级：3 层介入 + 纯感受报告

### v9.0 — 2026-05-24
- ESM v2.0 SQLite 全书数据中台
- Pass 1/Pass 2 分离
- after_write 双写

### v8.0 — 2026-05-21
- 导演 Agent 回归
- K1-K4 知识注入体系
- 经验日志机制



### 9.0.0 — 2026-05-24
- ESM v2.0 SQLite数据中台
- 五步流水线：导演思考→Pass 1→ESM before→Pass 2→ESM after
- K1-K4知识注入体系
- 场景模板池七类场景
