# 分镜脚本指南

> Step 1 章节解构的参考指南。如何从一章网文中拆出该画的关键帧。

## 核心原则

**漫画不是小说的翻译，是小说的再创作。** 一章 3000 字不可能全画出来，必须选择——选错了帧，画得再好也讲不清故事。

**格数由内容决定，不由数字决定。** 一章有多少值得"看到"的瞬间，就拆多少格。Agent 拥有完整的格数判断权。

## 选帧六原则

### 1. 情绪转折点优先

每次角色情绪发生变化的地方，都是一个分镜候选。一章通常有 3-5 个情绪转折点。

```
示例（深渊主宰 ch001）：
绝望（米不够了）→ 温暖（抱狗）→ 恐惧（门外脚步声）→ 决绝（卖身）→ 崩溃（哭泣）→ 希望（哥哥苏醒）
= 6 个情绪转折 = 6 个分镜
```

### 2. 动作高潮优先

打斗、追逐、冲突的瞬间比静态对话更适合漫画。

### 3. 信息揭示优先

新角色登场、关键道具出现、真相揭露——这些是读者最想"看到"的瞬间。

### 4. 避免纯对话帧

两个人站着说话是最差的漫画画面。如果必须画对话，让角色在**做某事的同时**说话（边走边说、边做饭边说）。

### 5. 机位交替

```
推荐节奏：全景 → 中景 → 近景 → 特写 → 中景 → 全景 → 近景 → 特写
```

连续相同机位会让读者疲劳。特写用于情绪高潮，全景用于场景建立。

### 6. 格数判断

格数不锁死，Agent 根据章节内容密度自主判断：

| 章节类型 | 格数范围 | 判断依据 |
|:---------|:---------|:---------|
| 过渡章（日常/铺垫） | 4-6格 | 情绪平稳，关键场面少 |
| 标准章（起承转合） | 6-8格 | 3-5个情绪转折，节奏正常 |
| 内容密集章（多线/战斗） | 10-15格 | 多场动作高潮，信息密集 |
| 高潮章（大事件爆发） | 15-20格 | 事件密度极高，分多页呈现 |

**核心判断标准**：每个值得"看到"的瞬间都该有独立分镜。宁可多画不可漏画——漏掉关键场面比多画几格更影响阅读体验。

超过12格时考虑分页（排版配置中用 separator 分隔，每页6-10格）。

### 7. 高光独占格

**原文中的高光时刻必须独占至少一格，禁止和多件事挤在同格。** 这是选帧的铁律。

高光时刻的判断标准：
- **反应型高光**：角色情绪骤变（震惊/暴怒/崩溃）→ 独占一格 reaction shot
- **转折型高光**：剧情方向逆转（背叛揭露/身份揭示）→ 独占一格，用特写或大格
- **震撼型高光**：空间或认知骤变（觉醒/进入新世界）→ 用**两格**：先压迫铺垫格（窄、暗、局促）再破格展开格（开阔、逆光、大画面），一抑一扬才出震撼

**反例**：把"角色A说话+角色B震惊反应+环境变化"塞进一格 → 三个信息互相稀释，哪个都没冲击力
**正例**：A说话一格（中景），B震惊反应一格（特写），环境变化一格（全景）→ 三格递进，每格一个焦点

> 独占格不等于大格。反应型高光可以用半宽格+特写，关键是**信息独占**——这一格只讲一件事。

### 8. 名场面设计

> 高光独占格解决"信息不稀释"，名场面设计解决"画面有没有冲击力"。一个独占格如果内容本身不震撼，独占了也是浪费格数。

#### 名场面识别三标准

一帧是否值得成为"名场面"（读者会截图分享的帧），用三条标准检验：

