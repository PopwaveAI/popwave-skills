# step-2-execute.md — 加载子 Skill + 执行 + 修改路由

> **读什么**：目标子 skill SKILL.md + steps/ + templates/ + references/emerge-loop/
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
- **涌现写作环 → expert-writer 主会话直接执行7步循环（不再路由到 emerge）**
- 弧线校准阶段 → `pop-writer-v3-arc`

```
种子设计/弧线校准：Get-Content -Encoding UTF8 -Raw 子 skill SKILL.md → 验证完整
涌现写作环：Get-Content -Encoding UTF8 -Raw references/emerge-loop/*.md（参考文档）
```

**library 查询提醒**：路由到子 skill 前，对照 SKILL.md 的 pop-trope-library 查询矩阵，提醒子 skill 查询对应模块。子 skill 自管查询逻辑（按 `skills/pop-trope-library/references/调用匹配SOP.md` 三维查询）。

**每次阶段完成后**：回写 `项目总控.md`，更新管线进度标记和当前阶段。

> ⛔ **强制**：每个阶段完成后必须更新项目总控.md 的阶段状态（待启动→进行中→已完成）。未更新项目总控 = 阶段未完成。

> ⛔ **阶段间一致性快检**：进入下一阶段前，对比种子文件夹六要素 + 活记忆状态。检测到种子要素与正文不一致时，暂停并提醒退回 v3-seed 修正。

---

## 2. 涌现写作环（expert-writer 主会话执行7步循环）

> expert-writer 是唯一调度器。涌现写作环由 expert-writer 主会话直接执行 Step 0/1/5/6，调度3个独立子skill执行 Step 2/3/4（context隔离）。不再路由到 pop-writer-v3-emerge。

### 循环概览

```
Step 0：本章规划（主会话）→ 参考 references/emerge-loop/step-0-chapter-plan.md
Step 1：信息获取（主会话，强制化）→ 参考 references/emerge-loop/step-1-info-forced.md
Step 2：调度 pop-writer-v3-create（context隔离）→ 参考 references/emerge-loop/step-2-dispatch-create.md
Step 3：调度 pop-writer-v3-revise（context隔离）→ 参考 references/emerge-loop/step-3-dispatch-revise.md
Step 4：调度 pop-writer-v3-qa（context隔离）→ 参考 references/emerge-loop/step-4-dispatch-qa.md
Step 5：记忆更新+种子生长+方向提示（主会话，机械执行）→ 参考 references/emerge-loop/step-5-memory-direction.md
Step 6：落盘+项目总控更新+弧线触发检查（主会话）→ 参考 references/emerge-loop/step-6-commit.md
```

### Step 0：本章规划（主会话）

加载 `references/emerge-loop/step-0-chapter-plan.md` 获取完整流程。

核心动作：
1. 读种子文件夹六要素 + 活记忆 + 上章正文末尾500字 + 方向提示
2. 故事状态感知（压力倒计时/线索超期/节奏趋势/战力/目的地/角色状态）
3. 5个决策点：场景设计/线索推进(≥3条)/爽点设计(≥1个即时)/危机设计/钩子设计(即时危机型)
4. 网文爽感机制10条法则对照检查（红线❌5）
5. 产出 chapter_plan（含 info_gaps 信息缺口引导 Step 1 搜索）

门禁：种子文件夹不存在=终止；10条法则未全对照=退回调；≥3线索/≥1爽点/章末即时钩子

### Step 1：信息获取（主会话，强制化）

加载 `references/emerge-loop/step-1-info-forced.md` 获取完整流程。

核心动作：
1. **强制读 `素材库/索引.md`**（红线❌6门禁：未读取=退回补读）
2. **读 `写作资产/设定库/_index.yaml`（如有）**——按 chapter_plan 判断是否需要读力量体系/社会结构/世界宪法/角色档案
3. 优先处理 chapter_plan.info_gaps（Step 0 产出的信息缺口）
4. 4类检查：制度流程/场景技法/已埋伏笔/创意参考
5. 索引匹配：有→读素材库文件；无→WebSearch→写入素材库/知识沉淀→更新索引
6. 搜索深度标准：每篇≥500字+具体案例/流程/数据+多轮搜索（最多3轮）
7. 无需求时 no_need_reasons 四项逐类说明
8. 产出 info_acquired（YAML格式）

