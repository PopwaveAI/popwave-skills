# Step 2 · 评审生成

> 消费 Step 1 的5个JSON → 合成 review.json（唯一评审输出文件）
> 核心原则：每个判断绑定 evidence_id，只消费 safe+mild 级别锚点

---

## 输入

读取 `工作稿/` 目录下的5个文件：

1. `chapter-index.json` — 章节索引（提供章号映射）
2. `structure-map.json` — 骨架地图（定位+结构+候选节点）
3. `anchor-pool.json` — 锚点池（卖点+争议+人物+关系）
4. `evidence-ledger.json` — 证据台账（原文摘录）
5. `reading-metrics.json` — 阅感指标（量化评分+避雷项）

---

## 合成逻辑

### 1. positioning（定位）

直接从 `structure-map.json` 的 `positioning` 字段提取：
- `one_liner` → 一句话定位
- `core_hook` → 核心钩子
- `tags` → 标签

### 2. synopsis（无剧透梗概）

基于 `structure-map.json` 的 `structure` 数组，合成3-4句话的无剧透梗概：
- 只使用 `summary_safe` 字段
- 只使用 `safe` 级别信息
- 禁止使用任何 `mild` 或 `major` 级别内容
- 梗概要讲清"故事方向"，不讲"发生了什么"

### 3. strengths（卖点）

从 `anchor-pool.json` 筛选 `type: "strength"` 的锚点：
- 只纳入 `spoiler_level` 为 `safe` 或 `mild` 的锚点
- 每个 strength 必须保留 `evidence_ids`
- 对 `mild` 级别的 strength，judgement 和 mechanism 需做模糊化处理（去掉具体情节，保留趋势描述）

### 4. characters（人物）

从 `anchor-pool.json` 筛选 `type: "character"` 的锚点：
- 只纳入 `spoiler_level` 为 `safe` 或 `mild` 的锚点
- 保留 surface_traits / inner_drive / relationship_function
- 对 `mild` 级别的人物，inner_drive 需做模糊化处理

### 5. world（世界）

从 `anchor-pool.json` 筛选 `type: "world"` 的锚点 + `structure-map.json` 的结构信息：
- 复杂度评级（low/medium/high）
- 核心规则（safe级别）
- 卷/阶段结构（从 structure-map 提取）

### 6. reading_experience（阅感）

直接从 `reading-metrics.json` 的 `reading_experience` 字段提取。

### 7. controversies（争议）

从 `anchor-pool.json` 筛选 `type: "controversy"` 的锚点：
- 只纳入 `spoiler_level` 为 `safe` 或 `mild` 的锚点
- 每个 controversy 必须保留 `evidence_ids`
- 对 `mild` 级别的 controversy，mechanism 需做模糊化处理

### 8. audience（受众）

基于 strengths + controversies + reading_metrics 综合判断：
- `recommended`：推荐给什么读者（3-4条）
- `avoid`：不推荐给什么读者（3-4条）
- 每条必须是具体读者画像，禁止泛泛的"喜欢XX的读者"

### 9. scoring（评分）

从 `reading-metrics.json` 的 `dimensions` 字段提取6维评分：
- characters / plot / prose / relationships / world / pacing
- 计算 base_score（6维均值）
- 计算 audience_bonus（如果 strengths ≥3 且 controversies ≤2，+1.0）

### 10. recommendation（推荐结论）

基于以上所有字段综合生成：
- `score_low` / `score_high`：评分区间（base_score-1.5 到 base_score+audience_bonus）
- `stars_low` / `stars_high`：星级区间（score/2）
- `grade`：等级（干草/粮草/粮草+/仙草-/仙草）
- `verdict`：一句话结论（为什么这个评分区间）
- `why_try`：为什么值得试读（1段话，面向犹豫的读者）

### 11. completion_note（完结说明）

从 `chapter-index.json` 的 metadata 提取完结状态：
- 如果 status 为 partial，必须注明"仅评价已有内容，对结局不做判断"

---

## 产出

`review.json` — 唯一评审输出文件

```json
{
  "schema_version": "1.0",
  "metadata": {
    "title": "",
    "author": "",
    "platform": "",
    "word_count": null,
    "status": ""
  },
  "positioning": {
    "one_liner": "",
    "core_hook": "",
    "tags": []
  },
  "synopsis": "无剧透梗概（3-4句）",
  "strengths": [
    {
      "title": "",
      "judgement": "",
      "mechanism": "",
      "boundary": "",
      "evidence_ids": []
    }
  ],
  "characters": [
    {
      "name": "",
      "identity": "",
      "surface_traits": [],
      "inner_drive": "",
      "relationship_function": "",
      "evidence_ids": []
    }
  ],
  "world": {
    "complexity": "medium",
    "rules": [],
    "structure": []
  },
  "reading_experience": {
    "style": "",
    "pacing_note": "",
    "emotional_tone": "",
    "readability": "",
    "plot_density_note": ""
  },
  "controversies": [
    {
      "title": "",
      "judgement": "",
      "mechanism": "",
      "boundary": "",
      "evidence_ids": []
    }
  ],
  "audience": {
    "recommended": [],
    "avoid": []
  },
  "scoring": {
    "dimensions": {
      "characters": 0,
      "plot": 0,
      "prose": 0,
      "relationships": 0,
      "world": 0,
      "pacing": 0
    },
    "base_score": 0,
    "audience_bonus": 0
  },
  "recommendation": {
    "score_low": 0,
    "score_high": 0,
    "stars_low": 0,
    "stars_high": 0,
    "grade": "",
    "verdict": "",
    "why_try": ""
  },
  "completion_note": ""
}
```

---

## 质量门控

- ❌ 禁止生成第二个 JSON 文件（review.json 是唯一输出）
- ❌ 禁止使用 `major` 级别的锚点或证据
- ❌ 禁止无 evidence_ids 的 strength/controversy
- ❌ 禁止 audience 字段出现泛泛描述（如"喜欢修仙的读者"）
- ✓ synopsis 必须 ≤4 句话且无剧透
- ✓ 所有 mild 级别内容必须经过模糊化处理
- ✓ completion_note 必须说明完结状态

---

## 完成检查

`review.json` 落盘后，进入 Step 3 HTML渲染。
