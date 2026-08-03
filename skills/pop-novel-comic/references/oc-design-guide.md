# OC 双角度定妆图设计指南

> Step 0 角色定妆图生成的核心参考。定妆图是跨章角色一致性的根基——画错了，后面全错。
> **铁律：定妆图画风必须对齐 M1 画风基准（`art-style-baseline.md` 元尊V1底盘），禁止用独立/老龄风格串。** 定妆照是图生图的参考真相源，选错画风会污染全书画风。见 `guides/pe-test-sop.md` §1.1 + §4.4。

## 为什么是双角度+版本号

| 方案 | 优点 | 缺点 | 结论 |
|:-----|:-----|:-----|:-----|
| 单角度+版本号 | 生成快，成本低 | 侧面/仰俯角度时参考不足，角色易漂移 | 不够用 |
| 三视图（正+侧+背） | 参考最全 | 生成3张成本高，背面在漫画中极少用，浪费 | 过度设计 |
| **双角度+版本号** | 正面定基调+侧面锁轮廓，覆盖95%漫画机位 | 背面仍需文字描述 | **最优解** |

**双角度 = 正面立绘（定面部+服装） + 侧面立绘（锁轮廓+发型）**。两张图共同作为图生图参考，跨章复用。角色外观变化时生成新版本，版本号递增。

## 角色妩造设计方法论

> 小说文字 → 视觉规格的转化不是"翻译"，是"设计"。原文给的是碎片，定妆图要给出完整的人。
>
> **v6.0.0 核心升级**：注入"专业漫画级美感"标准（对应"人物形象很low，像廉价AI"的痛点）。定妆图不是"画得对"，而是"画得漂亮且高级"。判断标准：如果定妆图像"随手AI图"，说明设计没有达到漫画角色标准。

### 韩漫美型公式（专业漫画角色感）

专业网文漫改（元尊/我独自升级/神之塔等）的角色都有一个共性——**为人物的"型"服务，而非人物本身**。要点：

| 维度 | 廉价AI感（杜绝） | 专业漫画感（追求） |
|:-----|:---------------|:-----------------|
| **五官** | 空洞无神、比例怪异 | 骨相清晰，眉眼有戏，情绪藏在五官里 |
| **发型** | 一坨糊、无层次 | 分层明显，发丝走向清晰，有体积感（如碎发簇/长刘海分层） |
| **服装** | 贴图感、无褶皱 | 面料有厚度，褶皱自然，腰带/配饰有型 |
| **面部** | 塑料感、光滑无瑕疵 | 有皮肤质感，可加细微伤疤/绒毛/雀斑增加真实感 |
| **肢体** | 僵硬、动作无目的 | 有体态语言，站姿/手势传达性格 |
| **记忆点** | 无特征、是路人 | 必须有1个"读者0.3秒认出"的视觉记忆点（异色瞳/疤痕/特殊发饰/披风等） |

**韩漫美型公式核心**：人物不是"被画出来的"，是"被设计出来的"。每个角色至少要有：
1. **轮廓可辨识**：剪影（轮廓）能单独区分（不同身高比例/体型/发型外轮廓）
2. **五官有戏**：眼神有情绪，表情是"被守护的宁静"或"压抑的锋芒"，而非无表情
3. **服装有设计感**：不是简单一件衣服，是有层次（内衬+外套+饰品）的完整穿搭

**视觉符号系统**：给每个主角设计一个"代表其命运的视觉符号"（可以藏在服装/纹身/配饰/火焰/光效里），让这个符号在关键页反复出现，形成视觉记忆锚点。例如：
- 主角的标志性特征（龙瞳/剑穗/玉佩/光晕）
- 反派的对立符号（黑雾/铁链/逆十字）
- 世界观的符号系统（星球徽章/宗门纹章）

### 七维度规格表

每个角色必须填写完整的七维度规格表：

