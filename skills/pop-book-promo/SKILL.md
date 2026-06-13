---
name: pop-book-promo
display_name: 多模态营销物料生成
description: 当用户说"生成营销物料/做宣传页/做角色海报/名场面海报/金句卡/四格漫画/立绘画廊/营销HTML/书宣物料/推书海报"时启用。从拆书数据（角色/场景/金句）出发，PRD 先行 → 设计哲学驱动 → 生图 + 定制 HTML。
version: 3.1.0
pipeline:
  upstream: [pop-reader-making]
  downstream: []
---

# pop-book-promo · 多模态营销物料生成 v3.1

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

### ① 火山引擎 Seedream（生图用）
内嵌在 `scripts/generate.py` 第 26 行：
```
SEEDREAM_API_KEY = "b597f4e5-2370-4bdf-875f-5ae43e43c52b"
```
覆盖方式：设置环境变量 `ARK_API_KEY` 或 `MODEL_IMAGE_API_KEY`

### ② Moonshot Kimi 2.5（快照/检修用）
内嵌在 `scripts/generate.py` 第 29 行：
```
KIMI_API_KEY = "sk-9FVFhuRY5B8jvwzlNb1HseqDmUvfOa2LYvN7We9EVXPMaXxT"
```
覆盖方式：设置环境变量 `KIMI_API_KEY`

> ⚠️ **如果换电脑、重装、迁移 skill，先来这里抄 key。**

---

## 执行流程（SOP）

### 模式 A：PRD 先行工作流（主推 ✅）

> **核心原则：先想明白要做什么，再动手。每一步出文档，迭代修正，最后出成品。**

#### 第①步：理解数据

**读什么：** 用户提供的 JSON 数据文件：
- `scenes.json` — 名场面场景列表
- `profile.json` — 角色深度档案
- `quotes.json` — 金句列表
- `characters.json` — 角色列表

**做什么：**
- 数据类型？场景集/角色集/金句集/混合？
- 数据量？几条？适合什么形式？
- 情感基调？温馨/悲壮/激烈？→ 决定视觉方向

**产出：** 数据理解摘要。

**❌ 门禁：** 数据为空或格式不对 → **退回**。要求上游提供正确的 JSON 数据。

---

#### 第②步：写 PRD（《物料设计文档》.md）

**读什么：** 第①步的数据理解摘要。

**做什么：** 输出以下格式的 PRD 文档——**每一步写出后向老板确认再往下走**：

```markdown
# 《书名》· 营销物料设计文档

## 1. 数据摘要
- 物料类型：四格漫画 / 金句卡 / 角色画廊 / 名场面海报 / 综合展示
- 条目数：N 条
- 核心情绪：[温馨/悲壮/激烈/悬疑]
- 目标受众：[小红书读者/公众号粉丝/推书帖读者]
- 发布场景：[朋友圈/小红书/官网/公众号]

## 2. 视觉方向
选择一种设计哲学：
- 方向：[水墨丹青 / 光影剧场 / 极简书卷 / 绮丽画集]
- 理由：[一句话说明]

## 3. 设计系统
- 主色：#xxxxxx（占 70%）
- 辅色：#xxxxxx（占 25%）
- 强调色：#xxxxxx（占 5%）
- 字体：inter / system-ui
- 间距体系：4px 模数

## 4. 内容编排
| 序号 | image_prompt | 配文 | 排版位置 |
|:----:|:-------------|:-----|:---------|
| 1 | …… | …… | 左图右文 |
| 2 | …… | …… | 全幅背景 |
```

**产出：** PRD 文档 `.md` 文件。

---

#### 第③步：生成图片

**读什么：** PRD 中的 image_prompt 列表。

**做什么：** 用 `generate.py` 逐张生图。

```bash
python3 scripts/generate.py --mode image \
  --prompt "Chinese xianxia novel scene: ..." \
  --output assets/scene1.png
```

**门禁：**
- [ ] 每张图片生成成功
- [ ] 图片无模糊/变形
- ❌ 生图失败 → 检查 API Key 是否过期，重试 3 次，仍失败则报错。

**产出：** `.png` 图片文件 + data URL。

---

#### 第④步：编写定制 HTML

**读什么：** PRD 设计系统 + 第③步生成的图片 data URL。

**做什么：** 严格按 PRD 设计系统写定制 HTML（非套模板）。

