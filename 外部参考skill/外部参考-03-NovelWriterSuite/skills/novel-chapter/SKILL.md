---
name: novel-chapter
description: 核心章节写作循环。9 步管线：outline → user_confirm → memory_load → write → self_check → fix_loop → memory_update → checkpoint → user_review。当用户说"写第 X 章"、"写下一章"、"继续写"、"接着写"、"重写第 X 章"、"write chapter N" 时触发。两阶段温度策略：写作时高温，自检和修复时低温。
---

# Novel Chapter —— 章节写作循环

## 功能

整合所有 skill 产出（story 圣经 / 角色 / 世界观 / 卷纲 / 写法 / 记忆 / 校稿）的核心写作管线。
执行严格的 9 步流程，每步有明确产出和强制门，跑通整本小说的逐章写作。

## 前置条件（写新章前必须满足）

1. `story.md` 存在且 brainstorm-done（即至少有简介、矛盾、30 章承诺）
2. `style/compiled/*.md` 至少有占位（可以未跑 style-engine，但要有 default 写作约束）
3. 当前卷有 `plot/arcs/{arc}-chapters.md` 或在 arc.md 里的 `## Chapter Outline` 段——即"卷级章节大纲"必须先做完
4. 至少有主角的 character 卡

如果不满足，**不要**强行进入。明确告诉用户缺什么、用哪个 skill 补。

## 9 步流程

### Step 6.1 - outline（单章章纲）

**输入**：用户说"写第 N 章"或"继续写"（自动 N+1）

**动作**：
1. 读取 `plot/arcs/{当前 arc}-chapters.md` 中第 N 章对应的章节大纲
2. 读取前 1 章正文（如不是第 1 章）
3. 检查连续性：
   - **时间**：本章是前章的什么时候？（当日 / 次日 / 数日后？章纲明确说了什么）
   - **位置**：前章结束时主角在哪？本章开头预定在哪？需要过渡吗？
   - **状态**：前章结尾主角是什么状态？本章开头要承接
   - **伏笔**：前章有什么 hook advance / planted 需要在本章衔接？

4. **生成单章章纲**（写到 `chapters/ch-{NNN}.md` 的 frontmatter 下方，但**还不写正文**）：

```markdown
---
chapter: 8
title: "雾林夜遇"
pov: sera-voss
location: whispering-vale-edge
arc: seras-reclamation
weight: ⭐⭐⭐
word-target: 3000-4000
status: outlined
created: 2026-05-20
---

## 本章章纲

- **时间**：前章后第二天黄昏
- **危机来源**：来自第 7 章 sera 决定加快赶路（这是隐患→ 暴露行踪）
- **核心冲突**：sera 第一次主动使用 ember 力量
- **主角抉择**：是否在斥候面前用 ember 暴露自己
- **抉择代价**：暴露 → 行踪传回 maren；不暴露 → 三人小队被擒
- **埋下隐患**：力量失控伤了 kael → 第 9 章兄妹关系裂痕
- **预定场景**：
  1. 黄昏扎营，与 kael 闲谈（500-800 字）
  2. 斥候迫近（800-1000 字）
  3. ember 失控 + 灼伤 kael（1200-1500 字）
  4. 善后 + 钩子（500-700 字）

## hook-账（预定）

### advance
- H001 sera 力量痕迹首次外显

### open
- [new] kael 第一次对 sera 表达恐惧 → 兄妹关系裂痕
```

### Step 6.2 - user_confirm（**强制门**）

> 借鉴 novel-writer 的强制确认。**不允许跳过**。

把上面生成的章纲展示给用户，**显式询问**：

```
✏️ 第 8 章章纲已生成（见上）。

请确认（任选）：
  - "确认章纲"（开始写作）
  - "改一下 {段}"（指出哪段要改）
  - "重新生成"（不满意，重做章纲）
```

**等待用户明确说"确认"**。在用户确认之前**绝对不能**进入 Step 6.3。

用户确认后：
- 把 `chapters/ch-{NNN}.md` 的 frontmatter status 改为 `outline-confirmed`
- 在 `status.md` 写入"Ch {N} 章纲已确认 - {time}"

### Step 6.3 - memory_load

调用 `novel-memory` 的 memory_load 操作，传入：
- chapter-number: N
- pov: 从章纲读
- expected-characters: 从章纲读
- expected-locations: 从章纲读

得到拼装好的 context blob（按 8 个 PRIORITY 分级，token 控制在 16-24k）。

### Step 6.4 - write（**高温**）

**温度建议**：0.7-0.8（具体由调用方控制，本 skill 不强制）

**prompt 组装**（按 AI-NWA 6 层 prompt 编译结构）：

```
[Layer 1: 世界与任务基础层]
{story.md 一句话简介 + 核心矛盾}
{当前 arc 一句话定位}
{本章章纲的全部内容}

[Layer 2: 写法主规则层]
{style/compiled/style-rules.md 的内容}

[Layer 3: 角色表达校正层]
{本章 POV 角色的 voice patterns（从 character 卡读）}
{本章其他出场角色的 voice 摘要}

[Layer 4: 反 AI 约束层]
{style/compiled/anti-ai.md 的内容}

[Layer 5: 输出格式层]
请输出本章正文。
- 字数：3000-4000 字
- 直接输出正文，不要标题不要解释
- 段落用空行分隔
- 章节末尾用 ## hook-账 段记录本章实际的 advance / resolve / open / defer

[Layer 6: 自检指令层]
写完后自检：
- 是否有"不是…而是…"句式 → 改写
- 是否有破折号 ——  → 改写
- 是否有元叙事词（读者可能 / 接下来）→ 删除
- 段落长度是否过于均匀 → 调整
若有违规，先修正再输出最终正文。
```

