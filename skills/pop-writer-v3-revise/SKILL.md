---
name: pop-writer-v3-revise
description: 涌现写作修订子skill（v3.5渲染层）。context隔离，完全重写模式+文风DNA硬阻塞（Get-Content -Raw完整加载）+文风DNA终验（7项附证据）+事实信息一致性检查（6项零改写）+导演意图验证（5项，v3.5新增核心质量机制）+AI观感词清理+字数终检。输入来源从种子文档改为写作参考/设定/（主角引擎+金手指）+L2卡活跃线索。context receipt预留接口（批次2完整实现）。
pipeline:
  upstream: [pop-writer-v3-create]
  downstream: []
version: 1.2.0
---

# 修订子skill

> 由 expert-writer 主会话涌现写作循环 Step 3 调度，context隔离。

v3.5 管线涌现写作的修订子skill（渲染层）。基于正文初稿+文风DNA完全重写渲染层：保留创作层产出的全部事实信息（人名/动作/事件顺序/对话内容/场景/数值），仅重做渲染层（句式/叙事距离/感官密度/对话留白/8020比例）。文风DNA在此层完整加载并硬阻塞（红线❌1）。

**v3.5 核心变化：**
1. **新增导演意图验证（红线❌3）**——重写后对照导演意图验证清单检查产出5项（叙事功能/事件链覆盖/情绪曲线对齐/子线推进/章末钩子）。这是 v3.5 的核心质量机制。注意：revise 不接收导演意图完整内容（创作决策不回传），只接收主会话从导演意图提取的5项验证标准（检查清单）。不通过则标注偏差项，不自动退回——退回由主会话 Step4 决定。
2. **输入来源调整**——种子文档已取消，要素切片来源改为：主角引擎→`写作参考/设定/主角引擎.md`、金手指→`写作参考/设定/金手指.md`、活跃线索→从L2卡嵌套子线提取（由主会话注入）。
3. **context receipt 预留**——产出时附带 context receipt 确认实际接收的注入项。本批次先预留格式说明，完整实现在批次2。

**保持的职责（不变）：** 完全重写模式；文风DNA终验（7项核心特征附正文证据）；事实信息一致性检查（6项逐项比对）；AI观感词清理（≤3种命中）；字数终检（2500-3500字）；硬约束绝不改写事实信息只改渲染层。

## 红线

| 编号 | 红线 | 检查方式 |
|------|------|----------|
| ❌1 | 文风DNA必须 `Get-Content -Raw` 完整加载，禁止 read 工具 limit 截断 | 修订前用 `Get-Content -Encoding UTF8 -Raw` 加载文风库文件；发现 limit 截断/文件空/路径错误=硬阻塞终止（不降级、不A/B、不空写） |
| ❌2 | 绝不改写事实信息（人名/动作/事件顺序/对话内容/场景/数值），只改渲染层 | 重写后逐项比对初稿，事实信息任一被改写=退回重写 |
| ❌3 | 导演意图验证5项必须全部检查（不通过则标注偏差项，不自动退回——退回由主会话决定） | 对照注入的导演意图验证清单逐项检查，未通过项标注偏差写入修订记录，由主会话 Step4 决定是否退回 |
| ❌4 | 字数终检 2500-3500字 | 重写稿字数<2500=退回create（事实信息不足）；>3500=强制精简渲染层（保留事实信息） |

> 说明：context隔离不再单列为红线，改由 context manifest/receipt 机制白盒化——revise 通过 context receipt 确认接收了哪些注入项、确认未接收哪些（导演意图完整内容/状态快照/info_acquired/L2卡完整内容）。

## 步骤加载

| 步骤 | 文件 | 说明 |
|------|------|------|
| step-1 | steps/step-1-revise.md | 文风DNA硬阻塞加载+完全重写+事实信息一致性检查（6项）+文风DNA终验（7项）+导演意图验证（5项）+AI观感词清理+字数终检+context receipt预留 |

## references/ — 知识层

| 什么时候 | 加载 | 产出 |
|:---------|:-----|:-----|
| step-1 修订执行 | `references/修订指南.md` | 完全重写规范+事实一致性检查+文风DNA终验+导演意图验证标准+AI观感词清理+字数终检 |

## templates/ — 模板层

| 什么时候 | 加载 | 产出 |
|:---------|:-----|:-----|
| step-1 修订产出 | `templates/修订checklist-模板.md` | 完全重写checklist+导演意图验证checklist+修订记录YAML（含rewrite_mode/fact_consistency/dna_final_check/director_intent_verification/word_count_check/context_receipt） |

## 输入/输出契约

### 输入（revise 接收）

