# Step 3: 生成 + 审核

> 增量定妆图（如有）→ 8并发生成 → 长条滚动HTML → 产出检查+感染力评审 → 记忆沉淀

## 设计哲学

Step 3 是**执行+收尾**——按 Step 2 的图纸施工，生成漫画页，叠文字，然后审核沉淀。不做创作决策，所有决策已在 Step 2 完成。

**生成后立即审核。** 不连续生成两章不审核——记忆断裂会导致下章角色状态和视觉问题丢失。

## 1. 增量定妆图（如有变化）

场景表标注了角色外观变化的，先生成增量定妆图：

1. 基于当前版本冻结提示词 + 变化描述，组装新提示词
2. 生成双角度新版本（正面+侧面），保存到 `assets/characters/char-{名}-v{N+1}-front.png` / `-side.png`
3. 新提示词冻结到角色库
4. 更新角色库增量定妆表和决策日志

> 无变化的章节跳过此步骤。

## 2. 生图（任务清单导出 + image_generate 工具）

> `generate_comic_page.py` **不再直连生图 API，也不内置任何 API Key**。它只负责：从 `PAGES` 解析每页提示词与参考图 → 校验尺寸 → 导出 `output/generation_tasks.json`，由主 agent 用 `image_generate` 工具逐张生成（图生图时传参考图保证角色一致）。

### 配置生成脚本

**从 `storyboard.md` 读取每页提示词和参考图**，写入 `generate_comic_page.py` 的 `PAGES` 列表：

```python
PAGES = [
    {
        "id": "page1",
        "prompt": "{从storyboard.md P1复制完整6段式提示词}",
        "ref_images": ["char-{角色名}-v{N}-front.png", "char-{角色名}-v{N}-side.png"],
        "size": "1125x1500",
    },
    # ... 更多页
]
OUTPUT_DIR = r"第{N}章/output"
CHAR_ASSETS_DIR = r"assets/characters"
```

> **提示词从 storyboard.md 复制，不重新组装。**

### 导出任务清单

```powershell
python "{本skill路径}/scripts/generate_comic_page.py"
```

输出：`output/generation_tasks.json`（含每页 id/prompt/size/ref_images/output_path）。

### 用 image_generate 工具逐张生成

读取 `output/generation_tasks.json`，对每条任务调用 `image_generate` 工具：
- 有 `ref_images` 时按工具能力传入参考图路径（图生图，保证角色一致）
- 输出到任务的 `output_path`（`output/page1.png` ~ `output/pageN.png`）

生成完成后校验图片格式（扩展名与实际字节一致，JPEG 需转码为真 PNG）。

## 3. 长条滚动 HTML

> **必读 `references/guides/page-layout-guide.md`** — 长条滚动完整 HTML 模板、文字叠加 CSS。

### 编写页面配置 JSON

在 `第{N}章/` 下创建 `页面配置.json`：

```json
{
  "title": "{章节标题}",
  "subtitle": "第{N}章 · {章节名}",
  "pages_dir": "output",
  "output_html": "index.html",
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
        {"type": "narration", "text": "旁白", "position": "bottom"},
        {"type": "dialogue", "text": "对白", "position": "top-right"}
      ]
    }
  ]
}
```

### 文字叠加类型

| 类型 | CSS 类 | 说明 |
|:-----|:-------|:-----|
| 旁白条 | `.caption-narration` | 旁白/独白/环境描写 |
| 对白气泡 | `.caption-dialogue` | 角色台词 |

> 大单页通常不加文字——名场面画面自说。

### 生成 HTML

根据页面配置 JSON 和 `references/guides/page-layout-guide.md` 的 HTML 模板生成 `index.html`。纯 HTML+CSS，零 JS。

### 本地预览

```powershell
cd "{漫画项目}/第{N}章"
python -m http.server 8000
```

### 截图分享（可选）

