# 内容层（Content Layer）

> Step 2 每格内容填充的强制参考。**工程化复现铁律：画风基准库管"画风"，排版基准库管"格子怎么排"，本文件管"每格内容怎么填"。**
> 前两支柱是"固定底盘"，本文件是"可变内容"——把每格场景装进元尊V1画风 + 元尊YZ-1~8排版里。

## 一、三段链路（先定整页 → 再排格 → 再填格内）

```
① 整页系统（本文件§二）→ ② 排版结构（layout-baseline选YZ-1~8）→ ③ 每格镜语（本文件§三-§五）
```

**核心顺序：先定整页叙事，再选排版，最后进格内镜语。** 不要倒过来——先排格子再想整页，会变成格子罗列。

---

## 二、整页系统（每页先于镜语的设计决策）

> 这一层管"整页作为一个叙事系统怎么编排"。核心铁律：**没有跨格的编排，就没有职业漫画的质感。**

### 2.1 整页设计顺序（每组页面必走）

1. **定整页情绪单元**：这页要承载什么情绪（从情感曲线推导）
2. **定页级色彩分区**：主色系 + 冷暖/线索色叙事（写进页面设计表备注）
3. **定跨格编排**：是否需要结构性破框？需要几个格的情绪蒙太奇累加？
4. **定权力姿态**：本页高位/神秘角色是否背影/侧影不露正脸？
5. **对应垂直象征轴线**：纵向页里权威格在上/受难格在下？

### 2.2 七个页级语法维度

| # | 维度 | 核心 | 强制要求 |
|:-:|:-----|:-----|:---------|
| 1 | **页面级色彩分区** | 色彩=叙事结构，不做氛围点缀 | 每页先定主色系+分区方式（冷/暖/线索色） |
| 2 | **权力姿态** | 背影/侧影=权威语法，不露正脸 | 每个高位/神秘角色标注是否全程不露正脸 |
| 3 | **垂直象征轴线** | 天(权威)—地(中介)—人(受难)三才 | 纵向页权威格在上/受难格在下 |
| 4 | **结构性破框** | 元素贯穿多格/前景压框线/特效层跨页 | 张力页优先设计1处结构性破框 |
| 5 | **情绪蒙太奇** | 多格累加同情绪（部位累加+景别推进） | 情绪高光拆2-3格，末格悬置 |
| 6 | **拟声字视觉编排** | 交给HTML，但导演卡必须规划 | 张力页标注拟声字（格位+内容+形制+颜色） |
| 7 | **每格完成度基准** | 拒绝廉价留白 | 每格标注满/实/剪影，满页剪影≤2 |

**每页完成度配额**：

| 层级 | 基准 | 每页配额 |
|:-----|:-----|:---------|
| **S级满格** | 完整场景透视+多角色+特效齐全 | ≤2格/页 |
| **A级实格** | 完整环境+角色+局部特效 | ≥过半格数 |
| **B级剪影格** | 明确设计意图的剪影/留白（节奏用） | ≤1-2格/页 |
| **禁用** | 无意图模糊背景+单人头部死板正面 | 0 |

---

## 三、每格镜语：镜头 × 构图 × 美术特效（L/C/F 三码）

> 每一格 = **镜头码 + 构图码 + 美术特效码** 三段拼接。**一格三码缺一不可。** 导演卡写编号（如 `L5 C3 F2`），组装提示词时翻译为英文串。

```
Panel N: {镜头码英文}, {构图码英文}. {美术特效码英文}. {光影}. {场景}. {人物}.
```

### 3.1 镜头模板库（L1-L12）

