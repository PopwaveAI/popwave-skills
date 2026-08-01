# 分镜脚本指南

> Step 1 章节解构的参考指南。如何从一章网文中拆出该画的关键帧。

> **v4.0 适配说明**：v4.0 的核心变化是**生成单位从"格"升级为"页"**。Seedream 在单张图内直出完整漫画页（含分格线、多格内容、镜头语言），HTML 仅叠加文字层（旁白条 narration / 对白气泡 dialogue）。本指南中所有"格"级方法论已适配为"页"级：选帧原则从"选哪些格"变为"选哪些页、每页几格"；提示词写法从"一格一提示词"变为"一页一提示词（含全页所有格子）"；布局系统从"HTML 7 种布局类排列格子"变为"HTML 全宽展示页面图 + 文字叠加"。方法论核心（改编策略、构图骨架、角色一致性工艺、风格三字段、负面提示词策略）不变，只是使用场景从"每格"变成"每页的每格描述"。

## 核心原则

**漫画不是小说的翻译，是小说的再创作。** 一章 3000 字不可能全画出来，必须选择——选错了帧，画得再好也讲不清故事。

**页数由剧情决定，每页格数由内容决定。** 一章有多少值得"看到"的瞬间，就拆多少页；每页有几条信息线，就分几格。Agent 拥有完整的页数和格数判断权。

> v4.0 生成单位变化：v3.x 每格一张图，HTML 用 7 种布局类排列组合；v4.0 每页一张图（含多格），HTML 全宽展示 + 文字叠加。页面类型（大单页 / 多格页 / 双格页）由导演卡决定，Seedream 直出。

## 页面级选帧原则

### 1. 情绪转折点优先

每次角色情绪发生变化的地方，都是一个分镜候选。一章通常有 3-5 个情绪转折点。

```
示例（深渊主宰 ch001）：
绝望（米不够了）→ 温暖（抱狗）→ 恐惧（门外脚步声）→ 决绝（卖身）→ 崩溃（哭泣）→ 希望（哥哥苏醒）
= 6 个情绪转折 = 可分配到 2-3 页中
```

### 2. 动作高潮优先

打斗、追逐、冲突的瞬间比静态对话更适合漫画。

### 3. 信息揭示优先

新角色登场、关键道具出现、真相揭露——这些是读者最想"看到"的瞬间。

### 4. 避免纯对话页

两个人站着说话是最差的漫画画面。如果必须画对话，让角色在**做某事的同时**说话（边走边说、边做饭边说）。

### 5. 机位交替

```
推荐节奏：全景 → 中景 → 近景 → 特写 → 中景 → 全景 → 近景 → 特写
```

连续相同机位会让读者疲劳。特写用于情绪高潮，全景用于场景建立。在 v4.0 中，机位交替在**同一页的多格之间**和**跨页之间**都要体现。

### 6. 页数与格数判断

页数不锁死，Agent 根据章节内容密度自主判断。每页格数由该页内容的信息线决定：

| 章节类型 | 页数范围 | 每页格数 | 判断依据 |
|:---------|:---------|:---------|:---------|
| 过渡章（日常/铺垫） | 2-3 页 | 1-3 格 | 情绪平稳，关键场面少，可用大单页 |
| 标准章（起承转合） | 3-4 页 | 2-4 格 | 3-5 个情绪转折，节奏正常 |
| 内容密集章（多线/战斗） | 4-5 页 | 4-6 格 | 多场动作高潮，信息密集 |
| 高潮章（大事件爆发） | 5-6 页 | 3-6 格 | 事件密度极高，名场面用大单页 |

**核心判断标准**：每个值得"看到"的瞬间都该有独立分镜。宁可多画不可漏画——漏掉关键场面比多画几页更影响阅读体验。

**格数与页面类型关系**：
- 1 格 = 大单页（名场面 / 冲击帧 / 章末钩子页，全页独占）
- 2 格 = 双格页（对比 / 反应 / 并进）
- 3-6 格 = 多格页（标准叙事页）

### 7. 高光独占页

**原文中的高光时刻必须独占至少一页或一格大格，禁止和多件事挤在同格。** 这是选帧的铁律。

高光时刻的判断标准：
- **反应型高光**：角色情绪骤变（震惊 / 暴怒 / 崩溃）→ 独占一格大格 reaction shot，或独占一页
- **转折型高光**：剧情方向逆转（背叛揭露 / 身份揭示）→ 独占一格大格，用特写或大单页
- **震撼型高光**：空间或认知骤变（觉醒 / 进入新世界）→ 用**大单页**（1 页 1 格全页独占），或用**两格跨页**：先压迫铺垫格（窄、暗、局促）再破格展开格（开阔、逆光、大画面），一抑一扬才出震撼

**反例**：把"角色 A 说话 + 角色 B 震惊反应 + 环境变化"塞进一格 → 三个信息互相稀释，哪个都没冲击力
**正例**：A 说话一格（中景），B 震惊反应一格（特写），环境变化一格（全景）→ 三格递进，每格一个焦点；或拆为两页，首页对话铺垫，次页独占反应

> 独占不等于大单页。反应型高光可以用多格页中的一格大格 + 特写，关键是**信息独占**——这一格只讲一件事。名场面级别的震撼型高光才值得用大单页（1 页 1 格全页独占）。

### 8. 名场面设计

> 高光独占页解决"信息不稀释"，名场面设计解决"画面有没有冲击力"。一个独占页如果内容本身不震撼，独占了也是浪费。

#### 名场面识别三标准

一页是否值得成为"名场面"（读者会截图分享的页），用三条标准检验：

| 标准 | 检验问题 | 满足条件 |
|:-----|:---------|:---------|
| 视觉奇观 | 这个画面画出来好不好看？有没有"哇"的瞬间？ | 画面有壮丽 / 震撼 / 诡异 / 美丽的视觉元素 |
| 情绪爆发 | 这个画面能不能让读者感到什么？ | 画面承载了强烈的情绪（震撼 / 悲壮 / 热血 / 恐惧） |
| 剧情转折 | 这个画面是否改变了故事走向？ | 画面呈现的是一个转折点 / 决策点 / 揭示点 |

**三条满足两条 = 名场面。** 名场面必须用**大单页**（1 页 1 格全页独占）呈现，配合视觉花样 + 高精度提示词。

> 每章至少 1 个名场面。如果一章找不出一个名场面，说明选帧有问题——不是每一章都有"画面感"强的内容，但每一章至少有一个"读者会记住"的瞬间。

#### 张力构建五技法

