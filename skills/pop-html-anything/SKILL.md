---
name: pop-html-anything
description: "HTML 渲染引擎 + 网站设计师。v2.4 上游预写 image_prompt——角色肖像和名场面 prompt 由上游拆书 skill 产出，本skill只负责执行生图+嵌入。硬性配图触发：有角色必须配肖像、有场景必须配插图。内嵌Seedream生图+三层叠图Hero+长文阅读器+内容互联。"
version: 2.4.0
---

# pop-html-anything · 统一 HTML 渲染引擎

> **定位：HTML 集中化。**
> 所有 skill 只产出结构化 Markdown，HTML 化统一交由本 skill。
> 本 skill 负责将任何结构化内容渲染为高质量的、视觉一致的单文件 HTML。

---

## 设计哲学

**一条原则：上游给素材原料 → 本 skill 独立做设计决策 → 输出统一高质量 HTML + 可选的 AI 配图。**

不再追求"每页独一无二的艺术品"——那是质量不稳定的根源。
本 skill 具备**网站设计师的思维能力**：拿到原始素材后，先理解内容、规划结构、选择视觉方向，然后按确定性管线渲染。既保证下限，也保留上限。

**核心转变：从被动渲染 → 主动设计。**
上游 SKILL 不懂设计、不懂视觉、不用给任何页面规划——那是本 skill 的工作。

视觉上限留给设计决策 + 场景骨架 + Seedream 生图，视觉底线由 `_design/` 保证。

---

## 管线概览

```
输入（上游原始素材 — 拆书笔记 / 角色JSON / 场景JSON / 设计文档 / 纯文本）
  ↓
Phase 0 ─ 素材分析与设计决策 ← ★ 核心
    理解素材内容 → 规划页面结构 → 配图硬性触发→ 选视觉方向 → 定配色/字体 → 产出设计简报
  ↓
Step 1 ─ 内容类型检测
  根据设计简报确定页面类型
  → 仪表盘 / 列表 / 详情 / 卡片集 / 知识库 / 时间线 / 网络图 / 画廊
  ↓
Step 2 ─ 选择渲染骨架
  根据内容类型选择对应的 HTML 页面结构
  → 导航型 / 流式 / 沉浸式（见 template 布局）
  ↓
Step 3 ─ 应用设计核心
  引用 _design/DESIGN_CORE.md 的设计系统
  → CSS 变量 / 间距体系 / 字体层级 / 背景方案
  ↓
Step 4 ─ 组装组件
  从 _design/components.md 按需取用组件
  → 卡片 / 表格 / 标签 / 指标 / Tab / 弹窗 ...
  ↓
Step 4.5 ─ 多模态配图（执行阶段）
  按设计简报执行 Phase 0 规划的配图 → Seedream 生图 → 转 Base64 → 嵌入 HTML
  ↓
Step 5 ─ 注入内容 + 渲染
  将内容填入骨架 + 组件，生成完整 HTML
  ↓
Step 6 ─ 质量门禁
  对照质量检查清单逐条验证
  ↓
输出（自包含单文件 HTML，图片内嵌 Base64）
```

---

## Phase 0：素材分析与设计决策（★ 核心新增）

> **定位：设计决策前置。**
> 本 skill 不做被动渲染。拿到任何上游素材后，先完成一份完整的设计简报（Design Brief），
> 再基于它走后面的渲染管线。

### 工作流

```
收到上游原始素材
  ↓
0.1 ─ 素材理解
  阅读/分析所有输入内容
  问自己三个问题：
  → 这是什么内容？（拆书笔记 / 角色集 / 场景集 / 数据报告 / ...）
  → 这些数据想表达什么？（叙事 / 展示 / 对比 / 索引 / 品牌推广 / ...）
  → 谁会看这个页面？（读者 / 团队 / 客户 / 公众 / ...）
  ↓
0.2 ─ 页面结构规划
  根据内容类型规划页面组成
  → 单页还是多页？（拆书 → 图谱/索引多页；角色集 → 单页画廊）
  → 信息层级怎么排？（最重要的内容放最前面）
  → 需要哪些交互？（筛选 / 搜索 / 弹窗 / Tab 切换）
  ↓
0.2.5 ─ 配图规划（★ 硬性触发）
    按硬性触发规则计算必须配图的数量和位置
    不可跳过、不可豁免
  ↓
0.3 ─ 视觉方向选择
  根据内容气质选择视觉方向
  → 选择 1 个主方向 + 说明理由
  → 不可随意选，必须关联内容气质
  ↓
0.4 ─ 配色 + 字体决策
  确定主色调（只改 --primary 和 --primary-light）
  确定字体方案（展示字 / 正文字 / 等宽字）
  ↓
0.5 ─ 输出设计简报
  产出决策记录（打印到回复中，供后续步骤使用）
  然后进入 Step 1
```

### 0.1 素材理解 —— 三个核心问题

拿到任何上游素材后(无论是 Markdown、JSON、YAML 还是纯文本)，按以下框架分析：

