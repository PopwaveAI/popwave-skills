---
name: pop-html-anything
description: 当用户说"HTML化/渲染成网页/发布页面/做网站/做展示页/做成HTML/做成网页/前端展示/可视化页面"时启用。HTML 集中化渲染引擎——所有上游 skill 只产出结构化数据，HTML 化统一交由本 skill。内嵌 Seedream 生图 + 三层叠图 Hero + 长文阅读器 + 内容互联。
version: 2.4.0
pipeline:
  upstream: [pop-reader-making, pop-book-promo, pop-YouTubewebbuilder]
  downstream: []
---

# pop-html-anything · 统一 HTML 渲染引擎 v2.4

> **定位：HTML 集中化。**
> 所有 skill 只产出结构化 Markdown，HTML 化统一交由本 skill。
> 本 skill 负责将任何结构化内容渲染为高质量的、视觉一致的单文件 HTML。
> **上游给素材原料 → 本 skill 独立做设计决策 → 输出统一高质量 HTML + 可选的 AI 配图。**

---

## 速查表

| 步骤 | 操作 | 读什么 | 产出什么 | 门禁 |
|:-----|:-----|:-------|:---------|:-----|
| Phase 0 | 素材分析 + 设计决策 | 上游原始素材 | 设计简报 | — |
| Step 1 | 内容类型检测 | 设计简报 | 页面类型 | — |
| Step 2 | 选择渲染骨架 | 页面类型 | 骨架选择 | — |
| Step 3 | 应用设计核心 | 骨架 + DESIGN_CORE.md | CSS 变量引用 | — |
| Step 4 | 组装组件 | 骨架 + components.md | 组件 HTML | — |
| Step 4.5 | 多模态配图（★ 必做） | 设计简报配图规划 | 图片 Base64 嵌入 HTML | ❌ 漏图退回 |
| Step 5 | 注入内容 + 渲染 | 以上全部 | 完整 HTML | — |
| Step 6 | 质量门禁 | 完整 HTML | 验证通过的 HTML | ❌ 不通过退回 |

### 输入方式

| 方式 | 格式 | 来源 |
|:-----|:-----|:-----|
| 方式 A | 结构化 Markdown（含 Frontmatter） | 其他 skill |
| 方式 B | 纯结构化 YAML（`*_结构化数据.yaml`） | pop-reader-making |
| 方式 C | JSON/YAML 数据结构 | 对话上下文 |

---

## ❌ 质量红线（任一条不通过 = 整次不合格）

```
[🔴] Phase 0 简报中规划的配图全部生成（数量 >= 规划值）
[🔴] 所有配图使用 python3 scripts/generate_image.py 生成（非 GenerateImage 工具 / 非 SVG 占位 / 非纯色块）
[🔴] 所有配图使用 Base64 Data URL 嵌入，无 file:// 或相对路径引用
[🔴] 角色列表有对应角色肖像配图（触发规则有 → 必须有）
[🔴] Hero 存在 → 有 Hero 背景配图
[🔴] 名场面/场景数据存在 → 有场景配图
[🔴] ★ **产出只留摘要** — HTML 生成后对话中不粘贴源码。说"已写入 {路径}。预览核心：{首页设计风格 + 关键视觉元素}。需调整告诉我。"
```

---

## 执行流程（SOP）

### Phase 0：素材分析与设计决策（★ 核心）

> **定位：设计决策前置。** 本 skill 不做被动渲染。拿到任何上游素材后，先完成设计简报，再基于它走渲染管线。

#### 0.1 素材理解

**读什么：** 上游原始素材（Markdown / JSON / YAML / 纯文本）。

**问三个问题：**
1. **这是什么内容？**（拆书笔记/角色集/场景集/数据报告/...）
2. **这些数据想表达什么？**（叙事/展示/对比/索引/品牌推广/...）
3. **谁会看这个页面？**（读者/团队/客户/公众/...）

**素材类型对照：**
| 素材类型 | 典型结构 | 来自哪个上游 |
|:---------|:---------|:-------------|
| 拆书方案 + 阅读笔记 + 结构化 YAML | 分卷表 + 章节叙事流 + 角色/势力/设定表 + YAML 章节标注 | pop-reader-making |
| 结构化 YAML 文件（*.yaml） | volume_stats + chapters + entity_cooccurrence | pop-reader-making |
| 角色档案/场景列表/金句集 | JSON 对象数组 | pop-book-promo |
| 频道数据 + 分析报告 | data.json + analysis_ready.json | pop-YouTubewebbuilder |
| 营销物料设计文档 | PRD 格式 | pop-book-promo（模式A）|
| 纯文本/概念描述 | 无结构化 | 用户直接输入 |