名场面不是"把事情画出来"，是"让读者感受到冲击"。五种技法：

| 技法 | 原理 | 提示词写法 | 示例 |
|:-----|:-----|:-----------|:-----|
| **尺度对比** | 角色渺小 vs 环境宏大 | 画面中放入参照物强调尺度差距 | 剑仙立于百丈剑峰前，人如蝼蚁，剑意却裂开半座山 |
| **静默铺垫** | 爆发前留一格安静的 | 前一页用静态 / 沉默画面，与爆发页形成反差 | 对话页 → 沉默特写页 → 爆发大单页（跨页递进，一静一动） |
| **反应镜头** | 不画事件本身，画旁观者的反应 | 画角色被光照亮 / 被冲击波掀飞 / 表情定格 | 不画出爆炸，画所有人被金光映亮的脸 |
| **视觉隐喻** | 用象征物承载情绪 | 将抽象概念具象为可视物体 | 金卷缓缓展开 = 战争倒计时启动；断剑插在废墟中 = 战败 |
| **留白截断** | 关键时刻画面截断 | 画面只展示前半，后半留给下一页或读者想象 | 手触碰门把手 → 下一页已是门内景象 |

> 五技法可组合使用。最经典的冲击页 = 静默铺垫 + 尺度对比 + 反应镜头（先安静 → 突然展示宏大 → 画角色的反应）。

#### 冲击页提示词升级

普通页的提示词写"发生了什么"，冲击页（大单页）的提示词写"**后果和感受**"：

| 错误写法 | 正确写法 |
|:---------|:---------|
| 剑意冲霄 | 百丈山峰被无形剑气切出一道裂痕，碎石纷飞如暴雨，剑仙负手立于裂痕之上 |
| 金瞳亮起 | 金色重瞳中倒映出整个蜀地版图，瞳孔中城池燃烧、山河崩塌 |
| 他很愤怒 | 桌案在掌下碎裂，木屑飞溅，地面出现蛛网裂纹，周围侍卫惊恐后退 |
| 他出关了 | 石门炸裂，尘雾中一道剑光冲天而起，方圆十里的飞鸟惊散，山石龟裂 |

**冲击页公式**：

```
[大单页模板: A single full-page manga panel] + [Seedream 执行串] + [具体视觉奇观描述] + [环境/他人反应] + [风格保真约束 + 高精度模板 HARD CONSTRAINTS]
```

> 冲击页必须使用高精度模板（4 块结构），因为普通提示词的约束力不够，容易画成泛化的"能量光效"而非具体的视觉奇观。

#### 名场面 vs talking head

**最大的反模式是 talking head（说话的头）**——角色站着 / 坐着说话，画面没有任何视觉信息，全靠对白气泡撑着。

| talking head（避免） | 名场面（追求） |
|:--------------------|:-------------|
| 角色 A 对角色 B 说"我要攻蜀"，两人站着对话 | 角色 A 的金瞳中倒映出燃烧的城池，手按在案上，案面出现裂纹 |
| 角色 C 说"我很强"，展示能力 | 山峰被无形力量切开，角色 C 站在裂痕中央，碎石悬浮 |
| 角色 D 说"出发"，转身离开 | 角色 D 的背影消失在山门中，身后剑光冲天，飞鸟惊散 |

> **核心原则**：如果一页的画面去掉对白气泡后什么都没有，它就是 talking head。名场面的画面应该**不需要对白也能传达信息**。

## 改编策略：从文字到画面

> 选帧解决"画什么"——但原文中大量内容无法直接选帧。内心独白、系统数值、世界观设定是网文的常态，它们对理解剧情至关重要，却不自带可画的画面。改编策略解决"怎么把画不了的东西变成能画的"。

### 改编决策树

面对一段内容，按以下顺序决策：

```
这段内容对理解剧情/角色是否关键？
├─ 否 → 砍掉
└─ 是 → 能否直接画面化？
    ├─ 能（有动作/情感/对话场面）→ 直接选帧
    └─ 不能（独白/系统/设定/闪回）→ 需要转化
        ├─ 转化方案A：抽象视觉隐喻
        ├─ 转化方案B：角色反应替代
        ├─ 转化方案C：旁白浓缩+象征画面
        └─ 转化方案D：原创视觉插入
```

### 四种转化方案

#### 方案A：抽象视觉隐喻

把无形的内心活动变成一个**可视的象征性场景**。角色从现实空间进入一个隐喻空间，用动作和意象表达心理状态。

适用：内心独白、意识挣扎、人格融合

| 原文内容 | 转化画面 | 提示词要点 |
|:---------|:---------|:-----------|
| "我要醒过来！必须醒过来！" | 角色坠入黑暗深渊，双手攀住光明的裂缝边缘向上挣扎 | 意识空间，黑暗深渊，裂缝透光，角色攀附挣扎 |
| 两个灵魂记忆在融合 | 意识空间中两个半透明身影重叠，一个逐渐消散如碎片 | 两个半透明身影重叠，一个化为光点碎片消散 |
| 恐惧压迫感 | 角色被巨大的黑影笼罩，黑影如手般收紧 | 巨大黑影笼罩角色，压迫感，光影对比强烈 |

> **关键**：隐喻帧的提示词不写对白，用画面动作和空间意象传达情绪。隐喻帧的机位和环境应与现实帧有明显区分（如纯黑背景、抽象空间）。

#### 方案B：角色反应替代

不画内心独白本身，画**角色因独白而产生的可见反应**——表情变化、握拳、咬牙、流泪、动作停顿。

适用：有外部场景的内心独白（角色在做事的同时内心活动）

| 原文内容 | 转化画面 | 提示词要点 |
|:---------|:---------|:-----------|
| "为了哥哥她愿意做任何事" | 薇薇安亲吻昏迷的索伦额头时，眼神从恐惧变为坚定 | 角色表情特写，眼神从恐惧到坚定的转变瞬间 |
| 索伦感知到外面有人要闯入 | 索伦虽然闭眼躺在床上面无表情，但手指微微攥紧被角 | 闭眼角色的手部特写，手指攥紧被角的细节 |

> **关键**：找一个"外部可观察但原文未着重描写"的动作细节来承载内心。

#### 方案C：旁白浓缩+象征画面

用 1-2 句旁白条概括大段文字，搭配一个**不直接叙事但氛围契合**的画面。旁白承担信息，画面承担情绪。

适用：世界观设定、背景历史、大段解释性文字

