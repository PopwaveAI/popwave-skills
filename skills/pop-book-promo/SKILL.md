---
name: pop-book-promo
display_name: 多模态营销物料生成
description: 从拆书数据（角色/场景/金句）出发，PRD 先行 → 设计哲学驱动 → 生图 + 定制 HTML。版本 3.0.0
version: 3.0.0
scenario: multimodal-marketing
dependencies:
  required:
    - "python3"
    - "templates/ (5 个 HTML 模板，模式 B 用)"
    - "（generate.py 仅用 Python 标准库，无需 pip install）"
  optional:
    - "参考图目录（角色 PNG，提升一致性）"
    - "style_bible 字段（视觉规范注入）"
    - "OPEN_ROUTER_API_KEY（仅切换 openrouter 后端时需要）"
    - "KIMI_API_KEY（快照/检修用，已内嵌可选环境变量覆盖）"
inject_context:
  - "scenes.json — 名场面场景列表"
  - "profile.json — 角色深度档案"
  - "quotes.json — 金句列表"
  - "characters.json — 角色列表"
  - "style_bible 字段（跨场景画风一致性）"
produces:
  - "PRD 设计文档 (.md)"
  - "单张图片或图集 (.png)"
  - "定制营销页面 HTML (.html)"
---

# pop-book-promo · 多模态营销物料生成

> **版本**: 3.0.0
> **路线切换**: 从"输入JSON→套模板"升级为 **PRD 先行 → 设计哲学驱动 → 定制 HTML**。旧模板管线作为模式 B 保留。

---

## 🔑 API Key（本 skill 的命根子）

### ① 火山引擎 Seedream（生图用）

内嵌在 `scripts/generate.py` 第 26 行：

```
SEEDREAM_API_KEY = "b597f4e5-2370-4bdf-875f-5ae43e43c52b"
```

**获取方式**：火山方舟控制台 → API Key 管理 → 创建/查看
**覆盖方式**：设置环境变量 `ARK_API_KEY` 或 `MODEL_IMAGE_API_KEY`

### ② Moonshot Kimi 2.5（快照/检修用）

内嵌在 `scripts/generate.py` 第 29 行：

```
KIMI_API_KEY = "sk-9FVFhuRY5B8jvwzlNb1HseqDmUvfOa2LYvN7We9EVXPMaXxT"
```

**用途**：对生成结果做视觉快照、质检复查
**覆盖方式**：设置环境变量 `KIMI_API_KEY`

> ⚠️ **如果换电脑、重装、或者迁移 skill，记得先来这里抄 key。**

---

## 概述

**核心定位**：把拆书数据做成可传播的营销物料。

**两条路线**：

| | 模式 A（主推 ✅） | 模式 B（⚠️ Deprecated — 向后兼容） |
|:---|:---|:---|
| 工作方式 | PRD → 设计哲学 → 定制 HTML | 输入 JSON → 注入预制模板 |
| 质量 | ⭐⭐⭐⭐⭐ 每页量身定做 | ⭐⭐⭐ 固定布局 |
| 速度 | 慢（出图 + 写 HTML） | 快（一键生成） |
| 适用场景 | 正式发布 / 品牌物料 | 测试 / 批量快速出稿 |

---

## 模式 A：PRD 先行工作流（推荐）

> **核心原则**：先想明白要做什么，再动手。每一步出文档，迭代修正，最后出成品。

### 工作流

```
① 理解数据                       ← 读入 scenes / quotes / characters / profile
    ↓
② 写 PRD                         ← 《物料设计文档》.md
    ├── 数据摘要（有什么内容）
    ├── 物料目标（发在哪儿？给谁看？）
    ├── 视觉方向选择（见下方 设计哲学）
    ├── 设计系统（颜色/字体/间距/排版）
    └── 内容编排（每张图配什么文字）
    ↓
③ LLM 生成图片                    ← python3 generate.py --mode image --prompt "..." --output assets/s1.png
    ↓
④ LLM 编写定制 HTML               ← 按 PRD 的设计系统写完整 HTML，嵌入图片
    ↓
⑤ 精修                            ← 检查对齐/间距/对比度/字体渲染
```

### 第①步：理解数据

读取输入的结构化数据，搞清楚：

- **数据类型**：场景集？角色集？金句集？还是混合？
- **数据量**：几个条目？适合做成什么形式？
- **情感基调**：温馨？悲壮？激烈？这决定视觉方向

### 第②步：写 PRD

格式如下——每一步写出后向老板确认再往下走：