#### ① 这是什么内容？

| 素材类型 | 典型结构 | 来自哪个上游 |
|:---------|:---------|:-------------|
| 拆书方案 + 阅读笔记 + 结构化 YAML | 分卷表 + 章节叙事流 + 角色/势力/设定表 + YAML 章节标注 | pop-reader-making |
| 结构化 YAML 文件（*.yaml） | volume_stats + chapters + entity_cooccurrence | pop-reader-making（新格式）|
| 角色档案/场景列表/金句集 | JSON 对象数组，每项有名称+描述+prompt | pop-book-promo |
| 频道数据 + 分析报告 | data.json + analysis_ready.json | pop-YouTubewebbuilder |
| 营销物料设计文档 | PRD 格式（数据摘要+视觉方向+内容编排） | pop-book-promo（模式 A）|
| 纯文本 / 概念描述 | 无结构化，只有叙事文本 | 用户直接输入 |

#### ② 这些数据想表达什么？

| 内容意图 | 对应页面风格 |
|:---------|:-------------|
| 讲一个故事（叙事/时间线） | 沉浸式时间线，按章节滚动 |
| 展示角色/人物（画廊/档案） | 卡片网格 + 详情弹窗 |
| 对比/评估数据（评分/风险） | 仪表盘 + 表格 + 图表 |
| 索引/百科（大量条目） | 分类索引 + 搜索 + 详情面板 |
| 品牌推广（营销/展示） | Hero + 画廊 + CTA |

#### ③ 谁会看这个页面？

| 受众 | 影响 |
|:----|:-----|
| 读者 / 粉丝 | 视觉丰富，注重氛围和传播性 |
| 团队内部 | 信息密度高，功能完整，少装饰 |
| 客户 / 管理层 | 专业整洁，重点突出，图表辅助 |
| 公众 | 首屏吸引眼球，信息层次清晰 |

### 0.2 页面结构规划

根据素材理解结果，规划最终页面的结构。

**核心原则：** 不要被动填充，要主动编排。

```
思考框架：
1. 这个页面最核心的信息是什么？→ 让它最突出
2. 用户会以什么顺序阅读？→ 安排自然的视线流
3. 哪些内容需要交互才能看到？→ 折叠 / Tab / 弹窗
4. 哪些内容需要视觉化？→ 图表 / 图片 / 评分条
```

#### 多页方案（导航型）

适用于信息量大、需要分视图展示的素材：

| 页码 | 页面 | 承载内容 |
|:----|:-----|:---------|
| 1 | 总览/仪表盘 | 核心指标 + 入口 |
| 2 | 列表/索引 | 所有条目 + 搜索筛选 |
| 3 | 详情/Tab | 单对象深度查看 |
| 4 | 对比/图谱 | 关系 / 对比视图 |
| 5 | 流程/看板 | 阶段管理 |

**示例（拆书素材 → 多页）：**
```
拆书方案 + 阅读笔记 + 实体列表
  → 页面1：书籍总览（分卷表 + 核心指标 + 阅读进度）
  → 页面2：角色索引（所有角色卡片网格 + 筛选）
  → 页面3：卷详情（每卷的叙事流 + 实体列表）
  → 页面4：关系图谱（跨卷角色轨迹 + 设定演变）
```

#### 单页方案（流式展示型）

适用于信息量集中、线性阅读的素材：

```
Hero（标题 + 副标题 + 核心视觉）
  → 关键数据/指标
  → 内容正文/描述
  → 条目卡片网格
  → 号召行动/结束
```

**示例（营销物料 → 单页）：**
```
角色数据 + 场景数据 + 金句
  → Hero：书名 / 作者 / 一句话定位
  → Stats：总角色数 / 名场面数 / 金句数
  → 角色画廊：卡片网格，每张角色卡
  → 名场面精选：带图的卡片
  → 金句滚动条
  → Footer
```

#### 沉浸式方案

适用于数据密集型、需要探索的素材：

```
全屏交互区（图谱 / 时间线 / 地图）
  └→ 浮动详情面板
  └→ 底部控制栏（搜索 / 筛选 / 缩放）
```

**示例（复杂关系数据 → 沉浸式）：**
```
多卷角色 + 跨卷关系
  → 全屏力导向图（按世界着色）
  → 点击节点弹出角色详情
  → 搜索 + 筛选（按世界/势力/角色类型）
```

### 0.2.5 配图规划（★ 硬性触发，不可跳过）

> **废掉了"思考决定"模式。改为硬性触发规则：**
> 只要素材包含某些类型的数据，就**必须**配图，没有"可能不需要"这个选项。

#### 硬性触发规则（触发即必须配，无豁免）