| 维度 | 从原文提取什么 | 设计补充什么 | 示例 |
|:-----|:-------------|:-----------|:-----|
| **年龄/性别/体型** | 直接提取 | 推断具体身高体型比例 | 18岁男性，瘦削178cm |
| **发型/发色** | 原文描述 | 补充长度、造型方式、发质 | 亚麻色短发微乱，前额碎发遮眉 |
| **瞳色/眼型** | 原文描述 | 补充眼型（凤眼/杏眼/三角眼） | 黑色凤眼，眼尾微挑 |
| **面部特征** | 疤痕/胎记等 | 补充脸型、鼻型、唇型、眉型 | 瓜子脸，高鼻薄唇，剑眉 |
| **服装** | 原文描述 | 补充材质、层次、配饰、鞋靴 | 破旧亚麻衬衫，赤脚，腰间麻绳 |
| **标志性特征** | 特殊道具/印记 | 设计视觉记忆点（读者0.3秒认出的特征） | 苍白面色，锁骨突出的瘦弱感 |
| **视觉锚点串** | 以上汇总 | 翻译为英文锚点标签 | `short messy sandy hair, black phoenix eyes, pale skin, thin build, worn linen shirt, barefoot, prominent collarbone` |

### 妩造设计原则

1. **一个记忆点**：每个角色必须有1个"读者一眼记住"的视觉特征（异色瞳/疤痕/特殊发饰/独特服装剪裁）。没有记忆点的角色是路人。
2. **服装分层**：外套→内衬→腰带→裤/裙→靴鞋，每层都写。漫画角色经常有换装/受伤/半裸场面，分层描述让增量版本有据可依。
3. **色彩锚定**：主色≤3色（如"黑发+黑瞳+灰衣"），辅助色≤2色。色彩太多角色不统一，太少则平庸。
4. **年龄感匹配**：少年角色不能画成大叔，老年角色不能太光滑。在提示词中明确 `young teenage face` 或 `weathered aged face`。

### 知名角色二创融合

对知名网文角色（起点万订/有官方漫画/有大量二创），生成定妆图前先搜索二创参考：

```
WebSearch: "{小说名} {角色名} 漫画 插画 二创"
```

提取视觉共识特征（多来源一致 = 读者共同记忆），回填到规格表。二创共识与原文冲突时以原文为准，但标注差异供门禁0决策。

> 冷门/原创小说跳过此步骤。

## 双角度定妆图提示词模板

> **v6.0.0 提示词升级**：加入"韩漫美型公式"落地关键词——`handsome_character_design`, `high quality professional illustration`, `detailed sophisticated design`，并在负面约束中彻底封死廉价感（`generic cheap quality`, `amateurish`, `low resolution`）。同时固定视觉符号锚点，让符号串进提示词。

### 定妆图质量基准（美型公式入口）

组装提示词前，先为这个角色定**美型档位**：

| 档位 | 适用范围 | 追加关键词 |
|:-----|:---------|:----------|
| **男神/女神档** | 主角/重要配角 | `attractive face, sharp jawline, defined bone structure, elaborate detailed costume` |
| **型格档** | 反派/配角 | `imposing presence, sharp piercing eyes, intricate armor/costume details` |
| **写实档** | 老人/路人 | `weathered aged face, realistic skin texture, wrinkles` |

> 每角色至少1个视觉符号锚点，写入提示词的「标志性特征」段位。

### 正面立绘提示词

> **画风底盘必填**：第一行填入 `art-style-baseline.md` §三-b 的定妆照画风串（元尊V1 + 题材配色）。禁止用独立/老龄风格串（如 Solo Leveling 厚涂串）。

```
[元尊V1画风串 + 题材配色，见 art-style-baseline.md §三-b].

CHARACTER DESIGN SHEET, FRONT VIEW:
A {年龄} {性别} with {体型}. {发型发色}, {瞳色眼型}, {脸型} face with {面部特征}. Wearing {服装分层描述}. {标志性特征}. {表情}.

COMPOSITION: Full body character design sheet, front view, character centered occupying 75% of frame, simple light gray background.

LIGHTING: Soft frontal lighting with subtle rim light on hair edges.

RENDERING: Professional illustration, high detail hair with volume and layers, realistic fabric texture with natural folds, clear facial features, visible skin pores, attractive face with expressive eyes.

{风格保真约束}.
Exactly one character. No duplicated limbs. Exactly five fingers per hand. No chibi proportions. No text.
```

### 侧面立绘提示词

> **画风底盘必填**：第一行同样填入元尊V1画风串 + 题材配色，与正面一致，保证双角度画风统一。

