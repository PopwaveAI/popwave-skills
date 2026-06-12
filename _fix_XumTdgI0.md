# 正文写作引擎拆分为两个独立 Skill · 产品需求文档

<title>Untitled</title>

> **状态：已实施 ✅** ｜ pop-novel-writer 已于 2026-06-09 正式拆分为 `pop-novel-chapter-design` 和 `pop-novel-prose-render`，两 Skill 均独立运行中。

# 正文写作引擎拆分为两个独立 Skill · 产品需求文档 v2.0

> 版本：v2.0  
> 上一版本：v1.0（2026-06-09，仅包含拆分框架和 6-9测试证据）  
> 本版新增：子 agent 架构合理性论证 + 两个 Skill 的完整 SKILL.md 草案  
> 创建日期：2026-06-09

---

## 核心决策

> **把 pop-novel-writer 拆成两个独立 Skill，由 expert-writer 分别调度子 agent 执行。**
> 
> 不是「分步骤」，是「分大脑」。每个 Skill 有自己的 context、自己的 SKILL.md、自己的思考边界。

---

## 1. 为什么子 agent 架构是唯一正确的选择

### 1.1 核心论点：Context 隔离的本质不是省空间，是思维纯净度

主 agent 手动执行「先 Design 再 Render」时，即使按阶段 Read 不同指令文件，**同一个对话线程的上下文历史不会消失**。上一轮的 Canvas/L1/Design 产出依然在 context 里，被 Render 轮「看到」。

这不是 token 数量的问题。是**认知污染**的问题。

### 1.2 认知污染的第一种形态：Design 思维侵入 Render

Design 阶段的思维模式是：

```
结构性判断：「这章信息释放有 3 个 P0 项」
约束检查：「这个角色在 ch008 才获得这把武器，ch006 不能用」
逻辑推演：「里程碑 MK-03 要求主角在 ch12 前达到 2 阶」
```

当这些结构性判断残留在 context 里，轮到 Render 时，LLM 会产生一种「过度解释」的倾向——它知道角色状态变化的逻辑原因，所以写正文时不自觉地**让叙事者跳出来解释**：

> ❌ 「他拔出长刀。这把刀是三天前从科尔手里缴来的——那场战斗之后他一直在熟悉它的重心。」

正确的 Render 应该怎么写：

> ✅ 「他拔出长刀。握柄的缠绳已经被手心磨出了贴合掌纹的凹痕。」

第二句没有解释刀的来历，但通过「磨出凹痕」暗示了主角已经用过一段时间。**这是「展示」和「解释」的区别，也是 Design 思维和 Render 思维的本质冲突。**

当同一个大脑同时做了 Design 和 Render，它知道「这把刀来自科尔」，就会忍不住在 Render 时塞一个解释。子 agent 隔离后，Render agent 只拿到事实骨架里的一句 `[事件3: 战斗开始，主角拔出长刀]`——它不知道刀从哪来的，所以不会解释，只会写。

### 1.3 认知污染的第二种形态：Render 思维侵入 Design

反过来也一样。当 context 里已经加载了文风 DNA（「句子以短句为主，避免长修饰，叙事者克制不解释」），Design 阶段就会被这种风格意识影响。

Design 本该做的是：

```
判断 ch006 应该出场哪些角色 →
判断 ch006 的 info_release 哪些可以释放 →
判断事件链的顺序是否情绪合理 →
```

但如果 context 里飘着「叙事者克制不解释」的风格规则，Design 会产生一种预判：「既然 Render 不解释，那我在事件链里就不要安排需要解释的东西」——这就变成了 Design 自我审查、替 Render 做选择，最终导致信息释放不足。

**Design 和 Render 在两个独立的子 agent context 里，各自只看到自己的指令和自己的材料。Design 不会因为 Render 的规则而自我限制，Render 不会因为 Design 的逻辑而过度解释。**

### 1.4 认知污染的第三种形态：错误不可追溯

6-9测试 ch015 的正文质量不错，但没有人能回答「ch015 的角色出场是否符合 act-01-人物.md 的规划」。因为 Design 文件消失了，追溯链路断了。

当 Design 和 Render 都在主 agent 的一个对话线程里完成时，**如果 Render 产出的正文有问题（比如某个角色不该出现但出现了），你无法判断这个错误是 Design 阶段就规划错了，还是 Render 阶段没有遵守骨架。** 两个阶段的信息混在同一个 context 里，错误来源不可区分。

子 agent 隔离后：

