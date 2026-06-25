# state-log.yaml — 叙事状态日志模板

> 生产方式: plot Step 3 创建（baseline #0）→ prose 每章追加 event → expert-writer 定期压缩
> 存储: `状态/state-log.yaml`（唯一文件，append-only）
> 设计原则: agent 读它像读日记，写它像写日记。不定义字段 schema，用叙事表达状态。

## 文件结构

```yaml
version: 1
last_compacted_at: 0          # 最后一次压缩到的章号

entries:

  # ===== baseline（全量快照，定期压缩产出） =====
  - chapter: 0
    type: baseline
    author: plot              # plot | prose | compact
    content: |
      ## 弧线
      {卷名}·{幕名}（ch{起}-ch{终}）

      ## 角色
      {角色名}（{角色定位}）：
        {等级/修为}
        {位置}
        {心理状态一句话}
        {装备/物品}
        {关键关系}

      ## 伏笔
      [G-001] {伏笔描述} → ch{预期回收章}
      [G-002] {伏笔描述} → ch{预期回收章}

      ## 世界状态
      {世界大局一句话}
      {关键地点状态}

  # ===== event（每章追加，只写变化） =====
  - chapter: 1
    type: event
    author: prose
    content: |
      ## 事件
      {本章发生了什么（2-5句话）}

      ## 变化
      {角色名}：{什么变了}
      {新实体/物品/功法}：{状态}

      ## 伏笔
      [G-001] {伏笔状态变化}
      [新] {新种埋的伏笔}

  # ===== 压缩后的 baseline（每 10-20 章执行一次） =====
  # 旧 event 全部合并进新 baseline，然后删掉旧 event
  - chapter: 10
    type: baseline
    author: compact
    content: |
      ## 弧线
      {更新后的弧线位置}

      ## 角色
      {合并后的角色当前状态}

      ## 伏笔
      {合并后的伏笔状态（open/resolved）}
```

## 三种操作

### 读（chapter step-1 / expert-writer step-3）

读最后一个 `type: baseline` 条目 + 它之后的所有 `type: event` 条目。
通常 = 1 条 baseline（~30-50 行）+ 0-19 条 event（每条 ~5-10 行）= ~100-200 行。
agent 一目了然，不需要解析 YAML 字段。

### 写（prose 章末）

追加一条 `type: event`。只写本章的变化：
- **事件**：本章发生了什么（2-5 句话）
- **变化**：角色状态变化、新实体、装备变化
- **伏笔**：新种埋的、回收的、状态变化的

不写全量状态——全量在 baseline 里。

### 压缩（expert-writer step-3，每 10-20 章触发）

1. 读最后一个 baseline B + B 之后的所有 event
2. 合并成一条新 baseline（角色变化、伏笔状态、世界状态全部体现在叙事中）
3. 删掉 B 及 B 之后的所有 event
4. 追加新的 baseline
5. 更新 `last_compacted_at`

压缩后文件大小回到 ~5-10KB，不随章数膨胀。

## 回滚（零脚本，纯文本操作）

| 场景 | 操作 |
|------|------|
| 回滚到第 N 章 | 删掉 entries 中 chapter > N 的所有条目 |
| 回滚到 plot 完成 | 删掉 entries 中 chapter > 0 的所有条目（只留 baseline #0） |
| 回滚到 world | 删 state-log.yaml 整个文件 |
| 回滚到 creative | 删 状态/ 整个目录 |

回滚后如果最后一个 baseline 的 chapter > N，需要从更早的 baseline 重建。
实际操作：找到 chapter ≤ N 的最后一个 baseline，删掉它之后的所有条目。

## CH1 初始化（chapter step-1）

plot Step 3 已创建 baseline #0（仅含弧线+伏笔+世界状态，无角色状态）。
chapter CH1 step-1 读到 baseline #0 后：
1. 读取全部角色卡，提取初始状态
2. 将角色状态合并到 baseline #0 的 content 中（直接编辑该条目的 content）
3. 不需要创建新条目——baseline #0 就是 CH1 的 before 状态

## 大小估算

- baseline：~30-50 行（~2-3KB）
- 每章 event：~5-10 行（~300-500B）
- 压缩前最大（20 章）：~2KB + 20×400B = ~10KB
- 压缩后：~3KB
- 100 章历史（5 次压缩）：~3KB + 最多 20 条 event = ~10KB（稳定）
