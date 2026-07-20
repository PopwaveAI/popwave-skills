# pop-recommend · 推书营销专家

> 从小说原文 → 读者推书卡（给新读者的无剧透推荐）
> v1.1.0：SKILL.md 内化 Step 1 完整方法论，保证首步自执行

---

## 做什么

输入：小说原文 txt 文件
输出：一张可分享的推书卡 HTML（9页式读者推荐卡）+ 评审 JSON

**定位**：推书，不是拆书。目标是帮新读者判断"这本书值不值得看、适不适合我"。

---

## 管线总览

| 步骤 | 做什么 | 产出 | 怎么执行 |
|:--|:--|:--|:--|
| Step 1 | 三阶段价值扫描 | 5个JSON → `工作稿/` | **内化在本文件，直接执行** |
| Step 2 | 评审生成 | `工作稿/review.json` | **读取 `steps/step2.md`，执行后读取 step3.md** |
| Step 3 | HTML渲染 | `{书名}-读者推书-v1.html` | **读取 `steps/step3.md`，执行后交付** |

---

# Step 1 · 三阶段价值扫描（内化）

> 核心原则：放弃逐章摘要，100章只精读30-40章，每个判断带原文证据 + spoiler标注

## 前置：ETL精简版

读取小说 txt，做最小化预处理（**不做逐章摘要**）：

1. **编码归一化**：检测编码（GB18030/UTF-8），转为 UTF-8
2. **章节分割**：按 `第X章` 正则切分，生成 `chapter-index.json`（仅章号+章名+字符位置，无摘要）
3. **元数据提取**：书名、作者、平台、字数、完结状态

### chapter-index.json

```json
{
  "schema_version": "1.0",
  "metadata": { "title": "", "author": "", "platform": "", "word_count": null, "status": "" },
  "chapters": [{ "chapter_id": "ch-0001", "title": "第1章 XXX", "char_start": 0, "char_end": 2400 }]
}
```

**禁止生成 digests 文件。**

---

## Phase 1 · 骨架扫描

**目标**：快速建立全书骨架认知，识别 Phase 2 需要深读的节点。

**读什么**（≈15-20章）：首章 + 每卷首尾 + 尾章。如果无法识别卷界，按章数均分4-6段，取每段首尾。

**怎么读**：每章全文，带着4个问题：
1. 开局是什么类型？（穿越/重生/开局即危机/日常起步）
2. 主角是谁？核心驱动力？
3. 这个阶段讲了什么？（一句话，无剧透）
4. 有什么值得深读的高光/争议/转折节点？

**产出**：`structure-map.json`

```json
{
  "schema_version": "1.0",
  "metadata": { "title": "", "author": "", "platform": "", "word_count": null, "status": "" },
  "positioning": {
    "one_liner": "一句话定位（≤30字）",
    "core_hook": "核心钩子：与同类书的不同之处（1-2句）",
    "tags": ["标签1", "标签2"]
  },
  "structure": [
    { "segment_id": "seg-01", "title": "阶段名", "chapter_range": "ch-0001~ch-0026", "summary_safe": "无剧透一句话", "function": "开局/升级/转折/高潮/收尾" }
  ],
  "deep_read_candidates": [
    { "chapter_id": "ch-0001", "reason": "首章·建立世界观", "scan_type": "character_intro" }
  ]
}
```

**scan_type 枚举**：`character_intro` / `highlight` / `controversy` / `relationship` / `world_reveal` / `power_shift`

**质量门控**：❌禁止"故事内容"/"待补充"占位符 ❌禁止 turning_point ✓每个阶段必须有具体的 summary_safe

---

## Phase 2 · 锚点深读

**目标**：推书价值提取的核心。从 Phase 1 的 `deep_read_candidates` 中深读 highlight/controversy/relationship/character_intro 章节（≈10-15章），深读时可顺延前后1-2章取上下文。

**怎么读**：带着4组问题——

**卖点扫描**：这段哪里好看？对什么读者有效？边界是什么？
**争议扫描**：有什么争议情节？本质是什么（价值观/节奏/人物行为）？哪些读者被劝退？
**人物扫描**：核心特质？行为逻辑自洽否？故事功能？
**关系扫描**：核心张力？推进有具体锚点否？变化凭什么发生？

**产出1**：`anchor-pool.json`

```json
{
  "schema_version": "1.0",
  "metadata": { "title": "", "author": "" },
  "anchors": [
    {
      "anchor_id": "anc-001", "type": "strength",
      "title": "卖点标题（6-12字）",
      "judgement": "判断（1-2句）", "mechanism": "机制（1-2句）", "boundary": "边界（1句）",
      "chapter_id": "ch-0056", "spoiler_level": "safe", "evidence_ids": ["ev-0008"]
    },
    {
      "anchor_id": "anc-002", "type": "controversy",
      "title": "争议标题", "judgement": "判断", "mechanism": "机制", "boundary": "影响范围",
      "chapter_id": "ch-0079", "spoiler_level": "mild", "evidence_ids": ["ev-0012"]
    },
    {
      "anchor_id": "anc-003", "type": "character",
      "title": "角色名", "identity": "身份",
      "surface_traits": ["特质1"], "inner_drive": "驱动力", "relationship_function": "故事功能",
      "chapter_id": "ch-0001", "spoiler_level": "safe", "evidence_ids": ["ev-0001"]
    },
    {
      "anchor_id": "anc-004", "type": "relationship",
      "title": "关系标题", "formula": ["A驱动力", "B驱动力"],
      "dynamic": "关系动态", "progression_signal": "向前标志",
      "chapter_id": "ch-0045", "spoiler_level": "mild", "evidence_ids": ["ev-0008"]
    }
  ]
}
```

