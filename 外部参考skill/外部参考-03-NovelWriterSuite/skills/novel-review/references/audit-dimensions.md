# 校稿维度清单 —— 37 维

> 借鉴 inkos packages/core/src/agents/continuity.ts 的 DIMENSION_LABELS，独立重写并扩展。
> 4 维统计学由 Python 脚本（`check_ai_tells.py`）实现；其他维度由 LLM 评估。

---

## A 组 - LLM 评估，通用基础维度（17 维）

通用网文校稿，所有项目默认开启。

| ID | 名称 | 检查方法 | severity 标准 |
|---|---|---|---|
| 1 | OOC 检查 | 角色行为 / 对白 vs `characters/{x}.md` 的 voice patterns | critical: 严重失格 / warning: 轻微偏差 |
| 2 | 时间线检查 | 章节时间点 vs `plot/timeline.md` 是否冲突 | critical: 时间矛盾 / warning: 模糊 |
| 3 | 设定冲突 | 章节内容 vs `worldbuilding/` 是否冲突 | critical: 硬冲突 / warning: 软冲突 |
| 4 | 战力崩坏 | 角色力量动作 vs `worldbuilding/systems/{x}.md` 的等级 / 边界 | critical: 越级或破坏体系 |
| 5 | 数值检查 | 数字（年龄 / 距离 / 时间）的内部一致性 | critical: 明显矛盾 |
| 6 | 伏笔检查 | LLM 层（脚本已查关键词回声）；这里检查"伏笔债务升级" | warning: 核心 hook 超 10 章未推进 / critical: 超 20 章 |
| 7 | 节奏检查 | 跟 `pacing-principles.md` 的节奏波形（蓄压→升级→爆发→后效）对比 | warning: 偏离 |
| 8 | 文风检查 | 章节风格 vs `style/compiled/` 是否漂移 | warning |
| 9 | 信息越界 | 角色是否提及他不应该知道的信息（POV 限制 / 信息差） | critical |
| 10 | 词汇疲劳 | 跨章节疲劳词重复（vs genre fatigue words） | warning |
| 11 | 利益链断裂 | 角色动机是否可信（vs 角色卡的 motivations） | warning |
| 12 | 年代考据 | 仅当 story.md 有 era constraints 时启用 | warning / critical |
| 13 | 配角降智 | 配角是否为剧情需要"突然变笨" | warning |
| 14 | 配角工具人化 | 配角是否只为推进主角而存在，无独立目标 | info |
| 15 | 爽点虚化 | 兑现的爽点是否真的爽（vs 30 章承诺累积的期待） | warning |
| 16 | 台词失真 | 对话是否符合角色 voice patterns（vs `voice-patterns.md`） | warning |
| 17 | 流水账 | 是否纯水日常（无功能性）| warning |

## B 组 - Python 脚本统计学（4 维）

由 `check_ai_tells.py` 实现。

| ID | 名称 | 算法 | severity |
|---|---|---|---|
| 20 | 段落等长 | 变异系数 < 0.15 | warning |
| 21 | 套话密度 | hedge words 密度 > 3/千字 | warning |
| 22 | 公式化转折 | 同转折词重复 ≥ 3 次 | warning |
| 23 | 列表式结构 | 连续 ≥ 3 句相同开头 | info |

## C 组 - LLM 评估，高级一致性（5 维）

| ID | 名称 | 检查方法 |
|---|---|---|
| 19 | POV 一致性 | 是否在章中无标记切换视角 |
| 24 | 支线停滞 | 支线伏笔长期不推进（vs `plot/arcs/{subplot}.md`） |
| 25 | 弧线平坦 | 角色情绪线是否在一段时间内同种压力（vs `.memory/`） |
| 26 | 节奏单调 | 近 5 章是否都同一种章节类型 |
| 27 | 敏感词检查 | 政治 / 色情 / 暴力 敏感词（按平台规则） |

## D 组 - LLM 评估，通用强制（2 维）

| ID | 名称 | 总是开启 |
|---|---|---|
| 32 | 读者期待管理 | 是否兑现了之前章节的承诺；是否累积新期待 |
| 33 | 章节备忘偏离 | 实际写作 vs 章纲承诺是否偏离 |

## E 组 - 续作 / 番外专用（4 维，仅当 vault 有 parent_canon.md 时开启）

| ID | 名称 |
|---|---|
| 28 | 正传事件冲突 |
| 29 | 未来信息泄露 |
| 30 | 跨书规则一致性 |
| 31 | 番外伏笔越权 |

## F 组 - 同人专用（4 维，仅 fanfic 模式开启）

| ID | 名称 |
|---|---|
| 34 | 角色还原度（vs canon） |
| 35 | 世界规则遵守 |
| 36 | 关系动态合理性 |
| 37 | 正典事件一致性 |

---

## 评分校准（overall_score 0-100）

直接抄 inkos：

| 分数 | 含义 |
|---|---|
| 95-100 | 可直接发表 |
| 85-94 | 小瑕疵但顺畅，读者不会出戏 |
| 75-84 | 明显问题但骨架稳，需修订但不紧急 |
| 65-74 | 多处问题影响阅读，节奏 / 连贯性有缺口 |
| < 65 | 结构崩坏，需大改 |

整体评分：不要因为单个小问题就扣很多分。

## passed 判定

`passed = false` 仅当存在 **critical** issue。

warning / info 不影响 passed，仅作记录。

## 启用配置

在 vault 的 `story.md` 顶层可添加：

```yaml
audit-config:
  always-active: [1, 2, 3, 6, 7, 17, 32, 33]   # 永远开启的维度
  disabled: [12]                                # 显式关闭的维度
  fanfic-mode: false                            # 是否启用同人维度
  has-parent-canon: false                       # 是否启用续作维度
  custom-additions: []                          # 自定义额外维度
```

v0.1 不强制读这个配置（所有 A+B+D 默认开启），v0.2 加入配置生效。