**产出规范（零外部依赖）：**
- ❌ 禁止 `@import url(...)` 引用外部 CSS/字体
- ❌ 禁止 `<link href="...">` 引用外部资源
- ❌ 禁止 `<script src="...">` 引用外部 JS
- ✅ 图片用 data URL 嵌入
- ✅ 字体用系统字体栈
- ✅ 标签闭合，双击可开

**❌ 门禁：** 搜索 `@import` / `https://` / `http://` 发现外部依赖 → **退回**。零外部依赖是硬底线。

**产出：** 定制 HTML 文件。

---

#### 第⑤步：精修

**读什么：** 第④步的 HTML 文件。

**做什么：** 逐项检查质量清单。

- [ ] 颜色不超过 4 种
- [ ] 强调色只用在一处
- [ ] 间距统一，使用标准尺度
- [ ] 留白 > 内容区域
- [ ] 字体层级清晰
- [ ] hover 状态精致但不浮夸
- [ ] 像专业出版物，不像"做出来的"
- [ ] 零外部依赖（`@import` / `https://` / `http://`）
- [ ] font-weight ≤ 600
- [ ] 纯黑 `#000` → `#1a1a1a`，纯白 `#fff` → `#f2f2f2`

**❌ 门禁：** 以上任意一项不通过 → **退回** 修改。

**产出：** 最终版定制 HTML。

---

### 模式 B：旧模板管线（向后兼容 ⚠️ Deprecated）

当不需要设计哲学和 PRD 时，直接用旧模板快速出稿：

```bash
python3 scripts/generate.py --mode comic --input examples/scenes.json --output ../书名_四格漫画.html
python3 scripts/generate.py --mode scroll --input examples/profile.json --output ../书名_人物画卷.html
python3 scripts/generate.py --mode scenes --input examples/scenes.json --output ../书名_名场面.html
python3 scripts/generate.py --mode quote --input examples/quotes.json --output ../书名_金句卡.html
python3 scripts/generate.py --mode gallery --input examples/characters.json --output ../书名_立绘画廊.html
```

**参数说明：**
| 参数 | 必填 | 说明 |
|:-----|:----:|:------|
| `--mode` | ✅ | image / comic / scroll / scenes / quote / gallery |
| `--backend` | ❌ | seedream（默认）或 openrouter |
| `--input` / `-i` | ⚠️ | 输入 JSON（模板模式需要） |
| `--output` / `-o` | ✅ | 输出路径 |
| `--prompt` / `-p` | ⚠️ | 出图提示词（仅 image 模式） |
| `--model` | ❌ | 图像模型 ID（默认: doubao-seedream-5-0-260128） |
| `--max-items` | ❌ | 前 N 项，冒烟测试 |
| `--reference-dir` | ❌ | 角色参考图目录 |
| `--save-assets` | ❌ | 同时保存图片到目录 |

---

## 设计哲学

> **核心原则：先定义视觉语言，再动手写 HTML。不走"先布局再调色"的弯路。**

### 视觉方向（四选一）

| 方向 | 适合 | 色板特征 | 氛围 |
|:-----|:-----|:---------|:-----|
| **水墨丹青** | 仙侠/古风/历史 | 墨色/宣纸色/朱砂点睛 | 温润克制，文字即主体 |
| **光影剧场** | 名场面/高燃/情感 | 深色底+发光强调 | 戏剧性，电影感 |
| **极简书卷** | 金句卡/人物简介 | 浅灰底+少量彩色 | 干净现代，内容突出 |
| **绮丽画集** | 角色画廊/综合展示 | 暖米色+档案标签色 | 丰富有层次 |

### 颜色体系

| 要素 | 规则 |
|:-----|:-----|
| 主色 | 1 个，占 70% 面积 |
| 辅色 | 1-2 个，占 25% |
| 强调色 | 1 个，占 5% |
| 文字色 | 2 层级（主文/辅助） |
| ❌ 禁用 | 彩虹色标签、超过 4 种不相关颜色 |

### 间距体系
```
尺度：4px → 8px → 12px → 16px → 24px → 32px → 48px → 64px → 96px
卡片内：20-24px | 卡片间：12-32px | 段落：16-24px | 区块：48-80px | 页边：24-48px
留白宁可多不可少
```

