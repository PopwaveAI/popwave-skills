# Step3：子agent创作 — context manifest组装 → create涌现 → revise重写

> **执行者**：子agent（create + revise），主会话调度
> **输入**：导演意图 + 状态快照 + 设定文件 + info_acquired + 文风DNA
> **产出**：初稿（create）→ 重写稿（revise）+ 两个receipt
> **人工check**：**【CHECK 2】用户验收** → 验收后才进Step4
> **红线**：❌2 不读子SKILL.md就路由 | ❌5 子agent失败降级时必须重读完整context+文风DNA完整加载+独立质检

---

## ❌ 读取协议（强制）

```
工具选择：skill_view（首选）或 Get-Content -Encoding UTF8 -Raw
❌ 禁止用 Read 工具读取 skill 文件（有行数限制，会截断）
✅ 路由到create/revise子agent前，必须先 Get-Content -Encoding UTF8 -Raw 目标子skill完整SKILL.md（红线2）
```

---

## 概述

Step3 调度两个子agent（create→revise），作为 **一次"创作调度"**：
- create阶段：注入导演意图+状态快照+上章末尾+设定文件+info_acquired → 产出初稿+receipt
- revise阶段：注入初稿+文风DNA+要素切片+导演意图验证清单 → 产出重写稿+receipt
- 两阶段自动连贯，中间不暂停

---

## 1. create阶段：涌现写作

### 1.1 读取子skill SKILL.md（红线2）

```powershell
Get-Content -Encoding UTF8 -Raw '{pop-writer-v3-create路径}/SKILL.md'
```

> 不读子 SKILL.md 就路由 = 红线2违规。

### 1.2 组装 context manifest

> context manifest 是子agent的完整上下文清单。白盒机制：主会话知道注入了什么，子agent知道收到了什么。

```yaml
context_manifest:
  manifest_version: "1.0"
  stage: create
  chapter: 3

  # 注入项清单
  items:
    - id: director_intent
      type: yaml
      source: "Step0产出"
      size: 350
      description: "导演意图（含三问+settings_ref）"

    - id: state_snapshot
      type: yaml
      source: "Step1产出"
      size: 380
      description: "状态快照（protagonist+pressures+pending）"

    - id: prev_chapter_tail
      type: text
      source: "正文/ch002.md末尾500-800字"
      size: 650
      description: "上章末尾（衔接用）"

    - id: settings_gold_finger
      type: text
      source: "写作参考/设定/金手指.md"
      size: 2048
      description: "金手指设定（升级机制）"

    - id: settings_protagonist
      type: text
      source: "写作参考/设定/主角引擎.md"
      size: 1536
      description: "主角引擎设定（行为准则）"

    - id: info_acquired
      type: yaml
      source: "Step2产出"
      size: 500
      description: "信息获取汇总（library+research结果）"

  # create阶段硬约束
  constraints:
    - "回答导演意图三问（info/pressure/hook）"
    - "按event_chain顺序推进事件"
    - "遵循emotion_curve和pacing"
    - "章末必须留chapter_hook"
    - "产出receipt（记录实际读取了哪些context项）"
```

### 1.3 调度 create 子agent

1. 将 context manifest 完整注入 pop-writer-v3-create 子agent
2. 子agent执行涌现写作
3. 子agent产出：
   - 初稿正文（`正文/ch003.md` 草稿）
   - create receipt（记录实际读取了哪些context项，status=full/partial）

### 1.4 create receipt 格式

```yaml
create_receipt:
  stage: create
  chapter: 3
  manifest_items_received: 6
  items_read:
    - id: director_intent
      status: full           # full=完整读取
      actual_read: 350       # 实际读取字数
    - id: state_snapshot
      status: full
      actual_read: 380
    - id: prev_chapter_tail
      status: full
      actual_read: 650
    - id: settings_gold_finger
      status: full
      actual_read: 2048
    - id: settings_protagonist
      status: full
      actual_read: 1536
    - id: info_acquired
      status: full
      actual_read: 500
  key_elements_confirmed:     # 关键元素确认
    - "导演意图三问全部回答"
    - "event_chain全部推进"
    - "chapter_hook已留"
  three_questions_confirmed:  # 三问确认
    info: true
    pressure: true
    hook: true
  status: full
```

---

## 2. revise阶段：完全重写

