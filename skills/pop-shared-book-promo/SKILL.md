---
name: pop-shared-book-promo
display_name: 多模态营销物料生成
description: 当用户说"生成营销物料/做宣传页/做角色海报/名场面海报/金句卡/四格漫画/立绘画廊/营销HTML/书宣物料/推书海报"时启用。从拆书数据（角色/场景/金句）出发，PRD 先行 → 设计哲学驱动 → 生图 + 定制 HTML。
version: 3.1.1
pipeline:
  upstream: [pop-writer-prose]
  downstream: []
---

# pop-shared-book-promo · 多模态营销物料生成 v3.1

> **定位：把拆书数据做成可传播的营销物料。** PRD 先行 → 设计哲学驱动 → 定制 HTML + 生图。旧模板管线作为模式 B 保留（向后兼容）。

---

## 速查表

| 操作 | 模式 | 读什么 | 产出 | 预期耗时 |
|:-----|:-----|:-------|:-----|:---------|
| 定制营销物料 | 模式 A（主推） | scenes.json / profile.json / quotes.json / characters.json | PRD .md + 图片 .png + HTML .html | 10-30min |
| 快速出稿 | 模式 B（兼容） | 同上 | 模板 HTML | 3-5min |
| 生单图 | `--mode image` | prompt | .png | 10-30s/张 |

---

## 🔑 API Key（命根子）

| API | Key | 位置 |
|:----|:----|:-----|
| 火山引擎 Seedream（生图） | `b597f4e5-2370-4bdf-875f-5ae43e43c52b` | `scripts/generate.py` L26，可环境变量 `ARK_API_KEY` 覆盖 |
| Moonshot Kimi 2.5（快照/检修） | `sk-9FVFhuRY5B8jvwzlNb1HseqDmUvfOa2LYvN7We9EVXPMaXxT` | `scripts/generate.py` L29，可环境变量 `KIMI_API_KEY` 覆盖 |

> ⚠️ 换电脑、重装、迁移 skill → 先来这里抄 key。

## 红线

> 硬约束。触犯任一条 = 产出不合格，退回重做。

| # | 红线 |
|:-:|:-----|
| 1 | **零外部依赖**：禁止 `@import`、`<link href>`、`<script src>`、任何 `https://`/`http://` 外部引用 |
| 2 | **PRD 未确认 → 不得生图/写 HTML**：停在 PRD 阶段等老板点头 |
| 3 | **图片必须 data URL 嵌入**：不得引用外部图片 URL |
| 4 | **颜色不超过 4 种**：主色 1 + 辅色 1-2 + 强调色 1 |
| 5 | **font-weight ≤ 600**，禁用纯黑 `#000`、纯白 `#fff` |
| 6 | **生图失败不走降级**：重试 3 次，仍失败则报错 |
| 7 | **输入数据为空/格式错误 → 退回上游**，不强行执行 |

---

## Drop Check（执行前必检）

进入主流程前，必须确认以下 3 项全部通过。任一项不通过 → **终止**，告知原因。