| 标准 | 检验问题 | 满足条件 |
|:-----|:---------|:---------|
| 视觉奇观 | 这个画面画出来好不好看？有没有"哇"的瞬间？ | 画面有壮丽/震撼/诡异/美丽的视觉元素 |
| 情绪爆发 | 这个画面能不能让读者感到什么？ | 画面承载了强烈的情绪（震撼/悲壮/热血/恐惧） |
| 剧情转折 | 这个画面是否改变了故事走向？ | 画面呈现的是一个转折点/决策点/揭示点 |

**三条满足两条 = 名场面。** 名场面必须用最大布局（panel-splash 或 panel-fullbleed）+ 视觉花样 + 高精度提示词。

> 每章至少 1 个名场面。如果一章找不出一个名场面，说明选帧有问题——不是每一章都有"画面感"强的内容，但每一章至少有一个"读者会记住"的瞬间。

#### 张力构建五技法

名场面不是"把事情画出来"，是"让读者感受到冲击"。五种技法：

| 技法 | 原理 | 提示词写法 | 示例 |
|:-----|:-----|:-----------|:-----|
| **尺度对比** | 角色渺小 vs 环境宏大 | 画面中放入参照物强调尺度差距 | 剑仙立于百丈剑峰前，人如蝼蚁，剑意却裂开半座山 |
| **静默铺垫** | 爆发前留一格安静的 | 前一帧用静态/沉默画面，与爆发帧形成反差 | 对话→沉默特写→爆发（三帧递进，一静一动） |
| **反应镜头** | 不画事件本身，画旁观者的反应 | 画角色被光照亮/被冲击波掀飞/表情定格 | 不画出爆炸，画所有人被金光映亮的脸 |
| **视觉隐喻** | 用象征物承载情绪 | 将抽象概念具象为可视物体 | 金卷缓缓展开=战争倒计时启动；断剑插在废墟中=战败 |
| **留白截断** | 关键时刻画面截断 | 画面只展示前半，后半留给下一帧或读者想象 | 手触碰门把手→下一格已是门内景象 |

> 五技法可组合使用。最经典的冲击帧 = 静默铺垫 + 尺度对比 + 反应镜头（先安静→突然展示宏大→画角色的反应）。

#### 冲击帧提示词升级

普通帧的提示词写"发生了什么"，冲击帧的提示词写"**后果和感受**"：

| 错误写法 | 正确写法 |
|:---------|:---------|
| 剑意冲霄 | 百丈山峰被无形剑气切出一道裂痕，碎石纷飞如暴雨，剑仙负手立于裂痕之上 |
| 金瞳亮起 | 金色重瞳中倒映出整个蜀地版图，瞳孔中城池燃烧、山河崩塌 |
| 他很愤怒 | 桌案在掌下碎裂，木屑飞溅，地面出现蛛网裂纹，周围侍卫惊恐后退 |
| 他出关了 | 石门炸裂，尘雾中一道剑光冲天而起，方圆十里的飞鸟惊散，山石龟裂 |

**冲击帧公式**：

```
[最大布局 panel-splash/fullbleed] + [Seedream 执行串] + [具体视觉奇观描述] + [环境/他人反应] + [风格保真约束 + 高精度模板 HARD CONSTRAINTS]
```

> 冲击帧必须使用高精度模板（4 块结构），因为普通提示词的约束力不够，容易画成泛化的"能量光效"而非具体的视觉奇观。

#### 名场面 vs talking head

**最大的反模式是 talking head（说话的头）**——角色站着/坐着说话，画面没有任何视觉信息，全靠对白气泡撑着。

| talking head（避免） | 名场面（追求） |
|:--------------------|:-------------|
| 角色A对角色B说"我要攻蜀"，两人站着对话 | 角色A的金瞳中倒映出燃烧的城池，手按在案上，案面出现裂纹 |
| 角色C说"我很强"，展示能力 | 山峰被无形力量切开，角色C站在裂痕中央，碎石悬浮 |
| 角色D说"出发"，转身离开 | 角色D的背影消失在山门中，身后剑光冲天，飞鸟惊散 |

