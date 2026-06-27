# step-2-execute.md — 加载子 Skill + 执行5步循环 + 修改路由

> **读什么**：目标子 skill SKILL.md + steps/step-2-0~5 + references/pipeline/manifest.md
> **产出什么**：子 Skill 执行结果（5步循环完成后产出本章正文+活记忆更新+项目总控更新）
> **闸门**：决策点闸门（种子设计/弧线校准 — 必须用户确认）

---

## ❌ 读取协议（强制）

```
工具选择：skill_view（首选）或 Get-Content -Encoding UTF8 -Raw
❌ 禁止用 Read 工具读取 skill 文件（有行数限制，会截断）
✅ 路由到子skill前，必须先 Get-Content -Encoding UTF8 -Raw 目标子skill完整SKILL.md（红线2）
```

---

## 1. 涌现写作环：5步循环（v3.5）

> v3.4 的6步（plan→info→create→revise→memory→commit）简化为v3.5的5步。
> 原 Step4（dispatch-revise）合并进 Step3（create→revise一次调度）。
> 原 Step4（memory）+ Step5（commit）合并为 Step5（活记忆更新+落盘）。

### 5步循环概览

| Step | 名称 | 执行者 | 核心动作 | 人工check | step文件 |
|:-----|:-----|:-------|:---------|:---------|:---------|
| Step0 | 导演意图提取 | 主会话 | 从L2卡结构分析表取本章行→组装导演意图（≤150字） | **CHECK 1**：用户确认 | step-2-0-director-intent.md |
| Step1 | 状态快照投影 | 主会话 | 从活记忆+L2卡物理坐标投影当前状态（≤400字） | 无 | step-2-1-state-snapshot.md |
| Step2 | 信息获取 | 主会话 | 设定指针强制读取→library按需查询→pop-research(如需) | 无 | step-2-2-info-acquisition.md |
| Step3 | 子agent创作 | 子agent | context manifest组装→create涌现写作→revise完全重写 | **CHECK 2**：用户验收 | step-2-3-dispatch-create-revise.md |
| Step4 | receipt检查 | 主会话 | 对照manifest vs receipt→对照导演意图验证 | 无 | step-2-4-receipt-check.md |
| Step5 | 活记忆更新+落盘 | 主会话 | 自然语言追加活记忆→正文落盘→项目总控更新 | 无 | step-2-5-memory-commit.md |

### 两个人工check点

- **CHECK 1**（Step0 → Step1 之间）：导演意图用户确认 → 确认后才进Step1
- **CHECK 2**（Step3 → Step4 之间）：revise重写稿最终正文验收 → 验收后才进Step4
- Step1→Step2→Step3 自动连贯执行，中间不交付用户、不暂停
- Step4→Step5 自动连贯执行，中间不暂停

### 弧线触发

- **每个L2单元结束时触发arc**（完整5步全跑）
- 触发条件：L2单元最后一章的Step5（落盘）完成后，自动检查是否为该L2单元最后一章 → 是则触发arc

---

## 2. 执行流程

### 2.1 Step0：导演意图提取（主会话执行）

1. 读取 `steps/step-2-0-director-intent.md`
2. 从L2卡结构分析表提取本章行
3. 组装导演意图（≤150字），含：
   - narrative_function（叙事功能）
   - event_chain（事件链）
   - emotion_curve（情绪曲线）
   - three_questions（三问：info/pressure/hook）
   - settings_ref（设定引用指针列表）
4. **【CHECK 1】** 交付用户确认导演意图 → 用户确认后才进Step1

### 2.2 Step1：状态快照投影（主会话执行）

1. 读取 `steps/step-2-1-state-snapshot.md`
2. 从活记忆最新events + L2卡物理坐标段实时投影当前状态（≤400字）
3. 产出state_snapshot YAML（不持久化，每章实时投影）
4. 自动进入Step2（不暂停）

### 2.3 Step2：信息获取（主会话执行）

1. 读取 `steps/step-2-2-info-acquisition.md`
2. **A. 设定指针强制读取**：看导演意图的settings_ref列表 → `Get-Content -Raw` 逐个读取对应文件 → 不靠agent判断，指针指向了就必须读
3. **B. 按需查询**：
   - library套路库/L2卡参考（按需）
   - pop-research（如需，尚未创建则WebSearch替代）
   - 前文细节（活记忆+前章正文）
4. 产出info_acquired记录
5. 自动进入Step3（不暂停）

### 2.4 Step3：子agent创作（调度子agent执行）

1. 读取 `steps/step-2-3-dispatch-create-revise.md`
2. **create阶段**：
   - 组装context manifest（导演意图+状态快照+上章末尾+设定文件+info_acquired）
   - 路由到 pop-writer-v3-create 子agent（红线2：先读子skill SKILL.md）
   - 注入完整context → 产出初稿+create receipt
3. **revise阶段**（自动连贯，不暂停）：
   - 注入初稿+文风DNA+要素切片+导演意图验证清单
   - 路由到 pop-writer-v3-revise 子agent（红线2：先读子skill SKILL.md）
   - 产出重写稿+revise receipt
4. **【CHECK 2】** 交付用户验收重写稿 → 用户验收后才进Step4

### 2.5 Step4：receipt检查（主会话执行）

1. 读取 `steps/step-2-4-receipt-check.md`
2. 对照manifest vs receipt逐项检查：
   - 完整性：receipt.status=full 且 actual_read≈manifest.size
   - 关键元素：key_elements_confirmed覆盖所有声明元素
   - 导演意图（create）：三问全部确认
   - 设定文件读取：settings_ref全部status=full
   - 文风DNA（revise）：status=full 且精确匹配（0误差）
   - 导演意图验证（revise）：5项验证全部通过
3. 修复策略：连续2次同一项不通过 → 降级策略B（红线5）
4. 检查通过 → 进入Step5

### 2.6 Step5：活记忆更新+落盘（主会话执行）

1. 读取 `steps/step-2-5-memory-commit.md`
2. **活记忆追加**：自然语言段落（一段话概括本章状态变化）→ 追加到 `活记忆/活记忆.yaml`
3. **正文落盘**：写入 `正文/chXXX.md`
4. **项目总控更新**：章号+1 / 弧线计数 / 管线阶段更新
5. **弧线触发检查**：如本章是L2单元最后一章 → 触发arc

---

## 3. 其他路由

### 3.1 路由到其他子skill

当 Think 阶段判断需要路由到非5步循环的子skill时：

1. `Get-Content -Encoding UTF8 -Raw` 读取目标子skill SKILL.md（红线2）
2. 按子skill SKILL.md 指引执行
3. 子skill执行完毕 → 回到 step-3-reflect.md

### 3.2 回滚

用户说"回滚到第N章"：

1. 确认回滚目标章号
2. 删除 `正文/chNNN.md` 及之后所有章节
3. 回退活记忆到第N章之前的状态（删除N及之后的events）
4. 更新项目总控：章号回退到N
5. 提示用户：重新从第N章 Step0 开始

---

## 4. 执行完毕

5步循环完成 → 进入 `step-3-reflect.md`（通用审视+项目总控回写+引导）