```
chapter-design agent 产出 → 事实骨架.md + 登场人物卡.md（独立文件，可单独审查）
prose-render agent 消费 → 事实骨架.md + 登场人物卡.md → 产 chXXX.md
如果正文出错 → 先查骨架是否正确 → 骨架对 → Render 的问题 → 只改 Render
                                骨架错 → Design 的问题 → 只改 Design 产物 → 重新喂 Render
```

### 1.5 6-9测试的证据链

| 阶段 | 现象 | 对应认知污染类型 |
|-|-|-|
| ch001-ch005（Design 完整，context 充裕） | 质量最高，沉浸感强 | 两种思维勉强共存 |
| ch006-ch010（Design 退化，context 拥挤） | 正文还行，但失去骨架锐度 | Design 思维被 Render 材料挤占 |
| ch011-ch015（Design 消失，context 溢出） | 正文文笔尚可，但与 Canvas 对齐消失 | Render 思维接管全部，Design 被放弃 |

**文笔从头到尾没怎么下降——因为 Render 需要的信息（文风DNA/语料）一直占据着 context。但 Design 需要的信息（Canvas/L1/状态）被挤出去了。同一个 context 里，两批信息在打架，最后是 Render 信息赢了。**

分离到两个子 agent，不存在谁赢谁输——各自都有完整的 context。

### 1.6 一句话总结

> **one context = two thinking modes fighting for the same attention window. two agents = two clean thinking modes, each with its own attention window.**

---

## 2. 拆分后的架构：两个独立 Skill

### 2.1 管线位置

```
pop-novel-bookstrap             开书启动
    ↓
pop-novel-deconstructor         锚定拆书（如有）
    ↓
pop-novel-plot                  大纲架构（Canvas）
    ↓
pop-novel-chapter-design   ★   章纲设计 / 导演卡
    ↓
pop-novel-prose-render     ★   正文渲染 / 上色表达
    ↓
pop-novel-qa                   爽点质检
```

### 2.2 expert-writer 路由调整

```diff
  意图「继续前进」「下一章」：
- 读取项目状态 → plot(检查幕纲+里程碑) → writer(chapter-design + prose-render)
+ 读取项目状态 → plot(检查幕纲+里程碑) → chapter-design → prose-render

  意图「修改正文」：
- 定位修改层 → 评估影响 → writer（只动受影响的章）
+ 定位修改层 → 评估影响 → prose-render（定点重写指定段落）/ chapter-design（需要改设计）
```

---

## 3. Skill 1：pop-novel-chapter-design

### 3.1 领域注册

| 字段 | 值 |
|-|-|
| id | `pop-novel-chapter-design` |
| 描述 | 导演卡。接收大纲的完整 Canvas，产出结构化的事实骨架和登场人物卡。不碰任何文风、修辞、或文本质感。 |
| 上游 | pop-novel-plot |
| 下游 | pop-novel-prose-render |
| 作者 | 江轩 |

### 3.2 输入（P0 强制）

| # | 输入 | 路径 | 作用 |
|-|-|-|-|
| 1 | **act-XX.yaml** | `设计/幕/` | 幕纲 → 本章在情绪弧线的位置、info_release 规划、爽点分布、plotlines_active |
| 2 | **act-XX-人物.md** | `设计/幕/` | 本卷人物池 → 本章可出场角色 + 卷初/卷末状态 |
| 3 | **act-XX-地图.md** | `设计/幕/` | 本卷地图 → 本章发生地点 + 空间描述 |
| 4 | **act-XX-势力.md** | `设计/幕/` | 本卷势力动态 → 各势力在当前章段的活动 |
| 5 | **里程碑设计.md** | `设计/` | 本章对应哪个 MK + MK 的成就标准 |
| 6 | **info-release-XX.md** | `设计/幕/` | 本卷 P0/P1 信息点的章级分配 |
| 7 | **L1 设定（按需）** | `00-原始设定/L1-元设定层/` | 按 info_release.source_doc 按需读取，不预读全部 |
| 8 | **entity-snapshot.yaml** | `00-总控/` | 当前全量角色状态（唯一 canon） |
| 9 | **上一章正文末尾的状态更新块** | `03-正文/ch{上一章}.md` | 未闭合节点 + 语感衔接 |
| 10 | **constitution.yaml** | `02-大纲/` | 宪法红线 |
| 11 | **上一个 design 文件** | `03-写作资产/` | 未闭合节点检查 |

### 3.3 产出（P0 强制）