| 原文内容 | 旁白文字 | 搭配画面 |
|:---------|:---------|:---------|
| 诸神之战历史+圣者时代+玩家机制 | "这个世界将来会迎来诸神的黄昏。" | 末日异象：天空撕裂，恶魔降临，城市燃烧 |
| 脑域开发科普+虚拟游戏背景 | "他的意识曾在虚拟世界中穿行。" | 角色闭眼，头顶浮现半透明的数据流光晕 |
| 贫民区背景介绍 | "这里是琥珀城被遗忘的角落。" | 贫民区全景：破败建筑、泥泞街道、麻木的人群 |

> **关键**：旁白字数控制在 15 字以内，画面要有足够的视觉冲击力独立成立。v4.0 中旁白通过 HTML 的 narration 旁白条叠加。

#### 方案D：原创视觉插入

原文完全没写到这个画面，但这个画面能**比文字更高效地传达同等信息**。相当于导演在剧本基础上加的视觉语言。

适用：需要快速建立认知、但原文用文字堆叠说明的内容

| 原文内容 | 原创画面 | 传达的信息 |
|:---------|:---------|:-----------|
| 索伦有盗贼技能+游戏系统 | 索伦睁眼时，眼前浮现半透明 UI 界面（模糊的属性数字、技能图标轮廓） | 他身上有游戏系统，不需要画完整面板 |
| 贫民区充满罪恶 | 一个角落里人贩子在与流氓交易，远处有孩子在捡垃圾 | 一帧建立"罪恶之地"认知 |
| 希斯是老猎犬后裔 | 希斯虽然老态龙钟，但瞬间露出的牙齿和眼神暗示其凶猛血统 | 用一个"凶猛一瞬"的表情暗示猎犬血统 |

> **关键**：原创画面必须忠于原文信息，不能添加原文没有的剧情。它只是换了一种方式呈现同样的信息。

### 闪回与记忆的视觉区分

原文中的记忆/闪回/预知等内容，在漫画中需要与当前时间线**视觉区分**，否则读者会混淆叙事层级。

| 区分手段 | 效果 | 提示词写法 |
|:---------|:-----|:-----------|
| 边框纹理 | 画面边缘有破碎/波纹/裂纹效果 | 画面边缘呈现破碎裂纹效果，如同记忆碎片 |
| 色调偏移 | 整体色调偏冷蓝/暖黄/去饱和 | 画面色调偏冷蓝去饱和，呈现回忆质感 |
| 画中画 | 在当前画面中浮现半透明的小画面 | 角色眼中反射出半透明的异象画面 |
| 抽象背景 | 背景不是真实场景而是意识空间 | 角色漂浮在纯黑/星空/数据流的抽象空间中 |

> 闪回页的提示词中应明确标注这是非当前时间线画面，使用上述一种或多种手段。

### 改编自检清单

选帧+转化设计完成后，逐条核对：

- [ ] 原文中每条**关键信息**都有对应的页或旁白承载？
- [ ] S 级信息是否分到了最佳页位（名场面/冲击页）？
- [ ] 本章至少有 1 个名场面（三标准满足两条）？
- [ ] 名场面不是 talking head（去掉对白气泡后画面仍有信息）？
- [ ] 冲击页的提示词写的是"后果和感受"而非"发生了什么"？
- [ ] 视觉转化页的提示词是否具体到可执行（有明确画面、动作、环境）？
- [ ] 旁白浓缩页的旁白文字是否已拟好且 ≤15 字？
- [ ] 闪回/记忆页是否有视觉区分手段？
- [ ] 从读者视角通读分镜序列：不看原文能理解本章发生了什么吗？

> 如果读者不看原文会丢失关键理解 → 回到步骤 3，补加转化页或旁白。

## 分镜提示词写法

### 基本公式

> **v4.0 重构**：生成单位从"格"升级为"页"。一个提示词描述一整页（含全页所有格子），Seedream 在单张图内直出完整漫画页（含分格线、多格内容、镜头语言）。基本公式不变（Seedream 执行串 + 构图骨架串 + 角色描述 + 场景 + 风格保真约束），但组装方式变为"一个提示词描述一整页"。

### 页面级提示词模板

#### 多格页模板（3-6 格）

```
[Seedream 执行串(画风,含参考作品)]。A vertical manga comic page divided into {N} panels in {格布局英文描述} with thick black gutters between panels.

Panel 1: {格1画面内容+构图骨架串+角色描述+场景描述(精简≤2句)}.
Panel 2: {格2画面内容+构图骨架串+角色描述+场景描述(精简≤2句)}.
...
Panel N: {格N画面内容+构图骨架串+角色描述+场景描述(精简≤2句)}.

[整体情绪氛围]. [风格保真约束]. [负面约束串].
```

#### 大单页模板（1 格全页独占）

```
[Seedream 执行串(画风,含参考作品)]。A single full-page manga panel, no gutters, full bleed.

{画面内容+构图骨架串+角色描述+场景描述}. [冲击帧描述：后果和感受，非"发生了什么"].

[情绪氛围]. [风格保真约束]. [负面约束串].
```

#### 双格页模板（2 格）

```
[Seedream 执行串(画风,含参考作品)]。A manga comic page divided into 2 panels in {vertical/horizontal split} with thick black gutters between panels.

Panel 1: {格1画面内容+构图骨架串+角色描述+场景描述(精简≤2句)}.
Panel 2: {格2画面内容+构图骨架串+角色描述+场景描述(精简≤2句)}.

[整体情绪氛围]. [风格保真约束]. [负面约束串].
```

### 示例

旧写法（v3.x 格级——失败，无法表现跨格关系）：
```
参考图中的人物形象。瘦弱女孩侧面蹲在破旧灶台前，用木棍搅动陶碗里的稀粥，
灶膛火光映亮她的脸。破烂的屋顶漏雨，屋内弥漫浓烟和蒸汽。阴暗破败的贫民区小屋，
墙角堆着湿柴。暗黑奇幻半写实日式漫画风格，水彩质感笔触，灰暗色调，暖色火光点缀，压抑氛围。
```