**受众对应页面风格：**
| 受众 | 影响 |
|:-----|:-----|
| 读者/粉丝 | 视觉丰富，注重氛围和传播性 |
| 团队内部 | 信息密度高，功能完整，少装饰 |
| 客户/管理层 | 专业整洁，重点突出 |
| 公众 | 首屏吸引眼球，信息层次清晰 |

**产出：** 素材理解摘要。

---

#### 0.2 页面结构规划

**读什么：** 0.1 的素材理解摘要。

**思考框架：**
1. 这个页面最核心的信息是什么？→ 让它最突出
2. 用户会以什么顺序阅读？→ 安排自然的视线流
3. 哪些内容需要交互？→ 折叠/Tab/弹窗
4. 哪些内容需要视觉化？→ 图表/图片/评分条

**页面方案选项：**
| 方案 | 适用场景 | 结构 |
|:-----|:---------|:-----|
| 多页导航型 | 信息量大、需分视图 | 左侧固定导航 + 右侧内容区 |
| 单页流式 | 信息集中、线性阅读 | Hero → Stats → 正文 → 卡片网格 → CTA |
| 沉浸式 | 数据密集型 | 全屏交互区 + 浮动面板 |

**❌ 门禁：** 选了不适合信息量的方案（如 200 条数据用单页流式）→ **退回**。重新规划。

**产出：** 页面结构方案。

---

#### 0.2.5 配图规划（★ 硬性触发，不可跳过）

> **废掉了"思考决定"模式。改为硬性触发规则：**
> 只要素材包含某些类型的数据，就**必须**配图，没有"可能不需要"这个选项。

**硬性触发规则（触发即必须配，无豁免）：**

| 素材包含的数据 | 触发的配图 | 数量下限 | 理由 |
|:--------------|:-----------|:---------|:-----|
| 角色/人物列表 | 角色肖像卡 | **每角色 1 张** | 角色页面没有角色图 = 不合格 |
| 名场面/场景数据 | 场景插图 | **每场景 1 张** | 名场面没有图 = 名不副实 |
| Hero / 首屏 Banner 概念 | Hero 背景图 | **1 张** | Hero 区没图 = 空洞 |
| 条目画廊 | 条目配图 | **每条目 1 张** | 画廊无图 = 欺骗 |
| 全文本内容（无以上数据） | 装饰性概念图 | **至少 1 张** | 纯文字页面需要视觉锚点 |

**配图数量计算：**
```python
def min_images(data):
    count = 0
    if has_hero or has_scenes: count += 1          # Hero背景
    if has_characters: count += len(characters)     # 每角色1张
    if has_moments: count += len(moments)           # 每名场面1张
    if has_gallery_items: count += len(gallery)     # 每画廊条目1张
    if count == 0 and has_long_text: count = 1      # 纯文字至少1张
    return count
```

**产出：** 配图清单（位置 + 数量 + 风格）。

**❌ 门禁：** 素材包含角色/场景/Hero 数据，但简报中没有对应配图规划 → **Phase 0 违规**，退回修正。

---

#### 0.3 视觉方向选择

**读什么：** 素材情感基调 + 0.2 的页面方案。

**选择（必须写理由，禁止盲选）：**
| 方向 | 适合内容 | 气质关键词 |
|:-----|:---------|:-----------|
| **暖色叙事** | 拆书笔记、角色画廊、长文阅读 | 温润、亲近、有温度 |
| **数据专业** | 仪表盘、评估报告、数据看板 | 干净、专业、高效 |
| **深色沉浸** | 小说阅读、知识图谱、百科 | 深邃、专注、科技感 |
| **品牌展示** | 营销落地页、创作者品牌页 | 大气、精致、有个性 |
| **撞色活力** | 游戏、创意、潮流内容 | 大胆、活力、年轻 |

**决策树：**
```
素材是虚构/叙事/阅读类内容？ → 暖色叙事 或 深色沉浸
素材是科技/专业/数据类？     → 数据专业
素材是品牌/营销/展示类？     → 品牌展示
素材是年轻/创意/潮流类？     → 撞色活力
```

**❌ 门禁：** 选了方向但不写理由 → **退回**。禁止盲选。

**产出：** 视觉方向选择 + 理由。

---

#### 0.4 配色 + 字体决策