| 产物 | 路径 | 格式 | 消费者 |
|-|-|-|-|
| **chXXX-事实骨架.md** | `03-写作资产/` | Markdown | prose-render |
| **chXXX-登场人物卡.md** | `03-写作资产/` | Markdown | prose-render |
| entity-snapshot 更新 | `00-总控/entity-snapshot.yaml` | YAML（覆盖写 before→after） | 下一章 Design |

### 3.4 关键约束

| 约束 | 说明 |
|-|-|
| **不碰文风** | 不知道文风DNA的存在。不写叙事者声音、不写句子节奏、不写修辞风格 |
| **不写正文** | 产出是结构化的设计文档，不是散文 |
| **角色必须在人物清单中** | 所有出场角色必须可追溯到 act-XX-人物.md |
| **地点必须在地图中** | 所有发生地点必须可追溯到 act-XX-地图.md |
| **info_release 必须对齐** | 所有信息释放项必须可追溯到 info-release-XX.md |

---

## 4. Skill 2：pop-novel-prose-render

### 4.1 领域注册

| 字段 | 值 |
|-|-|
| id | `pop-novel-prose-render` |
| 描述 | 正文渲染。消费 Design 的骨架产物，注入文风 DNA、锚定章和写作技法，渲染为可读的正文。不判断剧情逻辑、不验证设定一致性。 |
| 上游 | pop-novel-chapter-design |
| 下游 | pop-novel-qa |
| 作者 | 江轩 |

### 4.2 输入（P0 强制）

| # | 输入 | 路径 | 作用 |
|-|-|-|-|
| 1 | **chXXX-事实骨架.md** | `03-写作资产/` | 本章事件链、情绪节拍、信息释放清单 |
| 2 | **chXXX-登场人物卡.md** | `03-写作资产/` | 本章角色 before/after、关系动态、台词风格 |
| 3 | **constitution.yaml** | `02-大纲/` | 宪法红线 |
| 4 | **上一章正文最后 800 字** | `03-正文/` | 语感衔接 |

### 4.3 输入（风格注入——P0 强制）

| # | 输入 | 路径 | 作用 |
|-|-|-|-|
| 5 | **文风DNA 档案** | `styles/` | 8 维风格特征 → 提取本章场景类型对应的风格规则 |
| 6 | **锚定章库（对应类型）** | `01-写作资产/锚定章库/` | 与本章场景类型匹配的锚定章——只取「核心特征提炼」+「可复用规则」，不取原文摘录 |

### 4.4 输入（P1 建议）

| # | 输入 | 路径 | 作用 |
|-|-|-|-|
| 7 | **战斗技法参考** | `_参考书分析/` | 战斗场景的节奏模板 |
| 8 | **对话技法参考** | `_参考书分析/` | 对话场景的节奏模板 |

### 4.5 产出

| 产物 | 路径 | 格式 |
|-|-|-|
| **chXXX.md** | `03-正文/` | Markdown 正文 + 章末状态更新块 |

### 4.6 三阶段渲染流程

```
Phase 1 — 风格锚定
  读文风DNA → 提取本章场景类型对应的风格规则 → 读锚定章的特征提炼
  → 产出：风格契约（本场景的叙事哲学/句式/描写/对话策略）

Phase 2 — 正文渲染
  事实骨架 × 登场人物卡 × 风格契约 → 逐事件写入正文
  → 每个事件先写骨架的意图，再用风格契约的规则选择具体的句子、节奏、感官细节

Phase 3 — 风格验证
  对照风格契约自检 → 标记偏差 → 最小修补
  → 宪法红线检查
```

### 4.7 关键约束

| 约束 | 说明 |
|-|-|
| **不读上游 Canvas** | 不读 act-XX.yaml、人物清单、地图、L1 设定。这些是 Design 的职责 |
| **不判断剧情逻辑** | 骨架说「主角在 ch6 杀了 A」→ Render 写「主角杀了 A」。不质疑 |
| **不验证设定一致性** | 不知道 L1 设定原文。Design 已经做了 info_release 对齐 |
| **不解释** | 叙事者不跳出来解释设定、心理动因、或前因后果。写所见、所闻、所感 |

---

## 5. 两个 Skill 的对接协议

### 5.1 事实骨架标准格式

