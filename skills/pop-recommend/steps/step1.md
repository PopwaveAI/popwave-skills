# Step 1 · 三阶段价值扫描

> 从小说原文 → 5个JSON产出文件
> 核心原则：放弃逐章摘要，100章只精读30-40章，每个判断带原文证据+spoiler标注

---

## 前置：ETL精简版

读取小说 txt，做最小化预处理（不做逐章摘要）：

1. **编码归一化**：检测编码（GB18030/UTF-8），转为 UTF-8
2. **章节分割**：按 `第X章` 正则切分，生成 `chapter-index.json`（仅章号+章名+字符位置，无摘要）
3. **元数据提取**：书名、作者、平台、字数、完结状态

### chapter-index.json 结构

```json
{
  "schema_version": "1.0",
  "metadata": { "title": "", "author": "", "platform": "", "word_count": null, "status": "" },
  "chapters": [
    { "chapter_id": "ch-0001", "title": "第1章 前缘（一）", "char_start": 0, "char_end": 2400 }
  ]
}
```

**禁止生成 digests 文件**——逐章摘要是被废弃的方法，不要产出。

---

## Phase 1 · 骨架扫描

**目标**：快速建立全书骨架认知，识别 Phase 2 需要深读的节点。

**读什么**（≈15-20章）：
- 首章（建立开局基调）
- 每卷/每大段落的首章 + 末章（识别卷界和阶段转换）
- 全书尾章（识别结局状态）
- 如果无法识别卷界，按章数均分4-6段，取每段首尾

