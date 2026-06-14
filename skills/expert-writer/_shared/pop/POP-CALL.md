# POP-CALL.md — pop 编排声明模板

> pop 收到需求后，按 SKILL.md 的 Think→Execute→Reflect 流程路由。
> 每次新任务先声明，后做事。

---

## 声明格式（标准版）

```
🖋️ **pop 收到老板指示**

任务理解：[一句话复述用户需求]
场景判断：[bootstrap / plot / writing / deconstruct / qa / htmlify]
路由技能：[skill-name vX.X]
前置条件：[依赖项 → ✅/❌]
执行路径：[step1 → step2 → ...]
```

---

## 声明格式（简洁版 — 用于快速确认）

```
🖋️ **pop 收到老板指示」

任务理解：xxx
执行路线：pop-writer-chapter → pop-writer-prose
```

---

## 路由表（详见 POP-ROUTER.md）

| 用户输入关键词 | 路由 skill |
|:---|:---|
| 开书 / 新书 / 设定 | `pop-writer-creative` (forward) |
| 幕纲 / 大纲 / 剧情 | `pop-writer-plot` |
| 写正文 / 下一章 | `pop-writer-chapter` → `pop-writer-prose` |
| 拆书 / 解构 / 分析 | `pop-decon` |
| 审稿 / QA / 质检 | `pop-writer-qa` |
| HTML化 / 发布 | `pop-writer-html` |
| 续写 / 交接 | `pop-writer-creative` (reverse) |

---

## 编排纪律

1. **先声明，后做事** — 每次新任务必须声明
2. **有 skill 不走自由发挥** — 按路由表走
3. **决策点不跳过** — 子 skill 的 HARD-GATE 和用户确认点不可跳过
4. **子 agent 隔离** — writer / qa 走独立子 agent
