# Step 2：验证 + 输出

> 管线: pop-writer-prose v3.6

## 目的

验证正文质量 → 通过则输出，不通过则退回 Step 1。

## 验证

### 风格验证

对照文风DNA原文，逐段检查：

| 维度 | 检查 |
|:-----|:-----|
| 叙事者距离 | DNA 说紧贴感官 → 正文有「他心想」？ |
| 句式节奏 | DNA 战斗全短句 → 正文用了长排比？ |
| 对话方式 | DNA 无引导词 → 正文写了「他笑着说道」？ |

偏差 ≥ 2 处 → ❌ 退回 Step 1。

### 宪法检查

- [ ] 无 AI 观感词（他感到/他意识到/他仿佛）
- [ ] 无解说员句式（不是…而是… ≥ 2 次 → 退回）
- [ ] 骨架事件全部对应
- [ ] 叙事者不解释设定
- [ ] 视角一致（不跳跃、限知不写非锚点内心）
- [ ] 🔒 对白已嵌入
- [ ] 调味空间被遵守

### 文本脉冲检查

逐 500 字块扫描：每个块至少一次期待推翻或感官锐化。连续 > 500 字无微脉冲 → 退回最平淡段落补。

### 字数检查

| 偏差 | 处理 |
|:-----|:-----|
| ≤ 20% | ✅ 通过 |
| > 20% ≤ 50% | ⚠️ 提示 |
| > 50% | ❌ 退回 Step 1 |

---

## 输出（验证通过后）

写入 `正文/chXXX.md`：

```markdown
# chXXX · {本章标题}

{正文全文}
```

> ★ 状态由 pop-state-engine 维护——prose 章末调用 CLI 登记到引擎。chapter 从设计包的 after 状态更新 `状态/entity-snapshot.yaml`（双写过渡期并行）。

## 引擎登记（验证通过 + 落盘后）

正文写入 `正文/chXXX.md` 后，执行以下 5 步将本章叙事状态登记到 pop-state-engine：

### 步骤 1：设计包入库

```bash
python {engine_scripts}/command_executor.py -p {项目路径} -a store-chapter -j '{
  "chapter": {N},
  "content": "{设计包全文}",
  "tags": "{设计包tags}",
  "location": "{场景地点}",
  "characters": "{登场人物逗号分隔}",
  "mood": "{情绪基调}",
  "events": "{事件链逗号分隔}"
}'
```

### 步骤 2：agent 标注新实体和状态变化

阅读本章设计包，标注：
- 本章首次出现的实体（角色/地点/物品/功法/概念）
- 本章发生的状态变化（修为提升/关系变化/位置移动/获得物品）

### 步骤 3：脚本辅助验证

```bash
python {engine_scripts}/command_executor.py -p {项目路径} -a extract-entities -j '{
  "text": "{设计包全文}"
}'
```

将脚本提取结果与步骤 2 的 agent 标注对比。以 agent 标注为准，脚本结果作为查漏补缺。

### 步骤 4：写入新实体和状态变化

对每个确认的新实体：
```bash
python {engine_scripts}/command_executor.py -p {项目路径} -a add-node -j '{
  "id": "{实体ID}",
  "type": "{character|location|item|skill|concept}",
  "name": "{实体名}",
  "tags": "{标签}",
  "properties": "{}"
}'
```

对每个状态变化：
```bash
python {engine_scripts}/command_executor.py -p {项目路径} -a set-fact -j '{
  "entity": "{实体名}",
  "attribute": "{属性名}",
  "value": "{新值}",
  "chapter": {N},
  "importance": "{permanent|arc-scoped|chapter-scoped}"
}'
```

主角状态汇总写入 `_meta/protagonist_state`：
```bash
python {engine_scripts}/command_executor.py -p {项目路径} -a set-fact -j '{
  "entity": "_meta",
  "attribute": "protagonist_state",
  "value": "{修为}·{关键状态}·{当前位置}",
  "chapter": {N},
  "importance": "permanent"
}'
```

### 步骤 5：伏笔回收检测

```bash
python {engine_scripts}/command_executor.py -p {项目路径} -a list-hooks -j '{}'
```

检查本章是否回收了某个伏笔。若回收，执行：
```bash
python {engine_scripts}/command_executor.py -p {项目路径} -a resolve-hook -j '{
  "id": "{伏笔ID}",
  "resolution": "{回收方式简述}",
  "resolved_chapter": {N}
}'
```

## 产出自检

- [ ] 字数偏差 ≤ 20%
- [ ] 无 AI 观感词
- [ ] 🔒 对白已嵌入

---
⛔ 本 step 完成，交接给下游 skill。确认质量自检通过后再交接。
