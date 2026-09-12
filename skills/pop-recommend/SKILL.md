# pop-recommend

> 推书营销专家。输入小说原文，输出读者推书卡（给新读者的无剧透推荐）。v2.1.0

## 做什么

输入：小说原文txt文件
输出：一张可分享的推书卡HTML（9页式读者推荐卡），以及一份评审JSON

推书不是拆书。目标是帮新读者判断"这本书值不值得看、适不适合我"。每个判断都带原文证据与spoiler标注。

**执行模式**：Step 1 的三阶段价值扫描属于只读扫描类工作（100章只精读30-40章），适合交给子agent——子agent读取原文、扫描并提取锚点、打分，然后回报结果，主agent写入5个JSON；Step 2 的评审合成与 Step 3 的HTML渲染由主agent直接执行。

## 怎么操作（流程全内联）

> execution.mode: 串联式 | 强保障：本SKILL.md由平台强制注入 | 弱保障：references与templates需agent主动读取，设计时假设可能没读到

**Step 1 三阶段价值扫描**（内化）：ETL精简版（编码归一、章节分割、元数据读取，禁止逐章摘要）→Phase1骨架扫描（首章、每卷首尾、尾章，约15-20章，产出structure-map.json）→Phase2锚点深读（highlight、controversy、character、relationship类章节，约10-15章，产出anchor-pool.json与evidence-ledger.json）→Phase3阅感采样（全书均匀采样5-8章，6维度量化打分，产出reading-metrics.json）→5个JSON写入工作稿/

**Step 2 评审生成**：读取 `工作稿/` 下的5个JSON：chapter-index.json（章号映射）、structure-map.json（定位、结构、候选节点）、anchor-pool.json（卖点、争议、人物、关系锚点）、evidence-ledger.json（原文摘录）、reading-metrics.json（量化评分、避雷项），据此合成 `工作稿/review.json`（**唯一评审输出文件**，schema_version 1.0，metadata含title、author、platform、word_count、status）。合成规则如下：

| 字段 | 合成规则 |
|:--|:--|
| positioning | 直接取 structure-map 的 one_liner / core_hook / tags |
| synopsis | 基于 structure-map 的 structure 数组合成3-4句无剧透梗概：只使用 summary_safe 字段与safe级信息，**禁用任何mild/major内容**；讲清"故事方向"，不讲"发生了什么" |
| strengths[] | 从 anchor-pool 中筛选 type=strength 的条目，只纳入 safe/mild 级；字段为title、judgement、mechanism、boundary、evidence_ids（每条必留）；mild 级的 judgement 和 mechanism 模糊化（去掉具体情节，保留趋势描述） |
| characters[] | 从 anchor-pool 中筛选 type=character 的条目，只纳入 safe/mild 级；字段为name、identity、surface_traits、inner_drive、relationship_function、evidence_ids；mild 级的 inner_drive 模糊化 |
| world | anchor-pool 中 type=world 的条目与 structure-map 的结构信息：复杂度评级(low/medium/high)、核心规则(safe级)、卷与阶段结构 |
| reading_experience | 直接取 reading-metrics 的 reading_experience（style/pacing_note/emotional_tone/readability/plot_density_note） |
| controversies[] | 从 anchor-pool 中筛选 type=controversy 的条目，只纳入 safe/mild 级；字段同strengths；mild 级的 mechanism 模糊化 |
| audience | 基于 strengths、controversies、reading_metrics 综合判断：recommended 与 avoid 各3-4条，每条必须是具体读者画像，不得用泛泛的"喜欢XX的读者" |
| scoring | 取 reading-metrics 的 dimensions 6维评分(characters/plot/prose/relationships/world/pacing)；base_score 为6维均值；audience_bonus 在 strengths≥3且controversies≤2 时为+1.0 |
| recommendation | score_low/score_high=base_score-1.5 到 base_score+audience_bonus；stars_low/stars_high=score/2；grade=干草/粮草/粮草+/仙草-/仙草；verdict=一句话结论；why_try=面向犹豫读者的1段话 |
| completion_note | 从 chapter-index.json metadata 提取完结状态；status=partial 必须注明"仅评价已有内容，对结局不做判断" |

**Step 2 质量门控**：❌不得生成第二个JSON文件（review.json是唯一输出）｜❌不得使用 major 级别的锚点或证据｜❌不得出现无 evidence_ids 的 strength 或 controversy｜❌不得把 audience 写成泛泛描述（如"喜欢修仙的读者"）｜✓synopsis ≤4句且无剧透｜✓所有 mild 级内容经过模糊化处理｜✓completion_note 说明完结状态

**Step 3 HTML渲染**：
1. 读取 `工作稿/review.json` 与 `templates/recommend-card.tpl.html`（**模板必须读取**，内含完整CSS、9个渲染函数、4处SVG装饰）
2. review.json 转为 JS 变量内容：`window.__BOOK_DATA__ = {...};`
3. 替换模板中的两个占位符：把 `{{TITLE}}` 替换为书名；把 `{{REVIEW_DATA}}` 替换为JS变量内容
4. 写入项目根目录：`{书名}-读者推书-v1.html`。该文件自包含，用浏览器直接打开即可完成验证，整条管线到此结束。

模板说明：recommend-card.tpl.html 是完整可工作的HTML骨架，含完整CSS（5主题色、9种页面设计语言样式、品牌印记样式）、4处inline SVG装饰图标（封面翻书图标、卖点页靶标、仪表盘折线图、封底五星评级）、9个渲染函数（P1-P9对应9种页面类型），以及review.js的加载兜底逻辑。**不要修改模板中的任何CSS类名、SVG代码块或渲染函数**，只替换两个占位符。9页布局设计语言参考 `references/recommend-layout-guide.md`。

## 红线

1. **读取协议**：读取skill文件用`Get-Content -Encoding UTF8 -Raw`；Read工具有行数限制，会截断并丢失内容
2. **不得逐章摘要**：必须用三阶段价值扫描，100章只精读30-40章
3. **所有判断绑定evidence_id**：每条strength、controversy、character必须引用证据台账，excerpt≥50字
4. **review.json是唯一评审输出**：不得生成input与draft两个重复JSON
5. **管线顺序强制**：Step1价值扫描→Step2评审生成→Step3 HTML渲染，不得跳步（未完成扫描不得生成评审，未生成review.json不得渲染HTML）

## 速查表

| 文件 | 读取时机 | 核心内容 |
|:--|:--|:--|
| `references/recommend-layout-guide.md` | Step3渲染时参考 | 9页布局设计指南 |
| `templates/*.tpl.json` | Step1-2产出时复制填充 | JSON模板（structure-map/anchor-pool/reading-metrics/review） |
| `templates/recommend-card.tpl.html` | Step3渲染时使用 | HTML推书卡模板 |

## 版本

当前版本 v2.1.0。完整版本历史见 [CHANGELOG.md](CHANGELOG.md)。
