---
name: pop-recommend
description: "当用户说'推书/推书卡/读者推荐'时启用。从小说原文生成读者推书卡HTML，三阶段价值扫描100章只精读30-40章。"
---

# pop-recommend

> 推书营销专家。从小说原文→读者推书卡（给新读者的无剧透推荐）。v2.0.0

## 做什么

输入：小说原文txt文件
输出：一张可分享的推书卡HTML（9页式读者推荐卡）+ 评审JSON

推书不是拆书。目标是帮新读者判断"这本书值不值得看、适不适合我"。每个判断带原文证据+spoiler标注。

**执行模式**：Step 1 三阶段价值扫描是只读扫描类工作（100章只精读30-40章），天然适配子agent——子agent读原文扫描+提取锚点+打分并回报结果，主agent落盘5个JSON；Step 2 评审合成与 Step 3 HTML渲染主agent直执。

## 怎么操作（SOP全内联）

> execution.mode: 串联式 | 强保障：本SKILL.md由host层强制注入 | 弱保障：references/templates需agent主动读取，设计时假设可能没读到

**Step 1 三阶段价值扫描**（内化）：ETL精简版(编码归一+章节分割+元数据,禁止逐章摘要)→Phase1骨架扫描(首章+每卷首尾+尾章≈15-20章,产出structure-map.json)→Phase2锚点深读(highlight/controversy/character/relationship章≈10-15章,产出anchor-pool.json+evidence-ledger.json)→Phase3阅感采样(全书均匀采样5-8章,6维度量化打分,产出reading-metrics.json) → 5个JSON落盘工作稿/

**Step 2 评审生成**：读 `工作稿/` 下5个JSON——chapter-index.json（章号映射）/ structure-map.json（定位+结构+候选节点）/ anchor-pool.json（卖点+争议+人物+关系锚点）/ evidence-ledger.json（原文摘录）/ reading-metrics.json（量化评分+避雷项）→ 合成 `工作稿/review.json`（**唯一评审输出文件**，schema_version 1.0，metadata含title/author/platform/word_count/status）。合成规则：

| 字段 | 合成规则 |
|:--|:--|
| positioning | 直接取 structure-map 的 one_liner / core_hook / tags |
| synopsis | 基于 structure-map 的 structure 数组合成3-4句无剧透梗概：只用 summary_safe 字段+safe级信息，**禁用任何mild/major内容**；讲清"故事方向"不讲"发生了什么" |
| strengths[] | anchor-pool 筛 type=strength，只纳入 safe/mild 级；字段=title/judgement/mechanism/boundary/evidence_ids（每条必留）；mild 级的 judgement 和 mechanism 模糊化（去具体情节，保留趋势描述） |
| characters[] | anchor-pool 筛 type=character，只纳入 safe/mild 级；字段=name/identity/surface_traits/inner_drive/relationship_function/evidence_ids；mild 级的 inner_drive 模糊化 |
| world | anchor-pool type=world + structure-map 结构信息：复杂度评级(low/medium/high)+核心规则(safe级)+卷/阶段结构 |
| reading_experience | 直接取 reading-metrics 的 reading_experience（style/pacing_note/emotional_tone/readability/plot_density_note） |
| controversies[] | anchor-pool 筛 type=controversy，只纳入 safe/mild 级；字段同strengths；mild 级的 mechanism 模糊化 |
| audience | 基于 strengths+controversies+reading_metrics 综合判断：recommended / avoid 各3-4条，每条必须是具体读者画像，禁止泛泛的"喜欢XX的读者" |
| scoring | 取 reading-metrics 的 dimensions 6维评分(characters/plot/prose/relationships/world/pacing)；base_score=6维均值；audience_bonus=strengths≥3且controversies≤2时+1.0 |
| recommendation | score_low/score_high=base_score-1.5 到 base_score+audience_bonus；stars_low/stars_high=score/2；grade=干草/粮草/粮草+/仙草-/仙草；verdict=一句话结论；why_try=面向犹豫读者的1段话 |
| completion_note | 从 chapter-index.json metadata 提取完结状态；status=partial 必须注明"仅评价已有内容，对结局不做判断" |

**Step 2 质量门控**：❌禁止生成第二个JSON文件（review.json是唯一输出）｜❌禁止使用 major 级别的锚点或证据｜❌禁止无 evidence_ids 的 strength/controversy｜❌禁止 audience 泛泛描述（如"喜欢修仙的读者"）｜✓synopsis ≤4句且无剧透｜✓所有 mild 级内容经过模糊化处理｜✓completion_note 说明完结状态

**Step 3 HTML渲染**：
1. 读 `工作稿/review.json` + `templates/recommend-card.tpl.html`（**模板必须读取**，内含完整CSS+9个渲染函数+4处SVG装饰）
2. review.json 转为 JS 变量内容：`window.__BOOK_DATA__ = {...};`
3. 替换模板两个占位符：`{{TITLE}}`→书名；`{{REVIEW_DATA}}`→JS变量内容
4. 落盘项目根目录：`{书名}-读者推书-v1.html`——自包含文件，双击浏览器直接打开，打开即验证，链式管线结束

模板说明：recommend-card.tpl.html 是完整可工作的HTML骨架，含完整CSS（5主题色+9种页面设计语言样式+品牌印记样式）、4处inline SVG装饰图标（封面翻书图标/卖点页靶标/仪表盘折线图/封底五星评级）、9个渲染函数（P1-P9对应9种页面类型）、review.js fallback加载逻辑。**不要修改模板中的任何CSS类名、SVG代码块或渲染函数**，只做两个占位符替换。9页布局设计语言参考 `references/recommend-layout-guide.md`。

## 红线

1. **读取协议**——读取skill文件用`Get-Content -Encoding UTF8 -Raw`，Read工具有行数限制会截断丢内容
2. **禁止逐章摘要**——必须用三阶段价值扫描，100章只精读30-40章
3. **所有判断绑定evidence_id**——每条strength/controversy/character必须引用证据台账，excerpt≥50字
4. **review.json是唯一评审输出**——禁止生成input+draft两个重复JSON
5. **管线顺序强制**——Step1价值扫描→Step2评审生成→Step3 HTML渲染，禁止跳步（未完成扫描禁止生成评审，未生成review.json禁止渲染HTML）

## 速查表

| 文件 | 读取时机 | 核心内容 |
|:--|:--|:--|
| `references/recommend-layout-guide.md` | Step3渲染时参考 | 9页布局设计指南 |
| `templates/*.tpl.json` | Step1-2产出时复制填充 | JSON模板（structure-map/anchor-pool/reading-metrics/review） |
| `templates/recommend-card.tpl.html` | Step3渲染时使用 | HTML推书卡模板 |

## 版本

v2.0.0 | 2026-08-24 | steps 两件（step2/step3）全合入SKILL.md单文件精炼，steps目录删除；执行模式明确——Step1价值扫描可派子agent（只读扫描回报，主agent落盘），Step2/3主agent直执 → CHANGELOG.md

v1.3.0 | 2026-08-13 | 按Popwave Skill设计规范重写SKILL.md结构（≤100行），红线合并为5条含读取协议 → CHANGELOG.md
