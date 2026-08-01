# Step 2a: 页面提示词设计

> 读导演卡 → 逐页组装页面级提示词 → 形成分镜脚本表 → 🚪门禁确认

## 设计哲学

Step 2a 的唯一任务是"怎么画"——基于导演卡的页面设计表，将每页转化为具体的页面级提示词。**不做执行**——不调 API、不写 HTML、不跑脚本。

**导演卡是唯一输入源。** 不重新做改编分析，直接读导演卡的页面设计表组装提示词。

**页面级提示词是核心。** v4.0 生成单位是"页"——一个提示词描述一整页（含所有格子的分格线、每格内容、镜头语言），Seedream 一次直出完整漫画页。不再逐格生成再拼图。

**提示词必须持久化到 storyboard.md。** 提示词是分镜设计的真相源，供审核、复用、迭代。生成脚本从 storyboard.md 读取提示词，不是硬编码到脚本里。

**角色一致性靠定妆图参考+冻结提示词保证。** 每页的提示词中角色描述部分直接从角色库复制冻结提示词的关键特征。生成时带角色定妆图作为参考图。

## 1. 读取导演卡

读取 Step 1 产出的 `第{N}章/导演卡.md`，获取：

| 导演卡内容 | 用途 |
|:-----------|:-----|
| 章节概要 | 把握整体情绪走向 |
| 角色变化记录 | 规划增量定妆图（Step 2b 执行） |
| 改编策略表 | 拆提示词的输入源 |
| 转化帧设计 | 视觉转化帧的画面提示词基础 |
| 旁白文案 | 旁白浓缩帧的已拟文字 |
| **高光设计** | **名场面页的冲击帧提示词方向、张力构建技法** |
| **页面设计表** | **组装提示词的直接输入**——每页的格数/格布局/每格内容/视觉重心/旁白文字已确定，Step 2a 只需翻译为英文页面级提示词 |

> 如果导演卡不存在（跳过了 Step 1），**必须回退执行 Step 1**，不得直接从原文拆分镜。

> 格数、格布局、每格内容、视觉重心已在 Step 1 页面设计表中确定。Step 2a **继承**这些设计决策，不重新决定页面布局。

## 2. 逐页组装提示词

基于导演卡的**页面设计表**，为每页组装页面级提示词。**参考 `references/storyboard-guide.md`** 了解提示词方法论、构图骨架系统和转化方案库。

### 2.1 页面级提示词模板

**多格页模板**（3-6格）：

```
[Seedream 执行串(画风,含参考作品)]。A vertical manga comic page divided into {N} panels in {格布局英文描述} with thick black gutters between panels.

Panel 1: {格1画面内容+构图骨架串+角色描述+场景描述(精简≤2句)}.
Panel 2: {格2画面内容+构图骨架串+角色描述+场景描述(精简≤2句)}.
...
Panel N: {格N画面内容+构图骨架串+角色描述+场景描述(精简≤2句)}.

[整体情绪氛围]. [风格保真约束]. [负面约束串].
```

**大单页模板**（1格全页独占）：

```
[Seedream 执行串(画风,含参考作品)]。A single full-page manga panel, no gutters, full bleed.

{画面内容+构图骨架串+角色描述+场景描述}. [冲击帧描述：后果和感受，非"发生了什么"].

[情绪氛围]. [风格保真约束]. [负面约束串].
```

**双格页模板**（2格）：

```
[Seedream 执行串(画风,含参考作品)]。A vertical manga comic page divided into 2 panels {格布局英文描述} with thick black gutter between panels.

Top panel: {格1画面内容+构图骨架串+角色描述+场景描述}.
Bottom panel: {格2画面内容+构图骨架串+角色描述+场景描述}.

[情绪氛围]. [风格保真约束]. [负面约束串].
```

### 2.2 提示词组装规则

**关键规则**：

1. **首句必须是 Seedream 执行串**——从漫画角色库的「Seedream 执行串」字段复制，放在提示词最前面（高权重位）
2. **第二句必须是页面分格描述**——`A vertical manga comic page divided into {N} panels in {格布局英文}`，告诉 Seedream 这是一个多格漫画页
3. **每格描述以 `Panel N:` 开头**——明确标识每格内容，Seedream 会按顺序在对应区域绘制
4. **每格包含构图骨架串**——从导演卡页面设计表的「每格内容概述」中提取机位+构图手法，翻译为英文
5. **角色描述从角色库冻结提示词复制**——不重新组装，直接引用视觉锚点串和关键特征
6. **场景描述精简到≤2句/格**——过长的场景描述会把 Seedream 推向"电影概念艺术"模式
7. **末尾必须有风格保真约束**——从漫画角色库的「风格保真约束」字段复制，防止画风漂移
8. **提示词总长度 ≤2500 字符**——超过时精简场景描述

### 2.3 构图骨架串组装

从导演卡页面设计表的「每格内容概述」中提取构图方向（如"全景·仰视·对角线"），翻译为英文构图骨架串：

