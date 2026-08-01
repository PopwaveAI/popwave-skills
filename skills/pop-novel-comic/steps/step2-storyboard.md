# Step 2: 分镜生成

> 读导演卡 → 拆分镜(弹性格数) → 门禁确认 → 增量定妆图(如有) → 逐格生成 → 漫画HTML排版(Pillow备选)

## 设计哲学

选帧 step 的唯一任务是"怎么画"——基于导演卡的改编策略，将策略表中的每条信息转化为具体的分镜帧。

**导演卡是选帧的唯一输入源。** 不重新做改编分析，直接读导演卡的策略表和转化方案拆分镜。直接选帧的信息 → 正常分镜帧；视觉转化的信息 → 转化帧；旁白浓缩的信息 → 旁白+象征画面帧。

**角色一致性靠引用冻结提示词保证**，不靠重新组装。每帧的角色描述部分直接从角色库复制冻结提示词，加上场景动作描述和风格锚定串即可。

**角色是活的，定妆图也要跟着活。** 导演卡中标注的角色变化计划在本 step 执行——生成增量定妆图后，分镜表才能标注正确的定妆图版本。

**格数不锁死。** 一章内容有多少值得画的场面，就拆多少格。Agent 根据章节内容密度自主判断，不被固定数字束缚。

## 1. 读取导演卡

读取 Step 1 产出的 `第{N}章/导演卡.md`，获取：

| 导演卡内容 | 用途 |
|:-----------|:-----|
| 章节概要 | 把握整体情绪走向 |
| 角色变化记录 | 规划增量定妆图（§2） |
| 改编策略表 | 拆分镜的输入源——每条策略对应一个或多个分镜帧 |
| 转化帧设计 | 视觉转化帧的画面提示词基础 |
| 旁白文案 | 旁白浓缩帧的已拟文字 |
| **页面设计表** | **页面分割依据**——每页的功能位、视觉重心、格数预算、页内钩子（拼图时用 separator 还原页面边界） |
| **分格设计表** | **拆分镜的直接输入**——每格的布局类、节奏、叙事功能、信息来源、画面方向、效果类已确定，Step 2 只需补充画面提示词、定妆图版本、场景主镜等执行细节 |

> 如果导演卡不存在（跳过了 Step 1），**必须回退执行 Step 1**，不得直接从原文拆分镜。

> **v2.10.0 变更**：布局类、节奏、效果类已在 Step 1 分格设计表中确定。Step 2 **继承**这些设计决策，不重新决定布局。Step 2 的工作是"执行"——补充画面提示词、定妆图版本、场景主镜，然后生成画面并用 HTML 排版（Pillow 备选）。

## 2. 增量定妆图生成（如有变化）

执行导演卡中角色变化记录表标注的增量定妆图计划：

1. 基于角色的当前版本冻结提示词 + 变化描述，组装新提示词
2. 调用 `scripts/update_char_asset.py` 生成新版本定妆图
3. 新定妆图保存到 `assets/characters/char-{名}-v{N+1}.png`
4. **新提示词冻结到角色库**（作为 v{N+1} 的冻结提示词）
5. 记录到角色库的增量定妆表和决策日志

```powershell
python "{本skill路径}/scripts/update_char_asset.py" `
  --char-name "{角色名}" `
  --version {N+1} `
  --base-prompt "{当前版本冻结提示词}" `
  --change-desc "{变化描述}" `
  --output "{漫画项目}/assets/characters/char-{名}-v{N+1}.png"