新写法（v4.0 页级——修复，一个提示词描述整页）：
```
Semi-thick painting manga style, clean hard outer contour lines as skeleton with soft gradient shading inside color blocks, cel-shaded base with painterly soft-light overlays, 7.5-head semi-realistic proportions, modern refined illustration. Art style similar to Da Feng Da Geng Ren manga adaptation. A vertical manga comic page divided into 3 panels in vertical stack with thick black gutters between panels.

Panel 1: WIDE SHOT, eye level. Rule of thirds composition. 参考图中的人物形象，short messy black hair, black eyes, pale skin, thin build, worn dark jacket。瘦弱女孩侧面蹲在破旧灶台前，用木棍搅动陶碗里的稀粥，灶膛火光映亮她的脸。破败小屋。

Panel 2: CLOSE-UP, eye level. Extreme negative space. 参考图中的人物形象，short messy black hair, black eyes, pale skin, thin build。女孩低头看碗中稀粥，眉头紧锁。木碗特写。

Panel 3: MEDIUM SHOT, low angle. Framing through doorway. 破败小屋门外，黑暗中可见模糊人影逼近。

压抑氛围。Maintain visible outer contour lines. Use soft gradient shading inside color blocks, not full painterly blending. Keep manga readability. No lineless style. No cinematic concept art. No photorealistic 3D rendering.
```

### 注意事项

- **首句必须是 Seedream 执行串**（从漫画角色库的风格锚定串字段复制），不能以"参考图中的人物形象"开头
- **页面结构声明**：必须声明页面是"divided into {N} panels"还是"single full-page panel"
- **每格描述独立**：Panel 1/2/.../N 逐格描述，每格包含画面内容 + 构图骨架串 + 角色描述 + 场景描述（精简 ≤2 句）
- **场景描述精简到 ≤2 句**——过长的场景描述会把 Seedream 推向"电影概念艺术"模式，淹没画风
- **末尾必须有风格保真约束**（从漫画角色库的风格保真约束字段复制），防止画风漂移
- 不写对白（对白用 HTML 文字叠加，dialogue 对白气泡 / narration 旁白条）
- 不写任何文字内容（Seedream 文字渲染不可控）
- ≤500 字（英文部分不计入字数限制）

### 关键页升级：高精度模板

**高潮页、变身页、名场面页**可升级为高精度模板写法（见 `../pop-novel-visual/references/seedream-prompt-guide.md` §1.10）。在基础提示词上增加：

1. **镜头规格**：焦段（24mm/35mm）+ 机位（仰角/俯角/平视）
2. **渲染要求**：材质质感列表（fabric texture / leather / hair strands / particles）
3. **硬约束**：No duplicated limbs. Exactly five fingers. No chibi proportions.

> 普通页不需要升级，速度优先。只有"值得读者停留 3 秒"的页才值得用高精度模板。

## 文字叠加分类

> v4.0 适配：HTML 不再做格子布局，只做文字叠加。文字分两类——narration（旁白条）和 dialogue（对白气泡）。文字叠加规范详见 `references/page-layout-guide.md`。

| 类型 | HTML 叠加处理 | 示例 |
|:-----|:-------------|:-----|
| 角色台词 | dialogue 对白气泡 | "你会保护我的，对不对？" |
| 内心独白 | dialogue 对白气泡（思泡样式） | 米不多了。 |
| 环境拟声词 | 提示词中写明拟声词效果 | 啪！BOING—— |
| 人群喊叫 | 提示词中写明人群喊叫效果 | 打死小偷！ |
| 旁白叙述 | narration 旁白条 | 脚步声。不止一个人。 |

> 文字叠加规范（旁白条位置、对白气泡样式、避让规则）详见 `references/page-layout-guide.md`。

## 风格三字段速查

> v2.9.2 升级：画风从单字段（锚定串）升级为三字段（锚定串 + Seedream 执行串 + 风格保真约束）。完整画风池见 `art-style-pool.md`。

### 提示词中各字段的位置

```
[Seedream 执行串]  ← 提示词开头（高权重）
    ↓
参考图中的人物形象 + 角色动作 + 场景描述
    ↓
[风格保真约束]  ← 提示词末尾（防漂移）
```

### 速查表（仅列 Seedream 执行串和风格保真约束）

| 画风 | Seedream 执行串 | 风格保真约束 |
|:-----|:----------------|:------------|
| 日系赛璐璐平涂 | `Clean cel-shading manga style, bold visible outline strokes, flat color fills with no soft blending, two-tone cel shading with sharp highlight edges, anime 7-head proportions with large eyes, vibrant saturated palette. Art style similar to Douluo Dalu manga adaptation` | `Maintain visible bold outline strokes. Use flat color fills only, no soft gradient blending. Keep two-tone cel shading. No photorealistic rendering. No cinematic concept art. No 3D rendering appearance.` |
| 伪厚涂/半厚涂 | `Semi-thick painting manga style, clean hard outer contour lines as skeleton with soft gradient shading inside color blocks, cel-shaded base with painterly soft-light overlays, 7.5-head semi-realistic proportions, modern refined illustration. Art style similar to Da Feng Da Geng Ren manga adaptation` | `Maintain visible outer contour lines. Use soft gradient shading inside color blocks, not full painterly blending. Keep manga readability. No lineless style. No cinematic concept art. No photorealistic 3D rendering.` |
| 韩漫半写实厚涂 | `Korean webtoon semi-realistic painterly style, no visible lineart with full painterly color shaping, dramatic rim lighting, cool blue-purple color palette, realistic 7.5-8 head proportions with sharp facial features, cinematic lighting with detailed backgrounds. Art style similar to Solo Leveling webtoon` | `Use full painterly coloring without visible lineart. Maintain dramatic rim lighting. Keep cool blue-purple palette. No flat cel-shading. No anime-style bold outlines. No cute chibi proportions.` |
| 国漫玄幻修仙厚涂 | `Chinese xianxia painterly manga style, brush-like variable-width lineart, ornate costumes with metal and jade material textures, high-saturation glowing magic effects with particle layers, dense Eastern ornamental patterns, epic xianxia atmosphere. Art style similar to Battle Through the Heavens manga` | `Maintain brush-like variable-width lineart. Include Eastern ornamental patterns. Use high-saturation magic effects. No Western fantasy style. No flat cel-shading. No modern clothing elements.` |
| 硬朗武侠历史 | `Gritty wuxia historical manga style, rough carved lineart with bold powerful strokes, low-saturation earthy yellow-ochre-blood red palette, high-contrast hard lighting, realistic 8-head proportions with solid muscle-bone structure, rough heavy texture. Art style similar to Biao Ren manga` | `Maintain rough carved bold lineart. Use low-saturation earthy palette. Keep high-contrast hard lighting. No soft pretty anime style. No bright saturated colors. No modern elements.` |
| 少女水彩言情 | `Shoujo watercolor manga style, delicate soft lineart, watercolor wash coloring with bleeding edges, soft pastel macaron palette of pink-blue-lavender, light spots and petal decorations, dreamy soft-glow atmosphere, 7-head proportions with large teary eyes. Art style similar to Feng Qi Cang Lan manga` | `Maintain delicate soft lineart. Use watercolor wash coloring. Keep pastel macaron palette. No dark heavy themes. No thick oil painting texture. No realistic proportions.` |
| 暗黑悬疑高对比 | `Dark suspense manga style, bold black solid outline lines, large area shadow blackening, low-saturation desaturated tones with blood-red and sickly-green accent colors, extreme high-contrast lighting, rough noise texture with blood stains and fog. Art style similar to Zhongguo Jingqi Xiansheng manga` | `Maintain bold black solid lines. Use extreme high-contrast lighting. Keep desaturated palette with accent colors only. No bright cheerful tones. No soft gradient shading. No pretty anime style.` |
| 都市赛博 | `Urban cyberpunk manga style, modern hard lineart, neon cyan-magenta-electric blue color palette, screen glow and lens flare effects, 7.5-head semi-realistic proportions, UI overlay and data stream particles. Art style similar to Quanzhi Fashi manga adaptation` | `Maintain modern hard lineart. Use neon cyan-blue palette. Include cyberpunk UI elements. No historical or ancient elements. No soft watercolor style. No pastel colors.` |

