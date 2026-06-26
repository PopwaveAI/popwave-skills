# step-2-execute.md — 加载子 Skill + 执行 + 修改路由

> **读什么**：目标子 skill SKILL.md + steps/step-2-* + references/emerge-loop/
> **产出什么**：子 Skill 执行结果
> **闸门**：决策点闸门（种子设计/弧线校准 — 必须用户确认）

---

## ❌ 读取协议（强制）

```
工具选择：skill_view（首选）或 Get-Content -Encoding UTF8 -Raw
❌ 禁止用 Read 工具读取 skill 文件（有行数限制，会截断）
```

截断检测：读取后对比 content.length vs (Get-Item).Length，<90% 则回退 Raw 重读，连续 2 次不过则终止。

---

## 1. 强制加载（不可跳过）

按路由表加载对应 skill 集：
- 种子设计阶段 → `pop-writer-v3-seed`
- **涌现写作环 → expert-writer 主会话直接执行6步循环（v3.4剔除qa）**
- 弧线校准阶段 → `pop-writer-v3-arc`

```
种子设计/弧线校准：Get-Content -Encoding UTF8 -Raw 子 skill SKILL.md → 验证完整
涌现写作环：加载 `steps/step-2-*.md`（执行层）+ `references/emerge-loop/*.md`（知识层）
```

**library 查询提醒**：路由到子 skill 前，对照 SKILL.md 的 pop-trope-library 查询矩阵，提醒子 skill 查询对应模块。子 skill 自管查询逻辑（按 `skills/pop-trope-library/references/调用匹配SOP.md` 三维查询）。

**每次阶段完成后**：回写 `项目总控.md`，更新管线进度标记和当前阶段。

> ⛔ **强制**：每个阶段完成后必须更新项目总控.md 的阶段状态（待启动→进行中→已完成）。未更新项目总控 = 阶段未完成。

> ⛔ **阶段间一致性快检**：进入下一阶段前，对比种子文件夹六要素 + 活记忆状态。检测到种子要素与正文不一致时，暂停并提醒退回 v3-seed 修正。

---

## 2. 涌现写作环（6步循环，v3.4剔除qa）

> expert-writer 是唯一调度器。6步循环的详细执行流程在 `steps/step-2-*.md` 目录下，按步骤加载对应step文件执行。知识层参考文档在 `references/emerge-loop/`。

### 循环结构

| 步骤 | 执行者 | step文件 | 知识层参考 | 核心动作 |
|:-----|:-------|:---------|:-----------|:---------|
| Step 0 本章规划 | 主会话 | `steps/step-2-0-chapter-plan.md` | `references/emerge-loop/网文爽感机制.md` | 任务list规划+法则对照+info_gaps 【CHECK 1：用户确认】 |
| Step 1 信息获取 | 主会话 | `steps/step-2-1-info-forced.md` | `references/emerge-loop/信息获取强制化SOP.md` | 强制读资料总索引+WebSearch+写入素材库 |
| Step 2 调度创作 | 调度create子skill | `steps/step-2-2-dispatch-create.md` | - | 传入精简context→涌现写作+行为一致性（初稿不交付，自动连贯） |
| Step 3 调度修订 | 调度revise子skill | `steps/step-2-3-dispatch-revise.md` | - | 完全重写+文风DNA终验+事实一致性+字数终检 【CHECK 2：用户验收重写稿】 |
| Step 4 记忆+生长 | 主会话 | `steps/step-2-4-memory-direction.md` | `references/emerge-loop/活种子生长触发规则.md` | 机械执行：活记忆更新+种子生长写入+方向提示 |
| Step 5 落盘 | 主会话 | `steps/step-2-5-commit.md` | - | 重写稿落盘+项目总控更新+弧线触发检查 |

### 执行规则

1. **种子文件夹读取协议**（所有步骤通用）：
   - 先读 `种子/_index.yaml` → 获取版本号 + 要素文件清单 + 各要素 last_updated_ch
   - 再按步骤需要读取对应要素文件（不全量读取，按需加载）：
     - Step 0 本章规划：全量六要素（压力矩阵/主角引擎/金手指/冲突轴/成长路径/目的地）
     - Step 1 信息获取：按 chapter_plan 涉及的要素按需读
     - Step 2 调度create：传入六要素精简context
     - Step 3 调度revise：传入主角引擎+金手指+冲突轴
     - Step 4 种子生长：按revise修订记录更新对应要素文件
     - Step 5 落盘：读_index.yaml获取版本号回写项目总控

2. **按步骤顺序执行**，每步加载对应step文件获取完整流程
3. **Step 2/3 调度子skill时必须context隔离**（红线❌5）：传入精简context，不传会话历史
4. **Step 0 产出 chapter_plan 必须落盘到 `章节规划/chXXX-plan.md` 并经用户确认**后才进入Step 1
5. **v3.4自动连贯**：Step 1→Step 2→Step 3 自动执行不暂停，仅Step 0（plan确认）和Step 3（revise重写稿验收）两个人工check点
6. **Step 3 revise承担原qa全部质检职责**（文风DNA终验+事实一致性+字数终检），不再调用qa子skill
7. **Step 4 机械执行**：种子生长判断已在Step 3 revise完成，Step 4只按revise修订记录机械写入
8. **Step 5 循环回Step 0**：弧线未触发→回到Step 0开始下一章；触发→进入弧线校准

### 弧线校准执行（pop-writer-v3-arc）

1. 六项宏观检查：arc 自管检查，expert-writer 不重复
2. 种子修剪：arc 完成后，根据校准结果修剪种子文件夹中已失效的要素（移入_log.md已关闭区，version+1）
3. 回退：arc 判定需要回退的章节，由 arc 自管回退机制
4. 压缩：arc 完成后执行活记忆压缩（合并 baseline + event 为新 baseline）

---

## 3. 修改路由

> 用户要求修改已有产出时执行

**原则：改设定 ≠ 重写全书。退回产出该文件的子 skill 修改，不自己动手。**

### 3.1 修改路由

| 用户改了什么 | 退回哪个子 skill | 处理方式 |
|:------------|:----------------|:---------|
| 种子要素（六要素之一） | pop-writer-v3-seed | 修改种子文件夹对应要素文件 → version+1 → 重新消费 |
| 正文内容（某章） | expert-writer(涌现写作环) | 退回重写该章正文（不改种子） |
| 弧线/节奏问题 | pop-writer-v3-arc | 退回 arc 重新校准 → 必要时回退章节 |

### 3.2 项目回滚

> 回滚按 **章号** 执行：删活记忆 entries + 删正文。

**执行步骤**：
1. 确认回滚目标章号 N
2. 删除 `正文/ch{>N}.md` 所有文件
3. 编辑 `活记忆/活记忆.yaml`：删除 chapter > N 的所有 event 条目，将 baseline 回退到 chapter ≤ N 的最后一条
4. 不删除种子文件夹（种子是跨章节持久资产）
5. 更新项目总控.md：章号回退到 N、弧线计数调整、写入回滚记录
6. 告知用户："已回滚到第 N 章。活记忆已同步。可以重新写第 N+1 章了。"

---

## 4. 异常与边界条件

| 场景 | 动作 |
|:-----|:-----|
| 子 skill SKILL.md 找不到 | 终止 + 告知用户 |
| 子 agent 不可用 | 降级主会话执行（方案B兜底）：必须 `Get-Content -Raw` 重读完整种子context+文风DNA完整加载+独立质检，标注 `degraded_master_execution:true`。重试限制1次。降级≠跳过门禁 |
| 执行失败 | 通知用户 + 原因 + 可操作建议 |
| 前置阶段未完成 | 告知缺什么阶段，建议先补齐 |
| 无法匹配路由 | 回到 Think 追问补全信息 |
| 用户要跳步 | 说清代价，给两个选项。确认后立即切换 |
| 越界检测 | "这属于 [X] 的范围，到那一步处理。先完成当前阶段。" |
| 批量写N章/风格迁移 | 管线旁路：跳过正常涌现写作环，直接从源文本提取事件链 → 委托创作子skill并行渲染 |

**纪律**：
- 先问修改 → 再建议下一步 → 不催促
- QA 后只问修改
- 中文。不暴露内部 skill 名。
- 文件写入后对话只留摘要（≤200字）