**读什么：** 0.3 的视觉方向。

**Step 1：定温度**
```
中文/古典/文化/阅读类 → 暖色底（H≈30-40°）
科技/SaaS/数据仪表盘 → 冷色底（H≈210-260°）
医疗/教育/儿童 → 中性高亮度
```

**Step 2：选主点缀色 + 二次色**
- 不超过 2 个高饱和色
- 中式/叙事类推荐：朱砂 `#b6322c` + 鎏金 `#b8924a`

**Step 3：饱和度收一档** — HSL 的 S 值减 10-15%，L 值减 5%

**Step 4：确定 CSS 变量值** — 只改 `--primary` 和 `--primary-light`

**字体方案（三选一）：**
| 方案 | 展示字 | 正文字 | 适合 |
|:-----|:-------|:-------|:-----|
| 标准无衬线 | Inter | Inter | 数据/专业页面 |
| 衬线+无衬线 | Playfair Display | Inter | 叙事/品牌页面 |
| 等宽主导 | JetBrains Mono | Inter | 科技/数据页面 |

**产出：** 配色方案 + CSS 变量值 + 字体方案。

---

#### 0.5 输出设计简报

**读什么：** 0.1-0.4 的全部决策。

**产出格式：**
```
━━━ 设计简报 ━━━

素材来源：[上游 skill 名称]
内容类型：[拆书笔记/角色集/场景集/...]
目标受众：[读者/团队/客户/公众]

页面方案：[单页流式/多页导航/沉浸式]
页面结构：[页列表]

视觉方向：[方向名称]
选择理由：[一句话理由]

配色方案：
  色温：[暖色底/冷色底/中性]
  --primary: #xxxxxx
  --primary-light: #xxxxxx

字体方案：[方案名称]

配图规划：
  - [位置] x [数量] — 触发规则：[...] → 硬性触发
  合计：[N] 张
  风格：[描述]
━━━━━━━━━━━━━━
```

**❌ 门禁：** 设计简报必须包含配图规划。缺配图规划 → **退回**。

---

### Step 1：内容类型检测

**读什么：** Phase 0 设计简报。

**做什么：** 确定页面类型。
| 内容特征 | 推断类型 | 推荐骨架 |
|:---------|:---------|:---------|
| 有 metrics/概览数字 + 图表 + 列表 | 仪表盘 (Dashboard) | 导航型 |
| 多个条目，每项有名称+属性+状态 | 列表 (List) | 导航型 |
| 单个对象，有头像+属性+多Tab详情 | 详情 (Detail) | 导航型 |
| 多个角色/条目，每项有画像描述 | 卡片集 (Card Deck) | 流式 |
| 大量条目有分类+索引+搜索 | 知识库 (Knowledge Base) | 沉浸式 |
| 事件序列 + 时间线 | 时间线 (Timeline) | 流式/沉浸式 |
| 节点+边的关系数据 | 网络图 (Network) | 沉浸式 |
| 图片+标题+描述的条目 | 画廊 (Gallery) | 流式 |
| 长文本 + 章节目录 + 叙事流 | 阅读器 (Reader) | 长文阅读器 |

**无法确定时：** 条目少（<10）→ 卡片集/画廊；条目多 → 列表/知识库。

**产出：** 页面类型 + 推荐骨架名称。

---

### Step 2：选择渲染骨架

**读什么：** Step 1 的页面类型。

**骨架选项：**

| 骨架 | 结构 | 适用 |
|:-----|:-----|:-----|
| **骨架 A：导航型** | 左侧固定导航(240px) + 右侧内容区（Dashboard/List/Detail/Kanban） | 数据系统/后台 |
| **骨架 B：流式展示型** | Hero → Stats → About → Content Grid → CTA → Footer | 内容/品牌/画廊 |
| **骨架 C：沉浸式** | 全屏交互区 + 浮动面板 + 底部控制栏 | 知识库/图谱/大时间线 |
| **骨架 D：长文阅读器** | 固定顶栏 + 左侧目录 + 正文阅读区(640-760px) + 阅读控制 | 小说/叙事/文章 |

**骨架 D 核心体验参数（中文长文，不可妥协）：**
| 维度 | 值 | 原因 |
|:-----|:-----|:-----|
| 行宽 | 640-760px | 中文阅读金字塔区间 |
| 字号 | 三档可调：15/17/20px | 用户偏好差异大 |
| 行高 | 1.85-2.0 | 方块字需要更大行间 |
| 段首 | 2em text-indent | 中文长文必备 |
| 主题 | 暗/亮/纸 三档 | 适应不同环境 |