```

> 无变化的章节跳过此步骤。

## 3. 拆分镜脚本

基于导演卡的**分格设计表**拆出分镜序列。**参考 `references/storyboard-guide.md`** 了解选帧方法论、转化方案库和叙事驱动布局。**参考 `references/layout-pool.md`** 了解7种HTML排版布局的CSS实现、适用场景和避让规则。

> **v2.10.0 变更**：分格设计表已在 Step 1 确定了每格的布局类、节奏、叙事功能、信息来源、画面方向和效果类。Step 2 在此基础上**补充执行细节**（画面提示词、定妆图版本、场景主镜、对白文字），形成完整的分镜脚本表。不重新决定布局类和节奏。

### 格数由导演卡决定

格数和布局已在 Step 1 导演卡的分格设计表中确定。Step 2 校验格数合理性：

- **内容密集章**（多场战斗/多线交织/大量信息揭示）：10-15格
- **标准章节**（有起承转合，3-5个情绪转折）：6-8格
- **过渡章**（日常/铺垫为主，情绪平稳）：4-6格
- **高潮章**（大事件密集爆发）：可到15-20格，分多页呈现

> 如果导演卡的分格设计表格数与上述范围严重偏离，回 Step 1 重新评估。正常情况下直接按分格设计表执行。

### 分镜脚本表格式

> **v2.10.0**：分镜脚本表 = 分格设计表（Step 1 产出） + 执行细节（Step 2 补充）。布局类、节奏、效果类从分格设计表**继承**，场景组、定妆图版本、场景主镜、对白文字、画面提示词由 Step 2 **补充**。

每帧必须标注出场角色、定妆图版本、场景组、布局类和节奏：

| 帧号 | 所属页 | 场景组 | 场景 | 角色动作 | 机位 | 情绪 | 节奏 | 布局类 | 效果类 | 出场角色 | 定妆图版本 | 场景主镜 | 对白/文字 | 画面提示词 |
|:-----|:-------|:-------|:-----|:---------|:-----|:-----|:-----|:-------|:-------|:---------|:-----------|:---------|:---------|:-----------|
| 1 | P1 | A | 破屋，雨夜 | 薇薇安从米袋抓米 | 全景 | 压抑 | 慢 | panel-full | — | 薇薇安 | char-vivian-v1 | — | 旁白:没有食物了 | [提示词] |
| 2 | P1 | A | 破屋灶台 | 薇薇安抱老狗 | 中近景 | 温暖 | 慢 | panel-half | — | 薇薇安 | char-vivian-v1 | frame1 | 对白:又不会偷东西 | [提示词] |
| 3 | P1 | A | 门外 | 脚步声逼近 | 特写 | 恐惧 | 快 | panel-half | — | 无 | — | frame1 | 旁白:脚步声 | [提示词] |
| 5 | P2 | B | 集市 | 薇薇安穿新衣出行 | 中景 | 明亮 | 慢 | panel-full | — | 薇薇安 | char-vivian-v2 | — | 旁白:第一次穿上干净的衣裳 | [提示词] |
| 8 | P3 | C | 门口 | 索伦睁眼 | 特写 | 震惊 | 慢 | panel-hook | — | 索伦 | char-soren-v2 | — | — | [提示词] |

> 注意帧8使用 panel-hook（章末钩子）。**场景组**标识同一场景的连续帧——同组第2格起需用首格作为场景主镜参考图（见 storyboard-guide §场景主镜机制）。布局类和节奏标注参见 `references/storyboard-guide.md` 的「分镜节奏方法论」和「页面布局系统」章节。

### 直接选帧与转化帧混合排列

分镜表中直接选帧（来自策略"直接选帧"）和视觉转化帧（来自策略"视觉转化"）**混合排列**，按叙事时序组织。转化帧的"画面提示词"列直接使用导演卡中的转化方案设计。

### 提示词组装规则

> **v2.9.2 重构**：画风从末尾移到开头（Seedream 对提示词开头权重最高），场景描述精简，末尾加风格保真约束。解决分镜帧画风漂移到"电影概念艺术"的问题。

每格提示词结构：

```
[Seedream 执行串(画风,含参考作品)]。参考图中的人物形象，[视觉锚点串]。[微表情串（如有情绪）]。[角色动作描述]。[场景环境描述(精简≤2句)]。[情绪氛围]。[风格保真约束]。
```

**关键规则**：
- **首句必须是 Seedream 执行串**——从漫画角色库的「Seedream 执行串」字段复制，放在提示词最前面（高权重位）
- **末尾必须有风格保真约束**——从漫画角色库的「风格保真约束」字段复制，防止画风漂移
- **场景描述精简到≤2句**——过长的场景描述会把 Seedream 推向"电影概念艺术"模式
- 角色描述部分**从角色库的冻结提示词直接复制**，不重新组装
- **视觉锚点串**从角色库的锚点提示词串字段复制（见 storyboard-guide §角色一致性工艺包）
- **微表情**：有强情绪的帧，用 storyboard-guide §微表情技法中的映射表替换情绪词
- **场景主镜**：同场景第2格起，提示词中追加环境锁定描述（见 storyboard-guide §场景主镜机制）
- 只追加场景和动作描述

如果本章有增量定妆图（导演卡中标注的变化），变化后的帧使用新版本的冻结提示词。

### 关键帧高精度模板（可选）

**高潮帧、变身帧、名场面**等需要最高质量的帧，可使用高精度模板（见 `../pop-novel-visual/references/seedream-prompt-guide.md` §1.10）。将基础提示词结构升级为 4 块结构（LOCKED COMPOSITION / ENVIRONMENT AND LIGHTING / HARD CONSTRAINTS），加入镜头规格和硬约束。

判断标准：
- 这帧是否值得读者停留 3 秒以上看细节？→ 是 → 用高精度模板
- 这帧是否有复杂动作/特效/多角色交互？→ 是 → 用高精度模板
- 普通对话帧/过渡帧 → 用基础提示词，速度优先

示例（索伦觉醒后帧）：
```
# 开头的 Seedream 执行串（从角色库复制）：
Semi-thick painting manga style, clean hard outer contour lines as skeleton with soft gradient shading inside color blocks, cel-shaded base with painterly soft-light overlays, 7.5-head semi-realistic proportions, modern refined illustration. Art style similar to Da Feng Da Geng Ren manga adaptation.
# 从角色库复制的 v2 冻结提示词角色描述（觉醒后）：
参考图中的人物形象，一个18岁的瘦削男性角色，亚麻色短发微乱，金色眼眸（觉醒后），穿破旧亚麻衬衫，苍白面色，背部隐约可见金色纹路。
# 追加的场景和动作（精简≤2句）：
年轻男子站在废墟中，金色眼眸首次绽放光芒，周围碎石悬浮。觉醒的震撼氛围。
# 末尾的风格保真约束（从角色库复制）：
Maintain visible outer contour lines. Use soft gradient shading inside color blocks, not full painterly blending. Keep manga readability. No lineless style. No cinematic concept art. No photorealistic 3D rendering.
```

> 无角色帧（纯环境/特写）不需要参考图和角色描述，但仍然需要 [Seedream 执行串] 开头 + [风格保真约束] 结尾。

## 4. 🚪 门禁：分镜+角色变化确认

向用户呈现：

1. **角色变化记录表**（如有变化）—— 列出本章识别到的所有角色外观变化和增量定妆图计划
2. **分镜脚本表**（含每帧的出场角色+定妆图版本+格数）—— 直接选帧和视觉转化帧混合排列

用户确认后继续。如用户认为格数过多/过少或变化识别有误，调整后再次门禁。

> 改编策略已在 Step 1 导演卡门禁确认，本门禁只确认"帧选得对不对"。

## 5. 逐格分镜生成

### 高并发批量生成（推荐）

> **v3.1.0 升级**：`generate_storyboard.py` 升级为 ThreadPoolExecutor 高并发生成（默认8线程），16帧从6分钟降至~20秒。Seedream API 限制500图/分钟（8.3图/秒），8线程安全。内置自动重试（3次指数退避）和格式保真（JPEG→PNG转码）。

配置 `generate_storyboard.py` 的 `FRAMES` 列表和 `FRAME_REFS`（按帧映射参考图，支持场景主镜）：

```python
# 按帧映射参考图：[角色定妆图, 场景主镜图]
# 场景主镜 = 同场景首帧的输出图，锁定空间/光源/材质
FRAME_REFS = {
    "frame1": ["char-vivian-v1.png", None],           # 场景A首格，无主镜
    "frame2": ["char-vivian-v1.png", "frame1.png"],    # 场景A第2格，用frame1做主镜
    "frame3": [None, "frame1.png"],                    # 场景A无角色帧，只需主镜
    "frame4": ["char-vivian-v2.png", None],            # 场景B首格，无主镜（换装后）
    "frame5": ["char-vivian-v2.png", "frame4.png"],    # 场景B第2格，用frame4做主镜
    "frame6": None,                                     # 无角色无场景帧（纯抽象/转场）
    "frame7": ["char-soren-v1.png", None],             # 场景C首格
    "frame8": ["char-soren-v2.png", None],             # 场景D首格（新场景）
    # ... 格数不限于8，按实际分镜数量配置
}
```

```powershell
$env:ARK_API_KEY="{API_KEY}"
python "{本skill路径}/scripts/generate_storyboard.py"
```

### 单格生成

```powershell
python "{pop-novel-visual路径}/scripts/generate.py" image `
  --prompt '{分镜提示词}' `
  --model doubao-seedream-5-0-pro-260628 `
  --size 1728x2304 `
  --image "data:image/png;base64,{角色定妆图base64}" `
  --output "第{N}章/output/frame{N}.png"
```

