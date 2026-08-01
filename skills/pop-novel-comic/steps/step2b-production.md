# Step 2b: 页面生成+文字叠加

> 增量定妆图（如有）→ 逐页生成 → 翻页阅读器 HTML → 截图分享 → 进入 Phase 2

## 设计哲学

Step 2b 的唯一任务是"执行"——基于 Step 2a 的页面提示词，生成漫画页图片、叠加文字、截图。**不做创作决策**——所有创作决策（页面设计、提示词、旁白文字）已在 Step 1+2a 完成，Step 2b 只负责按图纸施工。

**v4.0 核心变化**：
- 生成单位从"格"升级为"页"——`generate_comic_page.py` 逐页生成，每页一张含多格的完整漫画图
- HTML 职责简化——不再做格子布局（画面已有分格线），只做文字叠加（旁白条/对白气泡）
- **v4.3 翻页阅读器**——从长滚动页面改为翻页阅读器，一次只显示一页，点击/滑动/方向键切换，移动端全屏沉浸

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

## 3. 翻页阅读器 HTML 生成

> **必读 `references/page-layout-guide.md`**：翻页阅读器完整 HTML 模板、文字叠加 CSS、导航交互实现。

**v4.3 核心变化**：从长滚动页面改为**翻页阅读器**——一次只显示一页，左右点击/滑动/方向键切换。更接近真实漫画阅读体验，移动端全屏沉浸。

### 编写页面配置 JSON

在 `{漫画项目}/第{N}章/` 下创建 `页面配置.json`：

```json
{
  "title": "{章节标题}",
  "subtitle": "第{N}章 · {章节名}",
  "poem": "鉴中千秋血，镜外万骨枯。",
  "seal": {"text": "终", "position": "bottom-right"},
  "pages_dir": "output",
  "output_html": "index.html",
  "footer": "popwave",
  "pages": [
    {
      "file": "page1.png",
      "captions": [
        {"type": "narration", "text": "旁白文字", "position": "bottom"}
      ]
    },
    {
      "file": "page2.png",
      "captions": [
        {"type": "narration", "text": "旁白文字", "position": "bottom"},
        {"type": "dialogue", "text": "对白文字", "position": "top-right"}
      ]
    },
    {
      "file": "page3.png",
      "captions": []
    }
  ]
}
```

> **翻页阅读器中不再使用 `separator` 字段**——翻页本身就是页面间的分隔。`poem`/`seal` 为可选字段（古风赛道文化元素，详见 `references/cultural-elements-guide.md`）。

### 文字叠加类型

| 类型 | CSS 类 | 位置 | 说明 |
|:-----|:-------|:-----|:-----|
| 旁白条 | `.caption-narration` | 底部/顶部渐变遮罩 | 旁白叙述/内心独白/环境描写，直接使用小说原文 |
| 对白气泡 | `.caption-dialogue` | 指定位置（top-left/top-right/bottom-left/bottom-right） | 角色台词，圆角气泡 |

> **大单页通常不加文字**——名场面画面自说，文字会干扰视觉冲击。如果导演卡标注"无（画面自说）"，captions 留空。
> 章节标题不再用文字叠加，而是由翻页阅读器的标题页（data-index=0）独立展示。

### 生成翻页阅读器 HTML

根据页面配置 JSON 和 `references/page-layout-guide.md` 中的完整 HTML 模板，生成 `index.html`：

1. **标题页**（data-index=0）：章节标题 + 副标题 + "点击进入"提示
2. **漫画页**（data-index=1~N）：每页一个 `.page-view`，内含 `.comic-page` 图片 + 文字叠加
3. **章末页**（data-index=N+1）："未完待续" + 品牌信息
4. **导航层**：左侧30%上一页 / 右侧30%下一页 / 中间40%不触发
5. **页码指示器**：底部居中，标题页和章末页不显示
6. **交互脚本**：键盘方向键 + 触摸滑动 + 点击导航

> 完整 HTML 模板（含 CSS + JavaScript）见 `references/page-layout-guide.md` §「完整 HTML 模板」。**直接复制模板，替换 `{章节标题}`/`{章节名}`/`pageN.png`/`{旁白文字}` 等占位符即可。**

### 本地预览

```powershell
cd "{漫画项目}/第{N}章"
python -m http.server 8000
# 浏览器打开 http://localhost:8000/index.html
```

### 输出

`{漫画项目}/第{N}章/index.html`（翻页阅读器，一次一页，点击/滑动/方向键切换）。

## 4. 截图分享（可选）

> 翻页阅读器适配：截图脚本需逐页激活 `.page-view` 后截图，再 Pillow 拼接为长图。

```powershell
python "{本skill路径}/scripts/screenshot_comic.py" "{漫画项目}/第{N}章/index.html" "{漫画项目}/第{N}章/长图-{章节名}.png"
```

### 注意事项

- 截图脚本需适配翻页阅读器结构：逐个激活 `.page-view`（设置 `active` 类）→ 截图 → 拼接
- 跳过标题页和章末页，只截取漫画内容页
- 截图前确保本地 HTTP 服务器已启动
- 如未安装 Playwright，执行 `pip install playwright && playwright install chromium`

## 5. 进入 Phase 2

页面生成+文字叠加完成后，自动进入 Phase 2（读取 `steps/step3-review.md`）执行视觉审核和记忆沉淀。
