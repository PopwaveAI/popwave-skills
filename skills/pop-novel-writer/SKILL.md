---
name: pop-novel-writer
display_name: "正文写作引擎（含黄金三章模式·风格注入）"
category: writing
scenario: production
mode: chapter
recommended: 4
tags: ["正文", "写作", "六阶段", "ESM", "黄金三章", "风格注入"]
fidelity: production
description: "正文写作引擎 v9.5。六阶段管线 + 黄金三章模式 + 可插拔风格注入系统。Director（设计说明+决策日志）→ Pass 1（事实骨架）→ ESM before（15项输入包，含style-bundle）→ Pass 2（渲染+自评）→ QC（三层介入）→ ESM after（状态变更）。project.yaml writing_style 字段可切换文风。"
version: v9.5.0
novel_agent_version: v3.3
orchestration:
  preflight: ["check_project_dir", "check_act_exists", "check_v3db", "check_reader_profile"]
  dependencies: ["project.yaml", "02-幕纲/act-XX.yaml"]
  inject_context:
    - "project.yaml#reader_profile"
    - "02-幕纲/act-XX.yaml"
    - "02-章纲/global-summary.md"
    - "00-原始设定/L1-元设定层/"
    - "00-原始设定/L0-产品层/"
    - "01-写作资产/锚定章库/"
    - "01-写作资产/"
    - "01-事实骨架/"
    - "styles/（风格注入包，按 project.yaml writing_style 读取）"
  subagent_required: true
directory: pop-novel-writer

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

> 版本：**9.5.0** · 2026-06-03
>
> v9.5 核心变化：
> - **风格注入系统**：styles/ 目录提供可插拔文风配置，project.yaml writing_style 字段切换
> - **ESM before 升级 15 项**：第 15 项为 style-bundle，约束 Pass 2 渲染
> - **默认风格显式化**：将管线隐含的写法规则提取为 styles/default.md
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
→ 无 act-XX.yaml → 先调 pop-novel-plot 设计幕纲
→ 无 v3.db → 确认项目已通过 bootstrap Phase 3 骨架创建
→ 无 reader_profile → 执行 bootstrap Phase 4 嵌入
→ ★ 无 spec.md → 先调 pop-novel-master 生成规格文档，审批通过后再进入正文写作
→ 提示用户缺失依赖，不进入正文写作

---

## 黄金三章模式（CH1–CH3）

前三章不是"起头"，是**整本书的浓缩核**。读者用前三章决定追不追，编辑用前三章决定签不签。

正常章节（CH4+）可以"慢慢释放"，但前三章不行。前三章必须在极短的篇幅内拉人→压住→释放，留下更大的悬念。
本质上这不是另一种写作方法，而是**同一套管线开到 120% 强度**——作者如果有无限精力，当然希望黄金三百章。

### 与正常章节的核心差异

| 维度 | 正常章节（CH4+） | 黄金三章（CH1–CH3） |
|:---|:---|:---|
| 爽点等级 | 微爽点打底，中爽点每3-5章1个 | **中爽点起步，三章内至少1个大爽点** |
| 字数目标 | 1800-2500（最低1800） | **2200-2500（最低2000）** |
| 爽点版场景卡 | 可选 | **强制**——每章核心事件写1段释放段，≥6段 |
| 风格种子注入 | CH1+全文注入参考书 | CH1注入参考书原文；CH2–CH3注入上章结尾原文 |
| 自检 | 5项轻量 | 5项通用 + **3项专项（首屏/翻页节点/三章连读）** |

### 黄金三章的情绪弧线

前三章不是三篇独立文章，是一条连续的读者情绪管理曲线：

```
CH1 · 拉进来
    目标：让读者产生"我要看下去"的冲动
    钩子：情绪驱使型（悬念/信息炸弹），不用弱钩子

CH2 · 压住
    目标：为第三章蓄力——"这章憋着，第三章应该能释放"
    钩子：在情绪最高点截断

CH3 · 释放 + 新钩子
    目标：第一次真正满足，同时抛出更大问题
    完美收尾：阶段性成果 ✅ → 但刚开个头 ⚠️ → 更大威胁出现 ❓
```

