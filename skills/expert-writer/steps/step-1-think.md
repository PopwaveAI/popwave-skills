# step-1-think.md — 状态感知 + 意图识别 + 智能调度

> **读什么**：项目总控.md + expert-writer SKILL.md（门禁表）
> **产出什么**：当前阶段判断 + 路由目标
> **闸门**：每次新会话必须执行本步（除非用户已明确指令）

---

## ❌ 读取协议（强制）

```
工具选择：skill_view（首选）或 Get-Content -Encoding UTF8 -Raw
❌ 禁止用 Read 工具读取 skill 文件（有行数限制，会截断）
✅ 目标子 skill SKILL.md 必须先完整读取再路由（红线2）
```

---

## 1. 管线锚定（v3.5）

### v3.5 管线顺序

```
种子设计(pop-writer-v3-seed) → L2卡设计(pop-writer-v3-plot) → 涌现写作环(expert-writer 5步循环) ↔ 弧线校准(pop-writer-v3-arc)
                                                            ↑ 按需：pop-research
```

> emerge 已废弃：5步循环由 expert-writer 主会话直接执行，不再作为独立环节引用。

### 管线阶段判断

读取 `项目总控.md`，检查：

| 条件 | 当前阶段 | 路由到 |
|:-----|:---------|:-------|
| 项目总控不存在 | 未初始化 | `step-0-init.md`（项目初始化） |
| `卷纲/L2-NNN-名称.md` 不存在 | 种子设计 | **pop-writer-v3-seed** |
| L2卡已产出，`正文/ch001.md` 不存在 | L2卡设计 | **pop-writer-v3-plot** |
| L2卡已产出，`正文/` 有文件，但L2单元未写完 | 涌现写作 | **expert-writer 5步循环**（本skill Execute阶段） |
| L2单元最后一章 Step5 完成 | 弧线校准 | **pop-writer-v3-arc** |
| 用户说"回滚" | 回退 | `step-2-execute.md` §3.2 |
| 用户说"调研/查资料" | 按需调研 | **pop-research**（按需调用） |

> **关键变化**：
> - 原判断"种子文档是否存在"→ 改为"L2卡是否存在"
> - 原判断"种子文档任务表"→ 改为"L2卡嵌套子线"
> - emerge 判断取消 → expert-writer 直接执行5步循环
> - arc 触发：不再等"每10-20章"→ 每个 L2 单元结束时触发

---

## 2. 意图识别

用户说的话 → 意图：

| 用户说 | 意图 | 路由 |
|:-------|:-----|:-----|
| "继续"/"下一步"/"写第X章" | 涌现写作继续 | Execute阶段→5步循环 |
| "开新书"/"启动项目" | 项目初始化 | step-0-init.md |
| "设计剧情"/"L2卡" | L2卡设计 | pop-writer-v3-plot |
| "检查"/"审稿"/"弧线校准" | 弧线校准 | pop-writer-v3-arc |
| "回滚到第N章" | 回退 | step-2-execute.md §3.2 |
| "调研"/"查资料" | 按需调研 | pop-research |
| "拆这本书"/"分析" | 拆书 | pop-decon |

---

## 3. 前置校验

路由到 **5步循环** 之前，检查：

1. **L2卡存在**：`卷纲/L2-NNN-名称.md` 存在？
   - 不存在 → 路由到 pop-writer-v3-plot
   - 存在 → 继续

2. **活记忆存在**：`活记忆/活记忆.yaml` 存在？
   - 不存在 → 报错（项目初始化不完整）
   - 存在 → 继续

3. **文风DNA存在**：`写作资产/文风库/{书名}.md` 存在？
   - 不存在 → 提示用户（文风DNA缺失，revise阶段无法消费）
   - 存在 → 继续

4. **写作参考索引存在**：`写作参考/索引.md` 存在？
   - 不存在 → 报错（Step2信息获取无入口）
   - 存在 → 继续

---

## 4. 路由到 Execute

前置校验通过 → 进入 `step-2-execute.md`（5步循环执行流程）

> **不读子 SKILL.md 就路由 = 红线2违规。**
> 路由到子skill（pop-writer-v3-create / pop-writer-v3-revise）之前，必须先 `Get-Content -Encoding UTF8 -Raw` 读取目标子skill完整 SKILL.md。
