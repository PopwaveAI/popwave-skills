# Step 3 · HTML渲染

> 消费 review.json → 生成9页式推书卡 HTML
> 核心原则：模板与数据分离，禁止内联JSON到 `<script>` 标签

---

## 输入

读取 `工作稿/review.json`。

---

## 渲染策略

**模板与数据分离**：HTML 文件中通过 `<script src="review.js">` 加载外部数据文件，而非内联到 `<script type="application/json">` 标签中。

实际操作：
1. 将 `review.json` 转为 `review.js`，内容为 `window.__BOOK_DATA__ = {...};`
2. HTML 文件通过 `<script src="review.js"></script>` 加载
3. 渲染脚本从 `window.__BOOK_DATA__` 读取数据

这样模板可跨书复用——换一本书只需替换 `review.js`，HTML 模板完全不动。

---

## 9页结构

推书卡固定9页，每页720×960px，对应 review.json 的不同字段：

### Page 1 · cover（封面）
- **数据来源**：`metadata` + `positioning` + `recommendation.score_range`
- **block组成**：quote（一句话定位）+ lede（核心钩子）+ tags（标签）
- **主题**：暗色封面，书名大字

### Page 2 · hook（核心梗）
- **数据来源**：`positioning.core_hook` + `strengths[0]`
- **block组成**：cards（4张差异卡）+ panel（真正的故事问题）
- **目的**：说清"这本书和同类书有什么不同"

### Page 3 · synopsis（无剧透梗概）
- **数据来源**：`synopsis` + `world.structure`
- **block组成**：steps（4步故事方向）+ panel（故事推进的轴心）
- **目的**：无剧透讲清故事方向

### Page 4 · characters（人物角色卡）
- **数据来源**：`characters`（取前4个）
- **block组成**：cards（4张人物卡）+ panel（群像功能）
- **目的**：说清"谁值得关注"

### Page 5 · chemistry（关系化学）
- **数据来源**：`anchor-pool` 中 `type: "relationship"` 的锚点（通过 review.json 的 characters 关联）
- **block组成**：formula（双方驱动力）+ cards（2张关系动态卡）+ panel（关系向前的标志）
- **目的**：说清"关系为什么好看"
- **注意**：如果无关系锚点，此页可省略，改为 selling_points 的延伸页

### Page 6 · structure（故事结构）
- **数据来源**：`world.structure` + `reading_experience`
- **block组成**：cards（4张结构卡）+ route（故事路线）
- **目的**：读者需知道的结构信息

### Page 7 · selling_points（具体卖点）
- **数据来源**：`strengths`（全部）
- **block组成**：cards（4张卖点卡）+ panel（强项边界）
- **目的**：说清"好看具体发生在哪里"

### Page 8 · risks（阅感与避雷）
- **数据来源**：`reading_experience` + `scoring.dimensions` + `controversies`
- **block组成**：radar（6维雷达图）+ warning（避雷项）+ panel（争议如何理解）
- **目的**：说清"哪些人可能弃书"

### Page 9 · verdict（最终结论）
- **数据来源**：`audience` + `recommendation`
- **block组成**：audience（推荐/不推荐）+ verdict（评分+结论）+ panel（为什么值得试读）
- **目的**：最终推荐

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

`{书名}-读者推书-v1.html` + `review.js`（数据文件）

两个文件放在同一目录，HTML通过相对路径引用 `review.js`。

---

## 质量门控

- ❌ 禁止将 review.json 内容内联到 HTML 的 `<script type="application/json">` 标签
- ❌ 禁止超过9页
- ❌ 禁止空页面（每页至少2个block）
- ✓ review.js 必须与 HTML 同目录
- ✓ 每页必须有 footer（页脚标注页码+页面类型）
- ✓ 雷达图6个维度必须全部有值

---

## 完成检查

HTML 文件可在浏览器直接打开，9页完整渲染，数据正确加载。

推书卡交付完成。