### 爽点分布规则（替代正常分配的微/中/大分档）

| 章号 | 爽点分布 |
|:---|:---|
| CH1 | 中爽点×2（打脸/获得/解谜各一）+ 大爽点级章末钩子 |
| CH2 | 中爽点×2 + 大爽点×1（能力质变/信息反转）+ 大爽点级章末钩子 |
| CH3 | 中爽点×1 + 大爽点×1 + **终极爽点级**章末钩子 |

### 写作前思考（节点C·黄金）

每章写作前（Phase 1·Director 之前），额外执行以下检查：

1. **位置对齐**：这章在弧线中是拉人/压住/释放？情绪起点是否衔接上一章结尾？
2. **读者画像检查**：从 project.yaml 读 reader_profile——这章写给谁看的？
3. **核心判断**：这章如果只让读者记住一件事，是哪件？
4. **首屏风险扫描**：前300字单独读一遍，能留住人吗？
5. **信息密度控制**：是否 ≥2 个新概念？章末钩子类型和上一章不同？

### 专项自检（写完 Phase 4 后，在通用 5 项之外追加）

- □ 前300字是否真正抓住了人？（单独读一遍，感觉"可以划走"→重写）
- □ 本章是否至少有 2 个"读者想划到下一页"的节点？
- □ 三章连起来读，节奏是否稳定？（CH1拉人→CH2压住→CH3释放）

### 完成后转入正常管线

前三章写完后，从 CH4 起走 `pop-novel-writer` 正常六阶段管线：
- 风格种子不再注入
- 场景卡改为可选
- 字数基线回到 1800-2500
- 自检回到 5 项通用

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

  → ⭐ 大纲层 QC（pop-novel-qa Phase 0）通过才能进入下一步

Phase 2 · Pass 1 · 骨架 Agent：
  遵循导演约束 → 输出事实骨架 + 预估字数
  → 骨架 {实体名} 计数 ≥ 8 → 通过
  → 预估字数 < 1800 → 退回加场景或合并章节
  → ⭐ 骨架层 QC（pop-novel-qa Phase 1）通过才能渲染

Phase 3 · ESM before（零LLM，v3.3 升级 / v4.0 spec 注入 / v9.5 style 注入）：
  ├── 第0项 · 读者画像（全管线共享）
  ├── 第1-5项 · 固定SQL
  ├── 第6-8项 · 骨架推断 + 文件读取
  ├── 第9项 · 锚定章片段（按Director引用的片段加载）
  ├── 第10项 · 经验日志自动匹配（按 scene_type 匹配）
  ├── 第11-13项 · K1-K4 知识注入 + 场景模板 + 上轮 QC 反馈
  ├── ★ 第14项 · spec.md（v4.0 新增——规格约束注入 Pass2）
  └── ★ 第15项 · style-bundle（v9.5 新增——文风约束注入 Pass2）
      从 project.yaml 读取 writing_style 字段
      默认 "default" → 加载 styles/default.md
      可选 "tomato" → 加载 styles/tomato.md
      如果指定风格文件不存在 → 降级到 styles/default.md
  → 输出 16 项输入包（15+1，含 spec.md + style-bundle）

Phase 4 · Pass 2 · 渲染 Agent：
  接收 15 项（含锚定章片段+读者画像+经验日志匹配+style-bundle）
  → 渲染正文
  → ⭐ 写后自评（新增——自问三段）：
      "我写的战斗场景和{锚定章}的画面密度差距在哪里？"
      "这一章我给了读者几个'停下来'的时刻？"
      "字数差了多少？差的篇幅本来应该写什么？"
  → 自评不通过 → 补一段最核心的缺失（不重写整章）

Phase 5 · QC Agent ⭐（pop-novel-qa v3.3）：
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