> Phase 0 选定画风后，三个字段都冻结到 `漫画角色库.md` 和 `漫画快照.md`。分镜提示词中的 Seedream 执行串和风格保真约束以冻结版本为准（可能含赛道微调修饰）。

## 角色一致性工艺包

> 冻结提示词解决的是"跨章不换脸"的基础问题。本节解决的是"同一章内角色够不够像、情绪够不够真"的工艺问题。

### 视觉锚点：给角色一个不可变的"识别标签"

规格表中的"标志性特征"字段容易被写成泛化描述（"苍白的脸""瘦弱的身材"），这种描述对 AI 的约束力不够。**视觉锚点是具体到位置、形状、颜色的不可变特征**，在每一帧的提示词中强制继承。

#### 锚点设计原则

1. **位置精确**：不写"有疤"，写"左眉骨上方一道3cm斜疤"
2. **形状具体**：不写"有印记"，写"眉间红莲印记，花瓣形状"
3. **颜色锁定**：不写"异色瞳"，写"左眼金色右眼蓝色"
4. **数量不少于3个**：面部锚点≥1 + 身体锚点≥1 + 服饰锚点≥1

#### 锚点提取表（Phase 0 定妆时填写，冻结到角色库）

| 角色 | 面部锚点 | 身体锚点 | 服饰锚点 | 锚点提示词串 |
|:-----|:---------|:---------|:---------|:------------|
| 索伦 | 亚麻色短发微乱，黑瞳，苍白面色，锁骨突出 | 瘦削病后初愈体型 | 破旧亚麻衬衫，赤脚 | `short messy sandy hair, black eyes, pale skin, prominent collarbone, thin build, worn linen shirt, barefoot` |
| 薇薇安 | 黑色长发编辫，大眼睛，圆脸 | 瘦弱小女孩体型 | 破旧麻布裙 | `black braided long hair, large eyes, round face, thin small build, worn burlap dress` |

> **使用方式**：每帧提示词中，`参考图中的人物形象` 后面紧跟锚点提示词串，确保 AI 在每帧中都能提取到相同的识别标签。在 v4.0 页级提示词中，每格的角色描述都应包含锚点串。

### 微表情技法：用生理反应代替心理描述

AI 不理解"他很痛苦"，但理解"下巴肌肉紧绷，下唇咬破，鼻翼微张"。**微表情是让角色"会演戏"的核心技法。**

#### 情绪→微表情映射表

| 情绪 | 错误写法 | 微表情写法（提示词用） |
|:-----|:---------|:---------------------|
| 隐忍痛苦 | 他在忍受疼痛 | `jaw muscles clenched tight, lower lip bitten raw, nostrils flaring slightly, veins visible on neck` |
| 压抑愤怒 | 他很生气但忍住了 | `eyes narrowed to slits, knuckles white from gripping, jaw set hard, barely controlled breathing` |
| 恐惧 | 她害怕极了 | `pupils dilated, lips trembling, cold sweat on forehead, fingers unconsciously gripping hem of dress` |
| 决绝 | 她下定了决心 | `eyes sharpened, chin lifted slightly, brow furrowed with resolve, hands stopped trembling` |
| 悲伤 | 他很伤心 | `eyes red-rimmed, tear tracks on cheeks, corners of mouth pulled down, shoulders hunched inward` |
| 狂喜 | 他非常开心 | `eyes crinkled at corners, mouth open in wide grin, cheeks flushed, body leaning forward` |
| 震惊 | 他惊呆了 | `eyes wide, mouth slightly open, body frozen mid-motion, one hand raised and stopped` |
| 阴险 | 他露出阴险的笑容 | `lips curled at one corner only, eyes half-lidded, chin tilted down, shadows pooling under eyes` |

> **使用方式**：在分镜提示词的角色动作描述部分，把情绪词替换为对应的微表情串。不要写"愤怒的表情"，写上表中的具体生理反应。

### 表情变体库（Phase 0 可选增强）

定妆图只有一张正面中性表情。当章节中有强情绪帧时，可基于定妆图生成**表情变体**作为图生图参考，比纯文字描述更可靠。

#### 标准表情变体集

| 变体名 | 生成提示词 | 使用场景 |
|:-------|:---------|:---------|
| angry | `参考图中的人物形象，保持面部特征不变，表情变为愤怒：眉头紧锁，嘴唇抿紧，眼神凌厉` | 争吵、战斗、被激怒 |
| sad | `参考图中的人物形象，保持面部特征不变，表情变为悲伤：眼眶泛红，嘴角下垂，泪痕` | 失去、被欺负、绝望 |
| surprised | `参考图中的人物形象，保持面部特征不变，表情变为震惊：眼睛圆睁，嘴巴微张` | 真相揭露、意外事件 |
| determined | `参考图中的人物形象，保持面部特征不变，表情变为坚毅：眼神锐利，下巴微抬，嘴唇紧抿` | 做决定、战斗前、觉醒 |
| fearful | `参考图中的人物形象，保持面部特征不变，表情变为恐惧：瞳孔放大，嘴唇颤抖，冷汗` | 被威胁、面对强敌 |

#### 使用策略

- **主角**：建议在 Phase 0 生成 3 个核心变体（determined + angry + sad），覆盖大部分强情绪帧
- **配角**：不需要变体，用微表情描述即可
- **调用方式**：图生图，参考图=定妆图，strength=0.55-0.65（太低不变，太高换脸）
- **存储**：`assets/characters/char-{名}-{表情}-v1.png`，冻结提示词到角色库