```powershell
python "{本skill路径}/scripts/screenshot_comic.py" "{漫画项目}/第{N}章/index.html" "{漫画项目}/第{N}章/长图-{章节名}.png"
```

## 4. 产出检查

| 检查项 | 达标标准 |
|:-------|:---------|
| 页数完整 | 导演卡每页 page{N}.png 全部存在 |
| 图片格式 | 全部真PNG（magic bytes `89 50 4E 47`） |
| HTML 已生成 | index.html 落盘，图片引用路径正确 |
| storyboard.md | 分镜脚本已落盘 |
| 导演卡 | 第{N}章/导演卡.md 已落盘 |

## 5. 感染力评审

| 维度 | 检查问题 | 通过标准 |
|:-----|:---------|:---------|
| **叙事流** | 不看原文能理解"谁做了什么、为什么、导致了什么"吗？ | 因果链完整，每页推进故事 |
| **页面节奏** | 相邻页格数/布局/类型有变化吗？ | 页面类型有交替 |
| **情绪钉子** | 至少有一页"读者会记住"的画面？ | 大单页承载核心情绪爆发 |
| **角色一致性** | 每页参考图配置正确？ | storyboard ref_images 与角色库版本对应 |
| **扫描测试** | 只看旁白/对白能读出完整故事弧？ | 旁白串起来讲清起因→后果 |

### 5.1 0基础可读性检查（v7.6.0）

> 2026-08-04 chapter1 实测血泪教训：改编精美的画面，0基础读者却"不知道讲了什么"。根因是纯视觉化、文字层太薄。此检查是**审稿门禁**，不通过不得进入记忆沉淀。

| 检查项 | 通过标准 |
|:-------|:---------|
| 无纯画面无文字页 | 每页至少 1 条旁白/台词/OS，无"图片+空白"页 |
| 因果链完整 | 旁白/OS 串起来能讲清"谁→做了什么→为什么→导致了什么" |
| 关键异变/规则/时空有解释 | 视觉事件、系统设定、场景跳转均有旁白交代 |
| 主角决策有动机 | 每次做决定都有 OS 或旁白说明理由 |
| 开场引子（第1章） | 标题下交代人物+处境+悬念 |
| 文字不遮关键画面 | 每页文字 ≤4 条，不压住表情/道具/表盘 |

> 方法论见 `references/guides/adaptation-guide.md` §0基础读者可读性（三层文字法：旁白讲因果/台词给事件/内心OS给动机）。

> ⚠️ 记录即可不阻断；❌ 记录问题并在下章导演卡中改进。

## 6. 记忆沉淀

### 6.1 Append 视觉沉淀.md

```markdown
## 第{N}章审核 | {日期}

### 产出状态
- 页数: {N}/{N} ✅
- HTML: ✅ | 长图: ✅ | storyboard: ✅ | 导演卡: ✅

### 感染力评审
- 叙事流: ✅/⚠️/❌ — {说明}
- 页面节奏: ✅/⚠️/❌ — {说明}
- 情绪钉子: ✅/⚠️/❌ — {说明}
- 角色一致性: ✅/⚠️/❌ — {说明}
- 扫描测试: ✅/⚠️/❌ — {说明}

### 定妆图使用
- {角色名}: v{N}（{出场页码}）

### 问题记录 & 改进规则
- {问题} → {规则}
```

### 6.2 更新漫画快照.md（replace）

- 章节清单：追加本章记录
- 角色出场记录：更新
- 风格锚定串：不变
- 已知视觉问题池：从沉淀提取

### 6.3 更新漫画状态.md（replace）

- 当前章位：下一章
- 角色状态：当前外观版本+描述
- 上一章问题：从沉淀提取
- 注意事项：下章需注意的（如"角色已换装，需使用v2定妆图"）

## 7. 完成

- 还有下一章 → 回到 Step 1（读取 `steps/step1-scene-breakdown.md`）
- 本卷结束 → 通知用户
