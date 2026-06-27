# Step3：子agent创作 — context manifest组装 → create涌现 → revise重写

> **执行者**：子agent（create + revise），主会话调度
> **输入**：导演意图 + 状态快照 + L2卡全文 + 设定文件全文 + info_acquired + 文风DNA全文 + create初稿全文
> **产出**：初稿（create）→ 重写稿（revise）+ 两个receipt
> **人工check**：**【CHECK 2】用户验收** → 验收后才进Step4
> **红线**：❌2 不读子SKILL.md就路由 | ❌5 子agent失败降级时必须重读完整context+文风DNA完整加载+独立质检 | ❌8 禁止摘要注入子agent（全文注入铁律）

---

## ❌ 读取协议（强制）

```
工具选择：skill_view（首选）或 Get-Content -Encoding UTF8 -Raw
❌ 禁止用 Read 工具读取 skill 文件（有行数限制，会截断）
✅ 路由到create/revise子agent前，必须先 Get-Content -Encoding UTF8 -Raw 目标子skill完整SKILL.md（红线2）
```

---

## ⚠️ 全文注入铁律（红线❌8，v9.7新增）

**主agent禁止摘要信息给子agent。所有文件类注入项必须全文注入。**

组装manifest时，对每个文件类注入项：
1. 用 `Get-Content -Encoding UTF8 -Raw` 读取文件全文
2. 将全文写入manifest的payload字段
3. size字段记录实际字节数
4. **禁止**只提取"关键部分"或"核心规则"注入

这适用于：L2卡、设定文件、文风DNA、create初稿。

---

## 概述

Step3 调度两个子agent（create→revise），作为 **一次"创作调度"**：
- create阶段：注入导演意图+状态快照+L2卡全文+上章末尾+设定文件全文+info_acquired+文风DNA全文（仅参考） → 产出初稿+receipt
- revise阶段：注入初稿全文+文风DNA全文+L2卡嵌套子线全文+导演意图验证清单 → 产出重写稿+receipt
- 两阶段自动连贯，中间不暂停

---

## 1. create阶段：涌现写作

### 1.1 读取子skill SKILL.md（红线2）

```powershell
Get-Content -Encoding UTF8 -Raw '{pop-writer-v3-create路径}/SKILL.md'
```

> 不读子 SKILL.md 就路由 = 红线2违规。

### 1.2 组装 context manifest（全文注入）

> context manifest 是子agent的完整上下文清单。白盒机制：主会话知道注入了什么，子agent知道收到了什么。

```yaml
context_manifest:
  manifest_version: "1.1"     # v9.7 全文注入
  stage: create
  chapter: 3

  # 注入项清单（全文注入，禁止摘要）
  items:
    - id: director_intent
      type: yaml
      source: "Step0产出"
      size: 400
      description: "导演意图（含五问+settings_ref+worldview_delivery）"
      injection: full              # full=全文注入

    - id: state_snapshot
      type: yaml
      source: "Step1产出"
      size: 380
      description: "状态快照（protagonist+pressures+pending）"
      injection: full

    - id: l2_card_full             # v9.7新增：L2卡全文注入
      type: text
      source: "卷纲/L2-001-名称.md"
      read_method: "Get-Content -Encoding UTF8 -Raw"
      size: 14000
      description: "L2卡全文（唯一运行时活文档，子agent从中提取本章行）"
      injection: full              # 禁止摘要！L2卡替代种子文档，必须全文

    - id: prev_chapter_tail
      type: text
      source: "正文/ch002.md末尾500-800字"
      size: 650
      description: "上章末尾（衔接用）"
      injection: full

    - id: settings_gold_finger
      type: text
      source: "写作参考/设定/金手指.md"
      read_method: "Get-Content -Encoding UTF8 -Raw"
      size: 22000
      description: "金手指设定全文"
      injection: full              # 禁止摘要！

    - id: settings_protagonist
      type: text
      source: "写作参考/设定/主角引擎.md"
      read_method: "Get-Content -Encoding UTF8 -Raw"
      size: 5000
      description: "主角引擎设定全文"
      injection: full              # 禁止摘要！

    - id: style_dna_reference      # v9.7新增：文风DNA全文（仅参考）
      type: text
      source: "写作资产/文风库/{书名}.md"
      read_method: "Get-Content -Encoding UTF8 -Raw"
      size: 12000
      description: "文风DNA全文（仅参考不强制对齐，文风硬阻塞在revise）"
      injection: full              # 禁止摘要！文风DNA包含原文证据

    - id: info_acquired
      type: yaml
      source: "Step2产出"
      size: 500
      description: "信息获取汇总（library+research结果）"
      injection: full

  # create阶段硬约束
  constraints:
    - "回答导演意图五问（info/pressure/hook/worldview/clarity）"
    - "按event_chain顺序推进事件"
    - "遵循emotion_curve和pacing"
    - "章末必须留chapter_hook"
    - "worldview_delivery必须通过正文传递"
    - "产出receipt（记录实际读取了哪些context项）"
```