### 2.1 读取子skill SKILL.md（红线2）

```powershell
Get-Content -Encoding UTF8 -Raw '{pop-writer-v3-revise路径}/SKILL.md'
```

### 2.2 组装 revise context manifest

```yaml
context_manifest:
  manifest_version: "1.0"
  stage: revise
  chapter: 3

  items:
    - id: create_draft
      type: text
      source: "create阶段产出的初稿"
      size: 3500
      description: "create初稿全文"

    - id: style_dna
      type: text
      source: "写作资产/文风库/{书名}.md"
      size: 4096
      description: "文风DNA档案（精确匹配目标）"

    - id: element_slices
      type: yaml
      source: "导演意图sublines_advance + 状态快照pending"
      size: 200
      description: "要素切片（子线+伏笔+承诺+揭示）"

    - id: director_intent_checklist
      type: yaml
      source: "Step0导演意图three_questions"
      size: 100
      description: "导演意图验证清单"

  constraints:
    - "文风DNA精确匹配（0误差）"
    - "导演意图5项验证全部通过"
    - "完全重写（不是微调）"
    - "保留create初稿的事件链和情节骨架"
    - "产出receipt"
```

### 2.3 调度 revise 子agent

1. 将 revise context manifest 完整注入 pop-writer-v3-revise 子agent
2. 子agent执行完全重写
3. 子agent产出：
   - 重写稿正文（最终版 `正文/ch003.md`）
   - revise receipt

### 2.4 revise receipt 格式

```yaml
revise_receipt:
  stage: revise
  chapter: 3
  manifest_items_received: 4
  items_read:
    - id: create_draft
      status: full
      actual_read: 3500
    - id: style_dna
      status: full
      actual_read: 4096
    - id: element_slices
      status: full
      actual_read: 200
    - id: director_intent_checklist
      status: full
      actual_read: 100
  style_dna_match:
    status: full              # full=精确匹配（0误差）
    deviations: 0             # 偏差数量
  director_intent_verification:  # 导演意图5项验证
    - item: "narrative_function已体现"
      passed: true
    - item: "event_chain完整推进"
      passed: true
    - item: "emotion_curve已遵循"
      passed: true
    - item: "chapter_hook已留"
      passed: true
    - item: "three_questions全部回答"
      passed: true
  status: full
```

---

## 3. 【CHECK 2】用户验收

> 重写稿交付用户验收。验收后才进Step4。

1. 将重写稿正文交付用户
2. 用引导语：
   > 第{chapter}章重写稿已完成。
   > 文风DNA匹配：{deviations}偏差。
   > 导演意图验证：{通过数}/5项通过。
   > 请验收正文。验收后进入receipt检查。
3. 等待用户验收
   - 用户验收 → 进入 Step4（receipt检查）
   - 用户要求修改 → 反馈给revise子agent重做 → 重新验收
   - 用户拒绝 → 暂停，等待用户指示

---

## 4. 降级策略（红线5）

> 子agent失败降级时必须：重读完整context + 文风DNA完整加载 + 独立质检

### 降级触发条件
- 子agent调用失败（超时/错误/产出格式不符）
- receipt检查连续2次同一项不通过（Step4判断）

### 降级策略B：主会话直接执行

1. 标注 `degraded_master_execution: true`
2. **重读完整context**：
   - 导演意图 + 状态快照 + 设定文件 + info_acquired + 文风DNA
   - 全部 `Get-Content -Raw` 完整加载（不截断）
3. **文风DNA完整加载**：
   - `Get-Content -Encoding UTF8 -Raw` 读取 `写作资产/文风库/{书名}.md`
   - 确认完整加载（不限制行数）
4. **独立质检**：
   - 主会话完成create后，自检导演意图三问
   - 主会话完成revise后，自检文风DNA精确匹配
5. 降级≠跳过门禁：receipt仍然必须产出，Step4仍然必须检查

---

## 5. 完成条件

- [x] create子agent SKILL.md已读取（红线2）
- [x] context manifest已组装（create）
- [x] create子agent已执行，初稿+receipt已产出
- [x] revise子agent SKILL.md已读取（红线2）
- [x] context manifest已组装（revise）
- [x] revise子agent已执行，重写稿+receipt已产出
- [x] 重写稿已交付用户验收（CHECK 2）
- [x] 用户已验收 → 进入 Step4