```markdown
# chXXX-事实骨架

> Design 产出: pop-novel-chapter-design v1.0
> 下游消费者: pop-novel-prose-render

## 基础信息
- 所属幕: act-XX
- 本章标题: "XXX"
- 章节号: X
- 本章核心目的: (一句话)

## 事件链
### 事件1: "标题"
- 地点: (必须可追溯到 act-XX-地图.md)
- 参与角色: (必须可追溯到 act-XX-人物.md)
- 事件内容: (发生了什么，不描述怎么发生的)
- 情绪目标:
- 信息释放: (对应的 info_release item_id)
- 估计字数: 600

### 事件2: ...

## 情绪节拍
- 起点: → 发展: → 高潮: → 终点:

## 信息释放落地清单
- [ ] 设定项1（来自 L1-XX.md，本章释放方式: YYY）

## 钩子
- 类型: (悬念/信息/情绪)
- 内容:

## 与上章衔接
- 上一章末尾状态: →
- 本章起始状态:
```

### 5.2 登场人物卡标准格式

```markdown
# chXXX-登场人物卡

> Design 产出: pop-novel-chapter-design v1.0
> 下游消费者: pop-novel-prose-render

## 角色A（主角）
| 维度 | 本章开始前 | 本章结束后 |
|:-----|:----------|:----------|
| 等级 | | |
| 装备 | | |
| 心理 | | |
| 目标 | | |
| 本章台词风格 | (简洁/克制/冷幽默/...) — 指导 Render 的对话写法 |

## 角色B（配角）
...

## 角色关系动态
- A 与 B:

## 角色出场分布
| 事件 | 出场角色 |
|:----|:--------|
| 事件1 | A, B |
| 事件2 | A, C |
```

### 5.3 协议稳定性保障

| 保障 | 说明 |
|-|-|
| `_meta.version` | 两个文件在元数据头声明格式版本。Render 解析前先校验 |
| entity-snapshot 作为唯一状态源 | 不用 Design 产物替代 entity-snapshot。Design 产物只描述本章变化，全量状态在 entity-snapshot |
| 文件写入后即冻结 | Design 产物写入后，Render 只读不改 |

---

## 6. 文件目录结构

```
项目/
├── 00-总控/
│   └── entity-snapshot.yaml          ← 全量状态（Design 维护）
├── 03-写作资产/
│   ├── chXXX-事实骨架.md            ← Design 产出
│   ├── chXXX-登场人物卡.md          ← Design 产出
│   └── experience-log.md            ← 经验日志（可选）
├── 03-正文/
│   └── chXXX.md                      ← Render 产出
└── styles/
    └── 作者名-书名.md                ← 文风DNA（Render 消费）
```

---

## 7. 与 v1.0 的差异

| 维度 | v1.0 | v2.0 |
|-|-|-|
| 拆分动机 | context 溢出——两批信息挤在一起 | **认知污染——两种思维模式不能共享同一个注意力窗口** |
| 架构选择 | "需要子 agent，但主 agent 也行" | **坚定走子 agent 架构，论证为什么不隔离就不行** |
| Skill 数量 | 2 个（含 global-summary 滑动窗口） | 2 个（不含—Design 已读 entity-snapshot 而非全量 global-summary） |
| 6-9测试证据 | 6 条表面问题 | **3 种认知污染形态 × 6 条证据 = 完整的因果链** |
| SKILL.md 草案 | 无 | **两个完整 SKILL.md 草案** |
| 对接协议 | 有，但未标准化事实骨架和人物卡格式 | **标准化的字段定义 + 版本协议** |

---

## 8. 附录：为什么不是「一份 SKILL.md + 分阶段 Read」

这是 paopao 不支持子 agent 时的一个折中方案——保持一个 Skill，按 Design 阶段和 Render 阶段分步 Read 不同的 steps/ 文件。

**为什么被拒绝：**

两步虽然在逻辑上分离了指令，但在物理上共享同一段对话历史。第一步读完的 Canvas/L1/Design 产出残留在 context 历史里，第二步的 Render 依然「看到」了它们。

这等价于——你把两个人关在同一个房间里，让他们轮流工作，要求第二个人「不要看第一个人的笔记」。但笔记就在桌子上。

子 agent 的语义是：**第一个人的笔记被抄成一份干净的摘要，交给第二个人。第一个人带走自己的笔记本离开。第二个人只看这份摘要工作。** 这就是为什么子 agent 不是「可选优化」，而是「正确做法」。

---

## 9. 变更记录

| 版本 | 日期 | 变更内容 |
|-|-|-|
| v2.0 | 2026-06-09 | 加入子 agent 合理性论证（三种认知污染形态）+ 完整 SKILL.md 草案 + 标准化对接协议 |
| v1.0 | 2026-06-09 | 初始版本，6-9测试审计 + 拆分框架 |