**怎么读**：每章读全文，带着以下问题：
1. 这本书的开局是什么类型？（穿越/重生/开局即危机/日常起步）
2. 主角是谁？核心驱动力是什么？
3. 这个阶段的故事在讲什么？（一句话，无剧透）
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
    {
      "segment_id": "seg-01",
      "title": "第一卷/第一阶段名称",
      "chapter_range": "ch-0001~ch-0026",
      "summary_safe": "无剧透的一句话阶段描述",
      "function": "这个阶段在全书中的功能（开局/升级/转折/高潮/收尾）"
    }
  ],
  "deep_read_candidates": [
    {
      "chapter_id": "ch-0001",
      "reason": "首章·建立世界观和主角",
      "scan_type": "character_intro"
    },
    {
      "chapter_id": "ch-0056",
      "reason": "疑似高光·感情线爆发",
      "scan_type": "highlight"
    }
  ]
}
```

**scan_type 枚举**（用于 Phase 2 分类）：
- `character_intro` — 人物出场/介绍
- `highlight` — 高光名场面
- `controversy` — 争议情节
- `relationship` — 关系转折
- `world_reveal` — 世界观揭秘
- `power_shift` — 力量格局变化

**质量门控**：
- ❌ 禁止输出"故事内容"/"待补充"等占位符
- ❌ 禁止输出 turning_point（剧透点）
- ✓ 每个阶段必须有具体的 summary_safe 和 function

---

## Phase 2 · 锚点深读

**目标**：这是推书价值提取的核心。从 Phase 1 识别的候选节点中深读，提取卖点/争议/人物/关系锚点。

**读什么**（≈10-15章）：
- Phase 1 的 `deep_read_candidates` 中标记为 `highlight`/`controversy`/`relationship`/`character_intro` 的章节
- 深读时可顺延阅读前后1-2章以获取上下文

**怎么读**：带着4组问题读：

### 第1组：卖点扫描
- 这段哪里好看？具体发生在什么场景？
- 这个卖点对什么类型的读者有效？
- 这个卖点的边界是什么？（什么读者会觉得没意思）

### 第2组：争议扫描
- 这段有什么可能引发争议的情节？
- 争议的本质是什么？（价值观/节奏/人物行为/结局处理）
- 哪些读者会被劝退？

### 第3组：人物扫描
- 这个角色的核心特质是什么？
- 行为逻辑是否自洽？驱动力是什么？
- 在故事中的功能是什么？

### 第4组：关系扫描
- 这组关系的核心张力是什么？
- 关系推进有没有具体锚点？
- 关系变化是凭什么发生的？

**产出1**：`anchor-pool.json`

```json
{
  "schema_version": "1.0",
  "metadata": { "title": "", "author": "" },
  "anchors": [
    {
      "anchor_id": "anc-001",
      "type": "strength",
      "title": "卖点标题（6-12字）",
      "judgement": "判断（1-2句，为什么这是卖点）",
      "mechanism": "机制（1-2句，具体怎么实现的）",
      "boundary": "边界（1句，什么读者不买账）",
      "chapter_id": "ch-0056",
      "spoiler_level": "safe",
      "evidence_ids": ["ev-0008"]
    },
    {
      "anchor_id": "anc-002",
      "type": "controversy",
      "title": "争议标题",
      "judgement": "判断",
      "mechanism": "机制",
      "boundary": "影响范围",
      "chapter_id": "ch-0079",
      "spoiler_level": "mild",
      "evidence_ids": ["ev-0012"]
    },
    {
      "anchor_id": "anc-003",
      "type": "character",
      "title": "角色名",
      "identity": "身份",
      "surface_traits": ["特质1", "特质2"],
      "inner_drive": "内在驱动力",
      "relationship_function": "在故事中的功能",
      "chapter_id": "ch-0001",
      "spoiler_level": "safe",
      "evidence_ids": ["ev-0001"]
    },
    {
      "anchor_id": "anc-004",
      "type": "relationship",
      "title": "关系标题",
      "formula": ["A的驱动力", "B的驱动力"],
      "dynamic": "关系动态描述",
      "progression_signal": "关系向前的标志是什么",
      "chapter_id": "ch-0045",
      "spoiler_level": "mild",
      "evidence_ids": ["ev-0008", "ev-0012"]
    }
  ]
}
```

**anchor type 枚举**：`strength` / `controversy` / `character` / `relationship` / `world`

**产出2**：`evidence-ledger.json`

```json
{
  "schema_version": "1.0",
  "metadata": { "title": "", "author": "" },
  "evidence": [
    {
      "evidence_id": "ev-0001",
      "chapter_id": "ch-0001",
      "anchor_id": "anc-003",
      "claim": "证据对应的判断（1句）",
      "excerpt": "原文摘录（50-200字，足以支撑判断）",
      "spoiler_level": "safe"
    }
  ]
}
```

**spoiler_level 标注规则**：
- `safe`：只涉及开局设定、角色公开特质、公知信息 → 推书卡全部页面可用
- `mild`：涉及中期发展方向、关系变化趋势 → 模糊化后可用
- `major`：涉及结局、核心反转、重大死亡 → 禁止出现在推书卡

**质量门控**：
- ❌ 禁止无 evidence_ids 的 anchor
- ❌ 禁止 excerpt 为空或不足50字的证据
- ❌ 禁止 spoiler_level 缺失
- ✓ 每个 strength 必须有 boundary
- ✓ 每个 controversy 必须说明影响范围

---

## Phase 3 · 阅感采样

**目标**：量化阅读体验指标，为避雷雷达图提供数据。

**读什么**（5-8章）：
- 全书均匀采样（如100章取第10/25/40/55/70/85/100章）
- 可与 Phase 1/2 重叠（已读的章不重复读）

**怎么读**：每章读全文，量化以下指标（1-10分）：

| 指标 | 1分 | 10分 | 说明 |
|:--|:--|:--|:--|
| pacing | 极慢热/极拖沓 | 快节奏/紧凑 | 剧情推进速度 |
| plot_density | 几乎无事发生 | 每章多个转折 | 单章事件密度 |
| relationship_density | 几乎无关系戏 | 关系戏密集 | 人物互动频率 |
| emotional_tone | 冷淡/压抑 | 温暖/燃 | 情绪基调 |
| prose | 干瘪/流水账 | 精致/有画面感 | 文风质量 |
| readability | 艰涩/需反复读 | 流畅易读 | 阅读门槛 |

**产出**：`reading-metrics.json`

```json
{
  "schema_version": "1.0",
  "metadata": { "title": "", "author": "" },
  "sampled_chapters": ["ch-0010", "ch-0025", "ch-0040", "ch-0055", "ch-0070", "ch-0085", "ch-0100"],
  "dimensions": {
    "characters": 8.0,
    "plot": 7.0,
    "prose": 8.0,
    "relationships": 8.0,
    "world": 7.0,
    "pacing": 6.5
  },
  "reading_experience": {
    "style": "文风描述（1句）",
    "pacing_note": "节奏描述（1句）",
    "emotional_tone": "情绪基调描述（1句）",
    "readability": "可读性描述（1句）",
    "plot_density_note": "事件密度描述（1句）"
  },
  "warnings": [
    "避雷项1（如：男主在感情中反复摇摆）",
    "避雷项2（如：前20章事件密度极低）"
  ]
}
```

**质量门控**：
- ❌ 禁止所有维度打分相同（说明没有真正区分）
- ❌ 禁止 warnings 为空（每本书都有劝退点）
- ✓ 采样章数 ≥5

---

## 完成检查

Phase 1-3 全部完成后，确认以下5个文件已落盘到 `工作稿/` 目录：

1. `chapter-index.json` — 章节索引（ETL产出）
2. `structure-map.json` — 骨架地图（Phase 1产出）
3. `anchor-pool.json` — 锚点池（Phase 2产出）
4. `evidence-ledger.json` — 证据台账（Phase 2产出）
5. `reading-metrics.json` — 阅感指标（Phase 3产出）

全部就绪后，进入 Step 2 评审生成。
