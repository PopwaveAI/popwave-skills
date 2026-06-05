# Step 5：状态更新（零 LLM）

> 职责：从渲染器产出的状态更新块中解析，写入文件。
> 零 LLM 调用——纯文件 IO。

---

## 输入

渲染器（Step 4）输出的状态更新块中的结构化数据

## 执行

### 1. 追加到 global-summary.md

路径：`design/global-summary.md`

操作：
1. 在"追加记录"表中新增一行：`| ch{编号} | {summary} |`
2. 更新"全书进展"顶层字段：
   - 主角状态 → 从 entity_updates 读取
   - 最新事件 → 从 event_log 读取

格式参考：`prompt-templates/global-summary-schema.md`

### 2. 更新 entity-state.yaml

路径：`design/entity-state.yaml`

操作：按 entity_updates 逐条更新：

```yaml
{角色名}:
  status: {新状态}
  location: {新位置}
  key_items: [{关键物品}]
```

按 world_updates 更新全局字段：

```yaml
时间: {新时间点}
地点: {新地点}
状态: {全局状态变化}
```

### 3. 更新伏笔状态（如有）

- 如果 event_log 中有涉及伏笔回收的事件 → 在 global-summary.md 的"已收伏笔"表中追加
- 如果 event_log 中有涉及新伏笔设伏的事件 → 在"未收伏笔"表中追加

---

## 输出文件

- `design/global-summary.md` — 追加后
- `design/entity-state.yaml` — 更新后（如不存在则新建）

---

## 注意事项

- 如果状态更新块中的字段缺失 → 对应的更新跳过，不编造数据
- entity-state.yaml 第一行为 `# 自动维护，由 Step 5 生成`
- global-summary.md 保持总长度 ≤ 1500 字，如果超出则压缩旧行