**骨架 D 功能优先级：**
| 功能 | 优先级 |
|:-----|:-------|
| 章节列表（sticky 侧栏，上下章导航） | ✅ 必做 |
| 字号调节（三档） | ✅ 必做 |
| 主题切换（暗/亮/纸） | ✅ 必做 |
| 阅读位置记忆（localStorage） | ✅ 必做 |
| 阅读进度条 | ✅ 推荐 |
| 键盘快捷键 ← → | ✅ 推荐 |

**产出：** 选定的骨架 + 理由。

---

### Step 3：应用设计核心

**读什么：** `_design/DESIGN_CORE.md`。

**强制要求：**
1. 使用 DESIGN_CORE 定义的 CSS 变量体系
2. 使用 DESIGN_CORE 定义的间距体系（4px 模数）
3. 使用 DESIGN_CORE 定义的字体层级
4. 使用 DESIGN_CORE 定义的颜色使用规则
5. 根据内容类型选择推荐的背景方案
6. 使用 DESIGN_CORE 定义的卡片设计

**❌ 门禁：** 自行发明变量名而不引用 DESIGN_CORE → **退回**。

**产出：** 引用了 DESIGN_CORE 的 CSS 变量映射。

---

### Step 4：组装组件

**读什么：** `_design/components.md` + Step 2 的骨架。

**强制要求：**
- 从组件库按需取用（至少 3 种，不超过 6 种）
- 组件 class 命名必须与 components.md 一致

**可用组件：**
指标卡片(Metric) / 内容卡片(Card) / 数据表格(Table) / 状态标签(Tag) / Tab切换(Tabs) / 筛选栏(Filters) / 弹窗(Modal) / 按钮(Button) / 加载状态(Skeleton) / 空状态(Empty State) / 内容互联(Content Interconnect)

**❌ 门禁：**
- 组件 < 3 种 → 页面单薄，**退回**
- 组件 class 名与 components.md 不一致 → **退回**

**产出：** 组件 HTML 片段。

---

### Step 4.5：多模态配图（执行阶段）

> **铁律：此步骤不可跳过、不可绕行、不可用任何理由豁免。**
> 如果 Phase 0 规划了配图但 Step 4.5 未执行 → **整次任务不合格。**

**读什么：** Phase 0 设计简报中的配图规划 + 上游 YAML 数据。

**执行步骤：**
1. 读取上游输入的 YAML 结构化数据
2. 从 YAML 中提取角色的 image_prompt + 名场面的 image_prompt + Hero prompt
3. 创建 `assets/` 目录
4. 遍历 prompt 列表，逐张生图：`python3 scripts/generate_image.py --prompt "[prompt]" --output "assets/{name}.png"`
5. 每张图生成后，转 Base64 Data URL
6. 嵌入 HTML 的 `<img>` 标签
7. 验证所有配图已嵌入（无 `file://` 或相对路径）
8. 删除 `assets/` 目录

**Prompt 来源规则：**
| 配图用途 | prompt 来源 | 谁写的 |
|:---------|:-----------|:-------|
| 角色肖像 | YAML 中该角色的 image_prompt 字段 | **上游 skill** |
| 名场面插图 | YAML 中该场景的 image_prompt 字段 | **上游 skill** |
| Hero 背景 | 从素材标题/描述/情绪自动合成 | **本 skill** |
| 装饰性配图 | 从素材整体氛围自动合成 | **本 skill** |

**图片嵌入规则：**
```html
<!-- ❌ 错误：文件路径引用（双击无法看到图片） -->
<img src="assets/hero.png" alt="">

<!-- ✅ 正确：Base64 Data URL 嵌入 -->
<img src="data:image/png;base64,iVBORw0KGgo..." alt="英雄形象">
```

**Hero 图三层叠图法（必须使用）：**
```html
<div class="banner" style="--bg-img: url('data:image/png;base64,...')">
  <!-- Layer 0：同图放大+blur 做兜底背景 -->
  <!-- Layer 1：正图，radial-gradient mask 让边缘消散 -->
  <img src="data:image/png;base64,..." alt="...">
  <!-- Layer 2：底部渐变到背景色，文字可读 -->
  <div class="banner-overlay">
    <h1>标题</h1>
    <p>副标题</p>
  </div>
</div>
```