**type 枚举**：`strength` / `controversy` / `character` / `relationship` / `world`

**产出2**：`evidence-ledger.json`

```json
{
  "schema_version": "1.0",
  "metadata": { "title": "", "author": "" },
  "evidence": [
    { "evidence_id": "ev-0001", "chapter_id": "ch-0001", "anchor_id": "anc-003", "claim": "1句判断", "excerpt": "原文摘录50-200字", "spoiler_level": "safe" }
  ]
}
```

**spoiler_level**：`safe`(开局设定/公开特质) / `mild`(中期方向/关系趋势) / `major`(结局/反转/重大死亡，禁入推书卡)

**质量门控**：❌禁止无 evidence_ids 的anchor ❌excerpt不足50字 ❌spoiler缺失 ✓每个strength有boundary ✓每个controversy有影响范围

---

## Phase 3 · 阅感采样

**读什么**（5-8章）：全书均匀采样（如 ch-0010/0025/0040/0055/0070/0085/0100），与Phase1/2已读章不重复。

**量化指标**（1-10分）：

| 指标 | 1分 | 10分 |
|:--|:--|:--|
| pacing | 极慢热 | 快节奏 |
| plot_density | 无事发生 | 每章多转折 |
| relationship_density | 无关系戏 | 关系密集 |
| emotional_tone | 冷淡 | 温暖/燃 |
| prose | 干瘪 | 精致有画面感 |
| readability | 艰涩 | 流畅易读 |

**产出**：`reading-metrics.json`

```json
{
  "schema_version": "1.0",
  "metadata": { "title": "", "author": "" },
  "sampled_chapters": ["ch-0010", "ch-0025", "ch-0040", "ch-0055", "ch-0070", "ch-0085", "ch-0100"],
  "dimensions": { "characters": 8.0, "plot": 7.0, "prose": 8.0, "relationships": 8.0, "world": 7.0, "pacing": 6.5 },
  "reading_experience": {
    "style": "文风描述", "pacing_note": "节奏描述", "emotional_tone": "情绪描述", "readability": "可读性描述", "plot_density_note": "事件密度描述"
  },
  "warnings": ["避雷项1", "避雷项2"]
}
```

**质量门控**：❌所有维度打分相同 ❌warnings为空 ✓采样章≥5

---

## Step 1 完成检查

5个文件必须落盘到 `工作稿/`：
1. `chapter-index.json`
2. `structure-map.json`
3. `anchor-pool.json`
4. `evidence-ledger.json`
5. `reading-metrics.json`

全部就绪 → **读取 `steps/step2.md` 并执行 Step 2 评审生成。**

---

## 红线

1. **禁止逐章摘要**——必须用三阶段价值扫描，100章只精读30-40章
2. **所有判断绑定 evidence_id**——每条 strength/controversy/character 必须引用证据台账
3. **review.json 是唯一评审输出**——禁止生成 input+draft 两个重复JSON
4. **Step 文件链式加载**——Step1 内化在本文件直接执行；Step1完成后读取 `steps/step2.md`；Step2完成后读取 `steps/step3.md`

---

## 速查表

### 产出路径

| 产出 | 路径 | 产生阶段 |
|:--|:--|:--|
| chapter-index.json + structure-map.json | `工作稿/` | Step1-Phase1 |
| anchor-pool.json + evidence-ledger.json | `工作稿/` | Step1-Phase2 |
| reading-metrics.json | `工作稿/` | Step1-Phase3 |
| review.json | `工作稿/` | Step2 |
| {书名}-读者推书-v1.html + review.js | 项目根目录 | Step3 |

### 9页设计语言

| 页 | type | 设计范式 |
|:--|:--|:--|
| 1 | cover | Cinematic Poster 电影海报 |
| 2 | hook | Swiss Grid 瑞士极简 |
| 3 | synopsis | Magazine Editorial 杂志页 |
| 4 | characters | Profile Spread 人物特写 |
| 5 | chemistry | Infographic 信息图 |
| 6 | structure | Horizontal Timeline 时间线 |
| 7 | selling_points | Feature Showcase 黑底展示 |
| 8 | risks | Dashboard 仪表盘 |
| 9 | verdict | Back Cover 封底 |

### 文件结构

```
skills/pop-recommend/
├── SKILL.md                  ← 本文件（Step 1 内化）
├── steps/step2.md            ← Step 2 评审生成
├── steps/step3.md            ← Step 3 HTML渲染
├── templates/                ← JSON模板 + HTML模板
├── references/               ← page-layout-guide.md
├── skill.json + CHANGELOG.md
```

---

## 版本

v1.1.0 | 2026-07-20 | SKILL.md内化Step1完整方法论。串联SOP升级：SKILL.md(Step1内化)→steps/step2.md→steps/step3.md链式加载。解决Pop平台仅注入SKILL.md导致step文件缺失的加载问题 → CHANGELOG.md