> **核心原则**：如果一帧的画面去掉对白气泡后什么都没有，它就是 talking head。名场面的画面应该**不需要对白也能传达信息**。

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

用 1-2 句旁白框概括大段文字，搭配一个**不直接叙事但氛围契合**的画面。旁白承担信息，画面承担情绪。

适用：世界观设定、背景历史、大段解释性文字

| 原文内容 | 旁白文字 | 搭配画面 |
|:---------|:---------|:---------|
| 诸神之战历史+圣者时代+玩家机制 | "这个世界将来会迎来诸神的黄昏。" | 末日异象：天空撕裂，恶魔降临，城市燃烧 |
| 脑域开发科普+虚拟游戏背景 | "他的意识曾在虚拟世界中穿行。" | 角色闭眼，头顶浮现半透明的数据流光晕 |
| 贫民区背景介绍 | "这里是琥珀城被遗忘的角落。" | 贫民区全景：破败建筑、泥泞街道、麻木的人群 |

> **关键**：旁白字数控制在 15 字以内，画面要有足够的视觉冲击力独立成立。

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

> 闪回帧的提示词中应明确标注这是非当前时间线画面，使用上述一种或多种手段。

### 改编自检清单

选帧+转化设计完成后，逐条核对：

- [ ] 原文中每条**关键信息**都有对应的帧或旁白承载？
- [ ] S 级信息是否分到了最佳帧位（名场面/冲击帧）？
- [ ] 本章至少有 1 个名场面（三标准满足两条）？
- [ ] 名场面不是 talking head（去掉对白气泡后画面仍有信息）？
- [ ] 冲击帧的提示词写的是"后果和感受"而非"发生了什么"？
- [ ] 视觉转化帧的提示词是否具体到可执行（有明确画面、动作、环境）？
- [ ] 旁白浓缩帧的旁白文字是否已拟好且 ≤15 字？
- [ ] 闪回/记忆帧是否有视觉区分手段？
- [ ] 从读者视角通读分镜序列：不看原文能理解本章发生了什么吗？

> 如果读者不看原文会丢失关键理解 → 回到步骤 3，补加转化帧或旁白。

## 分镜提示词写法

### 公式

> **v2.9.2 重构**：画风从末尾移到开头（高权重位），场景描述精简，末尾加风格保真约束。解决分镜帧画风漂移到"电影概念艺术"的问题。

```
[Seedream 执行串(画风,含参考作品)]。参考图中的人物形象，[视觉锚点串]。[微表情串(如有情绪)]。[角色动作描述]。[场景环境描述(精简≤2句)]。[情绪氛围]。[风格保真约束]。
```

**结构对比**：

| 位置 | 旧公式(失败) | 新公式(修复) |
|:-----|:------------|:------------|
| 开头 | `参考图中的人物形象` | `[Seedream 执行串]` ← 画风前置，高权重 |
| 中段 | 角色动作 + 场景(详细) | 角色动作 + 场景(**精简≤2句**) |
| 末尾 | `[风格锚定串]` ← 低权重，被淹没 | `[风格保真约束]` ← HARD CONSTRAINTS 防漂移 |

### 示例

旧写法（失败——画风在末尾被淹没）：
```
参考图中的人物形象。瘦弱女孩侧面蹲在破旧灶台前，用木棍搅动陶碗里的稀粥，
灶膛火光映亮她的脸。破烂的屋顶漏雨，屋内弥漫浓烟和蒸汽。阴暗破败的贫民区小屋，
墙角堆着湿柴。暗黑奇幻半写实日式漫画风格，水彩质感笔触，灰暗色调，暖色火光点缀，压抑氛围。
```

