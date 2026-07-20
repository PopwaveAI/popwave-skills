# Step 3 · HTML渲染

> 消费 review.json → 生成9页式推书卡 HTML
> 核心原则：模板与数据分离，禁止内联JSON到 `<script>` 标签

---

## 输入

读取 `工作稿/review.json`。

---

## 渲染策略

**数据内联**：将 review.json 转为 JS 变量后直接嵌入 HTML，不依赖外部文件。

实际操作：
1. 读取模板 `templates/recommend-card.tpl.html`
2. 将 `{{TITLE}}` 替换为书名
3. 将 `{{REVIEW_DATA}}` 替换为 `window.__BOOK_DATA__ = {...};`（review.json 的 JS 版）
4. 最终 HTML 是自包含的，可双击直接在浏览器打开，无 `file://` 协议限制

**弱水印**：模板 CSS 已内置 `popwave.cn` 水印（每页右下角，9px/18%透明度），无需额外操作。

---

## 9页结构

推书卡固定9页，720×960px。每页通过 `type` 映射独立的排版语言：

| type | 设计范式 | CSS class | 核心特征 |
|:--|:--|:--|:--|
| cover | **Cinematic Poster** | page-cover | 暗色渐变+超大衬线书名+金线引言 |
| hook | **Swiss Grid** | page-swiss | 纯白+左黑边+2×2十字分割+01-04数字 |
| synopsis | **Magazine Editorial** | page-magazine | 左深色边栏(竖排眉标)+右内容+时间线圆点 |
| characters | **Profile Spread** | page-profiles | 上眉线+2×2人物卡+名字下划线+驱动力正文 |
| chemistry | **Infographic** | page-infographic | 居中A×B公式框+2解释卡 |
| structure | **Horizontal Timeline** | page-timeline | 横向黑线+圆点节点+底部路线框 |
| selling_points | **Feature Showcase** | page-showcase | 全黑底+金字+1px分割网格+编号 |
| risks | **Dashboard** | page-dashboard | 左6维条形图+右红框警告+红标签 |
| verdict | **Back Cover** | page-backcover | 深色渐变+居中大评分+双栏推荐 |

### Page 1 · cover（封面）
- **数据来源**：`metadata` + `positioning` + `tags`
- **block组成**：quote（一句话定位）+ lede（核心钩子）+ tags（标签）

### Page 2 · hook（核心梗）
- **数据来源**：`positioning.core_hook` + strengths
- **block组成**：cards（4张差异卡）+ panel（真正的故事问题）

### Page 3 · synopsis（无剧透梗概）
- **数据来源**：`synopsis` + `world.structure`
- **block组成**：steps（4步故事方向）+ panel（故事推进的轴心）

### Page 4 · characters（人物角色卡）
- **数据来源**：`characters`（取前4个）
- **block组成**：cards（4张人物卡）+ panel（群像功能）

### Page 5 · chemistry（关系化学）
- **数据来源**：anchor-pool 中 type: "relationship" 的锚点
- **block组成**：formula（双方驱动力）+ cards（2张关系动态卡）+ panel（关系向前的标志）
- **省略条件**：无关系锚点时可跳过，9页变8页

### Page 6 · structure（故事结构）
- **数据来源**：`world.structure` + `reading_experience`
- **block组成**：cards（4张结构卡）+ route（故事路线）

### Page 7 · selling_points（具体卖点）
- **数据来源**：`strengths`（全部）
- **block组成**：cards（卖点卡）+ panel（强项边界）

### Page 8 · risks（阅感与避雷）
- **数据来源**：`reading_experience` + `scoring.dimensions` + `controversies`
- **block组成**：radar（6维雷达图）+ warning（避雷项）+ panel（争议如何理解）

### Page 9 · verdict（最终结论）
- **数据来源**：`audience` + `recommendation`
- **block组成**：audience（推荐/不推荐）+ verdict（评分+结论）+ panel（为什么值得试读）

---

## 主题系统

5种主题可选（根据书的类型自动选择或用户指定）：

| 主题 | 适用类型 | 主色 |
|:--|:--|:--|
| literary-red | 文学/言情 | 暗红+米白 |
| ink-blue | 仙侠/玄幻 | 墨蓝+青白 |
| warm-paper | 都市/现实 | 暖棕+纸黄 |
| dark-modern | 悬疑/科幻 | 暗灰+橙红 |
| diary-orange | 青春/校园 | 橙+蓝灰 |

选择规则：
- tags 含"修仙/玄幻/仙侠" → ink-blue
- tags 含"悬疑/科幻/恐怖" → dark-modern
- tags 含"青春/校园/暗恋" → diary-orange
- tags 含"都市/现实/职场" → warm-paper
- 默认 → literary-red

---

## block类型渲染规则

| block类型 | 渲染方式 | 数据字段 |
|:--|:--|:--|
| quote | 左侧粗边引言 | text |
| lede | 引导段落 | text |
| paragraph | 普通段落 | text |
| panel | 带标题的面板 | title + text |
| cards | 2列卡片网格 | items[{title, text}] |
| steps | 编号步骤列表 | items[{title, text}] |
| tags | 标签云 | items[] |
| route | 路径流 | items[] |
| formula | 公式流 | items[] |
| bullets | 双列列表 | items[] |
| warning | 警告框 | title + items[] |
| metrics | 3列指标 | items[{value, label}] |
| radar | 雷达条 | items[{label, value}] |
| audience | 推荐/不推荐双栏 | items{recommended[], avoid[]} |
| verdict | 深色结论框 | title + text |

---

## 产出

`{书名}-读者推书-v1.html` + `review.js`（备用，供外部调试加载）

---

## 质量门控

- ❌ 禁止 {{REVIEW_DATA}} 占位符未被替换为空数据 HTML
- ❌ 禁止超过9页
- ❌ 禁止空页面（每页至少2个block）
- ✓ HTML 内联 review.json 数据，可双击直接打开
- ✓ 每页必须有 footer（页脚标注页码+页面类型）
- ✓ 雷达图6个维度必须全部有值

---

## 完成检查

HTML 文件可在浏览器直接打开，9页完整渲染，数据正确加载。

推书卡交付完成。
