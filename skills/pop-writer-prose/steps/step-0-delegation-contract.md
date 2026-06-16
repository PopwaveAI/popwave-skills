# Step 0：父agent委托协议

> **定位**：当父agent（expert-writer 或 main loop）需要将 prose-render 任务 delegate 给子agent时的约束清单。
> **核心原则**：子agent自己加载 skill，父agent只传路径+门禁，不传过滤后的指令。

---

## 为什么需要这份协议

历史事故中，父agent delegate 时只凭自己理解写了"用遮天风格重构"，没有附带：
- 设计包原文事件列表 → 子agent不知道原文有什么，自创了战斗
- 上一章末尾段落 → 子agent不知道上一章结束状态，角色状态断裂
- 剧情不可变约束 → 子agent以为可以自由改编

**根因不是子agent能力不足，是父agent过滤了关键信息。** 本协议强制父agent传全所有必要字段。

---

## 父agent的职责（3件事）

### 1. 传路径矩阵

子agent需要以下路径才能自己加载 skill 和输入文件：

```yaml
design_pack: {项目}/写作资产/设计包v3/chXXX-设计包.md
style_dna: {项目}/styles/{风格名}.md
output: {项目}/正文/{风格名}/chXXX-{标题}.md
prev_chapter: {项目}/正文/{风格名}/ch{X-1}-{标题}.md  # 首章可略，标注 is_first_chapter: true
```

### 2. 传核心门禁

以下门禁必须逐条写在 delegate context 的显眼位置，不可隐藏在段落中：

```
门禁1: 【剧情不变】保留设计包/原文所有核心剧情事件，只改变叙事语言和风格。
       事件链是不可变更的骨架。不得自创原文不存在的战斗/场景/角色。
       不得改变事件的发生顺序。

门禁2: 【角色不可篡改】角色生死、关键状态（受伤/昏迷/觉醒等）不可改动。
       子agent不确定时 → 保持模糊，不自行决定。

门禁3: 【🔒标记原文照写】设计包中标注 🔒 的关键对白/数据必须逐字原文照写。
       不得替换、改写、缩写。
```

### 3. 传调用指令

子agent的入口指令（直接写在 delegate context 末尾）：

```
执行步骤：
1. skill_view('pop-writer-prose') — 全量加载 SKILL.md
2. skill_view('pop-writer-prose', 'steps/step-0-delegation-contract.md') — 确认本协议已读
3. skill_view('pop-writer-prose', 'steps/step-1-read-input.md')
4. skill_view('pop-writer-prose', 'steps/step-2-render.md')
5. skill_view('pop-writer-prose', 'steps/step-3-verify.md')
6. skill_view('pop-writer-prose', 'steps/step-4-output.md')
7. 按 step-1 ~ step-4 的顺序执行渲染
```

---

## 多章渲染时的额外要求

### 顺序渲染（推荐）

每章独立委托，父agent逐一发出。每章委托 context 中：
- `prev_chapter` 指向上一章刚写好的文件路径
- 子agent在 step-1 中自动读上一章末尾500字

### 并行渲染（仅当各章剧情无强依赖时可用）

当且仅当满足以下条件时才可并行：
- 各章时间线不重叠
- 角色不跨章移动
- 无因果关系（ch03 不依赖 ch02 的结果）

并行时，父agent必须为每个子agent准备 **章节连续性摘要**：

```yaml
chapter_continuity_summary:
  chapter_number: {N}
  title: {标题}
  previous_chapter_end:
    time: {上章末尾时间}
    location: {上章末尾地点}
    protagonist_state: {主角状态}
    companion_state: {配角状态}
    last_scene: {上章最后一幕简述}
  this_chapter_start:
    time_offset: {距离上章末尾的时间间隔}
    starting_point: {本章起始事件简述}
```

### 红线

- ❌ 不得多章合并为一个文件输出。每章独立 `ch{XX}-{标题}.md`
- ❌ 不得在委托指令中使用"用XX风格重构"等模糊表述 → 必须附加门禁1（剧情不变）
- ❌ 并行渲染时每个子agent必须获得 `chapter_continuity_summary`
- ❌ 父agent不可自行"总结"skill的步骤写入context——让子agent自己读 step 文件
- ❌ **父agent不可从DNA中提取"替换规则"写入context** — DNA是风格参考，不是内容改写手册。正确做法是：
  - ❌ 坏的："把潜行暗杀改为轻功步法"
  - ❌ 坏的："将数据面板改为丹田修行语言"  
  - ✅ 好的：将DNA路径传给子agent，让子agent自己读原文感受笔触
  - ✅ 好的：需要补充规则时，应描述**叙事属性**（节奏快慢/句子长短/距离远近）而非**内容替换**（A改成B）

---

## 父agent自检清单

发出 delegate 前逐项确认：

| # | 检查项 | 通过 |
|:-:|:-------|:----:|
| 1 | 路径矩阵四字段是否齐全（design_pack/style_dna/output/prev_chapter） | □ |
| 2 | 门禁1-3是否已写入 context 的显眼位置 | □ |
| 3 | 子agent入口指令(7步骤)是否已写入 context | □ |
| 4 | 如并行渲染：每个子agent的 continuity_summary 是否已准备 | □ |
| 5 | 是否标注了 is_first_chapter（首章）/ 提供了 prev_chapter（续章） | □ |
| 6 | 是否已用 skill_view 读过本文件（step-0-delegation-contract.md）全文 | □ |

**6项全部通过 → 方可发出 delegate。缺任何一项 → 退回补全，不可绕过。**
