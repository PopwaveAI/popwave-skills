# Step 2：锁定种子并落盘

> 触发：step-1 推荐方案经用户确认后进入。
> 目标：锁定种子，落盘 `涌现/seed-种子文档.md`，并首版正式落盘 `涌现/soul.md`。

## 前置确认

- step-1 已完成，用户已确认推荐方案。
- execution.mode 判定（引用 PRD §4.5）：
  - formal：核心承诺、主卖点、禁区、待 research 问题齐全。
  - draft：有缺口但可补全继续，产出标记 draft，落盘。
  - trial：不落盘，仅对话内。本步骤落盘必须达 formal 或 draft。

## 执行步骤

### 1. 锁定种子文档

参照 `templates/seed-doc.tpl.md` 空模板，填充：
- 元数据块（doc_type: seed, read_policy: full-if-targeted, primary_consumer: review）。
- execution.mode。
- 一句话主卖点（主角如何主动）。
- 核心承诺（元爽点/读者追读理由/主角主动方式/爽点外显方式/世界如何逼主角行动/题材承诺）。
- 候选 PK 表。
- 推荐方案（推荐/理由/吸收的败者强点/淘汰项）。
- 故事内容（主角/核心冲突/起点状态/终点方向/阶段性推进）。
- 核心情节线（主线推进/伏笔债务/阶段性目标）。
- 题材机制待 research。
- 不可牺牲项。
- 禁区。

落盘指令：写入 `涌现/seed-种子文档.md`。

### 2. 首版正式落盘 soul.md

这是核心修复：soul.md 不再只是 seed 文档里的"草案"段落，而是独立首版正式落盘文件。soul 回答"这是一本什么味道的小说"，管文风、笔触、风格，不管内容、情节、卖点（那些属于 seed）。

参照 `templates/soul.tpl.md` 空模板，填充 6 项必填字段：
1. 叙事人格
2. 句子气口和段落呼吸
3. 对白方式
4. 信息释放
5. 氛围基调
6. 文风禁区

元数据块要求（见 PRD §4.2、§5）：
- doc_type: soul
- read_policy: full-required
- primary_consumer: write
- source_of_truth: true

落盘指令：写入 `涌现/soul.md`。

soul 不记录主卖点、元爽点、读者追读承诺、主角主动方式、爽点外显方式（那些属于 seed）。soul 也不记录可变事实、具体剧情节点、人物当前状态、数值、招式名、系统规则（见 PRD §3.3）。

## 落盘后检查

- [ ] `涌现/seed-种子文档.md` 已写入，元数据块完整。
- [ ] `涌现/soul.md` 已写入，元数据块完整，6 项必填字段无空缺。
- [ ] 主卖点一句话说清且主角主动方式明确。
- [ ] 不把世界压迫当主角主动。
- [ ] 版本与 SKILL.md/skill.json/CHANGELOG 一致（3.5.0）。

## 下一步

种子和 soul 首版落盘后，建议执行：
- `pop-emergent-research`：补燃料和 content-mechanics。
- 随后 `pop-emergent-review`：初始化 current-state。
- 再 `pop-emergent-write`：写正文。

回复采用 PRD §4.7 统一格式。示例：

```markdown
本次采用 skill：pop-emergent-seed
execution.mode：{formal|draft|trial}

{主卖点结论一句话}；soul.md 首版已落盘（6 项必填字段齐全）。

下一步：建议执行 pop-emergent-research 补燃料和 content-mechanics
```