| 素材包含的数据 | 触发的配图 | 数量下限 | 理由 |
|:--------------|:-----------|:---------|:-----|
| 角色/人物列表（有名称、描述） | 角色肖像卡 | **每角色 1 张** | 角色页面没有角色图 = 不合格 |
| 名场面/场景数据（有标题、描述） | 场景插图 | **每场景 1 张** | 名场面没有图 = 名不副实 |
| Hero / 首屏 Banner 概念 | Hero 背景图 | **1 张** | Hero 区没图 = 空洞 |
| 条目画廊（图片+标题+描述） | 条目配图 | **每条目 1 张** | 画廊无图 = 欺骗 |
| 全文本内容（无以上任何数据） | 装饰性概念图 | **至少 1 张** | 纯文字页面需要视觉锚点 |

#### 配图数量计算规则

```python
# 计算必须配图的最小数量
def min_images(data):
    count = 0
    if has_hero or has_scenes: count += 1          # Hero背景
    if has_characters: count += len(characters)     # 每角色1张
    if has_moments: count += len(moments)           # 每名场面1张
    if has_gallery_items: count += len(gallery)     # 每画廊条目1张
    if count == 0 and has_long_text: count = 1      # 纯文字至少1张装饰图
    return count
```

#### 配图规划输出格式（设计简报中必须包含）

```
配图规划：
  - Hero 背景 × 1               ← 必配（Hero存在）
  - 角色肖像 × 8               ← 必配（8个角色）
  - 名场面插图 × 4             ← 必配（4个名场面）
  合计：13 张
  触发规则：角色/名场面数据存在 → 硬性触发
  风格：与视觉方向一致
```

> **违反后果：** 如果素材包含角色/场景/Hero 数据，但设计简报中没有对应配图规划，属于 **Phase 0 违规**，需要退回修正。

---

### 0.3 视觉方向选择

根据内容气质选择方向。**每个方向必须写出选择理由，禁止盲选。**

| 方向 | 适合内容 | 气质关键词 | 色板特征 |
|:-----|:---------|:-----------|:---------|
| **暖色叙事** | 拆书笔记、角色画廊、长文阅读 | 温润、亲近、有温度 | 暖米/宣纸色，深色文字，朱砂点缀 |
| **数据专业** | 仪表盘、评估报告、数据看板 | 干净、专业、高效 | 纯色/浅灰背景，靛蓝主色 |
| **深色沉浸** | 小说阅读、知识图谱、百科 | 深邃、专注、科技感 | 深蓝/深灰背景，发光强调色 |
| **品牌展示** | 营销落地页、创作者品牌页 | 大气、精致、有个性 | 根据品牌色定性 |
| **撞色活力** | 游戏、创意、潮流内容 | 大胆、活力、年轻 | 高饱和撞色，白色背景 |

#### 视觉方向决策树

```
素材是虚构/叙事/阅读类内容？
  → 暖色叙事（温暖）或 深色沉浸（沉浸）
素材是科技/专业/数据类？
  → 数据专业（冷色、高效）
素材是品牌/营销/展示类？
  → 品牌展示（依品牌色定）
素材是年轻/创意/潮流类？
  → 撞色活力（大胆、年轻）
```

### 0.4 配色 + 字体决策

#### Step 1：确定"温度"

配色的第一步不是选颜色，是**定温度**。温度决定了70%的页面氛围，后面所有点缀色都是在这个温度上微调。

```
中文 / 古典 / 文化 / 阅读类 → 暖色底（H≈30-40°，如 #15110d）
科技 / SaaS / 数据仪表盘     → 冷色底（H≈210-260°，如 #0d0d1a）
医疗 / 教育 / 儿童           → 中性高亮度（H任意，L≥85%）
```

> **这一步定错了，后面所有点缀色都救不回来。**

#### Step 2：选主点缀色 + 二次色

- **不超过 2 个高饱和色**
- 主色用于 CTA、强调、活动状态（改 `--primary`）
- 二次色用于副信息、装饰、辅助标签

中式/叙事类推荐组合：
- 朱砂 `#b6322c` + 鎏金 `#b8924a`
- 靛蓝 `#3a4a7a` + 月白 `#e8e4d3`
- 黛青 `#3d5764` + 银朱 `#c54245`

#### Step 3：饱和度收一档

取色板上看着"漂亮"的颜色，放进暗色背景里通常会过亮。
**实操：** 把 HSL 里的 S 值减 10-15%，L 值减 5%。

| 原色 | 调整后 | 差别 |
|:-----|:-------|:-----|
| `#c8332f`（鲜艳朱砂） | `#b6322c`（柔朱砂） | 不像警告色 |
| `#c9a961`（明亮鎏金） | `#b8924a`（内敛鎏金） | 像旧铜器 |

#### Step 4：确定 CSS 变量值

配色只改 `_design/DESIGN_CORE.md` 中 `--primary` 和 `--primary-light` 两个值，其余颜色继承默认。

**字体方案（三选一）：**

| 方案 | 展示字 | 正文字 | 适合 |
|:----|:-------|:-------|:-----|
| 标准无衬线 | Inter | Inter | 数据/专业页面 |
| 衬线 + 无衬线 | Playfair Display | Inter | 叙事/品牌页面 |
| 等宽主导 | JetBrains Mono | Inter | 科技/数据页面 |

