# 修订checklist模板

> 所属: pop-writer-v3-revise v1.2.0 · templates/
> 消费: step-1 修订产出
> 红线: ❌1 文风DNA必须Get-Content -Raw完整加载禁止limit截断；❌2 绝不改写事实信息只改渲染层；❌3 导演意图验证5项必须全部检查（不通过标注偏差不自动退回）；❌4 字数终检2500-3500字

## 使用说明

修订子skill执行时填写本模板。包含6项checklist和修订记录YAML+context receipt。每项checklist逐条检查，不通过的项需修正或触发门禁。

## Checklist 1：文风DNA硬阻塞+完全重写

| # | 检查项 | 标准 | 检查结果 | 修正记录 |
|:-:|:-------|:-----|:---------|:---------|
| 1.1 | DNA完整加载 | 文风DNA用 `Get-Content -Encoding UTF8 -Raw` 完整加载，无limit截断（红线❌1硬阻塞） | ☐ 通过 / ☐ 硬阻塞终止 | {加载方式或"终止"} |
| 1.2 | 层A整体风格 | 句式/叙事距离/战斗节奏/对话留白匹配DNA层A | ☐ 通过 / ☐ 需修正 | {修正内容} |
| 1.3 | 层B场景卡 | 场景类型对应的观察句/原文锚定已对齐 | ☐ 通过 / ☐ 需修正 | {修正内容} |
| 1.4 | 8020比例 | 80%展示+20%内省（按场景类型比例） | ☐ 通过 / ☐ **退回** | {比例超标描述} |
| 1.5 | 衔接检查 | 重写稿开头与上章末尾自洽（情绪/场景/时间线衔接） | ☐ 通过 / ☐ 需修正 | {衔接描述或修正} |

**8020比例检查明细：**

| 场景 | 类型 | 展示% | 内省% | 内省次数 | 是否超标 |
|:-----|:-----|:------:|:------:|:--------:|:--------|
| {场景1} | 行动/情感/对话/发现 | {N}% | {N}% | {N}处 | ☐ 否 / ☐ 是 |
| {场景2} | | | | | |

> 门禁：8020超标（连续2段以上纯内省）= 退回重写

## Checklist 2：事实信息一致性

| # | 检查项 | 标准 | 检查结果 | 修正记录 |
|:-:|:-------|:-----|:---------|:---------|
| 2.1 | 人名 | 角色名称/称呼零改写 | ☐ 通过 / ☐ **退回** | {改写内容或"零改写"} |
| 2.2 | 动作 | 角色动作/行为零改写（渲染可变，动作本身不可变） | ☐ 通过 / ☐ **退回** | {改写内容或"零改写"} |
| 2.3 | 事件顺序 | 事件发生先后顺序零改写 | ☐ 通过 / ☐ **退回** | {改写内容或"零改写"} |
| 2.4 | 对话内容 | 对话信息/意图零改写（引导词渲染可变，内容不可变） | ☐ 通过 / ☐ **退回** | {改写内容或"零改写"} |
| 2.5 | 场景 | 场景设置/地点/环境零改写 | ☐ 通过 / ☐ **退回** | {改写内容或"零改写"} |
| 2.6 | 数值 | 数值/距离/数量/时间零改写 | ☐ 通过 / ☐ **退回** | {改写内容或"零改写"} |

**幕纲要素切片一致性比对（补充）：**

| 比对维度 | 切片来源 | 正文表现 | 是否一致 |
|:---------|:---------|:---------|:--------|
| 主角引擎对齐 | `写作参考/设定/主角引擎.md`（驱动力+行为准则） | {本章主角行为是否符合} | ☐ 是 / ☐ 否 |
| 金手指限制 | `写作参考/设定/金手指.md`（能力+限制） | {金手指使用是否在限制内} | ☐ 是 / ☐ 否 |
| 活跃线索进展 | 幕纲活跃线索（主会话注入） | {活跃线索推进是否一致} | ☐ 是 / ☐ 否 |

> 门禁：6项事实信息任一被改写=退回重写（红线❌2）

## Checklist 3：文风DNA终验