## ESM before 加载的 15 项输入包

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
| 15 | **styles/** | **style-bundle（v9.5 新增——文风约束注入 Pass2）** |

## 风格注入系统（v9.5 新增）

### 概念

风格注入让「相同设定 + 相同大纲 + 相同事实骨架」产出不同阅读体感的正文。

方案不是在 SKILL.md 里写死文风规则，而是通过一个**可插拔的配置文件**——`styles/*.md`——在 ESM before 阶段注入 Pass 2 渲染层。换风格 = 换配置文件，不动管线结构。

### 用法

在 `project.yaml` 中新增字段：

```yaml
project:
  name: "我的小说"
  writing_style: "tomato"    # ← 新增：选择文风，默认为 "default"
```

可用风格：

| ID | 文件 | 定位 |
|:---|:----|:----|
| `default` | `styles/default.md` | 通用网文风格，当前管线的隐含规则显式化 |
| `tomato` | `styles/tomato.md` | 番茄快节奏：短句+对话驱动+极简描写，日更平台优化 |

### 风格文件的构成

每个 `styles/*.md` 基于 [style-dna-template.md](./styles/style-dna-template.md) 定义，包含 4 层结构：

| 层 | 覆盖范围 | 对应模板 section |
|:--|:--------|:----------------|
| 第1层·微观质感 | 句长/描写/对话/POV/段长/修辞/词汇等 7+ 维度 | 1.1 - 1.7 |
| 第2层·叙事策略 | 时间流速/信息释放/开篇/收束/情绪节奏/余白等 7 维度 | 2.1 - 2.7 |
| 第3层·技法偏好 | 对话比/心理动作比/过渡/金句/数字习惯等 7 维度 | 3.1 - 3.7 |
| 第4层·红线清单 | 本风格特有的 QC 检查项和触发规则 | 4.1 - 4.4 |

### 消费路径

```
ESM before 阶段：
  ① 读 project.yaml → 取 writing_style 字段
  ② 构建 path: styles/{writing_style}.md
  ③ 文件不存在 → 降级到 styles/default.md
  ④ 读取文件全文 → 作为第 15 项注入 bundle
  ⑤ Pass 2 渲染时：
     - 核心维度 → 约束渲染的语气/节奏/密度
     - 写法铁则 → 覆盖 K4 的通用铁则
     - 场景类型映射 → 覆盖模板池的写法建议
     - 字数基线 → 覆盖质量标准中的字数
     - 红线清单 → 传递给 QC 的检查项

不调 K4、不改模板池、不改 SKILL.md prompt。
只通过一份 .md 文件约束渲染行为。
```

### 当前文件清单

```
pop-novel-writer/styles/
├── style-dna-template.md   # 文风DNA全量模板（4层·30+维度）
├── default.md              # 默认风格（当前管线的隐含规则显式化）
└── tomato.md               # 番茄快节奏（短句+对话驱动+极简描写）
```

---

## 输出

| 步骤 | 产出 | 位置 |
|:----|:----|:----|
| Phase 1 | 设计说明 + 决策日志 | 传递给 Pass 1 |
| Phase 1-Gate | 大纲层 QC 报告 | 决定是否进入 Pass 1 |
| Phase 2 | 事实骨架 | 01-事实骨架/chXXX-事实骨架.md |
| Phase 2-Gate | 骨架层 QC 报告 | 决定是否进入 Phase 3 |
| Phase 3 | 15 项输入包（含style-bundle） | 01-写作资产/chXXX-bundle.md |
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

### v9.5 — 2026-06-03（v3.3）
- 风格注入系统：styles/ 目录提供可插拔文风配置
- ESM before 升级 15 项输入包（+style-bundle）
- 默认风格显式化：styles/default.md 提取当前管线的隐含规则
- 新增 tomato 文风：短句+对话驱动+极简描写优化

### v9.4 — 2026-06-03（v3.3）
- 黄金三章模式合并入正文引擎（原 pop-novel-opening-arc）
- SKILL.md 新增情绪弧线/爽点分布/节点C·黄金/专项自检 section

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