> **字体选型铁律：** system-ui 兜底链永远安全。展示型项目优先靠版面、留白、点缀色营造氛围，而非依赖 Web Font。

### 0.5 输出设计简报

完成以上分析后，在回复中输出**设计简报**，然后进入后续渲染管线。

**设计简报模板：**

```
━━━ 设计简报 ━━━

素材来源：[上游 skill 名称]
内容类型：[拆书笔记 / 角色集 / 场景集 / ...]
目标受众：[读者 / 团队 / 客户 / 公众]

页面方案：[单页流式 / 多页导航 / 沉浸式]
页面结构：
  - [页1：内容]
  - [页2：内容]
  - ...

视觉方向：[方向名称]
选择理由：[一句话说明为什么这个方向适合这份素材]

配色方案：
  色温：[暖色底 / 冷色底 / 中性] — H≈[度数]°
  --primary: #xxxxxx（主点缀色，S减10-15%后）
  --primary-light: #xxxxxx（浅色模式）
  背景方案：[纯色 / 渐变 / 网格 / 光影]

字体方案：[标准无衬线 / 衬线+无衬线 / 等宽主导]

配图规划：
  - [位置] × [数量] — 触发规则：[角色数据/场景数据/Hero存在] → 硬性触发
  - [位置] × [数量] — 触发规则：[同上]
  合计：[N] 张（下限由硬性触发规则计算）
  风格：[与视觉方向一致的描述]
━━━━━━━━━━━━━━
```

> **设计简报必须包含配图规划。** 如果素材包含角色/场景/Hero 数据而简报中没有规划，属于 Phase 0 违规。

---

## 第 1 步：内容类型检测

根据 Phase 0 设计简报确定页面类型：

| 内容特征 | 推断类型 | 推荐骨架 | 示例来源 |
|:---------|:---------|:---------|:---------|
| 有 metrics/概览数字 + 图表 + 列表 | 仪表盘 (Dashboard) | 导航型 | prd-builder PRD |
| 多个条目，每项有名称+属性+状态 | 列表 (List) | 导航型 | 资源/人员列表 |
| 单个对象，有头像+属性+多Tab详情 | 详情 (Detail) | 导航型 | KOL 详情 |
| 多个角色/条目，每项有画像描述 | 卡片集 (Card Deck) | 流式 | 拆书角色集 |
| 大量条目有分类+索引+搜索 | 知识库 (Knowledge Base) | 沉浸式 | 百科全书 |
| 事件序列 + 时间线 | 时间线 (Timeline) | 流式/沉浸式 | 叙事分析 |
| 节点+边的关系数据 | 网络图 (Network) | 沉浸式 | 关系图谱 |
| 图片+标题+描述的条目 | 画廊 (Gallery) | 流式 | 营销物料 |
| 长文本 + 章节目录 + 叙事流 | 阅读器 (Reader) | 长文阅读器 | 拆书阅读笔记 |

> **无法确定时**，用内容条数判断：条目少（<10）→ 卡片集/画廊；条目多 → 列表/知识库

---

## 第 2 步：选择渲染骨架

### 骨架 A：导航型（数据系统/后台）

```
左侧固定导航 (240px) + 右侧内容区
├── Dashboard 页（指标卡片 + 图表 + 最近列表）
├── List 页（筛选栏 + 数据表格/卡片网格）
├── Detail 页（详情头部 + Tab 切换）
├── Kanban 页（看板列流程管理）
└── Eval/Compare 页（对比视图）
```

**适用：** 仪表盘 / 列表 / 详情 / 带多视图的数据系统

### 骨架 B：流式展示型（内容/品牌/画廊）

```
自上而下流式布局
├── Hero（标题 / 副标题 / CTA）
├── Stats（关键数字指标）
├── About（介绍/描述文字）
├── Content Grid（卡片网格 / 列表）
├── CTA（号召行动）
└── Footer（版权 + 链接）
```

**适用：** 卡片集 / 画廊 / 时间线 / 品牌页

### 骨架 C：沉浸式（知识库/图谱）

```
全屏沉浸区域 + 浮动控制
├── 侧边/浮动面板（标题 + 详情描述）
├── 主交互区（Canvas/SVG/DOM 网格）
├── 底部控制栏（搜索 / 筛选 / 缩放 / 主题切换）
└── 浮动卡片（点击节点弹出详情）
```

**适用：** 知识库 / 网络图 / 大型时间线

### 骨架 D：长文阅读器（小说/叙事/文章）

```
固定顶部栏（书名 + 阅读设置 + 进度条）
├── 左侧章节目录（sticky 侧边栏或折叠菜单）
├── 正文阅读区（640-760px 行宽，17px 字号，1.85 行高）
│   ├── 章节标题
│   ├── 正文段落（2em 段首缩进）
│   ├── 上下章导航
│   └── 已读标记 + 阅读进度
└── 底部阅读控制（字号调节3档 / 暗亮纸主题切换 / 自动存档）
```