新写法（修复——画风前置+保真约束后置）：
```
Semi-thick painting manga style, clean hard outer contour lines as skeleton with soft gradient shading inside color blocks, cel-shaded base with painterly soft-light overlays, 7.5-head semi-realistic proportions, modern refined illustration. Art style similar to Da Feng Da Geng Ren manga adaptation. 参考图中的人物形象，short messy black hair, black eyes, pale skin, thin build, worn dark jacket。瘦弱女孩侧面蹲在破旧灶台前，用木棍搅动陶碗里的稀粥，灶膛火光映亮她的脸。破败小屋，屋顶漏雨。压抑氛围。Maintain visible outer contour lines. Use soft gradient shading inside color blocks, not full painterly blending. Keep manga readability. No lineless style. No cinematic concept art. No photorealistic 3D rendering.
```

### 注意事项

- **首句必须是 Seedream 执行串**（从漫画角色库的风格锚定串字段复制），不能以"参考图中的人物形象"开头
- **场景描述精简到≤2句**——过长的场景描述会把 Seedream 推向"电影概念艺术"模式，淹没画风
- **末尾必须有风格保真约束**（从漫画角色库的风格保真约束字段复制），防止画风漂移
- 不写对白（对白用 HTML 排版 caption 嵌入底部渐变遮罩）
- 不写任何文字内容（Seedream 文字渲染不可控）
- ≤300 字（英文部分不计入字数限制）

### 关键帧升级：高精度模板

**高潮帧、变身帧、名场面**可升级为高精度模板写法（见 `../pop-novel-visual/references/seedream-prompt-guide.md` §1.10）。在基础提示词上增加：

1. **镜头规格**：焦段（24mm/35mm）+ 机位（仰角/俯角/平视）
2. **渲染要求**：材质质感列表（fabric texture / leather / hair strands / particles）
3. **硬约束**：No duplicated limbs. Exactly five fingers. No chibi proportions.

> 普通帧不需要升级，速度优先。只有"值得读者停留 3 秒"的帧才值得用高精度模板。

## 对白/旁白/拟声词分类

| 类型 | HTML 排版处理 | 示例 |
|:-----|:-------------|:-----|
| 角色台词 | caption 文字嵌入底部渐变遮罩 | "你会保护我的，对不对？" |
| 内心独白 | caption 文字嵌入底部渐变遮罩 | 米不多了。 |
| 环境拟声词 | 提示词中写明拟声词效果 | 啪！BOING—— |
| 人群喊叫 | 提示词中写明人群喊叫效果 | 打死小偷！ |
| 旁白叙述 | caption 文字嵌入底部渐变遮罩（超长用 layout-narrow 侧边文字面板） | 脚步声。不止一个人。 |

> 旁白嵌入规范详见 `references/layout-pool.md` 原文旁白嵌入规范章节。

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

> **使用方式**：每帧提示词中，`参考图中的人物形象` 后面紧跟锚点提示词串，确保 AI 在每帧中都能提取到相同的识别标签。

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

> 同一场景的多格之间，空间结构、光源方向、材质质感必须一致。场景主镜是跨格场景一致性的核心手段。

### 核心规则

同一场景的**首格**生成并确认后，成为该场景的"主镜"（scene master）。该场景后续每格生成时，**必须将场景主镜图作为参考图之一输入**（与角色定妆图并列），锁定空间布局、光源方向、环境材质。

```
场景首格 → 确认 → 成为场景主镜
场景第2格 → 参考图 = [角色定妆图] + [场景主镜图]
场景第3格 → 参考图 = [角色定妆图] + [场景主镜图]
场景切换 → 旧主镜废弃，新场景首格成为新主镜
```

### 分镜表标注

分镜脚本表中新增**场景组**列，标识每帧所属的场景：

