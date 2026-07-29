# Step 2: 生成画面 + HTML 组装

> 角色定妆图 → 逐格分镜生成 → HTML 漫画页组装

## 设计哲学

Step 2 执行三件事：**定妆**（锁定角色外观）→ **画格**（逐帧生成分镜画面）→ **排版**（HTML 组装漫画页）。

角色定妆图是跨格一致性的关键——先画一张角色立绘，后续所有分镜都参考这张图，模型就能保持发色/服装/体型的统一。

对白气泡用 HTML/CSS 叠加，不让 Seedream 渲染文字——模型文字渲染不可控，CSS 定位精确且可迭代。

## 1. 角色定妆图

为主角生成 1-2 张角色立绘（纯文生图）。

### 提示词写法

```
一个[年龄]的[体型特征]角色，[发色/发型]，[面部特征]，穿[服装描述]，[标志性特征]。[表情]。[风格锚定串]，全身立绘，纯色背景。
```

### 调用方式

```powershell
$env:ARK_API_KEY="{API_KEY}"
python "{pop-novel-visual路径}/scripts/generate.py" image `
  --prompt '{角色定妆提示词}' `
  --model doubao-seedream-5-0-lite-260128 `
  --size 1728x2304 `
  --output "{输出目录}/output/char-{角色名}.png"
```

> 重要参数：`--size 1728x2304`（API 最小像素要求 3686400，不能用更小尺寸）

### 多角色处理

- 主角必出定妆图
- 出场≥3帧的配角建议出定妆图
- 只出场 1-2 帧的配角不需要，在分镜提示词中描述即可

## 2. 逐格分镜生成

读取 Step 1 的分镜脚本，逐格调用 API 生成画面。

### 单格生成方式

每格传入角色定妆图作为参考（图生图模式）：

```powershell
python "{pop-novel-visual路径}/scripts/generate.py" image `
  --prompt '{分镜提示词}' `
  --model doubao-seedream-5-0-lite-260128 `
  --size 1728x2304 `
  --image "data:image/png;base64,{角色定妆图base64}" `
  --output "{输出目录}/output/frame{N}.png"
```

### 批量生成方式（推荐）

使用本 skill 的批量生成脚本，一次生成全部 8 帧：

```powershell
$env:ARK_API_KEY="{API_KEY}"
python "{本skill路径}/scripts/generate_storyboard.py"
```

> 批量脚本需配置 `FRAMES` 列表（每帧的 id + prompt）和 `CHAR_IMG`（角色定妆图路径）。详见脚本注释。

### 提示词检查清单

每格提示词必须包含：
- [ ] `参考图中的人物形象`（首句，如该帧有角色出场）
- [ ] 角色动作描述（谁在做什么）
- [ ] 场景环境描述（什么地方、什么氛围）
- [ ] 风格锚定串（末尾追加，全章统一）
- [ ] ≤300 字（Seedream 中文提示词上限）

### 无角色帧处理

纯环境/特写帧（如"一只手触碰头发"）不需要参考图，直接文生图即可。

## 3. HTML 漫画页组装

将生成的分镜画面用 HTML/CSS 组装成完整漫画页面。

### 使用模板

读取 `templates/comic-page.tpl.html`，替换以下占位符：

| 占位符 | 替换为 |
|:-------|:-------|
| `{{TITLE}}` | 书名 |
| `{{SUBTITLE}}` | 章节名 |
| `{{FRAME_N_IMG}}` | 第 N 帧图片路径 |
| `{{FRAME_N_BUBBLE}}` | 第 N 帧对白气泡内容（可为空） |
| `{{FRAME_N_NARRATION}}` | 第 N 帧旁白内容（可为空） |
| `{{FRAME_N_SFX}}` | 第 N 帧拟声词（可为空） |

### 布局原则

- **Grid 布局**：2 列，全宽格和半宽格交替
- **节奏**：大格（全景/建立场景）→ 小格（细节/情绪）→ 大格（高潮）→ 小格 → 大格（结尾）
- **边框**：每格 3px 黑色边框，格间距 8px
- **气泡位置**：根据画面构图手动指定，避开角色面部和动作焦点
- **旁白框**：右上角或左上角，小尺寸，半透明背景

### 气泡 CSS 类

| 类型 | CSS 类 | 用途 |
|:-----|:-------|:-----|
| 对话气泡 | `.bubble` + `.pN-bubble` | 角色台词，白底黑字圆角 |
| 旁白框 | `.narration` + `.pN-narration` | 旁白/内心独白，米色底 |
| 拟声词 | `.sfx` + `.pN-sfx` | 拟声词，大字斜体描边 |

### 输出

```powershell
# 保存到输出目录
{输出目录}/漫画-{章节名}.html
```

## 4. HTML 图片内联化（必须执行）

popwave webview 安全策略禁止加载外部资源（相对路径、绝对路径、file:// 均被阻止），HTML 中的 `<img src="output/frame1.png">` 在 popwave 中会显示为图片损坏。

**必须**在上一步组装完 HTML 后，运行内联化脚本，将所有图片压缩为 base64 data URI 嵌入 HTML：

```powershell
python "{本skill路径}/scripts/inline_html.py" "{输出目录}/漫画-{章节名}.html"
```

脚本参数（可选）：
- `--width 800`：图片最大宽度像素（默认800，漫画页max-width=900px时够用）
- `--quality 65`：JPEG 质量（默认65，体积与画质平衡点）

```powershell
# 自定义压缩参数
python "{本skill路径}/scripts/inline_html.py" "{输出目录}/漫画-{章节名}.html" --width 600 --quality 50
```

执行后 HTML 文件被覆盖为自包含版本（图片内联为 base64），原图片文件保留在 `output/` 不受影响。

> 内联化后的 HTML 在浏览器和 popwave 中均能正常显示。未内联化的 HTML 仅在浏览器中可用。

### 预览

```powershell
cd {输出目录}
python -m http.server 8765
# 浏览器打开 http://localhost:8765/漫画-{章节名}.html
```

## 4. 质量检查

生成完成后检查：

| 检查项 | 方法 | 达标标准 |
|:-------|:-----|:---------|
| 单格画面质量 | 逐张目测 | 画面清晰、角色无畸形 |
| 角色一致性 | 8格对比主角外貌 | 发色/服装/体型一致率≥70% |
| 风格统一 | 8格色调/笔触对比 | 无明显割裂 |
| 叙事连贯 | 按顺序看8格 | 不看文字也能理解剧情 |
| 气泡不遮挡 | HTML页面目测 | 气泡不挡角色面部/动作焦点 |
| 图片格式 | 检查 output/*.png 文件头 | magic bytes 为 `89 50 4E 47`（真PNG），非 `FF D8 FF`（JPEG伪装）。脚本已内置自动转码 |
| HTML 自包含 | 检查 HTML 中 img src | 全部为 `data:image/jpeg;base64,...`，无 `output/` 路径引用 |

## 5. 降级处理

| 问题 | 降级方案 |
|:-----|:---------|
| 角色定妆图质量差 | 换 5.0 Pro 模型重生成 |
| 分镜画面角色漂移严重 | 重新生成该帧，或加强提示词中的角色描述 |
| HTML 气泡位置不好 | 手动调整 CSS 定位参数 |
| API 调用失败 | 检查 API Key 和网络，重试该帧 |