**核心体验参数（中文长文，不可妥协）：**

| 维度 | 值 | 原因 |
|:-----|:-----|:-----|
| 行宽 | 640-760px（约30-36字/行） | 中文阅读金字塔区间 |
| 字号 | 三档可调：15px / 17px / 20px | 用户偏好差异大 |
| 行高 | 1.85-2.0 | 中文方块字需要更大行间气息 |
| 段距 | 1.0-1.2em margin-bottom | 让段落呼吸 |
| 段首 | 2em text-indent | 中文长文必备 |
| 主题 | 暗色/亮色/纸色 三档 CSS variable 切换 | 适应不同阅读环境 |

**功能优先级（必做 / 推荐 / 可选）：**

| 功能 | 优先级 | 说明 |
|:-----|:-------|:-----|
| 章节列表 | ✅ 必做 | sticky 侧栏，上下章导航 |
| 字号调节（三档） | ✅ 必做 | 15/17/20px |
| 主题切换（暗/亮/纸） | ✅ 必做 | CSS variable 方案 |
| 阅读位置记忆 | ✅ 必做 | localStorage 自动存档 |
| 阅读进度条 | ✅ 推荐 | 顶部固定 |
| 键盘快捷键 ← → | ✅ 推荐 | 上下章切换 |
| 已读章节标记 | ✅ 推荐 | 侧栏标记 |
| 章内高亮搜索 | ⚠️ 可选 | 按需 |
| 字数/时长预估 | ⚠️ 可选 | 按需 |

**适用：** 拆书阅读笔记 / 小说正文 / 长篇文章 / 叙事内容

---

## 第 3 步：应用设计核心

**强制引用** `_design/DESIGN_CORE.md`：

1. 使用 DESIGN_CORE 定义的 CSS 变量体系
2. 使用 DESIGN_CORE 定义的间距体系（4px 模数）
3. 使用 DESIGN_CORE 定义的字体层级
4. 使用 DESIGN_CORE 定义的颜色使用规则
5. 根据内容类型选择 DESIGN_CORE 推荐的背景方案
6. 使用 DESIGN_CORE 定义的卡片设计

---

## 第 4 步：组装组件

**强制引用** `_design/components.md`：

从组件库按需取用以下组件（至少使用 3 种）：
- 指标卡片（Metric）— 数据概览
- 内容卡片（Card）— 通用容器
- 数据表格（Table）— 列表数据
- 状态标签（Tag）— 状态标记
- Tab 切换（Tabs）— 多视图
- 筛选栏（Filters）— 数据过滤
- 弹窗（Modal）— 详情弹出
- 按钮（Button）— 操作入口
- 加载状态（Skeleton）— 数据加载
- 空状态（Empty State）— 无数据提示
- 内容互联（Content Interconnect）— 卡片↔正文双向跳转 + hover 浮窗预览

### 组件使用原则

- **至少 3 种，不超过 6 种** — 太少页面单薄，太多信息过载
- **组件 CSS 直接引用 components.md 中的代码**，不要从零写
- **组件 class 命名必须与 components.md 一致**，确保可维护性

---

## 第 4.5 步：多模态配图（执行阶段）

> **铁律：此步骤不可跳过、不可绕行、不可用任何理由豁免。**
> 如果 Phase 0 规划了配图但 Step 4.5 未执行 → **整次任务不合格**。

### 凭据

API Key 内嵌在 `scripts/generate_image.py` 第 27 行：

```
Key: b597f4e5-2370-4bdf-875f-5ae43e43c52b
模型: doubao-seedream-5-0-260128
API:  https://ark.cn-beijing.volces.com/api/v3/images/generations
后备: 环境变量 ARK_API_KEY 或 MODEL_IMAGE_API_KEY
```

### 执行步骤

```
1. 读取上游输入的 YAML 结构化数据
2. 从 YAML 中提取：
   → 角色的 image_prompt（每角色1条预写 prompt）
   → 名场面的 image_prompt（每场景1条预写 prompt）
   → Hero/背景图的 prompt（从素材描述自动生成）
3. 创建 assets/ 目录（如 d:\assets\{项目名}\）
4. 遍历 prompt 列表，逐张生图：
   → python3 scripts/generate_image.py --prompt "[预写prompt]" --output "assets/{name}.png"
5. 每张图生成后，用 Python 读取文件转 Base64 Data URL
6. 嵌入 HTML 的 <img> 标签
7. 验证所有配图已嵌入（最终 HTML 中无 file:// 或相对路径引用）
8. 删除 assets/ 目录（清理临时文件）
```

### Prompt 来源规则