| # | 核心特征 | 终验内容 | 检查结果 | 正文证据 |
|:-:|:---------|:---------|:---------|:---------|
| 3.1 | 场景卡公式 | 正文符合DNA场景卡公式（观察句+原文锚定+时间演变） | ☐ 通过 / ☐ **退回** | {引用正文片段} |
| 3.2 | 数据嵌入格式 | 数值/数据嵌入符合DNA格式（戏剧/模糊/精确） | ☐ 通过 / ☐ **退回** | {引用正文片段} |
| 3.3 | 感官序列 | 感官描写顺序符合DNA感官序列锚定 | ☐ 通过 / ☐ **退回** | {引用正文片段} |
| 3.4 | 段落呼吸 | 段落长短/节奏符合DNA段落呼吸规律 | ☐ 通过 / ☐ **退回** | {引用正文片段} |
| 3.5 | 叙事者距离 | 叙事者距离符合DNA层A设定 | ☐ 通过 / ☐ **退回** | {引用正文片段} |
| 3.6 | 对话引导词 | 对话引导词/留白符合DNA层A对话留白 | ☐ 通过 / ☐ **退回** | {引用正文片段} |
| 3.7 | 8020比例 | 展示/内省比例符合场景类型要求 | ☐ 通过 / ☐ **退回** | {引用正文片段} |

> 门禁：终验任一项无正文证据=退回重写。7项全部附证据才可通过。

## Checklist 4：导演意图验证（v3.5新增，红线❌3）

对照主会话注入的导演意图验证清单，逐项检查重写稿是否完成导演意图定义的5项质量维度。

> **关键：** revise 只接收验证清单（5项验证标准），不接收导演意图完整内容（创作决策不回传）。

| # | 验证项 | 验证清单标准 | 正文证据/偏差 | 结果 |
|:-:|:-------|:---------|:---------|:---------|
| 4.1 | 叙事功能是否匹配 | expected: {验证清单叙事功能} | {正文证据或偏差说明} | ☐ 通过 / ☐ 偏差 |
| 4.2 | 事件链是否覆盖 | expected_events: {核心事件列表} | found: {已出现} / missing: {缺失} | ☐ 通过 / ☐ 偏差 |
| 4.3 | 情绪曲线是否对齐 | expected_curve: {验证清单情绪曲线} | actual_curve: {实际情绪曲线} | ☐ 通过 / ☐ 偏差 |
| 4.4 | 子线是否推进 | expected_sublines: {子线列表} | advanced: {已推进} / not_advanced: {未推进} | ☐ 通过 / ☐ 偏差 |
| 4.5 | 章末钩子是否有 | expected_hook: {验证清单章末钩子} | actual_hook: {实际章末钩子} | ☐ 通过 / ☐ 偏差 |

**验证结果汇总：** {N}/5 通过

> 门禁（特殊，红线❌3）：5项全部通过=验证通过；任一不通过=**标注偏差项写入修订记录，不自动退回**——退回决策由主会话Step4决定

## Checklist 5：AI观感词清理

逐段扫描正文，记录命中：

| # | 检查项 | 命中标准 | 命中次数 | 命中段落 | 修正方式 |
|:-:|:-------|:---------|:--------:|:---------|:---------|
| 5.1 | 心理动词 | "他感到/他意识到/他仿佛" | {N}次 | {段落引用} | {改为展示} |
| 5.2 | 对比句式 | "不是…而是…" ≥ 2次 | {N}次 | {段落引用} | {减少或重写} |
| 5.3 | 解说员句式 | 叙事者解释设定 | {N}次 | {段落引用} | {改为对话/行动} |
| 5.4 | 视角越界 | 限知视角写非锚点内心 | {N}次 | {段落引用} | {删除越界} |

**命中类型总计：** {N}种

> 门禁：AI观感词命中 > 3种 = **退回重写**

## Checklist 6：字数终检（红线❌4）

| # | 检查项 | 标准 | 检查结果 | 处理 |
|:-:|:-------|:-----|:---------|:---------|
| 6.1 | 字数区间 | 2500-3500字 | ☐ 通过 / ☐ <2500退回create / ☐ >3500精简 | {字数}{处理} |
| 6.2 | 事件密度 | ≤15个事件/章 | ☐ 通过 / ☐ 标记过载 | {事件数} |

## context receipt（预留接口，批次2完整实现）