> 表情变体不是必须的。微表情技法能解决 80% 的问题，变体库用于解决剩下 20% 的"图生图参考图不够准"的情况。

### 负面提示词策略

HARD CONSTRAINTS 块（高精度模板）是负面约束的载体。关键策略：

1. **位置优先**：负面约束放在提示词末尾，但高精度模板中作为独立块（HARD CONSTRAINTS），权重最高
2. **禁止项要具体**：不写"no bad anatomy"，写 `No duplicated limbs. No detached or fused anatomy. Exactly five fingers on each visible hand.`
3. **角色一致性专属禁止项**：

```
No facial drift. No changing hairstyle. No changing eye color. No changing skin tone. No costume variation. Character must match reference image exactly.
```

4. **多角色帧的防污染策略**：当一帧中有多个角色时，在 HARD CONSTRAINTS 中明确：

```
Exactly {N} characters. Each character maintains distinct appearance from reference images. No feature blending between characters.
```

## 场景主镜机制

> 同一场景的跨页之间，空间结构、光源方向、材质质感必须一致。场景主镜是跨页场景一致性的核心手段。

### 核心规则

同一场景的**首页**生成并确认后，成为该场景的"主镜"（scene master）。该场景后续每页生成时，**必须将场景主镜图作为参考图之一输入**（与角色定妆图并列），锁定空间布局、光源方向、环境材质。

```
场景首页 → 确认 → 成为场景主镜
场景第2页 → 参考图 = [角色定妆图] + [场景主镜图]
场景第3页 → 参考图 = [角色定妆图] + [场景主镜图]
场景切换 → 旧主镜废弃，新场景首页成为新主镜
```

### 分镜表标注

分镜脚本表中新增**场景组**列，标识每页所属的场景：

| 页号 | 场景组 | 场景 | 页面内容 | ... | 定妆图版本 | 场景主镜 |
|:-----|:-------|:-----|:---------|:----|:-----------|:---------|
| 1 | A | 破屋雨夜 | 薇薇安抓米 | ... | char-vivian-v1 | —（首页，自己成为主镜） |
| 2 | A | 破屋灶台 | 薇薇安抱狗 | ... | char-vivian-v1 | page1.png |
| 3 | A | 破屋门外 | 脚步声逼近 | ... | — | page1.png |
| 4 | B | 集市 | 薇薇安穿新衣 | ... | char-vivian-v2 | —（新场景，自己成为主镜） |
| 5 | B | 集市 | 被人群推搡 | ... | char-vivian-v2 | page4.png |

> 场景组相同的页共享同一个场景主镜。场景组切换 = 旧主镜废弃，新场景首页成为新主镜。

### 提示词写法

场景主镜图作为图生图参考时，提示词中追加环境锁定描述：

```
[Seedream 执行串]。A vertical manga comic page divided into {N} panels...
Panel 1: ... 场景环境与参考图一致：[从场景主镜提取的空间特征，如"破败小屋，左侧灶台，右墙漏雨"]。光源方向与参考图一致：[如"灶膛火光从左下方照射"]。
...
```

> 场景主镜锁的是**空间+光源+材质**，不是角色。角色一致性仍由角色定妆图负责。

### generate_comic_page.py 配置

`PAGE_REFS` 升级为支持多参考图（角色定妆图 + 场景主镜）：

```python
# 按页映射参考图：[角色定妆图, 场景主镜图]
PAGE_REFS = {
    "page1": ["char-vivian-v1.png", None],           # 场景A首页，无主镜
    "page2": ["char-vivian-v1.png", "page1.png"],     # 场景A第2页，用page1做主镜
    "page3": [None, "page1.png"],                     # 场景A无角色页，只需主镜
    "page4": ["char-vivian-v2.png", None],            # 场景B首页，无主镜
    "page5": ["char-vivian-v2.png", "page4.png"],     # 场景B第2页，用page4做主镜
}
```

> 脚本需按页号顺序生成（不能并行），因为后续页可能依赖前序页作为场景主镜。脚本内部已有顺序生成逻辑。

### 何时不用场景主镜

- **首页**：场景的第一页自己就是主镜，不需要参考
- **转化页**：抽象视觉隐喻页（意识空间/隐喻空间）不属于真实场景，不用主镜
- **闪回页**：非当前时间线，不用当前场景主镜（但闪回内如有连续多页，闪回首页可做闪回主镜）

## 分镜节奏方法论

> 选帧解决"画什么"，改编策略解决"怎么转化"，节奏方法论解决"读者看着累不累、有没有被钩住"。

### 快慢节奏控制

漫画阅读是视觉节奏体验。连续相同密度的页面会让读者疲劳，必须有快慢交替。

#### 节奏公式

```
慢节奏页（铺垫/日常）→ 快节奏页（冲突/高潮）→ 慢节奏页（余韵/钩子）
```

每章至少经历一次"慢→快→慢"的完整节奏弧。

#### 慢节奏页写法

| 特征 | 效果 | 页面类型 |
|:-----|:-----|:---------|
| 大格+少格 | 给读者时间消化信息 | 大单页 或 多格页（1-2格大格） |
| 静态画面 | 角色站立/坐着/沉思 | 双格页（并列对照） |
| 环境描写多 | 建立场景氛围 | 大单页（全页场景建立） |
| 旁白多 | 信息密度靠文字承载 | 多格页 + narration 旁白条叠加 |

> 慢节奏页每 3-4 行原文对应 1 页，允许画面"呼吸"。

#### 快节奏页写法

| 特征 | 效果 | 页面类型 |
|:-----|:-----|:---------|
| 小格+多格 | 快速切换制造紧迫感 | 多格页（4-6格） |
| 动态画面 | 角色在运动/打斗 | 多格页（紧凑分格） |
| 动作拆解 | 一个动作拆成 2-3 个瞬间 | 双格页 或 多格页（连续动作） |
| 拟声词多 | 视觉冲击强化 | 大单页 + 提示词拟声词效果 |

> 快节奏页每 1-2 行原文对应 1 格（页内多格），单格信息量小但切换快。

#### 节奏标注

在分镜表中为每页标注节奏类型，确保交替：