| 配图用途 | prompt 来源 | 谁写的 |
|:---------|:-----------|:-------|
| 角色肖像 | YAML 中该角色的 image_prompt 字段 | **上游 skill**（pop-reader-making 拆书时产出）|
| 名场面插图 | YAML 中该场景的 image_prompt 字段 | **上游 skill**（pop-reader-making 拆书时产出）|
| Hero 背景 | 从素材标题/描述/情绪关键词自动合成 | **本 skill**（Step 4.5 执行时合成）|
| 装饰性配图 | 从素材整体氛围自动合成 | **本 skill**（Step 4.5 执行时合成）|

> **为什么这样做？** 上游 skill 在读原文、理解角色和场景时，是最了解"这角色长什么样、这场面什么氛围"的。让它产出 image_prompt，质量远高于本 skill 在生图时临时编。pop-html-anything 只负责执行生图 + 嵌入，不负责替上游想 prompt。

### 铁律

1. **数量必须达标**：配图数量不得低于 Phase 0 规划的"合计"数值。少1张 = 不合格。
2. **必须用脚本生图**：不允许用 `GenerateImage` 工具、不允许用 placeholder SVG、不允许用纯色渐变块代替。唯一允许的方式是 `python3 scripts/generate_image.py`。
3. **生图失败就地处理**：如果 API 调用失败，脚本内置的 SVG 占位图会作为回退，但不允许跳过整张图的嵌入。
4. **每张图必须写入 HTML**：最终 HTML 中每张配图都必须有对应的 `<img src="data:image/...">` 标签。检测到任何 `src="assets/..."` 文件路径引用 = 不合格。
5. **配图规划锁死**：Step 4.5 不允许新增 Phase 0 未规划的配图，也不允许删除 Phase 0 已规划的配图。

### 与 Phase 0 的关系

| 阶段 | 做什么 | 决策人 | 可跳过？|
|:-----|:-------|:-------|:--------|
| Phase 0.2.5 | 规划：硬性触发规则决定配图清单 | 设计师（LLM）| ❌ 必须做 |
| Step 4.5 | 执行：逐张生图 → Base64 → 嵌入 | 执行者（LLM）| ❌ 必须做 |

### 图片嵌入规则

#### 标准嵌入（基础）

```python
# 将图片转为 Base64 Data URL 的核心逻辑（内嵌在 generate_image.py 的 img_to_data_url 函数中）
def img_to_data_url(img_bytes: bytes) -> str:
    if img_bytes[:3] == b'\xff\xd8\xff':  fmt = "jpeg"
    elif img_bytes[:8] == b'\x89PNG\r\n\x1a\n':  fmt = "png"
    elif img_bytes[:4] == b'RIFF':  fmt = "webp"
    else:  fmt = "png"
    b64 = base64.b64encode(img_bytes).decode()
    return f"data:image/{fmt};base64,{b64}"
```

```html
<!-- ❌ 错误：文件路径引用（双击 HTML 无法看到图片） -->
<img src="assets/hero.png" alt="">

<!-- ✅ 正确：Base64 Data URL 嵌入 -->
<img src="data:image/png;base64,iVBORw0KGgo..." alt="英雄形象">
```

#### Hero 图进阶嵌入（三层叠图法）

当配图用作 Hero 全幅背景时，直接 `object-fit:cover` 会导致图片边缘和深色背景硬切边。**必须使用三层叠图法**：

```html
<div class="banner" style="--bg-img: url('data:image/png;base64,...')">
  <!-- Layer 0：同图放大 + blur 做兜底背景 -->
  <!-- Layer 1：正图，radial-gradient mask 让边缘自然消散 -->
  <img src="data:image/png;base64,..." alt="Hero 描述">
  <!-- Layer 2：底部渐变到背景色，让文字可读 -->
  <div class="banner-overlay">
    <h1>标题文字</h1>
    <p>副标题</p>
  </div>
</div>
```

```css
.banner {
  position: relative; overflow: hidden;
  background: var(--bg); min-height: 60vh;
  display: flex; align-items: center; justify-content: center;
}

/* Layer 0：同图模糊兜底 — 解决图片尺寸不够时的露底问题 */
.banner::before {
  content: '';
  position: absolute; inset: -40px;
  background-image: var(--bg-img);
  background-size: cover; background-position: center;
  filter: blur(40px) brightness(.4) saturate(.7);
  transform: scale(1.15); z-index: 0;
}

/* Layer 1：正图，4 边 radial-gradient 消散 */
.banner img {
  position: relative; z-index: 1;
  width: 100%; height: 100%;
  object-fit: contain;
  -webkit-mask-image: radial-gradient(ellipse 90% 95% at center, black 50%, transparent 100%);
  mask-image: radial-gradient(ellipse 90% 95% at center, black 50%, transparent 100%);
}

/* Layer 2：底部渐变到背景，文字可读 */
.banner-overlay {
  position: absolute; inset: 0; z-index: 2;
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  text-align: center; padding: 40px 24px;
  background: linear-gradient(transparent 35%, rgba(0,0,0,.5) 65%, var(--bg) 95%);
}
.banner-overlay h1 { font-size: clamp(28px, 4vw, 48px); font-weight: 600; color: #fff; }
.banner-overlay p { font-size: 16px; color: rgba(255,255,255,.7); margin-top: 8px; }
```

