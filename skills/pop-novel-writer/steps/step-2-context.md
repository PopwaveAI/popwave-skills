# Step 2：上下文搜集（零 LLM）

> 职责：按 Director 的信息释放策略，从文件系统读取相关内容，组装为世界快照。
> 零 LLM 调用——纯文件 IO。

---

## 输入

Director 的设计说明中的信息释放策略

## 执行

按 Director 的信息释放策略，读取以下文件：

### 1. L1 设定

遍历 info_release 数组中的 source_doc 路径，逐一读取对应的 L1 设定文件。

例如 `info_release[0].source_doc: "01-写作资产/L1设定/力量体系.md"` → 读取该文件。

**注意**：
- 只读 Director 明确指定的 source_doc，不遍历整个 L1 目录
- 读取的是设定的原始文本，不做摘要或转换

### 2. 上一章结尾

读取上一章正文最后 800 字。路径：`{正文目录}/ch{上一章号}.md`

如果不存在（如 CH1 无上一章）→ 跳过

### 3. entity-state.yaml

读取 `design/entity-state.yaml`。

如果文件不存在 → 跳过，输出"首次启动，无历史状态"

### 4. global-summary.md

读取 `design/global-summary.md`，限 1500 字以内。

如果文件不存在 → 跳过，输出"首次启动，无全局摘要"

---

## 输出

世界快照（结构化 YAML，格式参考 `templates/entity-state-schema.md`）

```yaml
当前时间:
  日期/时间点: {从上一章或 global-summary 读取}
  经过时间: {从上一章结尾估算}
角色状态:
  {角色名}:
    status: {健康/受伤/昏迷/死亡}
    location: {位置}
    key_items: [{物品}]
全局环境:
  地点: {当前主要场景位置}
  天气/环境: {天气、光照等}
  当前威胁: {当前正在进行的危险/冲突}
未收伏笔:
  - {伏笔名} — {当前状态}
```

→ 进 Step 3