### 1.3 调度 create 子agent

1. 将 context manifest 完整注入 pop-writer-v3-create 子agent（**每项都是全文，不是摘要**）
2. 子agent执行涌现写作
3. 子agent产出：
   - 初稿正文（`正文/ch003.md` 草稿）
   - create receipt（记录实际读取了哪些context项，status=full/partial）

### 1.4 create receipt 格式

```yaml
create_receipt:
  stage: create
  chapter: 3
  manifest_items_received: 8
  items_read:
    - id: director_intent
      status: full           # full=完整读取
      actual_read: 400       # 实际读取字数
      injection_verified: full  # v9.7: 确认收到的是全文不是摘要
    - id: state_snapshot
      status: full
      actual_read: 380
      injection_verified: full
    - id: l2_card_full
      status: full
      actual_read: 14000
      injection_verified: full
    - id: prev_chapter_tail
      status: full
      actual_read: 650
      injection_verified: full
    - id: settings_gold_finger
      status: full
      actual_read: 22000
      injection_verified: full
    - id: settings_protagonist
      status: full
      actual_read: 5000
      injection_verified: full
    - id: style_dna_reference
      status: full
      actual_read: 12000
      injection_verified: full
    - id: info_acquired
      status: full
      actual_read: 500
      injection_verified: full
  key_elements_confirmed:     # 关键元素确认
    - "导演意图五问全部回答"
    - "event_chain全部推进"
    - "chapter_hook已留"
    - "worldview_delivery已传递"
  five_questions_confirmed:   # v9.6: 五问确认
    info: true
    pressure: true
    hook: true
    worldview: true
    clarity: true
  status: full
```

---

## 2. revise阶段：完全重写

### 2.1 读取子skill SKILL.md（红线2）

```powershell
Get-Content -Encoding UTF8 -Raw '{pop-writer-v3-revise路径}/SKILL.md'
```

### 2.2 组装 revise context manifest（全文注入）

```yaml
context_manifest:
  manifest_version: "1.1"     # v9.7 全文注入
  stage: revise
  chapter: 3

  items:
    - id: create_draft
      type: text
      source: "create阶段产出的初稿"
      size: 3500
      description: "create初稿全文"
      injection: full              # 禁止摘要！revise基于完整初稿重写

    - id: style_dna
      type: text
      source: "写作资产/文风库/{书名}.md"
      read_method: "Get-Content -Encoding UTF8 -Raw"
      size: 12000
      description: "文风DNA全文（含原文证据）"
      injection: full              # 禁止摘要！文风DNA的原文片段是理解风格的关键

    - id: l2_sublines             # v9.7新增：L2卡嵌套子线全文
      type: text
      source: "卷纲/L2-001-名称.md#嵌套子线"
      read_method: "Get-Content -Encoding UTF8 -Raw（提取嵌套子线段）"
      size: 3000
      description: "L2卡嵌套子线全文（子线+伏笔+承诺+揭示）"
      injection: full              # 禁止摘要！

    - id: director_intent_checklist
      type: yaml
      source: "Step0导演意图五问"
      size: 150
      description: "导演意图验证清单（6项验证标准）"
      injection: full

  constraints:
    - "文风DNA精确匹配（0误差）"
    - "导演意图6项验证全部通过（含世界观传递验证）"
    - "完全重写（不是微调）"
    - "保留create初稿的事件链和情节骨架"
    - "产出receipt"
```

### 2.3 调度 revise 子agent

1. 将 revise context manifest 完整注入 pop-writer-v3-revise 子agent（**每项都是全文，不是摘要**）
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
      injection_verified: full     # v9.7: 确认收到全文
    - id: style_dna
      status: full
      actual_read: 12000
      injection_verified: full     # 确认收到全文不是摘要
    - id: l2_sublines
      status: full
      actual_read: 3000
      injection_verified: full
    - id: director_intent_checklist
      status: full
      actual_read: 150
      injection_verified: full
  style_dna_match:
    status: full              # full=精确匹配（0误差）
    deviations: 0             # 偏差数量
  director_intent_verification:  # 导演意图6项验证（v9.6从5项扩展）
    - item: "narrative_function已体现"
      passed: true
    - item: "event_chain完整推进"
      passed: true
    - item: "emotion_curve已遵循"
      passed: true
    - item: "sublines_advance全部推进"
      passed: true
    - item: "chapter_hook已留"
      passed: true
    - item: "worldview_delivery已传递"   # v9.6新增
      passed: true
  injection_verified: full        # v9.7: 全部注入项确认收到全文
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