| 页# | 节奏 | 页面类型 | 理由 |
|:----|:-----|:---------|:-----|
| 1 | 慢 | 大单页 | 场景建立 |
| 2 | 慢 | 多格页（2格） | 日常铺垫 |
| 3 | 快 | 多格页（4格） | 突发事件 |
| 4 | 快 | 多格页（5格） | 冲突升级 |
| 5 | 快 | 大单页 | 爆发瞬间 |
| 6 | 慢 | 双格页 | 余韵 |
| 7 | 慢 | 大单页 | 章末钩子页 |

> **自检**：连续 3 页以上相同节奏 = 节奏单调，需要调整。

### 钩子页设计

**每章最后一页必须是钩子页。** 钩子页的功能不是"画完本章剧情"，而是"让读者想看下一章"。

#### 钩子页类型

| 类型 | 适用场景 | 画面设计 | 页面类型 |
|:-----|:---------|:---------|:---------|
| 悬念型 | 下一章有重大揭示 | 角色看向画面外的某个东西，表情震惊/恐惧，不画出来那个东西 | 大单页 |
| 反转型 | 本章末尾发生反转 | 反转事件的瞬间画面，角色表情定格在不可置信 | 大单页 |
| 预告型 | 下一章有新角色/新势力 | 新角色的剪影/背影/局部特写，不露全貌 | 大单页 |
| 情绪型 | 本章情感浓烈 | 角色在情感高潮的瞬间定格，配合暗角和光效 | 大单页 |
| 倒计时型 | 下一章有紧迫危机 | 角色看向某个倒计时/逼近的威胁，画面有压迫感 | 大单页 |

> 钩子页通常使用大单页（1 页 1 格全页独占），配合暗角效果和未完成感。

#### 钩子页提示词写法

钩子页的提示词要强调**未完成感**——画面中有一个"没说完的故事"：

```
[Seedream 执行串(画风,含参考作品)]。A single full-page manga panel, no gutters, full bleed.
参考图中的人物形象，[视觉锚点串]。[角色名] [动作：看向画面外/定格在某个表情]，[环境(精简)]。
[情绪氛围]，画面有强烈的未完成感和悬念感，暗角效果。[风格保真约束]。
```

#### 钩子页文字叠加

钩子页的文字叠加使用 narration 旁白条或 dialogue 对白气泡，叠加规范详见 `references/page-layout-guide.md`：

```json
{"file": "pageN.png", "narration": "脚步声，越来越近……"}
```

> 文字不是必须的。如果画面本身悬念足够强，不加文字更好。

### 信息密度校准

**信息密度 = 每页承载的关键信息量。** 不是页数越多越好——2 页过渡页的信息密度不如 1 页高潮页。

#### 密度分级

| 密度等级 | 特征 | 典型场景 | 页数建议 |
|:---------|:-----|:---------|:---------|
| 高密度 | 每页都有不可跳过的关键信息 | 高潮章、揭示章 | 4-5 页，快节奏为主 |
| 中密度 | 部分页是过渡，但有信息锚点 | 标准章 | 3-4 页，快慢交替 |
| 低密度 | 大量页是氛围/情绪，信息点少 | 铺垫章、日常章 | 2-3 页，慢节奏为主 |

#### 密度优化原则

1. **砍过渡页**：如果一页的信息可以通过旁白或下一页的背景传达，砍掉它
2. **合并同类页**：两个连续的情绪页可以合并为一个更强的情绪页
3. **一页一焦点**：每页只传达一个核心焦点，不要在一页里塞太多信息线
4. **宁可少不可空**：2 页有信息的漫画 > 4 页一半是过渡的漫画

#### 密度自检

选帧完成后，逐页问自己：

```
这页如果删掉，读者会丢失什么信息？
├─ 丢失关键信息 → 保留
├─ 只丢失氛围 → 考虑合并到相邻页
└─ 什么都不丢失 → 砍掉
```

## 页面布局系统

> **v4.0 完全重写**。v3.x 的 7 种 HTML 布局类（layout-splash/split/fullwide/overlay/narrow/fullbleed/climax）已废弃。v4.0 中 HTML 不做格子布局，只做文字叠加——页面图由 Seedream 直出（含分格线、多格内容、镜头语言），HTML 全宽展示页面图 + 叠加文字层。

### 页面类型

v4.0 的页面类型由导演卡（Step 1）决定，Seedream 直出。HTML 层面不再选择布局类，只做全宽展示 + 文字叠加。

| 页面类型 | 格数 | 用途 | 提示词页面结构声明 |
|:---------|:-----|:-----|:-----------------|
| 大单页 | 1 格 | 名场面/冲击帧/章末钩子页/场景建立 | `A single full-page manga panel, no gutters, full bleed` |
| 双格页 | 2 格 | 对比/反应/并进/动作拆解 | `A manga comic page divided into 2 panels in {split} with thick black gutters` |
| 多格页 | 3-6 格 | 标准叙事页 | `A vertical manga comic page divided into {N} panels in {布局} with thick black gutters` |

> 页面类型在 Step 1 导演卡的页面设计表中确定。Step 2 生成时按导演卡执行，不在生成阶段临时决定。

### HTML 文字叠加

v4.0 的 HTML 只负责文字叠加，不负责格子布局。文字分两类：

| 文字类型 | HTML 元素 | 用途 | 位置 |
|:---------|:---------|:-----|:-----|
| narration | 旁白条 | 旁白叙述、内心独白、环境描述 | 页面顶部/底部/侧边 |
| dialogue | 对白气泡 | 角色台词 | 画面中角色附近 |

> 文字叠加的详细规范（旁白条样式、对白气泡样式、避让规则、动画效果）见 `references/page-layout-guide.md`。

### 排版原则

1. **页面类型由导演卡决定** — 不在生成阶段临时选择页面类型
2. **不要全用同一种页面类型** — 连续 3 页相同类型 = 读者疲劳
3. **多格页和大单页交替是基础节奏** — 大单页用于打破节奏
4. **每章至少 1 个大单页** — 视觉锚点（名场面或钩子页）
5. **最后一页必须是钩子页** — 章末大单页 + 未完成感
6. **场景切换用 scene-break** — 不要强行用画面过渡

### 视觉花样系统（提示词层面）

> v4.0：复杂视觉效果全部通过 Seedream 提示词实现（速度线、画面倾斜、色调滤镜等），HTML 层面不做视觉花样。

#### 提示词层面的视觉效果

以下效果无法通过 HTML 实现，需在 Seedream 提示词中写明：

