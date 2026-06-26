# Step 2：调度创作子skill

> 参考: expert-writer 涌现写作环
> 类型: 主会话调度（调用 pop-writer-v3-create）
> 消费: Step 0本章规划 + Step 1信息获取 + 种子文件夹 + 活记忆
> 产出: 正文初稿 + 创作决策记录
> 红线: ❌7 子skill调度context隔离——传入精简context，不传会话历史

## 目的

emerge作为调度器，组装精简context调用pop-writer-v3-create子skill执行创作。不传会话历史，不传文风DNA/修订指南/质检模板。创作子skill专注故事涌现（场景流+压力源+钩子+行为一致性），context隔离。

## 输入context组装（精简，不传会话历史）

| 输入项 | 来源 | 内容 |
|:-------|:-----|:-----|
| 种子六要素 | `种子/文件夹`（当前版本） | 压力矩阵/主角引擎（含行为准则）/金手指/冲突轴+活跃线索/成长路径/目的地 |
| 活记忆七组件 | `活记忆/活记忆.yaml`（最后baseline+event） | 种子追踪/压力状态/角色状态/世界规则/节奏日志/战力曲线/目的地进度 |
| 上章末尾 | `正文/ch{上一章}.md` 最后~800字 | 语感衔接+悬念承接 |
| chapter_plan | `章节规划/chXXX-plan.md`（Step 0已落盘+用户确认） | 任务list（本章定位/主角目标/读者获得/剧情线目标/信息释放/信息需求/钩子方向） |
| info_acquired | Step 1产出 | 增量信息（制度细节/场景技法/伏笔回收线索） |
| 创作模板 | `pop-writer-v3-create/templates/创作-模板.md` | 正文涌现结构+创作决策记录格式+行为准则确认项 |

**不传入的内容：** 主会话历史、Step 0/1的执行过程、文风DNA、修订指南、质检模板。

## 调用

加载 `pop-writer-v3-create` SKILL.md → 按其 `steps/step-1-create.md` 执行

子skill执行内容：
- 上下文确认（含行为准则已加载确认）
- 涌现写作（场景流渲染+压力源逼近+章末钩子）
- **主角行为一致性检查（红线❌2，逐场景检查）**
- 创作决策记录

## 输出收集

| 输出项 | 格式 | 传递给 |
|:-------|:-----|:-------|
| 正文初稿 | markdown | 直接传给Step 3（调度revise），不交付用户 |
| 创作决策记录 | YAML | Step 4（记忆+生长） |

## v3.4自动连贯说明

create初稿产出后不暂停、不交付用户验收，直接组装context传给Step 3调度revise。中间无人工介入。第一个人工check点已在Step 0（plan确认），第二个人工check点在Step 3后（revise重写稿验收）。

## 子agent失败降级策略（方案B兜底）

优先使用子agent（sessions_spawn）调度create。子agent失败时降级为主会话执行，但必须：

1. **重读完整种子context**：用 `Get-Content -Encoding UTF8 -Raw` 重新加载种子六要素全量文件，不依赖会话历史记忆
2. **重读资料总索引+info_acquired**：确认本章信息获取成果完整加载
3. **独立质检下沉revise**：降级不跳过门禁——create产出后仍必须进Step 3 revise做文风DNA终验+事实一致性检查
4. **降级标记**：在创作决策记录中标注 `degraded_master_execution: true`
5. **重试限制**：子agent最多重试1次，第2次失败才降级主会话

> 降级≠跳过门禁。6步门禁在降级模式下同样必须全部通过。

## 门禁

| 检查项 | 失败动作 |
|:-------|:---------|
| **传入了会话历史（红线❌7）** | **退回，重组精简context** |
| 子skill未产出正文初稿 | 终止，报错 |
| 子skill行为一致性检查未通过（红线❌2） | 退回子skill重写 |
| 创作决策记录未产出 | 补产出后再继续 |
| 降级主会话执行但未重读种子context（红线❌5） | 退回 `Get-Content -Raw` 重读 |

---
下一 step：`steps/step-2-3-dispatch-revise.md` — 调度revise子skill（完全重写+文风DNA终验+事实一致性+字数终检，v3.4质检全部下沉到此层）