## 6. 漫画 HTML 排版

将分镜帧编排为 HTML 漫画页面，嵌入原文旁白，通过本地 HTTP 服务器预览。HTML 排版是 v3.0.0 起的主要产出格式，支持 7 种排版布局、渐变遮罩旁白、外部图片引用。

> **v3.0.0 变更**：从纯 Pillow 拼图回归 HTML 排版作为主要产出格式。解决 v2.11.0 Pillow 方案布局表达能力不足的问题——HTML 支持 7 种排版布局（含侧边文字面板、叠加嵌套、全幅出血等 Pillow 无法实现的布局），原文旁白直接嵌入 HTML 渐变遮罩。图片使用外部路径引用（非 base64 内联），通过本地 HTTP 服务器预览，HTML 文件轻量可编辑。Pillow 拼图保留为 §7 备选方案。

> **必读 `references/layout-pool.md`**：7 种布局的 CSS 实现要点、适用场景、叙事功能、避让规则、原文旁白嵌入规范、画风适配规则。

### 编写排版配置 JSON

在 `{漫画项目}/第{N}章/` 下创建 `拼图配置.json`（同时驱动 HTML 排版和 Pillow 备选），按分镜脚本表的帧顺序描述每帧的布局、旁白和样式：

```json
{
  "title": "诡秘之主",
  "subtitle": "第一章 · 绯红",
  "frames_dir": "{漫画项目}/第{N}章/output",
  "output_html": "{漫画项目}/第{N}章/index.html",
  "output_jpeg": "{漫画项目}/第{N}章/漫画-{章节名}.jpg",
  "footer": "popwave",
  "frames": [
    {"file": "frame1.png", "layout": "splash",   "caption": "没有食物了。"},
    {"separator": "line"},
    {"file": "frame2.png", "layout": "fullwide", "caption": "薇薇安从米袋里抓出最后一把米。"},
    {"file": "frame3.png", "layout": "split",    "caption_left": "破屋内", "caption_right": "门外脚步声逼近", "file_right": "frame4.png"},
    {"separator": "line"},
    {"file": "frame5.png", "layout": "narrow",   "narration": "这个世界将来会迎来诸神的黄昏。诸神的黄昏，意味着一切的终结。"},
    {"file": "frame6.png", "layout": "fullbleed", "caption": "剑气冲霄，百丈山峰被无形力量切出一道裂痕。"},
    {"file": "frame8.png", "layout": "climax",   "caption": "脚步声，越来越近……"}
  ]
}
```