**铁律：**
1. ❌ 数量不达标 → 不合格
2. ❌ 用 GenerateImage 工具/placeholder SVG/纯色块代替 → 不合格
3. ❌ 生图失败跳过不嵌入 → 不合格（用脚本内置 SVG 占位图兜底）
4. ❌ 引用 `src="assets/..."` 文件路径 → 不合格
5. ❌ Step 4.5 新增/删除 Phase 0 规划的配图 → 不合格

**产出：** 所有配图的 Base64 Data URL + 嵌入 HTML。

**❌ 门禁：** 见上方铁律 5 条，任一条不通过 → 整次不合格。

---

### Step 5：注入内容 + 渲染

**读什么：** 以上所有步骤的产出 + 原始素材内容。

**数据映射规则：**
| 内容元素 | 映射目标 | 组件 |
|:---------|:---------|:-----|
| 标题/名称 | 页面标题/Hero H1 | — |
| 描述/摘要 | Hero 副标题/About 段落 | — |
| 数字指标 | Stats/Metric 卡片 | `.metric` |
| 条目列表 | 数据表格/卡片网格 | `table` / `.card` |
| 状态字段 | Tag 标签 | `.tag` |
| 多 Tab 内容 | Tab 切换 | `.tabs` |
| `volume_stats`（YAML） | 顶部指标卡片+概览区 | `.metric` + Stats |
| `chapters[].tone`（YAML） | 时间线颜色编码 | 按情绪定色 |
| `entity_cooccurrence`（YAML） | 关系网络图 | Canvas 力导向图 |

**产出：** 完整 HTML 文件。

---

### Step 6：质量门禁

**读什么：** Step 5 产出的完整 HTML。

**标准检查清单：**
```
[ ] CSS 变量名全部来自 DESIGN_CORE（不自行发明）
[ ] 至少使用了 3 种组件库中的组件
[ ] 组件 class 名与 components.md 一致
[ ] 响应式三断点已支持
[ ] 双击 HTML 可直接在浏览器打开（零外部依赖）
[ ] 零 emoji（所有视觉标识用 CSS/SVG 实现）
[ ] 没有 <style> @import — 全部内联
[ ] 没有 <script src="..."> 外部库 — 全部内联（Chart.js CDN 除外）
[ ] Chart.js 统一使用 CDN 引用 v4.4.0

<!-- 反模式检查 -->
[ ] 没有 `body { overflow-x: hidden; }`（用 html { overflow-x: clip; }）
[ ] 没有纯色/渐变色块代替配图
[ ] 阅读器中 text-indent 生效（段内\n 未转<br>）
[ ] CSS 中同一颜色值没有在 3 个以上地方硬编码
```

**❌ 门禁：** 标准检查任一项不通过 → **退回** 修改。配图铁律任一项不通过 → 整次不合格。

**产出：** 验证通过的最终 HTML。

---

## 输出规范

```
- 自包含单文件 HTML
- 编码 UTF-8（<meta charset="utf-8">）
- 视口设置（<meta name="viewport" content="width=device-width, initial-scale=1">）
- 所有 CSS 在 <style> 标签内联
- 所有 JS 在 <script> 标签内联
- 字体通过 Google Fonts CDN 或系统字体
- 图标使用内联 SVG（禁止 emoji）
- 图表使用 Chart.js v4.4.0 CDN
- 文件命名：{内容主题}_{类型}.html
```

---

## 输入规范

### 方式 A：结构化 Markdown / YAML（推荐）

```markdown
---
type: dashboard|list|detail|card-deck|knowledge|timeline|network|gallery|reader
title: "页面标题"
description: "页面描述/副标题"
source: "来源 skill 名称"
---
```

### 方式 B：纯结构化 YAML（pop-reader-making 新格式）

```yaml
volume_stats:
  total_chapters: 59
  total_characters: 42
  core_characters: 8
chapters:
  ch1:
    title: "初入战警"
    entities: ["陈昂", "暴风女"]
    tone: "强势登场"
characters:
  - name: "陈昂"
    role: "主角"
    image_prompt: "..."
scenes:
  - title: "帝国大厦宣告"
    image_prompt: "..."
entity_cooccurrence:
  - pair: "陈昂 ↔ 左冷禅"
    chapters: 8
```

> 收到 `.yaml` 文件时自动按此格式解析。`volume_stats` → 指标卡片，`chapters` → 时间线/阅读器，`entity_cooccurrence` → 关系图谱。

### 方式 C：直接数据结构

直接传入 JSON/YAML 数据结构（通过对话上下文）。

---

## 模板目录