### 字体层级
```
主字体：Inter 或系统无衬线
等宽字体：JetBrains Mono
字号：大标题 40-56px / 标题 24-32px / 正文 14-16px / 辅助 11-13px / 标签 10-12px
禁用：font-weight > 600 | 超过 3 种权重 | 纯黑/纯白
```

### 排版规则
```
网格对齐：所有元素对齐隐式网格，同行卡片等高
留白：页面顶部 > 底部，段落间 > 行内
对比度：正文 7:1，辅助文字 4.5:1
边框：1px solid，或完全不用
圆角：不超过 12px
阴影：不允许，或极其克制
```

---

## 出图提示词规范

> ⚠️ **LLM 必须为每条数据编写 `image_prompt` 字段。**

### 黄金三原则

1. **写视觉描述，不是剧情**
2. **中英结合** — 开头用英文前缀，细节可混写
3. **固定尾部** — 末尾追加 `, traditional Chinese ink wash aesthetic, cinematic composition`

### 对比

| ❌ 差（剧情描述） | ✅ 好（视觉描述） |
|:---|:---|
| 乔晚穿到修真界，发现自己成了白月光的替身 | Chinese xianxia dramatic scene: young woman in white robes kneeling on stone floor, facing imposing figure in dark blue robes, golden light through lattice windows, tense atmosphere |

---

## 数据格式

### scenes.json
```json
{
  "novel": "书名",
  "scenes": [
    {
      "id": 1, "title": "场景标题", "chapter": "第X章",
      "description": "场景详细描述", "dialogue": "关键对白",
      "emotion": "情绪基调", "characters": ["角色A", "角色B"],
      "image_prompt": "LLM 预编写的出图提示词"
    }
  ]
}
```

### profile.json / quotes.json / characters.json
详见 `examples/` 目录下的示例文件。

---

## WRONG 示例

| ❌ 错误做法 | 问题 | ✅ 正确做法 |
|:-----------|:-----|:------------|
| 不写 PRD 直接开始生图写 HTML | 没有方向，返工率高 | PRD 先行，确认后再执行 |
| image_prompt写"主角在打架"这种剧情描述 | 模型无法生成 | 写视觉描述——场景、光线、构图、风格 |
| HTML 引用 Google Fonts CDN | 断网无法渲染 | 全部用系统字体栈，零外部依赖 |
| 颜色超过 4 种，五彩斑斓 | 视觉噪音，不专业 | 主色1+辅色1-2+强调色1，不超过4种 |
| 直接用纯黑 `#000` 和纯白 `#fff` | 太刺眼 | `#1a1a1a` / `#f2f2f2` |

---

## 异常与边界条件

| # | 异常场景 | 处理方式 |
|:-:|:---------|:---------|
| 1 | API Key 过期/报 401 | 检查环境变量 `ARK_API_KEY`/`KIMI_API_KEY` 是否覆盖 |
| 2 | 生图 API 返回空/报错 | 重试 3 次，每次间隔 2s；仍失败则报错，不走降级 |
| 3 | 输入 JSON 格式错误/字段缺失 | 退回，要求上游修复 JSON |
| 4 | PRD 写完后老板不确认 | 停在 PRD 阶段，不继续执行——不做无确认的交付 |
| 5 | 数据量极大（>50 个角色/场景） | 只生成 Top N（按重要性），标注未生成列表 |
| 6 | 用户直接要求模式 B（旧模板） | 确认"是想快速出稿？"是 → 走模式 B；否 → 引导走模式 A |
| 7 | `generate.py` 报 `module not found` | 检查 Python 环境和依赖，缺啥装啥 |
| 8 | HTML 输出到只读目录 | 改写入 `d:\popwave-skills\` |

---

## 目录结构

```
pop-book-promo/
├── skill.json                  ← 元数据（v3.0.0）
├── SKILL.md                    ← 本文
├── preflight.py                ← 前置检查
├── scripts/
│   ├── generate.py             ← 生图引擎（--mode image 为主，模板兼容）
│   ├── build_heroine_card.py   ← 女主角 IP 卡
│   ├── demo_from_title.py      ← 从书名演示
│   └── autocheck.py            ← 自检
├── templates/                  ← 5 个 HTML 模板（模式 B 用）
├── examples/                   ← 示例数据
└── skills/
    └── novel-ip-demo/
```

---

> 版本：v3.1.0 | 模式 A：PRD → 设计哲学 → 生图 → 定制 HTML | 模式 B：旧模板管线（向后兼容）
