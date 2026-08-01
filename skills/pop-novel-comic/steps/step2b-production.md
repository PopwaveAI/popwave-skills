# Step 2b: 页面生成+文字叠加

> 增量定妆图（如有）→ 逐页生成 → HTML 文字叠加 → 截长图 → 进入 Phase 2

## 设计哲学

Step 2b 的唯一任务是"执行"——基于 Step 2a 的页面提示词，生成漫画页图片、叠加文字、截图。**不做创作决策**——所有创作决策（页面设计、提示词、旁白文字）已在 Step 1+2a 完成，Step 2b 只负责按图纸施工。

**v4.0 核心变化**：
- 生成单位从"格"升级为"页"——`generate_comic_page.py` 逐页生成，每页一张含多格的完整漫画图
- HTML 职责简化——不再做格子布局（画面已有分格线），只做文字叠加（旁白条/对白气泡）
- 移动端优先——页面图片全宽展示，文字叠加使用相对定位，竖向滑动阅读

## 1. 增量定妆图生成（如有变化）

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

## 2. 逐页生成

### 配置生成脚本

**从 `storyboard.md` 读取每页的提示词和参考图配置**，写入 `generate_comic_page.py` 的 `PAGES` 列表：

```python
# 页面列表（每页是一张包含多格的完整漫画图）
PAGES = [
    {
        "id": "page1",
        "prompt": "{从storyboard.md P1复制完整页面级提示词}",
        "ref_images": ["char-{角色名}-v{N}.png"],  # 角色定妆图参考
        "size": "1728x2304",  # 竖幅，移动端友好
    },
    {
        "id": "page2",
        "prompt": "{从storyboard.md P2复制完整页面级提示词}",
        "ref_images": ["char-{角色名}-v{N}.png"],
        "size": "1728x2304",
    },
    # ... 更多页
]

# 输出目录
OUTPUT_DIR = r"第{N}章/output"

# 定妆图根目录（项目级，跨章复用）
CHAR_ASSETS_DIR = r"assets/characters"
```

> **提示词从 storyboard.md 复制，不重新组装。** storyboard.md 是提示词的真相源。

### 高并发批量生成

> `generate_comic_page.py` 支持 ThreadPoolExecutor 高并发生成（默认4线程），多页并行生成大幅缩短总耗时。内置自动重试（3次指数退避）和格式保真（JPEG→PNG转码）。

```powershell
$env:ARK_API_KEY="{API_KEY}"
python "{本skill路径}/scripts/generate_comic_page.py"
```

### 生成结果

- 每页输出一张 PNG：`output/page1.png`, `output/page2.png`, ...
- 元数据：`output/generation_meta.json`（记录页数/成功/失败/耗时）
- 格式保真：脚本内置 `ensure_png_bytes()` 检测 JPEG magic bytes 并转码为 PNG

> 如果某页生成失败，脚本会重试3次。全部失败后可单独重跑该页。

## 3. HTML 文字叠加

> **必读 `references/page-layout-guide.md`**：文字叠加 CSS 实现、旁白条/对白气泡规范、移动端适配。

v4.0 的 HTML 职责极度简化——**画面是 AI 画的（含分格线），文字是 HTML 叠的**。HTML 不做格子布局，只在漫画页图片上叠加文字层。

### 编写页面配置 JSON

在 `{漫画项目}/第{N}章/` 下创建 `页面配置.json`：

```json
{
  "title": "{章节标题}",
  "subtitle": "第{N}章 · {章节名}",
  "pages_dir": "output",
  "output_html": "index.html",
  "footer": "popwave",
  "pages": [
    {
      "file": "page1.png",
      "captions": [
        {"type": "narration", "text": "西蜀在大西塬吃亏。", "position": "bottom"}
      ]
    },
    {"separator": true},
    {
      "file": "page2.png",
      "captions": [
        {"type": "narration", "text": "迟早要攻蜀。", "position": "bottom"},
        {"type": "dialogue", "text": "伐蜀只是顺便。", "position": "top-right"}
      ]
    },
    {"separator": true},
    {
      "file": "page3.png",
      "captions": []
    },
    {"separator": true},
    {
      "file": "page4.png",
      "captions": [
        {"type": "narration", "text": "擒主焚庙可矣。", "position": "bottom"}
      ]
    }
  ]
}
```

