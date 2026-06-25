# step-2-execute.md — 加载子 Skill + 执行 + 修改路由

> **读什么**：目标子 skill SKILL.md + steps/ + templates/
> **产出什么**：子 Skill 执行结果
> **闸门**：决策点闸门（creative/plot/chapter/prose — 必须用户确认）

---

## ❌ 读取协议（强制）

```
工具选择：skill_view（首选）或 Get-Content -Encoding UTF8 -Raw
❌ 禁止用 Read 工具读取 skill 文件（有行数限制，会截断）
```

截断检测：读取后对比 content.length vs (Get-Item).Length，<90% 则回退 Raw 重读，连续 2 次不过则终止。

---

## 1. 强制加载（不可跳过）

> **模式检查（★v8.0.0）**：读取项目总控.md 的「管线模式」字段。
> - v2 → 加载 `skills/pop-writer-{阶段}/`
> - v3 → 按 v3 路由表加载 `skills/pop-writer-v3-{seed|emerge|arc}/`

```
Get-Content -Encoding UTF8 -Raw 子 skill SKILL.md → 验证完整
Get-Content -Encoding UTF8 -Raw steps/*.md, templates/*.md
```

**加载子 skill**：
- 从项目总控读取当前阶段（v2）或当前阶段+模式（v3）
- v2：加载 `skills/pop-writer-{阶段}/` 目录下的子 skill
- v3：按 v3 路由表加载对应 skill 集：
  - 种子设计阶段 → `pop-writer-v3-seed`
  - 涌现写作阶段 → `pop-writer-v3-emerge`
  - 弧线校准阶段 → `pop-writer-v3-arc`

**library 查询提醒**：路由到子 skill 前，对照 SKILL.md 的 pop-trope-library 查询矩阵，提醒子 skill 查询对应模块。子 skill 自管查询逻辑（按 `skills/pop-trope-library/references/调用匹配SOP.md` 三维查询）。

**每次阶段完成后**：回写 `项目总控.md`，更新管线进度标记和当前阶段。

> ⛔ **强制**：每个阶段完成后必须更新项目总控.md 的阶段状态（待启动→进行中→已完成）。未更新项目总控 = 阶段未完成。

> ⛔ **阶段间一致性快检**：进入下一阶段前，对比当前阶段产出与 PRD 核心字段（主角名/种族/起点/力量体系）。检测到不一致时暂停并触发 `prd-change-protocol.md`。
> **v3 模式**：一致性检查改为对比种子文档七要素 + 活记忆状态。检测到种子要素与正文不一致时，暂停并提醒退回 v3-seed 或 v3-emerge 修正。

---

## 2. 按子 skill 的 SOP 执行

### v2 模式（原有逻辑不变）

按子 skill 的分步指令执行。**子 skill 自管前置检查、落盘检查、阶段闸门、状态更新。** expert-writer 不重复这些。

### v3 模式执行要点（★v8.0.0新增）

> expert-writer 是纯调度器，执行细节由 v3 子 skill 自管。以下仅列出调度层需协调的事项。

**v3-emerge 执行时**：
1. 信息获取调度：根据 Think 层传递的信息需求清单，提醒 emerge 查询对应模块（套路库/文风库/活记忆）
2. 涌现写作 + 五问反思：emerge 自管，expert-writer 不介入
3. 活记忆更新：emerge 完成后追加 event 到 `活记忆/活记忆.yaml`
4. 种子生长调度：emerge 完成后检查种子是否需要生长（新要素涌现时），需要则提醒 emerge 写回种子文档（version+1，changelog 追加）

**v3-arc 执行时**：
1. 六项宏观检查：arc 自管检查，expert-writer 不重复
2. 种子修剪：arc 完成后，根据校准结果修剪种子文档中已失效的要素（移入已关闭区，version+1）
3. 回退：arc 判定需要回退的章节，由 arc 自管回退机制
4. 压缩：arc 完成后执行活记忆压缩（合并 baseline + event 为新 baseline）

**纪律**（v2/v3 共用）：
- 先问修改 → 再建议下一步 → 不催促
- QA 后只问修改
- 中文。不暴露内部 skill 名。
- 文件写入后对话只留摘要（≤200字）

---

## 3. 修改路由

> 用户要求修改已有产出时执行

**原则：改设定 ≠ 重写全书。退回产出该文件的子 skill 修改，不自己动手。**

### 3.1 重大变更影响范围声明（框架级变更时强制执行）

**触发条件**：用户要求修改 world/character/plot 层面的框架级设定（加穿越者、改力量体系、换核心矛盾等）

**执行步骤**：
1. 扫描全链文件清单（PRD→L1→数值→宪法→卷纲→剧情线→L2单元卡→设计包→正文）
2. 输出「影响范围声明」：

```markdown
## 影响范围声明

| 变更源 | 影响文件 | 影响程度 | 处理方式 |
|:-------|:---------|:---------|:---------|
| {改了什么} | {文件路径} | 🔴重写/🟡修改/🟢不受影响 | {怎么处理} |
```

3. 用户确认范围后逐文件更新
4. **不询问"要不要更新"——机械传播是 agent 的责任**，只问"这个范围对吗？"

### 3.2 回溯触发判定

| 用户改了什么 | 回溯到 | 保留下游 |
|:------------|:-------|:---------|
| 框架级设定（加穿越者/改力量体系） | creative 或 world | ❌ 全链重来 |
| 角色级设定 | character | ⚠️ 检查 plot→chapter→prose |
| 剧情级设定 | plot | ❌ chapter 之后重做 |
| 风格级设定 | prose | ✅ 仅影响后续章节 |