```markdown
# 《书名》· 营销物料设计文档

## 1. 数据摘要
- 物料类型：四格漫画 / 金句卡 / 角色画廊 / 名场面海报 / 综合展示
- 条目数：N 条
- 核心情绪：[温馨/悲壮/激烈/悬疑]
- 目标受众：[小红书读者/公众号粉丝/推书帖读者]
- 发布场景：[朋友圈/小红书/官网/公众号]

## 2. 视觉方向
选择一种设计哲学（见下方"设计哲学"章节）：
- 方向：[水墨丹青 / 光影剧场 / 极简书卷 / 绮丽画集]
- 理由：……

## 3. 设计系统
- 主色：#xxxxxx（占 70%）
- 辅色：#xxxxxx（占 25%）
- 强调色：#xxxxxx（占 5%）
- 字体：inter / system-ui
- 间距体系：遵循 4px 模数
- 卡片/版面布局描述

## 4. 内容编排
| 序号 | 图片提示词（image_prompt） | 配文 | 排版位置 |
|:---:|:---|:---|:---:|
| 1 | …… | …… | 左图右文 |
| 2 | …… | …… | 全幅背景 |
```

### 第③步：生成图片

用 `generate.py --mode image` 逐张生图：

```bash
python3 scripts/generate.py --mode image \
  --prompt "Chinese xianxia novel scene: ..." \
  --output assets/scene1.png
```

每次调用返回图片文件 + 打印 data URL，LLM 可直接嵌入 HTML。

### 第④步：编写定制 HTML

严格按 PRD 设计系统写 HTML：

- **必须遵守设计哲学**（见下方"设计哲学"章节）
- **页面是定制的，不是套模板的**
- **禁止使用固定模板**（除非走模式 B）
- 图片用 data URL 嵌入（`<img src="data:image/png;base64,...">`），零外部依赖
- 交付前验证：标签闭合、零外部 CDN、双击可开

### 第⑤步：精修

逐项检查：
- [ ] 颜色不超过 4 种
- [ ] 强调色只用在一处
- [ ] 间距统一，使用标准尺度
- [ ] 留白 > 内容区域
- [ ] 字体层级清晰
- [ ] hover 状态精致但不浮夸
- [ ] 像专业出版物，不像"做出来的"

### 第⑤步：模式 A 定制 HTML 产出规范

所有通过模式 A 产出的 HTML 必须遵守以下规范（交付前逐项验证）：

**零外部依赖**
- ❌ 禁止 `@import url(...)` 引用外部 CSS/字体
- ❌ 禁止 `<link href="...">` 引用外部资源
- ❌ 禁止 `<script src="...">` 引用外部 JS
- ✅ 图片用 data URL 嵌入（`data:image/png;base64,...`）
- ✅ 字体用系统字体栈（`-apple-system,"PingFang SC","Microsoft YaHei","Noto Sans SC",sans-serif`）
- ✅ 验证方式：搜索 `@import` / `https://` / `http://` 确保无外部引用

**文件完整性**
- ✅ 标签闭合（`</html>` 结尾）
- ✅ 双击可在浏览器直接打开（无 fetch/XHR/require 依赖）
- ✅ 中文编码（`<meta charset="UTF-8">`）

**设计体系一致性**
- ✅ 严格遵守 PRD 中定义的设计哲学（4 选 1）
- ✅ 颜色不超过 4 种，强调色 ≤ 1 个
- ✅ 间距使用 4px 模数
- ✅ font-weight ≤ 600（除非极短标题）
- ✅ 纯黑 `#000` 替换为 `#1a1a1a`，纯白 `#fff` 替换为 `#f2f2f2`

---

## 设计哲学

> 核心原则：**先定义视觉语言，再动手写 HTML。** 不走"先布局再调色"的弯路。

### 1. 视觉方向（四选一）

| 方向 | 适合 | 色板特征 | 氛围 |
|:---|:---|:---|:---|
| **水墨丹青** | 仙侠/古风/历史 | 墨色/宣纸色/朱砂点睛 | 温润克制，文字即主体 |
| **光影剧场** | 名场面/高燃/情感 | 深色底 + 发光强调 | 戏剧性，电影感 |
| **极简书卷** | 金句卡/人物简介 | 浅灰底 + 少量彩色 | 干净现代，内容突出 |
| **绮丽画集** | 角色画廊/综合展示 | 暖米色 + 档案标签色 | 丰富有层次，赏心悦目 |

### 2. 颜色体系

| 要素 | 规则 |
|:----|:-----|
| 主色 | 1 个，占 70% 面积 |
| 辅色 | 1-2 个，占 25%（卡片/面板） |
| 强调色 | 1 个，占 5% — 唯一吸引眼球的地方 |
| 文字色 | 2 层级（主文/辅助） |
| ❌ 禁用 | 彩虹色标签、超过 4 种不相关颜色 |

### 3. 间距体系

```
尺度：4px → 8px → 12px → 16px → 24px → 32px → 48px → 64px → 96px

应用：
  卡片内间距：20-24px
  卡片间距：12-16px（密集）或 24-32px（宽松）
  段落间距：16-24px
  区块间距：48-80px
  页面边距：24-48px
  留白宁可多不可少
```

### 4. 字体层级

