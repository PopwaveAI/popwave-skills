---
name: pop-shared-html
description: 当用户说"HTML化/渲染成网页/发布页面/做网站/做展示页/做成HTML/做成网页/前端展示/可视化页面"时启用。HTML 集中化渲染引擎——所有上游 skill 只产出结构化数据，HTML 化统一交由本 skill。内嵌 Seedream 生图 + 三层叠图 Hero + 长文阅读器 + 内容互联。
version: 2.5.0
pipeline:
  upstream: [pop-shared-reader, pop-shared-book-promo, tool-youtube-webbuilder]
  downstream: []
---

# pop-shared-html · 统一 HTML 渲染引擎 v2.5

> **定位：HTML 集中化。** 所有 skill 只产出结构化 Markdown，HTML 化统一交由本 skill。
> 本 skill 负责将任何结构化内容渲染为高质量的、视觉一致的单文件 HTML。
> **上游给素材原料 → 本 skill 独立做设计决策 → 输出统一高质量 HTML + 可选的 AI 配图。**

---

## 速查表

| 步骤 | 操作 | 详细文档 | 门禁 |
|:-----|:-----|:---------|:-----|
| Phase 0 | 素材分析 + 设计决策 | [steps/phase-0-design-brief.md](steps/phase-0-design-brief.md) | 缺配图规划 → 退回 |
| Step 1 | 内容类型检测 | [steps/step-01-content-type.md](steps/step-01-content-type.md) | — |
| Step 2 | 选择渲染骨架 | [steps/step-02-skeleton.md](steps/step-02-skeleton.md) | — |
| Step 3 | 应用设计核心 | [steps/step-03-design-core.md](steps/step-03-design-core.md) | 自创变量 → 退回 |
| Step 4 | 组装组件 | [steps/step-04-components.md](steps/step-04-components.md) | <3种组件 → 退回 |
| Step 4.5 | 多模态配图 | [steps/step-4.5-images.md](steps/step-4.5-images.md) | 漏图 → 退回 |
| Step 5 | 注入内容 + 渲染 | [steps/step-05-render.md](steps/step-05-render.md) | — |
| Step 6 | 质量门禁 | [steps/step-06-qa.md](steps/step-06-qa.md) | 不通过 → 退回 |

### 输入方式

| 方式 | 格式 | 来源 | 详见 |
|:-----|:-----|:-----|:-----|
| 方式 A | 结构化 Markdown（含 Frontmatter） | 其他 skill | [references/input-spec.md](references/input-spec.md) |
| 方式 B | 纯结构化 YAML（`*_结构化数据.yaml`） | pop-shared-reader | [references/input-spec.md](references/input-spec.md) |
| 方式 C | JSON/YAML 数据结构 | 对话上下文 | [references/input-spec.md](references/input-spec.md) |

---

## 红线

| # | 红线 |
|:-:|:-----|
| R1 | Phase 0 简报中规划的配图全部生成（数量 >= 规划值） |
| R2 | 所有配图使用 `python3 scripts/generate_image.py` 生成（非 GenerateImage 工具 / 非 SVG 占位 / 非纯色块） |
| R3 | 所有配图使用 Base64 Data URL 嵌入，无 `file://` 或相对路径引用 |
| R4 | 角色列表有对应角色肖像配图（触发规则有 → 必须有） |
| R5 | Hero 存在 → 有 Hero 背景配图 |
| R6 | 名场面/场景数据存在 → 有场景配图 |
| R7 | 产出只留摘要 — HTML 生成后对话中不粘贴源码。说"已写入 {路径}。预览核心：{首页设计风格 + 关键视觉元素}。需调整告诉我。" |

### Drop Check（前置闸门）

在开始 Step 1 之前，逐条确认：
```
[ ] 设计简报已完成？包含全部 5 项（素材来源、页面方案、视觉方向、配色方案、配图规划）？
[ ] 配图规划覆盖了所有硬性触发项（角色/名场面/Hero/画廊）？
[ ] 配图数量 >= min_images(data) 计算值？
[ ] 视觉方向写了理由（非盲选）？
[ ] 上游素材格式可解析（非空/非乱码）？
```
任一条不通过 → 回到 Phase 0 补全，不得继续。