### 布局类映射表（7 种 HTML 布局）

`layout` 值对应分镜脚本表中的「布局类」（由 Step 1 分格设计表确定，**继承不重新选择**）：

| 分格设计表布局类 | HTML layout 值 | 画幅 | 叙事功能 | Pillow 备选 layout |
|:----------------|:--------------|:-----|:---------|:-------------------|
| panel-splash | splash | 3:4 竖幅 | 章节开场/场景建立 | scene |
| panel-split | split | 双格 50/50 | 对比/并进/反应 | half×2 |
| panel-fullwide | fullwide | 4:3 横幅 | 情感舒缓/环境交代 | full |
| panel-overlay | overlay | 主图+inset 35% | 戏剧转折/因果对照 | — (回退 fullwide) |
| panel-narrow | narrow | flex 30/70 | 旁白密集/静态段落 | — (回退 fullwide) |
| panel-fullbleed | fullbleed | 16:9 出血 | 战斗/冲击/沉浸 | impact |
| panel-climax | climax | 3:4 竖幅 85vh | 情感高潮/章末收尾 | hook |

> 详细 CSS 实现要点、适用场景、避让规则见 `references/layout-pool.md`。Pillow 备选方案不支持 overlay 和 narrow 布局，遇到这两种布局且必须用 Pillow 时回退为 fullwide。