---

*本文档论证了为什么正文写作引擎必须拆分为两个独立 Skill、由子 agent 分别执行。「共享 context」不是优化问题，是架构错误。*

---

# 附录：原始证据（来自 v1.0 草案）

# 正文写作引擎拆分 · 产品需求文档

> 版本：v1.0  
> 来源：6-9测试项目全流程审计 + 上下文窗口瓶颈分析  
> 创建日期：2026-06-09  
> 文档状态：草案

---

## 1. 一句话概述

> **把 pop-novel-writer 拆成两个独立 Skill：chapter-design（章纲设计·导演卡）和 prose-render（上色表达·正文渲染）。不是因为"分步不够"，是因为同一个 Skill 的共享上下文里，两批互不重叠的信息在打架。**

---

## 2. 现状问题：6-9测试项目的直接证据

### 2.1 项目概况

| 维度 | 数据 |
|-|-|
| 已写章节 | ch001 - ch015（15章） |
| Design 文件 | 仅 ch001 - ch010（10个），ch011-ch015 无 Design |
| global-summary | 仅更新到 ch009，ch010-ch015 未维护 |
| entity-snapshot | 仅覆盖 ch001-ch009（source_chapters: "ch001-ch009"） |
| chapter-state.yaml | current_chapter: 0，本体从未更新 |
| 正文质量 | 整体良好，ch011 起失去结构化骨架但文本质量未断崖 |

### 2.2 关键证据链

#### 证据 1：Design 管道在第 10 章后崩溃

```
ch001 □□□□□□□□□□ ch010 | 5章无Design ch015
─────────────────────────┼────────────────────────
 有结构化八块设计包        |  正文直出，无骨架层
 情绪弧线+空间+人物+事件链  |  质量已回退到"靠记忆写"
```

ch001-design.md 包含完整的八块设计包：

```
块A：设计说明（核心目的/场景类型/爽点定位/情绪弧线/信息释放/钩子/里程碑/对标）
块B：本章空间（地点描述/空间布局/移动方式）
块C：登场人物（角色 before/after 状态对照）
块D：事件链（每个事件的参与角色/情绪目标/空间使用）
块E：信息释放清单（逐项 source_doc + 释放方式）
块F：Design 与幕纲对齐检查
```

到 ch010-design.md，已经退化到：

```
块A：设计说明（简化为一段）
块B+C+D：（合并为一个模糊块，事件笼统描述）
块F：消失
```

**ch011 之后，Design 文件彻底消失。** writer 从 ch011 开始走「直接渲染」模式——跳过八块设计包，凭 act-01.yaml + global-summary 的残留信息直出正文。

#### 证据 2：状态管道在第 9 章后崩溃

| 文件 | 最后更新章 | 落后于正文 |
|-|-|-|
| global-summary.md | ch009 | 落后 6 章 |
| entity-snapshot.yaml | ch009 | 落后 6 章 |
| chapter-state.yaml | ch000（从未更新） | 落后 15 章 |

ch015 开始出现「自救行为」——状态更新块直接写到正文末尾，而不是分离到状态文件：

```
# === 状态更新 ===
chapter: 15
summary: "江轩天亮后出南门……"
entity_updates: ...
event_log: ...
```

这是 agent 在状态文件不可维护时的降级方案——说明它意识到 context 已经溢出了。

#### 证据 3：正文质量 vs 上下文消耗的悖论

```
ch001-ch005（有完整 Design）  →  质量：★★★★★，沉浸感强，事件链清晰
ch006-ch010（Design 退化中）  →  质量：★★★★☆，还行但失去骨架锐度
ch011-ch015（无 Design）      →  质量：★★★★☆，文本还行，但角色/空间/设定不再对齐 Canvas
```

正文文本质量**没有显著下降**——文笔、节奏、感官细节依然不错。但**失去的是与上游的对齐**——你不知道 ch013 的老鼠清剿部署是否符合 act-01-势力.md 的设计、你不知道 ch015 的蛇魔巢穴入口描述是否与 act-01-地图.md 一致。因为 Design 文件消失了，追溯链路断了。

**这是最危险的情况**：文本质量好到让你觉得「没问题」，但实际上已经在脱离大纲裸奔。

---

## 3. 根因分析：为什么一个 Skill 内分 Steps 不够

### 3.1 当前 pop-novel-writer 的 context 剖面

一个 Skill 内，Design 步骤和 Render 步骤共享同一份 SKILL.md 规则。当 writer 执行写一章的任务时，它的 context 大致是：