### 文字叠加类型

| 类型 | CSS 类 | 位置 | 说明 |
|:-----|:-------|:-----|:-----|
| 旁白条 | `.caption-narration` | 底部渐变遮罩 | 旁白叙述/内心独白/环境描写，直接使用小说原文 |
| 对白气泡 | `.caption-dialogue` | 指定位置（top-left/top-right/bottom-left/bottom-right） | 角色台词，圆角气泡+尾巴 |
| 章节标题 | `.page-title` | 页面顶部 | 章节标题叠加（仅第一页） |

> **大单页通常不加文字**——名场面画面自说，文字会干扰视觉冲击。如果导演卡标注"无（画面自说）"，captions 留空。

### 移动端适配

```css
/* 移动端优先：页面图片全宽，竖向滑动阅读 */
.comic-page {
  width: 100%;
  max-width: 820px;  /* 桌面端最大宽度 */
  margin: 0 auto;
  position: relative;
}
.comic-page img {
  width: 100%;
  height: auto;
  display: block;
}
/* 文字叠加使用绝对定位，按百分比定位以适配不同屏幕 */
.caption-narration {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 40px 20px 16px;
  background: linear-gradient(0deg, rgba(0,0,0,0.85) 0%, rgba(0,0,0,0.4) 60%, transparent 100%);
}
.caption-dialogue {
  position: absolute;
  max-width: 45%;
  padding: 10px 14px;
  background: rgba(255,255,255,0.92);
  border-radius: 12px;
  font-size: 14px;
  line-height: 1.6;
  color: #1a1a1a;
}
```

> 完整 CSS 实现见 `references/page-layout-guide.md`。

### 生成 HTML 漫画页面

根据页面配置 JSON，生成 `index.html`：

1. 读取 `页面配置.json` 中的 pages 数组
2. 每页图片用 `<div class="comic-page">` 包裹，`<img src="output/pageN.png">`
3. 文字叠加用绝对定位的 `.caption-narration` / `.caption-dialogue` 元素
4. 页面之间插入 `<div class="scene-break">◇ ◇ ◇</div>` 对应 separator
5. 底部 footer 显示品牌信息

### 本地 HTTP 服务器预览

```powershell
cd "{漫画项目}/第{N}章"
python -m http.server 8000
# 浏览器打开 http://localhost:8000/index.html
```

### 输出

`{漫画项目}/第{N}章/index.html`（HTML 漫画页面，外部图片引用 + 文字叠加层）。

## 4. 截长图（分享用）

> 使用 Playwright 逐元素截图 + Pillow 拼接输出长图，用于分享。

```powershell
python "{本skill路径}/scripts/screenshot_comic.py" "{漫画项目}/第{N}章/index.html" "{漫画项目}/第{N}章/长图-{章节名}.png"
```

### 截图原理

1. Playwright headless 浏览器加载 HTML 页面
2. 等待所有图片完全加载（`img.complete && img.naturalWidth > 0`）
3. 自动检测页面元素（`.comic-page`, `.scene-break`）
4. 逐元素滚动到视口并截图
5. Pillow 拼接所有元素截图为完整长图

### 注意事项

- 截图前确保本地 HTTP 服务器已启动（或使用 file:// 协议直接加载）
- 视口宽度默认 820px，可通过 `SCREENSHOT_WIDTH` 环境变量调整
- 如未安装 Playwright，执行 `pip install playwright && playwright install chromium`

## 5. 进入 Phase 2

页面生成+文字叠加完成后，自动进入 Phase 2（读取 `steps/step3-review.md`）执行视觉审核和记忆沉淀。