| 码 | 镜头 | 英文骨架串 | 叙事功能 | 常用情绪 |
|:---|:-----|:----------|:---------|:---------|
| L1 | 极远景 | `EXTREME WIDE SHOT, high angle looking down` | 人如蝼蚁，天地苍茫 | 孤寂/宿命/渺小 |
| L2 | 全景·平视 | `WIDE SHOT, eye level` | 交代环境+关系 | 建立/过渡 |
| L3 | 全景·仰视 | `WIDE SHOT, low angle looking up` | 主体威严高大 | 威压/仰视 |
| L4 | 中景 | `MEDIUM SHOT, eye level` | 人物动作主体 | 推进/对话 |
| L5 | 近景 | `MEDIUM CLOSE-UP, eye level` | 表情+上半身动作 | 情绪/反应 |
| L6 | 特写 | `CLOSE-UP, eye level` | 单一情绪聚焦 | 情感钉 |
| L7 | 大特写 | `EXTREME CLOSE-UP` | 局部细节（眼/手/伤） | 爆发/心理 |
| L8 | 特写·仰视 | `CLOSE-UP, low angle looking up` | 个体压迫感放大 | 恐惧/威压 |
| L9 | 特写·俯视 | `CLOSE-UP, high angle looking down` | 个体被压垮 | 无助/受制 |
| L10 | 过肩 | `OVER-SHOULDER SHOT, eye level` | 窥视第二人视角 | 对峙/威胁 |
| L11 | 剪影 | `SILHOUETTE SHOT` | 隐身份/远望/氛围 | 悬念/决绝 |
| L12 | 主观视角 | `POV SHOT, first-person perspective` | 读者代入角色眼睛 | 沉浸/逼近 |

> **景别递进原则**：情绪推进从大到小（全→中→近→特）制造"逼近感"；情绪释放从小到大（特→中→全）制造"抽离感"。连续2格同景别=单调。

### 3.2 构图模板库（C1-C10）

| 码 | 构图 | 英文骨架串 | 叙事功能 | 适用情绪 |
|:---|:-----|:----------|:---------|:---------|
| C1 | 三分法 | `rule of thirds composition, subject at {交点}` | 平衡/引导视线 | 日常/对话 |
| C2 | 对角线 | `diagonal composition, dynamic angle, leading diagonal lines` | 动态张力/不安定 | 冲突/追逃 |
| C3 | 框架式 | `framing through {doorway/arch/window/gap}` | 聚焦/窥视感 | 登场/揭示/偷窥 |
| C4 | 仰角压迫 | `extreme low angle, looking up, imposing composition` | 威压/崇高 | 强者/权力 |
| C5 | 俯角渺小 | `high angle looking down, vulnerable composition` | 渺小/无助 | 受困/命运 |
| C6 | 大留白 | `extreme negative space, minimal composition, vast empty` | 孤独/余韵 | 章末/寂寥 |
| C7 | 前景遮挡 | `foreground silhouette occluding view, layered depth` | 纵深/窥探 | 暗处/伏击 |
| C8 | 对称 | `symmetrical composition, centered, formal` | 仪式/秩序 | 朝堂/法阵 |
| C9 | 倾斜 | `dutch angle, tilted frame, off-balance` | 失衡/精神动摇 | 崩溃/扭曲 |
| C10 | 对位并置 | `visual juxtaposition, two contrasting elements side by side in frame` | 冲突并置/对比象征 | 宿敌/善恶/今昔 |

> **S级页禁用 C1（三分法）**——S级页需要冲击不是安全。名场面从{C2/C4/C6/C9/C10}中选。相邻格构图必须变化，连续2格相同构图=单调。

### 3.3 美术特效模板库（F1-F9）

| 码 | 特效 | 英文骨架串 | 情绪作用 | 适用场景 |
|:---|:-----|:----------|:---------|:---------|
| F1 | 集中线 | `radial concentration lines converging {on character face/object}, spotlight effect` | 心理聚焦/震惊眩晕 | 觉醒/噩耗/揭示 |
| F2 | 速度线 | `speed lines radiating {behind subject}, motion energy` | 爆发冲劲/动态 | 觉醒/攀跃/出手 |
| F3 | 破框出血 | `[元素] bursts through the panel border, breaking the frame` | 力量越界/挣脱 | 力量爆发/呐喊 |
| F4 | 光效 | `{color} energy bloom, luminous shockwave, glowing particles` | 能量爆发/神圣 | 觉醒/神迹/大招 |
| F5 | 环境光雾 | `{light} filtering through {fog/dust/snow}, volumetric light` | 氛围/神秘/压迫 | 秘境/永夜/雾境 |
| F6 | 环境光晕 | `{warm/cold} ambient glow, halo light` | 温暖/神圣/梦幻 | 温情/希望/守护 |
| F7 | 飘雪/粒子 | `falling snow particles, slow drifting` | 时空感/寂寥/纯净 | 永夜/离别/回忆 |
| F8 | 视差压缩 | `extreme perspective compression, foreground blurred deep receding` | 纵深/冲击/压迫 | 隧道/追逃/深渊 |
| F9 | 双重曝光 | `double exposure, {subject} merged with {symbol}` | 身份/记忆/宿命 | 觉醒/回忆/幻象 |