```yaml
context_receipt:
  received:
    - item_id: draft
      source: create产出正文初稿
      status: full
      size_chars: {N}
    - item_id: style_dna
      source: 写作资产/文风库/{书名}.md
      load_method: "Get-Content -Encoding UTF8 -Raw"
      status: full          # 硬阻塞，必须 full 且 0 误差
      truncated: false
      size_chars: {N}
    - item_id: l2_slice
      source: 写作参考/设定/主角引擎.md + 写作参考/设定/金手指.md + 幕纲活跃线索(主会话注入)
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

## 修订记录YAML

```yaml
revision_log:
  chapter: {章号}
  rewrite_mode: full
  
  rewrite:
    dna_loaded: true  # 或 false（硬阻塞终止）
    dna_load_method: "Get-Content -Encoding UTF8 -Raw"
    dna_truncated: false
    layer_a_check: "{层A整体风格检查结果}"
    layer_b_check: "{层B场景卡检查结果}"
    ratio_8020: "通过/退回（{比例描述}）"
    tail_continuity: "通过——重写稿开头与上章末尾自洽/需修正"
  
  fact_consistency:
    names: pass
    actions: pass
    event_order: pass
    dialogue_content: pass
    scenes: pass
    values: pass
    total: "6/6 通过"
    l2_slice_check:
      protagonist_engine: "符合——{说明}"
      golden_finger: "符合——{说明}"
      active_sublines: "符合——{说明}"
  
  dna_final_check:
    scene_card_formula: "通过——证据：[正文片段]"
    data_embed_format: "通过——证据：[正文片段]"
    sense_sequence: "通过——证据：[正文片段]"
    paragraph_breath: "通过——证据：[正文片段]"
    narrator_distance: "通过——证据：[正文片段]"
    dialogue_lead_words: "通过——证据：[正文片段]"
    ratio_8020: "通过——证据：[正文片段]"
    total: "7/7 通过（均附证据）"
  
  director_intent_verification:        # v3.5新增
    checklist_received: true
    1_narrative_function:
      expected: "{验证清单叙事功能}"
      result: pass                       # pass / deviation
      evidence: "[正文片段]"
      deviation: ""
    2_event_chain_coverage:
      expected_events: ["{核心事件列表}"]
      result: pass
      found_events: ["{正文中出现的事件}"]
      missing_events: []
      deviation: ""
    3_emotion_curve_alignment:
      expected_curve: "{验证清单情绪曲线}"
      actual_curve: "{重写稿实际情绪曲线}"
      result: pass
      deviation: ""
    4_sublines_advance:
      expected_sublines: ["{子线列表}"]
      advanced_sublines: ["{已推进子线}"]
      not_advanced: []
      result: pass
      deviation: ""
    5_chapter_hook:
      expected_hook: "{验证清单章末钩子}"
      actual_hook: "{重写稿实际章末钩子}"
      result: pass
      deviation: ""
    intent_verification_result: "5/5 通过"   # 或 "3/5 通过，偏差项：[...]"
    auto_rollback: false                       # 不自动退回，由主会话Step4决定
  
  ai_word_cleanup:
    psychology_verb: {命中次数}
    contrast_pattern: {命中次数}
    narrator_explain: {命中次数}
    pov_breach: {命中次数}
    total_types: {命中类型总计}
    gate: "通过(≤3种)/退回(>3种)"
  
  word_count_check:
    word_count_before: {修订前字数}
    word_count_after: {修订后字数}
    in_range: true
    event_density: {事件数}
    overload: false
  
  context_receipt:                          # 预留接口，批次2完整实现
    received: [draft, style_dna, l2_slice, director_intent_checklist, prev_chapter_tail]
    not_received: [director_intent, info_acquired, l2_card_full, state_snapshot]
    anomalies: []
  
  degraded_master_execution: false
```

## 门禁汇总

| 门禁项 | 检查结果 | 失败动作 |
|:-------|:---------|:---------|
| **文风DNA未完整加载/limit截断（红线❌1）** | ☐ 通过 / ☐ 硬阻塞 | **硬阻塞终止** |
| **重写时改写事实信息（红线❌2）** | ☐ 通过 / ☐ 退回 | **退回重写** |
| **导演意图验证5项（红线❌3，特殊）** | ☐ 全部通过 / ☐ 有偏差 | **标注偏差项写入修订记录，不自动退回——退回由主会话Step4决定** |
| **字数终检不在2500-3500字区间（红线❌4）** | ☐ 通过 / ☐ 退回/精简 | **<2500退回create；>3500强制精简渲染层** |
| **AI观感词命中>3种** | ☐ 通过 / ☐ 退回 | **退回重写** |
| **8020比例超标** | ☐ 通过 / ☐ 退回 | **退回重写** |
| **事实信息一致性6项任一不通过** | ☐ 通过 / ☐ 退回 | **退回重写** |
| **文风DNA终验7项任一无证据** | ☐ 通过 / ☐ 退回 | **退回重写** |

> 注意：导演意图验证（红线❌3）是唯一不触发自动退回的门禁——revise 完成验证并标注偏差后正常产出，退回决策权在主会话Step4。
