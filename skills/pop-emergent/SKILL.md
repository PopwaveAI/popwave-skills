---
name: pop-emergent
description: Pop 涌现式小说调度入口。用于用户请求涌现式写作、seed共创、research写作燃料、正文锚定写作、质量review、AI味审稿、复盘沉淀时，按 seed -> research -> write -> review 路由到四个执行 skill：pop-emergent-seed、pop-emergent-research、pop-emergent-write、pop-emergent-review；不进入正式 world/plot/create 管线。
---

# Pop Emergent

这是涌现式小说入口 skill，只负责判断阶段、读取对应执行 skill、检查阶段边界。具体产物由四个执行 skill 完成。

## 执行 skill

| 阶段 | 执行 skill | 职责 |
| --- | --- | --- |
| seed | `skills/pop-emergent-seed/SKILL.md` | 碰撞 idea，形成全书/本轮种子文档 |
| research | `skills/pop-emergent-research/SKILL.md` | 找能进场面的本书涌现燃料和外部写作燃料 |
| write | `skills/pop-emergent-write/SKILL.md` | 读取 seed、research、正文锚定和项目状态，产出正文 |
| review | `skills/pop-emergent-review/SKILL.md` | 审 seed 兑现、爽文兑现、AI味，并沉淀涌现资产 |

## 路由

| 用户请求 | 路由 |
| --- | --- |
| 想 idea、做 seed、全书种子、方向碰撞 | 读取并执行 `pop-emergent-seed` |
| 找燃料、查资料、外部事件怎么入戏、世界观怎么接现实 | 读取并执行 `pop-emergent-research` |
| 写、续写、重写、把 X 写成 Y、开篇样章、单章爽文 | 读取并执行 `pop-emergent-write`；缺燃料时先执行 `pop-emergent-research` |
| 审稿、AI味、爽不爽、质量复盘、沉淀新增设定 | 读取并执行 `pop-emergent-review` |
| 跑完整涌现式 | 顺序执行 seed -> research -> write -> review |

## 调度规则

- 写作请求必须优先进入 `pop-emergent-write`，不得因为项目里已有草稿就自动改成 review。
- review 请求不得自动重写正文；用户要求修改后再进入 write。
- research 可以在 write 前自动补一轮轻量燃料，但不要写成长调研报告。
- seed 候选需要用户确认；用户明确说自动继续时才直接进入 research。
- 四个执行 skill 都使用 `formal / draft / trial` 执行模式，入口不得替它们伪造完成状态。
- 涉及真实项目落盘时，遵守执行 skill 的产物路径和“待确认/待冻结”边界。

### Research 触发规则

以下情况 write 前必须先执行 research：

- 新项目第一轮写作（无 seed/无燃料文件）。
- 跨世界观同人（如 BG3 × 战锤40K）：需 research 确认两个世界观的设定交集和冲突点。
- 涉及真实事件/技术/行业（如 DeepSeek R1）：需 research 确认事实细节。
- 距离上次 research 超过 5 章：需补一轮轻量 research。
- 用户明确要求查资料。

research 不需要长报告。目标是给 write 提供 3-5 条能进场面的燃料，每条有入戏方式、主角操作点、可外显爽点。

### 涌现资产分类存储

涌现日志禁止无限膨胀。按以下分类存储到 `涌现/` 目录：

```
涌现/
  seed-种子文档.md          # 种子（pop-emergent-seed 产出）
  research-写作燃料.md      # 燃料（pop-emergent-research 产出）
  review-沉淀.md             # 审稿沉淀（pop-emergent-review 产出）
  设定库.md                  # 冻结的设定（从 review 沉淀中确认纳入的）
  人物库.md                  # 冻结的人物状态
  剧情线.md                  # 冻结的剧情线追踪
  压缩归档/                  # 每10章压缩一次的历史记录
```

**每 10 章压缩一次**：把前 10 章的涌现日志压缩为一份摘要存入 `涌现/压缩归档/第1-10章摘要.md`，然后清空主日志只保留最近 10 章的详细记录。压缩时保留：
- 设定库/人物库/剧情线不受压缩影响（这些是累积的）
- 只压缩每章的详细新增设定、角色状态变化记录、剧情线推进记录
- 章末状态只保留最近一章的

全文加载协议加载优先级：设定库 > 人物库 > 剧情线 > 最近10章涌现日志 > 压缩归档摘要 > seed/燃料文件

## 红线

- 不调用正式 `pop-writer-v3-create` 处理涌现式试写。
- 不要求正式 plot 章级施工卡、章卡边界、微beat表；write 自己使用轻量"涌现写作包"。
- 不把 review 的沉淀直接冻结成正式设定，除非用户明确确认纳入项目。
- **禁止凭记忆写作**：write 执行前必须执行项目文件全文加载协议（见 pop-emergent-write SKILL.md），确保世界观/时间线/前序章节全文进入上下文。不允许"我之前读过"作为跳过理由。
- **禁止正文进对话历史**：正文写入 txt 文件，对话回复只给摘要+钩子。违反此条会导致上下文窗口被正文吃满，后续章节质量断崖。
- **禁止单章无限重写**：同一章重写超过 2 次后，降级为"试写-独立"处理，不得阻塞章节递进。