| 画面方向 | 构图手法 | 构图骨架串（英文） |
|:---------|:---------|:-----------------|
| 全景·仰视 | 仰角压迫 | `WIDE SHOT, extreme low angle, looking up, imposing` |
| 中景·平视 | 三分法 | `MEDIUM SHOT, eye level, rule of thirds composition` |
| 近景·俯视 | 前景遮挡 | `CLOSE-UP, high angle, foreground silhouette occluding view` |
| 特写·平视 | 大留白 | `EXTREME CLOSE-UP, extreme negative space, minimal composition` |
| 全景·仰视 | 对角线 | `WIDE SHOT, low angle, diagonal composition, dynamic angle` |

> **完整构图手法表见 `references/storyboard-guide.md` 构图骨架系统。**

### 2.4 角色描述写法

每格中的角色描述从角色库的冻结提示词中提取关键部分：

```
参考定妆图中的人物形象，[视觉锚点串]。[微表情串(如有情绪)]。[角色动作描述]。
```

**视觉锚点串**从角色库的锚点提示词串字段复制（如 `short messy black hair, black eyes, pale skin, thin build`）。

**微表情**：有强情绪的格，用 storyboard-guide §微表情技法中的映射表替换情绪词。

> **角色一致性靠定妆图参考图保证**——Step 2b 生成时，每页带角色定妆图作为参考图输入。提示词中的角色描述是辅助锁定，定妆图是主要锁定。

### 2.5 负面约束写法（关键页必须）

> 负面约束放在风格保真约束之后，作为 HARD CONSTRAINTS 块。

| 场景类型 | 负面约束串 |
|:---------|:---------|
| 无血场景 | `No blood. No gore. Clean wound without bleeding. No dismemberment.` |
| 无角色场景 | `No characters. No human figures. Empty landscape only.` |
| 多角色防污染 | `Exactly {N} characters. Each character maintains distinct appearance. No feature blending.` |
| 人体精度 | `No duplicated limbs. No detached anatomy. Exactly five fingers per hand. No chibi proportions.` |
| 角色一致性 | `No facial drift. No changing hairstyle. No changing eye color. Character must match reference image.` |

### 2.6 名场面页提示词升级

导演卡高光设计中标注的名场面页，提示词需升级：

1. **使用冲击帧写法**：写"后果和感受"，不写"发生了什么"（参考导演卡冲击帧提示词方向表）
2. **增加张力构建描述**：从导演卡张力构建设计表中提取技法，翻译为英文
3. **画面信息量加大**：名场面页的画面描述可以比普通格多1-2句，确保视觉奇观充分

**示例**（大单页名场面）：

```
[Seedream 执行串]。A single full-page manga panel, no gutters, full bleed.

WIDE SHOT, extreme low angle, looking up, imposing. 参考定妆图中的人物形象，[视觉锚点串]。石门炸裂，尘雾中一道剑光冲天而起，方圆十里的飞鸟惊散，山石龟裂。碎石悬浮在半空，剑意如实质般扭曲空气。角色负手立于裂痕之上，衣袍猎猎，冷峻面容。

史诗仙侠氛围，极致张力。[风格保真约束]. No duplicated limbs. Exactly five fingers. No chibi proportions. No facial drift. Character must match reference image.
```

### 2.7 转化帧提示词

导演卡改编策略表中标注为"视觉转化"的信息，提示词需特殊处理：

- **抽象视觉隐喻帧**：描述隐喻空间+象征性动作，不写对白
- **闪回/记忆帧**：在格描述中追加 `cold blue tint, dashed border frame` 等视觉区分手段
- **系统/UI 帧**：描述半透明 UI 叠层浮现的瞬间，不画完整数值

> **详见 `references/storyboard-guide.md` 转化方案库。**

## 3. 提示词持久化

将每页的提示词写入 `第{N}章/storyboard.md`，作为真相源。

### 分镜脚本表格式

```markdown
# 第{N}章 分镜脚本

## 页面提示词

### P1 — {页面类型}（{格数}格 · {格布局}）

**提示词**：
```
{完整页面级提示词}
```

**参考图**：char-{角色名}-v{N}.png
**旁白文字**：{旁白1} / {旁白2} / ...
**视觉重心**：{视觉重心}

---

### P2 — {页面类型}（{格数}格 · {格布局}）
...
```

> storyboard.md 是生成脚本的配置源——Step 2b 从 storyboard.md 读取每页的提示词、参考图、旁白文字，写入 `generate_comic_page.py` 的 PAGES 列表。

## 4. 🚪 门禁：页面提示词确认

向用户呈现 storyboard.md（`第{N}章/storyboard.md`），核心确认三件事：

1. **每页提示词是否准确描述了导演卡的页面设计** — 格布局对不对，每格内容对不对，视觉重心对不对
2. **名场面页是否有冲击力** — 冲击帧写法是否写的是"后果和感受"，张力构建技法是否到位
3. **角色描述是否正确** — 视觉锚点串是否从角色库复制，定妆图参考图版本是否正确

用户确认后，携带 storyboard.md 进入 Step 2b（读取 `steps/step2b-production.md`）执行页面生成+文字叠加。

> **提示词是页面生成的唯一输入源**——Step 2b 从 storyboard.md 读取提示词写入生成脚本，不重新组装提示词。