| 输入项 | 来源 | 用途 |
|:-------|:-----|:-----|
| 正文初稿 | create子skill产出 | 重写对象（事实信息来源，不可改写） |
| 文风DNA | `写作资产/文风库/{书名}.md` | 渲染引擎（硬阻塞，红线❌1，Get-Content -Raw完整加载） |
| L2卡要素切片·主角引擎 | `写作参考/设定/主角引擎.md` | 事实一致性比对依据（驱动力+行为准则） |
| L2卡要素切片·金手指 | `写作参考/设定/金手指.md` | 事实一致性比对依据（能力+限制） |
| L2卡要素切片·活跃线索 | 从L2卡嵌套子线提取（主会话注入） | 事实一致性比对依据（活跃子线进展） |
| 导演意图验证清单 | 主会话从导演意图提取的5项验证标准 | 导演意图验证5项检查的对照标准（红线❌3） |
| 上章末尾 | `正文/chXXX.md`末尾 | 衔接检查（重写稿开头与上章末尾自洽） |
| 修订checklist | `templates/修订checklist-模板.md` | 产出格式 |

### 输入（revise 不接收）

| 不接收项 | 原因 |
|:---------|:-----|
| 导演意图完整内容 | 创作决策不回传——revise 只接收验证清单，不接收导演意图本体 |
| info_acquired | 创作阶段信息获取产物，不回传渲染层 |
| L2卡完整内容 | 结构约束属创作层，渲染层只需要素切片 |
| 状态快照 | 状态注入属创作层，渲染层不接收 |

### 输出

| 输出项 | 格式 | 传递给 |
|:-------|:-----|:-------|
| 重写稿 | markdown | expert-writer调度器→交付用户验收（CHECK 2） |
| 修订记录 | YAML | expert-writer调度器→验收后传Step4（receipt检查+导演意图验证由主会话Step4执行） |
| context receipt | YAML | expert-writer调度器→Step4对照manifest检查一致性（批次2完整实现，本批次预留格式） |

## 路由

upstream `pop-writer-v3-create`（创作子skill，产出正文初稿） → **本skill** → downstream 无（revise是渲染层终点，重写稿交付用户验收CHECK 2）

**调度架构：** 本skill由expert-writer主会话涌现写作循环Step 3调用，context隔离——只接收精简context（正文初稿+文风DNA+L2卡要素切片+导演意图验证清单+上章末尾+修订checklist），不接收会话历史、导演意图本体、状态快照。完全重写+质检完成后返回重写稿+修订记录+context receipt给expert-writer调度器，交付用户验收（CHECK 2），验收后传Step4（receipt检查+导演意图验证由主会话执行）。

## context receipt（批次2预留接口）

revise 产出时附带 context receipt，确认实际接收了哪些注入项、确认未接收哪些。本批次（v1.2.0）先预留格式说明，完整一致性检查在批次2由主会话Step4执行。

### receipt 格式（预留）

```yaml
context_receipt:
  received:
    - item_id: draft
      source: create产出正文初稿
      status: full          # full / partial / missing
      size_chars: {N}
    - item_id: style_dna
      source: 写作资产/文风库/{书名}.md
      load_method: "Get-Content -Encoding UTF8 -Raw"
      status: full          # 硬阻塞，必须 full 且 0 误差
      truncated: false
      size_chars: {N}
    - item_id: l2_slice
      source: 写作参考/设定/主角引擎.md + 写作参考/设定/金手指.md + L2卡活跃线索(主会话注入)
      status: full
      components: [protagonist_engine, golden_finger, active_sublines]
    - item_id: director_intent_checklist
      source: 主会话从导演意图提取的5项验证标准
      status: full
      check_items: 5
    - item_id: prev_chapter_tail
      source: 正文/chXXX.md末尾
      status: full
  not_received:              # 确认未接收（创作决策不回传）
    - director_intent        # 导演意图完整内容
    - info_acquired
    - l2_card_full
    - state_snapshot
  anomalies: []             # 异常列表，空=正常
```

### 一致性检查项（批次2由主会话Step4执行）

| 检查维度 | 通过条件 | 不通过处理 |
|:---------|:---------|:-----------|
| style_dna 完整性 | status=full 且精确匹配（0误差） | 标记 dna_truncated，重新注入 Get-Content -Raw |
| 导演意图验证 | 5项验证全部通过 | 标记 intent_mismatch，主会话决定是否退回 |
| 关键元素确认 | key_elements 全部确认 | 标记 missing_elements |
| L2卡要素切片 | 主角引擎+金手指+活跃线索均接收 | 标记 slice_partial |

---

v1.0.0 | 2026-06-26 | 从pop-writer-v3-emerge v1.2.0拆分出修订子skill；人设丰富新增行为准则对齐检查；context隔离红线（红线❌2）
v1.1.0 | 2026-06-27 | v3.4重构：逐行修改→完全重写模式（基于正文骨架+文风DNA）；剔除qa，revise成为终点交付用户验收CHECK 2；新增红线❌3（重写改写事实信息=退回重写）+❌4（DNA用limit截断=退回重载）；新增文风DNA终验+事实信息一致性检查+字数终检
v1.2.0 | 2026-06-28 | v3.5重构：新增导演意图验证（5项，红线❌3）——重写后对照验证清单检查叙事功能/事件链/情绪曲线/子线/章末钩子，不通过标注偏差不自动退回；输入来源从种子文档改为写作参考/设定/（主角引擎+金手指）+L2卡活跃线索；新增上章末尾输入（衔接检查）；红线重构为4条（文风DNA完整加载/事实不改写/导演意图验证/字数终检）；context receipt预留接口（批次2完整实现）