| # | 检查项 | 不通过处理 |
|:-:|:-------|:-----------|
| 1 | 上游数据就绪（至少一个 JSON 文件存在且格式合法） | 退回，要求上游提供数据 |
| 2 | API Key 有效（`preflight.py` 通过） | 检查环境变量覆盖或内嵌 key |
| 3 | 输出目录可写 | 改写到 `d:\popwave-skills\` |

---

## 核心流程

> 详细步骤见 `steps/` 目录下各文件。

| 步骤 | 文件 | 产出 |
|:----:|:-----|:-----|
| ① | `steps/step-01-understand-data.md` | 数据理解摘要 |
| ② | `steps/step-02-write-prd.md` | PRD .md |
| ③ | `steps/step-03-generate-images.md` | .png + data URL |
| ④ | `steps/step-04-write-custom-html.md` | 定制 HTML |
| ⑤ | `steps/step-05-polish.md` | 最终版 HTML |

**模式 B（兼容旧模板）：** 见 `steps/step-b-legacy-mode.md`

---

## 设计哲学

> 详见 `references/design-philosophy.md`。核心：先定义视觉语言，再动手写 HTML。
> 视觉方向四选一：水墨丹青 / 光影剧场 / 极简书卷 / 绮丽画集

---

## 出图提示词规范

> ⚠️ LLM 必须为每条数据编写 `image_prompt` 字段。

**黄金三原则：** (1) 写视觉描述，不是剧情 (2) 中英结合 — 开头英文前缀，细节可混写 (3) 固定尾部追加 `, traditional Chinese ink wash aesthetic, cinematic composition`

| ❌ 差（剧情描述） | ✅ 好（视觉描述） |
|:---|:---|
| 乔晚穿到修真界，发现自己成了白月光的替身 | Chinese xianxia dramatic scene: young woman in white robes kneeling on stone floor, facing imposing figure in dark blue robes, golden light through lattice windows, tense atmosphere |

---

## 数据格式

`scenes.json` 结构：`{ "novel": "书名", "scenes": [{ "id", "title", "chapter", "description", "dialogue", "emotion", "characters":[], "image_prompt" }] }`

其余格式（profile.json / quotes.json / characters.json）详见 `examples/` 目录。

---

## WRONG 示例

| ❌ 错误做法 | 问题 | ✅ 正确做法 |
|:-----------|:-----|:------------|
| 不写 PRD 直接开始生图写 HTML | 没有方向，返工率高 | PRD 先行，确认后再执行 |
| image_prompt写剧情描述"主角在打架" | 模型无法生成 | 写视觉描述——场景、光线、构图、风格 |
| HTML 引用 Google Fonts CDN | 断网无法渲染 | 全部用系统字体栈，零外部依赖 |
| 颜色超过 4 种，五彩斑斓 | 视觉噪音，不专业 | 主色1+辅色1-2+强调色1，不超过4种 |
| 直接用纯黑 `#000` 和纯白 `#fff` | 太刺眼 | `#1a1a1a` / `#f2f2f2` |

---

## 异常与边界条件

| # | 异常场景 | 处理方式 |
|:-:|:---------|:---------|
| 1 | API Key 过期/报 401 | 检查环境变量 `ARK_API_KEY`/`KIMI_API_KEY` 覆盖 |
| 2 | 生图 API 返回空/报错 | 重试 3 次，间隔 2s；仍失败则报错，不走降级 |
| 3 | 输入 JSON 格式错误/字段缺失 | 退回，要求上游修复 JSON |
| 4 | PRD 写完后老板不确认 | 停在 PRD 阶段，不做无确认的交付 |
| 5 | 数据量极大（>50 个角色/场景） | 只生成 Top N（按重要性），标注未生成列表 |
| 6 | 用户直接要求模式 B（旧模板） | 确认"想快速出稿？"是→走模式B；否→引导走模式A |
| 7 | `generate.py` 报 `module not found` | 检查 Python 环境，缺啥装啥 |
| 8 | HTML 输出到只读目录 | 改写入 `d:\popwave-skills\` |

---

## 目录结构

```
pop-shared-book-promo/
├── skill.json / SKILL.md       ← 元数据 + 本文
├── preflight.py                ← 前置检查
├── steps/                      ← 核心流程分步文件
├── references/                 ← 设计哲学等参考文档
├── scripts/                    ← 生图引擎 + 工具脚本
├── templates/                  ← 5 个 HTML 模板（模式 B 用）
├── examples/                   ← 示例数据
└── skills/novel-ip-demo/       ← 子 skill
```

---

## 落盘检查点

| 检查项 | 路径 | 状态要求 |
|:-------|:-----|:---------|
| PRD 文档 | `{书名}-营销物料/PRD-{物料类型}.md` | 已写入，用户已确认 |
| 生成图片 | `{书名}-营销物料/images/*.png` | 已写入，data URL 嵌入 HTML |
| 定制 HTML | `{书名}-营销物料/index.html` | 已写入，零外部依赖验证通过 |
| 模式 B 模板 HTML | `{书名}-营销物料/index.html` | 已写入（向后兼容管线） |

---

## 版本

v3.1.1 | 2026-06-14 | 完整变更记录 → [CHANGELOG.md](CHANGELOG.md)