> **三层叠图法适用场景：** 所有需要"图片小但要撑满大区域"的位置——Hero banner、弹窗大图、卡片背景、章节插图。

### Image Prompt 写作规范

**结构：** `[内容类型]: [视觉描述], [氛围描述], [风格固定尾部]`

**固定尾部推荐：**
- 中国风/小说插画：`, 高品质商业插画, 细节丰富, 光影层次`
- 写实/摄影感：`, professional photography, cinematic lighting, high detail`
- 科技/未来感：`, digital art, clean lines, futuristic aesthetic`

**示例（❌ 差 —— 太笼统）：**
```
一个女孩在森林里
```

**示例（✅ 好 —— 有场景+人物+氛围+风格）：**
```
Chinese fantasy novel character portrait: a young woman in flowing white robes standing in an ancient bamboo forest, dappled sunlight through leaves, ethereal mist at ground level, warm golden lighting, peaceful atmosphere, high quality digital illustration, cinematic composition
```

### 图片质量门禁

```
[ ] 所有 Phase 0 规划中标记为"必须配"的图已全部生成
[ ] 每张图不模糊、不变形
[ ] 每张 <img> 有 alt 描述（无障碍）
[ ] 所有图片使用 Base64 Data URL 嵌入，无文件路径引用
[ ] 首屏图片（Hero）无 loading="lazy"
[ ] 非首屏图片有 loading="lazy"
[ ] 同页面多图风格一致
[ ] 生图失败时使用 generate_image.py 内置的 SVG 占位图（不跳过）
```

---

## 第 5 步：注入内容 + 渲染

将输入的结构化内容映射到骨架和组件中。

### 数据映射规则

| 内容元素 | 映射目标 | 组件 |
|:---------|:---------|:-----|
| 标题/名称 | 页面标题 / Hero H1 | — |
| 描述/摘要 | Hero 副标题 / About 段落 | — |
| 数字指标 | Stats / Metric 卡片 | `.metric` |
| 条目列表 | 数据表格 / 卡片网格 | `table` / `.card` |
| 状态字段 | Tag 标签 | `.tag` |
| 多 Tab 内容 | Tab 切换 | `.tabs` |
| 时间序列 | 时间线组件 | 自定义 |
| `volume_stats`（YAML） | 顶部指标卡片 + 概览区 | `.metric` + Stats 布局 |
| `chapters[].tone`（YAML） | 时间线颜色编码 | 按情绪定色 |
| `chapters[].entities`（YAML） | 角色共现热力图 / 关系图谱 | 自定义 SVG / Canvas |
| `chapters[].events[].type`（YAML） | 事件类型分布图 | 饼图 / 堆叠柱状图 |
| `entity_cooccurrence`（YAML） | 关系网络图 | Canvas 力导向图 |

---

## 第 6 步：质量门禁

**参照** `_design/DESIGN_CORE.md` 的质量检查清单逐条验证。

**另外强制检查：**
```
[ ] CSS 变量名全部来自 DESIGN_CORE（不自行发明变量名）
[ ] 至少使用了 3 种组件库中的组件
[ ] 组件 class 名与 components.md 一致
[ ] 响应式三断点已支持
[ ] 双击 HTML 可直接在浏览器打开（零外部依赖）
[ ] 零 emoji（所有视觉标识用 CSS/SVG 实现）
[ ] 没有 <style> @import — 全部内联
[ ] 没有 <script src="..."> 外部库 — 全部内联（Chart.js CDN 除外）
[ ] Chart.js 统一使用 CDN 引用 v4.4.0

<!-- 配图铁律检查（→ 任一条不通过 = 整次输出不合格） -->
[🔴] Phase 0 简报中规划的配图全部生成（数量 >= 规划值）
[🔴] 所有配图使用 python3 scripts/generate_image.py 生成（非 GenerateImage 工具 / 非 SVG 占位 / 非纯色块）
[🔴] 所有配图使用 Base64 Data URL 嵌入，无 file:// 或相对路径引用
[🔴] 角色列表有对应角色肖像配图（触发规则有 → 必须有）
[🔴] Hero 存在 → 有 Hero 背景配图
[🔴] 名场面/场景数据存在 → 有场景配图

<!-- 反模式检查（违反即不合格） -->
[ ] 没有 `body { overflow-x: hidden; }`（破坏 sticky，用 html { overflow-x: clip; } 替代）
[ ] 没有纯色/渐变色块代替配图（未生图的 SVG 占位方块不合格）
[ ] 阅读器骨架中 text-indent 生效（段内 `\n` 没有被转成 `<br>`）
[ ] CSS 中同一颜色值没有在 3 个以上地方硬编码（用 var() 引用）
[ ] 图片未使用 file path 引用（检测 src="assets/..." 模式）
```

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

本 skill 接收两种输入方式：

### 方式 A：结构化 Markdown / YAML（推荐）