| 帧号 | 场景组 | 场景 | 角色动作 | ... | 定妆图版本 | 场景主镜 |
|:-----|:-------|:-----|:---------|:----|:-----------|:---------|
| 1 | A | 破屋雨夜 | 薇薇安抓米 | ... | char-vivian-v1 | —（首格，自己成为主镜） |
| 2 | A | 破屋灶台 | 薇薇安抱狗 | ... | char-vivian-v1 | frame1.png |
| 3 | A | 破屋门外 | 脚步声逼近 | ... | — | frame1.png |
| 4 | B | 集市 | 薇薇安穿新衣 | ... | char-vivian-v2 | —（新场景，自己成为主镜） |
| 5 | B | 集市 | 被人群推搡 | ... | char-vivian-v2 | frame4.png |

> 场景组相同的帧共享同一个场景主镜。场景组切换 = 旧主镜废弃，新场景首格成为新主镜。

### 提示词写法

场景主镜图作为图生图参考时，提示词中追加环境锁定描述：

```
[Seedream 执行串]。参考图中的人物形象，[视觉锚点串]。[角色动作描述]。
场景环境与参考图一致：[从场景主镜提取的空间特征，如"破败小屋，左侧灶台，右墙漏雨"]。
光源方向与参考图一致：[如"灶膛火光从左下方照射"]。
[情绪氛围]。[风格保真约束]。
```

> 场景主镜锁的是**空间+光源+材质**，不是角色。角色一致性仍由角色定妆图负责。

### generate_storyboard.py 配置

`FRAME_REFS` 升级为支持多参考图（角色定妆图 + 场景主镜）：

```python
# 按帧映射参考图：[角色定妆图, 场景主镜图]
FRAME_REFS = {
    "frame1": ["char-vivian-v1.png", None],           # 场景A首格，无主镜
    "frame2": ["char-vivian-v1.png", "frame1.png"],    # 场景A第2格，用frame1做主镜
    "frame3": [None, "frame1.png"],                    # 场景A无角色帧，只需主镜
    "frame4": ["char-vivian-v2.png", None],            # 场景B首格，无主镜
    "frame5": ["char-vivian-v2.png", "frame4.png"],    # 场景B第2格，用frame4做主镜
}
```

> 脚本需按帧号顺序生成（不能并行），因为后续帧可能依赖前序帧作为场景主镜。脚本内部已有顺序生成逻辑。

### 何时不用场景主镜

- **首格**：场景的第一格自己就是主镜，不需要参考
- **转化帧**：抽象视觉隐喻帧（意识空间/隐喻空间）不属于真实场景，不用主镜
- **闪回帧**：非当前时间线，不用当前场景主镜（但闪回内如有连续多格，闪回首格可做闪回主镜）

## 分镜节奏方法论

> 选帧解决"画什么"，改编策略解决"怎么转化"，节奏方法论解决"读者看着累不累、有没有被钩住"。

### 快慢节奏控制

漫画阅读是视觉节奏体验。连续相同密度的格子会让读者疲劳，必须有快慢交替。

#### 节奏公式

```
慢节奏段（铺垫/日常）→ 快节奏段（冲突/高潮）→ 慢节奏段（余韵/钩子）
```

每章至少经历一次"慢→快→慢"的完整节奏弧。

#### 慢节奏段写法

| 特征 | 效果 | 布局选择 |
|:-----|:-----|:---------|
| 大格+少格 | 给读者时间消化信息 | panel-splash 或 panel-fullwide |
| 静态画面 | 角色站立/坐着/沉思 | panel-split（50/50 并列） |
| 环境描写多 | 建立场景氛围 | panel-fullwide（4:3 横幅） |
| 旁白多 | 信息密度靠文字承载 | panel-narrow（侧边文字面板） |

> 慢节奏段每 3-4 行原文对应 1 格，允许画面"呼吸"。

#### 快节奏段写法

| 特征 | 效果 | 布局选择 |
|:-----|:-----|:---------|
| 小格+多格 | 快速切换制造紧迫感 | panel-split 连续 |
| 动态画面 | 角色在运动/打斗 | panel-fullwide 紧凑排列 |
| 动作拆解 | 一个动作拆成 2-3 个瞬间 | panel-split（左右对照） |
| 拟声词多 | 视觉冲击强化 | panel-fullbleed + sfx 拟声词 |