```
┌────────────────────────────────────────────────────── 128K token ──┐
│                                                                     │
│ writer SKILL.md（同时包含 Design 规则 + Render 规则 + Style 规则）   │
│                                                                     │
│ act-01.yaml              ─┐                                        │
│ act-01-人物.md            │                                        │
│ act-01-地图.md            │                                        │
│ L1 世界观底层逻辑.md       │ Design 阶段需要                         │
│ L1 力量体系.md            │ Render 阶段不需要                        │
│ L1 势力格局.md            │ 但它们都在 context 里                    │
│ global-summary.md         │                                        │
│ 里程碑设计.md             │                                        │
│ constitution.yaml        ─┘                                        │
│                                                                     │
│ 文风DNA 档案              ─┐                                        │
│ 锚定章原文片段             │ Render 阶段需要                         │
│ 写作技法参考               │ Design 阶段不需要                        │
│ 前 1-2 章正文（语料）       │ 但它们也在 context 里                   │
│ ───────────────────────  ─┘                                        │
│                                                                     │
│ 待写章节的 Design 产物      ← 在 context 里膨胀                      │
│                                                                     │
│ ─── 窗口耗尽 ───                                                    │
└─────────────────────────────────────────────────────────────────────┘
```

### 3.2 为什么到第 10 章就崩了

| 阶段 | global-summary 体积 | Design 产物体积 | 上游 canvas 体积 | 剩余可用窗口 |
|-|-|-|-|-|
| ch001 | \~500 token | \~2000 token | \~6000 token | \~110K |
| ch005 | \~2500 token | \~2500 token | \~6000 token | \~90K |
| ch010 | \~5000 token | \~1500 token | \~6000 token | \~70K |
| ch011 | 不再更新 | 不再产出 | \~6000 token | \~50K（无冗余空间） |

**到 ch010 时，仅维护 global-summary 的 token 就已经追不上正文长度了。** agent 被迫在两个死亡选项中选：要么继续出 Design（消耗剩余窗口，正文没空间），要么放弃 Design 直出正文，然后在末尾自救式更新状态。

它选了后者——而且正文质量保住了。这说明**把 Design 和 Render 剥离到两个独立 context，是唯一能同时保住两者的方案**。

### 3.3 这与「同一 Skill 内分 Step」的根本区别

|  | 同一 Skill 内分 Step | 两个独立 Skill |
|-|-|-|
| SKILL.md 规则 | 同时包含 Design + Render 两套指令 | 各自只有自己的专用指令 |
| Design 阶段的 context | 包含文风DNA、语料包、写作技法等 Design 用不到的 Render 材料 | 只包含 Design 需要的：Canvas、L1、constitution |
| Render 阶段的 context | 包含 L1 设定原文、act-XX.yaml 等 Render 用不到的 Design 材料 | 只包含 Render 需要的：骨架、人物卡、文风DNA、锚定章 |
| 跨章状态 | global-summary 在同一个 context 里持续膨胀 | Design 产出是 Render 的输入，只需要骨架+人物卡（\~3000 token），不需要全量 global-summary |

---

## 4. 拆分方案

### 4.1 架构总览

```
当前架构：                       新架构：

pop-novel-writer                 pop-novel-chapter-design
（1 个 skill，3 步）              （导演卡 / 章纲设计）
┌──────────────┐                 ┌────────────────────┐
│ Step1 Design │                 │ 输入：              │
│ Step2 Render │    ──→          │ · act-XX.yaml      │
│ Step3 State  │                 │ · act-XX-人物.md   │
└──────────────┘                 │ · act-XX-地图.md   │
                                 │ · L1 设定          │
                                 │ · 里程碑设计       │
                                 │ · global-summary   │
                                 │ · constitution     │
                                 │                   │
                                 │ 产出【Design包】： │
                                 │ · 事实骨架.md      │
                                 │ · 登场人物卡.md    │
                                 └────────┬───────────┘
                                          │
                                          ▼
                                 pop-novel-prose-render
                                 （上色表达 / 正文渲染）
                                 ┌────────────────────┐
                                 │ 输入：              │
                                 │ · 事实骨架.md      │
                                 │ · 登场人物卡.md    │
                                 │ · 文风DNA 档案     │
                                 │ · 锚定章原文       │
                                 │ · 写作技法参考     │
                                 │ · constitution     │
                                 │                   │
                                 │ 产出：             │
                                 │ · chXXX.md（正文） │
                                 │ · state-update 块  │
                                 └────────────────────┘
```