### 原文旁白嵌入

旁白文字直接嵌入 HTML 排版的渐变遮罩中，不二次改写：

- **底部遮罩旁白**（splash/fullwide/fullbleed/climax/overlay）：使用 `caption` 字段，单帧不超过 3 行（约 80 字）
- **侧边文字面板**（narrow）：使用 `narration` 字段，可达 150-200 字
- **分格旁白**（split）：使用 `caption_left` / `caption_right` 字段，每格不超过 2 行（约 50 字）

> 旁白渐变遮罩规范、文字样式规范、内容规范详见 `references/layout-pool.md` 原文旁白嵌入规范章节。

### 排版避让铁律

> 详见 `references/layout-pool.md` 排版避让铁律章节。核心规则：

1. clip-path 斜切线只能穿过画面空白区（墙壁/地面/天空），绝不能穿过人物和文字
2. 使用斜切布局时，生成图片的提示词必须包含"画面左侧/右侧留白"的构图指令
3. 旁白文字不能放在被 clip-path 裁切的区域内
4. 斜切无叙事必要性时不使用，垂直分格（layout-split）是更安全的替代方案

### 生成 HTML 漫画页面

根据排版配置 JSON，生成 `index.html`：

1. 读取 `拼图配置.json` 中的 frames 数组
2. 按 layout 值为每帧套用对应 CSS 布局类（见 `references/layout-pool.md` 各布局 CSS 实现要点）
3. 图片使用外部路径引用：`<img src="output/frameN.png">`（非 base64 内联）
4. 旁白文字嵌入对应布局的 caption-layer / text-panel / narration 元素
5. 在帧之间插入 `<div class="scene-break">◇ ◇ ◇</div>` 对应 separator

### 本地 HTTP 服务器预览

```powershell
# 在章节目录下启动本地 HTTP 服务器
cd "{漫画项目}/第{N}章"
python -m http.server 8000

# 浏览器打开预览
# http://localhost:8000/index.html
```

> 本地 HTTP 服务器解决了图片外部路径引用的加载问题。HTML 文件保持轻量（不含 base64），可随时编辑调整布局和旁白。

### 输出

`{漫画项目}/第{N}章/index.html`（HTML 漫画页面，外部图片引用 + 原文旁白嵌入）。通过本地 HTTP 服务器在浏览器中预览。