**Memory context** 拼在 Layer 1 之前作为背景资料。

**输出**：完整正文 + ## hook-账 段。写入 `chapters/ch-{NNN}.md` 的正文部分。

### Step 6.5 - self_check（**低温**）

**温度建议**：0.2-0.3

**动作**：跑 4 个客观脚本（在 `novel-review/scripts/` 中，本 skill 调用）：

```bash
python3 novel-suite/skills/novel-review/scripts/check_ai_tells.py --chapter chapters/ch-008.md
python3 novel-suite/skills/novel-review/scripts/check_post_write.py --chapter chapters/ch-008.md --vault {vault}
python3 novel-suite/skills/novel-review/scripts/check_hook_ledger.py --chapter chapters/ch-008.md --vault {vault}
python3 novel-suite/skills/novel-review/scripts/check_consistency.py --chapter chapters/ch-008.md --vault {vault}
```

汇总结果，得到 issue 列表：
- `critical` issues：必须修
- `warning` issues：建议修
- `info` issues：记录但不修

### Step 6.6 - fix_loop（最多 3 轮）

如果 self_check 有 `critical` issues，启动自动修复：

**修复 prompt**（沿用 AI-NWA AI 味修正任务模板）：

```
[原文]
{chapter content}

[检测到的违规]
{critical issues list}

[修正要求]
- 保留剧情事实不变
- 仅修改违规表达
- 保留 ## hook-账 段不动
- 修正后重新输出全文
```

**温度**：0.2（确定性高）

**循环**：
- 修复后再跑 self_check
- 仍有 critical → 再修复
- 最多 3 轮
- 3 轮后仍有 critical → 停下来，**告诉用户**"自动修复无法解决，请手动处理"，列出剩余 issues

修复成功 → 进 Step 6.7。

### Step 6.7 - memory_update

调用 `novel-memory` 的 memory_update 操作，传入：
- chapter-file: chapters/ch-{NNN}.md
- chapter-outline: 从 frontmatter 读

让它跑完 8 步流程（详见 `novel-memory/SKILL.md`），更新所有 .memory/ bank。

### Step 6.8 - checkpoint

调用：

```bash
python3 novel-suite/shared/checkpoint.py create --vault {vault} --name "chapter_{N}_complete"
```

把当前 vault 状态做个快照。便于后续如果用户反悔，可以 rollback。

### Step 6.9 - user_review（**强制门**）

把章节正文展示给用户，**显式询问**：

```
✅ 第 N 章已完成（{字数} 字）。

self_check 结果：
  - critical: 0 / warning: 2 / info: 1
  - 警告：{列出 warning，但用户可以选择忽略}

请确认（任选）：
  - "通过"（进入下一章 / 完成本卷）
  - "修改 {段}"（指出哪段要改 → 回到 Step 6.4 写部分）
  - "重写本章"（不满意 → 回到 Step 6.4 完全重写）
  - "重做章纲"（连章纲都要改 → 回到 Step 6.1）
```

**等待用户反馈**：
- 通过 → 更新 chapters/_index.md 注册，status 改为 `reviewed`，进入下一章
- 修改 → 把修改意见追加到 `.memory/revision-notes.md`，回到对应步骤
- 重写 / 重做章纲 → 同上

## 两阶段温度策略（重要）

| 步骤 | 温度 | 原因 |
|---|---|---|
| 6.1 outline | 0.5-0.6 | 章纲需要创意但不能跑偏 |
| 6.4 write | 0.7-0.8 | 写作需要创造力 |
| 6.5 self_check | 不调 LLM | 纯脚本检查 |
| 6.6 fix_loop | 0.2-0.3 | 修复要精确，不能"自由发挥" |
| 6.7 memory_update | 0.3-0.4 | 抽取事实，确定性优先 |

本 skill **不强制**温度参数（由调用方控制），但**建议**遵循上表。

## 错误处理

- **章纲未通过 user_confirm 就被打断**：保留章纲到 `chapters/ch-{NNN}.md`，status=outlined，下次 resume 直接从 Step 6.2 开始
- **write 后 self_check 不过且 fix_loop 3 轮也不过**：保留半成品到 `chapters/ch-{NNN}.md`，status=needs-manual-fix，明确告诉用户剩余 issues
- **memory_update 失败**：不要中断流程，记录到 `.memory/decision-log.md`，告诉用户"记忆更新部分失败，建议手动检查"
- **checkpoint 失败**：跳过，警告用户"无法创建快照，请手动 git commit"

## 与其他 skill 的边界

- **不创建章纲以外的资产**：不加角色 / 不加地点 / 不写新卷纲。只**触发**对应 skill 的建议
- **不修改 vault 元数据**（除 chapters / _index.md 和 status.md）：所有"长期记忆"修改通过 novel-memory
- **不做主观质量评判**：那是 user_review 的事

## 与 novel-init / novel-brainstorm 的关系

- 如果用户首次进入此 skill 但 vault 还没初始化 → 直接转交 novel-init
- 如果 vault 初始化了但 story.md 关键段（核心矛盾 / 30 章承诺）还没填 → 提示 brainstorm
- 如果 plot/arcs/ 是空的 → 提示先做 novel-plot 设计卷纲

## resume 逻辑

每次进入本 skill，先读 `status.md` 看当前状态：
- 没有 "Ch X 已完成" 记录 → 写 Ch 1
- 最后完成 Ch N → 写 Ch N+1
- 有 "Ch X 章纲已确认 - 未完成" → 从 Step 6.3 开始（章纲已 ok）
- 有 "Ch X needs-manual-fix" → 提醒用户处理，不自动续写