> **特效密度**：每页 ≤2 格带特效、特效格 ≤2 种。F 码如非必要可省略（写 `-`）。

### 3.4 情绪→镜语强制映射表

> 想让这格传达某情绪，就从这里查推荐 L/C/F 组合，**禁止凭感觉自由发挥**。

| 情绪 | 推荐组合 | 说明 |
|:-----|:---------|:-----|
| 臣服/敬畏 | `L3 C4 F6` | 仰视+压迫+光晕 |
| 渺小/绝望 | `L1 C5 F5` | 极远景+俯角+雾 |
| 孤独/寂寥 | `L1 C6 F7` | 极远景+留白+飘雪 |
| 震惊/顿悟 | `L7 C9 F1` | 大特写+倾斜+集中线 |
| 恐惧/威压 | `L8 C4 F3` | 特写仰视+压迫+破框 |
| 决绝/觉醒 | `L7 C2 F2/F4` | 大特写+对角线+速度/光效 |
| 对峙/威胁 | `L10 C7 F8` | 过肩+前景遮挡+视差 |
| 温情/守护 | `L5 C3 F6` | 近景+框架式+光晕 |
| 悲伤/压抑 | `L6 C5 F5` | 特写+俯角+雾 |
| 宿命/翻涌 | `L7 C9 F9` | 大特写+倾斜+双重曝光 |
| 神秘/阴谋 | `L11 C7 F5` | 剪影+前景遮挡+雾 |
| 庄严/秩序 | `L3 C8 F4` | 全景仰视+对称+光效 |

---

## 四、多角色三重锁定（同页≥2角色）

**公式**：每个角色锁定 3 个独立维度（发型/发色 + 眼瞳色 + 服装主色）。

```
IMPORTANT: {N} distinct characters with triple-locked features.
The {角色A} has {发型A}+{眼色A}+{服装色A}.
The {角色B} has {发型B}+{眼色B}+{服装色B}.
Do NOT give {角色B} {角色A的特征}. Do NOT change any character's hair color or robe color between panels.
```

> 有血缘关系的角色可共享部分特征（如父子共享金眼），形成叙事编码。同角色跨格一致性：`All {N} panels show the SAME character. Same {发型}, same {眼色}, same facial features, same {服装}. ONLY the expression, posture, and lighting change.`

---

## 五、台词气泡（HTML 层，但导演卡必须规划）

> 解决"丢失的对话文案"痛点。Seedream 不画文字，文字全部交给 HTML 后处理，但**说话者/情绪/位置必须在导演卡提前定死**。

**台词气泡设计表**（写入导演卡）：

| 台词 | 说话者 | 情绪 | 所在页/格 | 气泡位置提示 |
|:-----|:-------|:-----|:---------|:------------|

**控制音量**：每页 ≤4 句气泡，两人对谈连续同页最多3句，之后必须切画面/动作。台词带情绪标签（哀求/决绝/冷笑/崩溃），供 HTML 区分气泡样式。

---

## 六、文字控制（Text Control）—— 禁止伪对话乱字，保留环境装饰字

> **2026-08-03 实测 + 老板确认（见 `workspace/文字控制测试/pe-log-2026-08-03.md`）：Seedream 生成的文字（伪汉字/数字）基本不可用。** 但**环境文字（日记/书本/招牌/符咒）的乱字可作为装饰保留**；真正要防的是**"伪对话场景"的乱字**——对话气泡/对话框里塞乱字，完全不可用且无法修复。
> **核心原则：对话类文字由 HTML 气泡承载，Seedream 只画"开口说话"的画面；环境文字可保留装饰，工具字（旁白/警告）由 HTML 承载。**