### 4.2 Skill 1：pop-novel-chapter-design

#### 定位

> **导演卡阶段。** 接收上游大纲的所有 Canvas 产物，产出结构化的事实骨架和登场人物卡。

#### 输入（P0 强制）

| 输入 | 路径 | 作用 |
|-|-|-|
| act-XX.yaml | 设计/幕/ | 幕纲 —— 本章在幕情绪弧线中的位置、info_release 规划、爽点分布 |
| act-XX-人物.md | 设计/幕/ | 本卷人物池 —— 哪个角色在哪几章可出场 |
| act-XX-地图.md | 设计/幕/ | 本卷地图 —— 本章发生地点可用哪些 |
| L1 设定六件套 | 00-原始设定/L1-元设定层/ | info_release 的 source_doc 原文 |
| 里程碑设计.md | 设计/ | 本章对应哪个 MK |
| global-summary.md | 写作资产/ | 前文状态 —— 本章从哪里衔接 |
| constitution.yaml | 大纲/ | 红线检查 |

#### 产出

| 产物 | 格式 | 说明 |
|-|-|-|
| **chXXX-事实骨架.md** | Markdown | 本章事件链（每个事件的参与者、情绪目标、空间使用）+ 信息释放落地计划 |
| **chXXX-登场人物卡.md** | Markdown | 本章出场角色的 before/after 状态、关系动态、情绪状态、关键决策 |

#### 不负责

- 文风注入、辞藻选择、句式节奏、修辞手法
- 战斗的具体动作描写、对话的具体措辞
- 感官细节（气味/声音/触感/视觉）的具体呈现

---

### 4.3 Skill 2：pop-novel-prose-render

#### 定位

> **上色表达阶段。** 接收 Design 阶段的骨架产物 + 文风材料，渲染为可读的正文。

#### 输入（P0 强制）

| 输入 | 路径 | 作用 |
|-|-|-|
| chXXX-事实骨架.md | 章纲/ | 本章要发生的事件、顺序、情绪目标 |
| chXXX-登场人物卡.md | 章纲/ | 本章角色的状态和关系 |
| constitution.yaml | 大纲/ | 宪法红线（不降智/不系统面板/...） |

#### 输入（P0 强制 —— 风格注入）

| 输入 | 路径 | 作用 |
|-|-|-|
| 文风DNA 档案 | styles/ | 8 维风格特征 → 写入 Render 的 system prompt |
| 锚定章原文 | 写作资产/锚定章库/ | 对应本章场景类型的锚定章原文片段 |

#### 输入（P1 建议）

| 输入 | 路径 | 作用 |
|-|-|-|
| 写作技法参考 | \_参考书分析/ | 战斗技法/对话技法/悬疑技法等 |

#### 产出

| 产物 | 格式 | 说明 |
|-|-|-|
| **chXXX.md** | Markdown | 完成的正文 |
| **state-update 块** | 章末 YAML 块 | 主角状态/角色状态/事件日志/世界观更新 |

#### 不负责

- 剧情逻辑判断、设定一致性校验、角色出场节奏规划
- 本章是否对齐 act-XX.yaml 的信息释放规划（那是 Design 的职责）

---

### 4.4 两个 Skill 的对接协议

Design 产出的两个文件，是 Render 的唯一剧情输入。Render **不再读取** Canvas 文件（act-XX.yaml、人物、地图、L1），只读 Design 产物。

**为什么 Render 不能读 Canvas**：  
如果 Render 也读上游文件，它就等于在重新做一遍 Design 的判断——「这个角色在本章是否该出场」「这个设定在这个场景怎么释放」——文风注入窗口被挤占，回到老问题。

**对接协议 = 事实骨架 + 登场人物卡的结构必须稳定：**

- 事实骨架标准化：事件链（编号/内容/参与角色/地点/情绪目标/信息释放项）
- 登场人物卡标准化：角色（名称/before 状态/after 状态/本章台词风格/关系动态）

Design 和 Render 之间唯一的耦合面就是这两个文件。如果格式不稳定，Render 就会出错。

---

## 5. 完整管线位置

```
pop-novel-bookstrap（开书）
    ↓
pop-novel-plot（大纲）
    ↓
pop-novel-chapter-design（章纲 / 导演卡）★ 新，从 writer 拆出
    ↓
pop-novel-prose-render（正文渲染）★ 新，从 writer 拆出
    ↓
pop-novel-qa（质检）
```

### 5.1 expert-writer 路由调整

