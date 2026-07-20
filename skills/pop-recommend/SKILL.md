# pop-recommend · 推书营销专家

> 从小说原文 → 读者推书卡（给新读者的无剧透推荐）
> v1.0.0：新建skill，替代 v1.5.3 工作稿的临时管线

---

## 做什么

输入：小说原文 txt 文件
输出：一张可分享的推书卡 HTML（9页式读者推荐卡）+ 评审 JSON

**定位**：推书，不是拆书。目标是帮新读者判断"这本书值不值得看、适不适合我"，不是帮创作者分析"这本书怎么写的"。

**和 decon 的边界**：
- decon = 创作者视角（8维度全拆+Beat Sheet），用于精拆一本书做立项圣经
- pop-recommend = 读者视角（价值扫描+无剧透评审），用于给新读者推书
- 两者读同一本书但视角完全不同，不冲突

---

## SOP骨架

| 步骤 | 做什么 | 产出 | 详细方法 |
|------|--------|------|---------|
| Step 1 | 三阶段价值扫描（骨架扫描→锚点深读→阅感采样） | 5个JSON文件 | steps/step1.md |
| Step 2 | 评审生成（消费5个JSON → 合成 review.json） | review.json | steps/step2.md |
| Step 3 | HTML渲染（review.json → 推书卡 HTML） | 推书卡.html | steps/step3.md |

---

## Step 1 三阶段价值扫描

**核心原则**：放弃逐章摘要。100章只精读30-40章，每个判断带原文证据 + spoiler标注。

| 阶段 | 读什么 | 读多少 | 产出 |
|:--|:--|:--|:--|
| Phase 1 骨架扫描 | 首章 + 每卷首尾 + 尾章 | ≈15-20章 | structure-map.json + chapter-index.json |
| Phase 2 锚点深读 | Phase1识别的高光/争议/人物/关系节点 | ≈10-15章 | anchor-pool.json + evidence-ledger.json |
| Phase 3 阅感采样 | 全书均匀采样 | 5-8章 | reading-metrics.json |

**Phase 2 是核心**——这是推书价值提取的主战场，所有卖点/争议/人物判断都来自这个阶段。

---

## spoiler控制

推书最怕剧透。每个锚点和证据必须标注 spoiler_level：

| 级别 | 含义 | 推书卡可用 |
|:--|:--|:--|
| safe | 无剧透，只涉及开局设定和公知信息 | ✓ 全部页面可用 |
| mild | 轻微剧透，涉及中期发展方向 | ✓ 模糊化后可用 |
| major | 重大剧透，涉及结局/核心反转 | ✗ 禁止出现在推书卡 |

Step 2 生成 review.json 时，只消费 safe + mild 级别的锚点和证据。

---

## 红线

1. **禁止逐章摘要**——必须用三阶段价值扫描替代，100章只精读30-40章，禁止生成逐章 digests 文件
2. **所有判断必须绑定 evidence_id**——strengths/controversies/characters 的每条判断都必须引用 evidence-ledger 中的证据，禁止无据判断
3. **review.json 是唯一评审输出文件**——禁止生成 input+draft 两个重复JSON，合并为一个 review.json
4. **HTML模板必须与数据分离**——禁止将 review.json 内联到 HTML 的 `<script>` 标签中，必须通过外部文件加载

---

## 速查表

### 产出文件

| 产出 | 路径 | 产出阶段 | 消费方 |
|:--|:--|:--|:--|
| chapter-index.json | `工作稿/` | Step1-Phase1 | Step1-Phase2导航 |
| structure-map.json | `工作稿/` | Step1-Phase1 | Step2 |
| anchor-pool.json | `工作稿/` | Step1-Phase2 | Step2 |
| evidence-ledger.json | `工作稿/` | Step1-Phase2 | Step2 |
| reading-metrics.json | `工作稿/` | Step1-Phase3 | Step2 |
| review.json | `工作稿/` | Step2 | Step3 |
| 推书卡.html | 项目根目录 | Step3 | 读者分享 |

### 推书卡9页结构

| 页码 | 类型 | 内容 | 数据来源 |
|:--|:--|:--|:--|
| 1 | cover | 封面：书名+作者+一句话定位+标签 | structure-map |
| 2 | hook | 核心梗：与同类书的差异 | anchor-pool |
| 3 | synopsis | 无剧透梗概：故事方向 | structure-map |
| 4 | characters | 人物角色卡：谁值得关注 | anchor-pool |
| 5 | chemistry | 关系化学：人物关系引擎 | anchor-pool |
| 6 | structure | 故事结构：读者需知道的结构 | structure-map |
| 7 | selling_points | 具体卖点：好看在哪里 | anchor-pool |
| 8 | risks | 阅感与避雷：哪些人弃书 | reading-metrics + anchor-pool |
| 9 | verdict | 最终结论：适合谁 | review.json |

### block类型

quote / lede / paragraph / panel / cards / steps / tags / route / formula / bullets / warning / metrics / radar / audience / verdict

---

## 版本

v1.0.0 | 2026-07-20 | 新建skill。三阶段价值扫描替代逐章摘要 + spoiler三级控制 + review.json合并去重 + HTML模板数据分离 → CHANGELOG.md