> 快节奏段每 1-2 行原文对应 1 格，单格信息量小但切换快。

#### 节奏标注

在分镜表中为每帧标注节奏类型，确保交替：

| 帧# | 节奏 | 布局 | 理由 |
|:----|:-----|:-----|:-----|
| 1 | 慢 | panel-splash | 场景建立 |
| 2 | 慢 | panel-fullwide | 日常铺垫 |
| 3 | 快 | panel-split | 突发事件 |
| 4 | 快 | panel-split | 冲突升级 |
| 5 | 快 | panel-fullbleed | 爆发瞬间 |
| 6 | 慢 | panel-fullwide | 余韵 |
| 7 | 慢 | panel-climax | 章末钩子 |

> **自检**：连续 3 帧以上相同节奏 = 节奏单调，需要调整。

### 钩子帧设计

**每章最后一格必须是钩子帧。** 钩子帧的功能不是"画完本章剧情"，而是"让读者想看下一章"。

#### 钩子帧类型

| 类型 | 适用场景 | 画面设计 | HTML 布局 |
|:-----|:---------|:---------|:----------|
| 悬念型 | 下一章有重大揭示 | 角色看向画面外的某个东西，表情震惊/恐惧，不画出来那个东西 | panel-climax + 居中遮罩 |
| 反转型 | 本章末尾发生反转 | 反转事件的瞬间画面，角色表情定格在不可置信 | panel-climax + 居中遮罩 |
| 预告型 | 下一章有新角色/新势力 | 新角色的剪影/背影/局部特写，不露全貌 | panel-fullbleed + 底部遮罩 |
| 情绪型 | 本章情感浓烈 | 角色在情感高潮的瞬间定格，配合暗角和光效 | panel-climax |
| 倒计时型 | 下一章有紧迫危机 | 角色看向某个倒计时/逼近的威胁，画面有压迫感 | panel-climax + 居中遮罩 |

#### 钩子帧提示词写法

钩子帧的提示词要强调**未完成感**——画面中有一个"没说完的故事"：

```
[Seedream 执行串]。参考图中的人物形象，[视觉锚点串]。[角色名] [动作：看向画面外/定格在某个表情]，[环境(精简)]。
[情绪氛围]，画面有强烈的未完成感和悬念感，暗角效果。[风格保真约束]。
```

#### 钩子帧排版配置

使用 `layout: "climax"` 布局类，85vh 最大画幅 + 居中文字渐变遮罩。caption 文字叠加在底部遮罩区域：

```json
{"file": "frameN.png", "layout": "climax", "caption": "脚步声，越来越近……"}
```

> caption 不是必须的。如果画面本身悬念足够强，不加文字更好。详见 `references/layout-pool.md` layout-climax 布局。

### 信息密度校准

**信息密度 = 每格承载的关键信息量。** 不是格数越多越好——6 格过渡帧的信息密度不如 2 格高潮帧。

#### 密度分级

| 密度等级 | 特征 | 典型场景 | 格数建议 |
|:---------|:-----|:---------|:---------|
| 高密度 | 每格都有不可跳过的关键信息 | 高潮章、揭示章 | 8-15格，快节奏为主 |
| 中密度 | 部分格是过渡，但有信息锚点 | 标准章 | 6-8格，快慢交替 |
| 低密度 | 大量格是氛围/情绪，信息点少 | 铺垫章、日常章 | 4-6格，慢节奏为主 |

#### 密度优化原则

1. **砍过渡帧**：如果一帧的信息可以通过旁白或下一帧的背景传达，砍掉它
2. **合并同类帧**：两个连续的情绪帧可以合并为一个更强的情绪帧
3. **一帧一信息**：每帧只传达一个关键信息点，不要在一帧里塞两个信息
4. **宁可少不可空**：4 格有信息的漫画 > 8 格一半是过渡的漫画

