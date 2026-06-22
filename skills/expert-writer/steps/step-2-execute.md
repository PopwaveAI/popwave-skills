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

```
Get-Content -Encoding UTF8 -Raw 子 skill SKILL.md → 验证完整
Get-Content -Encoding UTF8 -Raw steps/*.md, templates/*.md
```

**library 查询提醒**：路由到子 skill 前，对照 SKILL.md 的 pop-trope-library 查询矩阵，提醒子 skill 查询对应模块。子 skill 自管查询逻辑（按 `skills/pop-trope-library/references/调用匹配SOP.md` 三维查询）。

**每次阶段完成后**：回写 `项目总控.md`，更新管线进度标记和当前阶段。

---

## 2. 按子 skill 的 SOP 执行

按子 skill 的分步指令执行。**子 skill 自管前置检查、落盘检查、阶段闸门、状态更新。** expert-writer 不重复这些。

**纪律**：
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
1. 扫描全链文件清单（PRD→L1→数值→宪法→卷纲→剧情线→幕纲→设计包→正文）
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

### 3.3 常规修改路由

| 改什么 | 退回哪个子 skill |
|:-------|:----------------|
| 修辞/措辞 | pop-writer-prose（局部重写） |
| 人物性格/关系 | pop-writer-character（角色卡） |
| 剧情走向 | pop-writer-plot（受影响的卷/幕） |
| 世界观规则 | pop-writer-world（L1+宪法+级联） |
| 起点/终点状态 | pop-writer-world → plot → chapter → prose（级联） |

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