```
[元尊V1画风串 + 题材配色，见 art-style-baseline.md §三-b].

CHARACTER DESIGN SHEET, SIDE PROFILE VIEW:
The SAME character as reference image. {发型侧面轮廓描述}, {鼻型侧面轮廓}, {下颌线}, {服装侧面剪影}. {标志性特征侧面可见}. {表情}.

COMPOSITION: Full body character design sheet, exact side profile view (90 degrees), character centered occupying 75% of frame, simple light gray background.

LIGHTING: Soft frontal lighting with subtle rim light on hair edges.

RENDERING: Professional illustration, high detail hair with volume and layers, realistic fabric texture with natural folds, clear silhouette profile, sharp jawline, expressive eye visible in profile.

{风格保真约束}.
Exactly one character. No duplicated limbs. Exactly five fingers per hand. No chibi proportions. No text.
```

### 关键差异点

| 维度 | 正面立绘 | 侧面立绘 |
|:-----|:---------|:---------|
| 视角 | 正面全身 | 90度侧面全身 |
| 核心锁定 | 面部五官+服装正面 | 发型轮廓+鼻型+下颌线+服装剪影 |
| 用途 | 面部一致性参考 | 轮廓一致性参考（侧面/半侧面机位） |

> **侧面立绘必须传正面立绘作为参考图（图生图）**，确保两张图是同一个人。

### 生成命令

```powershell
$env:ARK_API_KEY="{API_KEY}"

# 正面立绘
python "{pop-novel-visual路径}/scripts/generate.py" image `
  --prompt '{正面提示词}' `
  --model doubao-seedream-5-0-pro-260628 `
  --size 1728x2304 `
  --output "{漫画项目}/assets/characters/char-{角色名}-v{N}-front.png"

# 侧面立绘（传正面立绘作参考）
python "{pop-novel-visual路径}/scripts/generate.py" image `
  --prompt '{侧面提示词}' `
  --model doubao-seedream-5-0-pro-260628 `
  --size 1728x2304 `
  --image "data:image/png;base64,{正面立绘base64}" `
  --output "{漫画项目}/assets/characters/char-{角色名}-v{N}-side.png"
```

## 版本管理

### 版本命名规则

```
char-{角色名}-v{版本号}-front.png   # 正面立绘
char-{角色名}-v{版本号}-side.png    # 侧面立绘
```

### 增量定妆图触发条件

| 变化类型 | 是否增量 | 版本操作 |
|:---------|:--------:|:---------|
| 换装 | ✅ | v{N+1}，基于v{N}+换装描述 |
| 受伤疤痕 | ✅ | v{N+1}，基于v{N}+伤痕描述 |
| 变身/觉醒 | ✅ | v{N+1}，基于v{N}+变身描述 |
| 年龄跳变 | ✅ | v{N+1}，重新设计 |
| 脏污/淋湿 | ❌ | 提示词中描述，不出增量 |
| 表情变化 | ❌ | 提示词中描述 |

### 增量提示词组装

```
[原版本冻结提示词] + [变化描述]

示例（v1→v2 换装）：
原提示词: ...wearing worn linen shirt, barefoot...
变化描述: Now wearing black leather armor over dark gray tunic, steel-toed boots, iron bracers
新提示词: ...wearing black leather armor over dark gray tunic, steel-toed boots, iron bracers...
```

> 新版本的提示词同样冻结到角色库。后续章节使用新版本。

## 与角色一致性管理的集成

> **必读 `references/guides/char-consistency-guide.md`** 了解四层角色结构和冻结提示词机制。

### 四层结构更新

| 层 | 双角度方案下的内容 |
|:---|:-----------------|
| 层1 规格表 | 七维度规格表（人读） |
| 层2 冻结提示词 | 正面+侧面两份提示词原文（API读，真相源） |
| 层3 定妆图资产 | `char-{名}-v{N}-front.png` + `char-{名}-v{N}-side.png` |
| 层4 决策日志 | append-only，记录每次版本变化的决策原因 |

### 漫画页生成时的参考图选择

| 机位 | 参考图 | 说明 |
|:-----|:-------|:-----|
| 正面/微侧（±30°） | front.png | 面部一致性 |
| 侧面/半侧面（30°-90°） | side.png | 轮廓一致性 |
| 仰视/俯视 | front.png + 文字补充 | 以正面为基准 |
| 背面 | front.png + 文字描述 | 背面极少用，文字描述发型/服装背面 |

> `generate_comic_page.py` 的 `ref_images` 参数支持多张参考图。多角色页选主要角色的参考图。