#### 密度自检

选帧完成后，逐帧问自己：

```
这帧如果删掉，读者会丢失什么信息？
├─ 丢失关键信息 → 保留
├─ 只丢失氛围 → 考虑合并到相邻帧
└─ 什么都不丢失 → 砍掉
```

## 页面布局系统

> 拼图系统支持多变布局。选帧时需为每帧指定布局类，拼图时按布局类排版。

> **v3.0.0 新增排版池**：7 种 HTML 排版布局的详细 CSS 实现、适用场景、叙事功能、避让规则见 `references/layout-pool.md`。HTML 排版是 v3.0.0 起的主要产出格式，Pillow 拼图为备选。

### 叙事驱动布局（v2.10.0 新增）

> **布局不从模板出发，从叙事需求推导。** Step 1 导演卡的页面设计表和分格设计表已经确定了每页的功能位、视觉重心、每格的布局类和节奏。Step 2 拼图时**直接继承导演卡的分格设计表**，不重新决定布局。

**推导链**：故事层情感曲线 → 页层功能位 → 格层布局类 → HTML 排版

| 推导环节 | 在哪里做 | 产出 |
|:---------|:---------|:-----|
| 情感曲线标注 | Step 1 步骤2.5 | 读者情绪轨迹 + 转折点 |
| 页面分割 | Step 1 步骤7 | 页面设计表（功能位/视觉重心/格数预算） |
| 分格布局 | Step 1 步骤8 | 分格设计表（布局类/节奏/效果类/画面方向） |
| HTML 排版 | Step 2 §6 | 按分格设计表的布局类生成 HTML 漫画页面 |

> **铁律：每个布局选择必须能回答"为什么这么布局"。** 回答不出 = 为动态而动态。S 级信息 → 独占大格；快节奏 → 紧密小格；高潮 → panel-splash/fullbleed；章末 → panel-climax。这些不是模板，是叙事需求推导的结果。

### 布局类速查

> v3.0.0 更新：以下布局类对应 `references/layout-pool.md` 排版池中的 7 种 HTML 布局。CSS 实现要点和避让规则详见排版池参考文件。

| 布局类 | HTML layout 值 | 用途 | 视觉效果 | 使用频率 |
|:-------|:--------------|:-----|:---------|:---------|
| `panel-splash` | layout-splash | 竖幅开场/场景建立 | 3:4全屏+标题叠加+底部遮罩 | 每章 1-2 次 |
| `panel-split` | layout-split | 对比/并进/反应 | 50/50分割+中线分隔 | 每章 1-3 次 |
| `panel-fullwide` | layout-fullwide | 情感舒缓/环境交代 | 4:3横幅+底部遮罩 | 每章 2-4 次 |
| `panel-overlay` | layout-overlay | 戏剧转折/因果对照 | 主图全幅+右下inset 35% | 每章 0-1 次 |
| `panel-narrow` | layout-narrow | 旁白密集/静态段落 | flex 30/70 左文字右竖图 | 每章 0-2 次 |
| `panel-fullbleed` | layout-fullbleed | 战斗/冲击/破格 | 100vw出血+16:9横幅 | 每章 0-1 次 |
| `panel-climax` | layout-climax | 情感高潮/章末收尾 | 3:4竖幅85vh+居中遮罩 | 每章 1 次（末帧） |
| `scene-break` | scene-break | 场景切换 | ◇ ◇ ◇ 分隔线 | 按需 |

### 页面功能位→布局映射

> v2.10.0 升级：从"情感段位"升级为"页面功能位"，与 Step 1 步骤7 的四种页面功能位对齐。布局选择从导演卡的页面设计表推导，不在 Step 2 临时决定。