```
templates/
├── dashboard/         ← 仪表盘（指标+图表+列表）
├── list-detail/       ← 列表→详情（筛选+表格+Tab）
├── card-gallery/      ← 卡片集（卡片网格+筛选）
├── knowledge-base/    ← 知识库（索引+搜索+详情面板）
├── timeline/          ← 时间线（事件序列+时间轴）
├── network-graph/     ← 网络图（节点+边+浮动详情）
├── promo-landing/     ← 营销落地页（Hero+画廊+CTA）
└── reader/            ← 长文阅读器（章节+正文+阅读设置）
```

> 模板是 LLM 理解"这个类型应该长什么样"的参考，不是复制粘贴。实际输出时基于 DESIGN_CORE + components 重新生成。

---

## 唯一责任原则

> **pop-html-anything 是系统中唯一产出 HTML 的 skill。** 其他所有 skill 不再自行产出 HTML。

**协作流程：**
```
其他 skill（如 pop-reader-making）
  └→ 产出结构化 Markdown + 配套 YAML 结构化数据
       └→ 调用 pop-html-anything
            └→ 本 skill 接管：Phase 0 设计简报 → 选骨架 → 应用设计核心 → 组装组件 → 硬性配图 → 质量门禁
                 └→ 输出最终 HTML
```

---

## WRONG 示例

| ❌ 错误做法 | 问题 | ✅ 正确做法 |
|:-----------|:-----|:------------|
| 不经过 Phase 0 直接开始写 HTML | 没有设计方向，质量不可控 | 先做设计简报，再走渲染管线 |
| 用 GenerateImage 工具手动手工生图 | 不可自动化、不可复现 | 必须用 `python3 scripts/generate_image.py` |
| 配图用文件路径 `src="assets/hero.png"` | 双击 HTML 看不到图 | 必须用 Base64 Data URL 嵌入 |
| 不配角色肖像图/场景插图 | 触发规则应配不配 | 硬性触发规则无豁免，必须配 |
| 自己发明 CSS 变量名 | 维护困难、风格不一致 | 全部引用 DESIGN_CORE |
| 角色有 10 个只配了 5 张图 | 数量不达标 | 每角色 1 张，一张不能少 |
| 用 emoji 代替图标（👍🎨📚） | 不专业、平台兼容差 | 用内联 SVG 做图标 |

---

## 异常与边界条件

| # | 异常场景 | 处理方式 |
|:-:|:---------|:---------|
| 1 | 上游数据为空/格式无法解析 | 退回，要求上游提供正确格式的结构化数据 |
| 2 | `generate_image.py` 脚本缺失 | 检查 `scripts/` 目录是否存在，缺失则报错 |
| 3 | 生图 API 调用失败（网络/Key/限流） | 重试 3 次，每次间隔 2s；仍失败用脚本内置 SVG 占位图兜底 |
| 4 | 用户直接给纯文本（无结构化数据） | 按纯文本做素材分析 → 装饰性概念图(≥1张) → 适合骨架 |
| 5 | 数据量极大（>100 个角色） | 只生成 Top N 配图（按重要性排序），标注未生成部分 |
| 6 | 输出 HTML 文件超过 2MB | 检查是否有超大 Base64 图，考虑压缩或拆分页面 |
| 7 | 角色和场景的 image_prompt 缺失（上游未提供） | 本 skill 自动合成 prompt，标注"prompt 由本 skill 补充" |
| 8 | `assets/` 目录创建失败（权限/磁盘满） | 改用临时目录，清理后再删除 |
| 9 | DESIGN_CORE.md 或 components.md 缺失 | 退回，检查 `_design/` 目录完整性 |
| 10 | 骨架 D（阅读器）的行宽超出 760px | 严格限制 640-760px，超出即退回 |

---

## 内部结构

```
pop-html-anything/           ← 唯一 HTML 渲染引擎
├── SKILL.md                 ← 本文（v2.4）
├── skill.json               ← 元数据
├── scripts/
│   └── generate_image.py    ← Seedream 生图脚本（Key 内嵌第27行）
├── _design/                 ← 设计系统（内部规范）
│   ├── DESIGN_CORE.md       ← CSS 变量/间距/字体
│   ├── components.md        ← 组件库参考（含内容互联）
│   └── responsive.md        ← 响应式规范
├── templates/               ← 场景骨架参考（8种类型）
└── ...
```

---

> 版本：v2.4.0 | 上游预写 image_prompt | 硬性配图触发 | 三层叠图 Hero | 长文阅读器 | 内容互联
