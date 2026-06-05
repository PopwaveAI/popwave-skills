# POP-ROUTER.md — pop 编排路由表

> pop 收到需求后，根据用户意图通过路由表匹配子 skill。
> 本文件为静态参考。实际路由在 SKILL.md 中由 pop agent 根据 Think→Execute 流程执行。

---

## 一、路由总表

| 用户意图 | 路由 skill | 前置条件 | 产出 |
|:---------|:-----------|:---------|:-----|
| 新书启动 / 开书 / 设世界观 | `pop-novel-bootstrap` (forward) | 一个故事想象 | story-engine.yaml + L1 设定 + 宪法 + 数值体系 |
| 设计幕纲 / 剧情架构 | `pop-novel-plot` | project.yaml + story-engine.yaml + L1 设定 | act-XX.yaml + 情节线纲汇总表 |
| 写正文 / 下一章 | `pop-novel-writer` | act-XX.yaml + L1 设定 + 宪法 + 章状态 | chXXX.md |
| 拆书 / 分析参考书 | `pop-novel-deconstructor` | 参考书原文 | 模式分析报告 |
| 审稿 / QA / 质检 | `pop-novel-qa` | 正文 MD | QA 报告 |
| HTML化 / 发布 | `pop-novel-html-renderer` | 任意文档 | 可视化 HTML |
| 续写 / 交接已有项目 | `pop-novel-bootstrap` (reverse) | 已有正文 | event logs + 逆向 L1 + 宪法 |
| 开篇 / 黄金三章 | `pop-novel-writer` (已内置黄金三章模式) | L0 设定 | ch001-ch003.md |

---

## 二、工作流（Think → Execute → Reflect，全在 SKILL.md 中定义）

master 不依赖外部编排脚本。每次收到用户任务：

```
① Think（加载对应 reference/think-*.md 审视框架）
    ↓
② 前置条件确认 + 需求质量检查
    ↓
③ Execute（按路由表定向到子 skill，组装上下文）
    ↓
    ┌─ 子 skill 执行中有"人必须在场的决策点"→ 主动拦截，等用户确认
    ↓
④ Reflect（四层审视：产出→一致性→QA→活人感）
```

### 关键规则

1. **有 skill 不走自由发挥** — 所有创作任务先路由到对应子 skill
2. **不跳过 HARD-GATE** — 每个子 skill 的质量红线不可跳过
3. **上下文隔离** — writer / qa 走子 agent 执行，不继承主对话历史
4. **异常先告知用户** — 前置条件不满足时告知用户，不静默跳过

---

## 三、关键词 → 路由映射

| 用户输入包含 | 路由 skill |
|:---|:---|
| 开书 / 启动 / 新书 / 设定 | `pop-novel-bootstrap` (forward) |
| 幕纲 / 大纲 / 剧情 / 架构 | `pop-novel-plot` |
| 写 / 正文 / 第N章 / 下一章 | `pop-novel-writer` |
| 前三章 / 开篇 / 黄金三章 | `pop-novel-writer` (黄金三章模式) |
| 拆书 / 解构 / 分析 / 对标 | `pop-novel-deconstructor` |
| 审稿 / QA / 质检 / 审一下 | `pop-novel-qa` |
| HTML化 / 发布 / 渲染 | `pop-novel-html-renderer` |
| 续写 / 交接 / 已有正文 | `pop-novel-bootstrap` (reverse) |

> 关键词匹配优先级：精确匹配 > 部分匹配。
> 如果多个 skill 匹配 → 选依赖关系最少的（bootstrap → plot → writer 天然顺序）。

---

## 四、路由纪律

1. **前置条件检查** — 路由前确认依赖文件存在。不存在则先走上游 skill 或告知用户
2. **子 agent 隔离** — writer / qa 走独立子 agent，不继承主对话历史
3. **离场不干扰** — master 不接管子 skill 的具体执行细节，只拦截决策点