### 格数超过8格

排版配置的 `frames` 数组长度不限，超过8格时继续在 `frames` 中追加帧配置即可。建议用 `separator` 分隔页面边界，保持阅读节奏。

## 7. 截长图（分享用）

> **v3.1.0 新增**。HTML 漫画页面排版完成后，使用 Playwright 逐元素截图 + Pillow 拼接输出长图，用于分享。解决浏览器全页截图底部质量退化问题。

```powershell
python "{本skill路径}/scripts/screenshot_comic.py" "{漫画项目}/第{N}章/index.html" "{漫画项目}/第{N}章/长图-{章节名}.png"
```

### 截图原理

1. Playwright headless 浏览器加载 HTML 页面
2. 等待所有图片完全加载（`img.complete && img.naturalWidth > 0`）
3. 自动检测页面元素（`.frame`, `.scene-break`, `.comic-page > div`）
4. 逐元素滚动到视口并截图（避免全页截图的底部模糊）
5. Pillow 拼接所有元素截图为完整长图

### 输出格式

- **PNG**（默认，无损）：适合存档
- **JPEG**（指定 .jpg 扩展名）：适合分享，quality=92

### 注意事项

- 截图前确保本地 HTTP 服务器已启动（或使用 file:// 协议直接加载）
- 视口宽度默认 820px，可通过 `SCREENSHOT_WIDTH` 环境变量调整
- 如未安装 Playwright，执行 `pip install playwright && playwright install chromium`

## 8. Pillow 拼图（备选方案）

当 HTML 排版环境不可用（无浏览器/无本地服务器）时，使用 `scripts/assemble_comic.py` 纯 Pillow 拼图作为备选方案，直接输出 JPEG 长图。

> Pillow 拼图不支持 layout-overlay 和 layout-narrow 布局（需文字面板/嵌套图），遇到这两种布局时回退为 layout-fullwide（full）。

### 执行拼图

```powershell
python "{本skill路径}/scripts/assemble_comic.py" "{漫画项目}/第{N}章/拼图配置.json"
```

### Pillow 布局类映射表

Pillow 模式下 layout 值映射为 Pillow 内部布局类：

| HTML layout 值 | Pillow layout 值 | 说明 | 尺寸 |
|:--------------|:----------------|:-----|:-----|
| splash | scene | 名场面格 2:3 | 852×568 |
| split | half×2 | 半宽格 1:1（自动配对并排） | 424×424 |
| fullwide | full | 全宽格 16:9 | 852×479 |
| overlay | full (回退) | 不支持，回退为全宽格 | 852×479 |
| narrow | full (回退) | 不支持，回退为全宽格 | 852×479 |
| fullbleed | impact | 冲击格 2:1 | 852×426 |
| climax | hook | 章末钩子（暗角+居中文字） | 852×479 |

### Pillow style 字段（可选，默认按 layout 自动推断）

| style | 效果 | 默认对应 layout |
|:------|:-----|:----------------|
| normal | 普通黑边2px | full, half |
| feature | 粗黑边3px + 红色发光 | scene |
| impact | 粗白边3px + 橙色发光 | impact |
| hook | 无边框 + 暗角 | hook |

### Pillow position 字段（可选，默认 center）

控制图片裁剪位置：`center` / `center 30%` / `top` / `bottom`。根据画面内容调整——人物在上方用 `center 20%`，人物在下方用 `center 80%`。

### 输出

`{漫画项目}/第{N}章/漫画-{章节名}.jpg`（900px 宽，JPEG quality 92）。纯 Pillow 实现，无需浏览器。

### 半宽格配对规则

连续两个 `layout: "half"` 的帧自动配对并排。单独 half 帧会警告并当全宽处理。

## 9. 进入 Phase 2

分镜生成完成后，自动进入 Phase 2（读取 `steps/step3-review.md`）执行视觉审核和记忆沉淀。