| 页面功能位 | 典型布局序列 | 视觉重心 | 理由 |
|:-----------|:------------|:---------|:-----|
| 建立页 | panel-splash → panel-fullwide → panel-split | 场景全景 | splash大格开场建立空间感，fullwide交代角色，split展示互动 |
| 发展页 | panel-split/panel-narrow 交替 → panel-fullwide 停在关键信息 | 角色互动/信息揭示 | 快慢交替推进因果，fullwide锚定关键转折 |
| 高潮页 | panel-fullbleed/panel-overlay → panel-split 反应 → panel-climax 后果 | 名场面/冲击帧 | 出血/叠加定格爆发，split画反应，climax画后果 |
| 钩子页 | panel-fullwide 余韵 → panel-climax 悬念 | 余韵/悬念暗示 | fullwide收束情绪，climax最大画幅留悬念 |

> **布局序列不是模板**——它是"如果这页是高潮页，通常这样排列"的参考。实际布局以导演卡分格设计表为准，因为分格设计表是基于本章具体内容推导的。

### 排版六原则

1. **从导演卡分格设计表继承布局** — 布局在 Step 1 已从叙事需求推导，Step 2 不重新决定布局类（详见 `references/layout-pool.md` 排版池）
2. **不要全用同一种格子** — 连续 3 个相同布局 = 读者疲劳
3. **fullwide 和 split 交替是基础节奏** — splash/fullbleed/climax 用于打破节奏
4. **每章至少 1 个 splash 或 climax** — 视觉锚点
5. **最后一格必须是 panel-climax** — 章末最大画幅+钩子文字
6. **场景切换用 scene-break** — 不要强行用画面过渡

### 视觉花样系统（HTML 布局 + 提示词效果）

> v3.0.0 更新：HTML 排版阶段，布局类决定"格子多大+什么叙事功能"，复杂视觉效果通过 Seedream 提示词实现。Pillow 备选方案中 style 字段仍可用（normal/feature/impact/hook）。排版池详见 `references/layout-pool.md`。

#### 提示词层面的视觉效果

以下效果无法通过 HTML 布局类实现，需在 Seedream 提示词中写明：

| 视觉效果 | 提示词写法方向 | 适用场景 |
|:---------|:-------------|:---------|
| 速度线 | radiating speed lines, motion lines | 爆发瞬间、必杀技 |
| 画面倾斜 | dynamic angled composition | 紧张对峙、快速移动 |
| 闪回色调 | cold blue tint, dashed border frame | 闪回、记忆 |
| 单色滤镜 | sepia tone / monochrome noir | 历史叙述、戏剧性时刻 |
| 梦境效果 | soft blur, color shifted, dreamlike | 梦境、幻觉 |

#### 花样×叙事场景对照

| 叙事场景 | 推荐布局 | 提示词方向 | 效果 |
|:---------|:---------|:----------|:-----|
| 角色觉醒/变身 | layout-fullbleed | speed lines + 发光 | 出血+速度线=爆发感 |
| 闪回记忆 | layout-overlay | cold blue tint | inset+冷蓝=时间线区分 |
| 角色牺牲/死亡 | layout-climax | monochrome noir | 最大画幅+黑白=悲剧感 |
| 梦境/意识空间 | layout-narrow | soft blur + color shift | 文字面板+模糊=非现实感 |
| 新角色登场 | layout-splash | full body shot | 全幅+标题=仪式感 |
| 章末钩子 | layout-climax | 暗角+未完成感 | 最大画幅+遮罩=悬念 |

#### 使用纪律

1. **每章最多 2-3 个进阶布局**（overlay/fullbleed） — 过多=花样自嗨，读者注意力被效果抢走
2. **布局服务于叙事** — 不是"好看就用"，是"这个场景需要什么叙事功能"（详见 `references/layout-pool.md` 画风适配规则）
3. **复杂视觉效果走提示词** — 速度线/倾斜/色调等在 Seedream 提示词中写明，不在 HTML 层面叠加
