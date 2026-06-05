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
执行路线：pop-novel-writer
```

---

## 路由表（详见 POP-ROUTER.md）

| 用户输入关键词 | 路由 skill |
|:---|:---|
| 开书 / 新书 / 设定 | `pop-novel-bootstrap` (forward) |
| 幕纲 / 大纲 / 剧情 | `pop-novel-plot` |
| 写正文 / 下一章 | `pop-novel-writer` |
| 前三章 / 开篇 | `pop-novel-writer`（黄金三章模式） |
| 拆书 / 解构 / 分析 | `pop-novel-deconstructor` |
| 审稿 / QA / 质检 | `pop-novel-qa` |
| HTML化 / 发布 | `pop-novel-html-renderer` |
| 续写 / 交接 | `pop-novel-bootstrap` (reverse) |

---

## 场景示例

### 示例 1：开书任务
```
🖋️ **pop 收到老板指示**

任务理解：写一本灰骑士穿越博德之门3的小说
场景判断：bootstrap → design
路由技能：pop-novel-bootstrap v3.0（forward）
前置条件：用户有故事想象 → ✅
执行路径：追问2-3轮 → story-engine.yaml → 参考书甄别 → L1设定 → 项目骨架
```

### 示例 2：写作任务
```
🖋️ **pop 收到老板指示**

任务理解：写第 5 章正文
场景判断：writing → production
路由技能：pop-novel-writer v11
前置条件：act-XX.yaml → ✅ / 章状态 → ✅
执行路径：Director 思考 → 骨架 → ESM → 渲染 → QC
```

### 示例 3：大纲任务
```
🖋️ **pop 收到老板指示**

任务理解：设计第二幕的幕纲
场景判断：plot → design
路由技能：pop-novel-plot v3.1
前置条件：project.yaml → ✅ / story-engine.yaml → ✅ / L1 → ✅
执行路径：节点B → 情节线草案 → 场景卡 → 节奏自检 → 输出
```

### 示例 4：续写任务
```
🖋️ **pop 收到老板指示**

任务理解：继续写之前搁置的书
场景判断：continuation → reverse
路由技能：pop-novel-bootstrap v3.0（reverse）
前置条件：已有正文 → ✅
执行路径：事件日志 → 逆向 story-engine → 逆向 L1 → 宪法提取 → 卷大纲确认
```

---

## 编排纪律

1. **先声明，后做事** — 每次新任务必须声明
2. **有 skill 不走自由发挥** — 按路由表走
3. **决策点不跳过** — 子 skill 的 HARD-GATE 和用户确认点不可跳过
4. **子 agent 隔离** — writer / qa 走独立子 agent