### 6.1 为什么文字乱（根因）

**Seedream 在"画面内容本身含文字载体"时，会条件反射生成乱码伪文字。** 负面词能压"画面里不该有文字"，但压不住"内容描述明确要求画文字载体"（日记/书本/UI/招牌）。只要 M3 内容层写了 `handwriting / label / banner / sign / writing / text / 数字`，模型就倾向渲染文字。

**根因定位：对话气泡靠负面词禁，环境文字靠内容层改写（可保留装饰）。**

### 6.2 锁定负面词（每页提示词必带，替换旧的 `No text, no speech bubbles...`）

**对话场景（角色开口/对峙，用 NEG_DIALOGUE）**：
```
No speech bubbles, no dialogue balloons, no thought bubbles, no caption boxes, no dialogue text, no quotes, no sound effect text. The characters speak purely through their expressions and posture, NO text bubbles anywhere. No text, no letters, no numbers, no words, no typography, no labels, no captions, no inscriptions, no writing, no calligraphy, no handwriting, no glyphs, no symbols, no runes, no icons, no logos, no dial numerals, no roman numerals. Pure visual imagery only, no readable characters anywhere.
```

**非对话场景（用 NEG_STRONG）**：
```
No text, no letters, no numbers, no words, no typography, no labels, no captions, no inscriptions, no writing, no calligraphy, no handwriting, no glyphs, no symbols, no runes, no icons, no logos, no dial numerals, no roman numerals. Pure visual imagery only, no readable characters anywhere.
```

> **负面词必须"逐字列举"**（letters/numbers/words/typography 等），比笼统的 `No text` 有效得多。**对话场景必须显式禁 `speech bubbles / dialogue balloons / dialogue text / sound effect text`**，否则可能画气泡塞乱字（R3 实测）。**必须显式禁 `dial numerals` / `roman numerals`**，否则表盘/钟面会生成数字（R1 实测）。

### 6.3 M3 内容层铁律

- **对话场景**：角色"开口说话/对峙"的画面可保留（R3 实测：画面本身不会触发画气泡），**对话内容由 HTML 气泡叠加**。
- **环境文字**（日记/书本/招牌/符咒）：**允许乱字作为装饰**，不做强制无字改写。仅当文字承载必须传达的信息（如日记内容、系统警告）时，将该信息改由 HTML 旁白条承载，画面可不画或画模糊墨迹。
- **禁止在内容层出现** `handwriting / label / banner / sign / writing / text / numbers` 等会**主动触发**文字渲染的词——除非你希望它作为环境装饰乱字出现。
- **绝对禁止**：对话气泡/对话框/拟声字出现在画面（由 HTML 承载）。

### 6.4 文字载体页改写对照表（2026-08-03 实测）

| 改写策略 | 描述写法 | 判定 |
|:---------|:---------|:-----|
| 环境文字保留 | 日记/书本/招牌保留乱字作装饰（老板可接受） | ✅ 达标 |
| 路线A 无字空白 | 需要"干净页面"时：空白泛黄纸页+模糊墨迹+无可读文字 | ✅ 达标 |
| 路线B 去载体 | 完全不出现文字载体，用视觉隐喻（霉斑/血掌印）承载信息 | ✅ 达标 |
| 抽象符号 | 抽象乱码线条/螺旋替代文字 | ❌ 合规被拒，弃用 |
| 对话气泡乱字 | 画面出现气泡且塞乱字 | ❌ 必禁，由 HTML 承载 |

---

## 七、速查

| 我要 | 读什么 |
|:-----|:------|
| 定整页系统 | 本文件 §二 |
| 每格选镜语 | 本文件 §3.1-3.3 L/C/F 库 |
| 按情绪选镜语 | 本文件 §3.4 情绪→镜语映射表 |
| 多角色页 | 本文件 §四 三重锁定 |
| 台词气泡 | 本文件 §五 |
| **禁对话气泡乱字 + 保环境装饰字** | 本文件 §六 文字控制 |
| 画风/排版如何进提示词 | director-card-template → 6段式PE |