### Step 2：调度 pop-writer-v3-create（context隔离）

加载 `references/emerge-loop/step-2-dispatch-create.md` 获取完整调度流程。

**传入精简context（不传会话历史，红线❌5）：**
- 种子文件夹六要素（压力矩阵/主角引擎含行为准则/金手指/冲突轴+活跃线索/成长路径/目的地）
- 活记忆七组件（最后baseline+event）
- 上章末尾~800字
- chapter_plan（Step 0产出）
- info_acquired（Step 1产出）
- 创作模板（pop-writer-v3-create/templates/创作-模板.md）

**不传入：** 会话历史、Step 0/1执行过程、文风DNA、修订指南、质检模板

子skill执行：上下文确认→涌现写作(场景流+压力源+钩子)→**行为一致性逐场景检查**→创作决策记录

门禁：传入了会话历史=退回重组；未产出正文初稿=终止；行为一致性未通过=退回重写

### Step 3：调度 pop-writer-v3-revise（context隔离）

加载 `references/emerge-loop/step-3-dispatch-revise.md` 获取完整调度流程。

**传入精简context（不传会话历史，红线❌5）：**
- 正文初稿（Step 2产出）
- 文风DNA（`写作资产/文风库/{书名}.md`，硬阻塞红线❌1）
- 种子文件夹六要素（主角引擎含行为准则/金手指/冲突轴）
- 活记忆七组件
- 修订checklist（pop-writer-v3-revise/templates/修订checklist-模板.md）

**不传入：** 会话历史、创作决策记录、质检模板

子skill执行：文风DNA硬阻塞检查→文风对齐→人设丰富(含行为准则对齐)→爽点验证→bug修复→AI观感词清理

门禁：文风DNA缺失=硬阻塞终止；AI观感词>3种=退回create重写；8020比例超标=退回重写

### Step 4：调度 pop-writer-v3-qa（context隔离）

加载 `references/emerge-loop/step-4-dispatch-qa.md` 获取完整调度流程。

**传入精简context（不传会话历史，红线❌5）：**
- 修订稿（Step 3产出）
- 活记忆七组件
- 种子文件夹六要素（活跃线索+压力矩阵+主角引擎含行为准则）
- 网文法则（references/emerge-loop/网文爽感机制.md）
- 质检模板（pop-writer-v3-qa/templates/质检报告-模板.md）

**不传入：** 会话历史、创作决策记录、修订记录、文风DNA

子skill执行：五问反思(引用正文证据)→种子生长判断→爽点终验→**行为一致性终验**→质检总结+回退判定

门禁：质检不通过=按回退目标回退（故事层→create；文风层→revise）；连续3次不通过=标记严重问题建议弧线校准

### Step 5：记忆更新+种子生长+方向提示（主会话，机械执行）

加载 `references/emerge-loop/step-5-memory-direction.md` 获取完整流程。

**机械执行，不做判断**——种子生长判断已在Step 4完成，本步骤只按质检报告机械写入。

核心动作：
1. 活记忆七组件更新（红线❌3：唯一写入者）——从修订稿提取状态变化，追加event
2. 种子生长执行（红线❌4）——读质检报告生长建议，有则更新种子文件夹对应要素文件+last_updated_ch+版本号minor+1+_log.md变更日志
3. 方向提示生成——从质检报告不达标项+超期预警机械转化为1-2句方向感（非章纲）
4. 方向提示回写活记忆event.direction_hint

### Step 6：落盘+项目总控更新+弧线触发检查（主会话）

加载 `references/emerge-loop/step-6-commit.md` 获取完整流程。

核心动作：
1. 修订稿落盘到 `正文/chXXX.md`
2. 项目总控更新：章号+1/种子版本/弧线计数/阶段状态
3. 弧线触发检查：定期触发(距上次校准满10-20章) / 事件触发(伏笔超期>20章/战力跳级/连续5章低密度/目的地20章无进展/线索10章未触及/要素last_updated_ch>15章)
4. 触发→提示用户进入 pop-writer-v3-arc；未触发→回到Step 0开始下一章

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
| 子 agent 不可用 | 声明 `⚠️ master 手动执行` |
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
