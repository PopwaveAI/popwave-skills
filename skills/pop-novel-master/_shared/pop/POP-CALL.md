# POP-CALL.md — pop 编排声明模板

> pop 已升级为 **Harness 编排层**。收到需求后：
> 1. 调 `glue/orchestrate.py` 自动匹配路由
> 2. dispatcher.py 解析 frontmatter + 前置检查 + 装配上下文
> 3. 输出 JobOrder 任务单
> 4. pop agent 按 JobOrder 执行 skill SOP

---

## 声明格式（标准版）

```
🖋️ **pop 收到老板指示**

任务理解：[一句话复述用户需求]
场景判断：[bootstrap / plot / writing / deconstruct / qa / market]
路由技能：[skill-name vX.X | 推荐排序 N]
前置条件：[依赖项 → ✅/❌]
执行路径：[step1 → step2 → ...]
```

---

## 声明格式（简洁版 — 用于快速确认）

```
🖋️ **pop 收到老板指示」

任务理解：xxx
执行路线：skill-emergent-writer v8.0
```

---

## 路由表（详见 POP-ROUTER.md）

| 用户输入关键词 | 路由 skill |
|:---|:---|
| 开书 / 新书 / 设计设定 | skill-project-bootstrap |
| 幕纲 / 大纲 / 剧情 | pop-novel-plot |
| 前三章 / 开篇 | pop-novel-writer（黄金三章模式） |
| 写第N章 / 正文 | skill-emergent-writer |
| 拆书 / 解构 / 分析 | skill-book-deconstructor |
| 审稿 / QA / 质检 | skill-qa-payoff |
| 市场验证 | skill-market-test |
| 续写 / 交接 | _continuation |
| 调研 / 搜索 | cnovel-research-main |

---

## 场景示例

### 示例 1：写作任务
```
🖋️ **pop 收到老板指示**

任务理解：写第 5 章正文
场景判断：writing → production
路由技能：skill-emergent-writer v8.0（推荐排序 1）
前置条件：act-XX.yaml → ✅ / global_summary → ✅ / character_state → ✅
执行路径：pre_flight → 导演思考 → 正文生成 → post_write → 更新摘要
```

### 示例 2：大纲任务
```
🖋️ **pop 收到老板指示**

任务理解：设计第二幕（act-02）的幕纲
场景判断：plot → design
路由技能：pop-novel-plot v2.7（推荐排序 2）
前置条件：project.yaml → ✅ / PRD → ✅ / L1 → ✅
执行路径：check_db → 情绪曲线 → 爽点版场景卡 → validate
```

### 示例 3：拆书任务
```
🖋️ **pop 收到老板指示**

任务理解：拆解《诡舍》第 11-50 章
场景判断：deconstruct → research
路由技能：skill-book-deconstructor v4.7（推荐排序 3）
前置条件：参考书原文 → ✅
执行路径：节点E判断 → 选模式 → 拆解 → 片段入库
```

### 示例 4：审稿任务
```
🖋️ **pop 收到老板指示**

任务理解：审稿第 5 章
场景判断：qa → review
路由技能：skill-qa-payoff v0.3（推荐排序 6）
前置条件：正文 ch005.md → ✅
执行路径：意图还原 → 7维评分 → QA报告
```

---

## 编排纪律

1. **pop 声明是强制前置信令** — 每次新任务必须声明
2. **声明后查 POP-ROUTER.md** — 按路由表走，不自由发挥
3. **HARD-GATE 最高优先** — 前置条件不满足就不执行
4. **glue 脚本不可跳过** — pre_flight / check_db / validate / post_write
5. **子Agent 隔离** — 正文/审稿必须走独立子Agent

---

> 此文件为 pop 声明基准。变更时同步更新 POP-ROUTER.md 和各 SKILL.md。