```
主字体：Inter 或系统无衬线
等宽字体：JetBrains Mono（数据/代码）

字号：
  大标题：40-56px，weight 200-300，字距 0.03em
  标题（h2）：24-32px，weight 300-400
  标题（h3）：18-22px，weight 400
  正文：14-16px，weight 400，行高 1.6
  辅助：11-13px，weight 400，颜色降级
  标签：10-12px，weight 400，字距 0.05em

禁用：
  font-weight > 600（除非极短标题）
  超过 3 种权重
  纯黑 #000 / 纯白 #fff（用 #1a1a1a / #f2f2f2 代替）
```

### 5. 排版规则

```
网格对齐：所有元素对齐隐式网格，同行卡片等高
留白：页面顶部 > 底部，段落间 > 行内
对比度：正文 7:1，辅助文字 4.5:1
边框：1px solid，比背景深 10-15%，或完全不用边框
圆角：不超过 12px
阴影：不允许，或极其克制（hover +2px 偏移）
```

---

## 模式 B：旧模板管线（向后兼容）

当不需要设计哲学和 PRD 时，可以直接用旧模板快速出稿：

```bash
# 四格漫画
python3 scripts/generate.py --mode comic \
  --input examples/scenes.json \
  --output ../书名_四格漫画.html

# 古风人物画卷
python3 scripts/generate.py --mode scroll \
  --input examples/profile.json \
  --output ../书名_人物画卷.html

# 名场面高光帧
python3 scripts/generate.py --mode scenes \
  --input examples/scenes.json \
  --output ../书名_名场面.html

# 金句分享卡
python3 scripts/generate.py --mode quote \
  --input examples/quotes.json \
  --output ../书名_金句卡.html

# 角色立绘画廊
python3 scripts/generate.py --mode gallery \
  --input examples/characters.json \
  --output ../书名_立绘画廊.html
```

### 参数说明

| 参数 | 必填 | 说明 |
|:----|:----|:------|
| `--mode` | ✅ | 输出模式：image / comic / scroll / scenes / quote / gallery |
| `--backend` | ❌ | 生图后端：`seedream`（默认）或 `openrouter` |
| `--input` / `-i` | ⚠️ | 输入 JSON（模板模式需要） |
| `--output` / `-o` | ✅ | 输出路径（image 模式输出 .png，模板模式输出 .html） |
| `--prompt` / `-p` | ⚠️ | 出图提示词（仅 image 模式需要） |
| `--model` | ❌ | 图像模型 ID（默认: `doubao-seedream-5-0-260128`） |
| `--max-items` | ❌ | 只生成前 N 项，低成本冒烟测试 |
| `--reference-dir` | ❌ | 角色参考图目录 |
| `--save-assets` | ❌ | 同时保存生成图片到目录 |

---

## 数据格式

### scenes.json（名场面场景列表）

```json
{
  "novel": "书名",
  "scenes": [
    {
      "id": 1,
      "title": "场景标题",
      "chapter": "第X章",
      "description": "场景详细描述",
      "dialogue": "关键对白",
      "emotion": "情绪基调",
      "characters": ["角色A", "角色B"],
      "image_prompt": "LLM 预编写的出图提示词（必须有）"
    }
  ]
}
```

### profile.json / quotes.json / characters.json

详见 `examples/` 目录下的示例文件。

---

## 出图提示词规范

> ⚠️ **LLM 必须为每条数据编写 `image_prompt` 字段。**

### 黄金三原则

1. **写视觉描述，不是剧情**
2. **中英结合** — 开头用英文前缀，细节可中英混写
3. **固定尾部** — 每条 prompt 末尾追加 `, traditional Chinese ink wash aesthetic, cinematic composition`

### 好 vs 坏的对比

| ❌ 差（剧情描述） | ✅ 好（视觉描述） |
|:---|:---|
| 乔晚穿到修真界，发现自己成了白月光的替身 | Chinese xianxia dramatic scene: young woman in white robes kneeling on stone floor, facing imposing figure in dark blue robes, golden light through lattice windows, tense atmosphere |

---

## 目录结构

```
pop-book-promo/
├── skill.json                    ← Popwave skill 元数据（v3.0.0）
├── SKILL.md                      ← 本文件
├── preflight.py                  ← 前置检查
├── scripts/
│   ├── generate.py               ← 生图引擎（--mode image 为主，模板兼容）
│   ├── build_heroine_card.py     ← 女主角 IP 卡
│   ├── demo_from_title.py        ← 从书名演示
│   └── autocheck.py              ← 自检
├── templates/                    ← 5 个 HTML 模板（模式 B 用）
├── examples/                     ← 示例数据
└── skills/
    └── novel-ip-demo/
```

---

## 更新日志

### v3.0.0
- **路线变更**: 从强制模板注入 → PRD 先行 + 设计哲学驱动
- generate.py 新增 `--mode image` 纯生图模式
- SKILL.md 新增完整设计哲学体系（5 维度）
- 新增 PRD 文档模板，工作流改为 PRD → 设计 → 生图 → 写 HTML → 精修
- 旧模板管线保留为模式 B（向后兼容）

### v2.1.0
- 生图后端切换为火山引擎 Seedream，API Key 内嵌

### v2.0.0
- 首次重构为统一生成引擎