其他 skill 产出的文件应包含以下 Frontmatter：

```markdown
---
type: dashboard|list|detail|card-deck|knowledge|timeline|network|gallery|reader
title: "页面标题"
description: "页面描述/副标题"
source: "来源 skill 名称"
---

## Metrics
...

## List
...
```

### 方式 B：纯结构化 YAML（pop-reader-making 新格式）

pop-reader-making 的 `*_结构化数据.yaml` 可直接作为输入：

```yaml
# 输入 = pop-reader-making 的 YAML 结构化数据
# pop-html-anything 自动识别并渲染
volume_stats:
  total_chapters: 59
  total_characters: 42
  core_characters: 8
  total_events: 87
  emotion_curve: "强势登场 → 紧张对峙 → 激烈冲突 → 阶段性胜利"

chapters:
  ch1:
    title: "初入战警"
    entities: ["陈昂", "暴风女", "镭射眼"]
    events:
      - type: "战斗"
        summary: "陈昂宣告到来，被攻击后化解"
        participants: ["陈昂", "暴风女", "镭射眼"]
    metrics:
      出场角色数: 4
      事件数: 3
      信息密度: 高
    signals: ["武学能力依然生效", "物理常量易撬动"]
    tone: "强势登场"

characters:
  - name: "陈昂"
    role: "主角"
    image_prompt: "Chinese xianxia novel protagonist portrait: a young man with sharp intelligent eyes, wearing flowing white ancient robes with subtle golden embroidery, standing confidently, ethereal glow around him, high quality digital illustration, cinematic lighting"

scenes:
  - title: "帝国大厦宣告"
    chapter: 81
    type: "登场"
    image_prompt: "Chinese xianxia cinematic scene: a lone figure standing atop the Empire State Building at dawn, electromagnetic waves radiating like aurora across the skyline, dramatic lighting, cinematic composition, high detail"

entity_cooccurrence:
  - pair: "陈昂 ↔ 左冷禅"
    chapters: 8
    strength: "大量"
```

> 💡 收到 `.yaml` 文件时，自动按此格式解析。`volume_stats` → 指标卡片 + Stats 区域，`chapters` → 时间线/阅读器骨架，`entity_cooccurrence` → 关系图谱。

### 方式 C：直接数据结构

直接传入带有结构化数据的 JSON/YAML（通过对话上下文）。

---

## 模板目录

`templates/` 目录按内容类型分组，每个模板是某种内容类型的**结构骨架参考**（不是成品复制）。

```
templates/
├── dashboard/         ← 仪表盘（指标 + 图表 + 列表）
├── list-detail/       ← 列表 → 详情（筛选 + 表格 + Tab 详情）
├── card-gallery/      ← 卡片集（卡片网格 + 筛选）
├── knowledge-base/    ← 知识库（索引 + 搜索 + 详情面板）
├── timeline/          ← 时间线（事件序列 + 时间轴）
├── network-graph/     ← 网络图（节点 + 边 + 浮动详情）
├── promo-landing/     ← 营销落地页（Hero + 画廊 + CTA）
└── reader/            ← 长文阅读器（章节 + 正文 + 阅读设置）
```

> 模板是 LLM 理解"这个类型应该长什么样"的参考，不是复制粘贴。
> 实际输出时，根据输入内容**重新生成**，基于 DESIGN_CORE + components 渲染。

---

## 内部结构

```
pop-html-anything/           ← 唯一 HTML 渲染引擎
├── SKILL.md                 ← 本文（v2.2 融合工程化改造方法论）
├── skill.json               ← 元数据 + 权限
├── scripts/
│   └── generate_image.py    ← Seedream 生图脚本
├── _design/                 ← 设计系统（内部规范）
│   ├── DESIGN_CORE.md       ← CSS 变量 / 间距 / 字体
│   ├── components.md        ← 组件库参考（含内容互联）
│   └── responsive.md        ← 响应式规范
├── templates/               ← 场景骨架参考（8种类型）
└── ...
```

## 唯一责任原则

> **pop-html-anything 是整个系统中唯一产出 HTML 的 skill。**
> 其他所有 skill（pop-book-promo、pop-YouTubewebbuilder、pop-reader-making、prd-builder 等）**不再自行产出 HTML**。

### 协作流程

```
其他 skill（如 pop-reader-making）
  └→ 产出结构化 Markdown + 配套 YAML 结构化数据
       └→ 调用 pop-html-anything
            └→ 本 skill 接管：读取 YAML → Phase 0 设计简报 → 选骨架 → 应用设计核心 → 组装组件 → 硬性配图 → 质量门禁
                 └→ 输出最终 HTML
```

### 输入格式

**推荐：** 其他 skill 输出 `.yaml` 纯结构化文件（如 pop-reader-making 的 `*_结构化数据.yaml`），pop-html-anything 自动识别并渲染。

**兼容：** 结构化 Markdown（含 Frontmatter），见上方「输入规范」章节。