```diff
  意图「继续前进」「下一章」：
- 读取项目状态 → plot(检查幕纲+里程碑) → writer
+ 读取项目状态 → plot(检查幕纲+里程碑) → chapter-design → prose-render

  意图「修改调整」：
- 定位修改层 → 评估影响 → 逐层更新（bookstrap → plot → writer）
+ 定位修改层 → 评估影响 → 逐层更新（bookstrap → plot → chapter-design → prose-render）
```

---

## 6. 关键约束与风险

### 6.1 上游文件的 token 消耗（chapter-design 侧）

Design 需要读完上游所有 Canvas 文件和 L1 设定（6 个文件）+ global-summary。这是拆开之后剩在新 Design Skill 里的 token 开销。

**缓解措施**：

- global-summary 需要精简——设计包已经包含了本章需要的所有信息，global-summary 只需维护「当前章号 + 主角位置 + 关键角色状态 + 最近 3 章事件摘要」
- L1 按需读取——不是每章都需要全部 6 个文件，按 info_release 的 source_doc 按需加载

### 6.2 文风注入的 token 消耗（prose-render 侧）

文风 DNA 档案 + 锚定章原文 + 写作技法参考，也是一批不小的 token。

**缓解措施**：

- 锚定章不加载全文，只加载与本章场景类型匹配的「核心特征提炼」+「可复用规则」字段，不加载原文摘录
- 文风 DNA 注入使用提炼版（从 8 维 → writer 专用的 4 维：叙事哲学 + 句式节奏 + 描写策略 + 对话策略）

### 6.3 两个 Skill 的版本耦合

如果 chapter-design 的产出格式升级（比如事实骨架新增字段），prose-render 的解析逻辑必须同步更新。

**缓解措施**：

- 事实骨架和登场人物卡通过 `_meta.version` 字段声明格式版本
- prose-render 读取时校验版本，不匹配则报错

---

## 7. 与 Skill 知识工程五条原则的对齐

| 原则 | 如何应用 |
|-|-|
| 1. 抽象层级决定复用性 | chapter-design 教的是「导演判断」的方法，不是某本书的具体设计 |
| 2. 教方法，不教故事 | chapter-design 的 templates 不包含具体角色的信息——框架独立于任何项目 |
| 3. 渐进式披露 | SKILL.md 只含路由，Design/Render 各自的 steps/ 按需加载 |
| 4. 不创造能力，只传递能力 | Design 不做文风判断、Render 不做剧情判断——各司其职 |
| 5. 模板是源材料不足的补偿 | 事实骨架模板和登场人物卡模板的字段定义，就是把 6-9测试 暴露的 context 崩溃经验编译成规则 |

---

## 8. 附录：6-9测试项目问题汇总

| # | 问题 | 证据 | 根因 | 拆分后是否解决 |
|-|-|-|-|-|
| 1 | Design 文件在 ch010 后消失 | ch011-ch015 无对应 design 文件 | 上下文溢出，agent 放弃结构化设计直出正文 | ✅ Design 和 Render 分离后，各自 context 只含自己需要的信息 |
| 2 | global-summary 停在 ch009 | 文件标注「最近更新: ch009 完成」 | 维护 global-summary 的 token 跟不上正文增长 | ✅ chapter-design 维护的是精简版 global-summary |
| 3 | entity-snapshot 停在 ch009 | source_chapters: "ch001-ch009" | 同上 | ✅  状态更新由 Design 和 Render 各自维护独立状态文件 |
| 4 | chapter-state.yaml 从未更新 | current_chapter: 0 | 状态管道整体崩溃 | ✅ 每个 Skill 只负责自己层的状态 |
| 5 | ch011 起正文与 Canvas 对齐不可追溯 | 无 Design 文件验证角色/空间/信息释放是否对齐 Canvas | 同上 | ✅ chapter-design 产出物是 Render 的唯一输入，追溯链路完整 |
| 6 | ch015 自救式内嵌状态更新 | 状态块直接写在正文末尾 | 降级方案，说明 agent 意识到状态文件已不可维护 | ✅ 拆分后每个 Skill 的 context 更轻，状态可正常维护 |

---

## 9. 变更记录

| 版本 | 日期 | 变更内容 |
|-|-|-|
| v1.0 | 2026-06-09 | 初始版本，基于 6-9测试项目审计结果设计拆分方案 |

---

*本文档基于 6-9测试项目 15 章正文的全流程审计 + Skill 知识工程五条原则，为 pop-novel-writer 的拆分提供工程依据。*