| 视觉效果 | 提示词写法方向 | 适用场景 |
|:---------|:-------------|:---------|
| 速度线 | radiating speed lines, motion lines | 爆发瞬间、必杀技 |
| 画面倾斜 | dynamic angled composition | 紧张对峙、快速移动 |
| 闪回色调 | cold blue tint, dashed border frame | 闪回、记忆 |
| 单色滤镜 | sepia tone / monochrome noir | 历史叙述、戏剧性时刻 |
| 梦境效果 | soft blur, color shifted, dreamlike | 梦境、幻觉 |

#### 花样×叙事场景对照

| 叙事场景 | 推荐页面类型 | 提示词方向 | 效果 |
|:---------|:---------|:----------|:-----|
| 角色觉醒/变身 | 大单页 | speed lines + 发光 | 全页 + 速度线 = 爆发感 |
| 闪回记忆 | 多格页 | cold blue tint | 冷蓝 = 时间线区分 |
| 角色牺牲/死亡 | 大单页 | monochrome noir | 全页黑白 = 悲剧感 |
| 梦境/意识空间 | 大单页或多格页 | soft blur + color shift | 模糊 = 非现实感 |
| 新角色登场 | 大单页 | full body shot | 全页 + 仪式感 |
| 章末钩子 | 大单页 | 暗角 + 未完成感 | 全页 + 悬念 |

#### 使用纪律

1. **每章最多 2-3 个大单页** — 过多 = 花样自嗨，读者注意力被效果抢走
2. **页面类型服务于叙事** — 不是"好看就用"，是"这个场景需要什么叙事功能"
3. **复杂视觉效果走提示词** — 速度线/倾斜/色调等在 Seedream 提示词中写明，不在 HTML 层面叠加

## 构图骨架系统

> **v3.2.0 新增**。解决"格子里的画面怎么构图"的流程缺口——skill v3.1.0 管死了"格子怎么排"（HTML布局铁律），但"格子里的画面怎么构图"完全放养，导致普通帧默认出"主体居中+平视"的中庸构图。

### 核心概念：机位 ≠ 构图

| 维度 | 回答什么 | 选项 | 举例 |
|:-----|:---------|:-----|:-----|
| **机位** | 摄像机在哪 | 全景/中景/近景/特写 + 仰/平/俯 | 全景·仰视 |
| **构图** | 画面元素怎么排 | 三分法/对角线/框架式/仰角压迫/大留白/前景遮挡/对称/倾斜 | 对角线 |

两者独立选择，组合使用。例如"全景·仰视 + 对角线"="从低角度仰拍，画面元素沿对角线排列"。

### 九种构图手法

| 构图手法 | 英文提示词方向 | 叙事功能 | 适用场景 |
|:---------|:-------------|:---------|:---------|
| **三分法** | rule of thirds composition, subject at intersection | 视觉平衡，引导视线 | 日常/对话/过渡/场景建立 |
| **对角线** | diagonal composition, dynamic angle, leading diagonal lines | 动态张力，不安定感 | 冲突/追逐/战斗/精神动摇 |
| **框架式** | framing through doorway/arch/window/gap | 聚焦主体，窥视感 | 角色登场/揭示/偷窥/暗处观察 |
| **仰角压迫** | extreme low angle, looking up, imposing | 威压/崇高/权力感 | 大人物登场/威压建立/仰视敬畏 |
| **俯角渺小** | high angle looking down, vulnerable | 渺小/无助/被俯视 | 角色受困/被碾压/孤独/命运感 |
| **大留白** | extreme negative space, minimal composition, vast empty | 孤独/空旷/余韵/寂寥 | 余韵/章末/孤独/时间流逝 |
| **前景遮挡** | foreground silhouette occluding view, layered depth | 纵深/窥探/层次感 | 暗处观察/偷窥/伏击/通过缝隙看 |
| **对称构图** | symmetrical composition, centered, formal | 仪式/庄严/权力/秩序 | 朝堂/法阵/仪式/对称空间 |
| **倾斜构图** | dutch angle, tilted frame, off-balance | 不安/失衡/精神动摇 | 精神崩溃/混乱/颠覆/世界扭曲 |

### 构图骨架串组装规则

分格设计表的「画面方向」+「构图手法」两列，在 step2 组装提示词时翻译为英文**构图骨架串**，放在画风串之后（Seedream 对提示词开头权重最高）。在 v4.0 页级提示词中，每格的描述都包含该格的构图骨架串：

```
[Seedream 执行串]。A vertical manga comic page divided into {N} panels...
Panel 1: [构图骨架串]. 参考图中的人物形象，[视觉锚点串]...
Panel 2: [构图骨架串]. ...
```

**构图骨架串格式**：`{机位英文}, {构图手法英文}.`

**组装示例**：

| 画面方向 | 构图手法 | 构图骨架串（英文） |
|:---------|:---------|:-----------------|
| 全景·仰视 | 仰角压迫 | `WIDE SHOT, extreme low angle, looking up. Imposing symmetrical composition.` |
| 中景·平视 | 三分法 | `MEDIUM SHOT, eye level. Rule of thirds composition, subject at right intersection.` |
| 近景·俯视 | 前景遮挡 | `CLOSE-UP, high angle looking down. Foreground silhouette occluding view, layered depth.` |
| 特写·平视 | 大留白 | `EXTREME CLOSE-UP, eye level. Extreme negative space, minimal composition.` |
| 全景·仰视 | 对角线 | `WIDE SHOT, low angle. Diagonal composition, dynamic angle with leading diagonal lines.` |

### 构图交替原则

相邻格构图手法应有变化，连续 3 格以上相同构图 = 画面单调。

**推荐节奏示例**：
```
三分法 → 框架式 → 仰角压迫 → 对角线 → 大留白 → 前景遮挡 → 三分法
```

**反面案例**（v3.1.0 玄鉴仙族ch1560测试）：
```
全帧无构图标注 → Seedream 全部默认"主体居中+平视" → 16帧画面构图雷同，读者感觉中庸
```

### 名场面构图优先级

名场面页的构图选择比普通页更重要——名场面用"中庸构图"是最大的浪费。

| 页类型 | 构图选择 | 理由 |
|:-------|:---------|:-----|
| S级名场面页 | 从{仰角压迫/大留白/对角线/倾斜构图}中选 | 高冲击构图配合冲击页公式 |
| A级关键页 | 从{框架式/前景遮挡/俯角渺小}中选 | 有叙事功能的构图 |
| B级普通页 | 三分法（安全平衡） | 日常页不需要强构图 |
| 钩子页 | 大留白或倾斜构图 | 留悬念感 |

> **S级页禁用三分法**——三分法是"安全"构图，S级页需要的是"冲击"不是"安全"。