---

## 核心流程

执行时严格按照 `steps/` 中的 8 个文件逐级推进：

1. **[Phase 0](steps/phase-0-design-brief.md)** — 素材理解 → 页面结构规划 → 配图规划(硬性触发) → 视觉方向 → 配色字体 → 输出设计简报
2. **[Step 1](steps/step-01-content-type.md)** — 内容类型检测，确定页面类型 + 推荐骨架
3. **[Step 2](steps/step-02-skeleton.md)** — 选择渲染骨架 A/B/C/D，骨架 D 需遵守中文长文参数
4. **[Step 3](steps/step-03-design-core.md)** — 应用 `references/design/DESIGN_CORE.md` 的 CSS 变量/间距/字体体系
5. **[Step 4](steps/step-04-components.md)** — 从 `references/design/components.md` 组装组件 (3-6 种)
6. **[Step 4.5](steps/step-4.5-images.md)** — 硬性配图执行：`generate_image.py` 生图 → Base64 嵌入
7. **[Step 5](steps/step-05-render.md)** — 注入内容 + 数据映射 + 渲染输出
8. **[Step 6](steps/step-06-qa.md)** — 质量门禁：CSS/组件/响应式/反模式 全量检查

## 输出规范

详见 [references/output-spec.md](references/output-spec.md)。核心要求：自包含单文件 HTML，UTF-8，所有 CSS/JS 内联，Base64 配图嵌入，零 emoji。

## 参考文件

| 文件 | 内容 |
|:-----|:-----|
| [references/design/DESIGN_CORE.md](references/design/DESIGN_CORE.md) | CSS 变量/间距/字体/颜色/背景/卡片设计系统 |
| [references/design/components.md](references/design/components.md) | 13 种组件 HTML+CSS 参考（含内容互联） |
| [references/design/responsive.md](references/design/responsive.md) | 三断点响应式规范 |
| [references/templates.md](references/templates.md) | 8 种模板目录说明 |
| [references/input-spec.md](references/input-spec.md) | 三种输入方式详解 |
| [references/output-spec.md](references/output-spec.md) | 输出文件规范 |
| [references/responsibility.md](references/responsibility.md) | 唯一责任原则 + 协作流程 |
| [references/wrong-examples.md](references/wrong-examples.md) | 常见错误做法对照 |
| [references/errors.md](references/errors.md) | 10 种异常场景处理 |
| [references/tooling/](references/tooling/) | Node.js 自动化管线工具（analyzer/style-engine/injector/palette/QA） |

---

## 内部结构

```
pop-shared-html/           ← 唯一 HTML 渲染引擎
├── SKILL.md                 ← 本文（v2.5）
├── skill.json               ← 元数据
├── CHANGELOG.md              ← 版本变更记录
├── steps/                   ← 8 个 SOP 步骤文件
│   ├── phase-0-design-brief.md
│   ├── step-01-content-type.md
│   ├── step-02-skeleton.md
│   ├── step-03-design-core.md
│   ├── step-04-components.md
│   ├── step-4.5-images.md
│   ├── step-05-render.md
│   └── step-06-qa.md
├── references/              ← 参考规范与工具
│   ├── design/              ← 设计系统（DESIGN_CORE / components / responsive）
│   ├── tooling/             ← Node.js 自动化管线工具
│   ├── templates.md
│   ├── input-spec.md
│   ├── output-spec.md
│   ├── responsibility.md
│   ├── wrong-examples.md
│   └── errors.md
├── scripts/
│   └── generate_image.py    ← Seedream 生图脚本（Key 内嵌第27行）
├── templates/               ← 场景骨架参考（8种类型）
├── qa/
│   └── config.js            ← QA 共享配置（Kimi API Key）
└── .gitignore
```

---

> 版本：v2.5.0 | 上游预写 image_prompt | 硬性配图触发 | 三层叠图 Hero | 长文阅读器 | 内容互联