**回溯执行顺序**：
1. 先出影响范围声明（3.1）
2. 用户确认范围
3. 按管线顺序自前向后更新
4. 更新完成后刷新项目总控版本戳

### 3.3 项目回滚（用户要求回到某个阶段重新开始时执行）

> **触发词**："回滚到XX层"/"回到XX重新设计"/"从XX开始重来"/"删掉XX之后的所有东西"
>
> 回滚 ≠ 回溯。回溯是"退回上游修改后级联更新"；回滚是"删除指定层之后的所有产出，从指定层重新开始"。

**执行步骤**：

1. **扫描当前项目状态**：读取项目目录，列出所有已产出文件及其所属管线层

2. **确认回滚目标**：向用户确认——"回滚到 {层} 意味着删除 {层} 之后的所有产出，包括：{文件列表}。确认？"

3. **管线层与文件映射**：

| 回滚到 | 保留 | 删除 |
|:-------|:-----|:-----|
| creative | — | world/character/plot/chapter/prose 全部产出 |
| world | PRD + 素材储备池 | character/plot/chapter/prose 全部产出 |
| character | PRD + 素材储备池 + world | plot/chapter/prose 全部产出 |
| plot | PRD + 素材储备池 + world + character | chapter/prose 全部产出 + 删 state-log.yaml（plot 会重新创建） |
| chapter | PRD + 素材储备池 + world + character + plot | prose 全部产出 + 删 state-log.yaml 中 chapter > N 的条目 |

4. **执行删除**：
   - 删除目标层之后的所有产出文件
   - 不删除 PRD、素材储备池、world 设定（除非回滚到 creative）
   - 保留目录结构（只删文件不删文件夹）

5. **回滚项目总控**：
   - 将管线进度标记回退到目标层
   - 清空执行顺序日志中目标层之后的记录
   - 更新产出物清单（已删除的标记为"已回滚"）
   - 更新当前阶段为目标层
   - 写入回滚记录：`| 回滚 | {时间} | 从 {层} 回滚到 {层} | 删除 {N} 个文件 |`

6. **重置状态文件**：
   - 回滚到 creative/world：删 `状态/state-log.yaml` + 删 `状态/角色/` 目录
   - 回滚到 plot：删 `状态/state-log.yaml`（plot Step 3 会重新创建 baseline #0）
   - 回滚到 chapter（第 N 章）：编辑 `状态/state-log.yaml`，删除 entries 中 chapter > N 的所有条目。如果删完后最后一个条目是 baseline 且其 chapter > N，继续向前找 chapter ≤ N 的最后一个 baseline，删掉它之后的所有条目
   - 回滚到 prose（第 N 章）：同上（state-log 回到 chapter=N 的最后一条 event，正文文件删除 ch>N 的）

7. **告知用户**："已回滚到 {层}。当前项目状态：{保留的产出列表}。可以重新开始 {层} 的设计了。"

### 3.4 常规修改路由

| 改什么 | 退回哪个子 skill |
|:-------|:----------------|
| 修辞/措辞 | pop-writer-prose（局部重写） |
| 人物性格/关系 | pop-writer-character（角色卡） |
| 剧情走向 | pop-writer-plot（受影响的卷/幕） |
| 世界观规则 | pop-writer-world（L1+宪法+级联） |
| 起点/终点状态 | pop-writer-world → plot → chapter → prose（级联） |

### 3.5 v3 修改路由（★v8.0.0新增）

> v3 模式修改路由逻辑与 v2 不同：不按管线层回溯，按种子/正文/活记忆三层处理。

| 用户改了什么 | 退回哪个子 skill | 处理方式 |
|:------------|:----------------|:---------|
| 种子要素（七要素之一） | pop-writer-v3-seed | 修改种子文档 → version+1 → emerge 重新消费 |
| 正文内容（某章） | pop-writer-v3-emerge | 退回重写该章正文（不改种子） |
| 弧线/节奏问题 | pop-writer-v3-arc | 退回 arc 重新校准 → 必要时回退章节 |

### 3.6 v3 项目回滚（★v8.0.0新增）

> v3 回滚 ≠ v2 回滚。v3 没有"管线层"概念，回滚按 **章号** 执行：删活记忆 entries + 删正文。

**执行步骤**：
1. 确认回滚目标章号 N
2. 删除 `正文/ch{>N}.md` 所有文件
3. 编辑 `活记忆/活记忆.yaml`：删除 chapter > N 的所有 event 条目，将 baseline 回退到 chapter ≤ N 的最后一条
4. 不删除种子文档（种子是跨章节持久资产）
5. 更新项目总控.md：章号回退到 N、弧线计数调整、写入回滚记录
6. 告知用户："已回滚到第 N 章。活记忆已同步。可以重新写第 N+1 章了。"

---

## 4. 异常与边界条件

| 场景 | 动作 |
|:-----|:-----|
| 子 skill SKILL.md 找不到 | 终止 + 告知用户 |
| 子 agent 不可用 | 声明 `⚠️ master 手动执行` |
| 执行失败 | 通知用户 + 原因 + 可操作建议 |
| 前置阶段未完成 | 告知缺什么阶段，建议先补齐 |
| 无法匹配路由 | 回到 Think 追问补全信息 |
| 用户要跳步 | 说清代价，给两个选项。确认后立即切换 |
| 越界检测 | "这属于 [X] 的范围，到那一步处理。先完成当前阶段。" |
| 批量写N章/风格迁移 | 管线旁路：跳过 creative→plot→chapter，直接从源文本提取事件链 → 委托 prose 并行渲染。批次划分/设计包格式/delegate context 由 prose 子 skill 自管 |
