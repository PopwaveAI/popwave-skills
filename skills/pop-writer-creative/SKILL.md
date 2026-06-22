---
name: pop-writer-creative
description: "当用户说'开新书/创意打磨/方向碰撞/我想写个故事/修仙/玄幻'时启用。用户给模糊想法 → agent 联网搜索+trope-library 生成 2-3 个故事概念选项 → 用户选择 → 产出 全书立项PRD.md（唯一立项宪法）。"
pipeline:
  upstream: [pop-decon]
  downstream: [pop-writer-world, pop-writer-plot]
  references: [pop-trope-library]
version: 4.4.0
---

# pop-writer-creative · 创意打磨

> 从用户模糊想法到高质量立项 PRD 的**唯一入口**。PRD 产出后交付 world。

## ❌ 质量红线

| # | 红线 |
|:-:|:-----|
| ❌1 | **读取协议** — 禁止用 Read 工具读取 skill 文件，用 `skill_view` 或 `Get-Content -Encoding UTF8 -Raw`。截断 = 信息丢失 = 创作失误 |
| ❌2 | **Phase R 不可跳过** — 路由诊断决定搜索宽度 |
| ❌3 | **PRD 推导不可跳过** — 9 步全走 |
| ❌4 | **不预设 L1 级施工细节** — PRD 可写核心创意命名（世界名/主角名/金手指名），不可写属性数值、冷却时间、详细转译规则、分幕划分。写完每条问自己：「这是创意决策还是施工图？」创意决策留 PRD，施工图留 L1/plot |
| ❌5 | **不把拆书复盘当开书推演** — PRD 是开书第一天的文档，不是 37 章读完后的 catalog |
| ❌6 | **Phase 2 自问链不可跳过** — 拿到元爽点标签不准停，必须向下追问 L1-L4 特征参数。无参数的爽点 = 没打磨的设计 |
| ❌7 | **不强行归类** — 元爽点不匹配 7 类常见模板时走元模板生成自定义追问链，不硬塞 |

## 速查表（完整目录引导）

### steps/ — 执行层

| 什么时候 | 读什么文件 | 产出 |
|:---------|:----------|:-----|
| 路由诊断 | `steps/step-r.md` | 输入粒度→搜索宽度 |
| 研究+生成选项 | `steps/step-prd-research.md` | 2-3 个故事概念选项（Step 1-2） |
| 用户选择后推导 PRD | `steps/step-prd-derive.md` | 全书立项PRD.md（Step 3-9） |

### references/ — 知识层（读后理解，指导操作）

| 什么时候 | 读什么文件 | 产出 |
|:---------|:----------|:-----|
| Step 1 Phase 2b 自问链 | `references/爽点追问链.md` | 7类追问链+元模板（L1-L4/L5特征参数） |
| Step 2.1 联网搜索 | `references/搜索SOP.md` | 三路搜索路径+关键词提取+质量自检 |

### templates/ — 模板层（复制填充，直接产出）

| 什么时候 | 读什么文件 | 产出 |
|:---------|:----------|:-----|
| Step 2.2 合成选项 | `templates/故事概念选项-模板.md` | 质量标准+吸引力设计+差异化矩阵 |
| Step 8 合成 PRD | `templates/prd-模板-空白.md` | PRD 宪法结构空模板（10块） |
| Step 2 生成选项时参考 | `templates/prd-模板-魔门.md` | 完整填充示例（让魔门再次伟大） |

### 外部依赖

| 什么时候 | 读什么文件 | 产出 |
|:---------|:----------|:-----|
| Step 2 生成选项前 | `skills/pop-trope-library/套路库/00-总索引.md` | 套路模式家族列表 |
| Step 2 生成选项前 | `skills/pop-trope-library/references/元爽点-变体映射表.md` | 元爽点→变体家族映射 |
| Step 2 搜索方向 | `skills/pop-trope-library/references/调用匹配SOP.md` | 三维查询协议（层×赛道×元爽点） |

## 路由

```
用户说"开书" / "我有一个想法"
  │
  ▼
Phase R · 路由诊断 → 判断输入粒度 → 决定搜索宽度
  详见 steps/step-r.md
  │
  ▼
Step PRD-A · 研究 + 生成选项 (step-prd-research.md)
  Step 1: 最小化爽点确认（≤3 问）→ Phase 2 自问链 → 特征参数表
  Step 2: trope-library 查询 + 联网搜索 → 2-3 个故事概念选项  ★
  │
  ⏸ 用户断点：呈现选项，等用户选择
  │
  ▼
Step PRD-B · 锁定概念 → 推导 PRD (step-prd-derive.md)
  Step 3: 用户选择 → 锁定概念 + 核心卖点(≥5条) + 用户画像
  Step 4: 从基因推导全书色彩 + 命名体系 + 视觉锚点场景
  Step 5: 推导世界宪法（4-6条，附违反后果）
  Step 6: 跨域素材指引（方向性，非详细方案）
  Step 7: 篇幅规划
  Step 8: 合成 PRD（宪法结构 10 块）
  Step 9: 验证 → 写入
  │
  ▼
全书立项PRD.md → 交付 world
```

## 产出

```
全书立项PRD.md — 唯一立项宪法（10块结构）
```

---

v4.4.0 | 2026-06-22 | 对齐 pop-shared-skill-create v5.0 标准（读取协议top1+速查表+CHANGELOG），集成 trope-library → [CHANGELOG.md](CHANGELOG.md)
